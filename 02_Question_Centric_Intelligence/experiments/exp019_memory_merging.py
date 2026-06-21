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
TRACE_STRENGTH_DIVISOR = 4.0
CO_ACTIVATION_MERGE_THRESHOLD = 2

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

BIRD_TENSION_ID = "t-bird-fly-vs-not_fly"
MAMMAL_TENSION_ID = "t-mammal-fly-vs-swim"
INSECT_TENSION_ID = "t-insect-fly-vs-crawl"

BIRD_QUESTION_ID = "eq-bird-fly-vs-not_fly"
MAMMAL_QUESTION_ID = "eq-mammal-fly-vs-swim"
INSECT_QUESTION_ID = "eq-insect-fly-vs-crawl"

ALL_TENSION_IDS = [BIRD_TENSION_ID, MAMMAL_TENSION_ID, INSECT_TENSION_ID]
ALL_QUESTION_IDS = [BIRD_QUESTION_ID, MAMMAL_QUESTION_ID, INSECT_QUESTION_ID]


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
class MemoryAbstraction:
    abstraction_id: str
    source_trace_ids: list[str]
    source_question_ids: list[str]
    tension_ids: list[str]
    categories: list[str]
    text: str
    merged_history: list[str]
    trace_strength: float


@dataclass
class ExperimentState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    abstractions: dict[str, MemoryAbstraction] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    co_activation_counts: dict[frozenset[str], int] = field(default_factory=dict)
    co_activation_events: list[str] = field(default_factory=list)
    merge_events: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_observation(
    state: ExperimentState,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: ExperimentState, category: str) -> None:
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


def refresh_group_members(state: ExperimentState, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def groups_for_category(state: ExperimentState, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: ExperimentState, category: str) -> list[PersistentTension]:
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


def record_tensions(state: ExperimentState, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: ExperimentState, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def memory_trace_for_tension(state: ExperimentState, tension_id: str) -> MemoryTrace | None:
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


def emerge_questions_from_tensions(state: ExperimentState) -> None:
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


def promote_emergent_questions(state: ExperimentState) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: ExperimentState, tension_id: str, note: str) -> None:
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


def apply_vitality_decay(state: ExperimentState, question_id: str) -> None:
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


def drive_question_to_extinction(state: ExperimentState, question_id: str) -> None:
    while True:
        question = state.lifecycle_questions.get(question_id)
        if question is None or question.state == "EXTINCT":
            return
        apply_vitality_decay(state, question_id)


def trace_strength_from_tension(tension: PersistentTension | None) -> float:
    if tension is None:
        return 0.5
    return min(INITIAL_TRACE_STRENGTH, tension.strength / TRACE_STRENGTH_DIVISOR)


def archive_and_delete_extinct_questions(state: ExperimentState) -> None:
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


def reopen_tension(state: ExperimentState, tension_id: str) -> None:
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


def ingest_category_observations(
    state: ExperimentState,
    category: str,
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            register_observation(state, entity, obs_category, behavior)
    form_difference_groups(state, category)
    record_tensions(state, category)


def ingest_initial_observations(state: ExperimentState) -> None:
    ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
    ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
    ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])


