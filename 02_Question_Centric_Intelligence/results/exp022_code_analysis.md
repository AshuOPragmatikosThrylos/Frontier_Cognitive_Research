# EXP-022 Code Analysis

Post-experiment read-only analysis of persistence removal and dual-world comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-022)

---

## Files Involved

| File | Role in EXP-022 |
|------|-----------------|
| `experiments/exp022_persistence_removal.py` | Dual-world pipeline through memory traces; divergent reintroduction; side-by-side reporting |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-021:

| Addition | Purpose |
|----------|---------|
| `persistent_memory: bool` on `WorldState` | World mode flag |
| `archive_persistent_traces()` | World A: stable archival |
| `decay_transient_traces()` | World B: immediate decay, no retention |
| `emerge_fresh_question()` | World B reintroduction without reconstruction |
| `process_persistent_reintroduction()` | World A: reconstruct from traces |
| `process_transient_reintroduction()` | World B: fresh emergence only |
| `decay_events`, `reconstructed_questions`, `emergent_questions` | Outcome tracking |

Removed from EXP-021: assumption-rich competition, ranking, budget, permanent losses.

---

## Execution Flow

### Shared phases (both worlds)

```python
ingest_initial_observations(state)    # Bird, Mammal, Insect — 16 obs
process_question_lifecycle(state)   # emerge → resolve → extinct
process_memory_traces(state)          # DIVERGES HERE
process_reintroduction(state)       # DIVERGES HERE
```

### Experiment driver

```python
world_a = run_world(persistent_memory=True)
world_b = run_world(persistent_memory=False)
```

---

## World A Mechanisms

**Memory phase — `archive_persistent_traces()`:**

- For each EXTINCT question: create `MemoryTrace` in `memory_traces` dict
- Delete live question; append to `deleted_questions`
- Trace retains full lifecycle history, identity, tension link, strength

**Reintroduction — `process_persistent_reintroduction()`:**

- Reintroduce observations → refresh groups → reopen tensions
- For each persistent tension with matching trace: `reconstruct_from_memory()`
- Sets `reconstructed_from_memory=True`; preserves lifecycle history
- Appends to `reconstructed_questions`

---

## World B Mechanisms

**Memory phase — `decay_transient_traces()`:**

- For each EXTINCT question: log decay event (`transient: mem-{id} formed and decayed immediately`)
- Delete live question; **no entry** in `memory_traces`
- `memory_traces` dict remains empty

**Reintroduction — `process_transient_reintroduction()`:**

- Same reintro + reopen as World A
- For each persistent tension: `emerge_fresh_question()` — no trace lookup
- Sets `reconstructed_from_memory=False`; new lifecycle history only
- Appends to `emergent_questions`

**Removed:** stable memory, identity preservation, reconstruction.

---

## Difference Formation

Identical to EXP-012–021. Six difference groups:

| Category | Groups |
|----------|--------|
| Bird | `Bird.fly` (4→6), `Bird.not_fly` (4→6) |
| Mammal | `Mammal.fly` (2→4), `Mammal.swim` (2→4) |
| Insect | `Insect.fly` (2→4), `Insect.crawl` (2→4) |

Reintroduction refreshes member counts via `refresh_group_members()`. **Invariant across worlds.**

---

## Tension Detection

Three persistent tensions; strength recalculated on reopen:

| Tension | Post-reintro strength |
|---------|----------------------|
| `t-bird-fly-vs-not_fly` | 6.0 |
| `t-mammal-fly-vs-swim` | 4.0 |
| `t-insect-fly-vs-crawl` | 4.0 |

All reopen as persistent. **Invariant across worlds.**

---

## Question Generation

**Initial phase (both worlds):** `emerge_questions_from_tensions()` → resolve → extinct.

Three questions: `eq-bird-fly-vs-not_fly`, `eq-mammal-fly-vs-swim`, `eq-insect-fly-vs-crawl`.

---

## Memory Trace Behavior

| Phase | World A | World B |
|-------|---------|---------|
| At extinction | 3 traces archived | 3 decay events, 0 retained |
| Trace strengths | Bird 1.00, Mammal 0.50, Insect 0.50 | N/A |
| After reintro | 3 traces stable | 0 traces |

World B implements "immediate decay after use" by skipping archival entirely and logging transient formation.

---

## Reconstruction Mechanisms

World A only — `reconstruct_from_memory()`:

```python
question = LifecycleQuestion(
    id=trace.question_id,
    lifecycle_history=list(trace.lifecycle_history),
    reconstructed_from_memory=True,
    ...
)
```

Copies trace text, source groups, tension link, and full history. Three reconstructions in completed run.

World B: **reconstruction code path never invoked.**

---

## Fresh Emergence Mechanisms

World B only — `emerge_fresh_question()`:

```python
question = LifecycleQuestion(
    id=question_id_for_tension(tension),
    reconstructed_from_memory=False,
    lifecycle_history=[f"EMERGENT (fresh, ... no trace)"],
    ...
)
```

Same question id format as reconstruction path but **no history inheritance**. Three fresh emergences in completed run.

---

## Persistence Patterns

| Metric | World A | World B |
|--------|---------|---------|
| Stable traces | True (3) | False (0) |
| Immediate decay | False | True (3 events) |
| Identity preserved | True | False |
| Reconstruction | 3 | 0 |

Helper: `identity_preserved_count()` — counts questions with `reconstructed_from_memory=True` and history length > 2.

---

## Organization Patterns

| Layer | World A | World B |
|-------|---------|---------|
| Observations | 28 | 28 |
| Difference groups | 6 | 6 |
| Persistent tensions | 3 | 3 |
| Live questions | 3 | 3 |
| Memory traces | 3 | 0 |

`organization_survives()` = difference_groups > 0 AND persistent_tensions > 0 → **True both worlds**.

**Structure without memory:** World B proves difference + tension layers maintain organization independently of trace retention.

---

## Side-by-Side Comparison

Print functions:

| Function | Content |
|----------|---------|
| `print_world_statistics()` | Observations, groups, tensions, traces, live questions |
| `print_persistence_patterns()` | Trace stability, decay, identity, reconstruction |
| `print_surviving_motifs()` | Per-question live status and origin (reconstructed vs fresh) |
| `print_organization_patterns()` | Layer-by-layer structure comparison |
| `print_overall_observations()` | Interpretation summary |

Key contrast: identical organizational skeleton; memory layer differs entirely.

---

## Overall Assessment

EXP-022 is the **second destructive test** in the assumption-removal arc (after EXP-021). Where EXP-021 attacked selection and found persistence surviving, EXP-022 attacks persistence and finds **difference + tension surviving**.

**Strengths:**

- Clean binary split at `process_memory_traces()` — minimal diff between worlds
- Reuses full EXP-012–015 pipeline without competition/ranking noise
- Side-by-side reporting makes optional-memory conclusion visible
- Directly falsifies H178 (persistence fundamental)

**Limitations (see exp022_failures.md):**

- Questions still depend on tensions and differences — not yet attacked
- Fresh emergence uses same question id format — structural recurrence, not random respawn
- Single reintroduction round

**Scientific value:**

One of the most important experiments in the program. Demotes persistence from fundamental primitive (post-EXP-021) to **optimization layer**. Elevates difference and tension. Pairs with EXP-021 as sequential destructive tests — selection demolished, then persistence demolished, organization remains.

**Central image:** Same six groups, same three tensions — World A remembers, World B forgets instantly — both worlds think again.
