# EXP-002 Code Analysis

Post-experiment read-only analysis of how EXP-002 Penguin World produced true question merging.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-002)

---

## Files Analyzed

| File | Role |
|------|------|
| `experiments/exp002_penguin_world.py` | Experiment driver; observation phase then merge phase |
| `src/world_model.py` | Category → behavior rules; prediction |
| `src/curiosity_engine.py` | One question per entity; no deduplication |
| `src/question_merger.py` | Similarity grouping; abstract question creation |
| `src/question_repository.py` | Storage; `merge_questions()` with genealogy |
| `src/question.py` | Question dataclass with similarity fields |
| `src/observation.py` | Observation dataclass |
| `results/exp001_code_analysis.md` | Prior analysis (deduplication baseline) |

---

## Search Results (Randomness)

Searched EXP-002 code path for:

`random`, `random()`, `choice()`, `shuffle()`, `sample()`, `numpy.random`, `secrets`, `uuid`, `hash`

| Term | Found in EXP-002 path? | Influences behavior? |
|------|------------------------|----------------------|
| `random` | No | — |
| `random()` | No | — |
| `choice()` | No | — |
| `shuffle()` | No | — |
| `sample()` | No | — |
| `numpy.random` | No | — |
| `secrets` | No | — |
| `hash` | No | — |
| `uuid` | No | Removed from `curiosity_engine.py` |

### Deterministic identifiers

```python
question_id = f"q-{entity.lower()}"                                    # curiosity_engine.py
observation.id = f"obs-{entity.lower()}-{observed.replace(' ', '-')}"   # curiosity_engine.py
abstract_id = f"q-abstract-{category.lower()}-{expected_behavior...}"    # question_merger.py
```

### time.time()

Used for observation timestamps only. Not read by merge or similarity logic.

### Conclusion on randomness

**No randomness present.** EXP-002 is fully deterministic given fixed observation order.

---

## Execution Flow

### Phase 1: Observations

`exp002_penguin_world.py` calls `observe()` for each tuple in fixed order.

#### Normal observations (no effect)

Sparrow, Robin, Dog, Cat, Salmon — predictions match rules; no questions created.

#### Flightless birds (four independent questions)

For each `(entity, Bird, not fly)`:

1. `observe()` → `predict("Bird")` = `"fly"`; `"not fly" != "fly"` → failure
2. `process_prediction_failure(entity, "Bird", "not fly", content)`
3. Creates question with:
   - `id`: `q-penguin`, `q-ostrich`, `q-emu`, `q-kiwi`
   - `text`: `"Why doesn't {entity} fly?"`
   - `category`: `"Bird"`
   - `expected_behavior`: `"fly"`
   - `observed_behavior`: `"not fly"`
   - `state`: `"NEW"`
   - `curiosity_debt`: `1.0`

No shared key. No deduplication. Four distinct repository entries.

#### Cross-category anomalies (no merge candidates)

Bat `(Mammal, fly)` and Whale `(Mammal, swim)`:

- `predict("Mammal")` → `None`
- Cross-category branch in `observe()` fires
- Questions created with empty `expected_behavior`
- `similarity_key()` returns `None` — excluded from merge grouping

### Phase 2: Merge detection

`find_merge_candidates(repository)`:

1. Iterate all questions in `MERGEABLE_STATES` = `{NEW, ACTIVE, INVESTIGATING}`
2. Compute `similarity_key(q)` = `(category, expected_behavior, observed_behavior)`
3. Group by key; return groups with `len >= 2`

Result: one group — `(Bird, fly, not fly)` → `[q-penguin, q-ostrich, q-emu, q-kiwi]`

### Phase 3: Merge execution

`merge_all_candidates()` → `merge_candidates()` for the bird group:

1. Create abstract question:
   - `id`: `q-abstract-bird-fly`
   - `text`: `"Why don't some birds fly?"`
   - `state`: `"ACTIVE"`
   - Inherits category/behavior fields from group

2. For each source in group, call:
   ```python
   repository.merge_questions(abstract.id, source.id, source_state="PARTIALLY_RESOLVED")
   ```

3. `merge_count` = 4

### Flow diagram

```
Observations
  Penguin  → q-penguin  (NEW, debt=1)
  Ostrich  → q-ostrich  (NEW, debt=1)
  Emu      → q-emu      (NEW, debt=1)
  Kiwi     → q-kiwi     (NEW, debt=1)
  Bat      → q-bat      (NEW, no similarity key)
  Whale    → q-whale    (NEW, no similarity key)

find_merge_candidates()
  group (Bird, fly, not fly) → [q-penguin, q-ostrich, q-emu, q-kiwi]

merge_candidates()
  create q-abstract-bird-fly
  merge q-penguin  → abstract.parent += penguin,  penguin.state = PARTIALLY_RESOLVED
  merge q-ostrich  → abstract.parent += ostrich,  ostrich.state = PARTIALLY_RESOLVED
  merge q-emu      → abstract.parent += emu,      emu.state = PARTIALLY_RESOLVED
  merge q-kiwi     → abstract.parent += kiwi,     kiwi.state = PARTIALLY_RESOLVED
  abstract.curiosity_debt = 4.0
```

---

## Question Merge Mechanism

### Similarity rule

Three-field exact match:

```python
(category, expected_behavior, observed_behavior)
```

All three must be non-empty. Questions in `NEW`, `ACTIVE`, or `INVESTIGATING` with identical triples are merge candidates.

