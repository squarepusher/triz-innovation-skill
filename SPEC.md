# TRIZ Innovation skill — advanced TRIZ engines (matrix, Su-Field, ARIZ, evolution) + router extension

## Context
The `triz-innovation` skill already exists and works (10-stage pipeline, 13+
reference files, 3 helper scripts, examples, cases, docs). This build **deepens it
toward real, rigorous TRIZ** by adding four advanced engines as Python helper
scripts, plus bundled data.

The Architect (Claude) has **already authored** all new knowledge content and data
for this build:
- New references (do NOT rewrite — original TRIZ synthesis, prose is final):
  `references/contradiction-matrix.md`, `references/substance-field-analysis.md`,
  `references/ariz.md`, `references/evolution-trends.md`,
  `references/scientific-effects.md`.
- Updated `SKILL.md` (+ its `.agents` mirror) and `references/triz-method-map.md`.
- Bundled data files under `.claude/skills/triz-innovation/scripts/data/`:
  `contradiction_matrix.csv`, `parameters_39.csv`, `inventive_principles.csv`.

This build has two jobs:
1. **Carpenter:** implement the four new/changed Python scripts described below.
2. **Reviewer:** verify the scripts against the acceptance criteria AND audit that
   the Architect-authored references and data files exist with the required
   structure. The Reviewer may flag a missing/empty/malformed file but must NOT
   rephrase any prose.

### Engineering constraints (all scripts)
- **Python 3.8+, standard library only** (no pip installs, no network). Must run on
  Windows.
- Keep core logic in an **importable function** with an `if __name__ == "__main__":`
  guard (a future MCP server will import them).
- Resolve bundled data relative to the **script's own location**
  (`Path(__file__).parent / "data" / ...`), never the current working directory, so
  the scripts work when invoked from any folder.
- Read CSVs with the `csv` module and `encoding="utf-8"`.
- Do not modify the bundled data files or any reference/SKILL markdown.

## Files to create

### 1. `.claude/skills/triz-innovation/scripts/triz_matrix.py`
Contradiction-matrix lookup over the bundled 39×39 Altshuller matrix.
- Public function `lookup(improving: int, worsening: int) -> dict` returning:
  - `"improving"`: `{"id": int, "name": str}` (name from `parameters_39.csv`).
  - `"worsening"`: `{"id": int, "name": str}`.
  - `"principles"`: list of `{"id": int, "name": str}` (names from
    `inventive_principles.csv`), in the order stored in the matrix row.
  - `"note"`: str or None.
- Behavior:
  - Validate `improving` and `worsening` are ints in **1..39**; otherwise raise
    `ValueError` (CLI catches it, prints a clear message, exits non-zero).
  - If `improving == worsening`: return empty `principles` and
    `note = "Same parameter on both sides — see references/physical-contradictions.md (separate in time/space/condition)."`.
  - If no matrix row exists for the pair: return empty `principles` and a
    `note` suggesting Resource Analysis + IFR as fallback.
- Helper functions allowed: `load_parameters()`, `load_principles()`,
  `load_matrix()` (each returns a dict keyed by id / by `(improving, worsening)`).
- CLI: `python triz_matrix.py <improving_id> <worsening_id>` prints the two named
  parameters and the ranked inventive principles (id + name), plus any note.
  With wrong/no args, print a one-line usage including a hint to run
  `python triz_matrix.py --list` ; `--list` prints the 39 parameters (id + name).

### 2. `.claude/skills/triz-innovation/scripts/triz_standard_solutions.py`
Su-Field → 76-standard-solutions class recommender (rule-based, transparent).
- Public function `recommend(state: str) -> dict` returning:
  - `"state"`: the normalized input state.
  - `"classes"`: list of `{"class": int, "name": str, "moves": [str, ...]}` —
    the standard-solution classes that apply, each with 2–4 concrete candidate
    moves.
  - `"note"`: str or None (e.g. a pointer to the matching reference section).
- Accept these states (case-insensitive, also accept the leading synonym):
  `incomplete` (`missing`), `insufficient` (`weak`), `harmful`,
  `measurement` (`detection`), `excessive` (`complex`).
- Keep the state→classes→moves mapping in a **single readable table/dict near the
  top of the file** so a human can extend it. The classes and moves must be
  consistent with `references/substance-field-analysis.md` (e.g. `harmful` →
  Class 1 moves: block the field / add a third substance S3 / redirect onto a
  sacrificial element; `insufficient` → Class 2 moves: chain Su-Fields / upgrade
  the field toward more controllable / fragment substances / make the field
  dynamic; `excessive` → Class 5 + trimming).
