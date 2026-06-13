# TRIZ master knowledge base — one canonical `TRIZ-MASTER.md` to derive skills from

## Context
The `triz-innovation` skill already exists and works (10-stage pipeline, 18
reference notes, helper scripts, examples, cases, docs). Each reference file is a
short, **already-clean original operational synthesis** of one TRIZ method.

This build consolidates that scattered knowledge into **one master markdown
document, `TRIZ-MASTER.md`, at the repository root** — a single, coherent,
comprehensive TRIZ body-of-knowledge that becomes the canonical source from which
the skill (and future skills) are derived. Think of it as the textbook; the skill
files become the quick-reference cards cut from it.

### Division of labour for THIS build
- **Carpenter:** author `TRIZ-MASTER.md` by **consolidating the existing
  `references/*.md` notes** (which are already correct and original) into one
  organized document following the exact skeleton in "Document structure" below,
  **enriching** each section with material from the MIT-licensed
  `triz-prompt-engineering-main/` repo, and adding the required full lists, a
  derivation map, and a provenance section.
- **Reviewer:** verify `TRIZ-MASTER.md` against the acceptance criteria below
  (structure, required sections, exact counts, keyword coverage, derivation map,
  provenance, copyright proxy) and flag — without rewriting prose — any section
  that contradicts the source `references/*.md` it consolidates.

### Source-priority & copyright rules (MANDATORY)
1. **Primary source:** the 18 files in
   `.claude/skills/triz-innovation/references/` plus the pipeline in
   `.claude/skills/triz-innovation/SKILL.md`. The master must **losslessly
   preserve** every concept already present in these files.
2. **Secondary enrichment:** `triz-prompt-engineering-main/` (MIT licensed) —
   may be used freely for additional structure, checklists, and examples.
3. **Tertiary, cross-check only:** files under `Books/` are **copyrighted**.
   Use them only to confirm concepts. **Do NOT copy book text.** No verbatim
   quotation from any file under `Books/` longer than **25 consecutive words**.
   The master must be original operational prose, tables, and checklists — never a
   transcription of book chapters. This matches the existing stance in
   `docs/source-map.md` ("no long passages were copied from the books").
4. `Books/` is gitignored and **must remain uncommitted**. Do **not** add
   `TRIZ-MASTER.md` to `.gitignore`.

## Files to create
### `TRIZ-MASTER.md` (repository root) — the only file this build creates
A single well-formed markdown document. Exactly **one H1 title**, then a
**Table of Contents** linking (with working in-document anchors) to every H2
section, then the H2 sections in the order listed under "Document structure".

## Document structure (exact H2 sections, in this order)
Each `##` heading text below must appear, in order. (Sub-bullets describe required
content, not extra headings.)

1. `## 0. How to use this document` — purpose; that this is the canonical source
   from which the skill files are derived; pointer to the Derivation map section.
2. `## 1. TRIZ foundations` — what TRIZ is; method-over-inspiration stance;
   ideality as the central idea; contradictions as the engine of invention;
   the difference between engineering and physical contradictions (overview).
3. `## 2. The problem-solving pipeline` — the full **10 stages** from `SKILL.md`,
   in order, each named with its one-line purpose: Problem framing · Function
   analysis · Root cause analysis · Contradiction analysis · Resource analysis ·
   Ideal Final Result · Method selection · Solution generation · Evaluation ·
   Experiment plan.
4. `## 3. Function analysis` — derives from `references/function-analysis.md`.
5. `## 4. Root cause analysis` — derives from `references/root-cause-analysis.md`.
6. `## 5. Engineering contradictions, the 39 parameters & the contradiction matrix`
   — derives from `references/contradiction-analysis.md` +
   `references/contradiction-matrix.md`. Must include the **full list of all 39
   engineering parameters** (id + name), sourced from
   `.claude/skills/triz-innovation/scripts/data/parameters_39.csv`.
7. `## 6. The 40 inventive principles` — derives from
   `references/inventive-principles.md`. Must list **all 40 principles** (number +
   name), names consistent with
   `.claude/skills/triz-innovation/scripts/data/inventive_principles.csv`.
8. `## 7. Physical contradictions & the 4 separation principles` — derives from
   `references/physical-contradictions.md`. Must name all **4 separations**:
   separation in **time**, in **space**, on **condition**, and by **scale
   (parts ↔ whole)**.
9. `## 8. Resource analysis` — derives from `references/resource-analysis.md`.
10. `## 9. Ideal Final Result & ideality` — derives from
    `references/ideal-final-result.md`.
11. `## 10. Trimming` — derives from `references/trimming.md`; name trimming
    rules A/B/C.
12. `## 11. System operator (9 Windows)` — derives from
    `references/system-operator.md`.
13. `## 12. Substance-field analysis & the 76 standard solutions` — derives from
    `references/substance-field-analysis.md`. Must name all **5 standard-solution
    classes** (1–5) and describe the Su-Field states (incomplete, insufficient,
    harmful, measurement, excessive), consistent with the recommender script.
14. `## 13. ARIZ-85C` — derives from `references/ariz.md`. Must list the **9
    parts** consistent with the worksheet generator
    (`triz_ariz.py`): Problem & technical contradiction · Resources · IFR &
    physical contradiction · Apply resources · Knowledge base · Reformulate ·
    Analyze the solution · Maximize the solution · Reflect on the process.
