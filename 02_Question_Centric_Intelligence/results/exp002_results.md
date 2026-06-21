# EXP-002 Results

Post-experiment summary for true question merging (Penguin World).

Date: 2026-06-21  
Experiment: EXP-002 Penguin World — True Question Merge

---

## Theme

Test whether questions can merge into abstractions while preserving genealogy — not by deduplicating in place (EXP-001), but by creating independent questions first and then forming a higher-level parent through explicit merge.

---

## Procedure (completed)

1. Feed normal observations (no failures).
2. Feed six anomalies (four flightless birds, Bat, Whale).
3. Record repository before merge.
4. Detect merge candidates by similarity.
5. Create abstract question and call `QuestionRepository.merge_questions()`.
6. Record repository after merge, genealogy, and merge count.

---

## Observed Outcome

### Before merge

Six independent questions:

| ID | Text | State | Debt |
|----|------|-------|------|
| q-penguin | Why doesn't Penguin fly? | NEW | 1.0 |
| q-ostrich | Why doesn't Ostrich fly? | NEW | 1.0 |
| q-emu | Why doesn't Emu fly? | NEW | 1.0 |
| q-kiwi | Why doesn't Kiwi fly? | NEW | 1.0 |
| q-bat | Why does Bat fly like a Bird? | NEW | 1.0 |
| q-whale | Why does Whale swim like a Fish? | NEW | 1.0 |

One merge candidate group detected: `(Bird, fly, not fly)` — all four bird questions.

### After merge

Seven questions in repository (four originals retained, one abstract added):

| ID | Text | State | Debt | parent_questions |
|----|------|-------|------|------------------|
| q-abstract-bird-fly | Why don't some birds fly? | ACTIVE | 4.0 | q-penguin, q-ostrich, q-emu, q-kiwi |
| q-penguin | Why doesn't Penguin fly? | PARTIALLY_RESOLVED | 1.0 | — |
| q-ostrich | Why doesn't Ostrich fly? | PARTIALLY_RESOLVED | 1.0 | — |
| q-emu | Why doesn't Emu fly? | PARTIALLY_RESOLVED | 1.0 | — |
| q-kiwi | Why doesn't Kiwi fly? | PARTIALLY_RESOLVED | 1.0 | — |
| q-bat | Why does Bat fly like a Bird? | NEW | 1.0 | — |
| q-whale | Why does Whale swim like a Fish? | NEW | 1.0 | — |

**Merge count:** 4  
**Abstract questions created:** 1  
**Total curiosity debt:** 10.0  
**Active questions:** 7 (including PARTIALLY_RESOLVED originals)

### Genealogy

```
q-penguin  ──┐
q-ostrich  ──┼──► q-abstract-bird-fly  ("Why don't some birds fly?")
q-emu      ──┤      parent_questions: [q-penguin, q-ostrich, q-emu, q-kiwi]
q-kiwi     ──┘

Each original lists q-abstract-bird-fly in child_questions.
```

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H3** — Questions can merge | Four bird questions merged into one abstract |
| **H8** — Questions can evolve | Originals transitioned state; abstract question born |
| **H9** — Questions can merge into abstractions | `"Why don't some birds fly?"` created from four specifics |
| **H10** — Questions produce descendant questions | Abstract question spawned with lineage to four parents |
| **H21** — Questions reproduce through specialization | Entity-specific questions preceded generalized form |

---

## Unexpected Observations

1. **Repository grew, not shrank.** Merge added a question (6 → 7) rather than consolidating count. Originals were retained by design.

2. **Curiosity debt split.** Abstract question holds aggregated debt (4.0); each original retains its own debt (1.0). Total repository debt (10.0) exceeds what a single merged question would carry in EXP-001 (10.0 on one object).

3. **Bat and Whale excluded.** Cross-category questions lack `expected_behavior`; similarity key is `None`. No merge attempted — only one instance per cross-category pattern.

4. **PARTIALLY_RESOLVED still active.** `get_active_questions()` includes PARTIALLY_RESOLVED. All seven questions count as active after merge.

---

## Surprises

1. **True merge vs EXP-001 deduplication.** EXP-001 produced one question with debt 10.0 via in-place updates. EXP-002 produces explicit genealogy with a separate abstract entity — closer to the research notes on question evolution.

2. **Inverted tree direction.** The abstract question lists originals in `parent_questions`; originals list the abstract in `child_questions`. The generalized question is the *child* in the child_questions link, though it reads as the conceptual parent.

3. **Abstraction without embeddings.** Exact-match similarity on three fields `(category, expected_behavior, observed_behavior)` sufficed to trigger merge — no LLM or vector similarity required.

4. **Merge is post-hoc.** Observation phase and merge phase are separate. Abstraction does not happen on the second anomaly; it happens when `merge_all_candidates()` runs after all observations.

---

## Comparison with EXP-001

| Property | EXP-001 | EXP-002 |
|----------|---------|---------|
| Bird questions before abstraction | 1 (deduplicated) | 4 (independent) |
| Mechanism | Key reuse + text rewrite | Similarity group + `merge_questions()` |
| Originals after abstraction | N/A (same object) | Retained as PARTIALLY_RESOLVED |
| Genealogy | None | parent_questions / child_questions |
| Bird debt on abstract | 10.0 (triangular) | 4.0 (sum of four 1.0) |
| Randomness | uuid ids | None (deterministic ids) |

---

## Future Directions

1. **Merge timing** — Trigger merge after N similar questions, or when curiosity debt exceeds threshold, rather than a single post-pass.

2. **Debt accounting** — Decide whether debt transfers to abstract, stays on originals, or is split — avoid double-counting in attention budget.

3. **Cross-category abstraction** — Bat and Whale share `(Mammal, *, fly/swim)` patterns; extend similarity rules or require multiple mammals before merge.

4. **State refinement** — PARTIALLY_RESOLVED originals may should become DORMANT when abstract exists; clarify active vs inactive after merge.

5. **Attention competition** — Run attention budget (H12–H15) with abstract vs particular questions competing for investigation.

6. **EXP-003** — Test question split: abstract question spawns new child when a counterexample appears.

---

## Conclusion

EXP-002 confirms that true question merging is achievable with simple deterministic rules. Four entity-specific questions became one abstract question with preserved genealogy. The behavior differs meaningfully from EXP-001's deduplication — originals survive, lineage is explicit, and merge uses the repository API as designed.

Abstraction is no longer emergent from a counter threshold alone; it is an explicit second phase driven by similarity grouping.
