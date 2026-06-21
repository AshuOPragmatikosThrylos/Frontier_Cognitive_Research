# EXP-015 Code Analysis

Post-experiment read-only analysis of ecosystem memory and reconstruction.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-015)

---

## Files Involved

| File | Role in EXP-015 |
|------|-----------------|
| `experiments/exp015_ecosystem_memory.py` | Full pipeline through extinction, memory deletion, and reconstruction |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-014:

| Addition | Purpose |
|----------|---------|
| `MemoryTrace` dataclass | Ecosystem-level archived question record |
| `reconstructed_from_memory` on `LifecycleQuestion` | Flag reconstruction origin |
| `memory_traces`, `deleted_questions`, `reconstruction_events` on `WorldState` | Memory and deletion tracking |
| `archive_and_delete_extinct_questions()` | Archive trace, delete object |
| `reconstruct_from_memory()` | Rebuild question from trace |
| `create_new_question()` | Fallback when no trace |
| `try_reconstruct_or_create()` | Reconstruction vs creation decision |
| `process_memory_deletion()` | Post-extinction deletion phase |
| `process_reintroduction()` | Revival observations + reconstruction |

Removed from EXP-014: resurrection logic (`try_resurrect_or_recreate`, `RESURRECTED` state).

---

## Execution Flow

### Phase 1: `ingest_initial_observations()`

10 observations → Bird groups/tensions, Mammal observations.

### Phase 2: `process_extinction_lifecycle()`

```python
emerge_questions_from_tensions(state)
promote_emergent_questions(state)
resolve_tension(BIRD_TENSION_ID, ...)
apply_vitality_decay(BIRD_QUESTION_ID) × 2  # → EXTINCT
```

### Phase 3: `process_memory_deletion()`

```python
archive_and_delete_extinct_questions(state)
# lifecycle_questions empty; memory_traces populated
```

### Phase 4: `process_reintroduction()`

```python
register_observation(...) × 4  # Crow, Raven, Chicken, Turkey
refresh_group_members("Bird")
reopen_tension(BIRD_TENSION_ID)
try_reconstruct_or_create(BIRD_TENSION_ID)
```

### Phase 5: Reporting

Memory traces, deleted questions, reconstruction events, identities, history, statistics, organization.

---

## Difference Formation

Initial: `form_difference_groups()` — identical to EXP-012–014.

Reintroduction: `refresh_group_members()` updates member lists from expanded `category_index`:

| Group | After reintro |
|-------|---------------|
| Bird.fly | 6 members |
| Bird.not_fly | 6 members |

Groups not recreated — existing group objects updated.

---

## Tension Detection

Initial: `record_tensions()` — Bird tension strength 4.0.

Reintroduction: `reopen_tension()` on existing tension record:

```python
tension.strength = min(len(group_a.members), len(group_b.members))  # 6.0
tension.resolved = False
tension.persistent = True
```

Same tension id preserved across extinction, deletion, and reconstruction.

---

## Emergent Question Generation

`emerge_questions_from_tensions()` — used in Phase 2 only.

Skips if question already linked to tension. After deletion phase, no live questions — but emergence not re-invoked; reconstruction handles reintroduction instead.

---

## Lifecycle Mechanisms

Identical to EXP-013 for Phase 2:

| State | Bird question phase |
|-------|---------------------|
| EMERGENT | Initial |
| ACTIVE | Promoted |
| RESOLVED | Tension resolved, vitality 2.0 |
| DORMANT | Decay 1, vitality 1.0 |
| EXTINCT | Decay 2, vitality 0.0 |

Five history entries at extinction (same as EXP-013/014 pre-revival).

---

## Deletion Mechanism

`archive_and_delete_extinct_questions()` — core EXP-015 distinction:

```python
for question_id, question in list(state.lifecycle_questions.items()):
    if question.state != "EXTINCT":
        continue
    state.memory_traces[f"mem-{question_id}"] = MemoryTrace(...)
    del state.lifecycle_questions[question_id]
    state.deleted_questions.append(question_id)
```

| Field archived in trace | Source |
|-------------------------|--------|
| `question_id` | Original id for reconstruction |
| `tension_id` | Link for lookup on reintro |
| `lifecycle_history` | Full copy of history list |
| `text`, `source_groups`, behaviors | Question content |
| `final_vitality`, `final_state` | Snapshot at deletion |

