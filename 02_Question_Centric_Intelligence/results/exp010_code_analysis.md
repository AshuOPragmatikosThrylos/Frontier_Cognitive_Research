# EXP-010 Code Analysis

Post-experiment read-only analysis of random worlds comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-010)

---

## Files Involved

| File | Role in EXP-010 |
|------|-----------------|
| `experiments/exp010_random_worlds.py` | Dual-world driver; pressure control, random control, comparison reporting |
| `src/curiosity_engine.py` | Anomaly question creation on prediction failure |
| `src/world_model.py` | Bird → fly, Dog → bark rules |
| `src/question_repository.py` | Question storage per world (separate instances) |
| `src/question.py` | Question dataclass with mutable `state` |
| `src/observation.py` | Observation dataclass (available, not directly instantiated) |

All dual-world and comparison logic lives in the experiment file. No `src/` modules modified. Prior experiment files untouched.

---

## Execution Flow

### Phase 0: Constants and shared observations

```python
INITIAL_TOLERANCES = {"Bird": 1.5, "Mammal": 4.0}
TOLERANCE_LEARN_RATE = 0.35
PRESSURE_SPLIT_LIMIT = 1.0
CONTRADICTION_INCREMENT = 1.0

RANDOM_SEED = 42
RANDOM_SPLIT_CHANCE = 0.25
RANDOM_STATE_CHANGE_CHANCE = 0.15
QUESTION_STATES = ["ACTIVE", "DORMANT", "PARTIALLY_RESOLVED", "NEW"]
```

Shared observation lists: `BIRD_CONFORMING` (×4), `BIRD_CONTRADICTING` (×4), `MAMMAL_CONTRADICTING` (×2).

### Phase 1: Run World A

`run_pressure_world()` — isolated state (repository, communities, speciation_events, tolerance_log).

1. Bird conforming observations → conforming questions, log tolerances
2. Bird contradicting observations → contradictions, `try_pressure_splits()`
3. Mammal contradicting observations → contradictions, `try_pressure_splits()`
4. Return `WorldResult` snapshot

### Phase 2: Run World B

`run_random_world()` — fresh isolated state with `random.Random(RANDOM_SEED)`.

Same observation sequence; after each observation, `apply_random_state_changes()`. At checkpoints, `try_random_splits()` instead of pressure splits.

### Phase 3: Side-by-side reporting

Six comparison print functions plus summary statistics. No mutation after world runs complete.

---

## Pressure World Mechanism (World A)

Reimplements EXP-009 adaptive tolerance logic with per-run state (no module-level globals).

### Observation processing

- Conforming behavior → `add_conforming_question()` (state ACTIVE)
- Contradicting behavior → `record_contradiction()` (debt += 1.0, tolerance += 0.35)

### Pressure calculation

```python
def pressure_level(community):
    return max(0.0, community.contradiction_debt - community.contradiction_tolerance)
```

### Split decision

```python
if community.members and pressure_level(community) >= PRESSURE_SPLIT_LIMIT:
    split_by_contradiction(..., trigger="pressure")
```

### Semantic split

Members partitioned by `question.observed_behavior == parent.expectation`:

- Conforming → `{parent}.Conforming`
- Contradicting → `{parent}.Contradicting` (expectation `"anomaly"`)

Children inherit parent tolerance. Parent members cleared.

---

## Random World Mechanism (World B)

Shares observation processing and debt/tolerance accumulation with World A — both worlds track the same contradiction statistics. Divergence occurs only in split triggers and state mutations.

### Split decision

```python
if community.members and rng.random() < RANDOM_SPLIT_CHANCE:
    split_randomly(...)
```

Evaluated at two checkpoints: after bird contradictions, after mammal contradictions. Each community with members gets an independent Bernoulli trial (p = 0.25).

### Random splitting

```python
rng.shuffle(members)
midpoint = len(members) // 2
groups = [members[:midpoint], members[midpoint:]]
```

Creates `{parent}.Random1` and `{parent}.Random2`. No behavioral semantics — arbitrary partition. Requires ≥ 2 members.

### Random state changes

Applied after **every** observation in World B only:

```python
for question in repository.get_all_questions():
    if rng.random() < RANDOM_STATE_CHANGE_CHANCE:
        question.state = rng.choice(QUESTION_STATES)
```

15% chance per question per observation step to reassign state uniformly from four possible values.

---

## Side-by-Side Comparison Methodology

Both worlds produce a `WorldResult` dataclass:

```python
@dataclass
class WorldResult:
    label: str
    communities: dict[str, Community]
    speciation_events: list[str]
    repository: QuestionRepository
    tolerance_log: list[dict]
```

