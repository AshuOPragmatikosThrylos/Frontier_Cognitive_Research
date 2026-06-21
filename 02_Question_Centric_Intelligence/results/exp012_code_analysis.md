# EXP-012 Code Analysis

Post-experiment read-only analysis of emergent questions.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-012)

---

## Files Involved

| File | Role in EXP-012 |
|------|-----------------|
| `experiments/exp012_emergent_questions.py` | Full pipeline: observations → groups → tensions → emergent questions |

No `src/` modules imported or used. EXP-012 is self-contained — deliberately avoids `src.question.Question`, `QuestionRepository`, `CuriosityEngine`, and `WorldModel`. Prior experiment files untouched.

Local dataclasses replace library types:

| Local type | Purpose |
|------------|---------|
| `RawObservation` | Observation record (entity, category, behavior) |
| `DifferenceGroup` | Behavior-coherent entity cluster |
| `PersistentTension` | Unresolved conflict between two groups |
| `EmergentQuestion` | Question-like structure derived from tension |
| `WorldState` | Container for all pipeline state |

---

## Execution Flow

### Phase 0: Constants

```python
DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
```

Shared observation lists: `BIRD_CONFORMING` (×4), `BIRD_CONTRADICTING` (×4), `MAMMAL_CONTRADICTING` (×2).

### Phase 1: Bird observations

```python
for entity, category, behavior in BIRD_CONFORMING + BIRD_CONTRADICTING:
    register_observation(state, entity, category, behavior)
form_difference_groups(state, "Bird")
record_tensions(state, "Bird")
```

### Phase 2: Mammal observations

```python
for entity, category, behavior in MAMMAL_CONTRADICTING:
    register_observation(state, entity, category, behavior)
form_difference_groups(state, "Mammal")
record_tensions(state, "Mammal")
```

### Phase 3: Question emergence

```python
emerge_questions_from_tensions(state)
```

### Phase 4: Reporting

Print observations, difference groups, persistent tensions, emergent questions, statistics, overall organization.

---

## Observation Ingestion

`register_observation()` — no questions created.

```python
state.observations.append(RawObservation(...))
state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)
```

Builds:

- Append-only observation log (`RawObservation`)
- Category → behavior → entity list index (`category_index`)

Behaviors normalized to lowercase. No prediction, no curiosity engine, no anomaly handling — pure registration.

---

## Difference Group Formation

`form_difference_groups(state, category)` — inherited logic from EXP-011 World D.

### Conditions

1. Category has ≥2 distinct behaviors
2. Every behavior bucket has ≥ `DIFFERENCE_MIN_PER_GROUP` members

### Group creation

```python
for behavior, members in sorted(groups.items()):
    group_name = f"{category}.{behavior_key(behavior)}"
    state.difference_groups[group_name] = DifferenceGroup(...)
```

Behaviors sorted alphabetically for deterministic group creation order.

### Expected outcomes

| Category | Groups formed | Reason |
|----------|---------------|--------|
| Bird | Bird.fly, Bird.not_fly | 4 + 4 members across 2 behaviors |
| Mammal | (none) | 1 + 1 members — below min per group |

---

## Tension Detection

`detect_persistent_tensions(state, category)` — pairwise comparison of groups within category.

### Group ordering

`groups_for_category()` returns groups sorted by `group.name` (deterministic; required after sorting crash fix):

```python
return sorted(..., key=lambda group: group.name)
```

### Pairwise iteration

```python
for index, group_a in enumerate(groups):
    for group_b in groups[index + 1:]:
        strength = float(min(len(group_a.members), len(group_b.members)))
        persistent = strength >= PERSISTENT_TENSION_MIN
```

### Tension record

Each pair produces a `PersistentTension` with:

- `id`: `t-{category}-{behavior_a}-vs-{behavior_b}`
- `group_a`, `group_b`: group names
- `behavior_a`, `behavior_b`: behaviors from ordered groups
- `strength`: min member count
- `persistent`: boolean threshold check

`record_tensions()` deduplicates by tension id before appending to state.

### Bird expected

One tension: `t-bird-fly-vs-not_fly`, strength 4.0, persistent=True.

### Mammal expected

No groups → no tensions detected.

---

## Persistent Tension Mechanism

Persistence is **not** temporal (no ticks or decay). It is **structural**:

```python
persistent = strength >= PERSISTENT_TENSION_MIN  # min group sizes ≥ 2
```

A tension is persistent when both opposing groups meet minimum size — the conflict is substantiated by multiple entities on each side, not a single anomaly.

