# EXP-004 Code Analysis

Post-experiment read-only analysis of question communities.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-004)

---

## Files Involved

| File | Role in EXP-004 |
|------|-----------------|
| `experiments/exp004_question_communities.py` | Experiment driver; graph and community logic |
| `src/curiosity_engine.py` | Entity question creation from anomalies |
| `src/world_model.py` | Category → behavior rules |
| `src/question_repository.py` | Question storage |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |

All graph, community, and relationship logic lives in the experiment file. No `src/` modules were modified. No merge API was invoked.

---

## Execution Flow

### Phase 1: Observations

Fixed observation order (same anomaly set as EXP-001–003):

1. Five normal observations — no questions created
2. Six anomalies — six entity questions via `CuriosityEngine.process_prediction_failure()`

Each entity question created with deterministic id `q-{entity}` and initial state `NEW`.

### Phase 2: Activate All Entity Questions

```python
for question in repository.get_all_questions():
    question.state = "ACTIVE"
```

All six entity questions set to ACTIVE before community questions are added.

### Phase 3: Add Community Questions

Three category/capability questions added separately — not via merge:

| ID | Text | Community |
|----|------|-----------|
| q-bird-flightlessness | Why don't some birds fly? | Bird |
| q-mammal-capabilities | Why do some mammals gain unexpected capabilities? | Mammal |
| q-species-capabilities | Why do species gain or lose capabilities? | Capability |

Each added via `add_community_question()` with `state = "ACTIVE"`.

### Phase 4: Build Graph

`build_graph()` wires typed relationships between existing question ids. No repository mutation beyond question storage.

### Phase 5: Reporting

Prints communities, relationship counts, question states, graph statistics.

---

## Community Formation Mechanism

Communities defined in experiment-local dict `COMMUNITIES`:

```python
COMMUNITIES = {
    "Bird": [q-penguin, q-ostrich, q-emu, q-kiwi, q-bird-flightlessness],
    "Mammal": [q-bat, q-whale, q-mammal-capabilities],
    "Capability": [q-species-capabilities],
}
```

Formation is **declarative**, not emergent from clustering algorithms:

1. Entity questions assigned to Bird or Mammal by category field from compression failure
2. Category questions placed in same community as their entities
3. Capability question forms bridge community connecting both domains

Unlike EXP-003, no merge or demotion step. Community membership is stable by construction.

---

## Relationship Types

### supports (6 edges)

Entity → category within same community.

| Source | Target |
|--------|--------|
| q-penguin | q-bird-flightlessness |
| q-ostrich | q-bird-flightlessness |
| q-emu | q-bird-flightlessness |
| q-kiwi | q-bird-flightlessness |
| q-bat | q-mammal-capabilities |
| q-whale | q-mammal-capabilities |

Semantically: investigating entity-specific questions strengthens the category-level question.

### depends_on (2 edges)

Category → capability bridge.

| Source | Target |
|--------|--------|
| q-bird-flightlessness | q-species-capabilities |
| q-mammal-capabilities | q-species-capabilities |

Semantically: the capability question cannot be fully pursued until domain abstractions are partially addressed.

### cooperates_with (3 edges)

Cross-community cooperation.

| Source | Target | Communities crossed |
|--------|--------|---------------------|
| q-bird-flightlessness | q-mammal-capabilities | Bird ↔ Mammal |
| q-bird-flightlessness | q-species-capabilities | Bird ↔ Capability |
| q-mammal-capabilities | q-species-capabilities | Mammal ↔ Capability |

Semantically: parallel investigation in one community aids progress in linked communities.

---

## Graph Statistics

| Metric | Value |
|--------|-------|
| Nodes | 9 |
| Edges | 11 |
| ACTIVE nodes | 9 |
| Communities | 3 |
| Cross-community edges | 5 |
| Avg edges per node | 1.22 |

### Edge breakdown

| Type | Count |
|------|-------|
| supports | 6 |
| depends_on | 2 |
| cooperates_with | 3 |
| **Total** | **11** |

