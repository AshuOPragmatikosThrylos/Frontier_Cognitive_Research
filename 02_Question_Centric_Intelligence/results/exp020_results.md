# EXP-020 Results

Post-experiment summary for cross-domain selection reproduction.

Date: 2026-06-22  
Experiment: EXP-020 Cross-Domain Reproduction

---

## Theme

Cross-Domain Reproduction

Test whether memory competition and selection — established in biological toy worlds (EXP-017) — reproduce when identical pipeline rules are applied to unrelated domains.

---

## Experiment Summary

Started from:

```
observations → differences → tensions → questions → extinction → memory traces → competition → selection
```

The experiment investigated whether selection reproduces outside biological worlds.

Four domains were tested with **identical rules** (`RECONSTRUCTION_BUDGET = 1`, trace strength = `min(1.0, tension.strength / 4.0)`, rank by strength, winner = top trace):

| Domain | Categories | Strong category (4+4) | Weak categories (2+2) |
|--------|------------|----------------------|------------------------|
| **Animals** | Bird, Mammal | Bird | Mammal |
| **Software Bugs** | Deadlock, MemoryLeak, RaceCondition | Deadlock | MemoryLeak, RaceCondition |
| **Scientific Theories** | WaveTheory, ParticleTheory, Relativity | WaveTheory | ParticleTheory, Relativity |
| **Distributed Databases** | Consistency, Availability, PartitionTolerance | Consistency | Availability, PartitionTolerance |

Each domain ran the full pipeline: initial ingest → extinction lifecycle → archival → reintroduction → tension reopen → memory competition.

### Selection reproduced in

| Domain | Winner | Losers | Pattern |
|--------|--------|--------|---------|
| **Animals** | Bird (`eq-bird`, strength 1.00) | Mammal (0.50) | Strong trace wins; weak trace archived without reconstruction |
| **Software Bugs** | Deadlock (`eq-deadlock`, 1.00) | MemoryLeak, RaceCondition (0.50 each) | Same EXP-017 motif across three categories |
| **Scientific Theories** | WaveTheory (`eq-wavetheory`, 1.00) | ParticleTheory, Relativity (0.50 each) | Same motif in abstract theory domain |

In these three domains, **winners and losers appeared**, **memory competition occurred**, and **stronger traces reconstructed** while weaker traces remained archived — reproducing EXP-017 selection dynamics without biological vocabulary.

### Selection did not reproduce in

**Distributed Databases**

Despite identical rules and successful pipeline execution through archival and competition phases, selection **did not reproduce** as a meaningful cross-domain phenomenon in this domain. The CAP-style tradeoff structure (Consistency, Availability, Partition Tolerance) did not yield the same winner/loser selection dynamic observed elsewhere. Domain coupling and joint constraint semantics overrode the simple strength-differentiation pattern.

### Overall outcome

The experiment demonstrated that **cross-domain recurrence exists** (3/4 domains), but **universality was not observed** (1/4 failure). Selection is partially domain-independent (H164), not fully so.

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H165** | Memory competition reproduces across domains | Animals, Software Bugs, and Scientific Theories all showed ranked competition, budget-limited reconstruction, and permanent losses |
| **H166** | Differences generate similar motifs in unrelated worlds | Same pipeline (differences → tensions → questions → traces → competition) produced comparable winner/loser structure in three non-biological domains |
| **H167** | Cross-domain recurrence is stronger evidence than additional single-domain experiments | Three independent domain successes increase confidence in selection motif beyond repeating Bird/Mammal/Insect |

---

## Partially Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H164** | Selection is domain-independent | Supported in Animals, Software Bugs, Scientific Theories; **not supported** in Distributed Databases — selection requires preconditions (H168) |

---

## Unexpected Observations

1. **Distributed Databases failed to produce selection.** The fourth domain broke the otherwise uniform cross-domain pattern despite identical code and observation counts.

2. **Selection proved non-universal.** Three successes do not imply all worlds will reproduce the same dynamics.

3. **Theory boundaries became visible.** The failure localized where the behavior-diff template meets structurally coupled engineering tradeoffs (CAP), not where the pipeline mechanics failed.

---

## Surprising Observations

1. **Absence of selection was informative.** The Distributed Databases failure is a boundary result, not a crash — the pipeline completed and the negative outcome constrains generalization claims.

2. **Failure in one domain increased confidence in the scientific process.** A partial success (3/4) with one documented failure is stronger than four undocumented single-domain runs.

3. **Cross-domain similarities appeared despite domain differences.** Software bugs, scientific theories, and animals share no semantic content yet produced parallel competition outcomes under shared rules.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H168** | Selection requires preconditions — not all observation structures support strength-differentiated competition |
| **H169** | Absence of selection is informative — domain failures reveal theory boundaries |
| **H170** | General theories should predict failures — a complete account must explain both reproduction and non-reproduction |

---

## Cross-Domain Comparison

| Property | Animals | Software Bugs | Scientific Theories | Distributed Databases |
|----------|---------|---------------|---------------------|----------------------|
| Pipeline completed | Yes | Yes | Yes | Yes |
| Memory traces archived | Yes | Yes | Yes | Yes |
| Competition ran | Yes | Yes | Yes | Yes |
| Selection reproduced | **Yes** | **Yes** | **Yes** | **No** |
| Strong/weak differentiation | 1.00 vs 0.50 | 1.00 vs 0.50 | 1.00 vs 0.50 | Insufficient for selection motif |

---

## Comparison: EXP-017 vs EXP-020

| Property | EXP-017 | EXP-020 |
|----------|---------|---------|
| Domains | 1 (biological) | 4 (cross-domain) |
| Categories | 3 | 2–3 per domain |
| Rules | budget=1, strength ranking | **Identical** |
| Outcome | Bird wins | Bird-equivalent wins in 3/4 domains |
| Generalization | Single world | **Partial cross-domain confirmation + 1 boundary failure** |

EXP-020 elevates EXP-017 from single-world result to **partially general phenomenon**.

---

## Future Directions

- Investigate preconditions for selection (H168)
- Investigate domain boundaries — when does behavior-diff template break?
- Investigate assumption removal — ranking, budget, max()
- Study simpler mechanisms — spontaneous competition without imposed sort
- Search for universal motifs — what survives across all successful domains?

---

## Conclusion

EXP-020 tested whether selection reproduces outside biological worlds. **Three of four domains confirmed** the EXP-017 competition motif. **Distributed Databases failed**, demonstrating that cross-domain recurrence exists but universality does not.

Memory competition reproduces across domains (H165). Differences generate similar motifs in unrelated worlds (H166). Cross-domain recurrence strengthens the evidence base more than additional single-domain runs (H167). Selection is only partially domain-independent (H164). Selection requires preconditions (H168); absence of selection is informative (H169); general theories should predict failures (H170).

Competition and ranking mechanisms remain externally imposed (see `exp020_failures.md`). The experiment strengthened confidence in cross-domain recurrence while exposing important limitations and boundaries.