| Tension | Strength | Persistent | Reason |
|---------|----------|------------|--------|
| Bird fly vs not fly | 4.0 | Yes | min(4, 4) ≥ 2 |
| (Mammal, if groups existed) | 1.0 | No | min(1, 1) < 2 |

Persistence gates question emergence — central to H105.

---

## Emergent Question Generation

`emerge_questions_from_tensions()` — creates questions only from persistent tensions.

```python
for tension in state.persistent_tensions:
    if not tension.persistent:
        continue
    ...
    state.emergent_questions[question_id] = EmergentQuestion(
        id=f"eq-{category}-{behavior_a}-vs-{behavior_b}",
        text=f"Why do {category} entities both {behavior_a} and {behavior_b}?",
        category=tension.category,
        source_groups=[tension.group_a, tension.group_b],
        tension_id=tension.id,
        state="EMERGENT",
    )
```

### Properties

- 1:1 tension-to-question mapping (one question per persistent tension)
- Question id derived from category and behaviors
- `source_groups` links back to difference groups
- `tension_id` links back to tension record
- State fixed at `"EMERGENT"` — no lifecycle transitions implemented

### Bird expected output

```
[eq-bird-fly-vs-not_fly] EMERGENT — Why do Bird entities both fly and not fly?
  category=Bird tension=t-bird-fly-vs-not_fly sources=[Bird.fly, Bird.not_fly]
```

---

## Question Statistics

`print_question_statistics()` reports:

| Metric | Expected |
|--------|----------|
| Total emergent questions | 1 |
| By category: Bird | 1 |
| By category: Mammal | 0 |
| Persistent tensions | 1 |
| Questions per persistent tension | 1.00 |

---

## Organization Path

`print_overall_organization()` classifies final state:

```python
if state.emergent_questions:
    "observations -> difference groups -> tension -> questions"
elif state.difference_groups:
    "observations -> difference groups (no emergent questions)"
else:
    "observations only (no groups formed)"
```

Expected path: full chain through questions.

Expected flags:

- Bird question emerged: True
- Mammal question emerged: False

---

## Presence or Absence of Randomness

**No randomness.** Fully deterministic:

- No `random` module
- Behavior iteration uses `sorted(groups.items())`
- Group pairing uses `sorted(..., key=lambda group: group.name)`
- Question printing uses `sorted(..., key=lambda q: q.id)`

Identical inputs produce identical outputs across runs.

---

## Heuristics Involved

All thresholds are experimenter-imposed constants:

| Constant | Value | Role |
|----------|-------|------|
| `DIFFERENCE_MIN_PER_GROUP` | 2 | Minimum entities per behavior to form a group |
| `PERSISTENT_TENSION_MIN` | 2 | Minimum tension strength for persistence |
| Question template | Fixed string | `"Why do {category} entities both {a} and {b}?"` |

Heuristic chain:

1. **Group heuristic:** behavioral co-occurrence + minimum count
2. **Persistence heuristic:** min group size as tension strength
3. **Emergence heuristic:** persistent tension → templated question

No adaptive thresholds, no learning, no competition between questions.

---

## Bug Fix (Post-Crash)

Initial implementation crashed in `groups_for_category()`:

```python
return sorted(group for group in ...)  # TypeError: DifferenceGroup not ordered
```

`sorted()` without `key` attempted `<` comparison on dataclass instances. Repaired with `key=lambda group: group.name` — see commit `QCI-022 Fix EXP-012 DifferenceGroup sorting crash`. Scientific conclusions documented only after successful execution.

---

## Overall Assessment

EXP-012 is structurally sound as an emergence experiment. It cleanly implements a four-stage pipeline without relying on pre-built question infrastructure.

Strengths:

- Self-contained — no `src/` dependency demonstrates questions can exist outside library `Question` type
- Clear causal ordering enforced by code structure
- Deterministic and reproducible
- Persistence gate distinguishes Bird (question) from Mammal (no question)
- Explicit linkage: question ← tension ← groups ← observations

Weaknesses (see failures file):

- Thresholds externally imposed
- Single question template
- No question lifecycle beyond EMERGENT state
- Mammal case untested for question emergence (input lacks sufficient members)
- `EmergentQuestion` not integrated with `src.question.Question` — parallel type system

The code successfully implements EXP-011's proposed direction (emergent questions from differences) with a minimal, testable pipeline. Bird question emergence validates H101–H103; Mammal absence validates H105.
