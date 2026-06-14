#!/usr/bin/env python3
"""
TRIZ method router — heuristic suggestions from problem text.
Matches keyword/intent cues from references/triz-method-map.md and
returns ranked methods plus contradiction guesses.

Usage:
    python triz_router.py "problem description text"
    python triz_router.py                  # prints usage

Standard library only — Python 3.8+.
"""

import sys
import json
from typing import Any

# ── Rules table ──────────────────────────────────────────────────────────────
# Each rule: (keywords_tuple, method, weight, why_template)
# keywords are lowercase substrings matched against the lowercased problem.
# Extend this table to add new heuristics without restructuring the router.
RULES: list[tuple[tuple[str, ...], str, int, str]] = [
    # -- Engineering Contradiction signals
    (
        ("but ", " but ", "but", "but,", "but.", "trade-off", "tradeoff", "at the cost of",
         "however", "increases", "decreases", "more ", " less ",
         "ma ", " ma ", "ma", "ma,", "ma.", "però", "tuttavia", "a scapito di", "aumenta",
         "diminuisce", "più ", " meno "),
        "Engineering Contradiction + 40 Inventive Principles",
        3, "contradiction cue detected (trade-off / conflict connector)"
    ),
    # -- Physical Contradiction signals
    (
        ("must be both", "must be", "present and absent", "presente e assente",
         "fast and slow", "veloce e lento", "big and small", "grande e piccolo",
         "on and off", "hot and cold", "caldo e freddo",
         "deve essere", "allo stesso tempo", "contemporaneamente",
         "opposite", "opposto", "opposti", "duplice"),
        "Physical Contradiction + Separation",
        4, "physical contradiction cue (opposite/dual-state language)"
    ),
    # -- Trimming signals
    (
        ("too many", "too complex", "troppe", "troppi", "troppo", "expensive",
         "costoso", "costosa", "remove", "rimuovere", "simplify", "semplifica",
         "redundant", "ridondante", "overhead", "bloated", "snellire",
         "eliminare", "tagliare", "dimagrire"),
        "Trimming",
        3, "complexity/bloat/redundancy cue"
    ),
    # -- Root Cause Analysis signals
    (
        ("keeps happening", "recurring", "ricorrente", "again", "ancora",
         "di nuovo", "fails", "fallisce", "root", "radice", "why", "perché",
         "intermittent", "intermittente", "persiste", "ripete", "why does"),
        "Root Cause Analysis",
        3, "recurrence / root-cause language"
    ),
    # -- Resource Analysis signals
    (
        ("no budget", "senza budget", "limited", "limitato", "limitati",
         "can't afford", "non posso permetter", "without adding",
         "senza aggiungere", "scarce", "scarso", "scarsi", "few people",
         "poche persone", "pochi soldi", "gratis", "free", "sotto budget"),
        "Resource Analysis",
        2, "resource/scarcity constraint mentioned"
    ),
    # -- Ideality / IFR signals
    (
        ("ideal", "ideale", "leapfrog", "superare", "rethink", "ripensare",
         "from scratch", "da zero", "best possible", "migliore possibile",
         "perfetto", "perfect", "senza costo", "senza attrito"),
        "Ideality / IFR",
        2, "ideal-state / reimagine language"
    ),
    # -- Function Analysis signals
    (
        ("unclear", "poco chiaro", "complex system", "sistema complesso",
         "many parts", "molte parti", "interactions", "interazioni",
         "how it works", "come funziona", "confuso", "intricato"),
        "Function Analysis",
        1, "system-clarity / understanding gap"
    ),
    # -- System Operator signals
    (
        ("future", "futuro", "evolve", "evolvere", "long term", "lungo termine",
         "context", "contesto", "bigger picture", "visione d'insieme",
         "nel tempo", "prospettiva", "scala"),
        "System Operator (9 Windows)",
        1, "time-scale / context / evolution language"
    ),
    # -- Smart Little People signals
    (
        ("stuck", "bloccato", "bloccata", "no idea", "nessuna idea",
         "creative block", "blocco creativo", "non so come", "impasse"),
        "Smart Little People",
        1, "stuck / creative-block signal"
    ),
    # -- FOS (Function-Oriented Search) signals
    (
        ("someone must have solved", "how do others", "is there a field that",
         "how do they", "has anyone solved", "cross-industry", "cross industry",
         "other industries", "another field", "chi ha risolto", "come fanno",
         "qualcuno ha già"),
        "Function-Oriented Search (FOS)",
        3, "cross-industry solution search cue"
    ),
    # -- MOS (Method-Oriented Search) signals
    (
        ("we have a technology", "where can we apply", "find problems for",
         "new application", "apply this to", "abbiamo una tecnologia",
         "dove possiamo applicare"),
        "Method-Oriented Search (MOS)",
        3, "technology-to-problem matching cue"
    ),
    # -- Business TRIZ signals
    (
        ("pricing", "prezzo", "prezzi", "customer", "cliente", "clienti",
         "market", "mercato", "revenue", "ricavi", "fatturato", "team",
         "process", "processo", "org", "workflow", "flusso", "business",
         "vendite", "marketing", "concorrenza"),
        "Business TRIZ",
        2, "business / org / market domain keyword"
    ),
    # -- Software TRIZ signals
    (
        ("app", "code", "codice", "latency", "latenza", "api", "database",
         "deploy", "architecture", "architettura", "bug", "notification",
         "notifica", "notifiche", "server", "frontend", "backend", "software",
         "programma", "algoritmo", "ui", "ux", "interfaccia"),
        "Software TRIZ",
        2, "software / architecture domain keyword"
    ),
    # -- Rehabilitation TRIZ signals
    (
        ("patient", "paziente", "pazienti", "exercise", "esercizio", "esercizi",
         "therapy", "terapia", "rehab", "riabilitazione", "adherence",
         "aderenza", "aderire", "clinic", "clinica", "physio", "fisioterapia",
         "fisioterapista", "infortunio", "recupero", "cura", "trattamento"),
        "Rehabilitation TRIZ",
        2, "rehabilitation / physio / clinical domain keyword"
    ),
    # -- Su-Field + 76 Standard Solutions signals
    (
        ("interaction", "interferes", "doesn't act on", "damages", "harmful",
         "weak effect", "too strong", "contact", "interagisce", "danneggia",
         "does not act", "doesn't affect", "does not affect", "barely acts",
         "agisce a malapena"),
        "Su-Field + 76 Standard Solutions",
        4, "interaction / Su-Field cue (harmful, weak, or missing interaction)"
    ),
    # -- Evolution Trends + S-curve signals
    (
        ("leapfrog", "next generation", "where is this going", "mature",
         "plateau", "diminishing returns", "reinvent", "obsolete", "evolve",
         "reinvent the category", "next-gen", "next gen", "saturated",
         "s-curve", "s curve", "lifecycle", "life cycle"),
        "Evolution Trends + S-curve",
        4, "evolution / maturity / leapfrog cue"
    ),
    # -- Scientific Effects signals
    (
        ("how do i", "mechanism", "without a", "is there a way to",
         "achieve", "what effect", "how to achieve", "is there a way",
         "is there an effect", "physical effect", "chemical effect"),
        "Scientific Effects",
        3, "function-first / mechanism-search cue"
    ),
    # -- ARIZ signals
    (
        ("still stuck", "tried everything", "hard problem",
         "nothing works", "very hard contradiction", "deep dive",
         "tried all", "can't solve", "cannot solve", "impossible to solve",
         "dead end", "vicolo cieco", "irrisolvibile"),
        "ARIZ (escalation)",
        5, "stuck / hard-contradiction / escalation cue"
    ),
]

