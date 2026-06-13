#!/usr/bin/env python3
"""
TRIZ Su-Field → 76 Standard Solutions class recommender.

Rule-based recommender that maps a Su-Field state (incomplete, insufficient,
harmful, measurement, excessive) to the matching standard-solution classes
with concrete candidate moves.

Usage:
    python triz_standard_solutions.py --state <state>
    python triz_standard_solutions.py --list
    python triz_standard_solutions.py          # print usage

Standard library only — Python 3.8+.
"""

import sys
from typing import Any

# ── State → classes → moves table ──────────────────────────────────────────────
# Single readable table near the top — extend it here.
# Each state key maps to a "synonyms" list (for input flexibility) and "classes"
# list.  Each class entry has "class" (int), "name" (str), and "moves" (list[str]).
# Consistent with references/substance-field-analysis.md.

_STATE_TABLE: dict[str, dict[str, Any]] = {
    "incomplete": {
        "synonyms": ["missing"],
        "classes": [
            {
                "class": 1,
                "name": "Class 1 — Build or complete a Su-Field",
                "moves": [
                    "Add the missing field F between S1 and S2 to complete "
                    "the interaction",
                    "Add the missing substance S2 that the tool should act on",
                    "Introduce an external additive to supply the missing "
                    "component (substance or field)",
                    "Use the environment itself as the missing substance or field",
                ],
            },
        ],
        "note": (
            "See references/substance-field-analysis.md — "
            "Class 1: complete an incomplete Su-Field (add the missing "
            "substance or field)."
        ),
    },
    "insufficient": {
        "synonyms": ["weak"],
        "classes": [
            {
                "class": 2,
                "name": "Class 2 — Develop / enhance the Su-Field",
                "moves": [
                    "Chain Su-Fields — add a second field and a third "
                    "substance S3 to boost the effect",
                    "Upgrade the field toward a more controllable form "
                    "(mechanical -> acoustic -> thermal -> chemical -> "
                    "electric -> magnetic -> electromagnetic)",
                    "Fragment substances to increase surface area and "
                    "interaction intensity (solid -> powder -> liquid -> "
                    "gas -> field)",
                    "Make the field dynamic — pulse it, match the natural "
                    "frequency, or create a standing wave or gradient",
                ],
            },
        ],
        "note": (
            "See references/substance-field-analysis.md — "
            "Class 2: strengthen a weak Su-Field (chain, upgrade field, "
            "fragment, make dynamic)."
        ),
    },
    "harmful": {
        "synonyms": [],
        "classes": [
            {
                "class": 1,
                "name": "Class 1 — Eliminate or block the harmful interaction",
                "moves": [
                    "Block the harmful field — insert a barrier substance "
                    "S3 between S1 and S2",
                    "Add a third substance S3 that absorbs or neutralizes "
                    "the harmful field",
                    "Redirect the harmful action onto a sacrificial element "
                    "that is cheap or easy to replace",
                    "Introduce a counter-field F2 that cancels or opposes "
                    "the harmful field F1",
                ],
            },
        ],
        "note": (
            "See references/substance-field-analysis.md — "
            "Class 1: block, absorb, or redirect harmful interactions."
        ),
    },
    "measurement": {
        "synonyms": ["detection"],
        "classes": [
            {
                "class": 4,
                "name": "Class 4 — Detection & measurement Su-Fields",
                "moves": [
                    "Generate a field that varies with the property to be "
                    "measured",
                    "Add an easily detectable additive (tag, tracer, marker) "
                    "to the substance",
                    "Use a resonant system — match the natural frequency to "
                    "amplify the measurement signal",
                    "Transform the measurement problem into a simpler "
                    "detection problem (go/no-go instead of a continuous scale)",
                ],
            },
        ],
        "note": (
            "See references/substance-field-analysis.md — "
            "Class 4: measurement and detection Su-Fields."
        ),
    },
    "excessive": {
        "synonyms": ["complex"],
        "classes": [
            {
                "class": 5,
                "name": "Class 5 — Simplification & helpers",
                "moves": [
                    "Trim a component — remove a substance or field and "
                    "transfer its function to another element already in "
                    "the system",
                    "Apply self-X (self-service, self-organization) — let "
                    "the system regulate or act on itself",
                    "Use voids, bubbles, foams, or field-generated "
                    "structures instead of added solid matter",
                    "Break the excessive field into smaller, independently "
                    "controllable sub-fields",
                ],
            },
        ],
        "note": (
            "See references/substance-field-analysis.md — "
            "Class 5 + Trimming: simplify, restructure, or use cheap/self-"
            "eliminating helpers."
        ),
    },
}

