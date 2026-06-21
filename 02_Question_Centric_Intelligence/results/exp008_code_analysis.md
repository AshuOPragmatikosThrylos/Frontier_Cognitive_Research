# EXP-008 Code Analysis

Post-experiment read-only analysis of contradiction pressure.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-008)

---

## Files Involved

| File | Role in EXP-008 |
|------|-----------------|
| `experiments/exp008_contradiction_pressure.py` | Experiment driver; contradiction debt and pressure split |
| `src/curiosity_engine.py` | Flightless bird question creation |
| `src/world_model.py` | Bird → fly rule |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

All contradiction pressure logic lives in the experiment file. No `src/` modules modified.

---

## Execution Flow

### Phase 0: Initialize

```python
Bird = Community(name="Bird", expectation="fly")
PRESSURE_SPLIT_LIMIT = 4.0
CONTRADICTION_INCREMENT = 1.0
```

### Phase 1: Conforming observations

For Sparrow, Robin, Eagle, Falcon:

1. `behavior == community.expectation` ("fly")
2. `add_conforming_question()` — manual ACTIVE question
3. No contradiction debt increment

### Phase 2: Contradicting observations

For Penguin, Ostrich, Emu, Kiwi:

1. `behavior != community.expectation`
2. `observe()` → `process_prediction_failure()` — creates anomaly question
3. `contradiction_debt += 1.0`
4. Log contradiction string

### Phase 3: Pressure check and split

```python
if bird.contradiction_debt >= PRESSURE_SPLIT_LIMIT:
    split_by_contradiction(repository, "Bird")
```

Debt 4.0 ≥ limit 4.0 → split.

### Phase 4: Reporting

Print expectations, contradictions, debt, pressure, structures, speciation events, question states.

---

## Expectation Mechanism

Each community carries an `expectation` string:

```python
@dataclass
class Community:
    expectation: str  # Bird: "fly"
```

Observations compared against **community expectation**, not only world model rule:

```python
if behavior == community.expectation:
    # conforming path
else:
    # contradicting path → debt
```

World model and community expectation align initially (`Bird → fly`). Community expectation persists through split — children receive `fly` or `anomaly`.

---

## Contradiction Detection

Contradiction detected when:

```python
behavior != community.expectation
```

Logged as:

```python
f"{entity}: expected {community.expectation}, observed {behavior}"
```

Examples:
- `Penguin: expected fly, observed not fly`
- `Ostrich: expected fly, observed not fly`

Four contradictions total — one per flightless bird.

Conforming path produces no log entry and no debt.

---

## Contradiction Debt Accumulation

```python
CONTRADICTION_INCREMENT = 1.0

community.contradiction_debt += CONTRADICTION_INCREMENT  # per contradiction
```

| Phase | Events | Running debt |
|-------|--------|--------------|
| Conforming (×4) | 0 contradictions | 0.0 |
| Penguin | +1 | 1.0 |
| Ostrich | +1 | 2.0 |
| Emu | +1 | 3.0 |
| Kiwi | +1 | 4.0 |

Debt is monotonic — no decay mechanism before split.

**Separate from curiosity_debt:** entity questions retain their own `curiosity_debt` via CuriosityEngine. Community `contradiction_debt` is a community-level aggregate.

---

## Pressure Calculations

```python
def pressure_level(community):
    return community.contradiction_debt

def should_split_by_pressure(community):
    return community.contradiction_debt >= PRESSURE_SPLIT_LIMIT
```

| Community | Pressure | Status |
|-------------|----------|--------|
| Bird (pre-split) | 4.0 | SPLIT |
| Bird (post-split) | 4.0 | historical |
| Bird.Conforming | 0.0 | stable |
| Bird.Contradicting | 0.0 | stable |

Pressure equals contradiction debt directly — no normalization by member count.

---

## Speciation Mechanism

Triggered by pressure, not diversity count (contrast EXP-007):

```python
# EXP-007: len(behavior_groups) >= 2 and all count >= 2
# EXP-008: contradiction_debt >= PRESSURE_SPLIT_LIMIT
```

### Split execution

1. Partition members by `question.observed_behavior == parent.expectation`
2. Create `Bird.Conforming` (expectation `fly`) and `Bird.Contradicting` (expectation `anomaly`)
3. Move members to children; clear parent members
4. Log speciation event with pressure at split time
5. Children start with fresh `contradiction_debt=0.0`

Parent retains historical debt and contradiction log — organizational memory (H76).

---

## Parent-Child Community Relationships

```
Bird (expectation=fly, debt=4.0, members=0)
├── Bird.Conforming (expectation=fly, debt=0.0, 4 members)
└── Bird.Contradicting (expectation=anomaly, debt=0.0, 4 members)
```

| Community | parent | children |
|-----------|--------|----------|
| Bird | none | Conforming, Contradicting |
| Bird.Conforming | Bird | none |
| Bird.Contradicting | Bird | none |

Same organizational pattern as EXP-007 (H67): empty parent survives as ancestor.

---

## Community Structures

### Pre-split

Bird: 8 members (4 conforming + 4 contradicting), debt 4.0

### Post-split

| Community | Members |
|-----------|---------|
| Bird | (none) |
| Bird.Conforming | q-sparrow, q-robin, q-eagle, q-falcon |
| Bird.Contradicting | q-penguin, q-ostrich, q-emu, q-kiwi |

---

## Question States

| Source | State |
|--------|-------|
| Conforming (manual) | ACTIVE |
| Contradicting (engine) | NEW |

Eight questions total. No state mutation during split — only community membership reassignment via new child communities.

---

## Presence or Absence of Randomness

| Source | Present? |
|--------|----------|
| `random` | No |
| `uuid` | No |
| Deterministic ids | Yes |
| Fixed observation order | Yes |
| Fixed pressure limit | Yes |

**Fully deterministic.**

---

## Heuristics Involved

| Heuristic | Rule |
|-----------|------|
| Expectation | Community-level string comparison |
| Debt increment | +1.0 per contradiction |
| Split trigger | debt ≥ 4.0 (not diversity count) |
| Child naming | Conforming / Contradicting by expectation match |
| Child expectations | fly / anomaly |
| Pressure reset | Children born at 0.0 debt |
| Parent memory | Parent keeps debt + contradiction log |

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed increment, fixed limit, fixed order. Reproducible.

**More natural than EXP-007** (partial emergence)

Split causally linked to expectation violations — closer to H71 (contradictions drive evolution) than behavior-type counting.

**External control remains**

`PRESSURE_SPLIT_LIMIT = 4.0` is experimenter-imposed — see failures doc.

### Key findings

| Property | Finding |
|----------|---------|
| Contradiction debt | Accumulates per violation |
| Split driver | Pressure, not diversity |
| Pressure relief | Children start at 0 debt |
| Parent survival | Empty parent with history |
| vs EXP-007 | More principled trigger |
| vs EXP-010 notes | Implements contradiction-as-tension |

### Conclusion

EXP-008 code implements contradiction-driven speciation as an improvement over diversity thresholds. Expectation → violation → debt → pressure → split forms a coherent causal chain. Threshold remains handcrafted; adaptive tolerance is the next step.

Contradiction pressure appears significantly more natural than diversity thresholds, while sharing EXP-007's limitation of external split control.
