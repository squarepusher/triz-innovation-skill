# Root Cause Analysis (Cause–Effect Chain)

Trace a symptom down to the **root cause(s)** so you fix the disease, not the
fever. In TRIZ this feeds straight into contradiction analysis: the best place to
break a chain is where a cause sits behind a contradiction.

## Step 1 — Anchor the symptom
State the observable problem as a measurable effect ("daily active patients
dropped 30% after week 2"). No causes yet.

## Step 2 — Build the cause–effect chain
Repeatedly ask **"why does this happen?"** (TRIZ-style 5+ Whys, but allow
branching — a cause can have several parents).

```
Symptom
 └─ why? → cause A
     └─ why? → cause A1   (deeper)
     └─ why? → cause A2
 └─ why? → cause B
```

Stop a branch when you hit either:
- a **root cause** you can act on (controllable), or
- a **physical/economic limit** you can't change (boundary), or
- a useful function whose downside is the cause (→ contradiction).

## Step 3 — Classify every cause
For each node tag:
- **Surface vs deep** (how far down the chain).
- **Controllable vs not controllable** (can you act on it?).
- **Cause-behind-a-contradiction?** (fixing it would hurt something useful →
  hand to `contradiction-analysis.md`).

## Step 4 — Find leverage points
A **leverage point** is a controllable cause that, if removed, collapses the most
downstream effects. Prefer leverage points that are:
1. upstream (kill many effects at once),
2. controllable, and
3. cheap to act on.

Rank causes by *(reach × controllability ÷ cost)* and pick the top 1–2.

## Step 5 — Convert to a problem to solve
Restate each leverage cause as a solvable problem, e.g.:
> "Reminders fire at random times" → *root cause* "we don't know the patient's
> active hours" → **solvable:** how do we learn or infer the active window
> without asking?

That restatement is what stages 4–8 of the pipeline operate on.

## Pitfalls
- Stopping at a blame-the-user cause ("patients are lazy") — push deeper to a
  system cause you can change.
- Single-line chains — real failures usually have 2–3 contributing branches.
- Confusing correlation with cause — apply the magic-wand test: remove the
  candidate cause mentally; does the symptom vanish?

Repo reference: `technical_triz/root_cause_analysis/` and the richer
`technical_triz/root_conflict_analysis/` (RCA+ that ties causes to contradictions).