# ── Contradiction detection cues (separate from method scoring) ─────────────
# Italian + English contradiction connectors
_CONTRADICTION_CONNECTORS = [
    "but", "however", "trade-off", "tradeoff", "although",
    "ma", "però", "tuttavia", "eppure", "sebbene", "benché",
]

# Physical-contradiction topic words (presence/absence, opposing states)
_PHYSICAL_TOPICS = [
    ("present", "absent"), ("presente", "assente"),
    ("fast", "slow"), ("veloce", "lento"), ("veloce", "lenta"),
    ("big", "small"), ("grande", "piccolo"), ("grande", "piccola"),
    ("on", "off"), ("acceso", "spento"), ("accesa", "spenta"),
    ("hot", "cold"), ("caldo", "freddo"), ("calda", "fredda"),
    ("light", "heavy"), ("leggero", "pesante"), ("leggera", "pesante"),
    ("strong", "weak"), ("forte", "debole"),
    ("open", "closed"), ("aperto", "chiuso"), ("aperta", "chiusa"),
    ("loud", "quiet"), ("rumoroso", "silenzioso"),
    ("visible", "hidden"), ("visibile", "nascosto"), ("visibile", "nascosta"),
]

_ANNOYANCE_WORDS = [
    "annoy", "annoying", "irritating", "frustrating", "bothersome",
    "fastidios", "fastidiosa", "fastidioso", "irritante", "seccante",
    "noioso", "noiosa", "invasivo", "invasiva", "molesto", "molesta",
]

