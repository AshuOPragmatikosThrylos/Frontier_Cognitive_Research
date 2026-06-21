# EXP-009 Code Analysis

Post-experiment read-only analysis of adaptive contradiction tolerance.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-009)

---

## Files Involved

| File | Role in EXP-009 |
|------|-----------------|
| `experiments/exp009_adaptive_tolerance.py` | Experiment driver; adaptive tolerance and relative pressure |
| `src/curiosity_engine.py` | Anomaly question creation |
| `src/world_model.py` | Bird → fly, Dog → bark rules |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

All adaptive tolerance logic lives in the experiment file. No `src/` modules modified.

---

## Execution Flow

### Phase 0: Initialize

```python
INITIAL_TOLERANCES = {"Bird": 1.5, "Mammal": 4.0}
TOLERANCE_LEARN_RATE = 0.35
PRESSURE_SPLIT_LIMIT = 1.0
CONTRADICTION_INCREMENT = 1.0
```

Two communities with different expectations and tolerances.

### Phase 1: Bird conforming (×4)

Flying birds match expectation `fly`. Conforming questions created. No debt or tolerance change.

`log_tolerances("after bird conforming")`

### Phase 2: Bird contradicting (×4)

Flightless birds violate expectation. Each calls `record_contradiction()`:

- debt += 1.0
- tolerance += 0.35
- contradiction logged

`try_split_all("after bird contradictions")` — Bird pressure 1.1 ≥ 1.0 → split.

### Phase 3: Mammal contradicting (×2)

Bat flies, Whale swims — both violate Mammal expectation `ground`.

`try_split_all("after mammal contradictions")` — Mammal pressure 0.0 → no split.

### Phase 4: Reporting

Print tolerances, debt, pressure, speciation, structures, statistics, question states.

---

## Tolerance Mechanism

```python
@dataclass
class Community:
    contradiction_tolerance: float  # mutable, per community
```

Each community maintains its own tolerance value, initialized from `INITIAL_TOLERANCES`:

| Community | Initial |
|-----------|---------|
| Bird | 1.5 |
| Mammal | 4.0 |

Tolerance is **community-level personality** — not global constant (contrast EXP-008).

---

## Tolerance Learning

On each contradiction:

```python
community.contradiction_tolerance += TOLERANCE_LEARN_RATE  # 0.35
```

Conforming observations do **not** increase tolerance — only contradictory experience teaches flexibility.

### Bird learning trajectory

| Contradictions | Tolerance |
|----------------|-----------|
| 0 | 1.5 |
| 1 | 1.85 |
| 2 | 2.20 |
| 3 | 2.55 |
| 4 | 2.90 |

Total learning: +1.40 (93% increase from initial).

### Mammal learning trajectory

| Contradictions | Tolerance |
|----------------|-----------|
| 0 | 4.0 |
| 1 | 4.35 |
| 2 | 4.70 |

Total learning: +0.70 (18% increase from initial).

---

## Contradiction Debt Accumulation

```python
community.contradiction_debt += CONTRADICTION_INCREMENT  # 1.0 per contradiction
```

Independent of tolerance learning — debt and tolerance increase in parallel on each contradiction.

| Community | Final debt |
|-----------|------------|
| Bird (parent) | 4.0 |
| Bird.Conforming | 0.0 |
| Bird.Contradicting | 0.0 |
| Mammal | 2.0 |

Children start with fresh debt after split; parent retains historical debt.

---

## Pressure Calculations

```python
def pressure_level(community):
    return max(0.0, community.contradiction_debt - community.contradiction_tolerance)
```

**Key advance over EXP-008:** pressure is **relative** — excess debt beyond what tolerance absorbs.

### Bird at split

```
pressure = max(0, 4.0 - 2.9) = 1.1
1.1 >= PRESSURE_SPLIT_LIMIT (1.0) → split
```

Without learning (tolerance stuck at 1.5): pressure would be 2.5 — learning reduced pressure by 56% but insufficient to prevent split.

### Mammal after 2 contradictions

```
pressure = max(0, 2.0 - 4.7) = 0.0
```

Tolerance exceeds debt — contradictions exist, pressure absent.

---

## Speciation Events

Split condition:

```python
def should_split(community):
    return pressure_level(community) >= PRESSURE_SPLIT_LIMIT
```

One speciation event expected:

```
Bird split -> [Bird.Conforming, Bird.Contradicting] (pressure=1.10, tolerance=2.90)
```

Split mechanics inherited from EXP-008 — partition by expectation match, create children, clear parent members.

---

## Tolerance Inheritance

```python
child = Community(
    ...
    contradiction_tolerance=parent.contradiction_tolerance,
    ...
)
```

At split time, children receive parent's **current** tolerance (2.9), not initial (1.5).

Both Bird.Conforming and Bird.Contradicting inherit identical tolerance — personality passed to offspring (H84).

Mammal never split — no child inheritance demonstrated for Mammal.

---

## Community Structures

### Final expected structure

| Community | Members | Parent |
|-----------|---------|--------|
| Bird | 0 | — |
| Bird.Conforming | 4 flying | Bird |
| Bird.Contradicting | 4 flightless | Bird |
| Mammal | 2 (Bat, Whale) | — |

---

## Community Statistics

Printed per community:
- current tolerance
- member count
- contradiction_debt
- member curiosity_debt (sum)
- pressure level

Enables comparison of organizational debt vs question-level curiosity debt.

---

## Question States

| Source | State |
|--------|-------|
| Conforming birds (manual) | ACTIVE |
| Contradicting birds/mammals (engine) | NEW |

Ten questions total (8 bird + 2 mammal). States unchanged by split — community reassignment only.

---

## Presence or Absence of Randomness

| Source | Present? |
|--------|----------|
| `random` | No |
| `uuid` | No |
| Deterministic parameters | Yes |
| Fixed observation order | Yes |
| Alphabetical tie-breaks | N/A |

**Fully deterministic.**

---

## Heuristics Involved

| Heuristic | Value / rule |
|-----------|--------------|
| Bird initial tolerance | 1.5 |
| Mammal initial tolerance | 4.0 |
| Learn rate | +0.35 per contradiction |
| Debt increment | +1.0 per contradiction |
| Pressure formula | max(0, debt - tolerance) |
| Split trigger | pressure ≥ 1.0 |
| Tolerance inheritance | copy parent at split |
| Conforming path | no debt, no learning |

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed initial tolerances, learn rate, and split limit — but **relative pressure** introduces community-specific dynamics.

**D — Emergent from interactions** (partial)

Mammal stability vs Bird split emerges from tolerance/debt interaction without separate rules per community.

### Progression across experiments

| EXP | Split driver |
|-----|--------------|
| EXP-007 | Diversity count |
| EXP-008 | Absolute debt ≥ limit |
| EXP-009 | Relative pressure ≥ limit + adaptive tolerance |

Each step increases naturalism.

### Key findings

| Property | Finding |
|----------|---------|
| Adaptive tolerance | Works — increases with experience |
| Relative pressure | Same contradictions, different outcomes |
| Personality | Initial tolerance shapes fate |
| Learning vs split | Complementary (H86), not opposing |
| Inheritance | Children receive parent tolerance |
| External control | PRESSURE_SPLIT_LIMIT still fixed |

### Conclusion

EXP-009 code implements the most naturalistic speciation trigger in the series to date. Tolerance learning and relative pressure produce distinct community personalities and differentiated outcomes. External split threshold remains the primary unresolved control — documented in failures analysis.

Adaptive tolerance produced significantly richer dynamics than EXP-008 fixed limits.
