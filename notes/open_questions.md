# Open Questions

Research-facing unknowns as of EXP-016 implementation. Not implementation tasks.

---

## Most Important Unresolved Questions

1. **What is the primitive operation?** Difference detection (EXP-011 D) vs tension management vs question competition — which is necessary and sufficient for *useful* cognition beyond Bird partitioning?

2. **Can difference-first scale?** Single toy domain (Bird/Mammal behaviors). Does the stack generalize to other observation structures without hand-tuned thresholds?

3. **What is the right unit of memory?** Traces (EXP-015), resurrected objects (EXP-014), dormant questions (EXP-005), or groups/tensions (EXP-013)? Are these competing or layered?

4. **Does forgetting help or harm identity?** EXP-016 design predicts core trace survives, clutter prunes — unverified in results corpus.

5. **Is any of this computationally advantageous?** No comparison to baseline agents, RL, or standard memory architectures.

---

## Most Dangerous Assumptions

| Assumption | Risk |
|------------|------|
| Bird/Mammal world represents general cognition | Overfitting narrative to one scenario |
| Questions were the right starting primitive | EXP-011/012 may have already inverted this |
| Hand-tuned thresholds (2 members, 0.25 decay, budget 4) are meaningful | Constants may drive outcomes |
| Deterministic toy logic → insight about intelligence | Analogical leap without validation |
| Ecosystem metaphors map to real minds | Category error if taken literally |
| Merge/abstraction always helps | EXP-003 showed it can destroy diversity |

---

## Most Promising Directions

1. **Formalize the difference → tension → question pipeline** as a minimal grammar with explicit falsification tests.
2. **Second domain** (e.g. tools, social roles, numeric patterns) — same machinery, no Bird entities.
3. **Document EXP-016 results** and decide if H133+ need clutter/forgetting/identity split.
4. **Compare resurrection (EXP-014) vs reconstruction (EXP-015)** under forgetting — which identity model survives decay?
5. **Bridge to 03_Compression_Failure_Engine** — unify compression failure (H4/H7) with difference-first stack.

---

## Questions That Could Destroy the Theory

1. **Does World D + memory + forgetting reproduce all "interesting" behavior without questions ever being instantiated?** If yes, question-centric framing was a long detour.

2. **Does a simpler single-mechanism model match all EXP-001–016 outcomes?** If a one-line rule fits, ecology adds no explanatory power.

3. **Do results change materially with threshold perturbation?** If ±1 member or ±0.1 decay reverses conclusions, findings are artifact not structure.

4. **Can random worlds + enough constraints eventually match pressure worlds?** Would undermine H87/H92.

5. **Does external replication fail?** Independent implementer gets different qualitative arc.

---

## Questions That Could Strengthen the Theory

1. **New domain shows same difference → tension → episodic question → trace cycle** without retuning Bird constants.

2. **Forgetting improves reconstruction quality** (less clutter, same identity) — EXP-016 World B documents cleanly.

3. **Explicit prediction registered before experiment** and confirmed (pre-register style).

4. **Mapping to cognitive science** — e.g. tension ≈ schema violation, traces ≈ semantic memory, questions ≈ conscious interrogatives.

5. **Minimal formal proof** that organization requires persistence threshold, not question objects.

---

## Carried Forward from Early Notes

- Can a system defined by unresolved questions outperform one defined by answers? (Q1 — partially tested, answer still open)
- Can compression failures lead to scientific discovery? (Q5 — analogically supported, not demonstrated)