# Build a reverse index: synonym → canonical state name
_SYNONYM_MAP: dict[str, str] = {}
for _canonical, _entry in _STATE_TABLE.items():
    _SYNONYM_MAP[_canonical] = _canonical
    for _syn in _entry.get("synonyms", []):
        _SYNONYM_MAP[_syn] = _canonical

_VALID_STATES = sorted(_STATE_TABLE.keys())


def recommend(state: str) -> dict[str, Any]:
    """Recommend standard-solution classes for a Su-Field state.

    Args:
        state: One of "incomplete" ("missing"), "insufficient" ("weak"),
               "harmful", "measurement" ("detection"), "excessive" ("complex").
               Case-insensitive.

    Returns:
        dict with keys:
        - "state": normalized canonical state name.
        - "classes": list of {"class": int, "name": str, "moves": [str, ...]}.
        - "note": str or None.

    Raises:
        ValueError: if the state is not recognised.
    """
    normalized = state.lower().strip()
    canonical = _SYNONYM_MAP.get(normalized)
    if canonical is None:
        raise ValueError(
            f"Unknown Su-Field state '{state}'. "
            f"Valid states: {', '.join(_VALID_STATES)}."
        )
    entry = _STATE_TABLE[canonical]
    return {
        "state": canonical,
        "classes": entry["classes"],
        "note": entry["note"],
    }


# ── CLI ────────────────────────────────────────────────────────────────────────

def _print_usage() -> None:
    """Print usage and the list of valid states."""
    print("Usage: python triz_standard_solutions.py --state <state>", file=sys.stderr)
    print("       python triz_standard_solutions.py --list", file=sys.stderr)
    print(file=sys.stderr)
    print("Valid states:", file=sys.stderr)
    for s in _VALID_STATES:
        entry = _STATE_TABLE[s]
        synonyms = entry.get("synonyms", [])
        if synonyms:
            syn_str = f"  (also: {', '.join(synonyms)})"
        else:
            syn_str = ""
        print(f"  {s}{syn_str}", file=sys.stderr)


def _print_list() -> None:
    """Print the 5 valid states with a one-line gloss."""
    glosses = {
        "incomplete": "A needed substance or field is missing — the function cannot happen.",
        "insufficient": "The interaction exists but is too weak to deliver the required function.",
        "harmful": "An unwanted or damaging action accompanies the useful one.",
        "measurement": "You need to detect or measure a property but cannot do so reliably.",
        "excessive": "The system works but is too costly, complex, or over-engineered.",
    }
    for s in _VALID_STATES:
        print(f"  {s:<14} — {glosses.get(s, '')}")


def main() -> None:
    if len(sys.argv) < 2:
        _print_usage()
        sys.exit(1)

    if sys.argv[1] == "--list":
        _print_list()
        return

    if sys.argv[1] != "--state":
        _print_usage()
        sys.exit(1)

    if len(sys.argv) < 3:
        _print_usage()
        sys.exit(1)

    state = sys.argv[2]

    try:
        result = recommend(state)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Su-Field state: {result['state']}")
    print()
    for cls in result["classes"]:
        print(f"  {cls['name']}")
        for i, move in enumerate(cls["moves"], 1):
            print(f"    {i}. {move}")
        print()

    if result["note"]:
        print(f"Note: {result['note']}")


if __name__ == "__main__":
    main()
