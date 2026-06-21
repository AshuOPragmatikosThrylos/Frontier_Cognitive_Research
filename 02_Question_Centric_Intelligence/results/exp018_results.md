# EXP-018 Results

Post-experiment summary for memory cooperation.

Date: 2026-06-22  
Experiment: EXP-018 Memory Trace Cooperation

---

## Theme

Memory Cooperation

Test whether weak memory traces could cooperate by forming coalitions that compete with individual traces under limited reconstruction resources — extending EXP-017's competitive selection with alliance mechanics.

---

## Experiment Summary

Started from:

```
observations → differences → tensions → questions → extinction → memory traces
```

The experiment investigated whether weak memory traces could cooperate and form coalitions. Individuals and coalitions were intended to compete under limited reconstruction resources (`RECONSTRUCTION_BUDGET = 1`).

Three categories (Bird, Mammal, Insect) produced three extinct questions archived as memory traces:

| Trace | Question | Trace strength |
|-------|----------|----------------|
| `mem-eq-bird-fly-vs-not_fly` | `eq-bird-fly-vs-not_fly` | 1.00 |
| `mem-eq-mammal-fly-vs-swim` | `eq-mammal-fly-vs-swim` | 0.50 |
| `mem-eq-insect-fly-vs-crawl` | `eq-insect-fly-vs-crawl` | 0.50 |

On reintroduction, all three tensions reopened. Competition proceeded among individual traces.

**No coalitions formed.** Individual competition dominated. The strongest individual trace (`mem-eq-bird-fly-vs-not_fly`, strength 1.00) reconstructed. Mammal and Insect remained extinct.

| Question | Outcome |
|----------|---------|
| `eq-bird-fly-vs-not_fly` | LIVE — reconstructed (solo winner) |
| `eq-mammal-fly-vs-swim` | EXTINCT — lost competition |
| `eq-insect-fly-vs-crawl` | EXTINCT — lost competition |

The experiment **failed to demonstrate cooperation**. It therefore **strengthened the previously observed selection mechanism** from EXP-017: trace strength ranking under budget constraint determines reconstruction, without alliance-mediated rescue of weak memories.

---

## Supported Hypotheses

None strongly supported.

---

## Weakly Supported Hypotheses

| Hypothesis | Statement | Evidence |
|------------|-----------|----------|
| **H154** | Competition may be easier to obtain than cooperation | Individual selection reproduced; coalition path did not produce cooperative outcomes |
| **H155** | Cooperation may require richer mechanisms | Simple weak-trace grouping insufficient to alter EXP-017-style dominance |

---

## Hypotheses Not Supported

| Hypothesis | Statement | Reason |
|------------|-----------|--------|
| **H150** | Memory traces can cooperate | No coalitions formed; no cooperative reconstruction |
| **H151** | Coalitions compete with individuals | No coalitions entered competition |
| **H152** | Weak memories survive through alliances | Weak traces (Mammal, Insect) remained extinct |
| **H153** | Selection alone is insufficient | Selection alone reproduced EXP-017 outcome — sufficient without cooperation |

---

## Unexpected Observations

1. **No coalitions formed.** Despite coalition logic in the implementation, the completed run produced zero active coalitions at the competition phase.

2. **Selection remained dominant.** Outcome matched EXP-017 individual competition: strongest trace won, weaker traces did not reconstruct.

3. **The strongest trace reconstructed successfully.** Bird identity preserved via solo reconstruction — same winner as EXP-017.

4. **Competition proved robust.** Adding cooperation machinery did not destabilize or overturn the selection pattern observed in EXP-017.

---

## Surprising Observations

1. **Negative results strengthened confidence in previous experiments.** EXP-018 failed to overturn EXP-017; this increases trust in EXP-017's selection findings rather than contradicting them.

2. **The failure to observe cooperation increased confidence in selection.** H141–H144 (EXP-017) appear more durable than pre-EXP-018 estimates suggested.

3. **The experiment introduced resistance into the research program.** A deliberate attempt to add cooperation was falsified — the program now has a documented negative result, not only positive mechanism discoveries.

---

## Comparison: EXP-017 vs EXP-018

| Property | EXP-017 | EXP-018 |
|----------|---------|---------|
| Competition | Individual traces only | Individuals + intended coalitions |
| Coalitions | N/A | None formed |
| Winner | Bird (1.00) | Bird (1.00) |
| Losers | Mammal, Insect | Mammal, Insect |
| Outcome type | Positive (selection) | **Negative (cooperation failed)** |
| EXP-017 confidence | Established | **Strengthened** |

---

## Future Directions

- Investigate richer forms of cooperation
- Study larger ecosystems
- Study coalition prerequisites
- Investigate adaptive cooperation
- Determine whether cooperation requires additional mechanisms

---

## Conclusion

EXP-018 attempted to extend memory competition with trace cooperation and coalition formation. The experiment produced an important **negative result**: no coalitions formed, individual selection dominated, and the strongest trace reconstructed — reproducing EXP-017's outcome.

Cooperation was not demonstrated. Selection from EXP-017 was reinforced rather than replaced. H150–H153 are not supported; H154–H155 are weakly supported. The program gains falsification resistance: not every added mechanism produces new phenomena.
