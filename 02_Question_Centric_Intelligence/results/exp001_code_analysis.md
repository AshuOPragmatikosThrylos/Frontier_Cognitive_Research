# EXP-001 Code Analysis

Post-experiment read-only analysis of how EXP-001 Penguin World produced its observed behavior.

Date: 2026-06-21  
Scope: Question-Centric Intelligence implementation (EXP-001)

---

## Files Analyzed

| File | Role |
|------|------|
| `experiments/exp001_penguin_world.py` | Experiment driver; feeds observations in fixed order |
| `src/world_model.py` | Category → behavior rules; prediction |
| `src/curiosity_engine.py` | Prediction failure handling; question creation and update |
| `src/question_repository.py` | Question storage; merge API (unused in EXP-001) |
| `src/question.py` | Question dataclass |
| `src/observation.py` | Observation dataclass |
| `results/exp001_results.md` | Prior experiment notes |

---

## Search Results (Randomness)

Searched all files under `02_Question_Centric_Intelligence/` for:

`random`, `random()`, `choice()`, `shuffle()`, `sample()`, `numpy.random`, `secrets`, `uuid`, `hash`

| Term | Found | File | Influences question generation? |
|------|-------|------|--------------------------------|
| `random` | No | — | — |
| `random()` | No | — | — |
| `choice()` | No | — | — |
| `shuffle()` | No | — | — |
| `sample()` | No | — | — |
| `numpy.random` | No | — | — |
| `secrets` | No | — | — |
| `hash` | No | — | — |
| `uuid` | **Yes** | `src/curiosity_engine.py` | **No** — used only for `id` fields |

### uuid usage

```python
id=str(uuid.uuid4())[:8]   # observation id (line 28)
id=str(uuid.uuid4())[:8]   # question id (line 54)
```

`uuid.uuid4()` generates random identifiers. These IDs differ on each run but do not affect:

- Which questions are created
- Question text
- Question keys or deduplication
- Curiosity debt
- State transitions
- Merge or generalization logic

### time.time()

`curiosity_engine.py` also uses `time.time()` for observation timestamps. This varies per run but is not read by any decision logic.

### Conclusion on randomness

**No randomness influences question generation, merging, debt, or state assignment.**  
Only non-functional identifiers (question id, observation id, timestamp) vary between runs.

---

## Execution Flow: Flightless Birds → Generalized Question

### Input sequence (from `exp001_penguin_world.py`)

After five normal observations (no failures), anomalies are processed in order:

1. Penguin — Bird — not fly  
2. Ostrich — Bird — not fly  
3. Emu — Bird — not fly  
4. Kiwi — Bird — not fly  

### Step 1: `exp001_penguin_world.py` → `observe()`

For each tuple `(entity, category, behavior)`:

1. `expected = world_model.predict(category)`  
   - For category `"Bird"`, `WorldModel.rules["Bird"]` → `"fly"`

2. `behavior = behavior.lower()` → `"not fly"`

3. Check: `expected and behavior != expected`  
   - `"fly"` is truthy; `"not fly" != "fly"` → **True**

4. Calls `engine.process_prediction_failure(entity, category, behavior, content)`

Normal observations (Sparrow flies, etc.) pass the check and **do not** call the engine.

### Step 2: `world_model.py`

- `predict("Bird")` returns `"fly"` from the rule `Bird → fly`
- No mutation occurs during observation processing
- World model is read-only in this experiment

### Step 3: `curiosity_engine.py` → `process_prediction_failure()`

Shared logic for all four bird anomalies:

1. `observed = "not fly"`
2. `expected = world_model.predict("Bird")` → `"fly"`
3. Branch: `expected and observed != expected` → **rule-violation path**
4. `question_key = f"{category}:{expected}"` → **`"Bird:fly"`** (same key for all four)
5. Initial text template: `f"Why doesn't {entity} {expected}?"`

#### Penguin (first anomaly)

