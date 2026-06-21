# Confidence Dashboard

Internal estimates only. Not claims about nature of intelligence.

Scale: **0–100%** (subjective, based on toy experiments and discussion coherence).

---

## Current Estimates (post EXP-016 implementation)

| Framework | Confidence | Notes |
|-----------|------------|-------|
| **Interesting Framework** | 78% | Rich dynamics, clear narrative arc, reproducible toy worlds |
| **Useful Framework** | 52% | Useful for thought experiments and architecture sketches; not yet operational |
| **Preprint-worthy Narrative** | 38% | Needs external validation, formalism, and EXP-016+ results documentation |
| **New Cognitive Principles** | 45% | Difference-first, tension-first, episodic questions — plausible but early |
| **Cross-domain Potential** | 35% | Analogies to science, attention, memory; no real-world benchmarks |
| **Fundamental Breakthrough** | 8% | Deliberately low — toy domain, no empirical psychology/AI comparison |
| **Dead-end Risk** | 28% | Reduced after EXP-010/011; still risk of overfitting Penguin World |

---

## Confidence History by Milestone

| Milestone | Interesting | Useful | Preprint | Principles | Cross-domain | Breakthrough | Dead-end |
|-----------|-------------|--------|----------|------------|--------------|--------------|----------|
| EXP-001 (merge) | 40 | 25 | 10 | 20 | 15 | 5 | 45 |
| EXP-003 (hierarchy collapse) | 50 | 30 | 12 | 25 | 15 | 5 | 40 |
| EXP-004 (communities) | 55 | 35 | 15 | 30 | 18 | 5 | 35 |
| EXP-005 (attention) | 60 | 38 | 18 | 35 | 20 | 5 | 32 |
| EXP-008 (pressure) | 65 | 42 | 20 | 40 | 22 | 6 | 30 |
| EXP-010 (falsification) | 68 | 44 | 22 | 42 | 22 | 6 | 25 |
| EXP-011 (minimal worlds) | 72 | 46 | 25 | 48 | 25 | 7 | 22 |
| EXP-013 (extinction) | 74 | 48 | 28 | 50 | 28 | 7 | 20 |
| EXP-015 (memory) | 76 | 50 | 32 | 48 | 30 | 8 | 18 |
| EXP-016 (forgetting, impl.) | 78 | 52 | 38 | 45 | 35 | 8 | 28 |

*EXP-016 row: implementation complete; formal results not yet recorded — preprint confidence not raised on outcomes.*

---

## What Moved Confidence Up

- **EXP-010:** Control worlds; mechanisms falsifiably matter.
- **EXP-011:** Minimal reduction identifies necessary vs sufficient structure.
- **EXP-013–015:** Coherent lifecycle + memory story without `src/` dependency drift.
- **Git discipline:** Full experiment history preserved.

## What Moved Confidence Down or Held It Back

- **EXP-011 World D:** Questions may be inert for core organization — challenges founding premise (H2).
- **Single domain:** Bird/Mammal toy world throughout.
- **No baselines:** No comparison to standard ML, ACT-R, or cognitive science models.
- **Hand-tuned constants:** Thresholds, decay rates, budgets not derived from data.
- **EXP-016:** Not yet in results corpus; dead-end risk ticked slightly (complexity creep in memory stack).

---

## Interpretation Guardrails

- High **Interesting** + low **Breakthrough** = good exploratory research, not a discovery claim.
- **Dead-end Risk** rises if next experiments only add mechanisms without new falsification or domain change.
- **Preprint-worthy** requires at least: documented EXP-016 results, explicit limitations section, and one non-Bird domain or external reader test.
