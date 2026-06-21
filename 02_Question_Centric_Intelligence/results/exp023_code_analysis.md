# EXP-023 Code Analysis

Post-experiment read-only analysis of question removal and dual-world comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-023)

---

## Files Involved

| File | Role in EXP-023 |
|------|-----------------|
| `experiments/exp023_question_removal.py` | Dual-world pipeline through tensions; optional question layer; side-by-side reporting |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-022:

| Addition | Purpose |
|----------|---------|
| `questions_enabled: bool` on `WorldState` | World mode flag |
| `process_question_lifecycle()` | World A only — emerge through extinct |
| `delete_extinct_questions()` | World A — remove questions without memory traces |
| `process_question_reintroduction()` | World A — fresh emergence |
| `process_tension_only_reintroduction()` | World B — log active tensions only |
| No `MemoryTrace` dataclass usage | Memory layer absent in both worlds |

Removed from EXP-022: persistent/transient memory split, reconstruction, decay events.

---

## Execution Flow

### Shared phases (both worlds)

```python
ingest_initial_observations(state)   # Bird, Mammal, Insect — 16 obs
# → form_difference_groups, record_tensions
```

### World A additional phase

```python
process_question_lifecycle(state)
# emerge → promote → resolve → extinct → delete_extinct_questions
```

### Shared reintroduction (divergent handler)

```python
ingest_reintroduction_observations(state)
reopened = reopen_all_tensions(state)

if state.questions_enabled:
    process_question_reintroduction(state, reopened)
else:
    process_tension_only_reintroduction(state, reopened)
```

### Experiment driver

```python
world_a = run_world(questions_enabled=True)
world_b = run_world(questions_enabled=False)
```

---

## World A Mechanisms

**Question lifecycle — `process_question_lifecycle()`:**

1. `emerge_questions_from_tensions()` — one question per persistent tension
2. `promote_emergent_questions()` — EMERGENT → ACTIVE
3. `resolve_tension()` for each category — vitality reduction
4. `drive_question_to_extinction()` — decay loop per question
5. `delete_extinct_questions()` — remove EXTINCT questions, **no archival**

**Reintroduction — `process_question_reintroduction()`:**

- Reintroduce observations, refresh groups, reopen tensions
- `emerge_fresh_question()` for each persistent reopened tension
- Three fresh emergences; questions live at end

**Not used:** memory traces, reconstruction, question identity preservation across cycles.

---

## World B Mechanisms

**Initial phase:** ingest only — differences and tensions recorded. **No question lifecycle invoked.**

**Reintroduction — `process_tension_only_reintroduction()`:**

- Same reintro + reopen as World A
- Log `tension active: {id} strength={s} (no question object)`
- **No** `emerge_fresh_question()`, **no** question IDs, **no** states

**Removed entirely:** Question class usage, question identity, question memory, question reconstruction, fresh emergence.

---

## Difference Formation

Identical both worlds. Six groups after full pipeline:

| Category | Groups |
|----------|--------|
| Bird | `Bird.fly`, `Bird.not_fly` |
| Mammal | `Mammal.fly`, `Mammal.swim` |
| Insect | `Insect.fly`, `Insect.crawl` |

Member counts grow on reintroduction (+2 per behavior group). **Invariant across worlds.**

---

## Tension Structures

Three persistent tensions; `reopen_tension()` recalculates strength:

| Tension | Post-reintro strength | Persistent |
|---------|----------------------|------------|
| `t-bird-fly-vs-not_fly` | 6.0 | Yes |
| `t-mammal-fly-vs-swim` | 4.0 | Yes |
| `t-insect-fly-vs-crawl` | 4.0 | Yes |

World B: tensions logged as active without question compression. **Structure identical to World A at tension layer.**

---

## Question Layer

**World A only.**

| Stage | Count |
|-------|-------|
| Initial emergent | 3 |
| Extinct before reintro | 3 (deleted) |
| Fresh emergent after reintro | 3 |
| Live at end | 3 |

Question ids: `eq-bird-fly-vs-not_fly`, `eq-mammal-fly-vs-swim`, `eq-insect-fly-vs-crawl`.

**World B:** question layer never instantiated — `lifecycle_questions` dict empty throughout.

---

## Question Removal

World B implements removal by **branching before question lifecycle**:

```python
if state.questions_enabled:
    process_question_lifecycle(state)
# World B skips entirely
```

No stub question objects, no null question ids, no empty states — the layer is absent, not disabled.

`organization_survives()` = `difference_groups > 0 AND persistent_tensions > 0` → **True both worlds**.

---

## Organization Patterns

| Layer | World A | World B |
|-------|---------|---------|
| Observations | 28 | 28 |
| Difference groups | 6 | 6 |
| Persistent tensions | 3 | 3 |
| Questions | 3 live | **none** |
| Structure without questions | N/A | **Yes** |

World B proves **structure without questions** at full organizational parity on difference+tension metrics.

---

## Surviving Motifs

| Motif | World A | World B |
|-------|---------|---------|
| Differences | 6 | 6 |
| Tensions | 3 | 3 |
| Questions | 3 | 0 |
| Fresh emergence | 3 | 0 |
| Question IDs | Yes | **No** |
| Question states | Yes | **No** |

**Survivor in World B:** difference groups + persistent tensions only.

---

## Side-by-Side Comparison

Print functions:

| Function | Content |
|----------|---------|
| `print_world_statistics()` | Observations, groups, tensions, questions, organization flag |
| `print_organization_patterns()` | Layer-by-layer; per-tension strength comparison |
| `print_surviving_motifs()` | Motif counts including question-layer absence |
| `print_overall_observations()` | Interpretation — questions optional |

Key contrast: identical difference+tension skeleton; World A adds live question compression layer.

---

## Overall Assessment

EXP-023 is the **third destructive test** in the sequence (after EXP-021 selection, EXP-022 persistence). It attacks the program's namesake primitive — questions — and finds organization **unchanged** at the difference+tension floor.

**Strengths:**

- Minimal split: single `questions_enabled` flag
- World B truly omits question layer (not hollow stubs)
- No memory noise — isolates question necessity cleanly
- Directly tests "Question-Centric" claim

**Limitations (see exp023_failures.md):**

- Organization still depends on tensions and differences
- World A fresh emergence may mask whether initial lifecycle was necessary for World B parity
- Tension/difference attacks not yet performed

**Scientific value:**

One of the most important experiments completed. Establishes candidate hierarchy: **Difference → Tension**; everything above optional. Reframes entire program from question-centric to **tension-centric with optional question compression**.

**Central image:** Same six groups, same three tensions — World A asks "why?" three times; World B doesn't — both worlds equally organized.
