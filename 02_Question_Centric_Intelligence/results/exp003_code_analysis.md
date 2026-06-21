# EXP-003 Code Analysis

Post-experiment read-only analysis of hierarchical question evolution.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-003)

---

## Files Involved

| File | Role in EXP-003 |
|------|-----------------|
| `experiments/exp003_hierarchical_questions.py` | Experiment driver; stage 1 and stage 2 merge orchestration |
| `src/curiosity_engine.py` | Entity question creation (one per anomaly) |
| `src/world_model.py` | Category → behavior rules |
| `src/question_merger.py` | Stage 1 bird merge via similarity grouping |
| `src/question_repository.py` | Storage; `merge_questions()` with genealogy |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

EXP-003 logic for mammal merge, stage 2 merge, and generation tracking lives entirely in the experiment file. No shared `src/` modules were modified for EXP-003.

---

## Execution Flow

### Phase 1: Observations

Fixed observation order (same as EXP-001/EXP-002):

1. Five normal observations — no questions created
2. Six anomalies — six entity questions at generation 0

Each entity question registered with `register_generation(id, 0)`.

### Phase 2: Stage 1 Merges

**2a — Bird merge (shared `question_merger.py`):**

- `find_merge_candidates()` groups by `(category, expected_behavior, observed_behavior)`
- One group: `(Bird, fly, not fly)` → four entities
- `merge_candidates()` creates `q-abstract-bird-fly`
- Four calls to `merge_questions()` — sources → PARTIALLY_RESOLVED
- Generation 1 assigned to bird abstract

**2b — Mammal merge (EXP-003 local):**

- `find_mammal_cross_candidates()` selects questions where `category == "Mammal"` and `expected_behavior` is empty
- Bat and Whale qualify (cross-category anomalies)
- `merge_mammal_abstraction()` creates `q-abstract-mammal-capabilities`
- Two calls to `merge_questions()`
- Generation 1 assigned to mammal abstract

**Stage 1 merge count:** 6

### Phase 3: Stage 2 Merge

**Meta merge (EXP-003 local):**

- Condition: both bird and mammal abstracts exist
- `merge_hierarchical_abstraction()` creates `q-abstract-species-capabilities`
- Text: `"Why do species gain or lose capabilities?"`
- Merges bird abstract and mammal abstract as sources
- Two calls to `merge_questions()` — category abstracts → PARTIALLY_RESOLVED
- Generation 2 assigned to meta abstract

**Stage 2 merge count:** 2

### Phase 4: Reporting

Prints hierarchy (top-down from meta), generations, merge counts, repository statistics.

---

## Stage 1 Merge Mechanism

### Bird path (similarity-based)

Uses EXP-002 machinery unchanged:

```python
similarity_key = (category, expected_behavior, observed_behavior)
minimum_group_size = 2
abstract_text = f"Why don't some {category.lower()}s {expected_behavior}?"
```

### Mammal path (category-based)

EXP-003-specific rule:

```python
category == "Mammal" and not expected_behavior
minimum_group_size = 2
abstract_text = "Why do some mammals gain unexpected capabilities?"
```

Cross-category mammals do not share a similarity triple with birds. A separate grouping rule was required for stage 1 mammal abstraction.

---

## Stage 2 Merge Mechanism

Explicit hierarchical merge — not similarity-driven:

```python
merge_hierarchical_abstraction(
    repository,
    [bird_abstract.id, mammal_abstract.id],
    "q-abstract-species-capabilities",
    "Why do species gain or lose capabilities?",
)
```

Creates new question, then calls `merge_questions()` for each category abstract. No automatic detection — stage 2 is hardcoded to merge exactly these two abstractions when both exist.

This is a **second-pass merge** layered on top of stage 1, not an emergent property of similarity grouping alone.

---

## Generation Assignment

Generations tracked in experiment-local dict `GENERATIONS`:

| Generation | Assignment | Questions |
|------------|------------|-----------|
| 0 | `register_generation()` after entity creation | 6 entity questions |
| 1 | After stage 1 abstract creation | 2 category abstractions |
| 2 | After stage 2 meta creation | 1 meta abstraction |

Generation is **not** a field on `Question`. It is computed and stored externally during the experiment run. Genealogy depth could alternatively be derived from `parent_questions` chain length.

---

## Parent-Child Genealogy

Link direction follows EXP-002 convention:

- **Target (abstract)** holds `parent_questions` listing source ids
- **Source (entity or lower abstract)** holds `child_questions` listing target id

