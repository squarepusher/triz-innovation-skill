I'll retrieve the repository structure and files to generate a comprehensive README.Let me explore the repository structure:Based on my review of the repository, I can now generate a comprehensive README. Here's a professionally structured README for this project:

```markdown name=README.md url=https://github.com/Cappe6969/triz-innovation-skill

# TRIZ Innovation Skill

A comprehensive, systematic innovation methodology implemented as a skill framework for solving complex problems across engineering, software, business, and clinical domains.

## What is TRIZ?

**TRIZ** (Teoriya Resheniya Izobretatelskikh Zadach — "Theory of Inventive Problem Solving") is a systematic innovation methodology developed by Genrich Altshuller and colleagues beginning in 1946. Rather than relying on random brainstorming or intuition, TRIZ provides repeatable, structured processes for solving technical contradictions and generating novel solutions.

### Core principles

- **Problems and solutions repeat across industries.** The same fundamental contradiction appears in mechanical engineering, software, business, and healthcare.
- **Innovation patterns are discoverable.** Altshuller extracted 40 recurring solution patterns from hundreds of thousands of patents — the "grammar" of invention.
- **Method over inspiration.** Replace "have a bright idea" with a disciplined, reusable process: model the problem → map to standardized parameters → look up validated solution patterns → apply them concretely.

## Repository structure

```
triz-innovation-skill/
├── TRIZ-MASTER.md                    Master knowledge base; canonical source for all methods
├── SPEC.md                           Build specification (work-in-progress tracking)
├── BACKLOG.md                        Deferred findings and known issues
├── CLAUDE.md                         Architect workflow and collaboration rules
│
├── .claude/skills/triz-innovation/   Reference implementation (skill files)
│   ├── SKILL.md                      10-stage problem-solving pipeline
│   ├── references/                   18 method reference files (each a standalone tool)
│   │   ├── function-analysis.md
│   │   ├── root-cause-analysis.md
│   │   ├── contradiction-analysis.md
│   │   ├── inventive-principles.md
│   │   ├── physical-contradictions.md
│   │   ├── resource-analysis.md
│   │   ├── ideal-final-result.md
│   │   ├── trimming.md
│   │   ├── system-operator.md
│   │   ├── substance-field-analysis.md
│   │   ├── ariz.md
│   │   ├── evolution-trends.md
│   │   ├── scientific-effects.md
│   │   ├── triz-method-map.md
│   │   ├── business-triz.md
│   │   ├── software-triz.md
│   │   └── rehabilitation-triz.md
│   └── scripts/                      Automation & lookup tools (Python)
│       ├── triz_router.py            Recommend TRIZ methods from problem description
│       ├── triz_matrix.py            Contradiction matrix lookup (39 parameters)
│       ├── triz_standard_solutions.py Su-Field diagnosis → standard solutions
│       ├── triz_ariz.py              ARIZ-85C worksheet generator
│       ├── triz_evolution.py         S-curve stage classification
│       ├── triz_case_template.py     Case file template for analysis persistence
│       ├── triz_evaluator.py         Solution scoring & ranking
│       └── data/                     CSV reference data
│           ├── parameters_39.csv
│           └── inventive_principles.csv
│
├── cases/                            Case studies & worked examples
├── docs/                             Documentation & theory notes
├── tests/                            Test suite (test coverage)
│
└── triz-prompt-engineering-main/     MIT-licensed TRIZ prompt library
    └── (source for enrichment & cross-reference)
```

## Quick start

### 1. Understanding the framework

Start with **`TRIZ-MASTER.md`** — the canonical knowledge base organized into 24 sections:

- **Sections 0–2:** Orientation (how to use this, foundations, the 10-stage pipeline)
- **Sections 3–20:** 18 TRIZ methods (function analysis, root cause, contradictions, trimming, ARIZ, evolution trends, business/software/clinical adaptations, etc.)
- **Sections 21–23:** Tooling, derivation map, and sources

### 2. Running a TRIZ analysis

Follow the **10-stage problem-solving pipeline** (from `SKILL.md`):

1. **Problem framing** — Restate neutrally; name system, stakeholders, constraints.
2. **Function analysis** — Model as Tool → Action → Object; grade each function U/H, N/I/E.
3. **Root cause analysis** — Chain symptom → root; classify causes; find leverage points.
4. **Contradiction analysis** — State engineering contradictions; map to 39 parameters; use the matrix.
5. **Resource analysis** — Inventory internal, external, free, temporal, spatial, human, digital resources.
6. **Ideal Final Result** — Define the north star: perfect function, zero cost/harm/complexity.
7. **Method selection** — Pick 2–5 TRIZ methods that fit the problem signature (use `triz_router.py`).
8. **Solution generation** — Produce 3 conservative, 3 creative, 3 non-obvious, 2 high-risk, 1 testable-this-week.
9. **Evaluation** — Score each solution on impact, feasibility, cost, speed, risk, reversibility, complexity, ideality.
10. **Experiment plan** — Name the best candidate, first experiment, success/failure criterion, next steps.

### 3. Use the helper scripts

```bash
# Recommend methods for a problem
python .claude/skills/triz-innovation/scripts/triz_router.py "too many features makes the product complex"

# Look up a contradiction (improving parameter X, worsening Y)
python .claude/skills/triz-innovation/scripts/triz_matrix.py 14 2
# Output: inventive principles to try

# Su-Field diagnosis → standard solutions
python .claude/skills/triz-innovation/scripts/triz_standard_solutions.py harmful

