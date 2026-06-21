# EXP-006 Failures

Post-experiment failure analysis for community competition.

Date: 2026-06-21  
Experiment: EXP-006 Community Competition

---

## Failure Analysis

EXP-006 did not fail mechanically. Community competition, allocation, and state propagation worked as designed. Eight of nine questions remained ACTIVE. Dominance shifted from Bird+Capability to Bird+Mammal as intended.

However, the experiment reveals **two complementary failure modes** at opposite extremes — connecting EXP-006 to the earlier EXP-003 failure and suggesting a balanced middle path.

---

## Failure Mode #1

Over-abstraction

Observed previously in EXP-003.

Hierarchy caused abstraction to dominate.

Specific questions lost activity.

### EXP-003 recap

Staged merges demoted entity and category questions to PARTIALLY_RESOLVED. Only the meta abstraction ("Why do species gain or lose capabilities?") remained ACTIVE. Attention collapsed upward. Diversity collapsed downward.

**Failure shape:** Abstraction consumes everything.

---

## Failure Mode #2

Over-specialization

Observed in EXP-006.

Specific communities dominated.

Bridge abstractions became DORMANT.

### EXP-006 observation

Bird and Mammal communities — driven by entity-level observation debt — claimed both ACTIVE slots. The Capability bridge community ("Why do species gain or lose capabilities?") went DORMANT and stayed DORMANT after mammal wave 1.

**Failure shape:** Specialization excludes integration.

---

## Description

Both extremes appear unhealthy.

| Extreme | Experiment | Symptom | What is lost |
|---------|------------|---------|--------------|
| Over-abstraction | EXP-003 | One ACTIVE apex | Entity diversity |
| Over-specialization | EXP-006 | Bridge DORMANT | Cross-domain integration |

Pure abstraction destroys diversity — specific questions lose activity, attention collapses to a single meta-level.

Pure specialization destroys integration — bridge communities cannot compete for attention, cross-domain links go dormant.

Healthy cognition may require **both** specific entity questions **and** bridge abstractions **simultaneously active** — a balance EXP-006 approximates (8/9 ACTIVE) but does not fully achieve (Capability dormant).

---

## The Capability Bridge Problem

EXP-004 established Capability as a connector via `cooperates_with` and `depends_on` edges. EXP-006 shows that **connectivity ≠ fitness**:

- Capability had graph links to both domains
- Capability had no observation feed to increase debt
- Static debt (2.0) could not compete with observation-driven domains (14.0, 13.0)

Bridge communities are structurally necessary (H61) but **ecologically vulnerable** under community competition without protection.

---

## What EXP-006 Did Right

Compared to EXP-003:

- No mass demotion of entity questions
- 8 of 9 questions ACTIVE
- Dominance shifted without deletion
- Community coherence preserved (all Bird members share state)

Community-level allocation (vs question-level in EXP-005) prevents intra-community starvation. Competition does not necessarily destroy diversity (H58 confirmed).

---

## Potential Future Solutions

### Mechanisms that maintain bridges

- Reserved attention slot for bridge communities
- Minimum fitness floor for cross-domain clusters
- Observation routing that feeds capability questions from domain anomalies

### Mechanisms that balance abstraction and specificity

- Dual budget: one slot for domain communities, one for bridge
- Fitness formula weighting connectivity (cooperates_with count)
- H62/H63: target middle ground between tree and flat graph

### Dynamic attention systems

- Rotating bridge priority across rounds
- Cycles that periodically activate DORMANT bridges (H54 from EXP-005)

### Community cooperation

- cooperates_with edges boost neighbor fitness (H19)
- Symbiotic uplift prevents bridge exclusion when domains thrive

---

## Overall Assessment

Healthy cognition may require balancing abstraction and specialization.

EXP-003 failed by over-abstracting. EXP-006 reveals the mirror risk: domain-specific communities may starve integration layers. Neither pure hierarchy nor pure domain competition suffices.

The experiment series suggests intelligence may live in H62's middle: graphs with active bridges **and** active specialists, protected by mechanisms that prevent either extreme from monopolizing attention.

EXP-006 is not a failure — it is a **diagnostic**. It maps the over-specialization boundary complementing EXP-003's over-abstraction boundary.

---

## Severity

| Dimension | Assessment |
|-----------|------------|
| Mechanical failure | None |
| Ecological failure | Partial — bridge dormant, integration at risk |
| Diversity | High — 8/9 ACTIVE |
| Hypothesis impact | Supports H55, H56, H58, H59–H63 |
| Urgency | Medium — bridge protection before scaling |

---

## Conclusion

EXP-006 exposes over-specialization as the dual failure mode to EXP-003's over-abstraction. Capability's dormancy is the central finding: bridge communities need explicit protection under community competition. Two extremes, one lesson — intelligence requires balance between abstraction and specialization.
