# EXP-007 Results

Post-experiment summary for community speciation.

Date: 2026-06-21  
Experiment: EXP-007 Community Speciation

---

## Theme

Community Speciation

Test whether a single community can accumulate internal diversity and split into homogeneous subcommunities while preserving parent-child genealogy.

---

## Experiment Summary

Started with a single **Bird** community.

### Phase 1: Flying birds

Four flying observations (Sparrow, Robin, Eagle, Falcon) produced four entity questions with `observed_behavior="fly"`.

### Phase 2: Flightless birds

Four flightless anomalies (Penguin, Ostrich, Emu, Kiwi) produced four entity questions with `observed_behavior="not fly"`.

### Before split

| Metric | Value |
|--------|-------|
| Bird members | 8 |
| Behavior types | 2 |
| Groups | fly=4, not fly=4 |

Internal diversity exceeded split threshold.

### Split outcome

The Bird community split into:

- **Bird.Flying** — Sparrow, Robin, Eagle, Falcon
- **Bird.Flightless** — Penguin, Ostrich, Emu, Kiwi

### After split

| Community | Members | Behavior types | Parent |
|-----------|---------|----------------|--------|
| Bird | 0 | 0 | — |
| Bird.Flying | 4 | 1 (fly) | Bird |
| Bird.Flightless | 4 | 1 (not fly) | Bird |

Parent-child community relationships emerged. Parent community survived without members. Speciation reduced internal diversity within each child community from 2 types to 1.

---

## Supported Hypotheses

| Hypothesis | Evidence |
|------------|----------|
| **H64** — Communities can speciate | Bird split into Bird.Flying and Bird.Flightless |
| **H65** — Excessive internal diversity causes splits | Split triggered when two behavior groups each reached threshold (≥2 members) |

---

## Unexpected Observations

1. **Parent communities survived after losing all members.** Bird retained identity with empty `members` list but populated `children`.

2. **Child communities became internally homogeneous.** Each subcommunity contains only one observed behavior type.

3. **Speciation reduced diversity within communities.** Bird went from 2 behavior types to 0; each child holds 1 type exclusively.

4. **Parent-child community genealogies appeared.** Bird → Bird.Flying, Bird.Flightless with explicit `parent` and `children` links.

---

## Surprising Observations

1. **The parent Bird community became an organizational concept rather than a member container.** After split, Bird has no direct members but remains structurally meaningful as ancestor.

2. **Communities behaved similarly to biological species and scientific disciplines.** A broad taxon (Bird) subdivided into specialized subgroups when internal contradiction (fly vs not fly) exceeded tolerance.

3. **Speciation reduced internal tension.** Flying and flightless questions no longer share a community — the compression failure tension within Bird was resolved by partition.

---

## New Hypotheses

| Hypothesis | Statement |
|------------|-----------|
| **H67** | Parents need not contain members |
| **H68** | Speciation reduces internal tension |
| **H69** | Community genealogies are as important as question genealogies |
| **H70** | Evolutionary pressure may arise from internal contradictions |

H70 connects to EXP-010 themes: fly vs not fly within Bird is an internal contradiction driving speciation.

---

## Future Directions

- Investigate who decides when communities split
- Investigate self-organized speciation
- Study repeated speciation events
- Study community extinction
- Study community mergers

---

## Comparison Across Experiments

| Property | EXP-003 | EXP-006 | EXP-007 |
|----------|---------|---------|---------|
| Structure change | Vertical merge | Competition | Horizontal split |
| Diversity effect | Collapsed upward | Domain vs bridge | Partitioned internally |
| Parent survival | Questions demoted | Communities compete | Empty parent survives |
| Genealogy | Question parent_questions | None | Community parent/children |

---

## Conclusion

EXP-007 demonstrates that communities can speciate when internal diversity exceeds a threshold. Parent communities persist as organizational nodes; child communities become homogeneous. Speciation resolves internal contradiction without deleting questions — a third evolutionary operation alongside merge (EXP-002/003) and competition (EXP-006).

Splitting remains externally triggered by hardcoded rules — see `exp007_failures.md`.
