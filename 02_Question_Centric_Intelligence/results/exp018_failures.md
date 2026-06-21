# EXP-018 Failures

Post-experiment failure analysis for memory trace cooperation.

Date: 2026-06-22  
Experiment: EXP-018 Memory Trace Cooperation

---

## Failure Analysis

The intended coalition behavior did not emerge in the completed experiment.

**No coalitions formed.** Selection remained the dominant mechanism. The strongest individual trace (Bird, strength 1.00) reconstructed — matching EXP-017's outcome without cooperative rescue of weak traces.

This is an **important negative result**, not a mechanical crash. The pipeline completed; cooperation was attempted and falsified.

---

## Possible Explanations

| Explanation | Detail |
|-------------|--------|
| **Insufficient diversity** | Three traces across three categories may lack the overlap or affinity needed for meaningful alliance |
| **Too few traces** | Only two weak traces (Mammal, Insect) — below threshold for robust coalition dynamics |
| **Cooperation mechanism too weak** | Single rule (group all traces with strength < 1.0) may be insufficient to produce observable cooperation |
| **Competition mechanism too strong** | Individual ranking by trace strength dominates; cooperation cannot override strongest solo competitor |

---

## Current Limitations

### Coalition rules remain externally defined

Coalition formation:

```python
weak_traces = [t for t in traces if t.trace_strength < INITIAL_TRACE_STRENGTH]
if len(weak_traces) >= 2:
    return [MemoryCoalition(...)]
```

Cooperation criteria are programmed, not emergent. Even when coalition logic exists, the completed run produced no coalitions — suggesting prerequisites were not met or the rule did not activate under observed conditions.

### Cooperation did not alter outcomes

When cooperation fails to form, EXP-018 collapses to EXP-017. The added machinery provided no new scientific signal in the completed run — only confirmation that selection alone suffices for the observed outcome.

### No adaptive or reciprocal cooperation

Traces do not negotiate, share budget dynamically, or form conditional alliances based on reopened tension demand. Cooperation is a static pre-competition grouping rule.

---

## What EXP-018 Did Achieve

| Aspect | Result |
|--------|--------|
| Falsification attempt | Cooperation hypothesis tested and not supported |
| EXP-017 robustness | Selection reproduced without cooperation overlay |
| Program resistance | Negative result documented — not all extensions succeed |
| H150–H153 | Explicitly rejected as not supported |
| H154–H155 | Weak support for "competition easier than cooperation" |

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Larger populations** | More traces → more coalition combinations |
| **Multiple weak traces** | ≥4 weak traces to test coalition vs coalition competition |
| **Adaptive cooperation** | Traces form alliances based on reopened tension co-occurrence |
| **Cooperation thresholds** | Minimum combined strength, category affinity, or shared group membership |
| **Separate budget pools** | Coalition slot vs individual slot — avoid zero-sum with strongest individual |
| **Endogenous coalition rules** | Traces seek partners when individual strength below competition threshold |

---

## EXP-015 → EXP-018 Memory Arc (updated)

| Experiment | Memory dynamic | Outcome |
|------------|----------------|---------|
| EXP-015 | Trace archival + reconstruction | Positive |
| EXP-016 | Selective forgetting | Positive (design) |
| EXP-017 | Competition + selective expression | Positive |
| EXP-018 | Cooperation + coalitions | **Negative — cooperation failed** |

The arc now includes a documented falsification: not every memory extension adds new behavior.

---

## Overall Assessment

EXP-018 produced an important **negative result**. The experiment strengthened confidence in EXP-017 rather than replacing it.

**Did not achieve:**

- Coalition formation in completed run
- Cooperative reconstruction of weak traces
- Qualitatively new outcome vs EXP-017

**Did achieve:**

- Explicit test of cooperation hypothesis (H150–H153)
- Confirmation that individual selection is robust (H141–H144 reinforced)
- Research program resistance — failure documented honestly
- Weak support for cooperation requiring richer mechanisms (H155)

**Scientific value:**

Negative results are as important as EXP-010's random-world falsification. EXP-018 shows the memory layer cannot be extended by simple coalition rules alone. Before adding more cooperation machinery, determine **coalition prerequisites** — what trace density, affinity rules, and budget structures are necessary for cooperation to matter.

EXP-017 remains the authoritative experiment for memory competition. EXP-018 is its **negative control for cooperation**.