_DEFAULT_FALLBACK = [
    {"method": "Function Analysis", "score": 0, "why": "default fallback — no specific cues matched"},
    {"method": "Root Cause Analysis", "score": 0, "why": "default fallback — no specific cues matched"},
    {"method": "Engineering Contradiction + 40 Inventive Principles", "score": 0, "why": "default fallback — no specific cues matched"},
    {"method": "Resource Analysis", "score": 0, "why": "default fallback — no specific cues matched"},
    {"method": "Ideality / IFR", "score": 0, "why": "default fallback — no specific cues matched"},
]


def _detect_engineering_contradiction(lower: str, problem: str) -> str | None:
    """Try to produce a one-line 'improve X / worsens Y' guess."""
    has_connector = any(c in lower for c in _CONTRADICTION_CONNECTORS)
    if not has_connector:
        return None

    # Find the connector position and split around it
    connector_pos = -1
    found_conn = ""
    for c in _CONTRADICTION_CONNECTORS:
        pos = lower.find(c)
        if pos != -1:
            if connector_pos == -1 or pos < connector_pos:
                connector_pos = pos
                found_conn = c

    if connector_pos == -1:
        return None

    before = problem[:connector_pos].strip().rstrip(".,;:!?")
    after = problem[connector_pos + len(found_conn):].strip().lstrip(".,;:!? ")

    # Try to extract short labels — prefer the last meaningful subject
    before_label = _short_label(before, 40)
    after_label = _short_label(after, 40)

    if before_label and after_label:
        return f"improve [{before_label}] / worsens [{after_label}]"
    if before_label:
        return f"trade-off near: {before_label}"
    return f"trade-off detected in: {_short_label(problem, 80)}"


def _detect_physical_contradiction(lower: str) -> str | None:
    """Try to produce a one-line 'must be A and not-A' guess."""
    # Check explicit paired opposites
    for a, b in _PHYSICAL_TOPICS:
        if a in lower and b in lower:
            return f"element must be both {a} and {b}"

    # Check annoyance/presence patterns — common in notification/adherence problems
    has_annoyance = any(w in lower for w in _ANNOYANCE_WORDS)
    has_but = any(c in lower for c in _CONTRADICTION_CONNECTORS)

    if has_but and has_annoyance:
        # Look for the subject that's annoying / must be both present and absent
        # Check for common subjects: notification, message, reminder, alert
        for subject in ["notification", "notifica", "notifiche", "message",
                        "messaggio", "reminder", "promemoria", "alert", "avviso",
                        "allarme", "email", "popup", "suono", "sound"]:
            if subject in lower:
                return f"'{subject}' must be present (to help) and absent (to avoid annoyance)"
        return "element must be present (useful) and absent (avoids annoyance)"

    # Check if we at least have a connector — give a generic
    if has_but:
        # Look for must-be / deve-essere patterns
        for must_word in ["must be", "deve essere", "devono essere", "should be",
                          "dovrebbe", "dovrebbero"]:
            if must_word in lower:
                return f"physical contradiction suspected near '{must_word}'"

    return None


def _short_label(text: str, max_len: int = 60) -> str:
    """Truncate and clean a text fragment into a short label."""
    # Take first sentence fragment
    text = text.strip()
    if not text:
        return ""
    # Cut at reasonable boundary
    if len(text) > max_len:
        # Try to cut at a word boundary
        cut = text[:max_len].rstrip()
        last_space = cut.rfind(" ")
        if last_space > max_len // 2:
            cut = cut[:last_space]
        text = cut + "…"
    return text


