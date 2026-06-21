# EXP-014 Failures

Post-experiment failure analysis for question resurrection.

Date: 2026-06-22  
Experiment: EXP-014 Question Resurrection

---

## Failure Analysis

No mechanical failure was observed. Pipeline completed: Bird question emerged, traversed full lifecycle to EXTINCT, tension reopened on revival observations, extinct question resurrected with preserved identity, promoted to ACTIVE. Resurrection event logged. Recreation fallback not invoked.

The significant findings are methodological: resurrection is richer than recreation, but resurrection rules remain externally programmed.

---

## Current Limitation

### Resurrection rules remain externally defined

Revival sequence is hardcoded:

```python
def process_revival(state):
    register_observation(...)  # 4 fixed entities
    refresh_group_members(state, "Bird")
    reopen_tension(state, BIRD_TENSION_ID)
    try_resurrect_or_recreate(state, BIRD_TENSION_ID)
```

Equivalent to:

```
reopen tension → resurrect question
```

No observation automatically triggers reopening or resurrection — experimenter schedules revival phase after extinction.

### Identity preservation is explicitly programmed

Resurrection is not emergent identity recognition — it is a conditional branch:

```python
if extinct_questions:
    question = extinct_questions[0]  # reuse same object
    question.vitality = RESURRECTION_VITALITY
    ...
else:
    recreate_question(state, tension)  # new object
```

The system does not *discover* that identity should persist. It is **instructed** to prefer resurrection when EXTINCT record exists. H118 (memory preserves identity) is true operationally but achieved through explicit lookup, not self-organized continuity.

### Questions do not yet determine whether resurrection should occur

No question-level agency:

- Questions cannot refuse resurrection
- Questions cannot request resurrection
- Questions cannot compete with potential recreated replacements
- `RESURRECTION_VITALITY = 3.0` imposed externally — question does not earn vitality from tension strength on revival (contrast initial vitality = tension.strength on emergence)

Resurrection is a system decision applied **to** questions, not **by** questions.

---

## What Improved vs EXP-013

| Aspect | EXP-013 | EXP-014 |
|--------|---------|---------|
| Post-extinction dynamics | None — terminal EXTINCT | Resurrection to ACTIVE |
| Identity across death | Preserved in record | Preserved and reactivated |
| History | Frozen at extinction | Continues across cycles |
| Question count after revival | 1 (extinct) | 1 (active, same id) |
| Tension state | Resolved, static | Reopened, dynamic |
| Lifecycle states | 5 | 6 (+ RESURRECTED) |

EXP-013 established that questions die. EXP-014 establishes that death can reverse without new birth — significantly richer than recreation would have been.

---

## Additional Limitations

### 1. Single resurrection cycle

One extinction, one resurrection. Repeated cycles (EXTINCT again → resurrect again) untested. H123 (memory accumulates across cycles) supported for one cycle only.

### 2. Recreation path untested in Bird run

`recreate_question()` exists but Bird always had EXTINCT record — resurrection branch always taken. Recreation semantics unverified empirically in this experiment.

### 3. Fixed resurrection vitality

```python
RESURRECTION_VITALITY = 3.0
```

Not tied to reopened tension strength (6.0). Emergence uses `vitality = tension.strength`; resurrection uses fixed constant — asymmetric rules.

### 4. No competition between old and new questions

If both resurrection and recreation were candidates, system always prefers resurrection when EXTINCT exists. No tension between identities, no selection pressure.

### 5. Revival observations hardcoded

Crow, Raven, Chicken, Turkey — not derived from ecosystem dynamics. Same limitation class as `TENSION_RESOLUTIONS` and `DECAY_STEPS` in EXP-013.

### 6. RESURRECTED state is transient

Immediately promoted to ACTIVE — RESURRECTED never appears in final statistics. State exists in history only, not as sustained phase.

### 7. Parallel type system persists

`LifecycleQuestion` still local — not integrated with `src.question.Question`.

---

## Potential Future Directions

| Direction | Purpose |
|-----------|---------|
| **Adaptive resurrection** | Vitality on revival scales with tension strength or accumulated history |
| **Memory-based resurrection** | Resurrection probability/trigger derived from history length or past cycles |
| **Competition between old and new questions** | Recreate alongside extinct record; ecosystem selects which persists |
| **Self-organized identity persistence** | Identity continuity without explicit EXTINCT lookup branch |
| **Repeated cycles** | Multiple extinction-resurrection loops; test H123 across N cycles |
| **Observation-driven revival** | New observations automatically reopen tensions and trigger resurrection |
| **Community resurrection** | Apply same identity-preservation logic to difference groups or communities |

---

## Resurrection vs Recreation (Design Intent)

EXP-014 explicitly tests two hypotheses:

| Mechanism | Identity | History | Question count |
|-----------|----------|---------|----------------|
| Resurrection | Preserved | Appended | Unchanged |
| Recreation | New id | Fresh | Increments |

Bird outcome supports resurrection — stronger ecological metaphor (same organism returns) than recreation ( offspring replaces parent).

Future experiments should **force recreation path** (delete extinct record or use new tension id) to compare dynamics side-by-side.

---

## EXP-012 → EXP-014 Arc

| Experiment | Question arc |
|------------|----------------|
| EXP-012 | Birth (emergence) |
| EXP-013 | Death (extinction) |
| EXP-014 | Rebirth (resurrection) |

Complete episodic cycle demonstrated within three experiments. Missing: repeated cycles, inheritance, ecosystem-level memory.

---

## Overall Assessment

Question resurrection produced significantly richer dynamics than simple recreation and strengthened ecological interpretations of cognition.

**Achieved:**

- Identity-preserving resurrection (H117, H118)
- Death-memory coexistence extended to rebirth (H119)
- Resurrection cheaper than recreation (H120)
- Cyclical lifecycle (H121–H124)
- Explicit resurrection vs recreation fork

**Still externally controlled:**

- Revival timing and observations
- Reopen tension call
- Resurrection branch selection rule
- Resurrection vitality constant
- Promotion RESURRECTED → ACTIVE immediate

**Scientific value:**

EXP-014 transforms EXTINCT from terminal endpoint (EXP-013) to recoverable state. Questions are neither permanent (EXP-012 static) nor gone forever (EXP-013 terminal) — they are **cyclical episodic structures** with persistent identity and accumulating experience.

The organism metaphor (EXP-013) gains reincarnation: same id, new vitality, extended history. This is richer than recreation would provide — but the preference for resurrection is programmed, not evolved.

Next stress test: run multiple cycles without hardcoded revival phases — determine whether resurrection self-organizes or requires perpetual experimenter scheduling.

Resurrection rules must become endogenous before rebirth can be called a property of the question ecosystem rather than the experimenter's epilogue.