---

## Community Statistics

| Community | Members | Internal edges |
|-----------|---------|----------------|
| Bird | 5 | 4 (supports: entities → category) |
| Mammal | 3 | 2 (supports: entities → category) |
| Capability | 1 | 0 |

Internal edges counted where both source and target belong to same community. Cross-community edges (5) connect clusters without merging them.

---

## Cross-Community Edges

Five edges span community boundaries:

**depends_on (2):**
- Bird → Capability (q-bird-flightlessness → q-species-capabilities)
- Mammal → Capability (q-mammal-capabilities → q-species-capabilities)

**cooperates_with (3):**
- Bird ↔ Mammal
- Bird ↔ Capability
- Mammal ↔ Capability

The Capability community has no internal edges but participates in all five cross-community connections — functioning as a bridge node.

---

## Question States

| State | Count | Questions |
|-------|-------|-----------|
| ACTIVE | 9 | All entity, category, and capability questions |
| PARTIALLY_RESOLVED | 0 | — |
| NEW | 0 | — (entity questions promoted to ACTIVE) |
| DORMANT | 0 | — |

**Contrast with EXP-003:** 1 ACTIVE, 8 PARTIALLY_RESOLVED.

No state transitions to demoted states occurred. Diversity preserved by design choice to avoid `merge_questions()`.

---

## Presence or Absence of Randomness

| Source | Present? | Affects behavior? |
|--------|----------|-------------------|
| `random` | No | — |
| `uuid` | No | — |
| Deterministic ids | Yes | `q-{entity}`, `q-bird-flightlessness`, etc. |
| `time.time()` | Yes | Timestamps only; not read by graph logic |

**Fully deterministic.** Fixed observation order, fixed community membership, fixed relationship wiring.

---

## Heuristics Involved

| Heuristic | Rule | Effect |
|-----------|------|--------|
| One question per entity | `q-{entity.lower()}` | Six independent entity questions |
| No merge | Merge API not called | No demotion, no absorption |
| Community assignment | Declarative COMMUNITIES dict | Three fixed clusters |
| supports wiring | Entity → category in same community | 6 internal strengthening edges |
| depends_on wiring | Category → capability | 2 upward dependency edges |
| cooperates_with wiring | Cross-community pairs | 3 cooperation edges |
| State promotion | All questions → ACTIVE | Full diversity preserved |
| Cross-community count | cooperates_with + depends_on only | 5 cross-community edges |

All heuristics explicit and deterministic.

---

## Overall Assessment

### Classification

**B — Heuristic but deterministic**

Fixed rules produce identical graph, communities, and states on every run.

**D — Emergent from interactions between simple rules** (partial)

Community structure is largely declarative, but cross-community bridge behavior emerges from relationship typing rather than merge hierarchy.

### Comparison with EXP-003

| Property | EXP-003 | EXP-004 |
|----------|---------|---------|
| Topology | Tree (3 levels) | Graph (3 communities) |
| ACTIVE at end | 1 | 9 |
| PARTIALLY_RESOLVED | 8 | 0 |
| Merge API used | Yes | No |
| Cross-domain links | Implicit (merge) | Explicit (cooperates_with, depends_on) |
| Diversity | Collapsed | Preserved |
| Failure mode | Over-abstraction | None observed |

### Key findings

| Property | Finding |
|----------|---------|
| Community stability | High — all questions ACTIVE |
| Graph vs tree | Graph preserves diversity; tree collapsed it |
| Bridge role | Capability community connects without absorbing |
| Relationship typing | supports, depends_on, cooperates_with sufficient for structure |
| Randomness | Absent |

### Conclusion

EXP-004 code implements a deliberate alternative to hierarchical merging. By replacing merge demotion with typed graph edges, the experiment preserves question diversity while still connecting entity, category, and capability levels. Communities appear significantly more stable than pure hierarchies for the Penguin World anomaly set.

The implementation is simple, deterministic, and aligned with research notes on question graphs (H17, H18) and symbiosis (H16, H19).
