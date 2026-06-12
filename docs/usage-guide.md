# Usage Guide — `triz-innovation`

How to use the TRIZ skill in Claude Code, invoke it manually, add references,
save cases, run the scripts, and (later) turn it into an MCP server.

## 1. Using the skill in Claude Code
The skill auto-triggers when you describe a real problem involving contradictions,
bottlenecks, constraints, function/root-cause analysis, resources, ideality,
trimming, redesign, or innovation (see the `description` in
`.claude/skills/triz-innovation/SKILL.md`).

Just describe your problem naturally, e.g.:
> "Use TRIZ to help me: my physio app needs better exercise adherence, but more
> notifications make it annoying."

Claude will run the 10-stage pipeline and end with a testable experiment.

### Invoking it manually / forcing it
- Be explicit: start your message with **"Run the triz-innovation skill on: …"**
- Or open the skill file and tell Claude: *"Follow
  `.claude/skills/triz-innovation/SKILL.md` for this problem."*
- To go deep on one method, ask Claude to read the specific reference, e.g.
  *"Read `references/physical-contradictions.md` and apply it here."*

## 2. The pipeline (what you'll get)
1. Problem framing → 2. Function analysis → 3. Root cause → 4. Contradictions →
5. Resources → 6. Ideal Final Result → 7. Method selection → 8. Solutions
(3 conservative / 3 creative / 3 non-obvious / 2 high-risk / 1 minimal) →
9. Evaluation (1–5 on 8 criteria) → 10. Experiment plan.

## 3. Adding new references
1. Create `references/<topic>.md` under `.claude/skills/triz-innovation/`.
2. Keep it **operational**: checklists, tables, procedures — not essays.
3. Add a row to the **Reference index** table in `SKILL.md` so the skill knows
   when to load it.
4. If it changes routing, also add keyword cues to
   `references/triz-method-map.md` (and the router script).
5. Record provenance in `docs/source-map.md`.

## 4. Saving TRIZ cases
```
python .claude/skills/triz-innovation/scripts/triz_case_template.py "Short problem title"
```
Creates `cases/YYYY-MM-DD-short-problem-title.md` from `cases/template-triz-case.md`.
Fill each section as you work; after running the experiment, update **Risultati**
and **Follow-up**. See `cases/README.md`.

## 5. Using the Python scripts
All scripts are plain-stdlib MVPs (no install needed; Python 3.8+).

**Router — which methods to use:**
```
python .claude/skills/triz-innovation/scripts/triz_router.py "Ho un'app di fisioterapia che deve aiutare i pazienti ad aderire agli esercizi, ma se aggiungo troppe notifiche diventa fastidiosa."
```
Prints likely engineering/physical contradictions and a ranked list of suggested
TRIZ methods.

**Case template generator:** see section 4.

**Evaluator — score solutions:**
```
python .claude/skills/triz-innovation/scripts/triz_evaluator.py solutions.csv
```
CSV columns: `solution,impact,feasibility,cost,speed,risk,reversibility,complexity,ideality`
(scores 1–5; for cost/risk/complexity, 5 = cheap/safe/simple). Prints a table
sorted by total. Run with `--help` for the exact format, or with no args to see a
demo on built-in sample data.

## 6. Future: turning this into an MCP server
The skill is already structured for it. A minimal local MCP server would expose
three tools mirroring the scripts:
- `triz_route(problem: str)` → methods + contradictions (wrap `triz_router`).
- `triz_new_case(title: str)` → path to created case file (wrap `triz_case_template`).
- `triz_evaluate(solutions: list)` → scored table (wrap `triz_evaluator`).

Plus optional resources exposing the `references/*.md` files so any MCP-aware
client can pull a method on demand. Recommended path when you're ready:
1. Add an MCP server (e.g. Python `mcp` SDK) under `mcp/` that imports the three
   script modules (keep their logic in importable functions, not just `__main__`).
2. Register it in your client config (Claude Desktop / Codex) as a local stdio server.
3. Keep `SKILL.md` as the human/agent-facing method; MCP just makes the scripts
   callable as tools. **Not built yet — out of scope for this version.**

## 7. Codex / other agents
A portable mirror lives at `.agents/skills/triz-innovation/SKILL.md` (self-
contained pipeline, same `name`/`description`). Point Codex Agent Skills at that
folder.
