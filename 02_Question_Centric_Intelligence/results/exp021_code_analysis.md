# EXP-021 Code Analysis

Post-experiment read-only analysis of assumption removal and dual-world comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-021)

---

## Files Involved

| File | Role in EXP-021 |
|------|-----------------|
| `experiments/exp021_assumption_removal.py` | Dual-world pipeline through extinction/archival; divergent reactivation; side-by-side reporting |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-017:

| Addition | Purpose |
|----------|---------|
| `WorldState` with `assumption_rich: bool` | Dual-world state container |
| `run_shared_pipeline()` | Shared ingest → extinction → archival |
| `run_assumption_rich_reactivation()` | World A: EXP-017 competition |
| `run_assumption_removed_reactivation()` | World B: no ranking/budget/strength priority |
| `run_experiment()` | Returns `(world_a, world_b)` tuple |
| Side-by-side print functions | Outcomes, traces, persistence, selection patterns |

---

## Execution Flow

### Shared phases (both worlds)

```python
ingest_initial_observations(state)     # Bird, Mammal, Insect — 16 obs
process_extinction_lifecycle(state)    # 3 questions → EXTINCT
process_memory_archival(state)         # 3 memory traces
```

### Divergent phase (reintroduction)

```python
ingest_reintroduction_observations(state)  # 12 reintro obs
reopened = reopen_all_tensions(state)        # all 3 persistent

if state.assumption_rich:
    run_assumption_rich_reactivation(state, reopened)
else:
    run_assumption_removed_reactivation(state, reopened)
```

### Experiment driver

```python
world_a = run_shared_pipeline(assumption_rich=True)
world_b = run_shared_pipeline(assumption_rich=False)
```

Both worlds start from identical state at archival boundary; only reactivation logic differs.

---

## World A Assumptions

| Mechanism | Implementation |
|-----------|----------------|
| **Ranking** | `candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))` |
| **Fixed budget** | `RECONSTRUCTION_BUDGET = 1` |
| **Strength ordering** | Sort key prioritizes higher `trace_strength` |
| **Winner selection** | `winners = candidates[:RECONSTRUCTION_BUDGET]` |
| **Losers** | Remaining candidates → `permanent_losses` |

Trace strengths at archival: Bird 1.00, Mammal 0.50, Insect 0.50. Budget=1 → Bird wins deterministically.

---

## World B Assumptions

| Removed | Replacement |
|---------|-------------|
| Ranking | None — no sort by strength |
| Fixed budget | None — all eligible traces reconstruct |
| Strength ordering | `sorted(reopened_tension_ids)` — tension_id order only |
| Winner=max() | None — no winners/losers lists populated |

Each persistent tension with a valid trace reconstructs via `reconstruct_from_memory()`. `trace_strength` logged but **not used for priority**.

---

## Difference Formation

Identical to EXP-017. Six difference groups across three categories:

| Category | Groups |
|----------|--------|
| Bird | `Bird.fly` (4), `Bird.not_fly` (4) |
| Mammal | `Mammal.fly` (2), `Mammal.swim` (2) |
| Insect | `Insect.fly` (2), `Insect.crawl` (2) |

Reintroduction refreshes member counts (+2 per group).

---

## Tension Detection

Three persistent tensions; strength = `min(|group_a|, |group_b|)`:

| Tension | Initial strength | Trace strength |
|---------|------------------|----------------|
| `t-bird-fly-vs-not_fly` | 4.0 | 1.00 |
| `t-mammal-fly-vs-swim` | 2.0 | 0.50 |
| `t-insect-fly-vs-crawl` | 2.0 | 0.50 |

`reopen_tension()` recalculates strength after reintroduction (Bird 6.0, Mammal 4.0, Insect 4.0).

---

## Question Generation

`emerge_questions_from_tensions()` — one question per persistent tension via `question_id_for_tension()`.

All three promoted EMERGENT → ACTIVE, resolved, decayed to EXTINCT before archival.

---

## Extinction Mechanism

Resolution: `vitality -= 2.0`. Decay loop until EXTINCT.

