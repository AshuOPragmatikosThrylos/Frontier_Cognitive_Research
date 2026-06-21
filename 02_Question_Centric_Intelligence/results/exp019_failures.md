# EXP-019 Failures

Post-experiment failure analysis for memory trace merging.

Date: 2026-06-22  
Experiment: EXP-019 Memory Trace Merging

---

## Failure Analysis

The intended memory merging behavior did not emerge in the completed experiment.

**No abstractions formed.** **No merge events occurred.** Three individual memory traces persisted with stable identities despite repeated mammal–insect co-activation reaching the configured threshold of 2.

This is an **important negative result**, not a mechanical crash. The pipeline completed; merge was attempted and falsified.

---

## Possible Explanations

| Explanation | Detail |
|-------------|--------|
| **Co-activation too weak** | Temporal co-occurrence at tension reopening may not constitute merge-worthy coupling |
| **Insufficient coupling** | Mammal and Insect share no tension, category, or structural dependency — only co-activation timing |
| **Identity highly stable** | Memory traces may resist dissolution once archived; identity anchored at archival time |
| **Threshold insufficient** | Count=2 co-activations may be too low, or count alone is wrong merge signal |
| **Layer mismatch** | Question merge (EXP-002) used similarity; memory merge used co-activation — wrong analog |

---

## Current Limitations

### Merge rules remain externally defined

Merge trigger:

```python
if co_activation_counts[pair_key] >= CO_ACTIVATION_MERGE_THRESHOLD:
    merge_traces(state, trace_ids)
```

The ecosystem does not autonomously discover that traces should merge. Even when threshold logic exists, the completed run produced no merges — suggesting the rule does not match conditions under which memory abstraction would naturally occur.

### No shared tension between merge candidates

Mammal and Insect traces link to distinct tensions (`t-mammal-fly-vs-swim`, `t-insect-fly-vs-crawl`). Co-activation is temporal, not structural. EXP-002 merge grouped questions by `(category, expected_behavior, observed_behavior)` similarity — a stronger coupling signal.

### Question vs memory asymmetry (H163)

EXP-002 merged live questions. EXP-019 attempted to merge archived traces. The failure may indicate that **questions are mergeable while memories are conservative** — different evolutionary laws at different layers.

---

## What EXP-019 Did Achieve

| Aspect | Result |
|--------|--------|
| Falsification | Memory merge via co-activation not supported (H156–H159) |
| Identity stability | H161 supported — traces resisted dissolution |
| Co-activation insufficiency | H160, H162 supported |
| Layer distinction | H163 introduced — questions ≠ memories for merge |
| Program resistance | Second consecutive memory-layer negative (after EXP-018) |

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Shared tensions** | Traces linked to same tension may merge more readily |
| **Dependency-based merging** | Merge when one trace's tension depends on another |
| **Cooperation before merging** | Successful coalitions (if achieved) as merge prerequisite |
| **Adaptive abstractions** | Merge rules change with ecosystem state |
| **Similarity-based trace merge** | Port EXP-002 similarity key to trace layer |
| **Stronger coupling threshold** | Require shared groups, not just co-activation count |

---

## EXP-002 → EXP-019 Merge Arc

| Experiment | Layer | Trigger | Outcome |
|------------|-------|---------|---------|
| EXP-002 | Questions | Similarity + merge call | **Merge succeeded** |
| EXP-019 | Memory traces | Co-activation count ≥ 2 | **Merge failed** |

Direct transfer of merge intuition from questions to memories was falsified.

---

## EXP-015 → EXP-019 Identity Arc

| Experiment | Identity claim | Outcome |
|------------|----------------|---------|
| EXP-015 | Identity survives deletion via trace | Supported |
| EXP-017 | Identity preserved on reconstruction | Supported |
| EXP-019 | Identity resists merge/dissolution | **Supported (negative merge)** |

Identity grows **more stable** as the memory layer matures — traces archive identity and resist subsequent transformation.

---

## Overall Assessment

EXP-019 produced an important **negative result**. Identity proved substantially more robust than expected.

**Did not achieve:**

- Memory trace merging
- Emergent abstractions
- Inherited merged histories (H159 untested)

**Did achieve:**

- Documented co-activation without merge (H160)
- Confirmed identity stability (H161)
- Falsified co-activation-as-abstraction trigger (H162)
- Introduced question/memory layer asymmetry (H163)

**Scientific value:**

Two consecutive memory-layer falsifications (EXP-018 cooperation, EXP-019 merging) strengthen the program's resistance culture. The memory stack may have reached a **conservative equilibrium**: traces archive identity, competition selects expression, but traces do not easily combine or cooperate under simple rules.

Next stress test: **shared tension** or **dependency-driven** merge — determine whether structural coupling succeeds where temporal co-activation failed.

Merge and cooperation rules must become structurally grounded before memory abstraction can be called emergent rather than experimenter-imposed.
