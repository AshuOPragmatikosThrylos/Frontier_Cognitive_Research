# EXP-008 Results

Post-experiment summary for contradiction pressure.

Date: 2026-06-21  
Experiment: EXP-008 Contradiction Pressure

---

## Theme

Contradiction Pressure

Test whether unresolved contradictions against community expectations accumulate pressure and drive speciation — without relying on explicit diversity thresholds.

---

## Experiment Summary

Communities maintained expectations.

The Bird community held expectation **fly**. Observations were processed against that community expectation, not only against individual question state.

### Phase 1: Conforming observations

Sparrow, Robin, Eagle, Falcon — all observed `fly`, matching community expectation.

| Effect | Value |
|--------|-------|
| Contradiction debt | 0.0 |
| Contradictions logged | 0 |
| Pressure | stable |

Conforming observations produced little pressure.

### Phase 2: Contradicting observations

Penguin, Ostrich, Emu, Kiwi — all observed `not fly`, violating community expectation.

| Contradiction | Debt increment |
|---------------|----------------|
| Penguin | +1.0 |
| Ostrich | +1.0 |
| Emu | +1.0 |
| Kiwi | +1.0 |

**Total contradiction debt:** 4.0  
**Pressure split limit:** 4.0 → split triggered

### Speciation outcome

Bird community split into:

- **Bird.Conforming** — Sparrow, Robin, Eagle, Falcon (expectation: fly)
- **Bird.Contradicting** — Penguin, Ostrich, Emu, Kiwi (expectation: anomaly)

Parent **Bird** survived with 0 members, 2 children, historical contradiction debt 4.0.

### After speciation

| Community | Contradiction debt | Contradictions | Members |
|-----------|-------------------|----------------|---------|
| Bird | 4.0 (historical) | 4 logged | 0 |
| Bird.Conforming | 0.0 | none | 4 |
| Bird.Contradicting | 0.0 | none | 4 |

Contradiction pressure disappeared in child communities after speciation. Parent-child community relationships emerged. Parent community survived without members.

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H71** — Contradictions drive evolution | Four contradictions triggered community split |
| **H72** — Contradiction debt accumulates | Debt rose 0 → 4.0 monotonically with each contradicting observation |
| **H73** — Communities evolve to reduce contradictions | Split partitioned conforming vs contradicting members; children internally consistent |

---

## Strengthened Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H74** — Difference may be more fundamental than questions | Split driven by expectation mismatch (difference), not question count or diversity metric |

Contradiction against community expectation preceded speciation more naturally than EXP-007's behavior-type counting.

---

## Unexpected Observations

1. **Contradiction debt vanished after splitting in child communities.** New children start at 0.0 debt — operational pressure reset.

2. **Child communities became internally stable.** Conforming children all match `fly`; Contradicting children all violate `fly` — no internal expectation conflict.

3. **Parent communities survived despite losing all members.** Bird persists as organizational ancestor with contradiction history.

4. **Speciation relieved internal tension.** Fly and not-fly no longer coexist under one expectation.

---

## Surprising Observations

1. **Evolution appeared to act as a pressure-relief mechanism.** Split occurred at pressure limit; child communities born without accumulated contradiction debt.

2. **Contradictions rather than diversity became the driving force.** EXP-008 replaces EXP-007's `behavior_types >= 2` rule with `contradiction_debt >= limit`.

3. **Communities behaved similarly to phase transitions and scientific revolutions.** Accumulating anomaly (contradiction debt) → critical threshold → structural reorganization (speciation).

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H75** | Evolution relieves contradiction pressure |
| **H76** | Organizational abstractions outlive contradictions |
| **H77** | Questions may be local manifestations of unresolved tensions |
| **H78** | Tension may be more fundamental than questions |

H77–H78 extend H74: questions (Penguin, Ostrich…) are surface expressions; contradiction pressure is the deeper variable.

---

## Future Directions

- Investigate who determines acceptable levels of contradiction
- Investigate adaptive pressure thresholds
- Study repeated contradiction cycles
- Study contradiction propagation across communities

---

## Comparison: EXP-007 vs EXP-008

| Property | EXP-007 | EXP-008 |
|----------|---------|---------|
| Split trigger | Diversity threshold (≥2 types, ≥2 each) | Contradiction debt ≥ 4.0 |
| Driving concept | Internal diversity count | Unresolved expectation violations |
| Pressure metric | behavior_types | contradiction_debt |
| Child names | Flying / Flightless | Conforming / Contradicting |
| Naturalness | Handcrafted | More natural (H71–H73) |

---

## Conclusion

EXP-008 demonstrates that contradiction pressure can drive community speciation without diversity counting. Expectation violations accumulate debt; sufficient pressure triggers split; children emerge internally stable. Evolution functions as tension relief — though split threshold remains externally imposed (see `exp008_failures.md`).

Contradiction may be more fundamental than questions (H74, H78). The experiment connects to Discussion 010 themes on contradiction and tension as sources of intelligence.
