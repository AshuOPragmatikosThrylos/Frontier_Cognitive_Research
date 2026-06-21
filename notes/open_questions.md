# Open Questions

Research-facing unknowns as of EXP-018. Not implementation tasks.

---

## Most Important Unresolved Questions

1. **What is the primitive operation?** Difference detection (EXP-011 D) vs tension management vs question competition — which is necessary and sufficient for *useful* cognition beyond Bird partitioning?

2. **Can difference-first scale?** Three categories (Bird/Mammal/Insect) share the same behavior-diff template. Does the stack generalize to structurally different observation types?

3. **What is the right unit of memory?** Traces (EXP-015), competition winners (EXP-017), or groups/tensions (EXP-013)? Layered or competing?

4. **What are coalition prerequisites?** EXP-018 falsified simple cooperation — what trace density, affinity rules, and budget structures are needed for cooperation to matter?

5. **Is any of this computationally advantageous?** No comparison to baseline agents, RL, or standard memory architectures.

---

## Most Dangerous Assumptions

| Assumption | Risk |
|------------|------|
| Bird/Mammal/Insect template represents general cognition | Overfitting narrative to behavior-diff scenarios |
| Every memory extension adds new behavior | EXP-018 showed otherwise — stacking may redundant |
| Hand-tuned thresholds (budget=1, strength/4) are meaningful | Constants may drive outcomes |
| Cooperation will emerge from more rules | May need qualitatively different architecture |
| Negative results generalize | EXP-018 may be artifact of weak coalition rule, not impossibility of cooperation |

---

## Most Promising Directions

1. **Coalition prerequisites study** — larger trace populations, adaptive cooperation, separate budget pools.
2. **Second domain** with structurally different observations — not just more behavior-diff categories.
3. **Threshold sensitivity audit** — ±20% on budget, strength divisor, coalition threshold.
4. **Adaptive reconstruction budgets** — suggested by EXP-017/018 future directions.
5. **Bridge to 03_Compression_Failure_Engine** — unify compression failure with difference-first stack.

---

## Questions That Could Destroy the Theory

1. **Does World D + memory + competition reproduce all interesting behavior without questions?** If yes, question layer may be decorative.

2. **Does a simpler single-mechanism model match all EXP-001–018 outcomes?** Ecology adds no explanatory power.

3. **Do results change materially with threshold perturbation?** EXP-017/018 conclusions may be artifact.

4. **Does external replication fail?** Independent implementer gets different arc.

5. **Does every new EXP-018-style extension fail?** Would suggest diminishing returns on memory layer.

---

## Questions That Could Strengthen the Theory

1. **New domain** shows difference → tension → trace → competition cycle without retuning.

2. **Richer cooperation succeeds** where EXP-018 failed — defines prerequisites precisely.

3. **EXP-018-style negative results continue** — program demonstrates ongoing falsifiability.

4. **Mapping to cognitive science** — selection ≈ retrieval competition; traces ≈ semantic memory.

5. **Minimal formal proof** that budget + strength ranking produces selection without cooperation.

---

## Resolved or Partially Resolved (since last update)

- **Forgetting vs loss (EXP-016/017):** Distinct — forgetting removes/weaken traces; competition loss retains traces without expression.
- **Cooperation with simple rules (EXP-018):** **Not supported** — requires richer mechanisms (H155).
- **Selection robustness (EXP-017/018):** EXP-018 failed to overturn EXP-017 — selection confirmed.

---

## Carried Forward from Early Notes

- Can a system defined by unresolved questions outperform one defined by answers? (Q1 — still open)
- Can compression failures lead to scientific discovery? (Q5 — analogically supported, not demonstrated)
