#!/usr/bin/env python3
"""
TRIZ solution evaluator — scores candidate solutions 1–5 on eight criteria
and produces a sorted monospaced table.

Usage:
    python triz_evaluator.py solutions.csv   # read CSV, print sorted table
    python triz_evaluator.py                 # demo mode with built-in sample
    python triz_evaluator.py --help          # print CSV format

CSV header (exact):
    solution,impact,feasibility,affordability,speed,safety,reversibility,simplicity,ideality

Standard library only — Python 3.8+.
"""

import sys
import csv
import io
from typing import Any

CRITERIA = [
    "impact",
    "feasibility",
    "affordability",
    "speed",
    "safety",
    "reversibility",
    "simplicity",
    "ideality",
]

_SAMPLE_DATA: list[dict[str, Any]] = [
    {
        "solution": "Phone-based exercise reminders with gamification",
        "impact": 4,
        "feasibility": 3,
        "affordability": 2,
        "speed": 4,
        "safety": 3,
        "reversibility": 5,
        "simplicity": 2,
        "ideality": 3,
    },
    {
        "solution": "Therapist-led weekly check-in calls",
        "impact": 5,
        "feasibility": 3,
        "affordability": 1,
        "speed": 2,
        "safety": 4,
        "reversibility": 4,
        "simplicity": 4,
        "ideality": 2,
    },
    {
        "solution": "Peer-support group chat with shared progress board",
        "impact": 3,
        "feasibility": 4,
        "affordability": 4,
        "speed": 3,
        "safety": 3,
        "reversibility": 5,
        "simplicity": 2,
        "ideality": 4,
    },
    {
        "solution": "AI-driven adaptive exercise plan with minimal notifications",
        "impact": 5,
        "feasibility": 2,
        "affordability": 2,
        "speed": 3,
        "safety": 2,
        "reversibility": 3,
        "simplicity": 1,
        "ideality": 4,
    },
]


def score(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Score a list of solution dicts.

    Each input row must have a "solution" key (str) plus the eight criteria
    as ints 1–5: impact, feasibility, affordability, speed, safety, reversibility,
    simplicity, ideality.

    Returns a new list of dicts with an added "total" key (sum of eight criteria),
    sorted by total descending.
    """
    scored = []
    for row in rows:
        entry = dict(row)
        total = sum(int(entry.get(c, 0)) for c in CRITERIA)
        entry["total"] = total
        scored.append(entry)
    scored.sort(key=lambda r: r["total"], reverse=True)
    return scored


def format_table(scored: list[dict[str, Any]]) -> str:
    """Format scored solutions as a monospaced markdown/ASCII table.

    Columns: solution, impact, feasibility, affordability, speed, safety,
             reversibility, simplicity, ideality, total.
    """
    headers = [
        "Solution", "Impact", "Feasibility", "Affordability", "Speed",
        "Safety", "Reversibility", "Simplicity", "Ideality", "Total",
    ]
    col_keys = ["solution"] + CRITERIA + ["total"]

    # Calculate column widths
    widths: list[int] = []
    for i, h in enumerate(headers):
        max_w = len(h)
        for row in scored:
            val = str(row.get(col_keys[i], ""))
            max_w = max(max_w, len(val))
        widths.append(max_w)

    def _row(values: list[str]) -> str:
        cells = [v.ljust(w) for v, w in zip(values, widths)]
        return "| " + " | ".join(cells) + " |"

    def _sep() -> str:
        parts = ["-" * w for w in widths]
        return "|-" + "-|-".join(parts) + "-|"

    lines: list[str] = []
    lines.append(_row(headers))
    lines.append(_sep())
    for row in scored:
        values = [str(row.get(k, "")) for k in col_keys]
        lines.append(_row(values))

    return "\n".join(lines)


def _parse_csv(filepath: str) -> list[dict[str, Any]]:
    """Parse a solutions CSV, validating scores."""
    expected_header = ["solution"] + CRITERIA
    rows: list[dict[str, Any]] = []

    with open(filepath, "r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            print("Error: CSV file appears to be empty or has no header.", file=sys.stderr)
            sys.exit(1)

        # Normalize fieldnames (strip whitespace, lowercase)
        actual = [f.strip().lower() for f in reader.fieldnames]
        if actual != expected_header:
            print(f"Error: unexpected CSV header.", file=sys.stderr)
            print(f"  Expected: {','.join(expected_header)}", file=sys.stderr)
            print(f"  Got:      {','.join(reader.fieldnames)}", file=sys.stderr)
            sys.exit(1)

        for line_num, raw_row in enumerate(reader, start=2):  # header is line 1
            row: dict[str, Any] = {}
            # Normalize keys
            for k, v in raw_row.items():
                row[k.strip().lower()] = v.strip() if isinstance(v, str) else v

            solution_label = row.get("solution", f"row-{line_num}")
            for crit in CRITERIA:
                val_str = row.get(crit, "").strip()
                try:
                    val = int(val_str)
                except (ValueError, TypeError):
                    print(
                        f"Error: row {line_num} ('{solution_label}'): "
                        f"'{crit}' value '{val_str}' is not a valid integer.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                if val < 1 or val > 5:
                    print(
                        f"Error: row {line_num} ('{solution_label}'): "
                        f"'{crit}' = {val} is out of range (must be 1–5).",
                        file=sys.stderr,
                    )
                    sys.exit(1)
                row[crit] = val
            rows.append(row)

    return rows


def _print_help() -> None:
    print("TRIZ Evaluator — CSV format")
    print()
    print("CSV header (exact, case-insensitive):")
    print("  solution,impact,feasibility,affordability,speed,safety,reversibility,simplicity,ideality")
    print()
    print("All eight criteria use a 1–5 scale where 5 = best, 1 = worst:")
    print("  impact         — 5 = highest positive impact")
    print("  feasibility    — 5 = most feasible to implement")
    print("  affordability  — 5 = most affordable (lowest cost)")
    print("  speed          — 5 = fastest to implement")
    print("  safety         — 5 = safest (lowest risk)")
    print("  reversibility  — 5 = easiest to reverse/roll back")
    print("  simplicity     — 5 = simplest (lowest complexity)")
    print("  ideality       — 5 = closest to ideal final result")
    print()
    print("Scoring: total = sum of all eight criteria (max 40).")
    print()
    print("Example CSV content:")
    print("  solution,impact,feasibility,affordability,speed,safety,reversibility,simplicity,ideality")
    print("  Gamified reminders,4,3,2,4,3,5,2,3")
    print("  Therapist calls,5,3,1,2,4,4,4,2")


def main() -> None:
    if len(sys.argv) < 2:
        # Demo mode
        print("TRIZ Evaluator — demo mode (built-in sample)")
        print()
        scored = score(_SAMPLE_DATA)
        print(format_table(scored))
        return

    arg = sys.argv[1]
    if arg == "--help" or arg == "-h":
        _print_help()
        return

    # Assume it's a CSV file path
    rows = _parse_csv(arg)

    scored = score(rows)
    print(format_table(scored))


if __name__ == "__main__":
    main()
