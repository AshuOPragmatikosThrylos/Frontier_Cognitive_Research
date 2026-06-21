# EXP-011 Code Analysis

Post-experiment read-only analysis of minimal worlds comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-011)

---

## Files Involved

| File | Role in EXP-011 |
|------|-----------------|
| `experiments/exp011_minimal_worlds.py` | Four-world driver; progressive reduction and comparison reporting |
| `src/curiosity_engine.py` | Prediction failure handling (Worlds A, B) |
| `src/world_model.py` | Bird → fly, Dog → bark rules (Worlds A, B) |
| `src/question_repository.py` | Question storage (Worlds A, B) |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass (available, not directly instantiated) |

All four-world logic lives in the experiment file. No `src/` modules modified. Prior experiment files untouched.

---

## Execution Flow

### Phase 0: Constants and shared observations

```python
ALL_OBSERVATIONS = BIRD_CONFORMING + BIRD_CONTRADICTING + MAMMAL_CONTRADICTING  # 10 total
DIFFERENCE_MIN_PER_GROUP = 2
PRESSURE_SPLIT_LIMIT = 1.0  # World A only
```

### Phase 1: Run four worlds independently

Each `run_*_world()` returns an isolated `WorldResult` — no cross-world state.

```python
results = [
    run_ecosystem_world(),      # A
    run_no_communities_world(), # B
    run_no_questions_world(),   # C
    run_difference_world(),     # D
]
```

### Phase 2: Four-column comparison reporting

Six print functions compare all worlds side-by-side:

1. Structures
2. State diversity
3. Speciation-like events
4. Organization detail
5. Summary statistics (minimal ingredient matrix)
6. Overall observations

Fully deterministic — no random module.

---

## World A (Ecosystem)

`run_ecosystem_world()` — reimplements EXP-009 adaptive tolerance logic.

### Components

- `QuestionRepository` + `CuriosityEngine` + `WorldModel`
- `make_initial_communities()` — Bird (tolerance 1.5, expectation fly), Mammal (tolerance 4.0, expectation ground)
- `process_ecosystem_observation()` — conforming vs contradicting paths
- `try_ecosystem_splits()` — pressure-triggered semantic split

### Phases

1. Bird conforming (×4) → conforming questions
2. Bird contradicting (×4) → contradictions, then split check
3. Mammal contradicting (×2) → contradictions, then split check

### Expected outcome

- 1 speciation event: Bird → Bird.Conforming + Bird.Contradicting
- Mammal stable (pressure 0.0)
- 10 questions, 4 communities (2 parent + 2 children with members)

---

## World B (No Communities)

`run_no_communities_world()` — questions without organizational layer.

### Components

- `QuestionRepository` + `CuriosityEngine` + `WorldModel`
- No `Community` dict
- `add_flat_question()` — creates ACTIVE question with category and observed_behavior only (no expected_behavior, no community membership)

### Processing

```python
for entity, category, behavior in ALL_OBSERVATIONS:
    observe(engine, world_model, entity, category, behavior)
    add_flat_question(repository, entity, category, behavior)
```

Single loop over all 10 observations. No split logic. No phase boundaries.

### Expected outcome

- 10 flat questions
- 0 speciation events
- 1 structural unit (`flat_questions`)
- Organization label: `"flat questions (no structure)"`

---

## World C (No Questions)

`run_no_questions_world()` — raw observation storage only.

### Components

- No repository, no engine, no world model
- String list only

### Processing

```python
for entity, category, behavior in ALL_OBSERVATIONS:
    observations.append(f"{entity} ({category}): {behavior.lower()}")
```

### Expected outcome

- 0 questions
- 10 observation strings
- 0 speciation events
- Organization label: `"raw observations only"`

Simplest world — no cognitive machinery invoked.

---

## World D (Difference)

`run_difference_world()` — minimal behavior-based grouping.

### Components

- `category_index: dict[str, dict[str, list[str]]]` — category → behavior → entity names
- `BehaviorGroup` dataclass — lightweight group (no tolerance, debt, expectation)
- `register_behavior()` — append entity to behavior bucket
- `try_difference_split()` — partition when ≥2 behaviors each with ≥2 members

### Split condition

```python
if len(groups) < 2:
    return
if not all(len(members) >= DIFFERENCE_MIN_PER_GROUP for members in groups.values()):
    return
```

### Phases

1. Register bird conforming + contradicting → `try_difference_split("Bird")`
2. Register mammal contradicting → `try_difference_split("Mammal")`

### Expected outcome

- Bird: fly (4) + not fly (4) → split → Bird.fly, Bird.not_fly
- Mammal: fly (1) + swim (1) → no split (min_per_group=2 unmet)
- 1 speciation event
- 0 questions, 0 communities
- Organization label: `"semantic groups (behavior difference)"`

Group names use `behavior_key()` — spaces replaced with underscores (`not_fly`).

---

## Comparison Methodology