# Generate an ARIZ-85C worksheet
python .claude/skills/triz-innovation/scripts/triz_ariz.py "system locks up under concurrent load"

# Evaluate candidate solutions
python .claude/skills/triz-innovation/scripts/triz_evaluator.py solutions.csv

# Create a persistent case file
python .claude/skills/triz-innovation/scripts/triz_case_template.py "reminder app adherence problem"
```

## Key methods at a glance

| Method | Problem signature | Output |
|--------|-------------------|--------|
| **Function Analysis** | "What even is going on?" | Function table; trimming candidates |
| **Root Cause Analysis** | "Why does this keep happening?" | Cause-effect chain; leverage points |
| **Contradiction Matrix** | "Improving A makes B worse" | 40 inventive principles (shortlist) |
| **Physical Contradictions** | "It must be X and also not-X" | 4 separation principles (time/space/condition/scale) |
| **Resource Analysis** | "We don't have budget / people" | Inventory of free, underused resources |
| **Ideal Final Result** | "Reinvent this whole thing" | North-star vision; work-backward moves |
| **Trimming** | "Too many parts / costly / complex" | Delete component, keep function via Rule A/B/C |
| **System Operator (9 Windows)** | "Problem feels stuck; need perspective shift" | 9-cell grid (sub/system/super × past/present/future) |
| **Su-Field + 76 Standard Solutions** | "Two things interact badly" | Standard-solution class; candidate mechanisms |
| **ARIZ-85C** | "Hard contradiction won't yield; need heavy artillery" | 9-part reformulation algorithm; solution concept |
| **Evolution Trends & S-curve** | "Where is this headed / leapfrog opportunity" | S-curve stage; 8 evolution trends + next moves |
| **Scientific Effects** | "I know the action but not the mechanism" | Function → physical/chemical effects catalog |
| **Business TRIZ** | Business, pricing, org, workflow problems | Same TRIZ machinery; business vocabulary |
| **Software TRIZ** | Architecture, performance, UX, reliability | Recurring software contradictions + IP shortcuts |
| **Rehabilitation TRIZ** | Patient adherence, therapy design, clinic workflow | Behavioral resources; clinical guardrails |

## Language & framework

- **Primary language:** Python (scripts)
- **Documentation:** Markdown (skill files, master knowledge base)
- **Runtime:** No external dependencies required for the core framework; scripts use only Python stdlib
- **Skill integration:** Compatible with Claude Artifact skills and custom integrators via the reference framework

## How it fits together

**TRIZ-MASTER.md** is the textbook — a single, coherent 900+ line reference document that consolidates:

1. **18 original reference files** from `.claude/skills/triz-innovation/references/` (already clean operational synthesis).
2. **Secondary enrichment** from the MIT-licensed `triz-prompt-engineering-main/` repo (extended checklists, examples).
3. **Original operational prose** — not transcription; every section includes procedure, example, and derivation back to source.

The **skill files** in `.claude/skills/triz-innovation/` are the working implementation — each reference a standalone quick card for one method. The **scripts** automate lookups (matrix, router, evaluator) and worksheet generation.

**Cases** persist worked examples so solutions are reusable. **Tests** verify script correctness.

## Try asking

- **"How do I resolve a trade-off where improving speed reduces reliability?"** → See **Contradiction Analysis** (section 5) and **The 40 Inventive Principles** (section 6).
- **"Our product has too many features and is getting hard to maintain. How do we simplify?"** → **Trimming** (section 10) with **Function Analysis** (section 3) as the prerequisite.
- **"A startup is stuck between personalization (hard to scale) and scale (hard to personalize). How do we leapfrog?"** → **Physical Contradictions** (section 7, separation on condition) + **Business TRIZ** (section 18).
- **"I have a problem that resists the quick TRIZ tools. What's the heavy-duty approach?"** → **ARIZ-85C** (section 13) — the master algorithm.
- **"Where is an entire industry headed? How do we get ahead of the curve?"** → **Evolution Trends & S-curve** (section 14).

## Status

- **Core content:** Complete (TRIZ-MASTER.md, 18 reference files, 10-stage pipeline, 7 helper scripts).
- **Coverage:** 24 major sections, 40 inventive principles, 39 engineering parameters, 76 standard solutions, 4 separation principles, 8 evolution trends, 9 ARIZ parts.
- **Known issues:** See `BACKLOG.md` for deferred findings (Books/ licensing, router keyword edge cases, TRIZ-MASTER.md refinements).

## License

- **TRIZ-MASTER.md & reference files:** Original operational synthesis. No long verbatim passages copied from copyrighted sources.
- **`triz-prompt-engineering-main/`:** MIT Licensed (secondary enrichment source).
- **Repository:** Available under the stated terms of this project.

## Further reading

- **SPEC.md** — Build requirements and acceptance criteria.
- **CLAUDE.md** — Architect workflow (how to file changes and improvements).
- **BACKLOG.md** — Known issues and deferred work.
- **`.claude/skills/triz-innovation/references/`** — 18 deep-dive method files (one method per file).

---

**Last updated:** June 2026  
**Repository:** https://github.com/Cappe6969/triz-innovation-skill
```

This README provides:
- **What it is:** Clear positioning as a systematic innovation framework.
- **How to start:** Quick-start guide, 10-stage pipeline, script examples.
- **Structure:** Annotated directory tree showing the relationship between TRIZ-MASTER.md, references, scripts, and skill files.
- **Key methods table:** Fast lookup for matching problems to methods.
- **Integration notes:** How the pieces fit together conceptually.
- **Try asking:** Concrete example questions that surface the framework's power.
