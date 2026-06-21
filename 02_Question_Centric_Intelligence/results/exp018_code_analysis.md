# EXP-018 Code Analysis

Post-experiment read-only analysis of memory trace cooperation.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-018)

---

## Files Involved

| File | Role in EXP-018 |
|------|-----------------|
| `experiments/exp018_memory_cooperation.py` | Full pipeline through extinction, archival, reintroduction, coalition attempt, and competition |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-017:

| Addition | Purpose |
|----------|---------|
| `MemoryCoalition` dataclass | Coalition id, member traces, combined strength |
| `CompetitionEntry` dataclass | Individual or coalition competition unit |
| `coalition_id` on `LifecycleQuestion` | Tag reconstruction origin |
| `coalitions` on `ExperimentState` | Formed coalition records |
| `form_coalitions()` | Group weak traces (strength < 1.0) into coalition |
| `build_competition_entries()` | Merge individual + coalition entries |
| `collect_eligible_traces()` | Extract traces for competition (refactored from EXP-017) |
| `print_coalitions()` | Report coalition formation |

Removed from EXP-017: `permanent_losses` tracking and print section.

---

## Execution Flow

### Phase 1: `ingest_initial_observations()`

16 observations across Bird, Mammal, Insect → groups, tensions, three emergent questions.

### Phase 2: `process_extinction_lifecycle()`

All three questions: EMERGENT → ACTIVE → RESOLVED → EXTINCT.

### Phase 3: `process_memory_deletion()`

Three memory traces archived; live questions = 0.

### Phase 4: `process_reintroduction_and_competition()`

```python
ingest_reintroduction_observations(state)  # 12 observations
reopened = reopen_all_tensions(state)       # 3 persistent
run_memory_competition(state, reopened)
```

Inside `run_memory_competition()`:

```python
traces = collect_eligible_traces(state, reopened)
coalitions = form_coalitions(traces)
entries = build_competition_entries(traces, coalitions)
winners = entries[:RECONSTRUCTION_BUDGET]
# reconstruct winner trace(s)
```

### Phase 5: Reporting

Memory traces, coalitions, competition events, reconstruction winners, question statistics, overall organization.

---

## Difference Formation

Identical threshold logic to EXP-017. Six difference groups across three categories (two behavior groups per category, ≥2 members each).

Reintroduction refreshes member lists via `refresh_group_members()`.

---

## Tension Detection

Three persistent tensions detected at initial ingest:

| Tension | Initial strength |
|---------|------------------|
| `t-bird-fly-vs-not_fly` | 4.0 |
| `t-mammal-fly-vs-swim` | 2.0 |
| `t-insect-fly-vs-crawl` | 2.0 |

All reopened after reintroduction with recalculated strength from expanded groups.

---

## Question Generation

Three emergent questions via `emerge_questions_from_tensions()` — one per persistent tension. Same text pattern as EXP-017 extended to Insect category.

---

## Extinction Mechanism

`resolve_tension()` for all three tensions, then `drive_question_to_extinction()` per question id.

Bird: two decay steps after resolution. Mammal/Insect: immediate EXTINCT after resolution (vitality 2.0 − 2.0 = 0.0).

---

## Memory Trace Creation

`archive_and_delete_extinct_questions()` — same as EXP-017:

```python
trace_strength = min(1.0, tension.strength / 4.0)
```

| Trace | Strength |
|-------|----------|
| Bird | 1.00 |
| Mammal | 0.50 |
| Insect | 0.50 |

---

## Coalition Mechanism

`form_coalitions(traces)`:

```python
weak_traces = [t for t in traces if t.trace_strength < INITIAL_TRACE_STRENGTH]
if len(weak_traces) < 2:
    return []
# single coalition from all weak traces, combined_strength = sum
```

**Intended behavior:** Mammal + Insect (both 0.50) → coalition with combined strength 1.00.

**Observed outcome (completed experiment):** No coalitions formed. Coalition list empty at competition phase. Individual entries only entered competition.

Possible gap between intended coalition logic and observed run documented in `exp018_failures.md`.

---

## Competition Mechanism

`build_competition_entries()` creates:

1. One **individual** entry per eligible trace
2. One **coalition** entry per formed coalition (none in completed run)

Entries sorted by `(-strength, entry_id)`. Top `RECONSTRUCTION_BUDGET` entries win.

With no coalitions, competition reduced to EXP-017 individual ranking:

| Rank | Entry | Strength |
|------|-------|----------|
| 1 | `individual-mem-eq-bird-fly-vs-not_fly` | 1.00 |
| 2 | `individual-mem-eq-insect-fly-vs-crawl` | 0.50 |
| 3 | `individual-mem-eq-mammal-fly-vs-swim` | 0.50 |

Budget = 1 → Bird wins.

---

## Reconstruction Winners

Single winner: `eq-bird-fly-vs-not_fly`

- Reconstructed solo (`coalition_id=""`)
- Identity preserved
- Vitality = reopened Bird tension strength
- Mammal and Insect not reconstructed

---

## Question Statistics

| Metric | Value |
|--------|-------|
| Deleted (archived) | 3 |
| Live after competition | 1 |
| Reconstruction winners | 1 |
| Coalitions formed | **0** |
| Memory traces retained | 3 |

---

## Overall Assessment

EXP-018 extended EXP-017 with coalition infrastructure but produced a **negative result** in the completed run: cooperation did not emerge, selection reproduced EXP-017.

**Code structure:** Clean extension — `MemoryCoalition`, `CompetitionEntry`, dual entry types in one tournament. Coalition path is additive; when empty, behavior collapses to EXP-017.

**Scientific outcome:** Valuable falsification. Attempted cooperation did not change reconstruction outcomes. EXP-017 selection mechanism confirmed robust.

**Key finding:** The experiment strengthens EXP-017 rather than extending the memory arc with cooperation. Next cooperation attempt requires richer prerequisites (see failures doc).

**Mismatch note:** Implementation includes coalition formation logic for weak traces; completed experiment reported zero coalitions. Code analysis records both the intended mechanism and the observed negative outcome for honest memory.
