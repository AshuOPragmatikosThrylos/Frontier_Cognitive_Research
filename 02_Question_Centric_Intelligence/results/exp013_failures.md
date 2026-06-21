# EXP-013 Failures

Post-experiment failure analysis for question lifecycles and extinction.

Date: 2026-06-22  
Experiment: EXP-013 Question Extinction

---

## Failure Analysis

No mechanical failure was observed. Pipeline completed full lifecycle: Bird question emerged, activated, resolved, decayed, and went extinct. Difference groups and resolved tension preserved. Lifecycle history recorded all transitions.

The significant findings are methodological and conceptual — lifecycle richness exceeds static Question objects, but vitality and transition rules remain externally controlled.

---

## Current Limitation

### Lifecycle transitions depend on explicit vitality thresholds

State assignment in `apply_lifecycle_state()`:

```python
if question.vitality <= 0.0:
    question.state = "EXTINCT"
elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
    question.state = "DORMANT"
elif tension_resolved:
    question.state = "RESOLVED"
```

Equivalent to:

```python
if vitality <= threshold:
    state transition occurs
```

Three experimenter-imposed constants govern all transitions:

| Constant | Value | Effect |
|----------|-------|--------|
| `RESOLUTION_VITALITY_REDUCTION` | 2.0 | Vitality drop on tension resolution |
| `DORMANT_VITALITY_THRESHOLD` | 1.0 | Boundary between RESOLVED and DORMANT |
| `DECAY_VITALITY_REDUCTION` | 1.0 | Vitality drop per decay step |

Same limitation class as `PRESSURE_SPLIT_LIMIT` (EXP-008/009), `DIFFERENCE_MIN_PER_GROUP` (EXP-011), and `PERSISTENT_TENSION_MIN` (EXP-012).

---

## Question Death Remains Externally Controlled

Extinction required:

1. Experimenter-defined `TENSION_RESOLUTIONS` list (when resolution occurs)
2. Experimenter-defined `DECAY_STEPS` list (when decay occurs, which question)
3. Fixed vitality reductions (how much each event costs)

Questions do not determine their own vitality. They passively receive reductions when external events fire. No endogenous decay, no question-initiated resolution, no competition for vitality.

Bird extinction path was **designed**:

```
vitality 4.0 - 2.0 (resolution) - 1.0 (decay) - 1.0 (decay) = 0.0
```

Change any constant or step count and extinction may not occur — demonstrating external control.

---

## What Improved vs EXP-012

| Aspect | EXP-012 | EXP-013 |
|--------|---------|---------|
| Question states | EMERGENT only | Five-state lifecycle |
| Vitality | Absent | Tracked and reduced |
| Tension resolution | Not modeled | Resolution → vitality loss |
| Question disappearance | Not modeled | DORMANT → EXTINCT |
| Memory after death | N/A | Groups, tensions, history preserved |
| Ecological metaphor | Emergence only | Birth, life, death |

EXP-012 asked whether questions can emerge. EXP-013 asks whether they can die. Answer: yes, with externally scheduled events.

---

## Additional Limitations

### 1. Resolution not observation-driven

`TENSION_RESOLUTIONS` is a hardcoded list — resolution does not emerge from new observations explaining the conflict. The "niche specialization" note is experimenter narrative, not computed from data.

### 2. Decay steps hardcoded by question ID

```python
DECAY_STEPS = ["eq-bird-fly-vs-not_fly", "eq-bird-fly-vs-not_fly"]
```

Which questions decay and how many times is predetermined — not a general rule (e.g., "all RESOLVED questions decay each tick").

### 3. No resurrection

EXTINCT is terminal in this implementation. `apply_vitality_decay()` skips extinct questions. No pathway back to ACTIVE if tension re-emerges.

### 4. Single question lifecycle

Only Bird question traversed lifecycle. No multi-question competition, no simultaneous lifecycles, no ecosystem-level birth/death balance.

### 5. Statistics show final state only

`print_question_statistics()` counts current states — intermediate EMERGENT/ACTIVE/RESOLVED/DORMANT counts at end are zero except EXTINCT. Transient states visible only in lifecycle history, not aggregate metrics.

### 6. Parallel type system persists

`LifecycleQuestion` remains local — not integrated with `src.question.Question` lifecycle fields.

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Adaptive vitality** | Vitality thresholds change with ecosystem experience |
| **Ecosystem memory** | Aggregate extinct question history into system-level recall |
| **Question resurrection** | EXTINCT → EMERGENT if tension re-emerges or vitality restored |
| **Self-organized lifecycles** | Transitions driven by observation flow, not hardcoded events |
| **Repeated birth-death cycles** | Same category produces multiple question generations |
| **Observation-driven resolution** | New observations trigger resolution when they explain conflict |
| **General decay rule** | All RESOLVED questions lose vitality per tick, not named IDs |

---

## EXP-012 → EXP-013 Progression

| Experiment | Question model | Key question |
|------------|----------------|--------------|
| EXP-012 | Emergent, static EMERGENT | Can questions arise from differences? |
| EXP-013 | Lifecycle, ends EXTINCT | Can questions die? |

Remaining arc:

| Future | Key question |
|--------|--------------|
| Resurrection | Can questions return? |
| Repeated cycles | Is birth-death equilibrium stable? |
| Ecosystem memory | What does the system know after all questions die? |

---

## The Organism Metaphor

EXP-013 strengthens ecological interpretation but risks over-metaphorizing:

- Questions "die" but are not deleted — records persist
- Vitality is a scalar, not energy conservation
- Decay is scheduled, not metabolic

The metaphor is **heuristically useful** (H109–H111) but **mechanically imposed**. Future work should test whether lifecycle richness survives removal of hardcoded events.

---

## Overall Assessment

Question lifecycles appear significantly richer than static Question objects and strengthen ecological interpretations of cognition.

**Achieved:**

- Full five-state lifecycle demonstrated (H109)
- Resolution-vitality coupling (H110)
- Extinction without memory destruction (H111, H112)
- Transient question interpretation (H113–H116)

**Still externally controlled:**

- Vitality initial value (= tension strength — inherited from EXP-012)
- All reduction amounts and thresholds
- Resolution timing and narrative
- Decay timing and target selection
- State transition priority order

**Scientific value:**

EXP-013 completes an emergence-mortality pair with EXP-012. Together they frame questions as **episodes** within a difference-based ecosystem rather than permanent primitives. The ecosystem can outlive its questions — a finding incompatible with question-centric models that treat questions as the primary persistent structure.

Next stress test: remove hardcoded `TENSION_RESOLUTIONS` and `DECAY_STEPS` — determine whether lifecycles self-organize or collapse without experimenter scheduling.

Vitality thresholds must become adaptive or emergent before question death can be called endogenous rather than scripted.
