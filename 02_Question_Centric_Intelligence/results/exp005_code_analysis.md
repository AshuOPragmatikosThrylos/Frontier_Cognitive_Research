# EXP-005 Code Analysis

Post-experiment read-only analysis of attention economy.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-005)

---

## Files Involved

| File | Role in EXP-005 |
|------|-----------------|
| `experiments/exp005_attention_economy.py` | Experiment driver; attention, dormancy, revival logic |
| `src/curiosity_engine.py` | Entity question creation; debt update on re-observation |
| `src/world_model.py` | Category → behavior rules |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass (state, curiosity_debt, importance) |
| `src/observation.py` | Observation dataclass |

All attention economy logic lives in the experiment file. No `src/` modules modified. No merge API used.

---

## Execution Flow

### Phase 1: Initial Observations

Eight observations processed in fixed order:

1. Sparrow, Robin — normal (no questions)
2. Penguin, Ostrich, Emu, Kiwi — bird anomalies → four entity questions
3. Bat, Whale — mammal cross-category anomalies → two entity questions

Six entity questions created with `state=NEW`, `curiosity_debt=1.0`, `importance=1.0`.

### Phase 2: Community Questions

Three questions added (same structure as EXP-004):

| ID | Debt | Importance | Fitness |
|----|------|------------|---------|
| q-bird-flightlessness | 4.0 | 2.0 | 8.0 |
| q-mammal-capabilities | 2.0 | 2.0 | 4.0 |
| q-species-capabilities | 6.0 | 3.0 | 18.0 |

### Phase 3: Initial Allocation

`allocate_attention(repository, "initial")` — first competition.

### Phase 4: Revival Round 1 — Penguin

`observe_with_revival(..., "Penguin", ...)`:

1. Detect q-penguin was DORMANT
2. `observe()` → debt 1.0 → 3.0, engine briefly sets ACTIVE
3. Record q-penguin in REVIVED list
4. Reallocate — Penguin enters top 4, Bat displaced

### Phase 5: Revival Round 2 — Whale

`observe_with_revival(..., "Whale", ...)`:

1. Detect q-whale was DORMANT
2. `observe()` → debt 1.0 → 3.0
3. Record q-whale in REVIVED list
4. Reallocate — Whale fitness 3.0 ties Penguin; loses tie-break on id; remains DORMANT

### Phase 6: Reporting

Prints allocation log, states, dormant list, revived list, community statistics.

---

## Attention Budget Mechanism

```python
ATTENTION_BUDGET = 4
```

Finite pool of ACTIVE slots. With nine questions, at least five must be DORMANT after each allocation.

Budget applies to **all** questions in repository — entity and community questions compete equally.

No partial allocation. Each question is either ACTIVE or DORMANT after each round.

---

## Attention Allocation Strategy

```python
def fitness(question):
    return question.curiosity_debt * question.importance

ranked = sorted(eligible, key=lambda q: (-fitness(q), q.id))
active_ids = top ATTENTION_BUDGET by rank
```

| Component | Role |
|-----------|------|
| curiosity_debt | Memory signal — accumulated anomaly pressure |
| importance | Priority weight — set manually on community questions |
| fitness | Product determines rank |
| q.id | Deterministic tie-break (alphabetical) |

### Initial ranking

| Rank | ID | Fitness |
|------|-----|---------|
| 1 | q-species-capabilities | 18.0 |
| 2 | q-bird-flightlessness | 8.0 |
| 3 | q-mammal-capabilities | 4.0 |
| 4 | q-bat | 1.0 |
| 5–9 | entities (except bat) | 1.0 each |

Community questions with higher importance dominate early allocation.

---

## Dormancy Mechanism

```python
if question.id in active_ids:
    question.state = "ACTIVE"
else:
    question.state = "DORMANT"
```

- DORMANT questions **remain in repository** — not deleted
- All fields preserved: debt, observations, genealogy fields
- DORMANT is reassigned every allocation — not sticky across rounds unless fitness keeps question out of top 4

No ABANDONED, RESOLVED, or DEAD transitions in this experiment.

---

## Revival Mechanism

```python
was_dormant = existing.state == "DORMANT"
observe(...)  # updates debt via CuriosityEngine
if was_dormant:
    REVIVED.append(question_id)
allocate_attention(...)
```

