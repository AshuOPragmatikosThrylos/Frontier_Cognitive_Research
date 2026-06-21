# EXP-013 Code Analysis

Post-experiment read-only analysis of question lifecycles and extinction.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-013)

---

## Files Involved

| File | Role in EXP-013 |
|------|-----------------|
| `experiments/exp013_question_extinction.py` | Full pipeline including lifecycle, vitality, resolution, decay, and extinction |

No `src/` modules imported or used. Self-contained like EXP-012. Prior experiment files untouched.

Local dataclasses:

| Type | Role |
|------|------|
| `RawObservation` | Observation record |
| `DifferenceGroup` | Behavior-coherent entity cluster |
| `PersistentTension` | Inter-group conflict (+ `resolved`, `resolution_note`) |
| `LifecycleQuestion` | Question with vitality and lifecycle history |
| `WorldState` | Pipeline state container |

EXP-012's `EmergentQuestion` extended to `LifecycleQuestion` with `vitality` and `lifecycle_history`.

---

## Execution Flow

### Phase 0: Constants

```python
DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0
```

Lifecycle drivers:

```python
TENSION_RESOLUTIONS = [
    ("t-bird-fly-vs-not_fly", "niche specialization resolves bird behavior conflict"),
]
DECAY_STEPS = ["eq-bird-fly-vs-not_fly", "eq-bird-fly-vs-not_fly"]
```

### Phase 1: `ingest_observations()`

EXP-012 logic unchanged:

1. Bird conforming + contradicting observations
2. `form_difference_groups("Bird")`, `record_tensions("Bird")`
3. Mammal contradicting observations
4. `form_difference_groups("Mammal")`, `record_tensions("Mammal")`

### Phase 2: `process_lifecycle()`

```python
emerge_questions_from_tensions(state)
promote_emergent_questions(state)
for tension_id, note in TENSION_RESOLUTIONS:
    resolve_tension(state, tension_id, note)
for question_id in DECAY_STEPS:
    apply_vitality_decay(state, question_id)
```

### Phase 3: Reporting

Print lifecycles, vitality, resolved tensions, extinct questions, statistics, overall organization.

---

## Difference Formation

Identical to EXP-012. `form_difference_groups()` requires ≥2 behaviors with ≥2 members each.

| Category | Result |
|----------|--------|
| Bird | Bird.fly (4), Bird.not_fly (4) |
| Mammal | (none) — 1+1 members |

Groups sorted by behavior key for deterministic creation.

---

## Tension Detection

Identical to EXP-012 with EXP-013 extensions on `PersistentTension`:

```python
resolved: bool = False
resolution_note: str = ""
```

`groups_for_category()` uses `key=lambda group: group.name` (EXP-012 crash fix preserved).

Bird tension: `t-bird-fly-vs-not_fly`, strength 4.0, persistent=True, resolved=False initially.

---

## Emergent Question Generation

`emerge_questions_from_tensions()` — same emergence logic as EXP-012 with vitality initialization:

```python
question = LifecycleQuestion(
    ...
    vitality=tension.strength,  # 4.0 for Bird
    state="EMERGENT",           # default
)
question.lifecycle_history.append(
    f"EMERGENT (vitality={question.vitality:.1f}, tension={tension.id})"
)
```

Initial vitality equals tension strength — links question life force to conflict intensity.

---

## Question Lifecycle States

Five states defined in `apply_lifecycle_state()`:

| State | Entry condition |
|-------|-----------------|
| EMERGENT | Question just created |
| ACTIVE | Promoted while tension unresolved |
| RESOLVED | Tension resolved and vitality > dormant threshold |
| DORMANT | Vitality ≤ 1.0 and > 0 |
| EXTINCT | Vitality ≤ 0 |

State priority (evaluated top-down):

```python
if question.vitality <= 0.0:
    question.state = "EXTINCT"
elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
    question.state = "DORMANT"
elif tension_resolved:
    question.state = "RESOLVED"
elif question.state == "EMERGENT":
    question.state = "EMERGENT"
else:
    question.state = "ACTIVE"
```

DORMANT overrides RESOLVED when vitality falls to threshold — senescence takes precedence over resolution status.

### Bird question lifecycle trace