Comparison functions accept `(world_a, world_b)` and print aligned columns:

| Function | Compares |
|----------|----------|
| `print_community_structures_comparison` | Community count, leaf communities, per-community member lists |
| `print_speciation_comparison` | Speciation count, event-by-event alignment |
| `print_community_statistics_comparison` | Tolerance, members, debt, curiosity debt, pressure per community |
| `print_question_states_comparison` | State counts; per-question diffs where states diverge |
| `print_evolution_patterns_comparison` | Pattern label (`evolution_pattern()`), tolerance history pressures |
| `print_summary_statistics` | Phenomenon reproduction flags, state diversity, interpretation |

Helper metrics:

- `community_count()` — total communities in dict
- `leaf_communities()` — communities with non-empty members
- `question_state_counts()` — histogram of question states
- `evolution_pattern()` — coarse label: stable, selective speciation, multi-speciation

---

## Community Structures

### World A (deterministic)

After full run, expected structure matches EXP-009:

```
Bird (members cleared after split)
├── Bird.Conforming — 4 flying bird questions
└── Bird.Contradicting — 4 flightless bird questions
Mammal — 2 contradicting members, no split
```

### World B (stochastic)

Structure depends on random split rolls at checkpoints:

- Bird may remain unified (8 members) or split into Bird.Random1 / Bird.Random2
- Mammal typically remains unified (2 members; split requires roll success and ≥ 2 members)
- No Conforming/Contradicting suffixes — random partition only

Comparison prints union of all community names across both worlds, marking absent communities implicitly via empty member lists.

---

## Question States

| World | Initial state | Evolution |
|-------|---------------|-----------|
| A | ACTIVE for conforming; engine-created anomalies may differ | No state mutation after creation |
| B | ACTIVE at creation | Probabilistic reassignment to any of 4 states after each observation |

Comparison reports aggregate counts per state and lists individual questions where A ≠ B.

Expected finding: World B shows higher state diversity (multiple distinct states) while World A concentrates in ACTIVE.

---

## Summary Statistics

`print_summary_statistics()` computes falsification-oriented flags:

```python
a_bird_split = any("Bird" in event for event in world_a.speciation_events)
b_bird_split = any("Bird" in event for event in world_b.speciation_events)
a_mammal_split = any("Mammal" in event for event in world_a.speciation_events)
b_mammal_split = any("Mammal" in event for event in world_b.speciation_events)
```

Reports:

- Bird speciation match (A vs B)
- Mammal stability match (neither split)
- Total speciation counts
- Question state diversity (distinct state count)
- Active question counts
- Interpretation string (reproduction success/failure)

Also prints random parameters (seed, split chance, state change chance) for reproducibility documentation.

---

## Random Seed Usage

```python
rng = random.Random(RANDOM_SEED)  # seed = 42
```

Single seeded `random.Random` instance passed through World B:

- Governs split Bernoulli trials at checkpoints
- Governs member shuffle order in `split_randomly()`
- Governs state change trials and state selection

World A uses no randomness — fully deterministic control.

**Limitation:** One seed, one random world instance. Generalization requires seed sweeps (see `exp010_failures.md`).

---

## Architectural Notes

### State isolation

Each world run creates fresh `QuestionRepository`, `WorldModel`, `CuriosityEngine`, and community dict. Worlds do not interact — fair comparison on identical inputs with independent dynamics.

### Shared vs divergent code paths

Shared: `process_observation()`, `record_contradiction()`, `make_initial_communities()`, debt/tolerance tracking.

Divergent: split trigger (`try_pressure_splits` vs `try_random_splits`), split partition logic (`split_by_contradiction` vs `split_randomly`), state changes (World B only).

### No src/ changes

All control and random logic experimental — consistent with prior EXP-001 through EXP-009 pattern.

---

## Overall Assessment

EXP-010 is structurally sound as a first falsification experiment. It cleanly separates:

1. **Positive control (World A)** — reproduces EXP-009 pressure dynamics in encapsulated form
2. **Null-style control (World B)** — same inputs, random dynamics
3. **Comparison layer** — systematic side-by-side metrics with explicit phenomenon-reproduction flags

Strengths:

- Deterministic World A enables exact replication of prior findings
- Shared observation processing ensures debt/tolerance parity before split divergence
- Comparison output covers structure, speciation, statistics, states, evolution, and summary

Weaknesses (documented in failures file):

- Single random seed
- Single random-world design (no gradient of randomness)
- Random splits ignore behavioral semantics by design — strong null, but not the only possible control

The code successfully implements the experimental intent: test whether random mechanisms reproduce organized phenomena, and report comparative evidence without modifying the core `src/` library or prior experiments.
