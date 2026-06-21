# EXP-003 Results

Post-experiment summary for hierarchical question evolution.

Date: 2026-06-21  
Experiment: EXP-003 Hierarchical Question Evolution

---

## Theme

Hierarchical Question Evolution

Test whether questions can evolve through multiple abstraction levels — entity → category → meta — while preserving genealogy across generations.

---

## Experiment Summary

EXP-003 extended EXP-002 with a second merge stage. Six anomalies produced entity questions, which merged into two category abstractions, which merged into one meta abstraction.

### Generation 0: Entity Questions

Six independent questions born from compression failures:

| ID | Text | Initial State |
|----|------|---------------|
| q-penguin | Why doesn't Penguin fly? | NEW |
| q-ostrich | Why doesn't Ostrich fly? | NEW |
| q-emu | Why doesn't Emu fly? | NEW |
| q-kiwi | Why doesn't Kiwi fly? | NEW |
| q-bat | Why does Bat fly like a Bird? | NEW |
| q-whale | Why does Whale swim like a Fish? | NEW |

### Generation 1: Category Abstractions

Stage 1 merges produced two abstractions:

| ID | Text | Sources | Merge Count |
|----|------|---------|-------------|
| q-abstract-bird-fly | Why don't some birds fly? | 4 bird entities | 4 |
| q-abstract-mammal-capabilities | Why do some mammals gain unexpected capabilities? | Bat, Whale | 2 |

**Stage 1 merge count:** 6

### Generation 2: Meta Abstraction

Stage 2 merge combined both category abstractions:

| ID | Text | Sources | Merge Count |
|----|------|---------|-------------|
| q-abstract-species-capabilities | Why do species gain or lose capabilities? | Bird + Mammal abstractions | 2 |

**Stage 2 merge count:** 2  
**Total merge count:** 8

### Final Hierarchy

```
[gen 2] Why do species gain or lose capabilities?
  [gen 1] Why don't some birds fly?
    [gen 0] Why doesn't Penguin fly?
    [gen 0] Why doesn't Ostrich fly?
    [gen 0] Why doesn't Emu fly?
    [gen 0] Why doesn't Kiwi fly?
  [gen 1] Why do some mammals gain unexpected capabilities?
    [gen 0] Why does Bat fly like a Bird?
    [gen 0] Why does Whale swim like a Fish?
```

### Final Repository State

| Metric | Value |
|--------|-------|
| Total questions | 9 |
| Generation levels | 3 |
| ACTIVE | 1 (meta abstraction only) |
| PARTIALLY_RESOLVED | 8 |
| Total curiosity debt | 18.0 |

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H9** — Questions merge into abstractions | Entity questions merged into category and meta abstractions |
| **H10** — Questions produce descendants | Each merge created a new question with lineage to sources |
| **H17** — Intelligence may be graph evolution rather than fact accumulation | Repository grew into a three-level hierarchy with explicit links |
| **H20** — Questions reproduce | Category and meta questions born from prior questions |
| **H23** — Question species emerge | Bird and mammal question families formed before cross-domain meta merge |

---

## Unexpected Observations

1. **Hierarchical question structure emerged.** Three distinct generations appeared without being hardcoded per entity — only merge rules and stage ordering drove structure.

2. **Question generations appeared naturally.** Generation 0 (entities) → Generation 1 (categories) → Generation 2 (meta) mapped cleanly onto merge stages.

3. **Parent-child genealogies remained intact.** All nine questions persisted. `parent_questions` and `child_questions` links survived both merge stages.

---

## Surprising Observations

1. **Almost all questions became PARTIALLY_RESOLVED.** Eight of nine questions ended in PARTIALLY_RESOLVED after stage 2. Only the meta abstraction remained the focal active question.

2. **Only the highest abstraction remained ACTIVE.** Category abstractions — previously ACTIVE after stage 1 — were demoted when absorbed into the meta question.

3. **Attention collapsed upward.** Curiosity debt aggregated to the meta level (6.0 on the top question). Lower levels retained their debt but lost ACTIVE status. Investigation pressure concentrated at the apex.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H38** | Excessive abstraction destroys question ecosystems |
| **H39** | Intelligence requires diversity across abstraction levels |
| **H40** | Questions should resist over-abstraction |

H38–H40 arise from the observation that hierarchical merging collapsed diversity: one ACTIVE question at the top, eight PARTIALLY_RESOLVED below. The system may have over-compressed its question ecology.

---

## Future Directions

Investigate communities and graph structures rather than deeper trees.

Specifically:

- Horizontal question communities (EXP-006 theme) instead of vertical stacking
- Limits on merge depth or merge resistance (H40)
- Attention budgets that preserve investigation at multiple generations simultaneously
- EXP-004: test whether split operations can recover diversity after over-abstraction

---

## Conclusion

EXP-003 confirms that hierarchical question evolution works with deterministic rules. Multi-level abstraction, genealogy, and generation structure emerge from staged merges. However, the experiment also revealed a failure mode: attention collapse toward the highest abstraction, threatening question ecosystem diversity.

The tree grew successfully. Whether it grew wisely remains an open question.
