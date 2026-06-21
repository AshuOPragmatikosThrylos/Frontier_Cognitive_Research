# EXP-007 Code Analysis

Post-experiment read-only analysis of community speciation.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-007)

---

## Files Involved

| File | Role in EXP-007 |
|------|-----------------|
| `experiments/exp007_community_speciation.py` | Experiment driver; community split logic |
| `src/curiosity_engine.py` | Flightless bird question creation |
| `src/world_model.py` | Bird → fly rule |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

All speciation logic lives in the experiment file. No `src/` modules modified.

---

## Execution Flow

### Phase 0: Initialize

- World model: `Bird → fly`
- Single community: `Bird` (empty members)
- `DIVERSITY_SPLIT_THRESHOLD = 2`

### Phase 1: Flying bird observations

For each of Sparrow, Robin, Eagle, Falcon:

1. `observe()` — prediction matches; no compression failure
2. `add_flying_bird_question()` — manual question creation with `observed_behavior="fly"`, state ACTIVE
3. Member appended to Bird community

Result: 4 flying members in Bird.

### Phase 2: Flightless bird observations

For each of Penguin, Ostrich, Emu, Kiwi:

1. `observe()` → `process_prediction_failure()` — creates entity question with `observed_behavior="not fly"`, state NEW
2. `assign_to_community("Bird", question_id)` — adds to Bird

Result: 8 total members in Bird (4 fly + 4 not fly).

### Phase 3: Diversity check

`diversity_metrics(Bird)`:

```python
behavior_types: 2
members: 8
groups: {fly: 4, not fly: 4}
```

`should_split(Bird)` → True (2 groups, each ≥ 2 members).

### Phase 4: Split

`split_community("Bird")`:

1. Group members by `observed_behavior`
2. Create `Bird.Flying` (behavior == "fly") and `Bird.Flightless` (else)
3. Set `parent` on children, append to `parent.children`
4. Clear `parent.members = []`

### Phase 5: Reporting

Print structures, genealogy, statistics, diversity, question states.

---

## Diversity Calculations

```python
def behavior_groups(community):
    group questions by observed_behavior

def diversity_metrics(community):
    behavior_types = len(groups)
    members = len(community.members)
    groups = {behavior: count}
```

| Community | behavior_types | groups |
|-----------|----------------|--------|
| Bird (pre-split) | 2 | fly=4, not fly=4 |
| Bird (post-split) | 0 | none |
| Bird.Flying | 1 | fly=4 |
| Bird.Flightless | 1 | not fly=4 |

Diversity metric is **count of distinct observed behaviors** among member questions.

---

## Split Mechanism

### Trigger condition

```python
def should_split(community):
    groups = behavior_groups(community)
    if len(groups) < 2:
        return False
    return all(len(ids) >= DIVERSITY_SPLIT_THRESHOLD for ids in groups.values())
```

Requires:
- At least 2 behavior types
- At least 2 members per type (`DIVERSITY_SPLIT_THRESHOLD = 2`)

### Split execution

```python
def split_community(parent_name):
    for behavior, member_ids in sorted(groups.items()):
        suffix = "Flying" if behavior == "fly" else "Flightless"
        child_name = f"{parent_name}.{suffix}"
        create child with parent=parent_name, members=member_ids
        parent.children.append(child_name)
    parent.members = []
```

Naming rule is deterministic:
- `fly` → `{Parent}.Flying`
- all else → `{Parent}.Flightless`

Single split pass — no recursive speciation in this experiment.

---

## Parent-Child Community Relationships

After split:

```
Bird (parent)
├── Bird.Flying (parent=Bird, 4 members)
└── Bird.Flightless (parent=Bird, 4 members)
```

| Community | parent | children | members |
|-----------|--------|----------|---------|
| Bird | none | Bird.Flying, Bird.Flightless | 0 |
| Bird.Flying | Bird | none | 4 |
| Bird.Flightless | Bird | none | 4 |

Parent survives as organizational node with empty member list (H67).

---

## Community Statistics

| Community | members | children | debt |
|-----------|---------|----------|------|
| Bird | 0 | 2 | 0.0 |
| Bird.Flying | 4 | 0 | 4.0 |
| Bird.Flightless | 4 | 0 | 4.0 |

Debt summed from member `curiosity_debt`. Parent Bird debt is 0 after members reassigned.

---

## Community Diversity Metrics

Post-split internal diversity drops to 1 behavior type per child community — speciation produces homogeneous subcommunities from heterogeneous parent.

Internal tension (fly vs not fly coexisting) eliminated at community level by partition.

---

## Question States

| Source | Initial state |
|--------|---------------|
| Flying birds (manual) | ACTIVE |
| Flightless birds (engine) | NEW |

Eight questions total. Flightless questions created via `process_prediction_failure` retain NEW unless explicitly updated. Flying questions explicitly set ACTIVE at creation.

No state changes during split — community membership changes; question objects unchanged.

---

## Presence or Absence of Randomness

| Source | Present? | Affects behavior? |
|--------|----------|-------------------|
| `random` | No | — |
| `uuid` | No | — |
| Deterministic ids | Yes | `q-{entity}` |
| Sorted group iteration | Yes | Deterministic child naming |
| Fixed observation order | Yes | Fly wave then flightless wave |

**Fully deterministic.**

---

## Heuristics Involved

| Heuristic | Rule |
|-----------|------|
| Split threshold | ≥2 behavior types, ≥2 members each |
| Diversity axis | `observed_behavior` field |
| Child naming | fly → Flying, else → Flightless |
| Parent after split | members cleared, children populated |
| Flying question creation | Manual (not compression failure) |
| Flightless questions | Via CuriosityEngine anomaly path |
| Split timing | Single check after all observations |

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Explicit threshold and naming rules produce identical speciation on every run.

**Partially externally imposed**

Split decision is hardcoded — not emergent from competition, debt, or attention (see failures doc).

### Key findings

| Property | Finding |
|----------|---------|
| Speciation works | Bird → Flying + Flightless |
| Parent survival | Empty parent persists as organizer |
| Diversity reduction | 2 types → 1 type per child |
| Genealogy | Community parent/children distinct from question genealogy |
| Question preservation | All 8 questions retained |
| Emergence | Limited — threshold is explicit |

### Comparison with question speciation (research notes)

Question reproduction/split (H20–H23) operates on individual questions. EXP-007 implements **community-level** speciation — a higher-order evolutionary operation.

### Conclusion

EXP-007 code demonstrates minimal viable community speciation with genealogy preservation. The mechanism is clear and deterministic but handcrafted. Parent-as-organizer (H67) and tension reduction (H68) are the primary scientific outputs. Emergent self-organized speciation remains future work.
