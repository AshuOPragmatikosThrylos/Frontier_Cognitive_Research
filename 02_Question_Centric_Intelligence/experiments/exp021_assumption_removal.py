import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0
INITIAL_TRACE_STRENGTH = 1.0
RECONSTRUCTION_BUDGET = 1
TRACE_STRENGTH_DIVISOR = 4.0

BIRD_CONFORMING = [
    ("Sparrow", "Bird", "fly"),
    ("Robin", "Bird", "fly"),
    ("Eagle", "Bird", "fly"),
    ("Falcon", "Bird", "fly"),
]

BIRD_CONTRADICTING = [
    ("Penguin", "Bird", "not fly"),
    ("Ostrich", "Bird", "not fly"),
    ("Emu", "Bird", "not fly"),
    ("Kiwi", "Bird", "not fly"),
]

MAMMAL_FLY = [
    ("Bat", "Mammal", "fly"),
    ("Squirrel", "Mammal", "fly"),
]

MAMMAL_SWIM = [
    ("Whale", "Mammal", "swim"),
    ("Dolphin", "Mammal", "swim"),
]

INSECT_FLY = [
    ("Bee", "Insect", "fly"),
    ("Ant", "Insect", "fly"),
]

INSECT_CRAWL = [
    ("Beetle", "Insect", "crawl"),
    ("Spider", "Insect", "crawl"),
]

BIRD_REINTRO_CONFORMING = [
    ("Crow", "Bird", "fly"),
    ("Raven", "Bird", "fly"),
]

BIRD_REINTRO_CONTRADICTING = [
    ("Chicken", "Bird", "not fly"),
    ("Turkey", "Bird", "not fly"),
]

MAMMAL_REINTRO_FLY = [
    ("Mouse", "Mammal", "fly"),
    ("Shrew", "Mammal", "fly"),
]

MAMMAL_REINTRO_SWIM = [
    ("Otter", "Mammal", "swim"),
    ("Beaver", "Mammal", "swim"),
]

INSECT_REINTRO_FLY = [
    ("Wasp", "Insect", "fly"),
    ("Fly", "Insect", "fly"),
]

INSECT_REINTRO_CRAWL = [
    ("Centipede", "Insect", "crawl"),
    ("Mantis", "Insect", "crawl"),
]

TENSION_RESOLUTIONS = [
    ("t-bird-fly-vs-not_fly", "niche specialization resolves bird behavior conflict"),
    ("t-mammal-fly-vs-swim", "locomotion niche resolves mammal behavior conflict"),
    ("t-insect-fly-vs-crawl", "body plan resolves insect behavior conflict"),
]

ALL_TENSION_IDS = [
    "t-bird-fly-vs-not_fly",
    "t-insect-fly-vs-crawl",
    "t-mammal-fly-vs-swim",
]

ALL_QUESTION_IDS = [
    "eq-bird-fly-vs-not_fly",
    "eq-insect-fly-vs-crawl",
    "eq-mammal-fly-vs-swim",
]


@dataclass
class RawObservation:
    entity: str
    category: str
    behavior: str


@dataclass
class DifferenceGroup:
    name: str
    category: str
    behavior: str
    members: list[str] = field(default_factory=list)


@dataclass
class PersistentTension:
    id: str
    category: str
    group_a: str
    group_b: str
    behavior_a: str
    behavior_b: str
    strength: float
    persistent: bool
    resolved: bool = False
    resolution_note: str = ""


@dataclass
class LifecycleQuestion:
    id: str
    text: str
    category: str
    source_groups: list[str]
    tension_id: str
    state: str = "EMERGENT"
    vitality: float = 0.0
    lifecycle_history: list[str] = field(default_factory=list)
    reconstructed_from_memory: bool = False


@dataclass
class MemoryTrace:
    trace_id: str
    tension_id: str
    question_id: str
    category: str
    behavior_a: str
    behavior_b: str
    source_groups: list[str]
    text: str
    lifecycle_history: list[str]
    final_vitality: float
    final_state: str
    trace_strength: float = INITIAL_TRACE_STRENGTH


@dataclass
class WorldState:
    label: str
    world_id: str
    assumption_rich: bool
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    phase_events: list[str] = field(default_factory=list)
    reconstruction_winners: list[str] = field(default_factory=list)
    permanent_losses: list[str] = field(default_factory=list)
    reactivated_questions: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_observation(
    state: WorldState,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: WorldState, category: str) -> None:
    groups = state.category_index.get(category, {})
    if len(groups) < 2:
        return
    if not all(len(members) >= DIFFERENCE_MIN_PER_GROUP for members in groups.values()):
        return

    for behavior, members in sorted(groups.items()):
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            continue
        state.difference_groups[group_name] = DifferenceGroup(
            name=group_name,
            category=category,
            behavior=behavior,
            members=list(members),
        )