- `_question_keys` has no entry for `"Bird:fly"`
- Creates new `Question`:
  - `text`: `"Why doesn't Penguin fly?"`
  - `curiosity_debt`: `1.0` (`DEBT_INCREMENT`)
  - `times_encountered`: `1`
  - `state`: `"NEW"`
- Stores mapping: `_question_keys["Bird:fly"] = question.id`
- Adds question to repository

#### Ostrich (second anomaly)

- `_question_keys["Bird:fly"]` exists → **reuse same question**
- `times_encountered`: `1 → 2`
- `curiosity_debt`: `1.0 + (1.0 × 2) = 3.0`
- `state`: `"ACTIVE"`
- **Generalization trigger:** `times_encountered >= 2`  
  - `text` rewritten to: `"Why don't some birds fly?"`
- Appends new observation id to `related_observations`

#### Emu (third anomaly)

- Same question via `"Bird:fly"`
- `times_encountered`: `2 → 3`
- `curiosity_debt`: `3.0 + (1.0 × 3) = 6.0`
- `state`: `"ACTIVE"`
- Text remains `"Why don't some birds fly?"`

#### Kiwi (fourth anomaly)

- Same question via `"Bird:fly"`
- `times_encountered`: `3 → 4`
- `curiosity_debt`: `6.0 + (1.0 × 4) = 10.0`
- `state`: `"ACTIVE"`
- Text remains `"Why don't some birds fly?"`

### Step 4: `question_repository.py`

- `add_question()` called once (Penguin)
- Subsequent anomalies only **update** the existing object via `get_question()`
- **`merge_questions()` is never called** in EXP-001

### Step 5: `question.py`

Passive data container. No logic. Fields mutated in place by `CuriosityEngine`.

### Flow diagram

```
Penguin (Bird, not fly)
  observe() → predict("Bird")="fly" → mismatch
  → process_prediction_failure()
  → key "Bird:fly" → NEW question "Why doesn't Penguin fly?" debt=1

Ostrich (Bird, not fly)
  → key "Bird:fly" exists → update same question
  → times_encountered=2 → debt=3 → state=ACTIVE
  → text generalizes → "Why don't some birds fly?"

Emu, Kiwi
  → same key → debt accumulates → text unchanged
  → final: debt=10, times_encountered=4, state=ACTIVE
```

---

## Question Merge Mechanism

### What the results describe as "merging"

The experiment output shows four separate anomalies producing one question: `"Why don't some birds fly?"`. This resembles the research concept of question merge (H9), but **the implementation does not use `QuestionRepository.merge_questions()`**.

### Actual mechanism: key-based deduplication + text generalization

| Mechanism | Location | Behavior |
|-----------|----------|----------|
| Deduplication | `CuriosityEngine._question_keys` | Maps `"Bird:fly"` → single question id |
| Generalization | `curiosity_engine.py` lines 49–50 | When `times_encountered >= 2`, rewrites `text` to plural form |
| Repository merge | `question_repository.py` | **Defined but unused** in EXP-001 |

`merge_questions(target_id, source_id)` would:

1. Add source `curiosity_debt` to target
2. Add source `times_encountered` to target
3. Extend `related_observations` and `child_questions`
4. Delete source question from repository

None of this runs in the current experiment. The bird case is **one question updated in place**, not two questions merged into one.

---

## Curiosity Debt Mechanism

Constant: `DEBT_INCREMENT = 1.0`

| Event | Formula | Running total (birds) |
|-------|---------|------------------------|
| First encounter (NEW) | `debt = 1.0` | 1.0 |
| Second encounter | `debt += 1.0 × 2` | 3.0 |
| Third encounter | `debt += 1.0 × 3` | 6.0 |
| Fourth encounter | `debt += 1.0 × 4` | 10.0 |

Debt scales with **encounter count at time of update** (triangular accumulation: 1 + 2 + 3 + 4 = 10).

