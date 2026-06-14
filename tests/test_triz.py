#!/usr/bin/env python3
"""
Pytest-compatible TRIZ test suite — also runnable with plain Python (unittest).

Usage:
    pytest tests/test_triz.py          # if pytest installed
    python tests/test_triz.py          # plain unittest runner
"""

import sys
import os
import json
import unittest
import tempfile
import re
from pathlib import Path

# ---- path setup: add the scripts directory so imports work ----
_SCRIPTS_DIR = (
    Path(__file__).resolve().parent.parent
    / ".claude" / "skills" / "triz-innovation" / "scripts"
)
sys.path.insert(0, str(_SCRIPTS_DIR))

import triz_matrix
import triz_router
import triz_evaluator
import triz_standard_solutions
import triz_evolution
import triz_ariz
import triz_case_template


class TestTRIZ(unittest.TestCase):
    """TRIZ skill test suite — matrix, router, evaluator, standard-solutions,
    evolution, ARIZ, case-template, and effects."""

    # ── Matrix tests ────────────────────────────────────────────────────────

    def test_matrix_lookup_valid(self):
        """matrix[14, 2] returns a list of inventive principles."""
        result = triz_matrix.lookup(14, 2)
        self.assertEqual(result["improving"]["id"], 14)
        self.assertEqual(result["worsening"]["id"], 2)
        self.assertIsInstance(result["principles"], list)
        self.assertGreater(len(result["principles"]), 0,
                           "Expected at least one principle for (14, 2)")
        for p in result["principles"]:
            self.assertIn("id", p)
            self.assertIn("name", p)
            self.assertIsInstance(p["id"], int)
            self.assertIsInstance(p["name"], str)
            self.assertGreater(len(p["name"]), 0)

    def test_matrix_diagonal(self):
        """Diagonal query (same id both sides) returns empty principles and
        a note mentioning a physical contradiction."""
        result = triz_matrix.lookup(10, 10)
        self.assertEqual(result["principles"], [],
                         "Diagonal query should return empty principles")
        self.assertIsNotNone(result["note"])
        self.assertIn("physical", result["note"].lower(),
                      "Diagonal note should mention physical contradiction")

    def test_matrix_invalid_id(self):
        """id=0 and id=40 both raise ValueError."""
        bad_calls = [
            (0, 5),
            (5, 0),
            (40, 5),
            (5, 40),
            (1, 40),
            (40, 1),
        ]
        for improving, worsening in bad_calls:
            with self.subTest(improving=improving, worsening=worsening):
                with self.assertRaises(ValueError):
                    triz_matrix.lookup(improving, worsening)

    def test_matrix_all_cells(self):
        """All 1248 populated matrix cells return non-empty principle lists."""
        matrix = triz_matrix.load_matrix()
        populated = [(k, v) for k, v in matrix.items() if v]
        self.assertEqual(
            len(populated), 1248,
            f"Expected 1248 populated cells, got {len(populated)}"
        )
        for key, val in populated:
            with self.subTest(improving=key[0], worsening=key[1]):
                self.assertIsInstance(val, list)
                self.assertGreater(len(val), 0,
                                   f"Cell {key} has empty principles list")
                for pid in val:
                    self.assertIsInstance(pid, int)
                    self.assertGreaterEqual(pid, 1)
                    self.assertLessEqual(pid, 40)

    # ── Parameters & Principles count ───────────────────────────────────────

    def test_parameters_count(self):
        """39 parameters load, with ids 1..39 and non-empty names."""
        params = triz_matrix.load_parameters()
        self.assertEqual(len(params), 39)
        for i in range(1, 40):
            with self.subTest(param_id=i):
                self.assertIn(i, params)
                self.assertIsInstance(params[i], str)
                self.assertGreater(len(params[i].strip()), 0)

    def test_principles_count(self):
        """40 inventive principles load, with ids 1..40 and non-empty names."""
        principles = triz_matrix.load_principles()
        self.assertEqual(len(principles), 40)
        for i in range(1, 41):
            with self.subTest(principle_id=i):
                self.assertIn(i, principles)
                self.assertIsInstance(principles[i], str)
                self.assertGreater(len(principles[i].strip()), 0)

    # ── Router tests ────────────────────────────────────────────────────────

    def test_router_english_contradiction(self):
        """'more speed but less reliability' detects an engineering
        contradiction via connector + keyword match."""
        result = triz_router.suggest_methods(
            "more speed but less reliability"
        )
        self.assertIsNotNone(
            result["engineering_contradiction"],
            "Should detect engineering contradiction from trade-off language"
        )
        methods = [m["method"] for m in result["methods"]]
        self.assertTrue(
            any("Engineering Contradiction" in m for m in methods),
            f"Expected Engineering Contradiction in methods, got {methods}"
        )

    def test_router_physical_contradiction(self):
        """'must be present and absent' detects a physical contradiction."""
        result = triz_router.suggest_methods(
            "the element must be present and absent"
        )
        self.assertIsNotNone(
            result["physical_contradiction"],
            "Should detect physical contradiction from paired opposites"
        )
        methods = [m["method"] for m in result["methods"]]
        self.assertTrue(
            any("Physical Contradiction" in m for m in methods),
            f"Expected Physical Contradiction in methods, got {methods}"
        )

    def test_router_default_fallback(self):
        """Empty text returns the 5 default fallback methods with score=0."""
        result = triz_router.suggest_methods("")
        self.assertIsNone(result["engineering_contradiction"])
        self.assertIsNone(result["physical_contradiction"])
        methods = result["methods"]
        self.assertEqual(len(methods), 5,
                         "Empty input should return 5 default fallback methods")
        for m in methods:
            with self.subTest(method=m["method"]):
                self.assertEqual(m["score"], 0)
                self.assertIn("default fallback", m["why"])

    # ── Evaluator tests ─────────────────────────────────────────────────────

    def test_evaluator_scoring(self):
        """Scoring works, including through CSV parse with renamed/mixed-case
        columns."""
        # Build a temp CSV with mixed-case column names
        csv_content = (
            "Solution,Impact,FEASIBILITY,affordability,Speed,"
            "Safety,Reversibility,Simplicity,Ideality\n"
            "TestA,4,3,2,1,5,4,3,2\n"
            "TestB,1,1,1,1,1,1,1,1\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = Path(tmpdir) / "test_solutions.csv"
            csv_path.write_text(csv_content, encoding="utf-8")

            rows = triz_evaluator._parse_csv(str(csv_path))
            self.assertEqual(len(rows), 2)

            scored = triz_evaluator.score(rows)
            self.assertEqual(len(scored), 2)

            # TestA: 4+3+2+1+5+4+3+2 = 24
            self.assertEqual(scored[0]["solution"], "TestA")
            self.assertEqual(scored[0]["total"], 24)

            # TestB: 1*8 = 8
            self.assertEqual(scored[1]["solution"], "TestB")
            self.assertEqual(scored[1]["total"], 8)

            # Verify all eight criteria keys are lowercased and present
            for crit in triz_evaluator.CRITERIA:
                self.assertIn(crit, scored[0],
                              f"Missing criterion '{crit}' after CSV parse")

    def test_evaluator_sorting(self):
        """Highest total sorts first (descending order)."""
        rows = [
            {
                "solution": "Low",
                "impact": 1, "feasibility": 1, "affordability": 1,
                "speed": 1, "safety": 1, "reversibility": 1,
                "simplicity": 1, "ideality": 1,
            },
            {
                "solution": "High",
                "impact": 5, "feasibility": 5, "affordability": 5,
                "speed": 5, "safety": 5, "reversibility": 5,
                "simplicity": 5, "ideality": 5,
            },
            {
                "solution": "Mid",
                "impact": 3, "feasibility": 3, "affordability": 3,
                "speed": 3, "safety": 3, "reversibility": 3,
                "simplicity": 3, "ideality": 3,
            },
        ]
        scored = triz_evaluator.score(rows)
        self.assertEqual(scored[0]["solution"], "High")
        self.assertEqual(scored[1]["solution"], "Mid")
        self.assertEqual(scored[2]["solution"], "Low")
        self.assertGreater(scored[0]["total"], scored[1]["total"])
        self.assertGreater(scored[1]["total"], scored[2]["total"])

    # ── Standard Solutions tests ────────────────────────────────────────────

    def test_standard_solutions_valid_state(self):
        """'harmful' state returns Class 1 with a matching name."""
        result = triz_standard_solutions.recommend("harmful")
        self.assertEqual(result["state"], "harmful")
        self.assertGreater(len(result["classes"]), 0)
        cls0 = result["classes"][0]
        self.assertEqual(cls0["class"], 1)
        self.assertIn("harmful", cls0["name"].lower())
        self.assertIsNotNone(result["note"])

    def test_standard_solutions_invalid_state(self):
        """Unknown state raises ValueError."""
        with self.assertRaises(ValueError):
            triz_standard_solutions.recommend("nonexistent_state_xyz")

    # ── Evolution tests ─────────────────────────────────────────────────────

    def test_evolution_growth_signals(self):
        """'rapid scaling adoption' classifies as Growth (stage 2)."""
        result = triz_evolution.analyze("rapid scaling adoption")
        self.assertEqual(result["s_curve_stage"]["name"], "Growth")
        self.assertEqual(result["s_curve_stage"]["stage"], 2)
        self.assertIn("scaling", result["s_curve_stage"]["why"].lower())
        # Always returns 8 trend prompts
        self.assertEqual(len(result["trends"]), 8)

    def test_evolution_maturity_signals(self):
        """'diminishing returns plateau' classifies as Maturity (stage 3)."""
        result = triz_evolution.analyze("diminishing returns plateau")
        self.assertEqual(result["s_curve_stage"]["name"], "Maturity")
        self.assertEqual(result["s_curve_stage"]["stage"], 3)
        self.assertIn("diminishing returns", result["s_curve_stage"]["why"].lower())

    # ── ARIZ tests ──────────────────────────────────────────────────────────

    def test_ariz_worksheet_creation(self):
        """create_worksheet produces a file with exactly 9 ARIZ parts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = triz_ariz.create_worksheet("Test ARIZ Problem", cases_dir=tmpdir)
            self.assertTrue(path.exists(), f"ARIZ worksheet not created at {path}")
            content = path.read_text(encoding="utf-8")
            parts = re.findall(r"^## Part \d", content, re.MULTILINE)
            self.assertEqual(len(parts), 9,
                             f"Expected 9 ARIZ parts, found {len(parts)}")
            # Verify the title is present
            self.assertIn("Test ARIZ Problem", content)

    # ── Case Template tests ─────────────────────────────────────────────────

    def test_case_template_creation(self):
        """create_case produces a file using the actual template."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = triz_case_template.create_case("My Test Case", cases_dir=tmpdir)
            self.assertTrue(path.exists(), f"Case file not created at {path}")
            content = path.read_text(encoding="utf-8")
            self.assertIn("My Test Case", content,
                          "Case file should contain the problem title")

    # ── Effects database tests ──────────────────────────────────────────────

    def test_effects_search(self):
        """Scientific effects database loads, each entry has required fields,
        and search by name works."""
        effects_path = _SCRIPTS_DIR / "data" / "scientific_effects.json"
        self.assertTrue(effects_path.exists(),
                        f"Effects database not found at {effects_path}")

        with open(effects_path, "r", encoding="utf-8") as fh:
            effects = json.load(fh)

        self.assertIsInstance(effects, list)
        self.assertGreater(len(effects), 0,
                           "Effects database should not be empty")

        required_fields = {"effect_name", "function_family", "domain"}
        for i, entry in enumerate(effects):
            with self.subTest(entry_index=i):
                for field in required_fields:
                    self.assertIn(field, entry,
                                  f"Entry {i} missing field '{field}'")

        # Search for a specific known effect
        matches = [
            e for e in effects
            if "capillarity" in e.get("effect_name", "").lower()
        ]
        self.assertGreater(len(matches), 0,
                           "Should find at least one 'Capillarity' effect")

        capillarity = matches[0]
        self.assertIn("mechanism", capillarity)
        self.assertIn("resources_needed", capillarity)
        self.assertIn("examples", capillarity)
        self.assertIsInstance(capillarity["resources_needed"], list)
        self.assertIsInstance(capillarity["examples"], list)


if __name__ == "__main__":
    unittest.main()
