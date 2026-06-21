# EXP-021 Results

Post-experiment summary for assumption removal and selection falsification.

Date: 2026-06-22  
Experiment: EXP-021 Assumption Removal

---

## Theme

Assumption Removal

Test whether memory selection — observed in EXP-017 and partially reproduced in EXP-020 — arises naturally from the difference-first pipeline, or depends on externally imposed competition assumptions (ranking, fixed budget, strength ordering).

---

## Experiment Summary

Started from:

```
observations → differences → tensions → questions → extinction → memory traces
```

Two worlds received **identical observations** through extinction and memory archival (Bird, Mammal, Insect — three categories, three traces). Worlds diverged only at reintroduction/reactivation.

### World A — Assumption-Rich

Used EXP-017 competition mechanics:

| Assumption | Value |
|------------|-------|
| Ranking | `sort(key=(-trace_strength, trace_id))` |
| Fixed budget | `RECONSTRUCTION_BUDGET = 1` |
| Strength ordering | Strongest trace wins |
| Winner selection | `candidates[:budget]` (top-N slice) |

**Outcome:** Selection **emerged** — Bird trace (strength 1.00) reconstructed; Mammal and Insect traces (0.50 each) permanently lost expression. One live question, two latent traces, two explicit permanent losses.

### World B — Assumption-Removed

Removed:

- Explicit ranking
- `winner=max()` / top-N winner logic
- Fixed budget
- Strength ordering for priority

Reactivation processed all eligible traces in **sorted tension_id order** (deterministic, not strength-based). Every persistent tension with a matching trace reconstructed.

**Outcome:** Selection **disappeared** — all three traces reactivated. Three live questions, zero permanent losses, zero latent traces. No winner/loser asymmetry.

### Shared outcome

**Stable traces persisted in both worlds.** All three memory traces remained archived with full identity and history. No natural trace disappearance occurred in either world.

### Conclusion

The experiment demonstrated that **previous selection behavior depended upon assumptions rather than arising naturally** from the pipeline through extinction and memory archival alone.

---

## Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H174** | Removing mechanisms reveals deeper mechanisms | Stripping ranking/budget exposed persistence as the surviving primitive |
| **H175** | Selection is not fundamental | Selection absent in World B; present only when assumptions imported |
| **H176** | Selection in previous experiments was externally imposed | EXP-017/020 selection reproduced exactly when World A assumptions applied; vanished when removed |
| **H177** | Persistence is more fundamental than selection | Traces stable in both worlds; selection asymmetry only in World A |

---

## Hypotheses Not Supported

| Hypothesis | Statement | Reason |
|------------|-----------|--------|
| **H171** | Selection does not require explicit ranking | World B removed ranking; no selection emerged |
| **H172** | Selection emerges from interaction | Pipeline interactions alone (tensions, extinction, traces) produced no selection in World B |
| **H173** | Selection survives assumption removal | Selection vanished completely when ranking, budget, and strength ordering removed |

---

## Unexpected Observations

1. **Selection vanished completely when assumptions were removed.** Not weakened — absent. Three live questions in World B vs one in World A.

2. **Stable traces persisted.** All three traces retained in memory in both worlds; archival identity unchanged.

3. **No natural disappearance occurred.** Neither world lost traces through pipeline dynamics alone; disappearance was not observed without additional mechanisms (cf. EXP-016 forgetting).

---

## Surprising Observations

1. **The project lost one of its strongest motifs.** Selection under budget — central to EXP-017, EXP-020 narrative — was shown to be assumption-dependent, not emergent.

2. **Persistence survived while selection disappeared.** The memory layer's conservative archival behavior outlasted the competitive selection story.

3. **Destroying assumptions produced more insight than adding mechanisms.** EXP-018–019 added cooperation/merging (failed); EXP-021 removed assumptions and falsified selection itself.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H175** | Selection is not fundamental |
| **H176** | Selection in previous experiments was externally imposed |
| **H177** | Persistence is more fundamental than selection |

*(H174 supported in same experiment; H175–H177 confirmed as principle-level claims.)*

---

## Side-by-Side Comparison

| Metric | World A (Rich) | World B (Removed) |
|--------|----------------|-------------------|
| Ranking | Yes | No |
| Fixed budget | 1 | None |
| Strength ordering | Yes | No |
| Memory traces | 3 | 3 |
| Live questions | 1 | 3 |
| Explicit winners | 1 (Bird) | 0 |
| Permanent losses | 2 | 0 |
| Selection pattern | **Yes** | **No** |
| Traces disappeared | No | No |

---

## Comparison: EXP-017 vs EXP-021 World A vs World B

| Experiment | Mechanism | Selection |
|------------|-----------|-----------|
| EXP-017 | Assumption-rich only | Bird wins |
| EXP-021 World A | Same as EXP-017 | Bird wins — **reproduced** |
| EXP-021 World B | Assumptions removed | **All three live — no selection** |

EXP-021 World A confirms EXP-017 is reproducible. World B falsifies selection as pipeline-emergent.

---

## Future Directions

- Investigate persistence — what makes traces stable across assumption changes?
- Study natural trace disappearance — EXP-016 forgetting as separate attack vector
- Search for assumption-free mechanisms — spontaneous asymmetries without sort/budget
- Investigate whether persistence survives further attacks
- Seek deeper motifs beneath selection — difference, tension, archival identity

---

## Conclusion

EXP-021 compared assumption-rich and assumption-removed reactivation on identical memory traces. Selection emerged in World A and **disappeared entirely** in World B. Stable traces persisted in both.

Removing mechanisms revealed persistence as deeper than selection (H174). Selection is not fundamental (H175). Prior selection results were assumption-imposed (H176). Persistence outranks selection as a primitive (H177). Hypotheses that selection could survive without ranking, emerge from interaction alone, or persist after assumption removal were **falsified** (H171–H173).

This experiment significantly reduced confidence in selection as a fundamental principle while strengthening confidence in persistence. See `exp021_failures.md` for limitation analysis.
