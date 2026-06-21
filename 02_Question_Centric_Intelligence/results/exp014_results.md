# EXP-014 Results

Post-experiment summary for question resurrection.

Date: 2026-06-22  
Experiment: EXP-014 Question Resurrection

---

## Theme

Question Resurrection

Test whether extinct questions are recreated as new objects or resurrected with preserved identity and history when tension re-emerges after extinction.

---

## Experiment Summary

Started from the EXP-013 pipeline extended with a revival phase:

```
observations → differences → tensions → emergent questions → lifecycle → extinction → resurrection
```

### Phase 1: Emergence through extinction (EXP-013)

Standard 10 observations. Bird question `eq-bird-fly-vs-not_fly` emerged, traversed EMERGENT → ACTIVE → RESOLVED → DORMANT → **EXTINCT** (vitality 4.0 → 0.0). Tension `t-bird-fly-vs-not_fly` marked resolved.

| Step | State | Vitality |
|------|-------|----------|
| Emerge | EMERGENT | 4.0 |
| Promote | ACTIVE | 4.0 |
| Resolve | RESOLVED | 2.0 |
| Decay 1 | DORMANT | 1.0 |
| Decay 2 | EXTINCT | 0.0 |

### Phase 2: Revival observations

Four new Bird observations ingested after extinction:

| Entity | Behavior |
|--------|----------|
| Crow | fly |
| Raven | fly |
| Chicken | not fly |
| Turkey | not fly |

Difference groups refreshed: `Bird.fly` (6 members), `Bird.not_fly` (6 members). Tension reopened — strength 6.0, `resolved=False`.

### Phase 3: Resurrection (not recreation)

System checked for EXTINCT question linked to reopened tension. Found `eq-bird-fly-vs-not_fly`.

The extinct Bird question was **not recreated**.

Instead, the same question regained vitality (`RESURRECTION_VITALITY = 3.0`) and entered **RESURRECTED** state, then promoted to **ACTIVE**.

Identity and history were preserved — no new question object created.

| Property | Before revival | After revival |
|----------|----------------|---------------|
| Question ID | `eq-bird-fly-vs-not_fly` | `eq-bird-fly-vs-not_fly` (unchanged) |
| Question count | 1 | 1 |
| State | EXTINCT | ACTIVE |
| Vitality | 0.0 | 3.0 |
| History entries | 5 | 7 |

Resurrection event recorded:

> resurrection: eq-bird-fly-vs-not_fly (identity preserved, history entries=5 → 7)

The experiment demonstrated: **observations → differences → tensions → questions → lifecycle → extinction → resurrection**

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H117** | Extinct questions can resurrect | Bird question EXTINCT → RESURRECTED → ACTIVE after tension reopening |
| **H118** | Memory preserves question identity | Same `eq-bird-fly-vs-not_fly` id retained; no `-recreated` suffix object |
| **H119** | Death and memory coexist | EXTINCT state coexisted with intact `lifecycle_history`; history appended after revival |
| **H120** | Resurrection is cheaper than recreation | Single object reactivated; recreation path (`recreate_question()`) not invoked |

H120: Resurrection reuses existing record — no new emergence, no duplicate tension-question mapping.

---

## Unexpected Observations

1. **No new question object was created.** `try_resurrect_or_recreate()` selected resurrection branch when EXTINCT question matched tension id.

2. **Question count remained one.** Total questions = 1 before and after revival; recreation would have produced count = 2.

3. **History accumulated across lifetimes.** Five pre-extinction entries plus two resurrection entries — continuous narrative across death.

4. **Extinction proved reversible.** EXTINCT is not terminal when tension re-emerges and extinct question record persists.

---

## Surprising Observations

1. **Identity survived extinction.** Question id unchanged despite vitality reaching zero — extinction is a state, not deletion (H121, H122).

2. **The question behaved more like a recurring organism than a disposable object.** Same individual returned rather than offspring replacing parent.

3. **History entries increased after resurrection.** Experience from first lifetime retained and extended — not reset (H123, H124).

4. **Questions appeared cyclical rather than linear.** Trajectory EMERGENT → … → EXTINCT → RESURRECTED → ACTIVE suggests loop structure, not one-way arrow.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H121** | Identity is independent of activity |
| **H122** | Extinction and absence are not identical |
| **H123** | Memory accumulates across cycles |
| **H124** | Experience survives extinction |

H121: Question id persists while state cycles through inactive (EXTINCT) and active (ACTIVE).

H122: EXTINCT question still exists in `lifecycle_questions` dict — absent from activity but present in memory.

H124: Prior lifecycle entries readable after resurrection — first-life experience accessible in second life.

---

## Future Directions

- Investigate repeated resurrection cycles (second extinction → second resurrection)
- Study memory persistence across multiple birth-death-rebirth loops
- Study question inheritance (can resurrected questions pass history to derived questions?)
- Investigate whether communities can resurrect (parallel to question resurrection)
- Investigate ecosystem memory (aggregate history across all resurrected questions)

---

## Comparison: EXP-013 vs EXP-014

| Property | EXP-013 end state | EXP-014 end state |
|----------|-------------------|-------------------|
| Bird question state | EXTINCT | ACTIVE (resurrected) |
| Question count | 1 | 1 |
| Tension | Resolved | Reopened (unresolved) |
| History | 5 entries, frozen | 7 entries, continuing |
| Revival | Not modeled | Resurrection |

EXP-014 answers EXP-013 future direction ("Investigate question resurrection") with identity-preserving resurrection rather than recreation.

---

## Resurrection vs Recreation

| Outcome | Condition | Result |
|---------|-----------|--------|
| **Resurrection** | EXTINCT question exists for tension | Same id, history preserved, RESURRECTED → ACTIVE |
| **Recreation** | No extinct question for tension | New `-recreated` id, fresh history |

Bird case: **resurrection** — supports H117–H120.

---

## Conclusion

EXP-014 demonstrates that extinct questions can return with preserved identity and accumulated history when tension re-emerges. The Bird question completed a full cycle including death and rebirth within a single record. Resurrection is distinct from recreation: cheaper (H120), memory-preserving (H118), and cyclical rather than linear.

Questions behave as recurring episodic structures (H113–H114 from EXP-013) with persistent identity (H121) — strengthening ecological and organism-like interpretations of question dynamics.

Resurrection rules remain externally programmed (see `exp014_failures.md`).