def process_extinction_lifecycle(state: ExperimentState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in ALL_QUESTION_IDS:
        drive_question_to_extinction(state, question_id)


def process_memory_deletion(state: ExperimentState) -> None:
    archive_and_delete_extinct_questions(state)


def active_traces_for_tensions(
    state: ExperimentState,
    tension_ids: list[str],
) -> list[MemoryTrace]:
    active: list[MemoryTrace] = []
    for tension_id in tension_ids:
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            continue
        trace = memory_trace_for_tension(state, tension_id)
        if trace is not None:
            active.append(trace)
    return sorted(active, key=lambda trace: trace.trace_id)


def record_co_activation(state: ExperimentState, round_label: str, active_traces: list[MemoryTrace]) -> None:
    trace_ids = [trace.trace_id for trace in active_traces]
    state.co_activation_events.append(
        f"{round_label}: co-activated {trace_ids}"
    )

    if len(active_traces) < 2:
        return

    pair_key = frozenset(trace.trace_id for trace in active_traces)
    state.co_activation_counts[pair_key] = state.co_activation_counts.get(pair_key, 0) + 1
    state.co_activation_events.append(
        f"{round_label}: pair count {sorted(pair_key)} -> "
        f"{state.co_activation_counts[pair_key]}"
    )


def build_merged_history(source_traces: list[MemoryTrace]) -> list[str]:
    merged: list[str] = []
    for trace in source_traces:
        merged.append(f"--- inherited from {trace.trace_id} ({trace.question_id}) ---")
        merged.extend(trace.lifecycle_history)
    merged.append("MERGED into abstraction")
    return merged


def emergent_abstraction_text(source_traces: list[MemoryTrace]) -> str:
    categories = sorted({trace.category for trace in source_traces})
    category_text = " and ".join(categories)
    return f"Why do {category_text} entities show multiple behavior conflicts?"


def merge_traces(state: ExperimentState, trace_ids: list[str]) -> MemoryAbstraction | None:
    source_traces = sorted(
        (state.memory_traces[tid] for tid in trace_ids if tid in state.memory_traces),
        key=lambda trace: trace.trace_id,
    )
    if len(source_traces) < 2:
        return None

    slug = "-".join(
        sorted(trace.question_id.replace("eq-", "") for trace in source_traces)
    )
    abstraction_id = f"mem-abstract-{slug}"
    abstraction = MemoryAbstraction(
        abstraction_id=abstraction_id,
        source_trace_ids=[trace.trace_id for trace in source_traces],
        source_question_ids=[trace.question_id for trace in source_traces],
        tension_ids=sorted({trace.tension_id for trace in source_traces}),
        categories=sorted({trace.category for trace in source_traces}),
        text=emergent_abstraction_text(source_traces),
        merged_history=build_merged_history(source_traces),
        trace_strength=sum(trace.trace_strength for trace in source_traces),
    )

    for trace in source_traces:
        del state.memory_traces[trace.trace_id]

    state.abstractions[abstraction_id] = abstraction
    state.merge_events.append(
        f"merged: {[t.trace_id for t in source_traces]} -> {abstraction_id} "
        f"(strength={abstraction.trace_strength:.2f})"
    )
    state.merge_events.append(
        f"  inherited question ids: {abstraction.source_question_ids}"
    )
    return abstraction


def try_merge_coactivated_traces(state: ExperimentState) -> None:
    for pair_key, count in sorted(
        state.co_activation_counts.items(),
        key=lambda item: (sorted(item[0]), item[1]),
    ):
        if count < CO_ACTIVATION_MERGE_THRESHOLD:
            continue
        trace_ids = sorted(pair_key)
        if not all(tid in state.memory_traces for tid in trace_ids):
            continue
        merge_traces(state, trace_ids)


def run_co_activation_round(
    state: ExperimentState,
    round_label: str,
    tension_ids: list[str],
    categories: list[str],
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for category, groups in zip(categories, _split_groups_by_category(categories, observation_groups)):
        ingest_category_observations(state, category, groups)
        refresh_group_members(state, category)

    for tension_id in tension_ids:
        reopen_tension(state, tension_id)

    active_traces = active_traces_for_tensions(state, tension_ids)
    record_co_activation(state, round_label, active_traces)
    try_merge_coactivated_traces(state)


def _split_groups_by_category(
    categories: list[str],
    observation_groups: list[list[tuple[str, str, str]]],
) -> list[list[list[tuple[str, str, str]]]]:
    if not observation_groups:
        return [[] for _ in categories]

    by_category: dict[str, list[list[tuple[str, str, str]]]] = {cat: [] for cat in categories}
    for group in observation_groups:
        if not group:
            continue
        category = group[0][1]
        by_category[category].append(group)
    return [by_category[cat] for cat in categories]


def process_co_activation_and_merging(state: ExperimentState) -> None:
    run_co_activation_round(
        state,
        "round 1",
        [BIRD_TENSION_ID],
        ["Bird"],
        [BIRD_REINTRO_CONFORMING, BIRD_REINTRO_CONTRADICTING],
    )
    run_co_activation_round(
        state,
        "round 2",
        [MAMMAL_TENSION_ID, INSECT_TENSION_ID],
        ["Mammal", "Insect"],
        [MAMMAL_REINTRO_FLY, MAMMAL_REINTRO_SWIM, INSECT_REINTRO_FLY, INSECT_REINTRO_CRAWL],
    )
    run_co_activation_round(
        state,
        "round 3",
        [MAMMAL_TENSION_ID, INSECT_TENSION_ID],
        [],
        [],
    )


def run_experiment() -> ExperimentState:
    state = ExperimentState()
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_deletion(state)
    process_co_activation_and_merging(state)
    return state


def identity_preserved_in_abstraction(abstraction: MemoryAbstraction, question_id: str) -> bool:
    return question_id in abstraction.source_question_ids


def print_memory_traces(state: ExperimentState) -> None:
    print("=== Memory Traces ===\n")
    if not state.memory_traces:
        print("  (none remaining — all merged or absent)")
        print()
        return

    for trace_id in sorted(state.memory_traces):
        trace = state.memory_traces[trace_id]
        print(f"  {trace_id}:")
        print(f"    question_id={trace.question_id}")
        print(f"    tension_id={trace.tension_id}")
        print(f"    strength={trace.trace_strength:.2f}")
    print()


def print_merge_events(state: ExperimentState) -> None:
    print("=== Merge Events ===\n")
    if not state.merge_events:
        print("  (none)")
        print()
        return

    for event in state.merge_events:
        print(f"  {event}")
    print()


def print_inherited_histories(state: ExperimentState) -> None:
    print("=== Inherited Histories ===\n")
    if not state.abstractions:
        print("  (none)")
        print()
        return

    for abstraction_id in sorted(state.abstractions):
        abstraction = state.abstractions[abstraction_id]
        print(f"  {abstraction_id}:")
        print(f"    sources: {abstraction.source_question_ids}")
        for entry in abstraction.merged_history:
            print(f"    {entry}")
        print()


def print_new_abstractions(state: ExperimentState) -> None:
    print("=== New Abstractions ===\n")
    if not state.abstractions:
        print("  (none)")
        print()
        return

    for abstraction_id in sorted(state.abstractions):
        abstraction = state.abstractions[abstraction_id]
        print(f"  {abstraction_id}:")
        print(f"    text: {abstraction.text}")
        print(f"    categories: {abstraction.categories}")
        print(f"    tension_ids: {abstraction.tension_ids}")
        print(f"    strength: {abstraction.trace_strength:.2f}")
        print(f"    source_traces: {abstraction.source_trace_ids}")
    print()


def print_question_statistics(state: ExperimentState) -> None:
    print("=== Question Statistics ===\n")
    print(f"  Deleted (archived): {len(state.deleted_questions)}")
    print(f"  Remaining traces: {len(state.memory_traces)}")
    print(f"  Abstractions: {len(state.abstractions)}")
    print(f"  Co-activation events: {len(state.co_activation_events)}")
    print(f"  Merge events: {len(state.merge_events)}")
    print()

    for question_id in ALL_QUESTION_IDS:
        in_trace = any(t.question_id == question_id for t in state.memory_traces.values())
        in_abstraction = any(
            question_id in abs_.source_question_ids for abs_ in state.abstractions.values()
        )
        if in_trace:
            print(f"  {question_id}: preserved in individual trace")
        elif in_abstraction:
            print(f"  {question_id}: preserved in merged abstraction")
        else:
            print(f"  {question_id}: (not found)")
    print()


def print_overall_organization(state: ExperimentState) -> None:
    print("=== Overall Organization ===\n")
    print(f"  Observations: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Memory traces: {len(state.memory_traces)}")
    print(f"  Abstractions: {len(state.abstractions)}")
    print(f"  Co-activation merge threshold: {CO_ACTIVATION_MERGE_THRESHOLD}")
    print()

    print("  Identity preservation:")
    for question_id in ALL_QUESTION_IDS:
        preserved = any(
            identity_preserved_in_abstraction(abs_, question_id)
            for abs_ in state.abstractions.values()
        ) or any(
            t.question_id == question_id for t in state.memory_traces.values()
        )
        status = "preserved" if preserved else "lost"
        print(f"    {question_id}: {status}")
    print()

    print("  Co-activation log:")
    for event in state.co_activation_events:
        print(f"    {event}")
    print()


def main() -> None:
    print("=== EXP-019 Memory Trace Merging ===\n")
    print("Pipeline: observations -> differences -> tensions -> questions -> extinction -> traces")
    print("Co-activation: repeated joint activation; traces merge into abstractions")
    print(f"Merge threshold: {CO_ACTIVATION_MERGE_THRESHOLD} co-activations\n")

    state = run_experiment()

    print_memory_traces(state)
    print_merge_events(state)
    print_inherited_histories(state)
    print_new_abstractions(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
