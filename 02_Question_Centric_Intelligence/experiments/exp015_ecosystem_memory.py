import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0

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


@dataclass
class WorldState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    reconstruction_events: list[str] = field(default_factory=list)


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


def form_difference_groups(state: WorldState, category: str) -> list[str]:
    groups = state.category_index.get(category, {})
    if len(groups) < 2:
        return []
    if not all(len(members) >= DIFFERENCE_MIN_PER_GROUP for members in groups.values()):
        return []

    created: list[str] = []
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
        created.append(group_name)
    return created


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
        if trace.tension_id == tension_id:
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
            f"tension resolved -> vitality={question.vitality:.1f}, state={question.state} "
            f"({note})"
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
        f"vitality decay {previous_state} -> {question.state} "
        f"(vitality={question.vitality:.1f})"
    )


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


def reconstruct_from_memory(state: WorldState, trace: MemoryTrace, tension: PersistentTension) -> str:
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


def create_new_question(state: WorldState, tension: PersistentTension) -> str:
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


def try_reconstruct_or_create(state: WorldState, tension_id: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None or not tension.persistent:
        state.reconstruction_events.append(f"{tension_id}: no action (tension not persistent)")
        return

    trace = memory_trace_for_tension(state, tension_id)
    if trace:
        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstruction_events.append(
            f"reconstruction: {question_id} (identity reconstructed from {trace.trace_id}, "
            f"history preserved={len(trace.lifecycle_history)} prior entries)"
        )
        return

    question_id = create_new_question(state, tension)
    state.reconstruction_events.append(
        f"new question: {question_id} (no memory trace, fresh identity)"
    )


def ingest_initial_observations(state: WorldState) -> None:
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


def process_extinction_lifecycle(state: WorldState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in DECAY_STEPS:
        apply_vitality_decay(state, question_id)


def process_memory_deletion(state: WorldState) -> None:
    archive_and_delete_extinct_questions(state)


def process_reintroduction(state: WorldState) -> None:
    for entity, category, behavior in BIRD_REINTRO_CONFORMING:
        register_observation(state, entity, category, behavior)

    for entity, category, behavior in BIRD_REINTRO_CONTRADICTING:
        register_observation(state, entity, category, behavior)

    refresh_group_members(state, "Bird")
    reopen_tension(state, BIRD_TENSION_ID)
    try_reconstruct_or_create(state, BIRD_TENSION_ID)


def print_memory_traces(state: WorldState) -> None:
    print("Memory traces:")
    if not state.memory_traces:
        print("  (none)")
        print()
        return

    for trace in sorted(state.memory_traces.values(), key=lambda t: t.trace_id):
        print(
            f"  [{trace.trace_id}] question={trace.question_id} tension={trace.tension_id} "
            f"final_state={trace.final_state}"
        )
        print(f"    text: {trace.text}")
        print(f"    history entries: {len(trace.lifecycle_history)}")
    print()


def print_deleted_questions(state: WorldState) -> None:
    print("Deleted questions:")
    if not state.deleted_questions:
        print("  (none)")
        print()
        return

    for question_id in state.deleted_questions:
        print(f"  {question_id} (object removed, trace preserved)")
    print()


def print_reconstruction_events(state: WorldState) -> None:
    print("Reconstruction events:")
    if not state.reconstruction_events:
        print("  (none)")
        print()
        return

    for event in state.reconstruction_events:
        print(f"  {event}")
    print()


def print_question_identities(state: WorldState) -> None:
    print("Question identities:")
    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        origin = "reconstructed" if question.reconstructed_from_memory else "original/new"
        print(f"  [{question.id}] origin={origin} state={question.state}")
    print()

    for trace in sorted(state.memory_traces.values(), key=lambda t: t.trace_id):
        print(f"  [trace {trace.trace_id}] archived identity={trace.question_id}")
    print()


def print_history_preservation(state: WorldState) -> None:
    print("History preservation:")
    for trace in sorted(state.memory_traces.values(), key=lambda t: t.trace_id):
        print(f"  Trace [{trace.trace_id}]: {len(trace.lifecycle_history)} archived entries")

    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        print(f"  Question [{question.id}]: {len(question.lifecycle_history)} current entries")
        if question.reconstructed_from_memory:
            print("    prior history restored from ecosystem memory")
        for entry in question.lifecycle_history:
            print(f"    - {entry}")
    print()


def print_question_statistics(state: WorldState) -> None:
    print("Question statistics:")
    print(f"  Active questions: {len(state.lifecycle_questions)}")
    print(f"  Deleted questions: {len(state.deleted_questions)}")
    print(f"  Memory traces: {len(state.memory_traces)}")
    print(f"  Reconstruction events: {len(state.reconstruction_events)}")

    reconstructed = sum(
        1 for question in state.lifecycle_questions.values() if question.reconstructed_from_memory
    )
    print(f"  Reconstructed from memory: {reconstructed}")
    print(f"  New without memory: {len(state.lifecycle_questions) - reconstructed}")
    print()


def print_overall_organization(state: WorldState) -> None:
    print("Overall organization:")
    print(f"  Observations ingested: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Memory traces: {len(state.memory_traces)}")
    print(f"  Live questions: {len(state.lifecycle_questions)}")
    print(
        "  Organization path: observations -> differences -> tensions -> questions -> "
        "extinction -> memory -> reintroduction"
    )

    if state.reconstruction_events:
        outcome = (
            "reconstruction"
            if state.reconstruction_events[0].startswith("reconstruction:")
            else "new question"
        )
        print(f"  Reintroduction outcome: {outcome}")

    bird_question = state.lifecycle_questions.get(BIRD_QUESTION_ID)
    if bird_question:
        same_id = bird_question.id == BIRD_QUESTION_ID
        print(f"  Bird question id matches original: {same_id}")
        print(f"  Reconstructed from memory: {bird_question.reconstructed_from_memory}")
    print()


def main() -> None:
    print("=== EXP-015 Ecosystem Memory ===\n")
    print("Path: observations -> differences -> tensions -> questions -> extinction -> memory")
    print("After extinction: delete question objects, preserve memory traces")
    print(f"Reintroduction observations: {len(BIRD_REINTRO_CONFORMING + BIRD_REINTRO_CONTRADICTING)}\n")

    state = WorldState()
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_deletion(state)
    process_reintroduction(state)

    print_memory_traces(state)
    print_deleted_questions(state)
    print_reconstruction_events(state)
    print_question_identities(state)
    print_history_preservation(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
