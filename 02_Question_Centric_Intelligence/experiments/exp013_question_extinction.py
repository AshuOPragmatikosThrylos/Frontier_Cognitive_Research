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

TENSION_RESOLUTIONS = [
    ("t-bird-fly-vs-not_fly", "niche specialization resolves bird behavior conflict"),
]

DECAY_STEPS = [
    "eq-bird-fly-vs-not_fly",
    "eq-bird-fly-vs-not_fly",
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


@dataclass
class WorldState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)


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
    elif question.state == "EMERGENT":
        question.state = "EMERGENT"
    else:
        question.state = "ACTIVE"


def emerge_questions_from_tensions(state: WorldState) -> None:
    for tension in state.persistent_tensions:
        if not tension.persistent:
            continue
        if tension.id in {question.tension_id for question in state.lifecycle_questions.values()}:
            continue

        question_id = (
            f"eq-{tension.category.lower()}-{behavior_key(tension.behavior_a)}-vs-"
            f"{behavior_key(tension.behavior_b)}"
        )
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


def ingest_observations(state: WorldState) -> None:
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


def process_lifecycle(state: WorldState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in DECAY_STEPS:
        apply_vitality_decay(state, question_id)


def print_question_lifecycles(state: WorldState) -> None:
    print("Question lifecycles:")
    if not state.lifecycle_questions:
        print("  (none)")
        print()
        return

    for question in sorted(state.lifecycle_questions.values(), key=lambda q: q.id):
        print(f"  [{question.id}] final={question.state}")
        for entry in question.lifecycle_history:
            print(f"    - {entry}")
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


def print_resolved_tensions(state: WorldState) -> None:
    print("Resolved tensions:")
    resolved = [tension for tension in state.persistent_tensions if tension.resolved]
    if not resolved:
        print("  (none)")
        print()
        return

    for tension in resolved:
        print(
            f"  [{tension.id}] {tension.behavior_a} vs {tension.behavior_b} "
            f"(strength={tension.strength:.1f})"
        )
        print(f"    resolution: {tension.resolution_note}")
    print()


def print_extinct_questions(state: WorldState) -> None:
    print("Extinct questions:")
    extinct = [
        question for question in state.lifecycle_questions.values() if question.state == "EXTINCT"
    ]
    if not extinct:
        print("  (none)")
        print()
        return

    for question in sorted(extinct, key=lambda q: q.id):
        print(f"  [{question.id}] {question.text}")
        print(f"    final vitality={question.vitality:.1f}")
    print()


def print_question_statistics(state: WorldState) -> None:
    print("Question statistics:")
    total = len(state.lifecycle_questions)
    print(f"  Total questions: {total}")

    by_state: dict[str, int] = {}
    for question in state.lifecycle_questions.values():
        by_state[question.state] = by_state.get(question.state, 0) + 1

    for state_name in ["EMERGENT", "ACTIVE", "RESOLVED", "DORMANT", "EXTINCT"]:
        if state_name in by_state:
            print(f"  {state_name}: {by_state[state_name]}")

    resolved_tensions = sum(1 for tension in state.persistent_tensions if tension.resolved)
    unresolved_tensions = sum(
        1 for tension in state.persistent_tensions if tension.persistent and not tension.resolved
    )
    print(f"  Resolved tensions: {resolved_tensions}")
    print(f"  Unresolved tensions: {unresolved_tensions}")
    print()


def print_overall_organization(state: WorldState) -> None:
    print("Overall organization:")
    print(f"  Observations ingested: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Tensions detected: {len(state.persistent_tensions)}")
    print(f"  Questions tracked: {len(state.lifecycle_questions)}")
    print(
        "  Organization path: observations -> differences -> tensions -> questions -> lifecycle"
    )

    extinct_count = sum(
        1 for question in state.lifecycle_questions.values() if question.state == "EXTINCT"
    )
    active_count = sum(
        1 for question in state.lifecycle_questions.values() if question.state == "ACTIVE"
    )
    print(f"  Extinct questions: {extinct_count}")
    print(f"  Active questions: {active_count}")
    print()


def main() -> None:
    print("=== EXP-013 Question Extinction ===\n")
    print("Path: observations -> differences -> tensions -> emergent questions -> lifecycle")
    print(f"Difference min per group: {DIFFERENCE_MIN_PER_GROUP}")
    print(f"Persistent tension min: {PERSISTENT_TENSION_MIN}")
    print(f"Resolution vitality reduction: {RESOLUTION_VITALITY_REDUCTION}")
    print(f"Dormant vitality threshold: {DORMANT_VITALITY_THRESHOLD}")
    print(f"Decay vitality reduction: {DECAY_VITALITY_REDUCTION}\n")

    state = WorldState()
    ingest_observations(state)
    process_lifecycle(state)

    print_question_lifecycles(state)
    print_question_vitality(state)
    print_resolved_tensions(state)
    print_extinct_questions(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
