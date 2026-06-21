# EXP-011 Results

Post-experiment summary for minimal worlds.

Date: 2026-06-22  
Experiment: EXP-011 Minimal Worlds

---

## Theme

Minimal Worlds

Test which mechanisms are necessary for organization and speciation-like phenomena by progressively stripping complexity from the full ecosystem model, feeding identical observations into each reduced world.

---

## Experiment Summary

Compared four worlds with decreasing complexity on identical observations (10 total: 4 bird conforming, 4 bird contradicting, 2 mammal contradicting).

| World | Mechanism | Questions | Communities | Split trigger |
|-------|-----------|-----------|-------------|---------------|
| **A (Ecosystem)** | Full EXP-009 logic: communities, adaptive tolerance, pressure | Yes | Yes | `pressure ≥ 1.0` |
| **B (No Communities)** | Flat questions via curiosity engine | Yes | No | None |
| **C (No Questions)** | Raw observation log | No | No | None |
| **D (Difference)** | Behavior grouping within category | No | No (BehaviorGroups) | ≥2 behaviors, ≥2 members each |

All worlds received identical observations.

### World A outcome

Bird accumulated four contradictions; pressure reached 1.1; semantic split into Bird.Conforming and Bird.Contradicting. Mammal absorbed two contradictions without splitting (pressure 0.0). Full ecosystem organization reproduced from EXP-009.

### World B outcome

Ten flat questions created (one per entity), all ACTIVE. Curiosity engine processed prediction failures. No community assignment, no hierarchy, no speciation events. Questions existed as an unstructured list.

### World C outcome

Ten observation strings logged (`entity (category): behavior`). No questions, no communities, no speciation. Raw data retained without cognitive structure.

### World D outcome

Behavior index built per category. Bird: four `fly` + four `not fly` → difference split into Bird.fly and Bird.not_fly. Mammal: one `fly` + one `swim` → below minimum per group (2) → no split. **Bird partitioning reproduced without questions, communities, pressure, or tolerance.**

### Summary findings

World B retained questions but produced no organization.

World C retained observations but produced no organization.

World D reproduced Bird partitioning despite containing no questions, communities, pressure, or tolerance.

The experiment attacked the necessity of previously introduced mechanisms.

### Final structure comparison

```
World A (Ecosystem)              World B (Flat)        World C (Raw)         World D (Difference)
├── Bird (organizational)        flat_questions ×10    observation_log ×10   ├── Bird.fly
│   ├── Bird.Conforming          (no hierarchy)        (no structure)        └── Bird.not_fly
│   └── Bird.Contradicting                                                     (Mammal: no split)
└── Mammal (stable)
```

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H94** | Interesting structure survives simplification | World D reproduced Bird partitioning with only behavior-difference detection |
| **H95** | Some mechanisms are unnecessary | Communities, pressure, tolerance, and questions not required for Bird partition in World D |

---

## Strengthened Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H96** | Differences may be more fundamental than questions | World D organized by behavior difference alone; World B's questions produced no hierarchy |

World B had questions but no organization. World D had no questions but produced semantic Bird groups. Difference detection outperformed question storage for structural outcomes.

---

## Unexpected Observations

1. **Questions alone produced no hierarchy or speciation.** World B created 10 questions with correct content but zero organizational events — questions are not sufficient for structure.

2. **Observations alone produced no cognitive structure.** World C preserved all input data as strings but generated no partitions, states, or groupings.

3. **Minimal difference grouping reproduced Bird partitioning.** World D split Bird into fly/not-fly groups using only `DIFFERENCE_MIN_PER_GROUP = 2` — no expectation, debt, or tolerance required.

4. **Communities and pressure proved sufficient but not necessary.** World A demonstrates sufficiency (full semantic speciation); World D demonstrates Bird partition without them.

---

## Surprising Observations

1. **The simplest world reproduced one of the most important phenomena.** Bird partitioning — the hallmark outcome of EXP-007 through EXP-009 — appeared in World D with the least machinery.

2. **Questions appeared descriptive rather than fundamental.** World B stores questions; World D produces organization without them. Questions may label differences rather than cause organization.

3. **Organization emerged without states, communities, or pressure.** World D uses entity lists grouped by behavior — no question states, no community objects, no pressure calculation.

4. **The project name itself became questionable.** "Question-Centric Intelligence" assumes questions are central; EXP-011 suggests difference management may be more primitive.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H97** | Difference alone can create organization |
| **H98** | Questions are compressed representations of differences |
| **H99** | Communities are higher-order organizations of differences |
| **H100** | Cognition may emerge from difference management rather than question management |

H98: World B's questions encode observed behaviors but do not partition; World D partitions on behavior directly — questions may be lossy or inert compressions.

H99: World A's communities (Conforming/Contradicting) mirror World D's behavior groups (fly/not_fly) with additional pressure/tolerance machinery layered on top.

H100: If World D organizes without questions, the primitive operation may be detecting and managing differences, with questions as a derived representation.

---

## Future Directions

- Investigate whether questions themselves can emerge from difference dynamics
- Investigate difference dynamics (accumulation, threshold, inheritance) as first-class mechanics
- Study minimal organizing principles — what lies below World D?
- Continue simplifying mechanisms until organization fails
- Search for the smallest world capable of cognition

---

## Comparison: EXP-010 vs EXP-011

| Property | EXP-010 | EXP-011 |
|----------|---------|---------|
| Control type | Random null world | Progressive reduction |
| Worlds compared | 2 | 4 |
| Attack vector | "Is mechanism needed vs randomness?" | "Which mechanism parts are needed?" |
| Key survivor | Pressure world organization | Difference-based grouping |
| Question role | Random increased diversity | Questions alone insufficient |

EXP-010 falsified random reproduction. EXP-011 falsified necessity of questions, communities, and pressure for Bird partitioning.

---

## Conclusion

EXP-011 demonstrates that progressive reduction can be more disruptive than random controls. Bird semantic partitioning survives in World D with only behavior-difference detection; questions and observations alone (Worlds B and C) produce no organization. Communities, pressure, and tolerance are sufficient (World A) but not necessary (World D) for this phenomenon.

The experiment shifts the research question from "how do questions evolve?" toward "what minimal difference-management produces organization, and do questions emerge from that?" Reduction successfully attacked several assumptions while increasing confidence in difference detection as a surviving primitive.
