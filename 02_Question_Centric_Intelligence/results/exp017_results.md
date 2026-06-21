# EXP-017 Results

Post-experiment summary for memory competition and selection.

Date: 2026-06-22  
Experiment: EXP-017 Memory Trace Competition

---

## Theme

Memory Competition and Selection

Test whether multiple extinct questions archived as memory traces compete for limited reconstruction resources when tensions reopen, and whether stronger traces win while weaker traces remain archived without becoming live questions.

---

## Experiment Summary

Started from:

```
observations → differences → tensions → questions → extinction → memory traces
```

Extended to three categories (Bird, Mammal, Insect) so **multiple extinct questions** existed before reintroduction.

### Phase 1: Emergence across three categories

| Category | Tension | Question | Initial vitality | Tension strength |
|----------|---------|----------|------------------|------------------|
| Bird | `t-bird-fly-vs-not_fly` | `eq-bird-fly-vs-not_fly` | 4.0 | 4.0 |
| Mammal | `t-mammal-fly-vs-swim` | `eq-mammal-fly-vs-swim` | 2.0 | 2.0 |
| Insect | `t-insect-fly-vs-crawl` | `eq-insect-fly-vs-crawl` | 2.0 | 2.0 |

All three questions promoted EMERGENT → ACTIVE, then resolved and decayed to **EXTINCT**.

### Phase 2: Archival and deletion

Three memory traces created via `archive_and_delete_extinct_questions()`:

| Trace | Question | Trace strength |
|-------|----------|----------------|
| `mem-eq-bird-fly-vs-not_fly` | `eq-bird-fly-vs-not_fly` | **1.00** |
| `mem-eq-mammal-fly-vs-swim` | `eq-mammal-fly-vs-swim` | **0.50** |
| `mem-eq-insect-fly-vs-crawl` | `eq-insect-fly-vs-crawl` | **0.50** |

Trace strength = `min(1.0, tension.strength / 4.0)` at archival. Live questions: **0**.

### Phase 3: Reintroduction

Twelve new observations (four per category) refreshed difference groups and **reopened all three tensions**. All remained persistent.

### Phase 4: Memory competition

`RECONSTRUCTION_BUDGET = 1`. Three traces entered competition, ranked by `(-trace_strength, trace_id)`:

| Rank | Trace | Strength | Outcome |
|------|-------|----------|---------|
| 1 | `mem-eq-bird-fly-vs-not_fly` | 1.00 | **Won** — reconstructed |
| 2 | `mem-eq-insect-fly-vs-crawl` | 0.50 | Lost — remains extinct |
| 3 | `mem-eq-mammal-fly-vs-swim` | 0.50 | Lost — remains extinct |

**Not every memory trace could reconstruct.** Stronger traces won competition. Weaker traces remained archived.

### Final state

| Question | Status | Notes |
|----------|--------|-------|
| `eq-bird-fly-vs-not_fly` | LIVE (ACTIVE) | Reconstructed; identity preserved |
| `eq-mammal-fly-vs-swim` | EXTINCT | Trace survives; lost competition |
| `eq-insect-fly-vs-crawl` | EXTINCT | Trace survives; lost competition |

Memory traces: **3** (all archived traces retained). Live questions: **1**.

The experiment demonstrated:

```
observations → differences → tensions → questions → extinction → memory → competition → reconstruction
```

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H141** | Memory traces compete | Three traces entered single competition round; ranked and filtered by budget |
| **H142** | Not every memory deserves resurrection | Two of three traces with valid tension reopenings did not reconstruct |
| **H143** | Selective resurrection improves organization | Only one live question after competition; latent traces exceed active questions |
| **H144** | Memory ecosystems exhibit evolutionary pressure | Trace strength determined survival under scarce reconstruction slots |

---

## Unexpected Observations

1. **Reopened tensions did not guarantee reconstruction.** All three tensions reopened and persisted, yet only Bird reconstructed — tension availability ≠ resurrection.

2. **Memory traces survived even when questions remained extinct.** Mammal and Insect traces retained full archival content at strength 0.50 while no live question existed for those tensions.

3. **The ecosystem remembered more than it actively expressed.** Three traces in memory; one live question — latent diversity exceeded active diversity.

---

## Surprising Observations

1. **Competition introduced scarcity.** EXP-015 reconstructed every matching trace; EXP-017 with budget=1 forced explicit tradeoffs among equally eligible memories.

2. **Selection emerged naturally.** Given fixed ranking rules and strength differentiation, Bird's dominance followed without per-trace manual assignment.

3. **Loss differed from forgetting.** EXP-016 removed traces via decay; EXP-017 losers **retained traces** but failed to become live questions — archival survival without expression.

4. **Memory became subject to evolutionary pressure.** Trace strength at archival acted as fitness proxy under reconstruction budget — stronger historical tension footprint won.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H145** | Memory and activity are separate |
| **H146** | Loss is not equivalent to forgetting |
| **H147** | Need alone is insufficient; resources matter |
| **H148** | Selection is more fundamental than resurrection |
| **H149** | Latent diversity exceeds active diversity |

H145: Three traces persisted while only one question was ACTIVE — memory substrate larger than expressed cognition.

H146: Permanent losses retained `MemoryTrace` objects; forgetting (EXP-016) deletes or weakens traces — distinct failure modes.

H147: All three tensions reopened (need present) but budget=1 allowed one winner — demand exceeded resources.

H148: Competition phase precedes and constrains reconstruction; resurrection is conditional on winning selection.

H149: 3 archived : 1 live ratio at experiment end.

---

## Comparison: EXP-015 vs EXP-016 vs EXP-017

| Property | EXP-015 | EXP-016 | EXP-017 |
|----------|---------|---------|---------|
| Memory traces | 1 (+ clutter in B) | 2 worlds | 3 |
| Reconstruction | All matching | All surviving | **Budget-limited** |
| Selection | None | Forgetting only | **Competition ranking** |
| Losers | — | Traces decay/absent | Traces **retained**, questions extinct |
| Scarcity type | None | Temporal decay | **Resource budget** |

EXP-017 adds **competitive selection** to the memory arc — complementing EXP-016's temporal forgetting.

---

## Future Directions

- Investigate adaptive reconstruction budgets
- Investigate competing memories (multiple traces per tension)
- Study memory inheritance
- Study ecosystem diversity
- Investigate evolutionary dynamics of memory

---

## Conclusion

EXP-017 demonstrates that memory traces compete under limited reconstruction resources. Bird's stronger trace (1.00) won the single budget slot; Mammal and Insect traces (0.50 each) remained archived while their questions stayed extinct despite reopened tensions.

The ecosystem held three memories but expressed one — separating memory from activity (H145) and introducing selection as a gate on resurrection (H148). Competition rules remain externally imposed (see `exp017_failures.md`).
