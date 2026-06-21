# EXP-024 Code Analysis

Post-experiment read-only analysis of tension removal and dual-world comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-024)

---

## Files Involved

| File | Role in EXP-024 |
|------|-----------------|
| `experiments/exp024_tension_removal.py` | Dual-world pipeline through differences; optional tension layer; side-by-side reporting |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-023:

| Addition | Purpose |
|----------|---------|
| `tensions_enabled: bool` on `WorldState` | World mode flag |
| `detect_persistent_tensions()` / `record_tensions()` | World A only — pairwise group conflicts |
| `reopen_tension()` / `reopen_all_tensions()` | World A — refresh strength on reintroduction |
| `process_tension_reintroduction()` | World A — log active tensions |
| `process_difference_only_reintroduction()` | World B — log active groups only |
| `organization_survives()` | Branching criterion: groups + tensions (A) vs groups alone (B) |

Removed from EXP-023: question lifecycle, fresh emergence, question IDs/states.

---

## Execution Flow

### Shared phases (both worlds)

```python
ingest_initial_observations(state)   # Bird, Mammal, Insect — 16 obs
# → form_difference_groups
# World A additionally: record_tensions per category
```

### Reintroduction (divergent handler)

```python
ingest_reintroduction_observations(state)   # +12 obs, refresh members
# World A: reopen_all_tensions → process_tension_reintroduction
# World B: process_difference_only_reintroduction
```

### Experiment driver

```python
world_a = run_world(tensions_enabled=True)
world_b = run_world(tensions_enabled=False)
```

---

## World A Mechanisms

**Initial phase — `ingest_category_observations()` with `tensions_enabled=True`:**

1. `register_observation()` — accumulate entities per category/behavior
2. `form_difference_groups()` — create groups when ≥2 behaviors with ≥2 members
3. `record_tensions()` — append persistent tensions from `detect_persistent_tensions()`

**Tension detection — `detect_persistent_tensions()`:**

- Pairwise compare groups within category
- Strength = `min(len(group_a.members), len(group_b.members))`
- Persistent when strength ≥ `PERSISTENT_TENSION_MIN` (2)
- IDs: `t-{category}-{behavior_a}-vs-{behavior_b}`

**Reintroduction — `process_tension_reintroduction()`:**

- Reintroduce observations, refresh group members, reopen all three known tension IDs
- Log `tension active: {id} strength={s}`
- Three persistent tensions at end

**Not used:** questions, memory traces, reconstruction, selection.

---

## World B Mechanisms

**Initial phase:** ingest and form difference groups only. **`record_tensions()` never called** — guarded by `if state.tensions_enabled` in `ingest_category_observations()`.

**Reintroduction — `process_difference_only_reintroduction()`:**

- Same reintro + member refresh as World A
- Log `difference active: {group_name} members={n} behavior={b}`
- **No** tension objects, IDs, or strength

**Removed entirely:** `PersistentTension` usage, tension detection, reopen logic, conflict representation.

---

## Difference Formation

Identical both worlds. Six groups after full pipeline:

| Category | Groups |
|----------|--------|
| Bird | `Bird.fly`, `Bird.not_fly` |
| Mammal | `Mammal.fly`, `Mammal.swim` |
| Insect | `Insect.fly`, `Insect.crawl` |

Member counts grow on reintroduction (+2 per behavior group). **Invariant across worlds.**

Thresholds: `DIFFERENCE_MIN_PER_GROUP = 2`; requires ≥2 distinct behaviors per category.

---

## Tension Layer

**World A only.**

| Tension | Post-reintro strength | Persistent |
|---------|----------------------|------------|
| `t-bird-fly-vs-not_fly` | 6.0 | Yes |
| `t-mammal-fly-vs-swim` | 4.0 | Yes |
| `t-insect-fly-vs-crawl` | 4.0 | Yes |

Tensions summarize pairwise conflicts between difference groups within a category.

**World B:** tension layer never instantiated — `persistent_tensions` list empty throughout.

---

## Tension Removal

World B implements removal by **branching before tension recording**:

```python
if state.tensions_enabled:
    record_tensions(state, category)
# World B skips entirely
```

Reintroduction similarly branches in `process_reintroduction()` — World B calls `process_difference_only_reintroduction()` instead of reopen + tension logging.

No stub tension objects, no zero-strength placeholders — the layer is absent, not disabled.

`organization_survives()`:

- World A: `difference_groups > 0 AND persistent_tensions > 0`
- World B: `difference_groups > 0` only → **True both worlds**

---

## Organization Patterns

| Layer | World A | World B |
|-------|---------|---------|
| Observations | 28 | 28 |
| Difference groups | 6 | 6 |
| Persistent tensions | 3 | **none** |
| Questions | none | none |
| Structure without tensions | N/A | **Yes** |

World B proves **structure without tensions** at full organizational parity on difference-group metrics.

---

## Surviving Motifs

| Motif | World A | World B |
|-------|---------|---------|
| Differences | 6 | 6 |
| Tensions | 3 | 0 |
| Tension strength tracking | Yes | **No** |
| Questions | 0 | 0 |
| Difference-only structure | No | **Yes** |

**Survivor in World B:** difference groups only.

---

## Side-by-Side Comparison

Print functions:

| Function | Content |
|----------|---------|
| `print_world_statistics()` | Observations, groups, tensions, organization flag |
| `print_organization_patterns()` | Layer-by-layer; per-group member comparison |
| `print_surviving_motifs()` | Motif counts including tension-layer absence |
| `print_overall_observations()` | Interpretation — tensions optional |

Key contrast: identical difference skeleton; World A adds persistent tension summary layer above groups.

---

## Overall Assessment

EXP-024 is the **fourth destructive test** in the sequence (after EXP-021 selection, EXP-022 persistence, EXP-023 questions). It attacks the post-EXP-023 organizing floor — tensions — and finds organization **unchanged** at the difference layer.

**Strengths:**

- Minimal split: single `tensions_enabled` flag
- World B truly omits tension layer (not hollow stubs)
- No question/memory noise — isolates tension necessity cleanly
- Directly tests tension-as-fundamental claim from EXP-023

**Limitations (see exp024_failures.md):**

- Organization still depends on differences
- World A tension reopen uses hardcoded `ALL_TENSION_IDS` — assumes known conflict topology
- Difference attack not yet performed

**Scientific value:**

One of the most important experiments completed so far. Establishes candidate hierarchy: **Difference** as current floor; everything above optional. Reframes program from tension-centric to **difference-centric**.

**Central image:** Same six groups — World A labels three pairwise conflicts; World B doesn't — both worlds equally organized.