- On an unknown state: raise `ValueError`; CLI prints a clear message listing the
  valid states and exits non-zero.
- CLI: `python triz_standard_solutions.py --state <state>` prints the matched
  classes and moves. With no `--state`, print usage listing the 5 valid states
  (exit non-zero). Support `--list` to print all 5 states with a one-line gloss.

### 3. `.claude/skills/triz-innovation/scripts/triz_ariz.py`
ARIZ worksheet generator (deterministic templating; mirrors the case generator).
- Public function `create_worksheet(title: str, cases_dir: str | Path = None) -> Path`.
- Behavior: write a new markdown file named `YYYY-MM-DD-ariz-<slug>.md` (today's
  date; slug = lowercased title, non-alphanumeric → single hyphens, trimmed) into
  the repo's `cases/` folder by default (resolve relative to the script location:
  `scripts` → skill → `.claude/skills/triz-innovation` → repo root → `cases`).
  Do not overwrite an existing file — if it exists, append `-2`, `-3`, …
- The worksheet must contain a fillable skeleton with these exact level-2 headings
  **in order** (one short prompt line under each is enough; point the reader to
  `references/ariz.md` for full guidance):
  `## Part 1 — Problem & technical contradiction`,
  `## Part 2 — Resources (operating zone & time)`,
  `## Part 3 — IFR & physical contradiction`,
  `## Part 4 — Apply resources (separation / Su-Field)`,
  `## Part 5 — Knowledge base (effects / analogies)`,
  `## Part 6 — Reformulate the problem`,
  `## Part 7 — Analyze the solution`,
  `## Part 8 — Maximize the solution`,
  `## Part 9 — Reflect on the process`.
  The first line of the file must record the original title (e.g. an H1
  `# ARIZ worksheet — <title>` or an HTML comment with the title).
- CLI: `python triz_ariz.py "Short title"` creates the file and prints its path.
  No argument → usage line, exit non-zero.

### 4. `.claude/skills/triz-innovation/scripts/triz_evolution.py`
S-curve stage classifier + 8-trend checklist (rule-based).
- Public function `analyze(signals: str = "") -> dict` returning:
  - `"s_curve_stage"`: `{"stage": int, "name": str, "why": str}` where stage is
    1..4 (Infancy/Growth/Maturity/Decline) or `0`/`"Unknown"` when signals are
    empty or inconclusive.
  - `"trends"`: list of all **8** trends, each `{"id": int, "name": str,
    "prompt": str}` (the "where are you on this trend / what's the next step"
    question), consistent with `references/evolution-trends.md`.
  - `"note"`: str or None.
- Stage heuristic: lowercase the signals, match documented cues — e.g.
  "diminishing returns", "plateau", "minor tweaks", "cost rising", "gains
  shrinking" → Maturity (3); "obsolete", "replaced", "declining" → Decline (4);
  "rapid", "scaling", "investment", "growing fast" → Growth (2); "prototype",
  "unreliable", "early", "experimental" → Infancy (1). Keep the cue table near the
  top of the file. No match → stage 0 / Unknown.
- CLI: `python triz_evolution.py --signals "..."` prints the detected S-curve
  stage and the 8 trend prompts. With no `--signals`, print stage Unknown and the
  8 trend prompts (still useful as a checklist).

### 5. Extend `.claude/skills/triz-innovation/scripts/triz_router.py`
Add the new advanced methods to the existing router's rules table so it can suggest
them. Do not break existing behavior or the existing acceptance criteria.
- Add scored rules (keywords → method → weight + reason) for, at minimum:
  - **Su-Field + 76 Standard Solutions** — cues: "interaction", "interferes",
    "doesn't act on", "damages", "harmful", "weak effect", "too strong",
    "contact", "interagisce", "danneggia".
  - **Evolution Trends + S-curve** — cues: "leapfrog", "next generation",
    "where is this going", "mature", "plateau", "diminishing returns",
    "reinvent", "obsolete", "evolve".
  - **Scientific Effects** — cues: "how do I", "mechanism", "without a",
    "is there a way to", "achieve ... without".
  - **ARIZ** — cues: "still stuck", "tried everything", "hard problem",
    "nothing works", "very hard contradiction".
