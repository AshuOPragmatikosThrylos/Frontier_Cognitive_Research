# EXP-010 Results

Post-experiment summary for random worlds and falsification.

Date: 2026-06-22  
Experiment: EXP-010 Random Worlds Comparison

---

## Theme

Random Worlds and Falsification

Test whether probabilistic mechanisms can reproduce the organized evolutionary phenomena observed under contradiction pressure and adaptive tolerance, and whether control worlds strengthen confidence in prior findings.

---

## Experiment Summary

Compared two worlds running on identical observations (10 total: 4 bird conforming, 4 bird contradicting, 2 mammal contradicting).

| World | Mechanism | Split trigger | State dynamics |
|-------|-----------|---------------|----------------|
| **World A (Pressure)** | Contradiction pressure + adaptive tolerance (EXP-009 logic) | `pressure ≥ 1.0` where `pressure = max(0, debt - tolerance)` | Questions remain ACTIVE unless created as anomalies |
| **World B (Random)** | Probabilistic splitting + random state changes | 25% chance per community at each checkpoint | 15% chance per question to flip state after each observation |

Both worlds received identical observations.

### World A outcome

Bird accumulated four contradictions against low initial tolerance (1.5). Tolerance adapted to 2.9; pressure reached 1.1 and triggered semantic speciation into Bird.Conforming and Bird.Contradicting. Mammal absorbed two contradictions with high tolerance (4.0 → 4.7); pressure remained 0.0; no split.

### World B outcome

Random splitting did not reproduce Bird's semantic speciation. Communities that did split partitioned members randomly (Bird.Random1 / Bird.Random2) rather than by conforming vs contradicting behavior. Random state changes increased question-state diversity across ACTIVE, DORMANT, PARTIALLY_RESOLVED, and NEW. Mammal remained unsplit in both worlds.

The random world failed to reproduce the Bird speciation observed in the pressure world.

Random mechanisms produced greater question-state diversity but weaker organization.

The experiment introduced control worlds and falsification into the research process.

### Final comparison (qualitative)

```
World A (Pressure)                    World B (Random)
├── Bird (organizational)             ├── Bird (may remain unified or split randomly)
│   ├── Bird.Conforming (semantic)    │   └── Bird.Random* (arbitrary partition)
│   └── Bird.Contradicting (semantic)
└── Mammal (stable, 2 members)        └── Mammal (stable, 2 members)
```

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H87** | Meaningful mechanisms outperform randomness | Pressure world produced semantic Bird speciation; random world did not reproduce the same organized split |
| **H88** | Random worlds exhibit weaker structure | Random splits ignore observed behavior; member partitions lack conforming/contradicting coherence |

---

## Unexpected Observations

1. **Random worlds produced more question-state diversity.** Probabilistic state changes (15% per question per observation) scattered questions across multiple states while the pressure world kept conforming questions ACTIVE.

2. **Randomness generated entropy rather than coherent organization.** Splits occurred without reference to behavioral coherence; diversity increased without corresponding structural meaning.

3. **Bird speciation occurred only in the pressure world.** Semantic partition by observed behavior (fly vs not fly) appeared exclusively under pressure-driven mechanics.

4. **Mammal stability appeared in both worlds.** Neither world split Mammal — pressure world due to high tolerance absorbing contradictions; random world due to probabilistic split chance not firing (or insufficient members at checkpoint).

---

## Surprising Observations

1. **Diversity and organization behaved differently.** World B exhibited higher state diversity without matching World A's community organization — diversity alone did not imply meaningful structure.

2. **Similar pressure statistics produced different evolutionary outcomes.** Both worlds accumulated identical contradiction debt and tolerance through shared observation processing; only World A translated accumulated pressure into semantically meaningful speciation.

3. **Controls proved essential.** Without World B, pressure-world Bird speciation could be mistaken for an inevitable consequence of the observation sequence rather than mechanism-dependent structure.

4. **The experiment marked a transition from construction to comparison.** Prior experiments (EXP-001 through EXP-009) built mechanisms incrementally; EXP-010 asks whether those mechanisms matter by pitting them against a null-style random control.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H90** | Randomness creates entropy rather than organization |
| **H91** | Randomness provides variation while pressure provides structure |
| **H92** | Mechanisms matter more than summary statistics |
| **H93** | Diversity and organization are distinct properties |

H92: Both worlds shared identical debt and tolerance trajectories from the same observations, yet diverged in speciation semantics — aggregate statistics insufficient to predict organizational outcome.

H93: World B's higher state diversity coexisted with weaker community structure, decoupling diversity from organization.

---

## Future Directions

- Investigate additional control worlds (e.g., diversity-threshold-only, attention-only)
- Compare alternative mechanisms side-by-side under identical inputs
- Study minimal requirements for organization (smallest mechanism set producing semantic speciation)
- Investigate robustness of observed phenomena across random seeds and parameter sweeps
- Continue adversarial testing — deliberately design controls that could falsify prior claims

---

## Comparison: EXP-009 vs EXP-010 World A

| Property | EXP-009 | EXP-010 World A |
|----------|---------|-----------------|
| Mechanism | Adaptive tolerance + pressure | Identical logic, encapsulated in `run_pressure_world()` |
| Observations | Same 10-observation sequence | Same sequence |
| Outcome | Bird splits, Mammal stable | Same (deterministic) |
| Control | None | Compared against World B |

EXP-010 World A reproduces EXP-009 as the positive control within a falsification framework.

---

## Conclusion

EXP-010 demonstrates that organized evolutionary phenomena — specifically semantic Bird speciation under adaptive tolerance — do not emerge from random splitting and state changes applied to the same observation stream. Random mechanisms increase entropy (state diversity) without producing coherent community organization. Mammal stability appeared in both worlds, suggesting some outcomes may be robust to mechanism while others are not.

Introducing control worlds shifts the research program from mechanism construction toward falsifiable comparison. Meaningful mechanisms (H87) outperform randomness; diversity and organization are separable properties (H93).
