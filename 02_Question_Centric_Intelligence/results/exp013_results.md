# EXP-013 Results

Post-experiment summary for question lifecycles and extinction.

Date: 2026-06-22  
Experiment: EXP-013 Question Extinction

---

## Theme

Question Lifecycles and Extinction

Test whether emergent questions (EXP-012) possess lifecycles, whether tension resolution reduces question vitality, and whether questions can go extinct while organizational memory persists.

---

## Experiment Summary

Started from the EXP-012 pipeline extended with lifecycle dynamics:

```
observations → differences → tensions → emergent questions → lifecycle
```

Questions possessed lifecycles with five states: EMERGENT, ACTIVE, RESOLVED, DORMANT, EXTINCT.

### Phase 1: Emergence (EXP-012 foundation)

Standard 10 observations ingested. Bird difference groups formed (`Bird.fly`, `Bird.not_fly`). Persistent tension `t-bird-fly-vs-not_fly` detected (strength 4.0). One question emerged:

| Property | Value |
|----------|-------|
| ID | `eq-bird-fly-vs-not_fly` |
| Text | *Why do Bird entities both fly and not fly?* |
| Initial vitality | 4.0 (= tension strength) |
| Initial state | EMERGENT |

Mammal: no groups, no tension, no question (same as EXP-012).

### Phase 2: Activation

Bird question promoted EMERGENT → **ACTIVE** while tension remained unresolved.

### Phase 3: Resolution

Tension `t-bird-fly-vs-not_fly` resolved:

> *niche specialization resolves bird behavior conflict*

Vitality reduced by 2.0 (4.0 → 2.0). Question entered **RESOLVED** state.

### Phase 4: Decay and extinction

Two vitality decay steps applied (1.0 reduction each):

| Step | Vitality | State |
|------|----------|-------|
| After resolution | 2.0 | RESOLVED |
| Decay 1 | 1.0 | DORMANT |
| Decay 2 | 0.0 | EXTINCT |

Resolution reduced vitality. Vitality decay produced DORMANT and eventually EXTINCT states.

### Final ecosystem state

| Component | Count | Status |
|-----------|-------|--------|
| Observations | 10 | Preserved |
| Difference groups | 2 | Preserved (Bird.fly, Bird.not_fly) |
| Tensions | 1 | Resolved |
| Questions | 1 | EXTINCT |
| Active questions | 0 | — |

The ecosystem ended with **no active questions**.

The experiment demonstrated: **observations → differences → tensions → questions → lifecycle**

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H109** | Questions possess lifecycles | Full trajectory EMERGENT → ACTIVE → RESOLVED → DORMANT → EXTINCT recorded in `lifecycle_history` |
| **H110** | Resolution reduces question vitality | Tension resolution subtracted 2.0 vitality; state transitioned to RESOLVED |
| **H111** | Questions can go extinct | Bird question reached EXTINCT at vitality 0.0 |
| **H112** | Memory and extinction coexist | Difference groups, resolved tension, and lifecycle history preserved after question extinction |

---

## Unexpected Observations

1. **The ecosystem finished with zero active questions.** All organizational precursors (observations, groups, resolved tension) remained; only the question ceased to be active.

2. **Question existence occupied only a small portion of the organizational chain.** Observations and difference groups persist indefinitely; the question existed transiently through lifecycle phases.

3. **Questions appeared temporary rather than permanent.** Static Question objects in prior experiments implied permanence; lifecycle model shows questions as time-bounded episodes.

---

## Surprising Observations

1. **Questions behaved similarly to organisms.** Birth (EMERGENT), active life (ACTIVE), response to environmental change (RESOLVED after tension resolution), senescence (DORMANT), death (EXTINCT).

2. **Question lifecycles resembled birth, life, dormancy and death.** Five-state trajectory maps cleanly onto biological lifecycle metaphors without explicit biological modeling.

3. **Question extinction did not destroy organizational history.** `lifecycle_history`, difference groups, and resolved tension records survived extinction — memory is structural, not identical to question aliveness.

4. **Questions appeared as transient structures rather than fundamental entities.** Builds on EXP-011/012: questions emerge, live, and die; differences and groups outlast them.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H113** | Questions are transient structures |
| **H114** | Questions are episodic rather than permanent |
| **H115** | Most organization exists outside questions |
| **H116** | Questions occupy only a temporary phase within cognitive ecosystems |

H115: At experiment end, 10 observations + 2 groups + 1 resolved tension persist; 0 live questions — organization mostly non-question.

H116: Questions are a phase within the chain, not the chain itself.

---

## Future Directions

- Investigate question resurrection (can EXTINCT questions revive if tension re-emerges?)
- Study rebirth after extinction (new question from same tension vs reactivation of old)
- Study memory preservation after extinction (what remains accessible vs what requires live questions)
- Investigate repeated lifecycles (same category, multiple birth-death cycles)
- Investigate ecosystem memory (aggregate history across extinct questions)

---

## Comparison: EXP-012 vs EXP-013

| Property | EXP-012 | EXP-013 |
|----------|---------|---------|
| Pipeline end | Emergent questions (EMERGENT) | Full lifecycle through EXTINCT |
| Question vitality | Not tracked | Tracked and reduced |
| Tension resolution | Not modeled | Resolution reduces vitality |
| Final question state | EMERGENT | EXTINCT |
| Active questions at end | 1 (EMERGENT) | 0 |

EXP-013 extends EXP-012 constructively: same emergence path, plus mortality.

---

## Conclusion

EXP-013 demonstrates that emergent questions possess full lifecycles and can go extinct while organizational memory persists. The Bird question traversed all five states in deterministic sequence; resolution and decay drove vitality to zero. The ecosystem ended with no active questions but intact difference groups and resolved tension records.

Questions appear episodic and transient (H113, H114) — occupying a temporary phase (H116) within a larger organizational structure (H115). This strengthens ecological interpretations of cognition: questions behave like organisms with birth, life, and death, not like permanent data structures.

Vitality thresholds remain externally imposed (see `exp013_failures.md`).