| Step | Event | Vitality | State |
|------|-------|----------|-------|
| 1 | Emerge | 4.0 | EMERGENT |
| 2 | Promote | 4.0 | ACTIVE |
| 3 | Resolve tension | 2.0 | RESOLVED |
| 4 | Decay 1 | 1.0 | DORMANT |
| 5 | Decay 2 | 0.0 | EXTINCT |

---

## Vitality Calculations

| Event | Formula | Bird example |
|-------|---------|--------------|
| Initial | `vitality = tension.strength` | 4.0 |
| Resolution | `vitality -= RESOLUTION_VITALITY_REDUCTION` | 4.0 - 2.0 = 2.0 |
| Decay | `vitality -= DECAY_VITALITY_REDUCTION` | 2.0 - 1.0 = 1.0; 1.0 - 1.0 = 0.0 |

Vitality is a scalar float; no upper bound enforced after emergence. Only decreases — no regeneration implemented.

---

## Resolution Mechanism

`resolve_tension(state, tension_id, note)`:

1. Mark tension `resolved = True`, store `resolution_note`
2. For each linked question: reduce vitality, apply lifecycle state, log history

```python
tension.resolved = True
question.vitality -= RESOLUTION_VITALITY_REDUCTION
apply_lifecycle_state(question, tension_resolved=True)
```

Resolution is experimenter-scheduled via `TENSION_RESOLUTIONS` list — not triggered by observations. One resolution event for Bird tension.

Resolved tension persists in `state.persistent_tensions` with `resolved=True` — not deleted.

---

## Dormancy Mechanism

Dormancy entered when vitality falls to or below `DORMANT_VITALITY_THRESHOLD` (1.0) but remains above 0:

```python
elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
    question.state = "DORMANT"
```

Bird question enters DORMANT after first decay step (vitality 1.0). Represents reduced engagement after resolution — question still exists but is inactive.

---

## Extinction Mechanism

Extinction when vitality reaches zero:

```python
if question.vitality <= 0.0:
    question.state = "EXTINCT"
```

`apply_vitality_decay()` skips further decay on EXTINCT questions.

Bird question extinct after second decay step. Question record remains in `lifecycle_questions` dict — extinction is state change, not deletion. `lifecycle_history` preserved.

---

## Question Statistics

`print_question_statistics()` reports:

| Metric | Expected |
|--------|----------|
| Total questions | 1 |
| EXTINCT | 1 |
| EMERGENT / ACTIVE / RESOLVED / DORMANT | 0 (final counts; history shows all were visited) |
| Resolved tensions | 1 |
| Unresolved tensions | 0 |

Note: statistics show **final** state counts only — intermediate states visible in lifecycle history, not in state histogram at end.

---

## Reporting Functions

| Function | Output |
|----------|--------|
| `print_question_lifecycles()` | Full history per question |
| `print_question_vitality()` | Current vitality and state |
| `print_resolved_tensions()` | Resolved tensions with notes |
| `print_extinct_questions()` | EXTINCT questions with final vitality |
| `print_question_statistics()` | Counts by final state |
| `print_overall_organization()` | Pipeline summary, active vs extinct counts |

---

## Presence of Randomness

None. Fully deterministic:

- Sorted group/behavior iteration
- Fixed resolution and decay sequences
- Fixed vitality constants

---

## Overall Assessment

EXP-013 is structurally sound as a lifecycle extension of EXP-012. It adds mortality without redesigning emergence.

Strengths:

- Clean five-state lifecycle with explicit history log
- Vitality links question fate to tension dynamics
- Resolution and decay are separate mechanisms (external answer vs neglect)
- Extinction preserves memory (groups, tensions, history)
- Deterministic full trajectory demonstrable in one run

Weaknesses (see failures file):

- Vitality thresholds externally imposed
- Resolution scheduled, not observation-driven
- No resurrection or repeated cycles
- Decay steps hardcoded by question id
- `LifecycleQuestion` not integrated with `src.question.Question`

The code successfully implements EXP-012 future direction ("Investigate question lifecycles", "Study how questions disappear"). Bird question traverses complete lifecycle; ecosystem ends with zero active questions while organizational memory persists — validating H109–H112.

Vitality trajectory (4.0 → 2.0 → 1.0 → 0.0) provides auditable evidence for each state transition.