Minimum group size: **2**.

### Abstract question creation

Template:

```python
f"Why don't some {category.lower()}s {expected_behavior}?"
```

Created **before** merging sources. Added to repository as a new entity.

### QuestionRepository.merge_questions()

Unlike EXP-001 (which deleted sources), EXP-002 **retains** source questions:

| Action | Target (abstract) | Source (original) |
|--------|-------------------|-------------------|
| Debt | `+= source.curiosity_debt` | unchanged |
| times_encountered | `+= source.times_encountered` | unchanged |
| related_observations | extend | unchanged |
| parent_questions | append source_id | — |
| child_questions | — | append target_id |
| state | unchanged (ACTIVE) | set to PARTIALLY_RESOLVED |
| deletion | — | **not deleted** |

### Merge vs EXP-001 deduplication

| | EXP-001 | EXP-002 |
|---|---------|---------|
| API used | In-place update via `_question_keys` | `merge_questions()` |
| Originals | Same object rewritten | Separate objects retained |
| Abstraction trigger | `times_encountered >= 2` | Similarity group size >= 2 |
| Genealogy | None | parent_questions / child_questions |
| When | During observation | After all observations |

---

## Parent-Child Genealogy

After merge:

**Abstract question (`q-abstract-bird-fly`):**
- `parent_questions`: `[q-penguin, q-ostrich, q-emu, q-kiwi]`
- `child_questions`: `[]`

**Each original (e.g. `q-penguin`):**
- `parent_questions`: `[]`
- `child_questions`: `[q-abstract-bird-fly]`

The abstract question holds references to its sources in `parent_questions`. Sources point back to the abstract in `child_questions`. Semantically the abstract generalizes the originals, but the link direction follows: sources → abstract as child.

No multi-generation tree in this experiment. Flat: four leaves → one abstract node.

---

## State Transitions

| Question | Before | After | Trigger |
|----------|--------|-------|---------|
| q-penguin | NEW | PARTIALLY_RESOLVED | merge_questions() |
| q-ostrich | NEW | PARTIALLY_RESOLVED | merge_questions() |
| q-emu | NEW | PARTIALLY_RESOLVED | merge_questions() |
| q-kiwi | NEW | PARTIALLY_RESOLVED | merge_questions() |
| q-abstract-bird-fly | — | ACTIVE | created in merge_candidates() |
| q-bat | NEW | NEW | no merge |
| q-whale | NEW | NEW | no merge |

States not used in EXP-002: `INVESTIGATING`, `RESOLVED`, `DORMANT`, `ABANDONED`.

`get_active_questions()` includes `PARTIALLY_RESOLVED`, so all seven post-merge questions are active.

---

## Curiosity Debt

### Per-entity creation

Each new question: `DEBT_INCREMENT = 1.0`

### On merge (aggregation to abstract)

Abstract receives sum of source debts: `1.0 + 1.0 + 1.0 + 1.0 = 4.0`

Sources **retain** their individual `1.0` — debt is copied to abstract, not moved.

### Repository total

`4.0 (abstract) + 4×1.0 (originals) + 1.0 (bat) + 1.0 (whale) = 10.0`

This double-counts bird debt relative to attention semantics — a design consequence, not a runtime bug.

---

## Heuristics Involved

| Heuristic | Location | Rule |
|-----------|----------|------|
| One question per entity | curiosity_engine.py | `question_id = f"q-{entity.lower()}"` |
| Mismatch detection | exp002 observe() | `behavior != expected` |
| Similarity key | question_merger.py | Exact triple match |
| Merge threshold | question_merger.py | Group size >= 2 |
| Mergeable states | question_merger.py | NEW, ACTIVE, INVESTIGATING only |
| Abstract text | question_merger.py | Pluralized category template |
| Source state after merge | merge_candidates() | PARTIALLY_RESOLVED (default) |
| Cross-category exclusion | similarity_key() | Empty expected_behavior → None |
| Observation order | exp002 main() | Fixed lists |
| Behavior owner | curiosity_engine.py | First matching rule in dict iteration order |

All heuristics are explicit and deterministic.

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed rules, fixed order, deterministic ids. Same inputs produce identical questions, merges, genealogy, and debt every run.

**D — Emergent from interactions between simple rules** (secondary)

The abstract question `"Why don't some birds fly?"` is not hardcoded per entity. It emerges from similarity grouping + merge template — but only when the explicit merge phase runs.

### Key findings

| Property | Finding |
|----------|---------|
| True merge | Yes — uses `merge_questions()`, originals retained |
| Genealogy | Yes — parent_questions on abstract, child_questions on sources |
| Randomness | Absent |
| Similarity | Exact triple match; no embeddings |
| Merge timing | Post-observation batch, not inline |
| EXP-001 regression | Architecture changed; EXP-001 now also creates separate entity questions (no merge step) |

### Research alignment

EXP-002 validates H9 (merge into abstractions) and H10 (descendant questions) more faithfully than EXP-001. The repository merge API — unused in EXP-001 — is now the central mechanism.

Open issue: genealogy link direction (abstract as child in `child_questions` on originals) may invert intuitive parent/child semantics and should be clarified in future experiments or documentation.

### Conclusion

EXP-002 demonstrates true question merging with preserved lineage using minimal deterministic machinery. The two-phase design (observe, then merge) separates question birth from abstraction — a cleaner test of H9 than EXP-001's in-place deduplication.
