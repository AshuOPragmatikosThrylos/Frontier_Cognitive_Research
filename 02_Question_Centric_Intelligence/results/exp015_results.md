# EXP-015 Results

Post-experiment summary for ecosystem memory and reconstruction.

Date: 2026-06-22  
Experiment: EXP-015 Ecosystem Memory

---

## Theme

Ecosystem Memory and Reconstruction

Test whether question identity and history can survive complete object deletion when preserved in ecosystem-level memory traces, and whether re-emergent tension triggers reconstruction or creation of a new question.

---

## Experiment Summary

Started from the EXP-013 pipeline through extinction, then added memory deletion and reintroduction phases:

```
observations → differences → tensions → questions → extinction → deletion → memory traces → reconstruction
```

### Phase 1: Emergence through extinction

Standard 10 observations. Bird question `eq-bird-fly-vs-not_fly` traversed EMERGENT → ACTIVE → RESOLVED → DORMANT → **EXTINCT** (vitality 4.0 → 0.0). Same lifecycle as EXP-013/014.

### Phase 2: Deletion and memory archival

After extinction, question objects were **deleted completely** via `archive_and_delete_extinct_questions()`:

| Action | Result |
|--------|--------|
| Archive | `MemoryTrace` `mem-eq-bird-fly-vs-not_fly` created |
| Preserve | 5 lifecycle history entries, question id, text, tension link |
| Delete | `eq-bird-fly-vs-not_fly` removed from `lifecycle_questions` |
| Live questions | 0 |

Only memory traces were preserved. The ecosystem retained organizational memory without live question objects.

### Phase 3: Reintroduction

Four new Bird observations (Crow, Raven, Chicken, Turkey) refreshed groups and reopened `t-bird-fly-vs-not_fly` (strength 6.0, unresolved).

### Phase 4: Reconstruction (not new creation)

System looked up memory trace for reopened tension. Trace found.

The ecosystem **reconstructed** the original question identity from memory traces:

| Property | After deletion | After reconstruction |
|----------|----------------|----------------------|
| Question object | Absent | New object (rebuilt) |
| Question ID | (archived only) | `eq-bird-fly-vs-not_fly` (same) |
| History | 5 entries in trace | 7 entries (5 restored + 2 new) |
| State | — | ACTIVE |
| Vitality | 0.0 (archived) | 6.0 (= reopened tension strength) |
| `reconstructed_from_memory` | — | True |

History was restored. The reconstructed question became ACTIVE again.

No new question identity appeared — `create_new_question()` fallback not invoked.

Reconstruction event:

> reconstruction: eq-bird-fly-vs-not_fly (identity reconstructed from mem-eq-bird-fly-vs-not_fly, history preserved=5 prior entries)

The experiment demonstrated: **observations → differences → tensions → questions → extinction → deletion → memory traces → reconstruction**

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H125** | Memory is an ecosystem property | `MemoryTrace` stored in `WorldState.memory_traces`, not inside question object |
| **H126** | Identity need not reside inside entities | Same `eq-bird-fly-vs-not_fly` id reconstructed after object deletion |
| **H127** | Death and deletion are different | EXTINCT then deleted — identity persisted in trace while object removed |
| **H128** | The ecosystem remembers more than individuals do | Trace retained full history after live question count dropped to zero |

---

## Unexpected Observations

1. **Question identity survived complete object deletion.** Id `eq-bird-fly-vs-not_fly` reappeared on reconstructed object — not a new id.

2. **History accumulated across deletion.** Five pre-deletion entries preserved in trace; two reconstruction entries appended — seven total on live question.

3. **Reconstruction restored prior history.** Reconstructed question's `lifecycle_history` begins with archived entries, not fresh EMERGENT.

4. **No new question identity appeared.** Reconstruction branch taken; `new question` fallback unused.

---

## Surprising Observations

1. **Identity appeared independent of physical objects.** Question id existed in memory trace while no `LifecycleQuestion` instance existed — H129.

2. **Memory traces became more fundamental than live questions.** During deletion phase, traces were the sole question-related records — H132.

3. **Reconstruction behaved as continuation rather than recreation.** Same id, restored history, `reconstructed_from_memory=True` — narrative continues across object gap (H131).

4. **The ecosystem itself acted as the memory carrier.** Not the question object (deleted) nor the tension alone — the `MemoryTrace` in ecosystem state.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H129** | Identity is relational rather than material |
| **H130** | Memory accumulates across reconstructions |
| **H131** | Reconstruction is continuation rather than repetition |
| **H132** | Memory traces are more fundamental than questions |

H129: Identity anchored to `question_id` in trace + `tension_id` link, not to object reference.

H130: Second reconstruction would append to seven-entry history — accumulation across object lifetimes.

H131: Contrast EXP-014 resurrection (same object) vs EXP-015 reconstruction (new object, same identity) — both continue; neither repeats naively.

---

## Comparison: EXP-014 vs EXP-015

| Property | EXP-014 (Resurrection) | EXP-015 (Reconstruction) |
|----------|------------------------|--------------------------|
| After extinction | Object kept | Object **deleted** |
| Memory location | Inside question object | Ecosystem `MemoryTrace` |
| Revival mechanism | Reactivate same object | Build new object from trace |
| Identity | Preserved in place | Preserved across deletion |
| History | Appended on same object | Copied from trace, then appended |

EXP-014: identity survives death. EXP-015: identity survives **deletion** — stronger claim.

---

## Future Directions

- Investigate distributed memory (traces across multiple ecosystem components)
- Investigate competing memories (multiple traces for same tension)
- Study memory corruption (partial or altered trace restoration)
- Study memory inheritance (traces passed to derived questions or groups)
- Investigate ecosystem-level forgetting (trace deletion policies)

---

## Conclusion

EXP-015 demonstrates that question identity and history can survive complete object deletion when archived in ecosystem memory traces. Re-emergent tension triggered reconstruction — not creation — restoring prior history and the original question id on a new live object.

Memory is an ecosystem-level property (H125), not confined to question instances. This strengthens distributed ecological interpretations: cognition may reside in traces, groups, and tensions — with questions as transient reconstructions rather than memory bearers.

Reconstruction rules remain externally defined (see `exp015_failures.md`).
