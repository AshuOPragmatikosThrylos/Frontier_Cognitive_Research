# EXP-007 Failures

Post-experiment failure analysis for community speciation.

Date: 2026-06-21  
Experiment: EXP-007 Community Speciation

---

## Failure Analysis

No mechanical failure was observed. Speciation triggered correctly, subcommunities formed, genealogy preserved, all questions retained. The Bird community split into Bird.Flying and Bird.Flightless as designed.

However, a **conceptual limitation** was identified: speciation is externally imposed rather than system-driven.

---

## Potential Issue

Community splitting currently depends on explicit thresholds.

```python
DIVERSITY_SPLIT_THRESHOLD = 2

def should_split(community):
    groups = behavior_groups(community)
    if len(groups) < 2:
        return False
    return all(len(ids) >= DIVERSITY_SPLIT_THRESHOLD for ids in groups.values())
```

Equivalent to:

```
if diversity > threshold:
    split()
```

This introduces hardcoded behavior.

---

## What This Means

### The system itself does not decide when to split

Split timing is determined by:

- A constant threshold set by the experimenter
- A single diversity axis (`observed_behavior`)
- A fixed check after a predetermined observation sequence
- Deterministic naming rules (`Flying` / `Flightless`)

The community does not "feel" internal tension and respond. The experiment observes diversity and applies a rule — similar to EXP-003's hardcoded stage-2 merge, but for splitting.

### Speciation remains externally imposed

Contrast with biological speciation:

| Biological | EXP-007 |
|------------|---------|
| Reproductive isolation emerges | Partition rule executes |
| Environmental pressure | Threshold constant |
| Gradual divergence | Single-step split |
| Fitness differences | Not used |

The outcome resembles speciation. The mechanism does not yet model evolutionary pressure.

---

## Related Limitations

1. **Single diversity axis.** Only `observed_behavior` considered. Other internal contradictions ignored.

2. **Binary naming.** Only fly → Flying, else → Flightless. Arbitrary for future behavior types.

3. **One split pass.** No repeated speciation, extinction, or merge-back.

4. **No competition or attention.** EXP-006 dynamics not integrated — split unrelated to fitness or budget.

5. **Flying questions manually created.** Asymmetric treatment vs flightless (engine path) — half the diversity is experimenter-seeded.

6. **Empty parent has no role.** Bird parent persists but performs no allocation, attention, or aggregation function yet.

---

## Potential Future Solutions

### Competition-driven splitting

Communities split when subgroups compete internally for attention — factions cannot coexist under budget.

### Debt-driven splitting

Split when curiosity debt diverges sharply between subgroups — one faction's anomalies dominate.

### Attention-driven splitting

Split when allocation repeatedly favors one subgroup within a community, starving the other.

### Emergent speciation

Replace explicit threshold with endogenous signals:

- Internal compression failure rate exceeds community coherence
- Cross-behavior `contradicts` edges exceed `supports` edges within community
- Community fitness variance exceeds split trigger derived from data

Goal: the system decides when to split, not the experimenter.

---

## Is This a Bug?

**No.** The code matches design intent. The issue is **maturity of the model** — speciation is a proof of concept, not self-organizing evolution.

EXP-007 succeeds at showing:
- Communities can split ✓
- Genealogy preserved ✓
- Homogeneous children emerge ✓
- Parent can survive empty ✓

EXP-007 does not yet show:
- Endogenous split decisions ✗
- Repeated evolutionary dynamics ✗
- Integration with attention economy ✗

---

## Overall Assessment

Speciation appears promising, but current mechanisms remain too handcrafted.

Reducing explicit control should become a major future objective.

The experiment series progression:

| EXP | Mechanism | Control level |
|-----|-----------|---------------|
| EXP-003 | Hierarchical merge | Hardcoded stage 2 |
| EXP-006 | Community competition | Hardcoded budget |
| EXP-007 | Community split | Hardcoded threshold |

Each adds ecological realism. Each relies on experimenter-defined rules. The next phase should derive split/merge/compete triggers from internal state — debt, attention, contradiction — rather than constants.

---

## Severity

| Dimension | Assessment |
|-----------|------------|
| Mechanical failure | None |
| Conceptual limitation | Significant — external control |
| Scientific value | High — proves speciation viable |
| Urgency for emergent rules | High |

---

## Conclusion

EXP-007 did not fail. It demonstrated community speciation with genealogy and tension reduction, while exposing that split decisions remain experimenter-imposed. The path forward is emergent speciation driven by internal contradiction (H70), attention scarcity (H46), and community competition (H55) — not `if diversity > threshold: split()`.

Handcrafted speciation is a stepping stone, not a destination.