def refresh_group_members(state: WorldState, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def groups_for_category(state: WorldState, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: WorldState, category: str) -> list[PersistentTension]:
    groups = groups_for_category(state, category)
    tensions: list[PersistentTension] = []

    for index, group_a in enumerate(groups):
        for group_b in groups[index + 1:]:
            strength = float(min(len(group_a.members), len(group_b.members)))
            persistent = strength >= PERSISTENT_TENSION_MIN
            tension_id = (
                f"t-{category.lower()}-{behavior_key(group_a.behavior)}-vs-{behavior_key(group_b.behavior)}"
            )
            tensions.append(PersistentTension(
                id=tension_id,
                category=category,
                group_a=group_a.name,
                group_b=group_b.name,
                behavior_a=group_a.behavior,
                behavior_b=group_b.behavior,
                strength=strength,
                persistent=persistent,
            ))

    return tensions


def record_tensions(state: WorldState, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: WorldState, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def memory_trace_for_tension(state: WorldState, tension_id: str) -> MemoryTrace | None:
    for trace in state.memory_traces.values():
        if trace.tension_id == tension_id and trace.trace_strength > 0.0:
            return trace
    return None


def question_id_for_tension(tension: PersistentTension) -> str:
    return (
        f"eq-{tension.category.lower()}-{behavior_key(tension.behavior_a)}-vs-"
        f"{behavior_key(tension.behavior_b)}"
    )


def apply_lifecycle_state(question: LifecycleQuestion, tension_resolved: bool) -> None:
    if question.vitality <= 0.0:
        question.state = "EXTINCT"
    elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
        question.state = "DORMANT"
    elif tension_resolved:
        question.state = "RESOLVED"
    elif question.state == "EMERGENT":
        pass
    else:
        question.state = "ACTIVE"


def emerge_questions_from_tensions(state: WorldState) -> None:
    for tension in state.persistent_tensions:
        if not tension.persistent:
            continue
        if tension.id in {question.tension_id for question in state.lifecycle_questions.values()}:
            continue

        question_id = question_id_for_tension(tension)
        question = LifecycleQuestion(
            id=question_id,
            text=(
                f"Why do {tension.category} entities both {tension.behavior_a} "
                f"and {tension.behavior_b}?"
            ),
            category=tension.category,
            source_groups=[tension.group_a, tension.group_b],
            tension_id=tension.id,
            vitality=tension.strength,
        )
        question.lifecycle_history.append(
            f"EMERGENT (vitality={question.vitality:.1f}, tension={tension.id})"
        )
        state.lifecycle_questions[question_id] = question


def promote_emergent_questions(state: WorldState) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: WorldState, tension_id: str, note: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None or tension.resolved:
        return

    tension.resolved = True
    tension.resolution_note = note

    for question in state.lifecycle_questions.values():
        if question.tension_id != tension_id:
            continue
        question.vitality -= RESOLUTION_VITALITY_REDUCTION
        apply_lifecycle_state(question, tension_resolved=True)
        question.lifecycle_history.append(
            f"tension resolved -> vitality={question.vitality:.1f}, state={question.state} ({note})"
        )


def apply_vitality_decay(state: WorldState, question_id: str) -> None:
    question = state.lifecycle_questions.get(question_id)
    if question is None or question.state == "EXTINCT":
        return

    tension = get_tension(state, question.tension_id)
    tension_resolved = tension.resolved if tension else False

    question.vitality -= DECAY_VITALITY_REDUCTION
    previous_state = question.state
    apply_lifecycle_state(question, tension_resolved=tension_resolved)
    question.lifecycle_history.append(
        f"vitality decay {previous_state} -> {question.state} (vitality={question.vitality:.1f})"
    )


def drive_question_to_extinction(state: WorldState, question_id: str) -> None:
    while True:
        question = state.lifecycle_questions.get(question_id)
        if question is None or question.state == "EXTINCT":
            return
        apply_vitality_decay(state, question_id)


def trace_strength_from_tension(tension: PersistentTension | None) -> float:
    if tension is None:
        return 0.5
    return min(INITIAL_TRACE_STRENGTH, tension.strength / TRACE_STRENGTH_DIVISOR)


def archive_and_delete_extinct_questions(state: WorldState) -> None:
    for question_id, question in list(state.lifecycle_questions.items()):
        if question.state != "EXTINCT":
            continue

        tension = get_tension(state, question.tension_id)
        trace_id = f"mem-{question_id}"
        state.memory_traces[trace_id] = MemoryTrace(
            trace_id=trace_id,
            tension_id=question.tension_id,
            question_id=question.id,
            category=question.category,
            behavior_a=tension.behavior_a if tension else "",
            behavior_b=tension.behavior_b if tension else "",
            source_groups=list(question.source_groups),
            text=question.text,
            lifecycle_history=list(question.lifecycle_history),
            final_vitality=question.vitality,
            final_state=question.state,
            trace_strength=trace_strength_from_tension(tension),
        )
        del state.lifecycle_questions[question_id]
        state.deleted_questions.append(question_id)


def reopen_tension(state: WorldState, tension_id: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None:
        return

    group_a = state.difference_groups.get(tension.group_a)
    group_b = state.difference_groups.get(tension.group_b)
    if group_a and group_b:
        tension.strength = float(min(len(group_a.members), len(group_b.members)))

    tension.resolved = False
    tension.resolution_note = ""
    tension.persistent = tension.strength >= PERSISTENT_TENSION_MIN


def reconstruct_from_memory(
    state: WorldState,
    trace: MemoryTrace,
    tension: PersistentTension,
) -> str:
    question = LifecycleQuestion(
        id=trace.question_id,
        text=trace.text,
        category=trace.category,
        source_groups=list(trace.source_groups),
        tension_id=tension.id,
        vitality=tension.strength,
        reconstructed_from_memory=True,
        lifecycle_history=list(trace.lifecycle_history),
    )
    question.lifecycle_history.append(
        f"RECONSTRUCTED from memory (vitality={question.vitality:.1f}, trace={trace.trace_id})"
    )
    question.state = "ACTIVE"
    question.lifecycle_history.append("RECONSTRUCTED -> ACTIVE (promoted)")
    state.lifecycle_questions[question.id] = question
    return question.id


def ingest_category_observations(
    state: WorldState,
    category: str,
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            register_observation(state, entity, obs_category, behavior)
    form_difference_groups(state, category)
    record_tensions(state, category)


def ingest_initial_observations(state: WorldState) -> None:
    ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
    ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
    ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])


def process_extinction_lifecycle(state: WorldState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in ALL_QUESTION_IDS:
        drive_question_to_extinction(state, question_id)


def process_memory_archival(state: WorldState) -> None:
    archive_and_delete_extinct_questions(state)
    state.phase_events.append(
        f"archived {len(state.memory_traces)} traces, live questions={len(state.lifecycle_questions)}"
    )


def ingest_reintroduction_observations(state: WorldState) -> None:
    ingest_category_observations(
        state,
        "Bird",
        [BIRD_REINTRO_CONFORMING, BIRD_REINTRO_CONTRADICTING],
    )
    refresh_group_members(state, "Bird")

    ingest_category_observations(
        state,
        "Mammal",
        [MAMMAL_REINTRO_FLY, MAMMAL_REINTRO_SWIM],
    )
    refresh_group_members(state, "Mammal")

    ingest_category_observations(
        state,
        "Insect",
        [INSECT_REINTRO_FLY, INSECT_REINTRO_CRAWL],
    )
    refresh_group_members(state, "Insect")


def reopen_all_tensions(state: WorldState) -> list[str]:
    reopened: list[str] = []
    for tension_id in ALL_TENSION_IDS:
        reopen_tension(state, tension_id)
        tension = get_tension(state, tension_id)
        if tension and tension.persistent:
            reopened.append(tension_id)
    return reopened


def run_assumption_rich_reactivation(state: WorldState, reopened_tension_ids: list[str]) -> None:
    candidates: list[MemoryTrace] = []

    for tension_id in reopened_tension_ids:
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            state.phase_events.append(f"{tension_id}: skipped (not persistent)")
            continue
        if any(question.tension_id == tension_id for question in state.lifecycle_questions.values()):
            state.phase_events.append(f"{tension_id}: skipped (question already live)")
            continue

        trace = memory_trace_for_tension(state, tension_id)
        if trace is None:
            state.phase_events.append(f"{tension_id}: skipped (no trace)")
            continue

        candidates.append(trace)

    candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))

    state.phase_events.append(
        f"competition start: {len(candidates)} candidates, budget={RECONSTRUCTION_BUDGET}"
    )
    for index, trace in enumerate(candidates):
        state.phase_events.append(
            f"  rank {index + 1}: {trace.trace_id} "
            f"strength={trace.trace_strength:.2f} question={trace.question_id}"
        )

    winners = candidates[:RECONSTRUCTION_BUDGET]
    losers = candidates[RECONSTRUCTION_BUDGET:]

    for trace in losers:
        state.permanent_losses.append(trace.question_id)
        state.phase_events.append(
            f"lost: {trace.trace_id} ({trace.question_id}) — remains extinct"
        )

    for trace in winners:
        tension = get_tension(state, trace.tension_id)
        if tension is None:
            continue
        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstruction_winners.append(question_id)
        state.phase_events.append(
            f"won: {trace.trace_id} -> {question_id} (strength-ranked winner)"
        )


def run_assumption_removed_reactivation(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reactivation start: {len(reopened_tension_ids)} reopened tensions "
        f"(no ranking, no budget, no strength ordering)"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            state.phase_events.append(f"{tension_id}: skipped (not persistent)")
            continue
        if any(question.tension_id == tension_id for question in state.lifecycle_questions.values()):
            state.phase_events.append(f"{tension_id}: skipped (question already live)")
            continue

        trace = memory_trace_for_tension(state, tension_id)
        if trace is None:
            state.phase_events.append(f"{tension_id}: skipped (no trace)")
            continue

        question_id = reconstruct_from_memory(state, trace, tension)
        state.reactivated_questions.append(question_id)
        state.phase_events.append(
            f"reactivated: {trace.trace_id} -> {question_id} "
            f"(tension order, trace_strength={trace.trace_strength:.2f} not used for priority)"
        )


def process_reintroduction(state: WorldState) -> None:
    ingest_reintroduction_observations(state)
    reopened = reopen_all_tensions(state)

    if state.assumption_rich:
        run_assumption_rich_reactivation(state, reopened)
        return

    run_assumption_removed_reactivation(state, reopened)


def run_shared_pipeline(assumption_rich: bool) -> WorldState:
    if assumption_rich:
        state = WorldState(
            label="World A (Assumption-Rich)",
            world_id="A",
            assumption_rich=True,
        )
    else:
        state = WorldState(
            label="World B (Assumption-Removed)",
            world_id="B",
            assumption_rich=False,
        )

    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_archival(state)
    process_reintroduction(state)
    return state


def run_experiment() -> tuple[WorldState, WorldState]:
    world_a = run_shared_pipeline(assumption_rich=True)
    world_b = run_shared_pipeline(assumption_rich=False)
    return world_a, world_b


def trace_count(state: WorldState) -> int:
    return len(state.memory_traces)


def live_question_count(state: WorldState) -> int:
    return len(state.lifecycle_questions)


def latent_trace_count(state: WorldState) -> int:
    live_tension_ids = {question.tension_id for question in state.lifecycle_questions.values()}
    return sum(
        1 for trace in state.memory_traces.values()
        if trace.tension_id not in live_tension_ids
    )


def traces_disappeared(state: WorldState) -> bool:
    return len(state.deleted_questions) > trace_count(state)


def selection_pattern_detected(state: WorldState) -> bool:
    if state.assumption_rich:
        return len(state.reconstruction_winners) > 0 and len(state.permanent_losses) > 0

    return live_question_count(state) < trace_count(state)


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<32} {value_a:<24} {value_b}")


def print_side_by_side_outcomes(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Side-by-Side Outcomes ===\n")
    print_comparison_row("Metric", "World A (Rich)", "World B (Removed)")
    print_comparison_row("Assumptions", "rank+budget+strength", "none")
    print_comparison_row("Memory traces", str(trace_count(world_a)), str(trace_count(world_b)))
    print_comparison_row("Live questions", str(live_question_count(world_a)), str(live_question_count(world_b)))
    print_comparison_row("Latent traces", str(latent_trace_count(world_a)), str(latent_trace_count(world_b)))
    print_comparison_row(
        "Explicit winners",
        str(len(world_a.reconstruction_winners)),
        str(len(world_b.reconstruction_winners)),
    )
    print_comparison_row(
        "Explicit losses",
        str(len(world_a.permanent_losses)),
        str(len(world_b.permanent_losses)),
    )
    print_comparison_row(
        "Reactivated (no rank)",
        "n/a",
        str(len(world_b.reactivated_questions)),
    )
    print()

    for question_id in ALL_QUESTION_IDS:
        live_a = question_id in world_a.lifecycle_questions
        live_b = question_id in world_b.lifecycle_questions
        print(f"  {question_id}:")
        print(f"    A: live={live_a}")
        print(f"    B: live={live_b}")
    print()


def print_trace_statistics(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Trace Statistics ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row("Traces archived", str(trace_count(world_a)), str(trace_count(world_b)))
    print_comparison_row("Traces disappeared", str(traces_disappeared(world_a)), str(traces_disappeared(world_b)))
    print_comparison_row("Deleted questions", str(len(world_a.deleted_questions)), str(len(world_b.deleted_questions)))
    print()

    all_trace_ids = sorted(set(world_a.memory_traces) | set(world_b.memory_traces))
    for trace_id in all_trace_ids:
        trace_a = world_a.memory_traces.get(trace_id)
        trace_b = world_b.memory_traces.get(trace_id)
        strength_a = f"{trace_a.trace_strength:.2f}" if trace_a else "(absent)"
        strength_b = f"{trace_b.trace_strength:.2f}" if trace_b else "(absent)"
        print(f"  {trace_id}:")
        print(f"    A: strength={strength_a} stable={trace_a is not None}")
        print(f"    B: strength={strength_b} stable={trace_b is not None}")
    print()


def print_persistence_patterns(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Persistence Patterns ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "All traces persist in memory",
        str(trace_count(world_a) == len(world_a.deleted_questions)),
        str(trace_count(world_b) == len(world_b.deleted_questions)),
    )
    print_comparison_row(
        "Expressed / archived ratio",
        f"{live_question_count(world_a)}/{trace_count(world_a)}",
        f"{live_question_count(world_b)}/{trace_count(world_b)}",
    )
    print_comparison_row(
        "Traces without live question",
        str(latent_trace_count(world_a)),
        str(latent_trace_count(world_b)),
    )
    print()

    for label, state in [("A", world_a), ("B", world_b)]:
        print(f"  World {label} trace persistence:")
        for trace_id in sorted(state.memory_traces):
            trace = state.memory_traces[trace_id]
            expressed = any(
                question.tension_id == trace.tension_id
                for question in state.lifecycle_questions.values()
            )
            print(
                f"    {trace_id}: strength={trace.trace_strength:.2f} "
                f"expressed={expressed} disappeared=False"
            )
        print()


def print_selection_patterns(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Selection Patterns ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "Selection-like pattern",
        str(selection_pattern_detected(world_a)),
        str(selection_pattern_detected(world_b)),
    )
    print_comparison_row(
        "Ranking used",
        "True",
        "False",
    )
    print_comparison_row(
        "Fixed budget used",
        f"True (budget={RECONSTRUCTION_BUDGET})",
        "False",
    )
    print_comparison_row(
        "Strength ordering used",
        "True",
        "False",
    )
    print()

    print("  World A phase events (assumption-rich):")
    for event in world_a.phase_events:
        if "rank" in event or "won" in event or "lost" in event or "competition" in event:
            print(f"    {event}")
    print()

    print("  World B phase events (assumption-removed):")
    for event in world_b.phase_events:
        if "reactivat" in event:
            print(f"    {event}")
    print()


def print_overall_observations(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds share identical observations through extinction and memory archival.")
    print("  2. World A applies explicit ranking, fixed budget, and strength ordering (EXP-017 rules).")
    print("  3. World B removes ranking, budget, and strength ordering — reactivates all eligible traces.")
    print(
        f"  4. Trace count: A={trace_count(world_a)} B={trace_count(world_b)} "
        f"(all traces stable in both worlds)."
    )
    print(
        f"  5. Live questions: A={live_question_count(world_a)} B={live_question_count(world_b)}."
    )
    print(
        f"  6. Selection pattern: A={selection_pattern_detected(world_a)} "
        f"B={selection_pattern_detected(world_b)}."
    )
    print(
        f"  7. Traces disappeared naturally: A={traces_disappeared(world_a)} "
        f"B={traces_disappeared(world_b)}."
    )
    print()
    print("  Interpretation:")
    print("    Selection in World A is assumption-imposed — rank, budget, and max-strength winner.")
    print("    World B shows whether selection survives without those assumptions.")
    print("    Stable traces emerge in both worlds; natural trace disappearance does not occur here.")
    print("    Any selection-like asymmetry in World A vanishes when assumptions are removed.")
    print()


def main() -> None:
    print("=== EXP-021 Assumption Removal ===\n")
    print("Pipeline: observations -> differences -> tensions -> questions -> extinction -> memory traces")
    print("World A: assumption-rich reactivation (rank, budget, strength ordering)")
    print("World B: assumption-removed reactivation (no ranking, no budget, no strength ordering)\n")

    world_a, world_b = run_experiment()

    print_side_by_side_outcomes(world_a, world_b)
    print_trace_statistics(world_a, world_b)
    print_persistence_patterns(world_a, world_b)
    print_selection_patterns(world_a, world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
