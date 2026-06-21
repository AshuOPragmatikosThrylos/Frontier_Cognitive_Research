# EXP-006 Results

Post-experiment summary for community competition.

Date: 2026-06-21  
Experiment: EXP-006 Community Competition

---

## Theme

Community Competition

Test whether communities — not individual questions — compete for a limited attention budget, and whether dominance shifts as observations accumulate over time.

---

## Experiment Summary

Communities competed for a limited attention budget (`COMMUNITY_ATTENTION_BUDGET = 2`).

Three communities (Bird, Mammal, Capability) vied for two ACTIVE slots. Community fitness = sum of member `curiosity_debt × importance`. All questions within a community inherit the community's state.

### Observation Waves

| Phase | Observations | Effect |
|-------|--------------|--------|
| Bird wave 1 | Penguin, Ostrich, Emu, Kiwi | Bird community debt rises |
| Bird wave 2 | Repeat all four birds | Bird debt doubles on entities |
| Mammal wave 1 | Bat, Whale | Mammal community enters |
| Mammal wave 2 | Bat, Whale × 2 repeats | Mammal debt surges |

### Community Attention Over Time

| Phase | ACTIVE Communities | DORMANT |
|-------|-------------------|---------|
| After bird wave 1 | Bird, Capability | Mammal |
| After bird wave 2 | Bird, Capability | Mammal |
| After mammal wave 1 | Bird, Mammal | Capability |
| After mammal wave 2 | Bird, Mammal | Capability |

### Key Outcomes

- **Bird community initially dominated** — highest fitness after both bird waves
- **Mammal community accumulated debt and later became competitive** — displaced Capability after mammal wave 1
- **Capability community lost attention and became DORMANT** — bridge abstraction could not sustain fitness against observation-driven communities
- **Question diversity remained high** — eight entity and category questions preserved
- **Most questions remained ACTIVE** — 8 of 9 questions ACTIVE at final state; only Capability community dormant

### Final Community Debt (approximate)

| Community | Debt | Fitness |
|-----------|------|---------|
| Bird | 14.0 | 15.0 |
| Mammal | 13.0 | 13.5 |
| Capability | 2.0 | 3.0 |

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H55** — Communities compete for attention | Budget of 2 forced one community DORMANT each round |
| **H56** — Community dominance emerges | Bird dominated early; Mammal rose later; Capability fell |
| **H58** — Competition does not necessarily destroy diversity | 8 of 9 questions remained ACTIVE; no questions deleted |

---

## Unexpected Observations

1. **Competition did not eliminate question diversity.** Unlike EXP-003 hierarchy collapse, community-level competition preserved most questions as ACTIVE.

2. **The most abstract community became DORMANT.** Capability — the cross-domain bridge — lost both attention slots once Bird and Mammal accumulated observation debt.

3. **Specific communities remained ACTIVE.** Bird and Mammal, driven by entity-level anomalies, outcompeted the abstract Capability cluster.

4. **Community fitness diverged significantly.** Final spread: Bird 15.0 vs Capability 3.0 — a 5× gap.

---

## Surprising Observations

1. **Capability community acted as a bridge but lost attention.** In EXP-004 it connected Bird and Mammal; in EXP-006 it could not compete for scarce community slots.

2. **Connectivity did not imply fitness.** Graph links (from EXP-004) did not translate to attention wins under community competition.

3. **Abstraction proved fragile.** The highest-level question ("Why do species gain or lose capabilities?") went DORMANT while specific entity questions stayed ACTIVE.

4. **ACTIVE questions remained high.** Community-level allocation keeps all members ACTIVE when community wins — contrasting EXP-005 question-level starvation.

5. **Competition favored specific communities over abstract communities.** Observation-driven debt favored domains with many anomalies over single bridge nodes.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H59** | Abstractions are expensive |
| **H60** | Specificity stabilizes cognition |
| **H61** | Bridge communities are vulnerable |
| **H62** | Intelligence exists between pure abstraction and pure specialization |
| **H63** | Healthy cognition requires balancing abstraction and specialization |

H59–H61 explain Capability's dormancy. H62–H63 frame the dual failure modes seen in EXP-003 (over-abstraction) and EXP-006 (bridge loss under specialization pressure).

---

## Future Directions

- Study mechanisms that protect bridge communities
- Study balance between abstraction and specialization
- Study long-term cycles of community dominance
- Study ecosystem resilience

---

## Comparison Across Experiments

| Property | EXP-003 | EXP-004 | EXP-005 | EXP-006 |
|----------|---------|---------|---------|---------|
| Competition unit | Merge hierarchy | None | Individual questions | Communities |
| Bridge/capability | Apex (ACTIVE) | Bridge (ACTIVE) | Competes individually | DORMANT |
| Diversity | Collapsed | Full | Partial (DORMANT) | High (8/9 ACTIVE) |
| Dominance shift | No | No | Yes (Bat→Penguin) | Yes (Capability→Mammal) |

---

## Conclusion

EXP-006 demonstrates that community-level competition produces shifting dominance without destroying question diversity. Bird observations initially control attention; mammal observations later make Mammal competitive; the abstract Capability bridge loses. Community competition is a healthier ecology than hierarchical merge, but bridge abstractions need protection under scarcity — abstraction pays a price under observation-driven fitness.
