# Kill Criteria

When to stop, pause, or archive this research program. Internal governance only.

---

## Conditions to Stop (Hard Stop)

Stop active development if **any** of:

1. **Three consecutive experiments** produce no new supported hypothesis and no falsification of prior claims — pure mechanism stacking without insight.

2. **Minimal world (EXP-011 D) + traces** reproduces all ranked S/S+ phenomena and remaining experiments only add notation — **redundant layer detected**.

3. **Threshold sensitivity audit** shows qualitative conclusions flip under ±20% parameter change across ≥3 core experiments — results are tuning artifacts.

4. **Independent replication attempt** (by human or agent) on same specs yields incompatible qualitative narrative and bug-free code — reproducibility failure.

5. **Research goal explicitly abandoned** — e.g. pivot to unrelated architecture with no carryover.

---

## Warning Signs (Soft Stop — Pause and Reassess)

| Signal | Action |
|--------|--------|
| Each experiment adds one dataclass field, no new comparison world | Pause; require falsification or new domain |
| Results docs repeat same Bird outcome without new surprise | Pause; change observation set |
| Hypothesis count grows; supported count flat | Pause; consolidate or reject |
| Confidence "Interesting" rises but "Useful" flat for 5+ experiments | Pause; seek external application |
| Implementation bugs (e.g. EXP-016 dict iteration) dominate discussion | Fix-only sprint; no new EXP until green |
| Chat/memory loss forces re-deriving basics repeatedly | Invest in memory docs (this folder); reduce scope |

---

## Dead-End Indicators

- **Metaphor lock-in:** Ecology vocabulary substitutes for testable claims.
- **Post-hoc hypotheses:** Every result "supports" something; nothing weakens or rejects.
- **Single world:** No experiment leaves Bird/Mammal before EXP-020 equivalent.
- **No controls:** New EXP without null/minimal world after EXP-010 precedent.
- **src/ vs local drift:** Two incompatible code paths without migration plan.
- **Breakthrough language** in commits/docs without matching confidence dashboard tier.

---

## Criteria for Declaring Success

Success **does not** require fundamental breakthrough. Sufficient success if:

1. **Published internal monograph** — story + timeline + hypotheses H1–Hn with honest status.

2. **Minimal reproducible stack** — difference → tension → optional question → trace, with one control world, documented and runnable.

3. **At least one falsification** documented (EXP-010 qualifies) and one **primitive pivot** documented (EXP-011 qualifies).

4. **Actionable design principles** for builders — e.g. "separate memory from attention," "resist over-merge," "test with stripped worlds."

5. **Clean archive** — git history, results per EXP, memory notes — usable by future self or collaborator in <2 hours onboarding.

---

## Criteria for Archiving the Project

Archive (preserve, stop extending) when:

- Success criteria met and no open question justifies >3 months more work.
- Kill criteria hard stop triggered.
- Effort shifts to **01_Darwinian_Memory** or **03_Compression_Failure_Engine** with explicit fork — QCI becomes read-only reference.
- Preprint attempt rejected twice for "toy only / no novelty" **and** no credible path to second domain or formalism.

**Archive means:** freeze experiments/, maintain notes/, tag final commit, write `ARCHIVE.md` with pointer to research_memory.md. **Not** delete repository.

---

## Current Status vs Kill Criteria

| Criterion | Status (Jun 2026) |
|-----------|-------------------|
| Consecutive empty experiments | No — EXP-011–015 high signal |
| Redundant layer | Possible — monitor post EXP-016 |
| Threshold sensitivity | **Not audited** — risk open |
| Independent replication | Not attempted |
| Warning: single domain | **Active** — Bird/Mammal throughout |
| Falsification culture | **Active** — EXP-010, EXP-011 |

**Verdict:** Continue with caution. Next priority: EXP-016 results doc + second domain or threshold audit before EXP-017.