Revival trigger: **re-observation of entity while DORMANT**.

Effects:
1. `times_encountered` increments
2. `curiosity_debt` increases by `DEBT_INCREMENT × times_encountered`
3. Question id appended to REVIVED list
4. Full reallocation runs

**Critical:** Revival is defined as "was DORMANT and received observation" — not "became ACTIVE". CuriosityEngine sets ACTIVE mid-observe, but `allocate_attention()` may immediately return question to DORMANT.

---

## Community Statistics

Computed per community after final allocation:

| Community | Members | Typical end state |
|-----------|---------|-------------------|
| Bird | 5 | 2 ACTIVE (penguin, bird-flightlessness), 3 DORMANT |
| Mammal | 3 | 1 ACTIVE (mammal-capabilities), 2 DORMANT (bat, whale) |
| Capability | 1 | 1 ACTIVE (species-capabilities) |

Debt accumulates unevenly across communities when entity questions in one community receive revival observations.

---

## Debt Accumulation

### Standard creation

New entity: `curiosity_debt = 1.0`

### Re-observation (CuriosityEngine)

```python
existing.curiosity_debt += DEBT_INCREMENT * existing.times_encountered
```

| Event | Penguin debt | Whale debt |
|-------|--------------|------------|
| First observation | 1.0 | 1.0 |
| Revival observation | 3.0 (1 + 2) | 3.0 (1 + 2) |

Community question debt set at creation, unchanged during experiment.

### Total repository debt (approximate final)

`3+1+1+1+4 + 1+3+2 + 6 = 22.0` (entity debts + community debts)

---

## State Transitions

| Question | Initial alloc | After Penguin revival | After Whale revival |
|----------|---------------|----------------------|---------------------|
| q-species-capabilities | ACTIVE | ACTIVE | ACTIVE |
| q-bird-flightlessness | ACTIVE | ACTIVE | ACTIVE |
| q-mammal-capabilities | ACTIVE | ACTIVE | ACTIVE |
| q-bat | ACTIVE | DORMANT | DORMANT |
| q-penguin | DORMANT | ACTIVE | ACTIVE |
| q-whale | DORMANT | DORMANT | DORMANT |
| q-ostrich, q-emu, q-kiwi | DORMANT | DORMANT | DORMANT |

Transitions observed: ACTIVE ↔ DORMANT (bidirectional across rounds).

---

## Presence or Absence of Randomness

| Source | Present? | Affects behavior? |
|--------|----------|-------------------|
| `random` | No | — |
| `uuid` | No | — |
| Deterministic ids | Yes | `q-{entity}` |
| Tie-break | Yes | Alphabetical by `q.id` |
| `time.time()` | Yes | Timestamps only |

**Fully deterministic.** Same observation order → same allocations, revivals, and final states.

---

## Heuristics Involved

| Heuristic | Rule |
|-----------|------|
| Budget size | Fixed at 4 |
| Fitness formula | debt × importance |
| Tie-break | Lower question id wins |
| Revival detection | Was DORMANT before observe |
| Revival list | Append if was DORMANT, regardless of post-allocation state |
| Dormancy | All non-top-4 after each allocation |
| Community debt stats | Sum debt per COMMUNITIES membership |

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed budget, fixed formula, fixed tie-breaks. Reproducible across runs.

**D — Emergent from interactions between simple rules** (partial)

Attention shifting (Bat → Penguin) emerges from debt competition without explicit rule naming winners.

### Key findings

| Property | Finding |
|----------|---------|
| Scarcity works | Budget forces dormancy without deletion |
| Revival works | Re-observation increases debt and triggers reallocation |
| Revival ≠ ACTIVE | Whale case exposes conceptual conflation |
| Memory vs attention | Debt and ACTIVE status decouple |
| Cycles | ACTIVE membership changes across rounds |
| vs EXP-004 | Static coexistence → dynamic competition |

### Conclusion

EXP-005 code implements a minimal attention economy with competition, dormancy, and revival. The architecture is simple and deterministic. The Whale ambiguity — revived but DORMANT — is architecturally faithful to the code (revival = observation received, not ACTIVE granted) and scientifically informative rather than defective.

Future experiments should separate memory (debt), importance (weight), and attention (ACTIVE allocation) as distinct subsystems.