def suggest_methods(problem: str) -> dict[str, Any]:
    """Suggest TRIZ methods for a problem description.

    Args:
        problem: Free-text problem description (any language, English + Italian
                 well supported).

    Returns:
        dict with keys:
        - "engineering_contradiction": str or None
        - "physical_contradiction": str or None
        - "methods": list of {"method", "score", "why"}, sorted score desc
    """
    lower = problem.lower()
    scored: dict[str, tuple[int, list[str]]] = {}

    for keywords, method, weight, why_tpl in RULES:
        for kw in keywords:
            if kw in lower:
                prev = scored.get(method)
                if prev is None:
                    scored[method] = (weight, [why_tpl])
                else:
                    total, reasons = prev
                    # Accumulate weight but cap per-method at 10
                    new_total = min(total + weight, 10)
                    if why_tpl not in reasons:
                        reasons.append(why_tpl)
                    scored[method] = (new_total, reasons)

    eng_cont = _detect_engineering_contradiction(lower, problem)
    phys_cont = _detect_physical_contradiction(lower)

    # Boost Physical Contradiction score when a physical contradiction is detected
    if phys_cont is not None:
        method_key = "Physical Contradiction + Separation"
        prev = scored.get(method_key)
        if prev is None:
            scored[method_key] = (4, ["physical contradiction explicitly detected"])
        else:
            total, reasons = prev
            reasons.append("physical contradiction explicitly detected")
            scored[method_key] = (min(total + 2, 10), reasons)

    # Boost Engineering Contradiction score when detected
    if eng_cont is not None:
        method_key = "Engineering Contradiction + 40 Inventive Principles"
        prev = scored.get(method_key)
        if prev is None:
            scored[method_key] = (3, ["engineering contradiction explicitly detected"])
        else:
            total, reasons = prev
            if "engineering contradiction explicitly detected" not in reasons:
                reasons.append("engineering contradiction explicitly detected")
            scored[method_key] = (min(total + 1, 10), reasons)

    # If we have a physical contradiction, also suggest Resource Analysis,
    # Ideality, and System Operator (decision table + spec coverage)
    if phys_cont is not None:
        for booster in ["Resource Analysis", "Ideality / IFR",
                        "System Operator (9 Windows)"]:
            if booster not in scored:
                scored[booster] = (1, ["suggested companion to Physical Contradiction"])

    # Build methods list
    if scored:
        methods = [
            {"method": m, "score": sc, "why": "; ".join(rs)}
            for m, (sc, rs) in scored.items()
        ]
        methods.sort(key=lambda x: x["score"], reverse=True)
    else:
        methods = list(_DEFAULT_FALLBACK)

    return {
        "engineering_contradiction": eng_cont,
        "physical_contradiction": phys_cont,
        "methods": methods,
    }


def _print_result(result: dict[str, Any]) -> None:
    """Pretty-print the router result to stdout."""
    if result["engineering_contradiction"]:
        print(f"Engineering Contradiction: {result['engineering_contradiction']}")
    else:
        print("Engineering Contradiction: (none detected)")

    if result["physical_contradiction"]:
        print(f"Physical Contradiction:   {result['physical_contradiction']}")
    else:
        print("Physical Contradiction:   (none detected)")

    print()
    print(f"{'Method':<55} {'Score':>5}")
    print("-" * 62)
    for m in result["methods"]:
        print(f"{m['method']:<55} {m['score']:>5}")
    print()
    print("Reasons:")
    for m in result["methods"]:
        if m["why"]:
            print(f"  [{m['method']}] {m['why']}")


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python triz_router.py \"problem description text\"")
        print()
        print("Heuristic TRIZ method router. Analyzes the problem text and suggests")
        print("which TRIZ methods to apply, ranked by relevance score.")
        print()
        print("Supports English and Italian problem descriptions.")
        sys.exit(0)

    problem = " ".join(sys.argv[1:])
    result = suggest_methods(problem)
    _print_result(result)


if __name__ == "__main__":
    main()