15. `## 14. Evolution trends & the S-curve` — derives from
    `references/evolution-trends.md`. Must name all **8 trends** and the **4
    S-curve stages** (Infancy, Growth, Maturity, Decline), consistent with
    `triz_evolution.py`.
16. `## 15. Scientific effects` — derives from `references/scientific-effects.md`.
17. `## 16. Function-Oriented Search & Method-Oriented Search` — derives from
    `references/triz-method-map.md` (FOS/MOS portions).
18. `## 17. Smart Little People` — derives from `references/triz-method-map.md`.
19. `## 18. Business TRIZ` — derives from `references/business-triz.md`.
20. `## 19. Software TRIZ` — derives from `references/software-triz.md`.
21. `## 20. Rehabilitation & clinical TRIZ` — derives from
    `references/rehabilitation-triz.md`.
22. `## 21. Tooling` — short table of the helper scripts
    (`triz_router.py`, `triz_matrix.py`, `triz_standard_solutions.py`,
    `triz_ariz.py`, `triz_evolution.py`, `triz_case_template.py`,
    `triz_evaluator.py`) and what each does in one line.
23. `## 22. Derivation map` — a markdown table with columns
    `Master section | Derives skill file(s)` mapping each method section (3–20)
    to the `references/...md` file(s) it consolidates, and the pipeline section to
    `SKILL.md`.
24. `## 23. Provenance & sources` — a table crediting sources: the MIT
    `triz-prompt-engineering-main` repo and the books **by title** (as listed in
    `docs/source-map.md`), plus an explicit copyright note stating the document is
    original operational synthesis containing no long verbatim book passages.

### Per-method-section template (sections 3–20)
Every method section (3 through 20) must contain, as **bold inline labels** (not
new headings), in this order:
- **When to use** — one or two lines on the problem signature.
- **Core idea** — the method in 2–4 sentences.
- **Procedure** — a numbered or bulleted step list.
- **Example** — one short worked micro-example (1–4 lines).
- **Derives →** — the `references/...md` file(s) this section consolidates.

## Acceptance criteria (must all be objectively checkable)
1. `TRIZ-MASTER.md` exists at the repository root, is valid markdown, has exactly
   one H1, and is **at least 900 lines** long.
2. It begins (after the H1) with a **Table of Contents** that links to every H2
   section; each TOC anchor resolves to a heading that exists in the file.
3. **All 24 H2 headings** listed in "Document structure" are present, with the
   exact section text, in the specified order.
4. **Full lists & exact counts present and correct:**
   - The 40 inventive principles: **40** distinct numbered names, matching the
     names in `scripts/data/inventive_principles.csv`.
   - The 39 engineering parameters: **39** distinct numbered names, matching
     `scripts/data/parameters_39.csv`.
   - The **4** separation principles are named (time, space, condition, scale).
   - The **8** evolution trends and **4** S-curve stages are named.
   - The **5** standard-solution classes (1–5) are named.
   - The **9** ARIZ parts are listed in the order used by `triz_ariz.py`.
   - The **10** pipeline stages are listed in order.
5. **Per-section template satisfied:** every method section (3–20) contains all
   five labels — `When to use`, `Core idea`, `Procedure`, `Example`,
   `Derives →` — in order.
6. **Coverage of existing references:** for each of the 18 `references/*.md`
   files, its corresponding master section exists and names the file in its
   `Derives →` label; and the master section reproduces that reference's key
   concept(s). (Reviewer spot-checks at least these anchor terms appear in the
   right section: `Tool → Action → Object` and `U/H` (function analysis);
   `leverage point` (root cause); `MATCHEMIB` or the field list (ideality/
   resources); `ideality equation` (IFR); separation `in time`/`in space`
   (physical contradictions); `9 Windows` (system operator); `S1`/`S2`/`field`
   (substance-field).)
7. **Derivation map** (section 22) is a table mapping every method section (3–20)
   to its `references/...md` file(s) and the pipeline section to `SKILL.md`; every
   referenced path exists on disk.
8. **Provenance** (section 23) credits the MIT prompt repo and the books by title
   and contains an explicit copyright note about original synthesis / no long
   verbatim passages.
9. **Copyright proxy:** no verbatim run of **25+ consecutive words** copied from
   any file under `Books/` appears in `TRIZ-MASTER.md`; the document is not a
   transcription of book chapters.
10. **No collateral changes:** the build creates only `TRIZ-MASTER.md`. It does
    **not** modify any file under `.claude/`, `.agents/`, `cases/`, `docs/`, or
    `triz-prompt-engineering-main/`; it does **not** modify the helper scripts or
    data CSVs; it does **not** commit anything under `Books/`; it does **not** add
    `TRIZ-MASTER.md` to `.gitignore`.
11. All prior acceptance criteria from the existing skill still hold (scripts
    compile, references/SKILL.md/data unchanged).

## Out of scope (do NOT build)
- **Re-deriving or regenerating the skill files from the master** (new SKILL.md /
  references). That is a deliberate follow-up build; this one only produces the
  master + the derivation map.
- Copying verbatim text from `Books/`; committing `Books/`.
- Any new scripts, MCP server, web app, GUI, or front-end.
- Editing existing references, `SKILL.md`, scripts, data CSVs, examples, or docs.
- Fixing the known router / `.agents`-mirror BACKLOG items (separate work).
