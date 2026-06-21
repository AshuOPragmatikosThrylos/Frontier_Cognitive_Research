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

EXP-012 through EXP-025 **descended the stack** without importing `src/`:
- Emergent questions from persistent tensions (EXP-012)
- Lifecycles and extinction (EXP-013)
- Resurrection on same object (EXP-014)
- Ecosystem memory traces and reconstruction after deletion (EXP-015)
- Perfect vs selective forgetting (EXP-016)
- Memory trace competition under budget (EXP-017)
- Memory cooperation attempt — **negative result** (EXP-018)
- Memory trace merging attempt — **negative result** (EXP-019)
- Cross-domain selection reproduction — **partial success** (EXP-020)
- Assumption removal — **selection falsified** (EXP-021)
- Persistence removal — **persistence falsified, organization survives** (EXP-022)
- Question removal — **questions falsified, organization survives** (EXP-023)
- Tension removal — **tensions falsified, organization survives** (EXP-024)
- Difference removal — **organization collapsed; difference bedrock confirmed** (EXP-025)

The arc: **questions-first → ecology → evolution → falsification → minimal worlds → difference-first → memory arc → cross-domain → reduction arc (021–025) → difference bedrock → growth from difference**.

---

## Major Phases

| Phase | Experiments | Theme |
|-------|-------------|-------|
| **I. Question objects** | EXP-001–002 | Compression failure, merge, genealogy |
| **II. Structure** | EXP-003–004 | Hierarchy vs communities vs graphs |
| **III. Scarcity** | EXP-005–006 | Attention economy, community competition |
| **IV. Evolution** | EXP-007–009 | Speciation, contradiction pressure, tolerance |
| **V. Falsification** | EXP-010–011 | Random controls, minimal worlds |
| **VI. Difference-first** | EXP-012–019 | Tensions, lifecycles, memory, competition, cooperation/merging (failed) |
| **VII. Cross-domain** | EXP-020 | Selection reproduction across four domains; boundary failure |
| **VIII. Assumption removal** | EXP-021 | Selection falsified; persistence elevated (then qualified) |
| **IX. Persistence removal** | EXP-022 | Persistence falsified; organization survives |
| **X. Question removal** | EXP-023 | Questions falsified; tension floor confirmed |
| **XI. Tension removal** | EXP-024 | Tensions falsified; difference floor confirmed |
| **XII. Difference removal** | EXP-025 | Organization collapsed; **reduction complete** |
| **VI. Growth from difference** | *(next)* | Constructive rebuild from bedrock |

---

## How the Project Evolved

1. **Construction era (EXP-001–009):** Each experiment added one mechanism and observed Bird/Mammal toy worlds.
2. **Comparison era (EXP-010+):** Control worlds ask *which* mechanisms matter.
3. **Reduction era (EXP-011):** Strip mechanisms until organization survives or dies.
4. **Reconstruction era (EXP-012–018):** Rebuild upward from differences, treating questions as transient phases and memory as ecosystem property.
5. **Resistance era (EXP-018–019):** Documented negative results — cooperation and merging falsified at memory layer.
6. **Cross-domain era (EXP-020):** Selection reproduced in 3/4 domains; Distributed Databases exposed theory boundary.
7. **Assumption-removal era (EXP-021):** Stripped rank/budget/strength ordering — selection vanished; persistence survived.
8. **Persistence-removal era (EXP-022):** Stripped stable memory — organization survived via fresh emergence.
9. **Question-removal era (EXP-023):** Removed question layer entirely — organization survived; tensions alone sufficient.
10. **Tension-removal era (EXP-024):** Removed tension layer entirely — organization survived; differences alone sufficient.
11. **Difference-removal era (EXP-025):** Removed difference layer — **organization collapsed**; difference confirmed as bedrock. **Reduction phase complete.**

Implementation style shifted: EXP-001–011 use `src/` modules; EXP-012–025 use self-contained experiment files with local dataclasses.

---

## Phase VI — Growth From Difference

**Status:** Current direction (post EXP-025)

Reduction arc (EXP-021–025) identified **difference** as bedrock. Next work is **constructive** — rebuild optional layers upward:

| Path | Question |
|------|----------|
| Difference → tensions | How do conflict summaries emerge from groups? |
| Difference → questions | How does compression reappear? |
| Difference → memory | When does persistence add value? |
| Difference → persistence | Identity continuity from bedrock |
| Difference → selection | Competition as derived, not primitive |
| Difference → intelligence | Full ecology from minimal base |