After all merges:

**Meta (gen 2):**
- `parent_questions`: `[q-abstract-bird-fly, q-abstract-mammal-capabilities]`

**Bird abstract (gen 1):**
- `parent_questions`: `[q-penguin, q-ostrich, q-emu, q-kiwi]`
- `child_questions`: `[q-abstract-species-capabilities]`

**Mammal abstract (gen 1):**
- `parent_questions`: `[q-bat, q-whale]`
- `child_questions`: `[q-abstract-species-capabilities]`

**Entity questions (gen 0):**
- `child_questions`: `[q-abstract-bird-fly]` or `[q-abstract-mammal-capabilities]`

All nine questions remain in repository. No deletions at any stage.

---

## State Transitions

| Stage | Question | Before | After |
|-------|----------|--------|-------|
| Entity creation | 6 entities | — | NEW |
| Stage 1 bird merge | 4 birds | NEW | PARTIALLY_RESOLVED |
| Stage 1 bird merge | bird abstract | — | ACTIVE |
| Stage 1 mammal merge | Bat, Whale | NEW | PARTIALLY_RESOLVED |
| Stage 1 mammal merge | mammal abstract | — | ACTIVE |
| Stage 2 meta merge | 2 category abstracts | ACTIVE | PARTIALLY_RESOLVED |
| Stage 2 meta merge | meta abstract | — | ACTIVE |

**Final state distribution:**

| State | Count |
|-------|-------|
| ACTIVE | 1 |
| PARTIALLY_RESOLVED | 8 |

`get_active_questions()` treats PARTIALLY_RESOLVED as active for counting purposes, but only one question holds ACTIVE state — the meta abstraction.

---

## Curiosity Debt Accounting

### Entity creation

Each entity: `DEBT_INCREMENT = 1.0`

### Stage 1 aggregation

- Bird abstract: `4.0` (sum of four entities)
- Mammal abstract: `2.0` (sum of Bat + Whale)
- Entities retain individual `1.0` each

### Stage 2 aggregation

- Meta abstract: `6.0` (bird abstract 4.0 + mammal abstract 2.0)
- Category abstracts retain their debt after demotion to PARTIALLY_RESOLVED

### Repository total

`6.0 (entities) + 4.0 (bird) + 2.0 (mammal) + 6.0 (meta) = 18.0`

Debt is **copied upward, not moved**. Each merge adds source debt to target while source retains its own. This produces multi-level double-counting — relevant to the attention collapse observation.

---

## Presence or Absence of Randomness

| Source | Present? | Affects behavior? |
|--------|----------|-------------------|
| `random` | No | — |
| `uuid` | No | Removed in EXP-002 architecture |
| `hash` | No | — |
| Deterministic ids | Yes | `q-{entity}`, `q-abstract-bird-fly`, etc. |
| `time.time()` | Yes | Timestamps only; not read by merge logic |

**Fully deterministic.** Fixed observation order, fixed merge stages, fixed abstract ids and text templates.

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Explicit rules at each stage produce identical hierarchy, genealogy, and states on every run.

**D — Emergent from interactions between simple rules** (partial)

The three-level tree is not fully hardcoded — it emerges from stage 1 similarity + stage 1 mammal rule + stage 2 explicit merge. But stage 2 requires hardcoded source ids and text; it does not auto-detect meta-merge candidates.

### Comparison Across Experiments

| Property | EXP-001 | EXP-002 | EXP-003 |
|----------|---------|---------|---------|
| Merge levels | 0 (dedup) | 1 | 2 |
| Questions after | 3 | 7 | 9 |
| Genealogy depth | 0 | 1 | 2 |
| ACTIVE at end | 3 | 7 | 1 |
| Diversity loss | Low | Medium | High |

### Key findings

| Property | Finding |
|----------|---------|
| Hierarchical merge | Works across two stages |
| Generation structure | Maps cleanly to merge depth |
| Genealogy | Preserved at all levels |
| Stage 2 | Requires explicit orchestration, not similarity alone |
| Failure mode | Attention collapse to single ACTIVE question |
| Debt accounting | Multi-level double-counting persists |

### Conclusion

EXP-003 demonstrates hierarchical question evolution with minimal machinery. The experiment succeeds at building a multi-generation question tree but reveals that unchecked abstraction may homogenize the question ecosystem — motivating H38–H40 and the pivot toward graph communities in future work.
