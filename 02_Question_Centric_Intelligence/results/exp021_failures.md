# EXP-021 Failures

Post-experiment failure analysis for assumption removal and selection falsification.

Date: 2026-06-22  
Experiment: EXP-021 Assumption Removal

---

## Failure Analysis

**Selection disappeared after assumption removal.**

World A (assumption-rich) reproduced EXP-017: Bird won, Mammal and Insect lost expression. World B (assumption-removed) reactivated all three traces — **zero winners, zero permanent losses, no selection-like asymmetry**.

This is a **program-level falsification**, not a mechanical crash. Both pipelines completed deterministically. The failure is **scientific**: selection — one of the project's strongest motifs — does not survive stripping of its governing assumptions.

---

## What Failed

| Claim (prior arc) | EXP-021 outcome |
|-------------------|-----------------|
| Selection emerges from memory competition | **Falsified** — requires imposed rank/budget |
| EXP-017 selection is ecosystem-native | **Qualified** — reproduced only with World A assumptions |
| EXP-020 cross-domain selection generalizes a deep principle | **Weakened** — same assumptions exported across domains |
| Selection gates resurrection naturally | **Falsified** — all traces reactivate without gate in World B |

---

## Current Limitation

### Selection depended upon externally imposed mechanisms

Selection in World A required all of:

```python
candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))
winners = candidates[:RECONSTRUCTION_BUDGET]  # RECONSTRUCTION_BUDGET = 1
```

| Mechanism | Role |
|-----------|------|
| **Ranking** | Orders candidates before selection |
| **Budget** | Hard cap on reconstructions — creates scarcity |
| **Strength ordering** | Bird (1.00) beats Mammal/Insect (0.50) |
| **winner=max()** | Top-N slice after sort — explicit winner |

These were **externally imposed** in EXP-017, EXP-018, EXP-020, and World A of EXP-021. They are not consequences of the pipeline through extinction and archival.

World B proves the pipeline alone — observations through memory traces — does **not** produce selection.

---

## What EXP-021 Did Achieve

| Aspect | Result |
|--------|--------|
| Selection falsification | H171–H173 not supported |
| Persistence confirmation | All traces stable both worlds (H177) |
| Mechanism transparency | H174, H176 supported |
| Prior result validation | World A reproduces EXP-017 |
| Narrative correction | Selection demoted; persistence elevated |

---

## What Did Not Occur

| Expected (if selection fundamental) | Observed |
|-------------------------------------|----------|
| Residual selection in World B | None — 3/3 live |
| Natural trace disappearance | None — 3/3 traces persist |
| Spontaneous asymmetry | None without sort/budget |
| Weaker traces self-suppressing | None — all reconstructed |

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Natural persistence** | Characterize what makes traces stable — identity, tension link, archival |
| **Assumption-free worlds** | Remove even tension_id ordering; test interaction-only dynamics |
| **Spontaneous asymmetries** | Seek selection-like patterns without sort/budget |
| **Minimal mechanisms** | What is the smallest rule set producing any asymmetry? |
| **Natural trace disappearance** | EXP-016 forgetting as persistence attack |
| **Persistence under further attacks** | Does archival survive more assumption stripping? |

---

## EXP-017 → EXP-021 Arc

| Stage | Selection status |
|-------|------------------|
| EXP-017 | Selection observed — treated as discovery |
| EXP-018 | Selection reproduced — cooperation failed |
| EXP-020 | Selection cross-domain — 3/4 domains |
| **EXP-021** | **Selection falsified as fundamental — assumption-imposed** |

The arc moved from **building selection** to **cross-domain validation** to **demolishing selection as primitive**.

---

## Overall Assessment

EXP-021 **significantly reduced confidence in selection as a fundamental principle** while **strengthening confidence in persistence**.

**Did not achieve:**

- Emergent selection without assumptions
- Natural trace disappearance
- Replacement primitive for selection

**Did achieve:**

- Clean falsification of selection-as-fundamental (H175, H176)
- Persistence invariant across worlds (H177)
- Destruction of project's strongest competitive motif — **high scientific value**
- Proof that assumption removal yields more insight than mechanism stacking (EXP-018–019 contrast)

**Scientific value:**

Assumption removal destroyed one of the project's strongest motifs — and in doing so, produced one of its most important results. A program that can falsify its own headline finding (selection under budget) is healthier than one that only accumulates confirming experiments.

Persistence — trace archival, identity retention, tension-linked memory — survives as the deeper memory-layer primitive. Selection remains a **useful imposed filter**, not an emergent law.

Next stress test: **persistence under attack** (forgetting, assumption stripping beyond reactivation) or **spontaneous asymmetry search** without rank/budget.