See `results/reduction_phase_summary.md`.

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
11. **Cooperation failed (EXP-018).** No coalitions formed; Bird won solo — EXP-017 selection reproduced.
12. **Merging failed (EXP-019).** Repeated co-activation; no abstractions — memory identity resistant; contrasts EXP-002 question merge.
13. **Cross-domain partial success (EXP-020).** Selection in Animals, Software Bugs, Scientific Theories; failed in Distributed Databases — recurrence without universality.
14. **Selection falsified (EXP-021).** Assumption removal destroyed selection motif; persistence invariant — one of most important experiments.
15. **Persistence falsified (EXP-022).** Transient traces; organization survived — difference+tension elevated.
16. **Questions falsified (EXP-023).** Question-Centric program removed questions — organization survived; tensions maintain structure.
17. **Tensions falsified (EXP-024).** Removed tension layer — organization survived; difference groups alone sufficient.
18. **Difference bedrock (EXP-025).** Removed difference layer — organization collapsed; raw observations insufficient. **Reduction complete.**

---

## Current Understanding

- **Difference / tension** may be more fundamental than questions (H74, H78, H100).
- **Questions** are compressed, episodic representations of persistent unresolved tension (H103, H107, H116).
- **Organization** (groups, communities, speciation) can exist with few or zero live questions (H115).
- **Memory** is distributed: traces, groups, tensions — not confined to question object references (H125, H132).
- **Identity** is relational (question_id + tension link), surviving extinction, deletion, and reconstruction (H121, H129).
- **Mechanisms matter**; randomness and aggregate stats are insufficient (H87, H92).
- **Forgetting** (EXP-016): selective decay prunes unused traces; core traces may survive at reduced strength.
- **Competition** (EXP-017): trace strength + budget determines who reconstructs — **qualified by EXP-021: assumption-imposed, not emergent.**
- **Cooperation** (EXP-018): **not demonstrated** — simple coalition rules insufficient; selection robust without alliances.
- **Merging** (EXP-019): **not demonstrated** — co-activation insufficient; trace identity highly stable (H161).
- **Questions ≠ memories** (H163): question merge works (EXP-002); memory merge does not under co-activation alone.
- **Cross-domain selection** (EXP-020): competition reproduces in 3/4 domains (H165); **same exported assumptions — qualified by EXP-021 (H176).**
- **Assumption removal** (EXP-021): selection not fundamental (H175); persistence > selection (H177, **qualified by EXP-022**).
- **Persistence removal** (EXP-022): persistence not fundamental (H178); difference+tension deeper (H186).
- **Question removal** (EXP-023): questions not fundamental (H187); tensions maintain org (H188) — **qualified by EXP-024**.
- **Tension removal** (EXP-024): tensions not fundamental (H194); differences maintain org (H198).
- **Difference removal** (EXP-025): differences fundamental (H202); raw obs insufficient (H203); bedrock confirmed (H204–H205).

---

## Current Worldview

Intelligence in this program is modeled as **ecological difference management**, with **difference as bedrock**:

- Observations create **differences** — **confirmed primitive** (EXP-025 collapse test).
- **Tensions** pair and rank group conflicts — **optional** (EXP-024).
- **Questions** compress tensions into live objects — **optional** (EXP-023).
- **Memory, persistence, selection** — optional optimizations (EXP-021–022).
- **Communities** evolve via pressure, tolerance, and speciation when contradictions exceed capacity.
- **Attention** allocates scarce processing; **memory** persists separately.
- **Traces** outlive question instances when persistence enabled (EXP-015); **optional** — organization survives without (EXP-022).
- **Persistence** optimizes identity continuity; **not fundamental** (EXP-022).
- **Fresh emergence** replaces reconstruction when memory removed (EXP-022).
- **Selection** gates expression only when rank/budget assumptions imported (EXP-017, EXP-021 World A) — **not emergent** (EXP-021 World B).
- **Cooperation** requires richer mechanisms than tested (EXP-018).
- **Merging** requires stronger coupling than co-activation (EXP-019).
- **Questions and memories obey different rules** (H163) — merge at question layer (EXP-002), resistance at trace layer.
- **Selection partially generalizes** (EXP-020) — reproduces across unrelated domains but requires preconditions (H168); **falsified as fundamental** (EXP-021, H175–H176).

We do **not** claim this is how real minds work. We claim the toy ecosystem produces coherent, falsifiable dynamics — including **destructive reduction** (EXP-021–025) ending in **bedrock confirmation** — that challenge answer-centric and question-primitive assumptions. **Hierarchy: Difference.** Everything above optional. **Reduction complete; growth phase begins.**
