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
CLUTTER_TRACE_STRENGTH = 0.5
FORGETTING_DECAY = 0.25
FORGETTING_STEPS = 3

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

MAMMAL_CONTRADICTING = [
    ("Bat", "Mammal", "fly"),
    ("Whale", "Mammal", "swim"),
]

BIRD_REINTRO_CONFORMING = [
    ("Crow", "Bird", "fly"),
    ("Raven", "Bird", "fly"),
]

BIRD_REINTRO_CONTRADICTING = [
    ("Chicken", "Bird", "not fly"),
    ("Turkey", "Bird", "not fly"),
]

TENSION_RESOLUTIONS = [
    ("t-bird-fly-vs-not_fly", "niche specialization resolves bird behavior conflict"),
]

DECAY_STEPS = [
    "eq-bird-fly-vs-not_fly",
    "eq-bird-fly-vs-not_fly",
]

BIRD_TENSION_ID = "t-bird-fly-vs-not_fly"
BIRD_QUESTION_ID = "eq-bird-fly-vs-not_fly"
ORPHAN_TENSION_ID = "t-mammal-fly-vs-swim"


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
class WorldResult:
    label: str
    world_id: str
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    reconstruction_events: list[str] = field(default_factory=list)
    forgetting_events: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_observation(
    state: WorldResult,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: WorldResult, category: str) -> None:
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


def refresh_group_members(state: WorldResult, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def groups_for_category(state: WorldResult, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: WorldResult, category: str) -> list[PersistentTension]:
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


def record_tensions(state: WorldResult, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: WorldResult, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def memory_trace_for_tension(state: WorldResult, tension_id: str) -> MemoryTrace | None:
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


def emerge_questions_from_tensions(state: WorldResult) -> None:
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


def promote_emergent_questions(state: WorldResult) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: WorldResult, tension_id: str, note: str) -> None:
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
            f"tension resolved -> vitality={question.vitality:.1f}, state={question.state} "
            f"({note})"
        )


def apply_vitality_decay(state: WorldResult, question_id: str) -> None:
    question = state.lifecycle_questions.get(question_id)
    if question is None or question.state == "EXTINCT":
        return

    tension = get_tension(state, question.tension_id)
    tension_resolved = tension.resolved if tension else False

    question.vitality -= DECAY_VITALITY_REDUCTION
    previous_state = question.state
    apply_lifecycle_state(question, tension_resolved=tension_resolved)
    question.lifecycle_history.append(
        f"vitality decay {previous_state} -> {question.state} "
        f"(vitality={question.vitality:.1f})"
    )


def archive_and_delete_extinct_questions(state: WorldResult) -> None:
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
            trace_strength=INITIAL_TRACE_STRENGTH,
        )
        del state.lifecycle_questions[question_id]
        state.deleted_questions.append(question_id)


def seed_clutter_trace(state: WorldResult) -> None:
    state.memory_traces["mem-orphan-clutter"] = MemoryTrace(
        trace_id="mem-orphan-clutter",
        tension_id=ORPHAN_TENSION_ID,
        question_id="eq-orphan-clutter",
        category="Mammal",
        behavior_a="fly",
        behavior_b="swim",
        source_groups=["Mammal.fly", "Mammal.swim"],
        text="Why do Mammal entities both fly and swim?",
        lifecycle_history=["EMERGENT (orphan clutter trace, never revisited)"],
        final_vitality=0.0,
        final_state="EXTINCT",
        trace_strength=CLUTTER_TRACE_STRENGTH,
    )


def apply_selective_forgetting(state: WorldResult) -> None:
    for trace_id in list(state.memory_traces):
        trace = state.memory_traces[trace_id]
        trace.trace_strength -= FORGETTING_DECAY
        if trace.trace_strength <= 0.0:
            del state.memory_traces[trace_id]
            state.forgetting_events.append(f"forgotten: {trace_id}")
        else:
            state.forgetting_events.append(
                f"weakened: {trace_id} strength={trace.trace_strength:.2f}"
            )


def reopen_tension(state: WorldResult, tension_id: str) -> None:
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


def reconstruct_from_memory(state: WorldResult, trace: MemoryTrace, tension: PersistentTension) -> str:
    trace.trace_strength = INITIAL_TRACE_STRENGTH
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


def create_new_question(state: WorldResult, tension: PersistentTension) -> str:
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
        f"EMERGENT (new, vitality={question.vitality:.1f}, tension={tension.id})"
    )
    question.state = "ACTIVE"
    question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")
    state.lifecycle_questions[question_id] = question
    return question_id


