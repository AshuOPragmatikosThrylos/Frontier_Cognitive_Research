# EXP-011 Failures

Post-experiment failure analysis for minimal worlds comparison.

Date: 2026-06-22  
Experiment: EXP-011 Minimal Worlds

---

## Failure Analysis

No mechanical failure was observed. All four worlds executed independently on identical observations. World A reproduced EXP-009 outcomes. Worlds B and C correctly produced unstructured outputs. World D partitioned Bird by behavior difference without errors.

The significant finding is conceptual, not mechanical: **reduction proved more dangerous than randomness.** EXP-010's random control failed to reproduce organization but left the question-centric framework intact. EXP-011's minimal worlds succeeded in reproducing Bird partitioning without questions, communities, or pressure — directly challenging the project's central assumption.

---

## The Experiment Challenged the Central Assumption of Question-Centric Intelligence

The research program (EXP-001 through EXP-010) incrementally built question-based mechanisms:

- Questions as cognitive units (EXP-001)
- Question merge and genealogy (EXP-002–003)
- Question communities (EXP-004)
- Attention on questions (EXP-005–006)
- Community speciation of questions (EXP-007–008)
- Adaptive tolerance on question communities (EXP-009)
- Falsification against randomness (EXP-010)

EXP-011 asks: which of this machinery is **necessary**?

| Assumption | EXP-011 result |
|------------|----------------|
| Questions produce organization | **Falsified** — World B has questions, no organization |
| Observations suffice for structure | **Falsified** — World C has observations, no structure |
| Communities required for Bird partition | **Falsified** — World D partitions without communities |
| Pressure/tolerance required for Bird partition | **Falsified** — World D has neither |
| Difference detection sufficient for Bird partition | **Supported** — World D reproduces Bird grouping |

The project name — Question-Centric Intelligence — presumes questions are primitive. EXP-011 suggests they may be derivative.

---

## Questions Alone Failed to Produce Organization

World B created 10 questions with correct entity-behavior content. Curiosity engine processed prediction failures. All questions remained ACTIVE in a flat list.

```
World B: [q-sparrow] ACTIVE — How does Sparrow fly?
         [q-penguin] ACTIVE — How does Penguin not fly?
         ... (no grouping, no hierarchy, no speciation)
```

Questions stored information but did not **organize** it. Storage ≠ structure. This is stronger than EXP-010's finding (randomness ≠ organization) — it attacks whether questions themselves are organizational primitives.

Implication for H98: questions may be compressed **representations** of differences, not engines of organization.

---

## The Simplest World Reproduced Meaningful Partitioning

World D — behavior index + difference threshold — produced:

```
Bird.fly:      [Sparrow, Robin, Eagle, Falcon]
Bird.not_fly:  [Penguin, Ostrich, Emu, Kiwi]
```

This mirrors World A's semantic outcome:

```
Bird.Conforming:   [q-sparrow, q-robin, q-eagle, q-falcon]
Bird.Contradicting: [q-penguin, q-ostrich, q-emu, q-kiwi]
```

Same partition. Different machinery. World A requires ~270 lines of ecosystem logic; World D requires ~25 lines of difference logic.

**Reduction did not weaken the key phenomenon — it revealed a simpler generator.**

---

## Potential Implications

| Mechanism | Status after EXP-011 |
|-----------|---------------------|
| Questions | Descriptive, not fundamental (H98) |
| Communities | Higher-order grouping of differences (H99) |
| Pressure and tolerance | Higher-level descriptions of difference accumulation (H100) |
| Behavior difference detection | Surviving primitive (H97) |

Pressure and tolerance may be **stories we tell about differences** rather than primitive operations. Communities may be **named clusters of difference groups**. Questions may be **serialized difference records**.

These are hypotheses, not conclusions — but EXP-011 provides empirical motivation for each.

---

## What Improved vs EXP-010

| Aspect | EXP-010 | EXP-011 |
|--------|---------|---------|
| Control strategy | Random null | Progressive reduction |
| Attack on assumptions | Mechanism vs noise | Mechanism vs necessity |
| Surviving primitive | Pressure (not random) | Difference (not questions) |
| Risk to framework | Low (random failed) | High (minimal succeeded) |
| Scientific value | Falsification | Ablation / necessity analysis |

