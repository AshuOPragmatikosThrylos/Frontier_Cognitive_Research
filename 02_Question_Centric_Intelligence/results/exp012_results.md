# EXP-012 Results

Post-experiment summary for emergent questions.

Date: 2026-06-22  
Experiment: EXP-012 Emergent Questions

---

## Theme

Emergent Questions

Test whether question-like structures can arise from difference dynamics alone, without pre-instantiated Question objects — addressing H98 from EXP-011 (questions as compressed representations of differences).

---

## Experiment Summary

Started from observations only on the standard 10-observation sequence (4 bird conforming, 4 bird contradicting, 2 mammal contradicting).

No `Question` objects from `src.question` were instantiated initially. The pipeline used local dataclasses only: `RawObservation`, `DifferenceGroup`, `PersistentTension`, `EmergentQuestion`.

### Causal chain

```
observations → difference groups → persistent tensions → emergent questions
```

| Stage | Mechanism | Threshold |
|-------|-----------|-----------|
| Difference groups | Behavior buckets per category | ≥2 behaviors, ≥2 members each |
| Persistent tension | Pairwise group comparison | `strength = min(sizes) ≥ 2` |
| Emergent question | One question per persistent tension | Template from tension behaviors |

### Bird phase

Four flying birds and four flightless birds registered. Two difference groups formed:

| Group | Behavior | Members |
|-------|----------|---------|
| Bird.fly | fly | Sparrow, Robin, Eagle, Falcon |
| Bird.not_fly | not fly | Penguin, Ostrich, Emu, Kiwi |

Persistent tension detected: `fly` vs `not fly`, strength 4.0.

One emergent question emerged:

> *Why do Bird entities both fly and not fly?*

(`eq-bird-fly-vs-not_fly`, state EMERGENT, sources Bird.fly + Bird.not_fly)

### Mammal phase

Bat (fly) and Whale (swim) registered. Only one entity per behavior — below `DIFFERENCE_MIN_PER_GROUP = 2`. No difference groups formed. No tensions. No emergent question.

Mammal observations did not generate sufficient persistent tension and therefore no Mammal question emerged.

### Summary findings

Difference groups emerged.

Persistent tensions formed between difference groups.

Question-like structures emerged from persistent tensions.

Bird observations generated a persistent tension; a Bird question emerged.

Differences alone were insufficient for question emergence — persistence proved necessary (Mammal case).

The experiment demonstrated: **observations → differences → tensions → questions**

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H101** | Questions are emergent structures | `EmergentQuestion` created only after tension detection; no upfront instantiation |
| **H102** | Persistent differences generate questions | Bird tension (strength 4.0, persistent) → one question; Mammal (no persistence) → none |
| **H103** | Questions are compressed representations of tensions | Question text encodes the two conflicting behaviors and source groups from tension record |

---

## Strengthened Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H104** | Questions are not primitive objects | Full pipeline runs without `src.question.Question`; questions appear last in causal chain |

Builds on EXP-011 H98: questions may be derived, not foundational. EXP-012 provides a constructive demonstration — questions can be *generated* from lower-level structures.

---

## Unexpected Observations

1. **Questions emerged without explicit instantiation.** No question existed at experiment start; `EmergentQuestion` objects materialized only at the final stage.

2. **One persistent tension produced one emergent question.** Strict 1:1 mapping — no question proliferation from a single tension.

3. **Mammal observations failed to generate a question.** Two behaviors with one member each did not meet group-formation threshold — differences present but not persistent at group level.

4. **Differences alone were insufficient.** EXP-011 World D produced groups without questions; EXP-012 adds tension persistence as additional gate.

5. **Persistence proved necessary.** Transient or sub-threshold differences (Mammal) produce no question even when behavioral diversity exists.

---

## Surprising Observations

1. **The causal direction reversed.** Prior experiments (EXP-001+) assumed questions first, then organization. EXP-012: organization precursors (groups, tensions) precede questions.

2. **Questions appeared after tensions rather than before them.** Temporal ordering in code mirrors conceptual ordering: tension unresolved → question crystallizes.

3. **Question formation behaved like information compression.** Multi-entity, multi-group tension collapsed into a single interrogative string — lossy summary of persistent conflict (H107).

4. **The experiment partially redeemed Question-Centric Intelligence.** EXP-011 challenged the project name; EXP-012 reframes it: question-*centric* can mean questions emerge at the center of the pipeline's *output*, not its *input*.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H105** | Questions require persistence rather than mere differences |
| **H106** | Questions are symptoms rather than causes |
| **H107** | Question formation is a compression process |
| **H108** | Questions are higher-order structures built from tensions |

H105: Mammal has differences (fly vs swim) but no persistence at group threshold → no question.

H106: Questions mark unresolved state; they do not drive group formation (groups precede questions).

H108: Hierarchy: observations < groups < tensions < questions.

---

## Future Directions

- Investigate emergent communities (can communities arise from tension clusters like questions do?)
- Investigate question lifecycles (EMERGENT → ACTIVE → RESOLVED → disappearance)
- Study how questions disappear when tensions resolve
- Study multiple simultaneous tensions (what if Mammal also had persistent tension?)
- Study whether communities themselves can emerge from difference groups without preset Bird/Mammal containers

---

## Comparison: EXP-011 World D vs EXP-012

| Property | EXP-011 World D | EXP-012 |
|----------|-----------------|---------|
| Start | Observations | Observations |
| Groups | Yes (behavior) | Yes (behavior) |
| Questions | No | Emergent from persistent tension |
| Bird partition | Yes | Yes (groups) + question |
| Mammal | No groups | No groups, no question |
| Primitive | Difference | Difference + persistence |

EXP-012 extends World D with tension tracking and question emergence — testing H98 constructively.

---

## Conclusion

EXP-012 demonstrates that question-like structures can emerge from a difference-first pipeline without pre-instantiated Question objects. Bird behavioral conflict produced persistent tension and one emergent question; Mammal's weaker difference structure did not. Questions appear to be compressed, higher-order representations of persistent tensions (H103, H107, H108), not primitive cognitive units (H104).

The causal chain observations → differences → tensions → questions offers a path to reconcile difference-first findings (EXP-011) with the question-centric research program: questions may be emergent symptoms of unresolved organizational tension rather than foundational entities.

Note: Initial run crashed on `DifferenceGroup` sorting; repaired before results documented (see `exp012_failures.md`).
