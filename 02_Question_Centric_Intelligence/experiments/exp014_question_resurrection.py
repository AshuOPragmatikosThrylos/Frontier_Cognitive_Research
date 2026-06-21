import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0
RESURRECTION_VITALITY = 3.0

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

BIRD_REVIVAL_CONFORMING = [
    ("Crow", "Bird", "fly"),
    ("Raven", "Bird", "fly"),
]

BIRD_REVIVAL_CONTRADICTING = [
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


@dataclass
class WorldState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    resurrection_events: list[str] = field(default_factory=list)


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


def questions_for_tension(state: WorldState, tension_id: str) -> list[LifecycleQuestion]:
    return [
        question
        for question in state.lifecycle_questions.values()
        if question.tension_id == tension_id
    ]


def apply_lifecycle_state(question: LifecycleQuestion, tension_resolved: bool) -> None:
    if question.vitality <= 0.0:
        question.state = "EXTINCT"
    elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
        question.state = "DORMANT"
    elif tension_resolved:
        question.state = "RESOLVED"
    elif question.state in ("EMERGENT", "RESURRECTED"):
        pass
    else:
        question.state = "ACTIVE"


def question_id_for_tension(tension: PersistentTension) -> str:
    return (
        f"eq-{tension.category.lower()}-{behavior_key(tension.behavior_a)}-vs-"
        f"{behavior_key(tension.behavior_b)}"
    )


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

    for question in questions_for_tension(state, tension_id):
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


def recreate_question(state: WorldState, tension: PersistentTension) -> str:
    recreation_id = f"{question_id_for_tension(tension)}-recreated"
    question = LifecycleQuestion(
        id=recreation_id,
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
        f"EMERGENT (recreated, vitality={question.vitality:.1f}, tension={tension.id})"
    )
    state.lifecycle_questions[recreation_id] = question
    question.state = "ACTIVE"
    question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")
    return recreation_id


def try_resurrect_or_recreate(state: WorldState, tension_id: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None or not tension.persistent:
        state.resurrection_events.append(f"{tension_id}: no action (tension not persistent)")
        return

    extinct_questions = [
        question for question in questions_for_tension(state, tension_id)
        if question.state == "EXTINCT"
    ]

    if extinct_questions:
        question = extinct_questions[0]
        previous_history_len = len(question.lifecycle_history)
        question.vitality = RESURRECTION_VITALITY
        question.state = "RESURRECTED"
        question.lifecycle_history.append(
            f"EXTINCT -> RESURRECTED (vitality={question.vitality:.1f}, tension reopened)"
        )
        question.state = "ACTIVE"
        question.lifecycle_history.append("RESURRECTED -> ACTIVE (promoted)")
        state.resurrection_events.append(
            f"resurrection: {question.id} (identity preserved, "
            f"history entries={previous_history_len} -> {len(question.lifecycle_history)})"
        )
        return

    recreation_id = recreate_question(state, tension)
    state.resurrection_events.append(
        f"recreation: {recreation_id} (new identity, no prior history)"
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


def process_revival(state: WorldState) -> None:
    for entity, category, behavior in BIRD_REVIVAL_CONFORMING:
        register_observation(state, entity, category, behavior)

    for entity, category, behavior in BIRD_REVIVAL_CONTRADICTING:
        register_observation(state, entity, category, behavior)

    refresh_group_members(state, "Bird")
    reopen_tension(state, BIRD_TENSION_ID)
    try_resurrect_or_recreate(state, BIRD_TENSION_ID)


def extract_transitions(history: list[str]) -> list[str]:
    transitions: list[str] = []
    for entry in history:
        if " -> " in entry:
            transitions.append(entry.split(" (")[0])
        elif entry.startswith("EMERGENT"):
            transitions.append("birth: EMERGENT")
        elif entry.startswith("tension resolved"):
            transitions.append("event: tension resolved")
        elif entry.startswith("vitality decay"):
            transitions.append(entry.split(" (")[0])
    return transitions


def print_question_histories(state: WorldState) -> None:
    print("Question histories:")
    if not state.lifecycle_questions:
        print("  (none)")
        print()
        return

    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        print(f"  [{question.id}] final={question.state}")
        for entry in question.lifecycle_history:
            print(f"    - {entry}")
    print()


def print_lifecycle_transitions(state: WorldState) -> None:
    print("Lifecycle transitions:")
    if not state.lifecycle_questions:
        print("  (none)")
        print()
        return

    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        transitions = extract_transitions(question.lifecycle_history)
        print(f"  [{question.id}]")
        for transition in transitions:
            print(f"    {transition}")
    print()


def print_resurrection_events(state: WorldState) -> None:
    print("Resurrection events:")
    if not state.resurrection_events:
        print("  (none)")
        print()
        return

    for event in state.resurrection_events:
        print(f"  {event}")
    print()


def print_question_vitality(state: WorldState) -> None:
    print("Question vitality:")
    if not state.lifecycle_questions:
        print("  (none)")
        print()
        return

    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        print(
            f"  [{question.id}] vitality={question.vitality:.1f} state={question.state} "
            f"tension={question.tension_id}"
        )
    print()


def print_question_statistics(state: WorldState) -> None:
    print("Question statistics:")
    total = len(state.lifecycle_questions)
    print(f"  Total questions: {total}")

    by_state: dict[str, int] = {}
    for question in state.lifecycle_questions.values():
        by_state[question.state] = by_state.get(question.state, 0) + 1

    for state_name in [
        "EMERGENT", "ACTIVE", "RESOLVED", "DORMANT", "EXTINCT", "RESURRECTED",
    ]:
        if state_name in by_state:
            print(f"  {state_name}: {by_state[state_name]}")

    resurrected = sum(1 for event in state.resurrection_events if event.startswith("resurrection:"))
    recreated = sum(1 for event in state.resurrection_events if event.startswith("recreation:"))
    print(f"  Resurrection events: {resurrected}")
    print(f"  Recreation events: {recreated}")
    print(f"  Total history entries (bird question): "
          f"{len(state.lifecycle_questions[BIRD_QUESTION_ID].lifecycle_history) if BIRD_QUESTION_ID in state.lifecycle_questions else 0}")
    print()


def print_overall_organization(state: WorldState) -> None:
    print("Overall organization:")
    print(f"  Observations ingested: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Tensions detected: {len(state.persistent_tensions)}")

    bird_tension = get_tension(state, BIRD_TENSION_ID)
    if bird_tension:
        print(
            f"  Bird tension: strength={bird_tension.strength:.1f} "
            f"resolved={bird_tension.resolved} persistent={bird_tension.persistent}"
        )

    print(f"  Questions tracked: {len(state.lifecycle_questions)}")
    print(
        "  Organization path: observations -> differences -> tensions -> questions -> "
        "lifecycle -> extinction -> revival"
    )

    active_count = sum(
        1 for question in state.lifecycle_questions.values() if question.state == "ACTIVE"
    )
    extinct_count = sum(
        1 for question in state.lifecycle_questions.values() if question.state == "EXTINCT"
    )
    print(f"  Active questions: {active_count}")
    print(f"  Extinct questions: {extinct_count}")

    if state.resurrection_events:
        outcome = "resurrection" if state.resurrection_events[0].startswith("resurrection:") else "recreation"
        print(f"  Revival outcome: {outcome}")
    print()


def main() -> None:
    print("=== EXP-014 Question Resurrection ===\n")
    print("Path: observations -> differences -> tensions -> questions -> lifecycle -> revival")
    print(f"Revival observations: {len(BIRD_REVIVAL_CONFORMING + BIRD_REVIVAL_CONTRADICTING)}")
    print(f"Resurrection vitality: {RESURRECTION_VITALITY}\n")

    state = WorldState()
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_revival(state)

    print_question_histories(state)
    print_lifecycle_transitions(state)
    print_resurrection_events(state)
    print_question_vitality(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
