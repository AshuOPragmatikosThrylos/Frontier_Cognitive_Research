# EXP-009 Results

Post-experiment summary for adaptive contradiction tolerance.

Date: 2026-06-21  
Experiment: EXP-009 Adaptive Contradiction Tolerance

---

## Theme

Adaptive Contradiction Tolerance

Test whether communities can develop different tolerance levels through experience, whether pressure becomes relative to tolerance, and whether flexible communities avoid speciation that rigid communities undergo.

---

## Experiment Summary

Communities possessed different contradiction tolerances.

Two communities initialized with distinct personalities:

| Community | Initial tolerance | Expectation |
|-----------|-------------------|-------------|
| Bird | 1.5 | fly |
| Mammal | 4.0 | ground |

Tolerance changed through experience. Each contradiction increased tolerance by `0.35` (learning) in addition to adding `1.0` contradiction debt.

### Phase 1: Bird conforming

Four flying birds — no contradictions. Bird tolerance remains 1.5, debt 0.

### Phase 2: Bird contradicting

Four flightless birds — four contradictions.

| After event | Debt | Tolerance | Pressure |
|-------------|------|-----------|----------|
| Start | 0.0 | 1.5 | 0.0 |
| 4 contradictions | 4.0 | 2.9 | **1.1** |

Pressure 1.1 ≥ split limit 1.0 → **Bird splits** into Bird.Conforming and Bird.Contradicting.

Bird community began with low tolerance and adapted upward (1.5 → 2.9) but still speciated.

### Phase 3: Mammal contradicting

Bat (fly) and Whale (swim) — two contradictions against expectation `ground`.

| After event | Debt | Tolerance | Pressure |
|-------------|------|-----------|----------|
| Start | 0.0 | 4.0 | 0.0 |
| 2 contradictions | 2.0 | 4.7 | **0.0** |

Mammal community began with higher tolerance, adapted upward (4.0 → 4.7), and **absorbed contradictions without splitting**.

### Inheritance

Child communities inherited tolerance from parent at split time (2.9). Bird.Conforming and Bird.Contradicting both carry parent tolerance; contradiction debt reset to 0 on children.

### Final structure

```
Bird (organizational, debt=4.0, tolerance=2.9)
├── Bird.Conforming (4 members, tolerance=2.9)
└── Bird.Contradicting (4 members, tolerance=2.9)

Mammal (2 members, debt=2.0, tolerance=4.7, no split)
```

Communities displayed distinct behavioral styles: rigid-low-tolerance Bird speciated; flexible-high-tolerance Mammal stabilized.

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H79** — Tolerance evolves | Bird 1.5→2.9, Mammal 4.0→4.7 through contradiction experience |
| **H80** — Communities develop personalities | Different initial tolerances → different outcomes on similar contradiction loads |
| **H81** — Rigid communities speciate more frequently | Bird (low initial tolerance) split; Mammal (high) did not |
| **H82** — Flexible communities preserve diversity | Mammal retained unified community with 2 contradicting members |

---

## Unexpected Observations

1. **Learning did not necessarily prevent evolution.** Bird adapted tolerance upward by 93% yet still split — adaptation slowed but did not eliminate pressure.

2. **Mammal community accumulated contradictions without crisis.** Debt 2.0 with tolerance 4.7 produced zero pressure.

3. **Tolerance was inherited by child communities.** Bird.Conforming and Bird.Contradicting both received tolerance 2.9 from parent.

4. **Communities exhibited distinct styles of responding to contradiction.** Same increment mechanics, different trajectories due to initial tolerance.

---

## Surprising Observations

1. **Pressure depended on tolerance.** Formula `pressure = max(0, debt - tolerance)` makes contradiction relative (H83, H85).

2. **The same amount of contradiction produced different outcomes.** Four bird contradictions → split. Two mammal contradictions → stability. Not because counts differ only — tolerance dominated.

3. **Communities behaved similarly to cultures, scientific disciplines, and personalities.** Low-tolerance rigidity vs high-tolerance absorptive capacity.

4. **Contradictions existed without necessarily producing tension.** Mammal logged 2 contradictions with zero pressure — contradictions recorded, tension absent relative to tolerance.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H83** | Pressure is relative rather than absolute |
| **H84** | Communities inherit personality |
| **H85** | Contradictions only become pressure relative to tolerance |
| **H86** | Adaptation and evolution are complementary rather than opposing processes |

H86: Bird both adapted (tolerance↑) and evolved (split) — learning and speciation co-occur.

---

## Future Directions

- Investigate ecosystem-level selection of tolerance
- Study whether communities can select personalities
- Study long-term consequences of inherited tolerance
- Investigate tolerance diversity across ecosystems

---

## Comparison: EXP-008 vs EXP-009

| Property | EXP-008 | EXP-009 |
|----------|---------|---------|
| Split trigger | debt ≥ fixed limit | pressure ≥ limit |
| Tolerance | None | Adaptive per community |
| Pressure | = debt | = debt - tolerance |
| Multi-community | Bird only | Bird + Mammal |
| Outcome diversity | Single split path | Split vs absorb |

---

## Conclusion

EXP-009 demonstrates that adaptive tolerance produces richer dynamics than fixed thresholds. Communities develop personalities, pressure becomes relative, and identical contradiction mechanics yield different fates. Learning reduces but does not eliminate evolutionary pressure on rigid communities; flexible communities absorb contradictions that would crisis rigid ones.

Adaptive tolerance is a step toward self-regulation: absolute contradiction is insufficient to predict evolution — tolerance determines whether contradiction becomes pressure. Split threshold remains externally imposed (see `exp009_failures.md`).
