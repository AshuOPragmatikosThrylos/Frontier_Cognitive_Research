# EXP-025 Code Analysis

Post-experiment read-only analysis of difference removal and dual-world comparison.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-025)

---

## Files Involved

| File | Role in EXP-025 |
|------|-----------------|
| `experiments/exp025_difference_removal.py` | Dual-world pipeline from observations; optional difference layer; side-by-side reporting |

No `src/` modules imported or used. Self-contained. Prior experiment files untouched.

New relative to EXP-024:

| Addition | Purpose |
|----------|---------|
| `differences_enabled: bool` on `WorldState` | World mode flag |
| `raw_entities: list[str]` | World B only — flat entity stream |
| `register_raw_entity()` | World B — append entity without category/behavior indexing |
| `ingest_observation_batch()` | Branching ingest for both worlds |
| `process_raw_reintroduction()` | World B — log flat observations |
| `organization_survives()` | World A: groups > 0; World B: always False |

Removed from EXP-024: tension layer entirely.

---

## Execution Flow

### Shared input (both worlds)

Same entity tuples from Bird/Mammal/Insect observation constants (16 initial + 12 reintro = 28 entities).

### World A path

```python
ingest_initial_observations(state)   # register_observation + form_difference_groups
process_reintroduction(state)        # refresh members + process_difference_reintroduction
```

### World B path

```python
ingest_initial_observations(state)   # register_raw_entity only
process_reintroduction(state)        # process_raw_reintroduction
```

### Experiment driver

```python
world_a = run_world(differences_enabled=True)
world_b = run_world(differences_enabled=False)
```

---

## World A Mechanisms

**Observation registration — `register_observation()`:**

- Append `RawObservation(entity, category, behavior)`
- Index into `category_index[category][behavior]`

**Difference formation — `form_difference_groups()`:**

- Requires ≥2 behaviors per category, each with ≥2 members
- Creates `DifferenceGroup` with name `{Category}.{behavior_key}`

**Reintroduction — `process_difference_reintroduction()`:**

- Refresh member lists via `refresh_group_members()`
- Log active difference groups with member counts

**Not used:** tensions, questions, memory, persistence, selection, reconstruction.

---

## World B Mechanisms

**Raw registration — `register_raw_entity()`:**

- Append entity string to `raw_entities` only
- **No** category index, **no** behavior indexing, **no** group formation

**Reintroduction — `process_raw_reintroduction()`:**

- Log total raw count and last 12 entities as `raw observation: {entity}`
- **No** labels, categories, partitions, or distinction objects

**Removed entirely:** `category_index` population, `difference_groups`, all structural parsing of category/behavior fields.

---

## Difference Formation

**World A only.** Six groups after full pipeline:

| Category | Groups |
|----------|--------|
| Bird | `Bird.fly`, `Bird.not_fly` |
| Mammal | `Mammal.fly`, `Mammal.swim` |
| Insect | `Insect.fly`, `Insect.crawl` |

Threshold: `DIFFERENCE_MIN_PER_GROUP = 2`.

Member counts grow on reintroduction (+2 per behavior group). **Invariant — World B has no equivalent structure.**

---

## Difference Removal

World B implements removal by **branching before structural parsing**:

```python
if state.differences_enabled:
    register_observation(state, entity, obs_category, behavior)
else:
    register_raw_entity(state, entity)
```

Category and behavior fields in source tuples are **ignored** for structure in World B — only entity names retained in order.

No stub groups, empty partitions, or disabled difference flags — the layer is absent.

---

## Organization Patterns

| Layer | World A | World B |
|-------|---------|---------|
| Observations | 28 structured | 28 flat |
| Difference groups | 6 | **none** |
| Categories | 3 | **none** |
| Partitions | 6 | **none** |
| Organization survives | **True** | **False** |

World A proves **structure with difference groups alone**. World B proves **no structure without them**.

---

## Surviving Motifs

| Motif | World A | World B |
|-------|---------|---------|
| Differences | 6 | 0 |
| Categories | 3 | 0 |
| Partitions | 6 | 0 |
| Raw entities | 28 | 28 |
| Tensions | 0 | 0 |
| Questions | 0 | 0 |
| Organization | Yes | **No** |

**Survivor in World A:** difference groups only. **World B:** no surviving organizational motif.

---

## Side-by-Side Comparison

Print functions:

| Function | Content |
|----------|---------|
| `print_world_statistics()` | Observations, groups, categories, organization flag |
| `print_organization_patterns()` | Layer contrast; World A groups vs World B raw tail |
| `print_surviving_motifs()` | Motif counts including collapse in World B |
| `print_overall_observations()` | Interpretation — differences necessary |

Key contrast: identical entity counts; World A has six groups and organization; World B has flat list and collapse.

---

## Collapse Conditions

`organization_survives()` logic:

```python
if not state.differences_enabled:
    return False
return len(state.difference_groups) > 0
```

**Collapse triggers in World B:**

1. `differences_enabled=False` — organizational criterion never met
2. Zero difference groups — no partitions form from flat stream
3. No category index — no behavioral distinction objects

Same 28 entities as World A; collapse is **mechanism-dependent**, not input-dependent.

---

## Overall Assessment

EXP-025 is the **fifth and final destructive test** in the reduction arc (EXP-021–025). It attacks the bedrock candidate — differences — and finds **organizational collapse** when difference groups are removed.

**Strengths:**

- Minimal split: single `differences_enabled` flag
- World B truly omits difference layer (not hollow stubs)
- Clean collapse condition — first falsification of "organization survives removal"
- Completes reduction program with identifiable bedrock

**Limitations (see exp025_failures.md):**

- No deeper motif discovered below difference
- World B discards category/behavior entirely — does not test partial difference removal
- Toy pipeline only

**Scientific value:**

Marks **successful completion of reduction phase**. Difference confirmed as deepest surviving organizing principle. Establishes foundation for **growth from difference** (Phase VI).

**Central image:** Same 28 entities — World A sees six groups; World B sees a list — organization lives or dies on that distinction.
