# EXP-014 Code Analysis

Post-experiment read-only analysis of question resurrection.

Date: 2026-06-22  
Scope: Question-Centric Intelligence implementation (EXP-014)

---

## Files Involved

| File | Role in EXP-014 |
|------|-----------------|
| `experiments/exp014_question_resurrection.py` | Full pipeline through extinction plus revival/resurrection phase |

No `src/` modules imported or used. Self-contained like EXP-012/013. Prior experiment files untouched.

New/expired relative to EXP-013:

| Addition | Purpose |
|----------|---------|
| `BIRD_REVIVAL_*` observation lists | Post-extinction observations reopening tension |
| `RESURRECTION_VITALITY = 3.0` | Vitality restored on resurrection |
| `resurrection_events` on `WorldState` | Log resurrection vs recreation outcomes |
| `RESURRECTED` state | Intermediate lifecycle state |
| `refresh_group_members()` | Update group membership after new observations |
| `reopen_tension()` | Mark tension unresolved, recalculate strength |
| `try_resurrect_or_recreate()` | Resurrection vs recreation decision |
| `recreate_question()` | Fallback recreation path |

---

## Execution Flow

### Phase 0: Constants

```python
RESURRECTION_VITALITY = 3.0
BIRD_TENSION_ID = "t-bird-fly-vs-not_fly"
BIRD_QUESTION_ID = "eq-bird-fly-vs-not_fly"
```

### Phase 1: `ingest_initial_observations()`

EXP-012/013 logic — 10 observations, Bird groups/tensions, Mammal observations.

### Phase 2: `process_extinction_lifecycle()`

```python
emerge_questions_from_tensions(state)
promote_emergent_questions(state)
resolve_tension(...)  # Bird tension
apply_vitality_decay(...) × 2  # Bird question → EXTINCT
```

### Phase 3: `process_revival()`

```python
register_observation(...) × 4  # revival birds
refresh_group_members(state, "Bird")
reopen_tension(state, BIRD_TENSION_ID)
try_resurrect_or_recreate(state, BIRD_TENSION_ID)
```

### Phase 4: Reporting

Histories, transitions, resurrection events, vitality, statistics, overall organization.

---

## Difference Formation

Initial formation identical to EXP-012/013 via `form_difference_groups()`.

Revival adds `refresh_group_members()` — updates existing group member lists from `category_index` without creating new groups:

```python
state.difference_groups[group_name].members = list(members)
```

After revival:

| Group | Members (count) |
|-------|-----------------|
| Bird.fly | Sparrow, Robin, Eagle, Falcon, Crow, Raven (6) |
| Bird.not_fly | Penguin, Ostrich, Emu, Kiwi, Chicken, Turkey (6) |

---

## Tension Detection

Initial detection via `record_tensions()` — same as EXP-012/013.

Revival uses `reopen_tension()` on existing tension record:

```python
tension.strength = float(min(len(group_a.members), len(group_b.members)))  # 6.0
tension.resolved = False
tension.resolution_note = ""
tension.persistent = tension.strength >= PERSISTENT_TENSION_MIN
```

Tension object preserved — same `t-bird-fly-vs-not_fly` id, state flipped from resolved to unresolved.

---

## Emergent Question Generation

`emerge_questions_from_tensions()` — unchanged from EXP-013.

Skips tension if any question already linked:

```python
if tension.id in {question.tension_id for question in state.lifecycle_questions.values()}:
    continue
```

This gate prevents duplicate emergence after first life — forces resurrection path on revival rather than second EMERGENT creation.

---

## Lifecycle States

Six states used (five from EXP-013 plus RESURRECTED):

| State | When |
|-------|------|
| EMERGENT | Initial creation |
| ACTIVE | Promoted (EMERGENT or RESURRECTED) |
| RESOLVED | Tension resolved, vitality above dormant |
| DORMANT | Vitality ≤ 1.0, > 0 |
| EXTINCT | Vitality ≤ 0 |
| RESURRECTED | Transient — between EXTINCT and ACTIVE on revival |

`apply_lifecycle_state()` preserves EMERGENT and RESURRECTED until explicit promotion:

```python
elif question.state in ("EMERGENT", "RESURRECTED"):
    pass
```

### Full Bird question lifecycle

