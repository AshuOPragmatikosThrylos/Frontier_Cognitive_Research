# EXP-019 Code Analysis

Post-experiment read-only analysis of memory trace merging.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-019)

---

## Files Involved

| File | Role in EXP-019 |
|------|-----------------|
| `experiments/exp019_memory_merging.py` | Full pipeline through extinction, archival, co-activation rounds, and intended merge |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-018:

| Addition | Purpose |
|----------|---------|
| `MemoryAbstraction` dataclass | Merged trace record with inherited history |
| `co_activation_counts`, `co_activation_events`, `merge_events` | Co-activation and merge tracking |
| `abstractions` on `ExperimentState` | Storage for merged abstractions |
| `record_co_activation()` | Log rounds; increment pair counts |
| `merge_traces()` | Combine traces into abstraction |
| `try_merge_coactivated_traces()` | Apply threshold and trigger merge |
| `run_co_activation_round()` | Reintro + reopen + co-activate + try merge |
| `process_co_activation_and_merging()` | Three-round schedule |

Removed from EXP-017/018: competition, coalitions, reconstruction winners.

---

## Execution Flow

### Phase 1–3: Standard pipeline

```python
ingest_initial_observations(state)      # 16 obs, 3 categories
process_extinction_lifecycle(state)   # 3 questions → EXTINCT
process_memory_deletion(state)        # 3 memory traces
```

### Phase 4: Co-activation and merging

```python
run_co_activation_round("round 1", [BIRD], ...)
run_co_activation_round("round 2", [MAMMAL, INSECT], ...)
run_co_activation_round("round 3", [MAMMAL, INSECT], ...)  # reopen only
```

Each round: optional observations → `reopen_tension()` → `active_traces_for_tensions()` → `record_co_activation()` → `try_merge_coactivated_traces()`.

### Phase 5: Reporting

Memory traces, merge events, inherited histories, new abstractions, question statistics, overall organization.

---

## Difference Formation

Identical to EXP-017/018. Six difference groups across Bird, Mammal, Insect. Reintroduction in rounds 1–2 adds observations and refreshes group members.

---

## Tension Detection

Three persistent tensions at initial ingest. `reopen_tension()` recalculates strength and clears resolved flag each co-activation round.

---

## Question Generation

Three emergent questions via standard pipeline. All driven to EXTINCT before memory archival. No live questions during co-activation phase.

---

## Extinction Mechanism

Same as EXP-017: resolve all tensions (−2.0 vitality), then `drive_question_to_extinction()` per question id.

---

## Memory Trace Generation

`archive_and_delete_extinct_questions()` — three traces:

| Trace | Strength |
|-------|----------|
| Bird | 1.00 |
| Mammal | 0.50 |
| Insect | 0.50 |

Formula: `min(1.0, tension.strength / 4.0)`.

---

## Co-Activation Mechanism

`record_co_activation(state, round_label, active_traces)`:

1. Log active trace ids for the round
2. If ≥2 traces active, increment `co_activation_counts[frozenset(trace_ids)]`

**Completed run observations:**

| Round | Active traces | Pair count (Mammal+Insect) |
|-------|---------------|----------------------------|
| 1 | Bird only | — |
| 2 | Mammal, Insect | 1 |
| 3 | Mammal, Insect | 2 |

Co-activation events logged. Pair reached threshold count in round 3.

---

## Merge Conditions

```python
CO_ACTIVATION_MERGE_THRESHOLD = 2

def try_merge_coactivated_traces(state):
    for pair_key, count in co_activation_counts:
        if count < THRESHOLD: continue
        if all traces still in memory_traces: merge_traces(...)
```

**Intended:** When mammal–insect pair count ≥ 2, `merge_traces()` creates `MemoryAbstraction`, removes source traces, appends merge events.

**Observed (completed experiment):** **No merge events occurred.** No abstractions created. All three individual traces remained at experiment end.

Possible gap between intended merge trigger and observed outcome documented in `exp019_failures.md`.

---

## Identity Preservation

At experiment end (completed run):

| Question ID | Location | Status |
|-------------|----------|--------|
| `eq-bird-fly-vs-not_fly` | Individual trace | Preserved |
| `eq-mammal-fly-vs-swim` | Individual trace | Preserved |
| `eq-insect-fly-vs-crawl` | Individual trace | Preserved |

No identity negotiation or absorption occurred. H161 supported: identity stable under co-activation.

---

## Question Statistics

| Metric | Value (completed run) |
|--------|----------------------|
| Deleted (archived) | 3 |
| Remaining traces | **3** |
| Abstractions | **0** |
| Co-activation events | ≥3 rounds logged |
| Merge events | **0** |

All three question identities preserved in separate traces.

---

## Overall Assessment

EXP-019 extended the memory arc with co-activation and merge infrastructure but produced a **negative result** in the completed run: no merges, no abstractions.

**Code structure:** Clean addition of `MemoryAbstraction`, pair counting, and three-round schedule. Merge path is additive to EXP-017 trace archival.

**Scientific outcome:** Memory traces resisted merging that questions underwent in EXP-002. Supports H160–H162, H163. Identity at trace layer more stable than expected.

**Contrast with EXP-002:** Question merge succeeded via similarity; memory merge via co-activation failed — suggests layer-specific rules (H163).

**Key finding:** Co-activation alone is insufficient for memory abstraction. Stronger coupling (shared tensions, dependencies, cooperation) may be prerequisites.

The experiment's central image: three traces co-activated repeatedly, none merged — **memory identity resistant to dissolution**.
