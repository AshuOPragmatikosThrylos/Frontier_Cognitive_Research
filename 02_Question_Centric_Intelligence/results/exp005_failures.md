# EXP-005 Failures

Post-experiment failure analysis for attention economy.

Date: 2026-06-21  
Experiment: EXP-005 Attention Economy

---

## Failure Analysis

No catastrophic failure was observed. The attention economy functioned as implemented: budget enforced, dormancy preserved questions, revival observations updated debt, reallocation ran deterministically.

However, a **potential ambiguity** was discovered that may be more interesting than a bug.

---

## Potential Ambiguity Discovered

### A revived question does not necessarily become ACTIVE

**Example: Whale**

1. q-whale was DORMANT after initial allocation (fitness 1.0, ranked below top 4)
2. Whale re-observation triggered revival path:
   - `was_dormant = True`
   - Debt increased: 1.0 → 3.0
   - q-whale appended to REVIVED list
3. Reallocation ran. Top 4 by fitness:
   - q-species-capabilities (18.0)
   - q-bird-flightlessness (8.0)
   - q-mammal-capabilities (4.0)
   - q-penguin (3.0) — wins tie-break over q-whale (3.0) on id ordering
4. **q-whale remained DORMANT** despite being listed as revived

Whale accumulated debt and was listed as revived, but remained DORMANT.

---

## Possible Interpretations of "Revival"

The experiment conflates three distinct concepts:

| Concept | Whale outcome |
|---------|---------------|
| **Receiving observations** | Yes — second Whale anomaly processed |
| **Increasing debt** | Yes — 1.0 → 3.0 |
| **Becoming ACTIVE** | No — still DORMANT after allocation |

Current code defines revival as:

```python
if was_dormant:
    REVIVED.append(question_id)
```

Revival means **"a dormant question received a repeat observation"** — not **"a dormant question earned an ACTIVE slot"**.

CuriosityEngine briefly sets ACTIVE during `observe()`, but `allocate_attention()` immediately overwrites state based on fitness ranking.

---

## Penguin Contrast

Penguin revival succeeded on all three interpretations:

- Observation received ✓
- Debt increased (1.0 → 3.0) ✓
- Became ACTIVE ✓ (displaced q-bat)

The difference is competitive rank, not mechanism. Same revival code path, different allocation outcome.

---

## Potential Future Risk

**Memory, attention, and importance may be mixed together.**

Current model uses:

| Variable | Intended role | Actual role in code |
|----------|---------------|---------------------|
| curiosity_debt | Memory of unresolved anomalies | Ranks for attention |
| importance | Priority weight | Ranks for attention |
| state (ACTIVE/DORMANT) | Attention allocation | Overwritten each round |
| REVIVED list | Unclear | Observation receipt, not ACTIVE grant |

Without separation:

- High debt may not earn attention (Whale)
- High importance on community questions may starve entities permanently
- Revival may be reported without ecological effect (Whale)
- Observers may misread REVIVED as ACTIVE

---

## Need to Distinguish

Future architecture should clarify five distinct concepts:

### Memory

Persistent record of anomalies and encounters.  
Implemented as: `curiosity_debt`, `times_encountered`, `related_observations`.  
Whale memory increased correctly on revival.

### Attention

Finite resource allocated to investigation.  
Implemented as: ACTIVE state within ATTENTION_BUDGET.  
Whale did not receive attention despite memory update.

### Importance

Relative priority weighting.  
Implemented as: `importance` field in fitness formula.  
Community questions benefit from manually higher importance.

### Dormancy

Set-aside state without deletion.  
Implemented as: `state = "DORMANT"`.  
Whale correctly remained dormant when outranked.

### Activation

Earning an ACTIVE slot through competition.  
Implemented as: top-N fitness ranking.  
Whale failed activation despite revival list inclusion.

---

## Is This a Bug?

**Probably not a implementation bug.** The code behaves consistently:

1. Observe updates memory
2. Revival list records observation-on-dormant event
3. Allocation assigns ACTIVE independently

The ambiguity is **conceptual** — the experiment name and REVIVED label suggest activation, but the mechanism delivers memory update + reallocation only.

---

## Overall Assessment

This ambiguity is interesting and may reveal deeper structure rather than being a bug.

EXP-005 accidentally demonstrated that:

- Questions can **remember** without **attending**
- Revival can **occur** without **succeeding**
- Scarcity creates **competition** among revived questions, not guaranteed re-entry

This supports new hypotheses H51 (memory ≠ attention) and H52 (importance ≠ attention) and motivates explicit subsystem separation in future experiments.

---

## Recommendations (Documentation Only)

No code changes requested. For future experiments, consider:

1. Rename REVIVED → REOBSERVED or split into `reobserved` and `reactivated` lists
2. Report revival success rate (reactivated / reobserved)
3. Separate memory update phase from attention allocation phase in logs
4. Test whether minimum attention guarantees preserve entity diversity under budget scarcity

---

## Conclusion

EXP-005 did not fail mechanically. It revealed that revival, memory, and activation are conflated in the current design. The Whale case is the central finding of the failure analysis — not an error to fix silently, but a structural insight to investigate further.

Dormancy preserves optionality (H53). Whether that optionality converts to attention depends on competition — a lesson the Whale case teaches explicitly.