| Question | Path |
|----------|------|
| Bird | RESOLVED → DORMANT → EXTINCT |
| Mammal | RESOLVED → EXTINCT |
| Insect | RESOLVED → EXTINCT |

Identical in both worlds.

---

## Memory Trace Generation

`archive_and_delete_extinct_questions()` — three traces, live questions = 0.

```python
trace_strength = min(1.0, tension.strength / TRACE_STRENGTH_DIVISOR)
```

Full lifecycle history and identity preserved. **Identical trace sets in World A and World B at reactivation boundary.**

---

## Reactivation Mechanisms

### World A — `run_assumption_rich_reactivation()`

1. Collect candidates (persistent tension + trace exists + no live question)
2. Sort by `(-trace_strength, trace_id)`
3. Log ranks
4. Split winners/losers by budget
5. Reconstruct winners only

### World B — `run_assumption_removed_reactivation()`

1. Log start (no ranking, no budget)
2. Iterate `sorted(reopened_tension_ids)`
3. For each: if persistent + trace exists → reconstruct
4. Append to `reactivated_questions` (not `reconstruction_winners`)

No `permanent_losses` populated in World B.

---

## Persistence Patterns

| Metric | World A | World B |
|--------|---------|---------|
| Traces at end | 3 | 3 |
| Traces disappeared | 0 | 0 |
| Trace strengths unchanged | Yes | Yes |
| Expressed / archived ratio | 1/3 | 3/3 |
| Latent traces (no live question) | 2 | 0 |

**Persistence invariant across assumption change.** Traces neither created nor destroyed by reactivation phase.

Helper functions:

- `trace_count()` — len(memory_traces)
- `latent_trace_count()` — traces without matching live question
- `traces_disappeared()` — always False in completed run

---

## Selection Patterns

| Metric | World A | World B |
|--------|---------|---------|
| `selection_pattern_detected()` | **True** | **False** |
| Ranking used | True | False |
| Budget used | True (1) | False |
| Strength ordering used | True | False |
| Explicit winners | 1 | 0 |
| Permanent losses | 2 | 0 |

World A: `len(reconstruction_winners) > 0 and len(permanent_losses) > 0`  
World B: `live_question_count < trace_count` → 3 < 3 → False

Selection is **entirely a product of World A assumptions**, not an emergent property detectable in World B.

---

## Side-by-Side Comparison

Print functions:

| Function | Content |
|----------|---------|
| `print_side_by_side_outcomes()` | Traces, live questions, winners, losses per world |
| `print_trace_statistics()` | Per-trace strength and stability |
| `print_persistence_patterns()` | Expressed/archived ratio, latent counts |
| `print_selection_patterns()` | Assumption flags and key phase events |
| `print_overall_observations()` | Interpretation summary |

Key contrast: identical inputs → divergent live question counts (1 vs 3) from reactivation logic alone.

---

## Overall Assessment

EXP-021 is a **controlled assumption-removal experiment** — the cleanest falsification of selection in the program to date. Shared pipeline through archival eliminates observation/tension variance; only reactivation assumptions differ.

**Strengths:**

- Minimal diff between worlds — one branch at `process_reintroduction()`
- Reproduces EXP-017 exactly in World A (validates prior result under same code path)
- World B falsifies selection without adding new mechanisms
- Side-by-side reporting makes assumption dependence visible

**Limitations (see exp021_failures.md):**

- World B uses `sorted(tension_id)` — still deterministic order, not interaction-driven priority
- No natural trace disappearance tested (would require EXP-016-style forgetting)
- Single reactivation round; no iterative dynamics

**Scientific value:**

Demotes selection from "emergent ecosystem property" to "externally imposed filter." Elevates persistence as the surviving memory-layer primitive. One of the most important experiments in the arc — comparable to EXP-010 (falsification) and EXP-011 (minimal worlds) in narrative impact.

**Central image:** Same three traces, same reopened tensions — one world picks a winner, one world revives all. Selection was in the assumptions, not the traces.
