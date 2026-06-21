# EXP-003 Failures

Post-experiment failure analysis for hierarchical question evolution.

Date: 2026-06-21  
Experiment: EXP-003 Hierarchical Question Evolution

---

## Failure Mode

Over-abstraction

---

## Description

Attention collapsed to the highest-level question.

After stage 2 merge, the repository contained nine questions across three generations. Only one remained ACTIVE:

**Why do species gain or lose capabilities?**

All other questions — six entity questions and two category abstractions — transitioned to PARTIALLY_RESOLVED. They persist in the repository with intact genealogy, but none compete for investigation at the ACTIVE level.

Lower-level questions became PARTIALLY_RESOLVED:

| Generation | Questions | Final State |
|------------|-----------|-------------|
| 0 | Penguin, Ostrich, Emu, Kiwi, Bat, Whale | PARTIALLY_RESOLVED |
| 1 | Bird abstraction, Mammal abstraction | PARTIALLY_RESOLVED |
| 2 | Species capabilities abstraction | ACTIVE |

The hierarchy grew taller but the active frontier narrowed to a single node.

---

## Risk

Loss of diversity

When abstraction stacks vertically without constraint:

- Entity-specific inquiry is suppressed (Why doesn't Penguin fly?)
- Category-specific inquiry is suppressed (Why don't some birds fly?)
- Only the meta question remains eligible for ACTIVE investigation

The question ecosystem becomes a monoculture — one dominant abstraction consuming attention that previously distributed across six independent unknowns.

Curiosity debt compounds upward (meta holds 6.0 aggregated) while lower levels retain orphaned debt (12.0 across eight PARTIALLY_RESOLVED questions). Total repository debt reaches 18.0 with unclear attention allocation.

---

## Analogy

### Overfitting

A model that explains all training anomalies with one high-level rule may lose sensitivity to individual cases. The meta question "Why do species gain or lose capabilities?" subsumes penguin flightlessness and bat echolocation-adjacent flight into one frame — potentially at the cost of explanatory precision.

### Monocultures

Biological monocultures are efficient but fragile. A question repository with one ACTIVE question is similarly fragile: if the meta abstraction proves unproductive, no diverse lower-level questions remain in ACTIVE state to continue investigation.

### Excessive compression

Each merge stage compresses multiple questions into one. EXP-003 applied compression twice. The result resembles a world model that has over-compressed its anomalies — H4 and H7 warn that compression failures generate curiosity, but over-compression may kill it at lower levels.

---

## Contributing Factors

1. **No merge depth limit.** Stage 2 merged without checking whether category abstractions should remain ACTIVE.

2. **PARTIALLY_RESOLVED still counts as active** in `get_active_questions()`, masking the collapse in aggregate statistics (9 "active" by API, 1 ACTIVE by state).

3. **Debt aggregation without transfer.** Lower questions keep debt after merge, but state demotion removes them from ACTIVE competition — debt exists without attention pathway.

4. **No split or resistance mechanism.** H40 (questions should resist over-abstraction) was not implemented. Nothing blocked stage 2.

5. **Tree-only topology.** Vertical stacking has no horizontal branches. All paths lead to one apex.

---

## Potential Future Solution

Communities and graph structures

Rather than deeper trees, future experiments should explore:

- **Question communities** (H18): Bird and mammal families as parallel clusters, not stacked layers
- **Graph evolution** (H17): Questions linked by supports, contradicts, depends_on — not only generalizes/specializes hierarchy
- **Merge resistance (H40):** Threshold or vote before demoting ACTIVE questions to PARTIALLY_RESOLVED
- **Attention budget across levels (H12–H15):** Reserve investigation capacity for generation 0 and generation 1 questions even when generation 2 exists
- **Split operations:** Allow meta abstractions to spawn children when counterexamples appear, recovering diversity

The failure of EXP-003 is informative: hierarchical merging works mechanically but may be ecologically unsafe without diversity preservation mechanisms.

---

## Severity

| Dimension | Assessment |
|-----------|------------|
| Mechanical failure | None — merge and genealogy worked as designed |
| Ecological failure | Significant — diversity collapsed |
| Hypothesis impact | Supports H38; challenges unchecked H9 application |
| Urgency for next experiment | High — graph communities before deeper trees |

---

## Conclusion

EXP-003 succeeded as an engineering test of hierarchical question evolution and failed as a model of healthy question ecology. Over-abstraction concentrated attention at the apex and demoted the diversity that originally drove curiosity. Future work should treat this failure mode as a first-class design constraint.
