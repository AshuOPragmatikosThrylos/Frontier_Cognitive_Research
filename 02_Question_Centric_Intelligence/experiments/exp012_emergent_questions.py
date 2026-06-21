import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2

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

ALL_OBSERVATIONS = BIRD_CONFORMING + BIRD_CONTRADICTING + MAMMAL_CONTRADICTING


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


@dataclass
class EmergentQuestion:
    id: str
    text: str
    category: str
    source_groups: list[str]
    tension_id: str
    state: str = "EMERGENT"


@dataclass
class WorldState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    emergent_questions: dict[str, EmergentQuestion] = field(default_factory=dict)


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
        group for group in state.difference_groups.values() if group.category == category
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


def emerge_questions_from_tensions(state: WorldState) -> None:
    for tension in state.persistent_tensions:
        if not tension.persistent:
            continue
        if tension.id in {question.tension_id for question in state.emergent_questions.values()}:
            continue

        question_id = (
            f"eq-{tension.category.lower()}-{behavior_key(tension.behavior_a)}-vs-"
            f"{behavior_key(tension.behavior_b)}"
        )
        state.emergent_questions[question_id] = EmergentQuestion(
            id=question_id,
            text=(
                f"Why do {tension.category} entities both {tension.behavior_a} "
                f"and {tension.behavior_b}?"
            ),
            category=tension.category,
            source_groups=[tension.group_a, tension.group_b],
            tension_id=tension.id,
        )


def process_observations(state: WorldState) -> None:
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

    emerge_questions_from_tensions(state)


def print_observations(state: WorldState) -> None:
    print("Raw observations (no questions instantiated):")
    for index, observation in enumerate(state.observations, start=1):
        print(
            f"  {index}. {observation.entity} ({observation.category}): "
            f"{observation.behavior}"
        )
    print()


def print_difference_groups(state: WorldState) -> None:
    print("Difference groups:")
    if not state.difference_groups:
        print("  (none)")
        print()
        return

    for name in sorted(state.difference_groups):
        group = state.difference_groups[name]
        members = ", ".join(group.members)
        print(f"  {name}: behavior={group.behavior} members=[{members}]")
    print()


def print_persistent_tensions(state: WorldState) -> None:
    print("Persistent tensions:")
    if not state.persistent_tensions:
        print("  (none)")
        print()
        return

    for tension in state.persistent_tensions:
        status = "persistent" if tension.persistent else "transient"
        print(
            f"  [{tension.id}] {tension.category}: {tension.behavior_a} vs "
            f"{tension.behavior_b} (strength={tension.strength:.1f}, {status})"
        )
        print(f"    groups: {tension.group_a} <-> {tension.group_b}")
    print()


def print_emergent_questions(state: WorldState) -> None:
    print("Emergent questions:")
    if not state.emergent_questions:
        print("  (none)")
        print()
        return

    for question in sorted(state.emergent_questions.values(), key=lambda q: q.id):
        groups = ", ".join(question.source_groups)
        print(f"  [{question.id}] {question.state} — {question.text}")
        print(f"    category={question.category} tension={question.tension_id} sources=[{groups}]")
    print()


def print_question_statistics(state: WorldState) -> None:
    print("Question statistics:")
    total = len(state.emergent_questions)
    print(f"  Total emergent questions: {total}")

    by_category: dict[str, int] = {}
    for question in state.emergent_questions.values():
        by_category[question.category] = by_category.get(question.category, 0) + 1

    if by_category:
        print("  By category:")
        for category in sorted(by_category):
            print(f"    {category}: {by_category[category]}")
    else:
        print("  By category: (none)")

    persistent_count = sum(1 for tension in state.persistent_tensions if tension.persistent)
    print(f"  Persistent tensions: {persistent_count}")
    print(f"  Questions per persistent tension: {total / persistent_count if persistent_count else 0:.2f}")
    print()


def print_overall_organization(state: WorldState) -> None:
    print("Overall organization:")
    print(f"  Observations ingested: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Tensions detected: {len(state.persistent_tensions)}")
    print(
        f"  Persistent unresolved tensions: "
        f"{sum(1 for t in state.persistent_tensions if t.persistent)}"
    )
    print(f"  Emergent questions: {len(state.emergent_questions)}")

    if state.emergent_questions:
        print("  Organization path: observations -> difference groups -> tension -> questions")
    elif state.difference_groups:
        print("  Organization path: observations -> difference groups (no emergent questions)")
    else:
        print("  Organization path: observations only (no groups formed)")

    bird_question = any(q.category == "Bird" for q in state.emergent_questions.values())
    mammal_question = any(q.category == "Mammal" for q in state.emergent_questions.values())
    print(f"  Bird question emerged: {bird_question}")
    print(f"  Mammal question emerged: {mammal_question}")
    print()


def main() -> None:
    print("=== EXP-012 Emergent Questions ===\n")
    print("Start: observations only (no Question objects)")
    print("Path: observations -> difference groups -> persistent tension -> emergent questions")
    print(f"Observation sequence: {len(ALL_OBSERVATIONS)} observations")
    print(f"Difference min per group: {DIFFERENCE_MIN_PER_GROUP}")
    print(f"Persistent tension min: {PERSISTENT_TENSION_MIN}\n")

    state = WorldState()
    process_observations(state)

    print_observations(state)
    print_difference_groups(state)
    print_persistent_tensions(state)
    print_emergent_questions(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