### Unified result container

```python
@dataclass
class WorldResult:
    label: str
    world_id: str  # A, B, C, D
    communities: dict[str, Community]
    behavior_groups: dict[str, BehaviorGroup]
    speciation_events: list[str]
    repository: QuestionRepository | None
    observations: list[str]
```

Each world populates only relevant fields; others remain empty defaults.

### Four-column layout

```python
print_comparison_row(label, [value_a, value_b, value_c, value_d], width=18)
```

All comparison functions accept `list[WorldResult]` and iterate uniformly — extensible pattern from EXP-010's two-column design.

---

## Structure Counts

`structure_count(result)` — world-type-aware counting:

| World | Count logic | Expected |
|-------|-------------|----------|
| A | `len(communities)` | 4 |
| B | 1 (flat_questions) | 1 |
| C | 1 (observation_log) | 1 |
| D | `len(behavior_groups)` | 2 |

`leaf_structures(result)` — names of terminal organizational units:

| World | Leaves |
|-------|--------|
| A | Bird.Conforming, Bird.Contradicting, Mammal |
| B | flat_questions |
| C | observation_log |
| D | Bird.fly, Bird.not_fly |

---

## State Diversity

Measured only where questions exist (Worlds A, B):

```python
def state_diversity(result):
    return len(question_state_counts(result))
```

| World | Distinct states | Expected |
|-------|-----------------|----------|
| A | 1 (ACTIVE) | 1 |
| B | 1 (ACTIVE) | 1 |
| C | 0 | 0 |
| D | 0 | 0 |

World D achieves organization with zero state diversity — decoupling organization from question-state entropy (cf. EXP-010 H93).

---

## Speciation Events

`speciation_events` list used across Worlds A and D only.

| World | Events | Content |
|-------|--------|---------|
| A | 1 | `Bird split -> [Bird.Conforming, Bird.Contradicting] (pressure=1.10, tolerance=2.90)` |
| B | 0 | — |
| C | 0 | — |
| D | 1 | `Bird difference split -> [Bird.fly, Bird.not_fly] (min_per_group=2)` |

`print_speciation_comparison()` aligns events by index across all four worlds, printing `(none)` where absent.

Summary matrix includes Bird partition flag per world:

```python
"yes" if any("Bird" in event for event in result.speciation_events) else "no"
```

Expected: A=yes, B=no, C=no, D=yes.

---

## Organization Metrics

`organization_label(result)` — coarse classification per world:

| World ID | Label |
|----------|-------|
| A | `semantic speciation (pressure)` |
| B | `flat questions (no structure)` |
| C | `raw observations only` |
| D | `semantic groups (behavior difference)` |

`print_organization_comparison()` prints label row plus per-world detail:

- A: community member lists (question IDs)
- B: flat question list with states
- C: observation strings
- D: behavior group entity lists

### Minimal ingredient matrix

`print_summary_statistics()` reports yes/no for:

- Communities present
- Questions present
- Bird partition achieved

Enables direct necessity analysis across worlds.

---

## Helper Metrics Summary

| Function | Purpose |
|----------|---------|
| `question_count()` | Questions in repository |
| `question_state_counts()` | State histogram |
| `state_diversity()` | Distinct state count |
| `structure_count()` | Organizational units |
| `leaf_structures()` | Terminal structure names |
| `organization_label()` | Qualitative organization class |

---

## Architectural Notes

### Progressive reduction design

Each world removes one layer:

```
A: observations → questions → communities → pressure → splits
B: observations → questions (stop)
C: observations (stop)
D: observations → behavior index → difference splits (no questions)
```

World D is not a subset of World A — it bypasses questions entirely and uses a parallel minimal path.

### No shared state between worlds

Each run creates fresh objects. Fair comparison: identical inputs, independent processing.

### Determinism

No `random` module. World D split order uses `sorted(groups.items())` for reproducible group creation.

---

## Overall Assessment

EXP-011 is structurally sound as a reduction experiment. It extends EXP-010's comparison methodology from two worlds to four, with a unified `WorldResult` container accommodating heterogeneous world types.

Strengths:

- Clean progressive stripping (A → B → C on one axis; D on a parallel minimal axis)
- Four-column comparison scales the EXP-010 pattern
- Minimal ingredient matrix directly answers necessity questions
- World D isolates behavior-difference as smallest tested organizing principle

Weaknesses (see failures file):

- World D's split threshold (`DIFFERENCE_MIN_PER_GROUP = 2`) is externally imposed
- Only one minimal world design tested (behavior grouping)
- Questions not tested as emergent from differences
- "Cognition" not defined — organization used as proxy

The code successfully implements the experimental intent: attack mechanism necessity through simplification, compare structures/states/speciation/organization across four worlds, and report which primitives survive reduction.

Bird partitioning survives in A and D; questions alone (B) and observations alone (C) do not organize. This is the central empirical finding the comparison layer captures.
