# EXP-020 Failures

Post-experiment failure analysis for cross-domain selection reproduction.

Date: 2026-06-22  
Experiment: EXP-020 Cross-Domain Reproduction

---

## Failure Analysis

Selection **failed to reproduce in Distributed Databases**.

Three domains (Animals, Software Bugs, Scientific Theories) reproduced the EXP-017 winner/loser pattern: strongest trace (strength 1.00) reconstructed under budget=1; weaker traces (0.50) permanently lost expression. The fourth domain did not.

This is an **important boundary result**, not a mechanical crash. The pipeline completed in all four domains; memory traces archived; competition ran. The failure is **scientific** — selection as a cross-domain motif did not hold universally.

---

## Why Distributed Databases Failed

| Factor | Detail |
|--------|--------|
| **CAP coupling** | Consistency, Availability, and Partition Tolerance are jointly constrained tradeoffs — not independent behavior-diff categories |
| **Resolution semantics** | All three resolution notes reference systemic tradeoffs (`quorum`, `redundancy`, `cap tradeoff`) — tensions resolve as coupled system properties, not isolated behavioral splits |
| **Template overfit** | Behavior-diff template (group A vs group B within category) maps cleanly to animals and bugs but strains against engineering constraint domains |
| **Mechanical vs meaningful selection** | Trace strength differentiation existed (1.00 vs 0.50) but did not constitute meaningful selection reproduction in domain terms |

The failure localizes **theory boundaries**, not implementation bugs.

---

## Current Limitation

### Competition and ranking mechanisms remain externally imposed

Shared assumptions exported identically into every world:

```python
RECONSTRUCTION_BUDGET = 1
candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))
winners = candidates[:RECONSTRUCTION_BUDGET]
```

The ecosystem does not autonomously discover that traces should compete or that strength should determine rank. A skeptic may argue that **the same mechanism was exported into every world** — and three successes only show the mechanism works where the observation template fits.

Distributed Databases falsifies the stronger claim: **exporting the mechanism guarantees selection everywhere**.

---

## Shared Assumptions (All Domains)

| Assumption | Value | Risk |
|------------|-------|------|
| Reconstruction budget | 1 | Fixed scarcity — not emergent |
| Strength ranking | `sort by -trace_strength` | Externally imposed fitness proxy |
| Winner selection | `candidates[:budget]` | Top-N slice, not ecological dynamics |
| Trace strength formula | `min(1.0, tension/4.0)` | Fixed at archival; not adaptive |
| Strong/weak category design | 4+4 vs 2+2 | Experimenter-chosen differentiation |

These assumptions produced selection in three domains and failed to produce meaningful selection in one — suggesting **preconditions beyond shared rules** (H168).

---

## Skeptic's Objection

> The same mechanism was exported into every world.

**Valid.** EXP-020 does not prove selection emerges spontaneously. It proves that under fixed rules, **similar observation structures** produce **similar outcomes** in three unrelated semantic domains — and **do not** in a fourth.

The objection strengthens H169 and H170: absence of selection in Distributed Databases is informative precisely because the mechanism was identical. The variable is domain structure, not code path.

---

## What EXP-020 Did Achieve

| Aspect | Result |
|--------|--------|
| Cross-domain reproduction | 3/4 domains confirmed EXP-017 motif (H165) |
| Similar motifs | Differences → tensions → competition in non-biological worlds (H166) |
| Evidence upgrade | Cross-domain recurrence > single-domain repetition (H167) |
| Boundary discovery | Distributed Databases failure (H164 partial, H168–H170) |
| Single-world risk reduced | Four domains tested; failure documented honestly |

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Remove ranking assumptions** | Let competition emerge without `sort()` |
| **Remove fixed budgets** | Scarcity from resource dynamics, not constant |
| **Study spontaneous competition** | Traces compete without experimenter-imposed rank |
| **Study assumption-free worlds** | Minimal rules; observe whether selection appears |
| **Investigate necessary conditions for selection** | Formalize H168 preconditions |
| **Domain boundary mapping** | Classify which observation structures support selection |
| **Coupled-tension domains** | Test whether shared meta-tensions change competition outcomes |

---

## EXP-017 → EXP-020 Arc

| Experiment | Scope | Outcome |
|------------|-------|---------|
| EXP-017 | Single domain (biological), 3 categories | Bird wins; selection demonstrated |
| EXP-020 | Four domains, identical rules | Selection in 3/4; **boundary failure in 1/4** |

EXP-017 established selection. EXP-020 tested generalization and found **partial confirmation with documented limits**.

---

## Overall Assessment

EXP-020 **strengthened confidence in cross-domain recurrence** while **exposing important limitations and boundaries**.

**Did not achieve:**

- Universal selection reproduction (H164 not fully supported)
- Proof that selection emerges without imposed ranking/budget
- Automatic domain-independence

**Did achieve:**

- Memory competition reproduces across three non-biological domains (H165)
- Similar motifs in unrelated worlds (H166)
- Stronger evidence than additional single-domain runs (H167)
- Informative failure in Distributed Databases (H169)
- Precondition and boundary hypotheses (H168, H170)

**Scientific value:**

A program that documents **where theory works and where it breaks** is stronger than one that only reports successes. EXP-020 is Tier S++ not because all domains succeeded, but because **recurrence plus boundary failure** advances the research arc more than a fourth biological rerun would have.

Next stress test: **remove ranking assumptions** or **formalize selection preconditions** — determine whether selection can emerge without exported EXP-017 mechanics, or whether preconditions can predict Distributed-Databases-class failures before running.
