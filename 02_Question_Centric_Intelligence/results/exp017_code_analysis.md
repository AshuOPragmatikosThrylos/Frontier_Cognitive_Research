# EXP-017 Code Analysis

Post-experiment read-only analysis of memory trace competition.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-017)

---

## Files Involved

| File | Role in EXP-017 |
|------|-----------------|
| `experiments/exp017_memory_competition.py` | Full pipeline through extinction, archival, reintroduction, competition, and reconstruction |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-016:

| Addition | Purpose |
|----------|---------|
| Three-category observation sets | Bird, Mammal, Insect — multiple extinct questions |
| `RECONSTRUCTION_BUDGET = 1` | Limited reconstruction resources |
| `TRACE_STRENGTH_DIVISOR = 4.0` | Normalize trace strength from tension strength |
| `competition_events`, `reconstruction_winners`, `permanent_losses` on `ExperimentState` | Competition tracking |
| `drive_question_to_extinction()` | Loop decay until EXTINCT per question |
| `trace_strength_from_tension()` | Compute archival trace strength |
| `run_memory_competition()` | Rank traces, apply budget, reconstruct winners |
| `reopen_all_tensions()` | Reopen all three category tensions at reintroduction |
| `ingest_category_observations()` | Shared ingest helper for initial and reintro phases |

Removed from EXP-016: dual-world comparison (perfect vs selective forgetting), clutter trace seeding, forgetting decay loop.

---

## Execution Flow

### Phase 1: `ingest_initial_observations()`

16 observations across three categories:

```python
ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])
```

Each call: `register_observation` → `form_difference_groups` → `record_tensions`.

### Phase 2: `process_extinction_lifecycle()`

```python
emerge_questions_from_tensions(state)
promote_emergent_questions(state)
for tension_id, note in TENSION_RESOLUTIONS:
    resolve_tension(state, tension_id, note)
for question_id in ALL_QUESTION_IDS:
    drive_question_to_extinction(state, question_id)
```

Bird: resolve 4.0→2.0, two decays → EXTINCT.  
Mammal/Insect: resolve 2.0→0.0 → EXTINCT immediately.

### Phase 3: `process_memory_deletion()`

```python
archive_and_delete_extinct_questions(state)
# 3 traces; lifecycle_questions empty
```

### Phase 4: `process_reintroduction_and_competition()`

```python
ingest_reintroduction_observations(state)  # 12 new observations
reopened = reopen_all_tensions(state)       # all 3 persistent
run_memory_competition(state, reopened)     # rank, budget, reconstruct
```

### Phase 5: Reporting

Memory traces, competition events, reconstruction winners, permanent losses, question statistics, overall organization.

---

## Difference Formation

`form_difference_groups()` — identical threshold logic to EXP-012–016:

- ≥2 behavior types per category
- ≥2 members per behavior group

| Category | Groups formed |
|----------|---------------|
| Bird | `Bird.fly` (4), `Bird.not_fly` (4) |
| Mammal | `Mammal.fly` (2), `Mammal.swim` (2) |
| Insect | `Insect.fly` (2), `Insect.crawl` (2) |

Reintroduction: `refresh_group_members()` updates member counts (each group grows by 2).

---

## Tension Detection

`detect_persistent_tensions()` pairs groups within category; strength = `min(|group_a|, |group_b|)`.

| Tension | Initial strength | Persistent |
|---------|------------------|------------|
| `t-bird-fly-vs-not_fly` | 4.0 | Yes |
| `t-mammal-fly-vs-swim` | 2.0 | Yes |
| `t-insect-fly-vs-crawl` | 2.0 | Yes |

`reopen_tension()` recalculates strength from refreshed groups and clears `resolved` flag.

After reintroduction: Bird strength 6.0, Mammal 4.0, Insect 4.0.

---

## Question Generation

`emerge_questions_from_tensions()` — one `LifecycleQuestion` per persistent tension:

| Question ID | Text pattern |
|-------------|--------------|
| `eq-bird-fly-vs-not_fly` | Why do Bird entities both fly and not fly? |
| `eq-mammal-fly-vs-swim` | Why do Mammal entities both fly and swim? |
| `eq-insect-fly-vs-crawl` | Why do Insect entities both fly and crawl? |

Initial vitality = tension strength. Promoted EMERGENT → ACTIVE before resolution.

---

## Extinction Mechanism

Resolution: `vitality -= 2.0` per `TENSION_RESOLUTIONS` entry.

Decay: `drive_question_to_extinction()` loops `apply_vitality_decay()` until `state == EXTINCT`.

