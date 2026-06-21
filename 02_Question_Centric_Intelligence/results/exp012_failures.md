# EXP-012 Failures

Post-experiment failure analysis for emergent questions.

Date: 2026-06-22  
Experiment: EXP-012 Emergent Questions

---

## Failure Analysis

### Mechanical failure (repaired)

Initial experiment crashed before producing results.

**Error:**

```
TypeError: '<' not supported between instances of 'DifferenceGroup' and 'DifferenceGroup'
```

**Location:** `groups_for_category()`

```python
return sorted(
    group for group in state.difference_groups.values() if group.category == category
)
```

**Cause:** `sorted()` without a `key` invokes `<` comparisons between elements. `@dataclass DifferenceGroup` does not define ordering, so Python raised `TypeError` when Bird groups were paired for tension detection.

**Repair:** Added deterministic sort key:

```python
key=lambda group: group.name
```

Bug repaired in commit `QCI-022 Fix EXP-012 DifferenceGroup sorting crash`. Scientific conclusions were drawn only after successful execution.

### No remaining mechanical failures

After repair, pipeline completed: Bird groups formed, persistent tension detected, emergent question created. Mammal correctly produced no groups, tensions, or questions.

---

## What the Crash Revealed

The crash occurred at the tension-detection stage — the bridge between difference groups and emergent questions. Without stable group ordering:

- Pairwise iteration order would be undefined
- Tension ids (`behavior_a` vs `behavior_b`) could flip
- Question emergence would be non-reproducible even before the TypeError halted execution

The fix was minimal and preserved experiment design. Sorting by `group.name` aligns with `form_difference_groups()` which creates names from sorted behavior keys.

---

## Current Limitations

### 1. Question emergence depends on explicit persistence thresholds

```python
PERSISTENT_TENSION_MIN = 2
persistent = strength >= PERSISTENT_TENSION_MIN
```

Persistence is a fixed constant, not learned or adapted. Mammal's fly/swim difference (strength 1.0) fails persistence by design — experimenter decides what counts as "persistent."

Same limitation class as `PRESSURE_SPLIT_LIMIT` (EXP-008/009) and `DIFFERENCE_MIN_PER_GROUP` (EXP-011).

### 2. Question generation rules remain externally imposed

Emergent questions use a fixed template:

```python
text=f"Why do {tension.category} entities both {tension.behavior_a} and {tension.behavior_b}?"
```

The experimenter defines:

- When questions appear (persistent tension only)
- What form they take (interrogative template)
- How many appear (one per persistent tension)

Questions are "emergent" relative to observations, but generation rules are still top-down.

### 3. Parallel type system

`EmergentQuestion` is local to the experiment file — not integrated with `src.question.Question`. Emergence demonstrated conceptually but not wired into the existing codebase architecture.

### 4. No question lifecycle

All emergent questions remain in `EMERGENT` state. No resolution, dormancy, or disappearance when tensions hypothetically resolve.

### 5. Mammal untested for question path

Input design gives Mammal one entity per behavior — cannot test question emergence for Mammal without different observations or lower thresholds. Absence of Mammal question is logically consistent but not a positive test of selective emergence.

### 6. Single tension per category pair

Only one behavior pair per category checkpoint. Multiple simultaneous tensions (e.g., three behaviors with sufficient members) untested.

---

## What Improved vs EXP-011

| Aspect | EXP-011 | EXP-012 |
|--------|---------|---------|
| Questions | Absent (World D) or primitive (World A/B) | Emergent from tensions |
| H98 test | Conceptual only | Constructive demonstration |
| Causal chain | observations → groups | observations → groups → tensions → questions |
| Question necessity | Questions not required for organization | Questions derived from organization |

EXP-012 significantly reduced the need for explicitly programmed `Question` objects at pipeline start and strengthened difference-first explanations (H96, H100).

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Adaptive persistence** | Tolerance or strength thresholds that change with observation history |
| **Emergent thresholds** | Groups and persistence criteria self-organize rather than fixed constants |
| **Question competition** | Multiple emergent questions compete for attention when tensions multiply |
| **Self-organized question generation** | Question form and timing emerge from tension dynamics, not fixed template |
| **Question disappearance** | Resolve or dissolve questions when tensions fall below threshold |
| **Integration with src.question** | Map `EmergentQuestion` → `Question` at emergence boundary |
| **Emergent communities** | Extend pipeline: tensions → questions AND communities |

---

## EXP-010 vs EXP-011 vs EXP-012 Control Progression

| Experiment | Control strategy | Primary finding |
|------------|------------------|-----------------|
| EXP-010 | Random null | Mechanism beats randomness |
| EXP-011 | Progressive reduction | Difference beats questions-as-primitive |
| EXP-012 | Emergence pipeline | Questions beat pre-instantiation |

Together: organization requires meaningful mechanism (EXP-010), difference is more primitive than questions (EXP-011), and questions can be outputs rather than inputs (EXP-012).

---

## The Redemption Arc

EXP-011 threatened the project name by showing questions are not fundamental. EXP-012 partially redeems "Question-Centric Intelligence" by reframing:

| EXP-011 framing | EXP-012 reframing |
|-----------------|-------------------|
| Questions unnecessary | Questions emergent |
| Difference-first | Difference → tension → question |
| Project name questionable | Project name = questions at center of output, not input |

Questions may be centric to what the system *produces* even if not centric to what it *starts with*.

---

## Overall Assessment

EXP-012 significantly reduced the need for explicitly programmed Question objects and strengthened difference-first explanations.

**Achieved:**

- Constructive proof of question emergence (H101)
- Persistence as necessary gate (H105)
- Compression interpretation supported (H103, H107)
- Causal reversal documented: tensions precede questions (H106)

**Still externally controlled:**

- Group minimum (2)
- Persistence minimum (2)
- Question template (fixed)
- Emergence timing (end of pipeline only)

**Reduction proved more dangerous than randomness (EXP-011). Emergence proved more constructive than reduction (EXP-012).** The research program now has:

1. A falsification control (EXP-010)
2. A necessity analysis (EXP-011)
3. An emergence construction (EXP-012)

Next stress tests should target the remaining imposed constants — especially persistence thresholds and question templates — to determine whether emergence survives further reduction or requires another layer of self-organization.

The initial sorting crash was a implementation defect, not a scientific finding. It was repaired without redesigning the experiment. All documented conclusions rest on post-fix execution.