Object **removed** — not merely marked inactive (contrast EXP-014).

After deletion: `len(lifecycle_questions) == 0`, `len(memory_traces) == 1`.

---

## Memory Trace Generation

One trace per deleted extinct question:

```
mem-eq-bird-fly-vs-not_fly
  question_id: eq-bird-fly-vs-not_fly
  tension_id: t-bird-fly-vs-not_fly
  lifecycle_history: 5 entries
  final_state: EXTINCT
  final_vitality: 0.0
```

Lookup: `memory_trace_for_tension(state, tension_id)` iterates traces by `tension_id`.

---

## Reconstruction Mechanism

`try_reconstruct_or_create(state, tension_id)`:

```python
trace = memory_trace_for_tension(state, tension_id)
if trace:
    reconstruct_from_memory(state, trace, tension)
else:
    create_new_question(state, tension)
```

### `reconstruct_from_memory()`

```python
question = LifecycleQuestion(
    id=trace.question_id,           # same id
    lifecycle_history=list(trace.lifecycle_history),  # copy archived history
    reconstructed_from_memory=True,
    vitality=tension.strength,      # 6.0 from reopened tension
    ...
)
question.lifecycle_history.append("RECONSTRUCTED from memory ...")
question.state = "ACTIVE"
question.lifecycle_history.append("RECONSTRUCTED -> ACTIVE (promoted)")
```

New Python object, same logical identity.

### Bird reconstruction trace

| Metric | Value |
|--------|-------|
| Prior history entries | 5 |
| New entries | 2 |
| Total on live question | 7 |
| Vitality | 6.0 |
| State | ACTIVE |

---

## Identity Preservation

Identity preserved via trace fields, not object persistence:

| Mechanism | EXP-014 | EXP-015 |
|-----------|---------|---------|
| Id storage | In live object | In `MemoryTrace.question_id` |
| Object across death | Same object | Deleted then rebuilt |
| Id after revival | Unchanged | Unchanged (from trace) |

`print_question_identities()` reports `origin=reconstructed` and archived trace identity.

---

## History Restoration

History copied from trace before append:

```python
lifecycle_history=list(trace.lifecycle_history)  # deep copy of list
```

Restored entries include full first lifetime (EMERGENT through EXTINCT). Reconstruction entries appended after — history spans deletion gap without gap in narrative log.

`print_history_preservation()` prints trace entry count vs live question entry count.

---

## Question Statistics

Expected final output:

| Metric | Value |
|--------|-------|
| Active questions | 1 |
| Deleted questions | 1 (archived) |
| Memory traces | 1 |
| Reconstruction events | 1 |
| Reconstructed from memory | 1 |
| New without memory | 0 |

During deletion-only intermediate state: active=0, traces=1, deleted=1.

---

## Reporting Functions

| Function | Output |
|----------|--------|
| `print_memory_traces()` | Archived traces with entry counts |
| `print_deleted_questions()` | Ids removed with trace note |
| `print_reconstruction_events()` | Reconstruction vs new-question log |
| `print_question_identities()` | Live + archived identities |
| `print_history_preservation()` | Trace vs question history detail |
| `print_question_statistics()` | Counts and reconstruction tallies |
| `print_overall_organization()` | Pipeline summary, reintroduction outcome |

---

## Presence of Randomness

None. Deterministic deletion, trace archival, reconstruction from single trace.

---

## Overall Assessment

EXP-015 is structurally sound as an ecosystem memory experiment. It cleanly separates object deletion from identity preservation via external memory traces.

Strengths:

- Sharp contrast with EXP-014 (deletion vs retention)
- Explicit reconstruction vs creation fork
- History copy auditable via entry counts
- `MemoryTrace` as first-class ecosystem construct
- Zero live questions intermediate state demonstrates memory-without-entities

Weaknesses (see failures file):

- Trace creation and reconstruction rules externally defined
- Single trace, single tension — no competition or corruption
- Forgetting not modeled
- `create_new_question()` fallback untested in Bird run

The code successfully implements EXP-014 future direction ("Investigate ecosystem memory") with a constructive demonstration: identity and history survive object deletion when archived at ecosystem level.

Reconstruction produces continuation (same id, restored history) on a new object — distinct from EXP-014 resurrection (same object) and from naive recreation (new id, empty history).

Vitality on reconstruction uses reopened tension strength (6.0), not archived final vitality (0.0) — partial renewal, not full state restore.