def try_reconstruct_or_create(state: WorldResult, tension_id: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None or not tension.persistent:
        state.reconstruction_events.append(f"{tension_id}: no action (tension not persistent)")
        return

    trace = memory_trace_for_tension(state, tension_id)
    if trace:
        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstruction_events.append(
            f"reconstruction: {question_id} (from {trace.trace_id}, "
            f"strength={trace.trace_strength:.2f})"
        )
        return

    question_id = create_new_question(state, tension)
    state.reconstruction_events.append(
        f"new question: {question_id} (trace missing or forgotten)"
    )


def ingest_initial_observations(state: WorldResult) -> None:
    for entity, category, behavior in BIRD_CONFORMING:
        register_observation(state, entity, category, behavior)

    for entity, category, behavior in BIRD_CONTRADICTING:
        register_observation(state, entity, category, behavior)

    form_difference_groups(state, "Bird")
    record_tensions(state, "Bird")

    for entity, category, behavior in MAMMAL_CONTRADICTING:
        register_observation(state, entity, category, behavior)

    form_difference_groups(state, "Mammal")
    record_tensions(state, "Mammal")


def process_extinction_lifecycle(state: WorldResult) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in DECAY_STEPS:
        apply_vitality_decay(state, question_id)


def process_memory_deletion(state: WorldResult) -> None:
    archive_and_delete_extinct_questions(state)
    seed_clutter_trace(state)


def process_forgetting(state: WorldResult, selective: bool) -> None:
    if not selective:
        return
    for step in range(FORGETTING_STEPS):
        state.forgetting_events.append(f"--- forgetting step {step + 1} ---")
        apply_selective_forgetting(state)


def process_reintroduction(state: WorldResult) -> None:
    for entity, category, behavior in BIRD_REINTRO_CONFORMING:
        register_observation(state, entity, category, behavior)

    for entity, category, behavior in BIRD_REINTRO_CONTRADICTING:
        register_observation(state, entity, category, behavior)

    refresh_group_members(state, "Bird")
    reopen_tension(state, BIRD_TENSION_ID)
    try_reconstruct_or_create(state, BIRD_TENSION_ID)


def run_perfect_memory_world() -> WorldResult:
    state = WorldResult(label="World A (Perfect Memory)", world_id="A")
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_deletion(state)
    process_forgetting(state, selective=False)
    process_reintroduction(state)
    return state


def run_selective_forgetting_world() -> WorldResult:
    state = WorldResult(label="World B (Selective Forgetting)", world_id="B")
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_deletion(state)
    process_forgetting(state, selective=True)
    process_reintroduction(state)
    return state


def trace_count(state: WorldResult) -> int:
    return len(state.memory_traces)


def clutter_count(state: WorldResult) -> int:
    return sum(1 for trace in state.memory_traces if trace.trace_id == "mem-orphan-clutter")


def identity_preserved(state: WorldResult) -> bool:
    question = state.lifecycle_questions.get(BIRD_QUESTION_ID)
    if question is None:
        return False
    return question.reconstructed_from_memory and question.id == BIRD_QUESTION_ID


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<28} {value_a:<22} {value_b}")


def print_memory_traces_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Memory Traces ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row("Trace count", str(trace_count(world_a)), str(trace_count(world_b)))
    print_comparison_row("Clutter traces", str(clutter_count(world_a)), str(clutter_count(world_b)))
    print()

    all_ids = sorted(
        set(world_a.memory_traces) | set(world_b.memory_traces)
    )
    for trace_id in all_ids:
        trace_a = world_a.memory_traces.get(trace_id)
        trace_b = world_b.memory_traces.get(trace_id)
        strength_a = f"{trace_a.trace_strength:.2f}" if trace_a else "(absent)"
        strength_b = f"{trace_b.trace_strength:.2f}" if trace_b else "(absent)"
        print(f"  {trace_id}:")
        print(f"    A: strength={strength_a}")
        print(f"    B: strength={strength_b}")
    print()


