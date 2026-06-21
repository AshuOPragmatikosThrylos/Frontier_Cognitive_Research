# EXP-008 Failures

Post-experiment failure analysis for contradiction pressure.

Date: 2026-06-21  
Experiment: EXP-008 Contradiction Pressure

---

## Failure Analysis

No mechanical failure was observed. Contradiction debt accumulated correctly, pressure reached the split limit, Bird divided into Conforming and Contradicting subcommunities, and child communities emerged with zero operational debt.

EXP-008 improves on EXP-007 by replacing diversity counting with contradiction accumulation. The central limitation persists in a softer form: **split timing remains externally controlled**.

---

## Current Limitation

Speciation still depends on explicit thresholds.

```python
PRESSURE_SPLIT_LIMIT = 4.0

def should_split_by_pressure(community):
    return community.contradiction_debt >= PRESSURE_SPLIT_LIMIT
```

Equivalent to:

```python
if contradiction_pressure > threshold:
    split()
```

Threshold values remain externally imposed.

---

## What This Means

### Communities do not yet determine their own tolerance

The Bird community cannot:
- Raise or lower its split tolerance based on internal state
- Tolerate higher contradiction load when resources permit
- Split early under accelerating contradiction rate
- Resist split when members benefit from coexistence

Split occurs exactly when experimenter-defined limit is reached — four contradictions at +1.0 each. A fifth conforming observation would not reduce pressure; a third conforming bird before flightless arrivals would not prevent eventual split.

### Improvement over EXP-007, not elimination of control

| Experiment | Split trigger | Naturalness |
|------------|---------------|-------------|
| EXP-007 | `behavior_types >= 2` AND `count >= 2` per type | Low — counts diversity |
| EXP-008 | `contradiction_debt >= 4.0` | Medium — tracks violations |

EXP-008's trigger is **more principled** — tied to expectation violations (H71) — but still a constant set by the experimenter.

---

## Related Limitations

1. **Uniform increment.** All contradictions add 1.0 regardless of severity, entity importance, or recurrence.

2. **No debt decay.** Conforming observations do not reduce contradiction debt — only split resets children.

3. **Single split pass.** No repeated pressure cycles or re-merge under low tension.

4. **Parent retains debt.** Bird parent keeps 4.0 debt after split — ambiguous whether parent is "still under pressure" or merely historical.

5. **Binary partition.** Only Conforming vs Contradicting — no partial tolerance or graded responses.

6. **No cross-community propagation.** Contradictions in Bird do not affect Mammal or Capability communities (not present in this experiment).

---

## Potential Future Solutions

### Adaptive thresholds

Tolerance derived from community size, member debt, or historical split frequency:

```python
threshold = base_tolerance * len(members) * coherence_factor
```

### Competition-driven tolerance

Communities under attention competition (EXP-006) split when internal contradiction impedes fitness.

### Attention-driven tolerance

Communities split when contradiction debt prevents effective use of attention budget (EXP-005).

### Self-organized pressure regulation

Replace constant with endogenous dynamics:
- Contradiction rate (debt per observation window)
- Internal `contradicts` edge density in question graph
- Compression failure rate against community expectation
- Member voting or fitness-weighted split decision

Goal: communities determine their own tolerance — H79 candidate.

---

## Is This a Bug?

**No.** Code matches design. Four contradictions at limit 4.0 → split. Deterministic and correct.

The issue is **model maturity** — same class of limitation as EXP-007 failures, partially addressed but not resolved.

---

## Comparison Across Speciation Experiments

| Property | EXP-007 | EXP-008 |
|----------|---------|---------|
| Trigger | Diversity count | Contradiction debt |
| Conceptual basis | Behavior variety | Expectation violation |
| External constant | `DIVERSITY_SPLIT_THRESHOLD` | `PRESSURE_SPLIT_LIMIT` |
| Self-organized | No | No |
| Pressure relief on split | Homogeneous children | Zero debt children |
| Scientific naturalness | Handcrafted | Improved |

---

## Overall Assessment

Contradiction pressure appears significantly more natural than diversity thresholds, but external control remains present.

Reducing externally imposed thresholds should become a major future objective.

EXP-008 validates the **contradiction → pressure → speciation** causal chain (H71–H75). The next step is **adaptive tolerance** — who decides acceptable contradiction levels, and can that decision emerge from community state rather than experimenter constants?

---

## Severity

| Dimension | Assessment |
|-----------|------------|
| Mechanical failure | None |
| Conceptual limitation | Moderate — threshold still external |
| Scientific advance over EXP-007 | Significant |
| Urgency for adaptive tolerance | High |

---

## Conclusion

EXP-008 did not fail. It demonstrated that contradiction pressure drives speciation more naturally than diversity counting, while exposing that `PRESSURE_SPLIT_LIMIT = 4.0` is still an experimenter's hand on the scale.

The path forward: self-organized pressure regulation where communities own their tolerance — connecting contradiction (H71), attention (H46), and competition (H55) into a unified evolutionary economy.

Handcrafted thresholds are a stepping stone. Adaptive tolerance is the destination.