- These cues are documented in `references/triz-method-map.md` ("Router
  heuristics"); keep the router's rules table consistent with it.

## Acceptance criteria (must all be objectively checkable)
1. All four new scripts exist at the exact paths above and are valid Python
   (`python -m py_compile` succeeds for each), as does the edited `triz_router.py`.
2. Every script uses **only the standard library** (no third-party imports).
3. Each script exposes its named public function AND a `__main__` guard.
4. **Data files present & well-formed:**
   `scripts/data/parameters_39.csv` has header `id,name` and **39** data rows;
   `scripts/data/inventive_principles.csv` has header `id,name` and **40** data
   rows; `scripts/data/contradiction_matrix.csv` has header
   `improving,worsening,principles` and **at least 1000** data rows.
5. **Matrix lookup:** `triz_matrix.lookup(14, 1)` returns a dict whose
   `improving.name` is the parameter 14 name, `worsening.name` is the parameter 1
   name, and `principles` is a non-empty list of `{"id","name"}` whose ids all fall
   in 1..40 and match the corresponding names from `inventive_principles.csv`.
6. **Matrix CLI:** `python triz_matrix.py 14 1` prints both parameter names and at
   least one inventive principle (id + name); `python triz_matrix.py 5 5` reports
   the "same parameter → physical contradiction" note and an empty principle list;
   an out-of-range id (e.g. `0` or `40`) exits non-zero with a clear message.
7. **Standard solutions:** `triz_standard_solutions.recommend("harmful")` returns a
   dict whose `classes` is non-empty, includes class **1**, and every class entry
   has a non-empty `moves` list. `recommend("insufficient")` includes class **2**.
   An unknown state (e.g. `"banana"`) raises `ValueError`, and the CLI form
   `python triz_standard_solutions.py --state banana` exits non-zero listing the 5
   valid states.
8. **ARIZ worksheet:** `python triz_ariz.py "Pump cavitation test"` creates a file
   matching `cases/20??-??-??-ariz-pump-cavitation-test.md` that contains all nine
   `## Part 1` … `## Part 9` headings listed above in order; running it twice does
   not overwrite the first file (a `-2` variant is created).
9. **Evolution:** `triz_evolution.analyze("gains shrinking, diminishing returns,
   minor tweaks")` returns `s_curve_stage.stage == 3` (Maturity) and a `trends`
   list of exactly **8** entries each with a non-empty `prompt`.
   `triz_evolution.analyze("")` returns stage `0`/Unknown and still 8 trends. The
   CLI `python triz_evolution.py --signals "obsolete, replaced by new tech"`
   reports Decline (stage 4).
10. **Router extension:** `triz_router.suggest_methods(...)` on an interaction-style
    problem (e.g. "The cleaning brush barely acts on the surface and the vibration
    damages the bearing") returns a `methods` list that **includes "Su-Field + 76
    Standard Solutions"**; on a maturity/leapfrog problem (e.g. "This product
    category is mature with diminishing returns — how do we leapfrog it?") the
    `methods` list **includes "Evolution Trends + S-curve"**. The router's original
    example from the prior build still returns its previously required methods
    (Physical Contradiction + Separation, Resource Analysis, Ideality/IFR,
    Trimming, System Operator).
11. **Content audit (Reviewer):** these Architect-authored files exist and are
    non-empty: `references/contradiction-matrix.md`,
    `references/substance-field-analysis.md`, `references/ariz.md`,
    `references/evolution-trends.md`, `references/scientific-effects.md`.
12. **Reference-index audit:** `SKILL.md`'s reference index lists each of the five
    new reference files above, and the file each row points to exists. Both
    `SKILL.md` files (`.claude/...` and `.agents/...`) still start with YAML
    frontmatter containing `name: triz-innovation` and a `description:` mentioning
    TRIZ and multiple domains.
13. **SKILL.md advanced track:** `SKILL.md` contains an "Advanced track" section
    that references ARIZ, Su-Field / 76 Standard Solutions, Evolution Trends, and
    Scientific Effects, and mentions the four new script filenames.
14. All prior acceptance criteria from the existing skill still hold: the three
    original scripts (`triz_router.py`, `triz_case_template.py`,
    `triz_evaluator.py`) still compile and their documented public functions/CLIs
    still work.

## Out of scope (do NOT build)
- No MCP server, web app, GUI, or any front-end.
- No rewriting/replacing Architect-authored markdown or the bundled data CSVs
  (Reviewer may only flag a missing/empty/malformed file, not rephrase prose).
- No embedding of the **full 76-standard-solutions text** or the full scientific-
  effects database — the recommenders work at the class/family level by design.
- No external Python dependencies; no network calls.
- Do not change the 10-stage pipeline numbering or the three original scripts'
  public APIs.