| # | Event | State | Vitality |
|---|-------|-------|----------|
| 1 | Emerge | EMERGENT | 4.0 |
| 2 | Promote | ACTIVE | 4.0 |
| 3 | Resolve tension | RESOLVED | 2.0 |
| 4 | Decay | DORMANT | 1.0 |
| 5 | Decay | EXTINCT | 0.0 |
| 6 | Resurrect | RESURRECTED | 3.0 |
| 7 | Promote | ACTIVE | 3.0 |

---

## Extinction Mechanism

Identical to EXP-013 — vitality decay to zero:

```python
if question.vitality <= 0.0:
    question.state = "EXTINCT"
```

Question record **not deleted** from `lifecycle_questions` dict — enables later resurrection lookup.

---

## Resurrection Mechanism

`try_resurrect_or_recreate(state, tension_id)` — core EXP-014 logic:

```python
extinct_questions = [
    question for question in questions_for_tension(state, tension_id)
    if question.state == "EXTINCT"
]

if extinct_questions:
    question = extinct_questions[0]
    question.vitality = RESURRECTION_VITALITY
    question.state = "RESURRECTED"
    question.lifecycle_history.append("EXTINCT -> RESURRECTED ...")
    question.state = "ACTIVE"
    question.lifecycle_history.append("RESURRECTED -> ACTIVE (promoted)")
    # log resurrection event
else:
    recreate_question(state, tension)  # fallback
```

### Decision tree

```
tension persistent?
  no → no action
  yes → extinct question for tension exists?
    yes → RESURRECT (same id)
    no → RECREATE (new -recreated id)
```

Bird case: extinct question exists → **resurrection**.

---

## Identity Preservation

Resurrection preserves:

| Field | Preserved? |
|-------|------------|
| `id` | Yes — `eq-bird-fly-vs-not_fly` |
| `text` | Yes — unchanged |
| `tension_id` | Yes |
| `source_groups` | Yes |
| `lifecycle_history` | Yes — appended, not replaced |

Recreation (`recreate_question()`) would create:

```python
recreation_id = f"{question_id_for_tension(tension)}-recreated"
```

New id, empty history — **not invoked** in Bird run.

---

## History Accumulation

`lifecycle_history` is append-only across entire experiment:

- Pre-extinction: 5 entries
- Post-resurrection: 7 entries (+2)

Statistics report:

```python
f"history entries={previous_history_len} -> {len(question.lifecycle_history)}"
```

`extract_transitions()` parses history for transition-focused printing — includes resurrection transitions.

---

## Question Statistics

Expected final output:

| Metric | Value |
|--------|-------|
| Total questions | 1 |
| ACTIVE | 1 |
| EXTINCT | 0 |
| Resurrection events | 1 |
| Recreation events | 0 |
| Bird question history entries | 7 |

Note: RESURRECTED not in final state counts — transient state immediately promoted to ACTIVE.

---

## Reporting Functions

| Function | Output |
|----------|--------|
| `print_question_histories()` | Full append-only history |
| `print_lifecycle_transitions()` | Parsed transition list |
| `print_resurrection_events()` | Resurrection vs recreation log |
| `print_question_vitality()` | Current vitality and state |
| `print_question_statistics()` | Counts, resurrection/recreation tallies |
| `print_overall_organization()` | Pipeline summary, revival outcome |

---

## Presence of Randomness

None. Fully deterministic revival observations, fixed resurrection vitality, explicit decision branch on EXTINCT lookup.

---

## Overall Assessment

EXP-014 is structurally sound as a resurrection extension of EXP-013. It cleanly separates resurrection (identity preserved) from recreation (new identity) with an explicit decision branch.

Strengths:

- Resurrection vs recreation fork testable in one run
- Identity preservation auditable via id and history length
- Tension reopening without new tension object — parallel to question resurrection
- Append-only history supports H123/H124
- `emerge_questions_from_tensions()` skip logic forces resurrection when prior question exists

Weaknesses (see failures file):

- Resurrection rules externally defined
- `try_resurrect_or_recreate()` always resurrects if EXTINCT — no competition with recreation
- Single revival cycle only
- RESURRECTION_VITALITY fixed at 3.0
- Revival observations hardcoded

The code successfully implements EXP-013 future direction ("Investigate question resurrection") with a constructive demonstration: Bird question dies and returns as the same individual with extended history — not a copy.

Vitality trajectory across full experiment: 4.0 → 2.0 → 1.0 → 0.0 → 3.0 — death and partial restoration visible in scalar trace.
