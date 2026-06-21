# EXP-017 Failures

Post-experiment failure analysis for memory trace competition.

Date: 2026-06-22  
Experiment: EXP-017 Memory Trace Competition

---

## Failure Analysis

No mechanical failure was observed. Pipeline completed: three questions emerged across Bird, Mammal, and Insect categories, went extinct, archived to memory traces, tensions reopened on reintroduction, three traces entered competition, Bird won the single reconstruction budget slot, Mammal and Insect remained extinct with traces preserved.

The significant findings are methodological: competition introduced scarcity and evolutionary pressure, but selection criteria remain externally programmed.

---

## Current Limitation

### Competition rules remain externally imposed

Ranking and selection:

```python
candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))
winners = candidates[:RECONSTRUCTION_BUDGET]
losers = candidates[RECONSTRUCTION_BUDGET:]
```

Equivalent to:

```
sort traces by strength
select top N
reconstruct winners only
```

Selection criteria are explicitly programmed. The ecosystem does not yet determine competition mechanisms autonomously — it does not discover that traces should compete, how to rank them, or what budget applies. The experimenter sets `RECONSTRUCTION_BUDGET = 1` and `trace_strength_from_tension()`.

### Trace strength is assigned at archival, not earned through competition

```python
trace_strength = min(1.0, tension.strength / TRACE_STRENGTH_DIVISOR)
```

Bird wins because Bird had more initial observations (4 vs 2 per group), not because the trace proved fitness during competition. Strength is a static archival property — competition only reads it, never updates it.

H144 (evolutionary pressure) is supported metaphorically but achieved through predetermined strength differentiation.

### The ecosystem does not yet determine what deserves resurrection

All-or-nothing policy:

- Every reopened persistent tension with a trace → enters competition
- Every winner → full reconstruction
- Every loser → no reconstruction (trace retained)
- No trace-initiated bids, no tension-priority overrides, no partial reconstruction

Resurrection remains conditional on winning an externally defined tournament.

---

## What Improved vs EXP-015 and EXP-016

| Aspect | EXP-015 | EXP-016 | EXP-017 |
|--------|---------|---------|---------|
| Trace count | 1 | 2 (World A/B) | 3 |
| Reconstruction | All matching | All surviving | **Budget-limited** |
| Losers | None | Forgotten (World B) | **Retained but unexpressed** |
| Scarcity | None | Temporal decay | **Resource competition** |
| Multi-question | No | No | **Yes** |
| Selection | None | Passive decay | **Active ranking** |

EXP-015: memory externalized. EXP-016: memory pruned. EXP-017: memory **selected** — expression scarcer than storage.

---

## Additional Limitations

### 1. Single competition round

One budget application after reintroduction. No multi-round tournaments, no re-competition after new observations, no dynamic budget adjustment.

### 2. Fixed budget constant

`RECONSTRUCTION_BUDGET = 1` hardcoded. With three traces, exactly two losses guaranteed — outcome sensitivity to budget untested.

### 3. Tie-breaking is lexical

Mammal and Insect both at strength 0.50. Rank determined by `trace_id` string order — `mem-eq-insect-fly-vs-crawl` before `mem-eq-mammal-fly-vs-swim`. No ecological tie-break (e.g. reopened tension strength, recency, category priority).

### 4. Loss ≠ forgetting

Permanent losses retain traces indefinitely. Ecosystem accumulates unexpressed memory — potential clutter without EXP-016-style decay on losers.

### 5. No competing traces per tension

One trace per question, one question per tension. No conflicting memories, duplicate archives, or merge-under-competition.

### 6. Reintroduction observations hardcoded

Twelve fixed entities across three categories — same limitation class as prior experiments.

### 7. Trace strength tied to initial observation count

Bird's advantage (1.00 vs 0.50) reflects initial group sizes, not post-extinction experience or reintroduction demand. Reopened tension strengths (6.0, 4.0, 4.0) do not affect competition ranking.

### 8. Parallel type system persists

`LifecycleQuestion`, `MemoryTrace`, `ExperimentState` local — not integrated with `src.question.Question`.

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Adaptive selection** | Ranking rules or budget change with ecosystem state |
| **Dynamic budgets** | Reconstruction slots scale with observation load or tension count |
| **Cooperation between memories** | Traces coalition or merge to share budget |
| **Distributed competition** | Category-local budgets vs global pool |
| **Self-organized resource allocation** | Traces bid for reconstruction; ecosystem allocates without fixed sort |
| **Strength updates during competition** | Reopened tension strength feeds back into trace fitness |
| **Multi-round selection** | Iterative competition across observation waves |
| **Loss with forgetting** | Combine EXP-016 decay on permanent losers |

---

## EXP-012 → EXP-017 Memory Arc

| Experiment | Memory dynamic |
|------------|----------------|
| EXP-012 | Emergence only |
| EXP-013 | Lifecycle + extinction |
| EXP-014 | Resurrection (same object) |
| EXP-015 | Trace archival + reconstruction |
| EXP-016 | Selective forgetting (decay) |
| EXP-017 | **Competition + selective expression** |

Progression: remember → forget → **compete for expression**.

---

## Loss vs Forgetting vs Extinction

| Outcome | Trace | Live question | EXP |
|---------|-------|---------------|-----|
| Extinction (pre-archive) | — | Dead → archived | 013 |
| Forgetting | Deleted/weakened | — | 016 |
| Competition loss | **Retained** | **Not reconstructed** | 017 |
| Competition win | Retained | Reconstructed | 017 |

H146: loss and forgetting are distinct — EXP-017 introduces silent memory (archived but unexpressed).

---

## Overall Assessment

Competition introduced scarcity and evolutionary pressure, significantly enriching ecosystem behavior beyond simple reconstruction.

**Achieved:**

- Memory traces compete (H141)
- Not every memory resurrects (H142)
- Selective resurrection under budget (H143)
- Evolutionary pressure metaphor via strength ranking (H144)
- Memory/activity separation (H145)
- Loss ≠ forgetting (H146)
- Latent diversity > active diversity (H149)

**Still externally controlled:**

- When to compete (after all tensions reopen)
- How to rank (strength descending, trace_id tie-break)
- How many win (`RECONSTRUCTION_BUDGET`)
- What strength means (archival formula from initial tension)
- What losers suffer (no reconstruction, no trace penalty)

**Scientific value:**

EXP-017 is the first experiment where **multiple valid memories coexist but only one expresses**. This is the closest the program has come to evolutionary selection within the memory layer — yet selection rules remain experimenter-imposed.

The two permanent losses with surviving traces are the experiment's strongest image: the ecosystem **knows** Mammal and Insect questions but **chooses** (via programmed budget) not to speak them.

Next stress test: endogenous competition — traces or tensions that determine their own ranking, budgets that adapt, and cooperation among memories before selection culls expression.

Competition mechanisms must become endogenous before memory selection can be called a property of the ecosystem rather than the experimenter's sort function.