EXP-010 strengthened confidence in pressure mechanisms. EXP-011 **weakened confidence in questions as primitive** while strengthening difference detection.

---

## What Remains Externally Controlled

1. **DIFFERENCE_MIN_PER_GROUP = 2** — World D's split threshold is experimenter-imposed (same class of limitation as PRESSURE_SPLIT_LIMIT in EXP-009).

2. **Single minimal design** — World D uses behavior grouping only; other minimals untested (pairwise difference, entropy threshold, single-link clustering).

3. **Bird-only partition match** — Mammal does not split in A or D for different reasons (tolerance vs min_per_group); equivalence of outcomes is partial, not complete.

4. **Organization undefined formally** — "Organization" inferred from speciation events and group semantics; no metric distinguishes meaningful from arbitrary grouping.

5. **No emergent question test** — World D does not attempt to derive questions from differences; H98 remains untested.

6. **Observation sequence fixed** — 4+4 bird split is designed into the input; minimal world success may partly reflect input structure.

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Emergent questions** | Derive question objects from difference groups — test H98 |
| **Emergent communities** | Let communities form from difference clusters without preset Bird/Mammal |
| **Difference-first architectures** | Rebuild EXP-001+ using difference as primitive, questions as derived |
| **Minimal cognitive worlds** | Strip below World D — pairwise difference only, no categories |
| **Ablation within World A** | Remove tolerance, then pressure, then communities — find World A's minimal subset |
| **Alternative min_per_group values** | Test sensitivity of World D splits |
| **Formal organization metric** | Define organization independently of speciation event count |

---

## Reduction vs Randomness as Controls

EXP-010 and EXP-011 form complementary control strategies:

```
EXP-010: "Does randomness reproduce the phenomenon?"  → No
EXP-011: "Does simplification preserve the phenomenon?" → Yes (World D)
EXP-011: "Does the removed component alone suffice?"   → No (Worlds B, C)
```

Together: organization requires meaningful mechanism (EXP-010) but not the specific mechanisms built so far (EXP-011). The surviving primitive appears to be **behavior difference detection**, not questions or pressure.

---

## The Naming Crisis

If questions are not fundamental, "Question-Centric Intelligence" misnames the research object. Candidate reframings implied by EXP-011:

- Difference-Centric Intelligence
- Organization from Contradiction (retained from early notes)
- Minimal Cognitive Ecology

This is not a failure of the experiment — it is the experiment working. Reduction successfully attacked assumptions the construction phase could not test.

---

## Overall Assessment

Reduction proved more dangerous than randomness.

| Control type | Effect on confidence |
|--------------|---------------------|
| Random (EXP-010) | Increased confidence in pressure mechanisms |
| Reduction (EXP-011) | Decreased confidence in questions as primitive; increased confidence in difference detection |

Simplicity successfully attacked several assumptions and increased confidence in only those mechanisms that survived:

**Survived reduction:**
- Behavior-difference-based partitioning (World D)
- Full ecosystem path still works (World A) — sufficient but heavyweight

**Failed reduction (shown unnecessary for Bird partition):**
- Questions alone (World B)
- Observations alone (World C)
- Communities, pressure, tolerance (absent in World D yet Bird partitions)

**Not yet tested:**
- Whether World D's groups are "the same" as World A's semantically (naming differs: fly/not_fly vs Conforming/Contradicting)
- Whether difference dynamics alone support attention, merge, genealogy, and other EXP-001–008 phenomena
- Whether questions can emerge from differences rather than precede them

Introducing minimal worlds shifted the research program from falsification (EXP-010) toward **necessity analysis**. The project should continue simplifying until organization fails, then rebuild upward from the smallest surviving primitive — likely difference management (H97, H100).

EXP-011 does not invalidate prior experiments. It recontextualizes them: questions, communities, and pressure may be layers built on a deeper difference-detection substrate, not the substrate itself.

That reframing is the primary scientific advance — and the primary threat — of EXP-011.