| Question | Path to EXTINCT |
|----------|-----------------|
| Bird | RESOLVED (2.0) → DORMANT (1.0) → EXTINCT (0.0) |
| Mammal | RESOLVED → EXTINCT (0.0 directly) |
| Insect | RESOLVED → EXTINCT (0.0 directly) |

---

## Memory Trace Creation

`archive_and_delete_extinct_questions()` for each EXTINCT question:

```python
trace_id = f"mem-{question_id}"
trace_strength = min(1.0, tension.strength / 4.0)
del state.lifecycle_questions[question_id]
```

| Trace | Strength formula | Result |
|-------|------------------|--------|
| Bird | 4.0 / 4.0 | 1.00 |
| Mammal | 2.0 / 4.0 | 0.50 |
| Insect | 2.0 / 4.0 | 0.50 |

Full lifecycle history, text, tension link preserved in trace.

---

## Competition Mechanism

`run_memory_competition(state, reopened_tension_ids)`:

1. **Collect candidates** — trace exists, strength > 0, tension persistent, no live question for tension
2. **Sort** — `key=lambda trace: (-trace.trace_strength, trace.trace_id)` (deterministic tie-break)
3. **Split** — `winners = candidates[:RECONSTRUCTION_BUDGET]`, `losers = candidates[RECONSTRUCTION_BUDGET:]`
4. **Record** — losers → `permanent_losses`; winners → `reconstruct_from_memory()`

All three traces qualified as candidates. Budget=1 selected one winner.

---

## Budget Constraints

```python
RECONSTRUCTION_BUDGET = 1
```

Hard cap on reconstructions per competition round. With three eligible traces and budget 1, exactly two permanent losses guaranteed.

No partial reconstruction — winner gets full trace copy or nothing.

---

## Reconstruction Winners

Single winner: `eq-bird-fly-vs-not_fly`

`reconstruct_from_memory()`:

- `id=trace.question_id` (same identity)
- `lifecycle_history=list(trace.lifecycle_history)` + reconstruction entries
- `vitality=tension.strength` (reopened, 6.0)
- `reconstructed_from_memory=True`
- `state=ACTIVE`

---

## Permanent Losses

| Question | Trace retained | Live question |
|----------|----------------|---------------|
| `eq-mammal-fly-vs-swim` | Yes (0.50) | No |
| `eq-insect-fly-vs-crawl` | Yes (0.50) | No |

Loss = failed to win budget slot. Traces not deleted — distinct from EXP-016 forgetting.

Mammal/Insect tied at 0.50; tie-break by `trace_id` placed Insect rank 2, Mammal rank 3. Both lost equally regardless of order.

---

## Identity Preservation

`identity_preserved(state, question_id)`:

```python
question.reconstructed_from_memory and question.id == question_id
```

| Question | Identity preserved |
|----------|-------------------|
| Bird | **Yes** — reconstructed with original id and history |
| Mammal | **No** — not reconstructed |
| Insect | **No** — not reconstructed |

Winner identity preserved via trace copy — same mechanism as EXP-015, now gated by competition.

---

## Question Statistics

| Metric | Value |
|--------|-------|
| Deleted (archived) | 3 |
| Live after competition | 1 |
| Reconstruction winners | 1 |
| Permanent losses | 2 |
| Memory traces | 3 |
| Observations (total) | 28 |
| Difference groups | 6 |
| Persistent tensions (reopened) | 3 |

Latent-to-active ratio: 3 traces : 1 live question.

---

## Overall Assessment

EXP-017 successfully extends the EXP-012–015 pipeline with **multi-trace competition under budget constraint**. The implementation is minimal: one sort, one slice, one reconstruction call per winner.

**Strengths:**

- Clean separation of memory (3 traces) from activity (1 question)
- Deterministic ranking removes ambiguity
- Three-category design validates competition beyond single Bird case
- Builds directly on EXP-015 reconstruction without new object types

**Limitations (see exp017_failures.md):**

- Competition rules externally imposed (sort by strength, take top N)
- Trace strength formula fixed at archival
- Single competition round; no iterative or adaptive budget
- Tie at 0.50 resolved by trace_id ordering, not ecological mechanism

**Scientific value:**

Completes a memory arc progression: **archive (015) → forget (016) → compete (017)**. Introduces scarcity of expression separate from scarcity of storage — H145, H146, H148.

The experiment's central image: three tensions reopened, three memories eligible, one question reborn — selection as gatekeeper on resurrection.
