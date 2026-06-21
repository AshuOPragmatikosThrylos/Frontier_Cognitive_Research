# EXP-006 Code Analysis

Post-experiment read-only analysis of community competition.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-006)

---

## Files Involved

| File | Role in EXP-006 |
|------|-----------------|
| `experiments/exp006_community_competition.py` | Experiment driver; community-level attention logic |
| `src/curiosity_engine.py` | Entity question creation; debt on re-observation |
| `src/world_model.py` | Category → behavior rules |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

All community competition logic lives in the experiment file. No `src/` modules modified.

---

## Execution Flow

### Phase 0: Setup

Three community questions added before observations:

| ID | Debt | Importance |
|----|------|------------|
| q-bird-flightlessness | 2.0 | 1.5 |
| q-mammal-capabilities | 1.0 | 1.5 |
| q-species-capabilities | 2.0 | 1.5 |

### Phase 1: Bird Wave 1

Four bird anomalies → four entity questions (debt 1.0 each).

`allocate_community_attention("after bird wave 1")`

### Phase 2: Bird Wave 2

Repeat four bird observations → entity debt increases (triangular accumulation per CuriosityEngine).

`allocate_community_attention("after bird wave 2")`

### Phase 3: Mammal Wave 1

Bat and Whale anomalies → two mammal entity questions.

`allocate_community_attention("after mammal wave 1")`

### Phase 4: Mammal Wave 2

Four mammal observations (Bat, Whale, Bat, Whale) → rapid mammal debt growth.

`allocate_community_attention("after mammal wave 2")`

### Phase 5: Reporting

Prints allocation history, debt history, community states, question states, statistics.

---

## Community Attention Allocation Mechanism

```python
COMMUNITY_ATTENTION_BUDGET = 2

ranked = sorted(COMMUNITIES.keys(), key=lambda name: (-community_fitness(...), name))
active_communities = top 2
```

- **Unit of competition:** community, not individual question
- **Budget:** 2 of 3 communities ACTIVE
- **Tie-break:** alphabetical community name
- **Propagation:** all member questions inherit community state

Contrast with EXP-005: question-level top-4 allocation could split a community (some members ACTIVE, some DORMANT). EXP-006 keeps communities coherent — all Bird questions ACTIVE or all DORMANT together.

---

## Community Debt Accumulation

```python
community_debt = sum(member.curiosity_debt for member in community)
```

Logged after each allocation in `COMMUNITY_DEBT_LOG`.

### Trajectory (approximate)

| Phase | Bird | Mammal | Capability |
|-------|------|--------|------------|
| After bird wave 1 | 6.0 | 1.0 | 2.0 |
| After bird wave 2 | 14.0 | 1.0 | 2.0 |
| After mammal wave 1 | 14.0 | 3.0 | 2.0 |
| After mammal wave 2 | 14.0 | 13.0 | 2.0 |

Bird debt grows early via four entities × two waves. Mammal debt stagnant until mammal waves, then accelerates via repeated Bat/Whale observations. Capability debt static — no observations target it directly.

---

## Community Fitness Calculations

```python
community_fitness = sum(member.curiosity_debt * member.importance for member in community)
```

| Phase | Bird | Mammal | Capability | Top 2 |
|-------|------|--------|------------|-------|
| Bird wave 1 | 7.0 | 1.5 | 3.0 | Bird, Capability |
| Bird wave 2 | 15.0 | 1.5 | 3.0 | Bird, Capability |
| Mammal wave 1 | 15.0 | 3.5 | 3.0 | Bird, Mammal |
| Mammal wave 2 | 15.0 | 13.5 | 3.0 | Bird, Mammal |

Fitness diverges because observation-driven entity debt dominates static community question debt.

---

## Community States

Stored in `COMMUNITY_STATES` dict, updated each allocation:

| Community | Final State |
|-----------|-------------|
| Bird | ACTIVE |
| Mammal | ACTIVE |
| Capability | DORMANT |

Community states transition over time:

- Mammal: DORMANT → DORMANT → ACTIVE → ACTIVE
- Capability: ACTIVE → ACTIVE → DORMANT → DORMANT

---

## Question States

Inherited from community state — no independent question-level allocation.

| Final | Count |
|-------|-------|
| ACTIVE | 8 (all Bird + all Mammal members) |
| DORMANT | 1 (q-species-capabilities) |

Question states mirror community outcome exactly. This preserves intra-community diversity when community wins.

---

## Competition Dynamics

### Bird dominance (waves 1–2)

Four entity questions × debt accumulation → high community fitness. Mammal has only static `q-mammal-capabilities` (debt 1.0) — cannot compete.

### Capability interim slot (waves 1–2)

Capability fitness (3.0) exceeds Mammal (1.5) — earns second ACTIVE slot as "best of the rest" despite no new observations.

### Mammal rise (waves 3–4)

Entity observations for Bat and Whale add debt. Mammal fitness surpasses Capability (3.5 > 3.0 after wave 1; 13.5 > 3.0 after wave 2).

### Capability exclusion (waves 3–4)

Bridge community has single member with fixed debt. No observation path increases Capability fitness. Permanently outranked once both domain communities accumulate entity debt.

---

## Presence or Absence of Randomness

| Source | Present? | Affects behavior? |
|--------|----------|-------------------|
| `random` | No | — |
| `uuid` | No | — |
| Deterministic ids | Yes | `q-{entity}` |
| Tie-break | Yes | Alphabetical community name |
| Fixed wave order | Yes | Bird before mammal |

**Fully deterministic.**

---

## Heuristics Involved

| Heuristic | Rule |
|-----------|------|
| Community budget | 2 of 3 ACTIVE |
| Fitness formula | Sum of member debt × importance |
| Tie-break | Alphabetical community name |
| State propagation | All members inherit community state |
| Observation waves | Bird × 2, then Mammal × 2 (escalating repeats) |
| Capability debt | Static — no observation feed |

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed budget, formula, waves, and tie-breaks. Reproducible dominance shifts.

**D — Emergent from interactions between simple rules** (partial)

Capability's rise and fall emerges from relative fitness without explicit rules naming winners — but wave ordering encodes bird-first dominance.

### Key findings

| Property | Finding |
|----------|---------|
| Community-level allocation | Preserves intra-community diversity |
| Dominance shifts | Bird → Bird+Mammal over time |
| Bridge vulnerability | Capability loses when domains accumulate debt |
| vs EXP-005 | Community unit prevents splitting members |
| vs EXP-003 | No hierarchy collapse; diversity preserved |
| Abstraction cost | Static bridge cannot compete with observation-driven domains |

### Conclusion

EXP-006 code implements community-level attention competition with shifting dominance and high question diversity. The architecture improves on EXP-005's individual starvation and EXP-003's hierarchy collapse, while exposing bridge community vulnerability under observation-driven fitness — motivating H59–H63 and protection mechanisms in future work.
