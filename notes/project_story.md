# Project Story

## What This Is

**Frontier Cognitive Research** is an external memory system for exploring alternative intelligence architectures. The active program lives in **02_Question_Centric_Intelligence**: a toy ecosystem where cognition is modeled as the management of unresolved structure — questions, communities, tensions, and memory — rather than as fact storage.

Workflow: discussion → research notes → deterministic Python experiments → git history → next discussion. No LLMs, embeddings, or randomness inside experiments.

---

## Overall Narrative

The project began with a contrarian premise: **unresolved anomalies matter more than accumulated answers**. Early work asked whether questions could be first-class entities with lifecycles, debt, and genealogy — like organisms in an ecology.

EXP-001 through EXP-004 built a **question repository**: compression failures spawn questions; questions merge, form hierarchies, and cluster into communities. EXP-003 revealed a failure mode — hierarchical merging **over-compressed** diversity. EXP-004 recovered stability through **parallel communities and graphs** instead of trees.

EXP-005 and EXP-006 introduced **scarcity**: attention budgets at question and community levels. Memory (debt) and attention (ACTIVE slots) diverged. Abstract bridge communities proved fragile under competition.

EXP-007 through EXP-009 shifted from questions toward **communities as evolutionary units**. Internal diversity triggers speciation; contradiction **pressure** (not just diversity thresholds) drives splits; **adaptive tolerance** gives communities personality — rigid Bird speciates, flexible Mammal absorbs.

EXP-010 introduced **falsification**: random control worlds produce entropy, not semantic organization. Same observations, different mechanisms → different outcomes.

EXP-011 was the **inversion point**. World D (difference-only) reproduced Bird partitioning **without questions, communities, pressure, or tolerance**. The primitive operation may be **difference management**, with questions as derived compressions.

EXP-012 through EXP-016 **descended the stack** without importing `src/`:
- Emergent questions from persistent tensions (EXP-012)
- Lifecycles and extinction (EXP-013)
- Resurrection on same object (EXP-014)
- Ecosystem memory traces and reconstruction after deletion (EXP-015)
- Perfect vs selective forgetting (EXP-016, implemented; results pending formal documentation)

The arc: **questions-first → ecology → evolution → falsification → minimal worlds → difference-first → memory and forgetting**.

---

## Major Phases

| Phase | Experiments | Theme |
|-------|-------------|-------|
| **I. Question objects** | EXP-001–002 | Compression failure, merge, genealogy |
| **II. Structure** | EXP-003–004 | Hierarchy vs communities vs graphs |
| **III. Scarcity** | EXP-005–006 | Attention economy, community competition |
| **IV. Evolution** | EXP-007–009 | Speciation, contradiction pressure, tolerance |
| **V. Falsification** | EXP-010–011 | Random controls, minimal worlds |
| **VI. Difference-first** | EXP-012–016 | Tensions, lifecycles, memory, forgetting |

---

## How the Project Evolved

1. **Construction era (EXP-001–009):** Each experiment added one mechanism and observed Bird/Mammal toy worlds.
2. **Comparison era (EXP-010+):** Control worlds ask *which* mechanisms matter.
3. **Reduction era (EXP-011):** Strip mechanisms until organization survives or dies.
4. **Reconstruction era (EXP-012–016):** Rebuild upward from differences, treating questions as transient phases and memory as ecosystem property.

Implementation style shifted: EXP-001–011 use `src/` modules; EXP-012–016 use self-contained experiment files with local dataclasses.

---

## Important Surprises

1. **Merge ≠ deduplication (EXP-002).** True merge grows the repository and preserves genealogy; EXP-001's in-place abstraction hid this.
2. **Hierarchy collapse (EXP-003).** One ACTIVE meta-question starved the ecology — abstraction can destroy diversity.
3. **Whale revival without ACTIVE (EXP-005).** Memory signal (debt) ≠ attention allocation.
4. **Capability dormancy (EXP-006).** Bridge abstractions lose under domain-specific anomaly pressure.
5. **Empty parent communities (EXP-007).** Speciation leaves shell parents with genealogical role but no members.
6. **Identical debt, different organization (EXP-010).** Summary statistics don't predict semantic structure.
7. **World D wins (EXP-011).** Bird partitions from behavior differences alone — no question machinery required.
8. **Organization outlives questions (EXP-013).** At extinction: groups and tensions persist; zero live questions.
9. **Identity without objects (EXP-015).** Question deleted; trace retains id and history; reconstruction continues narrative.
10. **Dict iteration bug (EXP-016).** `clutter_count()` iterated keys not values — type error, not corruption of memory model.

---

## Current Understanding

- **Difference / tension** may be more fundamental than questions (H74, H78, H100).
- **Questions** are compressed, episodic representations of persistent unresolved tension (H103, H107, H116).
- **Organization** (groups, communities, speciation) can exist with few or zero live questions (H115).
- **Memory** is distributed: traces, groups, tensions — not confined to question object references (H125, H132).
- **Identity** is relational (question_id + tension link), surviving extinction, deletion, and reconstruction (H121, H129).
- **Mechanisms matter**; randomness and aggregate stats are insufficient (H87, H92).
- **Forgetting** (EXP-016 design): selective decay prunes unused traces; core traces may survive at reduced strength.

---

## Current Worldview

Intelligence in this program is modeled as **ecological difference management under scarcity**:

- Observations create **differences**.
- Persistent differences create **tensions**.
- Tensions compress into **questions** (temporary, lifecycle-bound).
- **Communities** evolve via pressure, tolerance, and speciation when contradictions exceed capacity.
- **Attention** allocates scarce processing; **memory** persists separately.
- **Traces** outlive question instances; **forgetting** prevents clutter accumulation.

We do **not** claim this is how real minds work. We claim the toy ecosystem produces coherent, falsifiable dynamics that challenge answer-centric and question-primitive assumptions — and that the stack now points toward **tension-and-memory-first** models rather than question-first models.
