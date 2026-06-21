# EXP-005 Results

Post-experiment summary for attention economy.

Date: 2026-06-21  
Experiment: EXP-005 Attention Economy

---

## Theme

Attention Economy

Test whether finite attention budget creates dynamic question ecosystems — with competition, dormancy, and revival — without deleting unresolved questions.

---

## Experiment Summary

Introduced scarcity through a limited attention budget (`ATTENTION_BUDGET = 4`).

Nine questions competed for four ACTIVE slots. Questions ranked by `curiosity_debt × importance`; top four received ACTIVE status, remainder became DORMANT.

### Phases

1. **Initial observations** — six entity questions from anomalies
2. **Community setup** — three category/capability questions added (from EXP-004 structure)
3. **Initial allocation** — first competition for attention
4. **Revival observations** — Penguin and Whale re-encountered while DORMANT
5. **Re-allocation** — attention redistributed after each revival

### Key Outcomes

- Questions competed for attention
- Some questions became **DORMANT** (5 of 9 after initial allocation)
- Dormant questions were **preserved** in repository — not deleted
- New observations caused dormant questions to **revive** (debt increase + reallocation)
- Question ecosystems became **dynamic** — ACTIVE/DORMANT membership changed across rounds

### Initial Allocation (top 4)

| Rank | Question | Fitness |
|------|----------|---------|
| 1 | q-species-capabilities | 18.0 |
| 2 | q-bird-flightlessness | 8.0 |
| 3 | q-mammal-capabilities | 4.0 |
| 4 | q-bat | 1.0 |

**DORMANT:** q-penguin, q-ostrich, q-emu, q-kiwi, q-whale

### After Penguin Revival

Penguin debt rose to 3.0. Displaced q-bat from ACTIVE slot.

**ACTIVE:** q-species-capabilities, q-bird-flightlessness, q-mammal-capabilities, **q-penguin**

### After Whale Revival

Whale debt rose to 3.0. Listed as revived but remained DORMANT — fitness tied with Penguin at 3.0 but lost tie-break (id ordering).

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H46** — Intelligence emerges from scarcity | Attention budget forced competition; not all questions could be ACTIVE |
| **H47** — Dormancy is necessary | Five questions went DORMANT without deletion when budget exceeded |
| **H49** — Dormant questions can resurrect | Penguin and Whale received revival observations; Penguin re-entered ACTIVE |

---

## Unexpected Observations

1. **Questions transitioned between ACTIVE and DORMANT.** q-bat was ACTIVE initially, DORMANT after Penguin revival.

2. **Attention shifted from Bat to Penguin.** Same budget, different winners after debt change — dynamic reallocation without new questions.

3. **Communities accumulated different amounts of debt.** Bird community debt exceeded Mammal after revivals (Penguin debt increase).

4. **Dormant entities retained significance.** DORMANT questions kept identity, debt, and observations — ready for future revival.

---

## Surprising Observations

1. **Memory, attention, and importance appeared to behave differently.** Curiosity debt (memory of anomalies) increased on revival, but ACTIVE status depends separately on budget competition weighted by importance.

2. **Dormancy behaved differently from death.** DORMANT questions persist fully; ABANDONED/DEAD states were never used.

3. **Question ecosystems exhibited cycles rather than permanence.** ACTIVE membership is round-dependent, not fixed — contrast with EXP-004 (all permanently ACTIVE) and EXP-003 (most permanently PARTIALLY_RESOLVED).

4. **Revival ≠ ACTIVE.** Whale was revived (observation received, debt increased) but remained DORMANT — see `exp005_failures.md`.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H51** | Memory and attention are distinct |
| **H52** | Importance and attention are distinct |
| **H53** | Dormancy preserves future optionality |
| **H54** | Intelligence requires cycles rather than permanence |

H51–H52 arise from the Whale case: debt (memory signal) increased without earning attention (ACTIVE slot). H53 from preserved DORMANT questions. H54 from observed ACTIVE/DORMANT cycling.

---

## Future Directions

- Study attention dynamics across multiple revival rounds
- Study long-term memory (curiosity debt persistence and accumulation)
- Study question importance (weighting in allocation formula)
- Study cyclic ecosystem behavior (ACTIVE ↔ DORMANT oscillation)

---

## Conclusion

EXP-005 introduces scarcity into the question-centric model. Attention budget creates competition, dormancy preserves optionality, and revival observations perturb allocation. The experiment moves beyond static graph communities (EXP-004) toward dynamic ecology — with an important ambiguity between revival, debt, and ACTIVE status that warrants further investigation.

---

## Comparison Across Experiments

| Property | EXP-003 | EXP-004 | EXP-005 |
|----------|---------|---------|---------|
| Scarcity | Implicit (merge) | None | Explicit budget |
| DORMANT | No | No | Yes |
| Dynamic states | One-way demotion | Static ACTIVE | Cyclic ACTIVE/DORMANT |
| Revival | Not tested | Not tested | Yes |
| Failure mode | Over-abstraction | None | Ambiguity (revival vs ACTIVE) |
