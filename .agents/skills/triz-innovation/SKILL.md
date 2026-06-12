---
name: triz-innovation
description: Use this skill when solving real-world technical, business, software, workflow, rehabilitation, clinical, product, or organizational problems using structured TRIZ methods. Trigger this skill for contradictions, bottlenecks, constraints, creative problem solving, function analysis, root cause analysis, resource optimization, ideality, trimming, system redesign, or innovation strategy.
---

# TRIZ Innovation (Codex / agent-portable)

Structured TRIZ problem-solving engine. Not brainstorming — a fixed pipeline that
turns a messy problem into a few **evaluated, testable** solutions. Method over
inspiration.

> This is the portable mirror of the Claude Code skill. The full, canonical
> version with on-demand reference files and helper scripts lives at
> `../../../.claude/skills/triz-innovation/`. Read those `references/*.md` for
> depth when a stage needs it; this file alone is enough to run the pipeline.

## Operating rules
1. Run stages 1–10 in order; if a stage is empty, say so and continue.
2. Ask at most 3 questions, only when the answer changes the analysis; else assume and proceed.
3. Be concrete — name components, parameters, resources, steps. No generic advice.
4. Tag each solution with the TRIZ method that produced it.
5. Always finish with a testable experiment (stage 10).

## Pipeline
1. **Problem framing** — restate neutrally; name system / sub / super; stakeholders; main useful function; harmful/insufficient/excessive functions; real constraints; separate symptoms vs causes vs goals.
2. **Function analysis** — components (3 levels) + table `Tool | Action | Object | U/H | N/I/E | Parameter`; flag harmful/redundant; mark trimming candidates.
3. **Root cause analysis** — cause→effect chain; surface vs deep; controllable vs not; leverage points.
4. **Contradiction analysis** — engineering ("IF X THEN Y BUT Z"); physical ("element must be A and not-A"); note time/space/condition/scale separations.
5. **Resource analysis** — internal · external · free/underused · informational · temporal · spatial · human · digital. How each could be used.
6. **Ideal Final Result** — function happens by itself, no cost/harm, ideally no new component. Maximize useful, minimize cost/complexity/friction/risk.
7. **Method selection** — pick 2–5: Function Analysis · RCA · Engineering Contradiction+40 IP · Physical Contradiction+Separation · Resource Analysis · Ideality/IFR · Trimming · System Operator · Function/Method-Oriented Search · 76 Standard Solutions · Smart Little People · Business/Software/Rehab TRIZ. Justify each.
8. **Solution generation** — 3 conservative, 3 creative-realistic, 3 non-obvious TRIZ, 2 high-risk/high-upside, 1 minimal test. Tag each with its method.
9. **Evaluation** — score 1–5 on impact, feasibility, cost, speed, risk, reversibility, complexity, ideality. Table, sorted.
10. **Experiment plan** — best candidate; first experiment; data to collect; success/failure criterion (a number); next step if it works; next step if it fails.

## Helper scripts (optional)
- `triz_router.py "problem"` → suggested methods + likely contradictions.
- `triz_case_template.py "title"` → new markdown case file in `cases/`.
- `triz_evaluator.py solutions.csv` → scored, sorted table.

Keep `description` and `name` in sync with the Claude version so both hosts route identically.
