# EXP-015 Failures

Post-experiment failure analysis for ecosystem memory and reconstruction.

Date: 2026-06-22  
Experiment: EXP-015 Ecosystem Memory

---

## Failure Analysis

No mechanical failure was observed. Pipeline completed: Bird question emerged, went extinct, was archived and deleted, tension reopened on reintroduction, question reconstructed from memory trace with preserved id and history, promoted to ACTIVE.

The significant findings are methodological: ecosystem memory is richer than question-local memory, but trace creation and reconstruction rules remain externally programmed.

---

## Current Limitation

### Memory traces and reconstruction rules remain externally defined

Archival trigger:

```python
if question.state != "EXTINCT":
    continue
state.memory_traces[trace_id] = MemoryTrace(...)
del state.lifecycle_questions[question_id]
```

Reconstruction trigger:

```python
trace = memory_trace_for_tension(state, tension_id)
if trace:
    reconstruct_from_memory(state, trace, tension)
else:
    create_new_question(state, tension)
```

Equivalent to:

```
memory trace exists → reconstruction occurs
```

No trace → new question. The ecosystem does not **discover** that memory should be consulted — it is **instructed** to look up traces by tension id.

### Identity restoration remains explicitly programmed

Reconstruction copies predetermined fields from trace:

```python
id=trace.question_id
lifecycle_history=list(trace.lifecycle_history)
text=trace.text
```

Identity is restored because the experimenter archived `question_id` and the reconstruction function reads it back — not because the ecosystem inferentially recognizes "this is the same question."

H126 (identity need not reside inside entities) is supported operationally but achieved through explicit archival schema.

### The ecosystem does not yet determine what should be remembered or forgotten

All-or-nothing rules:

- Every EXTINCT question → archived (no selective forgetting)
- Every matching trace → full reconstruction (no partial recall)
- No trace decay, corruption, or competition
- No question-initiated memory requests

Memory is write-on-extinction, read-on-tension-reopen — fixed policy, not adaptive ecology.

---

## What Improved vs EXP-014

| Aspect | EXP-014 | EXP-015 |
|--------|---------|---------|
| Memory location | Inside question object | Ecosystem `MemoryTrace` |
| Object after extinction | Kept (EXTINCT) | Deleted |
| Identity survival | Object-bound | Trace-bound |
| Revival | Resurrection (same object) | Reconstruction (new object) |
| Zero live questions phase | No | Yes (between deletion and reintro) |
| Memory carrier | Question | Ecosystem |

EXP-014 showed identity survives death. EXP-015 shows identity survives **deletion** — memory externalized from entities.

---

## Additional Limitations

### 1. Single memory trace

One trace, one tension, one question. No competing traces, conflicting memories, or merge logic.

### 2. Recreation path untested

`create_new_question()` exists for tension without trace — Bird always had trace after deletion. Fresh-identity path unverified empirically.

### 3. Full history always restored

No partial reconstruction, corrupted trace, or selective memory fields. All-or-nothing copy from trace.

### 4. No forgetting mechanism

Traces persist indefinitely. `memory_traces` never pruned. Ecosystem cannot forget — only archive.

### 5. Reintroduction observations hardcoded

Crow, Raven, Chicken, Turkey — same limitation class as EXP-014 revival observations.

### 6. Vitality asymmetry on reconstruction

Emergence: `vitality = tension.strength` (initial).
Reconstruction: `vitality = tension.strength` (reopened, 6.0).
Archived: `final_vitality = 0.0`.

Vitality not restored from trace — only id and history. Partial state restoration undocumented as design choice.

### 7. Parallel type system persists

`LifecycleQuestion` and `MemoryTrace` local — not integrated with `src.question.Question`.

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Adaptive memory** | Trace creation/retrieval rules change with ecosystem experience |
| **Selective forgetting** | Traces decay, merge, or delete under resource pressure |
| **Memory competition** | Multiple traces for same tension; ecosystem selects which to reconstruct |
| **Memory corruption** | Partial or noisy trace restoration; test identity robustness |
| **Distributed memory architectures** | Traces split across groups, tensions, observations |
| **Self-organized reconstruction** | Reconstruction triggered by observation patterns, not tension id lookup |
| **Repeated deletion-reconstruction cycles** | Test H130 across N generations |

---

## EXP-012 → EXP-015 Memory Arc

| Experiment | Memory model |
|------------|--------------|
| EXP-012 | No memory beyond emergence |
| EXP-013 | History in live object; extinction preserves record |
| EXP-014 | History in live object; resurrection appends |
| EXP-015 | History in ecosystem trace; object deleted; reconstruction copies |

Progressive externalization of memory from question → ecosystem.

---

## Resurrection vs Reconstruction vs Recreation

| Mechanism | Object | Identity | History | EXP |
|-----------|--------|----------|---------|-----|
| Resurrection | Same | Preserved | Appended | 014 |
| Reconstruction | New | Preserved (from trace) | Restored + appended | 015 |
| Recreation | New | New id | Fresh | 015 fallback |

EXP-015 reconstruction is philosophically between EXP-014 resurrection and naive recreation — new object, old identity, continuous history.

---

## Overall Assessment

Ecosystem memory produced richer dynamics than question-local memory and strengthened the interpretation of cognition as a distributed ecological process.

**Achieved:**

- Memory as ecosystem property (H125)
- Identity without entity (H126)
- Death ≠ deletion (H127)
- Ecosystem remembers when individuals absent (H128)
- Reconstruction as continuation (H131)
- Traces more fundamental than live questions during deletion phase (H132)

**Still externally controlled:**

- When to archive (all EXTINCT)
- When to reconstruct (trace exists + tension persistent)
- What to restore (full trace copy)
- When to forget (never)
- Reintroduction scheduling

**Scientific value:**

EXP-015 completes a memory externalization arc. Questions become reconstructible episodes; ecosystem traces become the durable substrate. This aligns with H100 (difference management), H115 (organization outside questions), and H132 (traces fundamental).

The zero-question intermediate state is the experiment's strongest image: the ecosystem held memory while no question lived — cognition without current question instances.

Next stress test: multiple competing traces, selective forgetting, and corrupted reconstruction — determine whether identity preservation survives imperfect ecosystem memory or requires the current all-or-nothing archival design.

Memory rules must become endogenous before ecosystem memory can be called a property of the system rather than the experimenter's archive policy.