Bat and Whale each encounter once → debt remains `1.0`.

---

## Question State Assignment

| State | When assigned | Used in EXP-001? |
|-------|---------------|------------------|
| `NEW` | Question first created | Yes — Penguin |
| `ACTIVE` | Question updated on repeat encounter | Yes — Ostrich, Emu, Kiwi |
| `INVESTIGATING` | — | No |
| `PARTIALLY_RESOLVED` | — | No |
| `RESOLVED` | — | No |
| `DORMANT` | — | No |
| `ABANDONED` | — | No |

States are simple string assignments in `CuriosityEngine`. No state machine or transition table.

`get_active_questions()` treats `NEW`, `ACTIVE`, `INVESTIGATING`, and `PARTIALLY_RESOLVED` as active. All three generated questions qualify.

---

## Heuristics Involved

| Heuristic | Rule | Effect |
|-----------|------|--------|
| Mismatch detection | `behavior != expected` | Triggers question path |
| Question key | `f"{category}:{expected}"` | Groups failures by category + expected behavior |
| Cross-category key | `f"{category}:cross:{observed}"` | Separate questions for Bat, Whale |
| Generalization threshold | `times_encountered >= 2` | Rewrites singular → plural question text |
| Behavior owner lookup | First rule in `world_model.rules` matching behavior | Bat → Bird, Whale → Fish |
| Debt scaling | `DEBT_INCREMENT × times_encountered` | Repeated anomalies increase debt faster |
| Observation order | Fixed lists in `main()` | Deterministic processing sequence |

All heuristics are **fixed, explicit, and deterministic** given the same inputs.

---

## Bat and Whale (brief)

- `world_model.predict("Mammal")` → `None` (no rule)
- `observe()` second branch: find category whose rule behavior matches observed behavior
- Bat flies → matches `Bird: fly` → cross-category question
- Whale swims → matches `Fish: swim` → cross-category question
- Each gets its own key; no generalization (only one encounter each)

---

## Overall Assessment

### Classification

**Primary: D — Emergent from interactions between simple rules**

The generalized question `"Why don't some birds fly?"` is not hardcoded. It emerges from:

1. A single category rule (`Bird → fly`)
2. String mismatch on `"not fly"`
3. Key-based reuse of one question object
4. A count threshold (`>= 2`) triggering text rewrite

**Secondary: B — Heuristic but deterministic**

Explicit heuristics (keys, thresholds, debt formula) produce repeatable outcomes. Same inputs → same questions, text, debt, and states every run.

**Not C — Random**

No random selection affects cognition. `uuid` only labels entities.

**Not strictly A — Fully deterministic**

Question ids and timestamps differ per run. Functional behavior (question count, text, debt, states) is deterministic.

### Summary table

| Property | Finding |
|----------|---------|
| Randomness in logic | Absent |
| Randomness in ids | Present (`uuid`), non-functional |
| Question "merge" in EXP-001 | Deduplication + in-place update, not `merge_questions()` |
| Abstraction | Heuristic generalization at encounter ≥ 2 |
| Curiosity debt | Triangular accumulation on repeat encounters |
| States used | `NEW`, `ACTIVE` only |
| Reproducibility of behavior | Yes (modulo ids/timestamps) |

### Research note

`exp001_results.md` describes "four separate anomalies merged into one question." The code achieves a similar **observable outcome** through a simpler mechanism than the documented `merge_questions()` API. The repository merge function exists as infrastructure but plays no role in the current experiment path.

---

## Verification Run

Command: `python experiments/exp001_penguin_world.py`

Functional output (consistent across runs):

- 1 bird question: `"Why don't some birds fly?"` — debt 10.0, state ACTIVE, times_encountered 4
- 1 bat question: debt 1.0, state NEW
- 1 whale question: debt 1.0, state NEW
- Total curiosity debt: 12.0

Question ids change each run; all other reported fields remain stable.
