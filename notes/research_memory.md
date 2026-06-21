# Research Memory — Chat Recovery Brief

**Purpose:** Paste or attach at start of a new session. Compact state of Frontier Cognitive Research / QCI program.

**Last updated:** 2026-06-22 (post EXP-016 implementation + crash fix; results doc pending)

---

## One-Sentence State

Toy deterministic ecology evolved from **question-first** (merge, communities) through **evolution and falsification** to **difference-first** (tensions, episodic questions, ecosystem memory traces, selective forgetting).

---

## Repository Map

```
Frontier_Cognitive_Research/
├── 01_Darwinian_Memory/          (parallel track, less active)
├── 02_Question_Centric_Intelligence/   ← ACTIVE
│   ├── experiments/exp001–exp016.py
│   ├── results/exp*_results.md   (exp016 results NOT yet written)
│   └── src/                      (EXP-001–011 only; EXP-012+ self-contained)
├── 03_Compression_Failure_Engine/
└── notes/                        ← THIS MEMORY LAYER (you are here)
```

**Workflow:** Discussion → Cursor experiment → git commit (QCI-NNN) → results docs when experiment "completed."

---

## Current Phase

**Phase VI: Difference-first memory stack** (EXP-012–016)

- EXP-012: emergent questions from tensions
- EXP-013: lifecycles + extinction
- EXP-014: resurrection (same object)
- EXP-015: deletion + trace reconstruction
- EXP-016: perfect vs selective forgetting — **implemented, not formally resulted; clutter_count bug fixed**

---

## Current Direction

1. Document EXP-016 results (`exp016_results.md` etc.) when user marks experiment complete.
2. Avoid adding mechanisms without control/minimal world.
3. Strong candidate next step: **second domain** OR **threshold sensitivity audit** (see kill_criteria.md).
4. Do not rerun/modify prior experiments unless explicitly asked.

---

## Narrative (30 seconds)

Built question repository with merge and communities. Hierarchy over-merged (EXP-003). Graphs/communities stable (EXP-004). Attention scarcity separates memory from focus (EXP-005). Communities evolve via contradiction pressure and tolerance (EXP-008–009). Random controls prove mechanisms matter (EXP-010). **World D partitions Bird with differences only** (EXP-011) — pivot. Rebuilt stack: tension → emergent question → extinct → trace → reconstruct (EXP-012–015). Forgetting prunes clutter in design (EXP-016).

---

## Tier Rankings (headline)

| Tier | Experiments |
|------|-------------|
| **S++** | EXP-010, EXP-011 |
| **S+** | EXP-003, EXP-008, EXP-012, EXP-015 |
| **S** | EXP-004, EXP-009, EXP-013, EXP-014 |
| **A** | EXP-001, 002, 005–007, 016 |

Full rationale: `notes/tier_rankings.md`

---

## Confidence Dashboard (snapshot)

| | % |
|--|---|
| Interesting Framework | 78 |
| Useful Framework | 52 |
| Preprint-worthy Narrative | 38 |
| New Cognitive Principles | 45 |
| Cross-domain Potential | 35 |
| Fundamental Breakthrough | 8 |
| Dead-end Risk | 28 |

Full history: `notes/confidence_dashboard.md`

---

## Most Important Hypotheses (now)

| ID | Claim | Status |
|----|-------|--------|
| H100 | Cognition from difference management | Strengthened (EXP-011) |
| H104 | Questions not primitive | Supported (EXP-012) |
| H115 | Organization mostly non-question | Supported (EXP-013) |
| H125 | Memory is ecosystem property | Supported (EXP-015) |
| H129 | Identity relational not material | Supported (EXP-015) |
| H2 | Questions primary objects | **Weak** — founding tension |

Full H1–H132: `notes/major_hypotheses.md`

---

## Open Questions (top 5)

1. Primitive operation: difference vs tension vs question?
2. Scale beyond Bird/Mammal?
3. Memory unit: trace vs object vs group?
4. EXP-016 outcomes — forgetting vs identity?
5. Any computational advantage vs baselines?

Full list: `notes/open_questions.md`

---

## Kill Criteria (headline)

**Stop if:** 3 barren experiments; threshold audit fails; independent replication diverges.

**Warning:** still single domain; EXP-016 undocumented.

Full: `notes/kill_criteria.md`

---

## Shared Observation Sequence (EXP-012–016)

- 4 bird fly, 4 bird not fly, 2 mammal (bat fly, whale swim)
- Reintro: crow/raven fly; chicken/turkey not fly
- Bird tension: `t-bird-fly-vs-not_fly`; question: `eq-bird-fly-vs-not_fly`

---

## Git / Commit Convention

- Implementation: `QCI-NNN Implement EXP-0XX ...`
- Results: `QCI-NNN Record EXP-0XX ...`
- Latest: QCI-026 (EXP-016 impl + clutter_count fix)
- Commit only when user asks; push only when user asks.

---

## Rules for New Sessions

- Do NOT modify code/experiments/src unless asked.
- Do NOT rerun experiments unless asked.
- Results docs only when user says experiment completed.
- Deterministic: no randomness, LLM, embeddings, vector DB in experiments.
- Read `notes/research_memory.md` + relevant `results/exp*_results.md` before continuing work.

---

## Deep Dives (when needed)

| File | Content |
|------|---------|
| `notes/project_story.md` | Full narrative, phases, surprises, worldview |
| `notes/timeline_of_discoveries.md` | Per-EXP one-liners |
| `notes/preprint_outline.md` | Internal paper sketch (not claims) |
| `02_Question_Centric_Intelligence/notes/research_journal.md` | Discussions 001–010, H1–H37 origins |

---

## Active Tension in the Research

**Founding premise (questions first) vs empirical pivot (differences first).** The project is most honest when it holds both: questions are *useful derived objects*, not proven cognitive primitives.
