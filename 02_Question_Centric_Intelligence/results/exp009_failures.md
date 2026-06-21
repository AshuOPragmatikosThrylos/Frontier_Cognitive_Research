# EXP-009 Failures

Post-experiment failure analysis for adaptive contradiction tolerance.

Date: 2026-06-21  
Experiment: EXP-009 Adaptive Contradiction Tolerance

---

## Failure Analysis

No mechanical failure was observed. Tolerance adapted correctly, relative pressure calculated correctly, Bird split at pressure 1.1, Mammal stabilized at pressure 0.0, children inherited parent tolerance.

EXP-009 advances significantly over EXP-008 by introducing adaptive tolerance and relative pressure. The remaining limitation is familiar: **ultimate split decisions still use an externally imposed threshold**.

---

## Current Limitation

Pressure thresholds remain externally imposed.

```python
PRESSURE_SPLIT_LIMIT = 1.0

def should_split(community):
    return pressure_level(community) >= PRESSURE_SPLIT_LIMIT
```

Equivalent to:

```python
if pressure > threshold:
    split()
```

Communities still do not determine their own acceptable pressure levels.

---

## What Improved vs EXP-008

| Aspect | EXP-008 | EXP-009 |
|--------|---------|---------|
| Split basis | Absolute debt | Relative pressure |
| Tolerance | None | Adaptive |
| Community personality | None | Initial + learned |
| Same contradictions | Same fate | Different fates possible |

EXP-009 answers **how much pressure** matters relative to tolerance (H83, H85). It does not answer **who sets the split limit**.

---

## What Remains Externally Controlled

1. **PRESSURE_SPLIT_LIMIT = 1.0** — universal across all communities. Bird and Mammal share the same split threshold despite different personalities.

2. **INITIAL_TOLERANCES** — experimenter assigns Bird 1.5, Mammal 4.0. Communities do not self-select starting personality.

3. **TOLERANCE_LEARN_RATE = 0.35** — fixed learning rate for all communities. No variation in adaptability.

4. **CONTRADICTION_INCREMENT = 1.0** — uniform severity for all contradictions.

5. **Split timing** — checked only at predefined phases, not continuously or endogenously.

Tolerance adaptation exists, but ultimate thresholds remain externally controlled.

---

## The Bird Paradox

Bird learned tolerance from 1.5 to 2.9 — substantial adaptation — yet still split. This is scientifically informative:

- Learning **reduced** pressure (from hypothetical 2.5 to actual 1.1)
- Learning **did not prevent** split at limit 1.0
- Adaptation and evolution co-occurred (H86)

A community that adapts is not necessarily a community that avoids speciation. The experimenter's threshold still governs the final decision.

---

## Potential Future Solutions

### Self-organized thresholds

Split limit derived from community state:

```python
split_limit = f(tolerance, member_count, historical_splits)
```

Each community sets its own crisis point.

### Ecosystem-level selection

Communities with poorly calibrated tolerance fail; well-calibrated survive — selection over generations (H79 extended).

### Competition between personalities

Rigid and flexible communities compete for attention (EXP-006); ecosystem favors optimal tolerance distribution.

### Adaptive pressure regulation

- Split limit scales with tolerance (high tolerance → high limit)
- Pressure decay when community investigates contradictions
- Cross-community pressure sharing via bridge communities

Goal: no experimenter constant for `PRESSURE_SPLIT_LIMIT`.

---

## Is This a Bug?

**No.** Bird at pressure 1.1 with limit 1.0 should split. Mammal at pressure 0.0 should not. Code is correct.

The limitation is **model depth** — tolerance adapts, threshold does not.

---

## Overall Assessment

Adaptive tolerance produced significantly richer dynamics than fixed thresholds, but external control remains present.

Reducing externally imposed control should remain a major objective.

The experiment series control reduction arc:

| EXP | External control |
|-----|------------------|
| EXP-007 | Diversity threshold |
| EXP-008 | Absolute debt limit |
| EXP-009 | Pressure limit (tolerance adapts, limit fixed) |
| EXP-010? | Self-organized limit (proposed) |

EXP-009 is the strongest step so far toward endogenous evolution. One constant remains.

---

## Severity

| Dimension | Assessment |
|-----------|------------|
| Mechanical failure | None |
| Conceptual limitation | Moderate — split limit external |
| Advance over EXP-008 | Significant |
| Scientific value | High — relative pressure validated |
| Urgency for self-organized thresholds | High |

---

## Conclusion

EXP-009 did not fail. It demonstrated adaptive tolerance, relative pressure, community personalities, and tolerance inheritance — while confirming that `PRESSURE_SPLIT_LIMIT` is the next control to internalize.

Contradictions become pressure only relative to tolerance (H85). Communities must eventually set their own tolerance for that pressure to become fully endogenous (H79–H86).

Adaptive tolerance is progress. Self-organized thresholds are the next frontier.
