# EXP-010 Failures

Post-experiment failure analysis for random worlds comparison.

Date: 2026-06-22  
Experiment: EXP-010 Random Worlds Comparison

---

## Failure Analysis

No mechanical failure was observed. Both worlds executed independently on identical observations. World A deterministically reproduced EXP-009 outcomes. World B applied probabilistic splits and state changes without corrupting shared debt/tolerance tracking. Comparison reporting aligned metrics across worlds.

The significant finding is methodological, not mechanical: **random mechanisms failed to reproduce pressure-world organization** while increasing state diversity — confirming that prior observations depend on mechanism, not input sequence alone.

---

## Potential Danger

Researchers may construct mechanisms that merely confirm their assumptions.

Each incremental experiment (EXP-001 through EXP-009) added a plausible mechanism and observed coherent phenomena — deduplication, merge, communities, attention, speciation, contradiction pressure, adaptive tolerance. Without controls, it remained possible that **any** post-hoc mechanism would appear to "explain" the same observation sequence.

EXP-010 exposes this risk explicitly:

| Risk | How EXP-010 addresses it |
|------|--------------------------|
| Confirmation bias | Random null world tests whether phenomena are mechanism-dependent |
| Narrative fitting | Side-by-side comparison with phenomenon-reproduction flags |
| Over-interpretation of diversity | Shows diversity (state entropy) ≠ organization (semantic speciation) |

The danger is not that prior experiments were wrong — it is that their correctness was **unfalsified** until EXP-010.

---

## Need for Controls Became Evident

Prior experiments built structure without adversarial comparison. EXP-010 introduces:

1. **Positive control** — World A (pressure) must reproduce EXP-009
2. **Null-style control** — World B (random) tests whether organization emerges without meaningful mechanism
3. **Explicit mismatch reporting** — summary statistics flag when random world fails to reproduce Bird speciation or Mammal stability patterns

Controls proved essential (H87 strengthened): Bird speciation appeared only under pressure-driven semantic splitting, not under random partition of the same members.

---

## Random Worlds Showed That Diversity Alone Does Not Imply Meaningful Organization

World B produced greater question-state diversity (ACTIVE, DORMANT, PARTIALLY_RESOLVED, NEW scattered via 15% mutation rate) while failing to produce Bird.Conforming / Bird.Contradicting semantic structure.

This falsifies an implicit assumption that **more diversity always indicates richer cognition**. Diversity and organization are distinct properties (H93):

| Property | World A | World B |
|----------|---------|---------|
| Community organization | Semantic speciation | Arbitrary or absent |
| Question-state diversity | Low (mostly ACTIVE) | High (multi-state) |
| Interpretation | Structured evolution | Entropic variation |

Random worlds generate variation; pressure mechanisms generate structure (H91).

---

## Current Limitation

Current comparison involved only one random world.

```python
RANDOM_SEED = 42
RANDOM_SPLIT_CHANCE = 0.25
RANDOM_STATE_CHANGE_CHANCE = 0.15
```

Single seed, single probability triple. Outcomes include:

- Bird may or may not split randomly (25% per checkpoint per community)
- State distribution depends on cumulative Bernoulli trials across 10 observations

A single World B run cannot establish statistical confidence about random-world behavior — only demonstrate that **this** random configuration failed to reproduce **this** pressure-world pattern.

---

## What Improved vs EXP-009

| Aspect | EXP-009 | EXP-010 |
|--------|---------|---------|
| Falsification | None | Random control world |
| Comparison | Single world | Side-by-side metrics |
| Confidence basis | Mechanism plausibility | Mechanism vs null divergence |
| Research mode | Construction | Construction + comparison |

EXP-009 answered how tolerance modulates pressure. EXP-010 asks whether pressure-tolerance speciation is mechanism-dependent — answer: yes, for Bird semantic speciation.

---

## What Remains Externally Controlled

1. **Single random seed (42)** — one stochastic trajectory documented
2. **Fixed random probabilities** — 0.25 split, 0.15 state change; no sensitivity analysis
3. **One null model design** — random partition ignores behavior; other nulls (shuffled expectations, permuted observations) untested
4. **World A still uses external split threshold** — inherited from EXP-009 (`PRESSURE_SPLIT_LIMIT = 1.0`); control comparison does not resolve EXP-009's threshold limitation
5. **No ablation of World A components** — full EXP-009 logic vs full random logic; minimal mechanism set unknown

---

## Future Work Should Include

| Direction | Purpose |
|-----------|---------|
| **Alternative random seeds** | Estimate distribution of random-world outcomes; quantify reproduction failure rate |
| **Additional control worlds** | Diversity-threshold-only (EXP-007), fixed-debt (EXP-008), attention-limited (EXP-005) as alternate positives |
| **Simpler mechanisms** | Strip tolerance, strip learning — find minimal set producing Bird speciation |
| **Ablation studies** | Remove one component at a time from World A (tolerance, pressure formula, semantic split) |
| **Minimal models** | Smallest code path that preserves semantic speciation |
| **Null hypotheses** | Formalize H₀: "observation sequence alone determines speciation" — test across mechanism classes |

Seed sweep example (not implemented):

```
for seed in range(100):
    run_random_world(seed)
    record bird_speciation, state_diversity, mammal_stability
```

---

## The Mammal Robustness Note

Mammal stability appeared in both worlds — neither split Mammal under documented runs. This is a partial match, not full falsification of all prior claims:

- **Robust outcome:** Low contradiction load + high tolerance → no Mammal split (World A) or low split probability with 2 members (World B)
- **Non-robust outcome:** Bird semantic speciation — mechanism-dependent

Future controls should test which phenomena are robust across null worlds vs mechanism-specific.

---

## The Statistics Trap (H92)

Both worlds accumulated identical contradiction debt and tolerance because they share `process_observation()` and `record_contradiction()`. A researcher comparing **only** debt/tolerance tables would conclude the worlds are equivalent.

EXP-010's comparison layer explicitly checks **organizational outcomes** (speciation semantics, community structure, state coherence) — not summary statistics alone. Mechanisms matter more than aggregate counters (H92).

---

## Overall Assessment

Introducing controls significantly strengthened confidence in previous observations and shifted the project toward falsifiable science.

| Before EXP-010 | After EXP-010 |
|----------------|---------------|
| Mechanisms produced coherent phenomena | Mechanisms **distinct from randomness** produce coherent phenomena |
| Each experiment validated the next | Experiments require null comparison |
| Diversity interpreted as progress | Diversity distinguished from organization |
| Construction-only research loop | Construction + adversarial testing |

EXP-010 does not invalidate EXP-001 through EXP-009. It **conditions** their interpretation: organized speciation under adaptive tolerance is a real mechanistic outcome, not an artifact of the observation sequence or a property achievable through random splitting alone.

Remaining weakness: one random world, one seed, one null design. Confidence is strengthened but not complete. The research program should continue adversarial testing with seed sweeps, ablations, and additional control worlds before treating any phenomenon as established.

The transition from construction to comparison is the primary scientific advance of EXP-010.
