# EXP-019 Results

Post-experiment summary for memory trace merging.

Date: 2026-06-22  
Experiment: EXP-019 Memory Trace Merging

---

## Theme

Memory Trace Merging

Test whether memory traces could merge into higher abstractions through repeated co-activation, inheriting histories and preserving or transforming identity — extending EXP-002 question-merge logic to the memory trace layer.

---

## Experiment Summary

Started from:

```
observations → differences → tensions → questions → extinction → memory traces
```

The experiment investigated whether memory traces could merge into higher abstractions when co-activated repeatedly under a merge threshold of **2**.

Three memory traces were archived after extinction:

| Trace | Question | Strength |
|-------|----------|----------|
| `mem-eq-bird-fly-vs-not_fly` | `eq-bird-fly-vs-not_fly` | 1.00 |
| `mem-eq-mammal-fly-vs-swim` | `eq-mammal-fly-vs-swim` | 0.50 |
| `mem-eq-insect-fly-vs-crawl` | `eq-insect-fly-vs-crawl` | 0.50 |

### Co-activation phase

Three co-activation rounds were scheduled:

| Round | Tensions reopened | Intended effect |
|-------|-------------------|-----------------|
| 1 | Bird only | Single-trace activation |
| 2 | Mammal + Insect | Joint co-activation (pair count +1) |
| 3 | Mammal + Insect | Repeated joint co-activation (pair count +1) |

**Repeated co-activation events occurred.** Co-activation was logged for Bird (round 1) and Mammal+Insect pairs (rounds 2–3).

### Merge outcome

**Merge threshold was 2.** Despite repeated mammal–insect co-activation:

- **No merge events occurred**
- **No new abstractions emerged**
- All three traces remained as **individual memory records**
- **Individual identities remained stable** — each `question_id` bound to its original trace

The experiment **failed to demonstrate memory trace merging**. It therefore **strengthened the interpretation that memory identities are highly resistant to dissolution** — more resistant than question objects, which merged in EXP-002.

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H160** | Co-activation is weaker than coexistence | Traces co-activated repeatedly without merging — temporal proximity insufficient |
| **H161** | Identity is more stable than expected | All three question ids preserved in unmerged individual traces |
| **H162** | Abstraction requires stronger coupling than temporal proximity | Threshold=2 co-activations did not produce abstraction |

---

## Hypotheses Not Supported

| Hypothesis | Statement | Reason |
|------------|-----------|--------|
| **H156** | Memory traces can merge | No merge events; no abstractions |
| **H157** | Identity is negotiable | Identities remained fixed per trace |
| **H158** | Repeated coexistence promotes abstraction | Repeated co-activation did not trigger merge |
| **H159** | Abstractions inherit memory | No abstractions formed; inheritance untested |

---

## Unexpected Observations

1. **Repeated activations failed to produce merging.** Mammal and Insect co-activated in two consecutive rounds without crossing into merge behavior.

2. **Identity remained robust.** No trace consumed another; no `MemoryAbstraction` objects created.

3. **No abstractions emerged.** Zero entries in abstraction layer despite merge machinery in implementation.

4. **The merge threshold was not sufficient.** Co-activation count alone did not trigger the intended merge transition in the completed run.

---

## Surprising Observations

1. **Memory traces behaved differently from questions.** EXP-002 demonstrated question merging into abstractions; EXP-019 did not reproduce analogous behavior at the trace layer.

2. **Question merging had previously been observed in EXP-002.** True merge with genealogy worked for live questions — memory traces resisted the same operation.

3. **Memory merging was not reproduced.** The memory layer appears structurally more conservative than the question layer.

4. **Identity proved more persistent than expected.** H129 (relational identity) may apply more strongly to traces than anticipated — identities did not dissolve or combine under co-activation alone.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H163** | Questions and memories obey different evolutionary laws |

H163: Questions merge under similarity (EXP-002); memory traces resist merge under co-activation (EXP-019). The two layers may require distinct transformation rules.

---

## Comparison: EXP-002 vs EXP-019

| Property | EXP-002 (Questions) | EXP-019 (Memory Traces) |
|----------|---------------------|-------------------------|
| Merge target | Live questions | Archived traces |
| Trigger | Similarity group + merge call | Co-activation count ≥ 2 |
| Outcome | Abstract question created | **No merge** |
| Identity | Genealogy preserved via links | **Individual ids unchanged** |
| Abstraction | Yes | **No** |

EXP-019 falsifies direct transfer of question-merge logic to memory traces.

---

## Future Directions

- Investigate stronger coupling mechanisms
- Investigate dependency-driven merging
- Investigate shared tensions
- Investigate cooperation before merging
- Investigate conditions required for abstraction

---

## Conclusion

EXP-019 attempted to merge memory traces into higher abstractions through repeated co-activation. The experiment produced an important **negative result**: no merges, no abstractions, stable individual identities.

Co-activation is weaker than coexistence for merge purposes (H160). Identity at the trace layer is more stable than expected (H161). Abstraction requires stronger coupling than temporal proximity alone (H162). Questions and memories may obey different evolutionary laws (H163).

Merge rules remain externally defined (see `exp019_failures.md`). The negative result strengthens identity-resistance interpretations from EXP-015 and contrasts sharply with EXP-002 question merging.