def print_reconstruction_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Reconstruction Events ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "Events",
        str(len(world_a.reconstruction_events)),
        str(len(world_b.reconstruction_events)),
    )
    print()

    max_events = max(len(world_a.reconstruction_events), len(world_b.reconstruction_events), 1)
    for index in range(max_events):
        event_a = (
            world_a.reconstruction_events[index]
            if index < len(world_a.reconstruction_events)
            else "(none)"
        )
        event_b = (
            world_b.reconstruction_events[index]
            if index < len(world_b.reconstruction_events)
            else "(none)"
        )
        print(f"  Event {index + 1}:")
        print(f"    A: {event_a}")
        print(f"    B: {event_b}")
    print()


def print_clutter_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Clutter ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "Orphan clutter present",
        str(clutter_count(world_a) > 0),
        str(clutter_count(world_b) > 0),
    )
    print_comparison_row(
        "Total traces after reintro",
        str(trace_count(world_a)),
        str(trace_count(world_b)),
    )
    print()


def print_identity_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Identity Preservation ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "Bird identity preserved",
        str(identity_preserved(world_a)),
        str(identity_preserved(world_b)),
    )

    for label, state in [("A", world_a), ("B", world_b)]:
        question = state.lifecycle_questions.get(BIRD_QUESTION_ID)
        if question:
            origin = "reconstructed" if question.reconstructed_from_memory else "new"
            print(f"    {label}: {question.id} origin={origin} history={len(question.lifecycle_history)}")
        else:
            print(f"    {label}: (no bird question)")
    print()


def print_organization_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Organization ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row(
        "Observations",
        str(len(world_a.observations)),
        str(len(world_b.observations)),
    )
    print_comparison_row(
        "Live questions",
        str(len(world_a.lifecycle_questions)),
        str(len(world_b.lifecycle_questions)),
    )
    print_comparison_row(
        "Forgetting events",
        str(len(world_a.forgetting_events)),
        str(len(world_b.forgetting_events)),
    )
    print()


def print_memory_statistics(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Memory Statistics ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row("Traces at reintro", str(trace_count(world_a)), str(trace_count(world_b)))
    print_comparison_row("Deleted questions", str(len(world_a.deleted_questions)), str(len(world_b.deleted_questions)))
    print_comparison_row("Forgetting events", str(len(world_a.forgetting_events)), str(len(world_b.forgetting_events)))
    print_comparison_row("Reconstructions", str(len(world_a.reconstruction_events)), str(len(world_b.reconstruction_events)))
    print()


def print_forgetting_events(world_b: WorldResult) -> None:
    print("Forgetting events (World B only):")
    if not world_b.forgetting_events:
        print("  (none)")
        print()
        return

    for event in world_b.forgetting_events:
        print(f"  {event}")
    print()


def print_overall_observations(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds received identical observations through extinction and reintroduction.")
    print("  2. World A retained all memory traces including unused clutter.")
    print("  3. World B applied selective forgetting to unused traces before reintroduction.")

    if clutter_count(world_a) > 0 and clutter_count(world_b) == 0:
        print("  4. Clutter trace forgotten in World B but persisted in World A.")

    if identity_preserved(world_a) and identity_preserved(world_b):
        print("  5. Bird identity reconstructed in both worlds — core trace survived forgetting.")
    elif identity_preserved(world_a) and not identity_preserved(world_b):
        print("  5. Bird identity preserved only in World A — forgetting erased reconstruction capacity.")

    print(
        f"  6. Trace count: A={trace_count(world_a)} B={trace_count(world_b)} "
        f"(clutter A={clutter_count(world_a)} B={clutter_count(world_b)})"
    )
    print(
        f"  7. Forgetting events: A={len(world_a.forgetting_events)} "
        f"B={len(world_b.forgetting_events)}"
    )
    print()
    print("  Interpretation:")
    print("    Perfect memory accumulates clutter; selective forgetting prunes unused traces.")
    print("    Identity reconstruction depends on trace survival at reintroduction time.")
    print()


def main() -> None:
    print("=== EXP-016 Ecosystem Forgetting ===\n")
    print("World A: perfect memory (traces persist forever)")
    print("World B: selective forgetting (unused traces decay and may disappear)")
    print(f"Forgetting decay: {FORGETTING_DECAY} per step, steps: {FORGETTING_STEPS}\n")

    world_a = run_perfect_memory_world()
    world_b = run_selective_forgetting_world()

    print_memory_traces_comparison(world_a, world_b)
    print_reconstruction_comparison(world_a, world_b)
    print_clutter_comparison(world_a, world_b)
    print_identity_comparison(world_a, world_b)
    print_organization_comparison(world_a, world_b)
    print_memory_statistics(world_a, world_b)
    print_forgetting_events(world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
