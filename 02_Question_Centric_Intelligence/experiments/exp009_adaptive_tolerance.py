import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

CONTRADICTION_INCREMENT = 1.0
TOLERANCE_LEARN_RATE = 0.35
PRESSURE_SPLIT_LIMIT = 1.0

INITIAL_TOLERANCES: dict[str, float] = {
    "Bird": 1.5,
    "Mammal": 4.0,
}


@dataclass
class Community:
    name: str
    expectation: str
    contradiction_tolerance: float
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    contradiction_debt: float = 0.0
    contradictions: list[str] = field(default_factory=list)


COMMUNITIES: dict[str, Community] = {
    "Bird": Community(name="Bird", expectation="fly", contradiction_tolerance=INITIAL_TOLERANCES["Bird"]),
    "Mammal": Community(name="Mammal", expectation="ground", contradiction_tolerance=INITIAL_TOLERANCES["Mammal"]),
}

SPECIATION_EVENTS: list[str] = []
TOLERANCE_LOG: list[dict] = []


def observe(engine: CuriosityEngine, world_model: WorldModel, entity: str, category: str, behavior: str) -> None:
    expected = world_model.predict(category)
    behavior = behavior.lower()
    content = f"{entity} {behavior}"

    if expected and behavior != expected:
        engine.process_prediction_failure(entity, category, behavior, content)
        return

    if expected is None:
        for rule_category, rule_behavior in world_model.rules.items():
            if rule_behavior == behavior and rule_category != category:
                engine.process_prediction_failure(entity, category, behavior, content)
                return


def pressure_level(community: Community) -> float:
    return max(0.0, community.contradiction_debt - community.contradiction_tolerance)


def log_tolerances(label: str) -> None:
    TOLERANCE_LOG.append({
        "label": label,
        "tolerances": {name: COMMUNITIES[name].contradiction_tolerance for name in COMMUNITIES},
        "debts": {name: COMMUNITIES[name].contradiction_debt for name in COMMUNITIES},
        "pressures": {name: pressure_level(COMMUNITIES[name]) for name in COMMUNITIES},
    })


def add_conforming_question(
    repository: QuestionRepository,
    community: Community,
    entity: str,
    observed: str,
    category: str = "Bird",
) -> Question:
    question = Question(
        id=f"q-{entity.lower()}",
        text=f"How does {entity} {observed}?",
        state="ACTIVE",
        category=category,
        expected_behavior=community.expectation,
        observed_behavior=observed,
        curiosity_debt=1.0,
    )
    repository.add_question(question)
    community.members.append(question.id)
    return question


def record_contradiction(
    engine: CuriosityEngine,
    world_model: WorldModel,
    repository: QuestionRepository,
    community_name: str,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    community = COMMUNITIES[community_name]
    behavior = behavior.lower()

    observe(engine, world_model, entity, category, behavior)
    question_id = f"q-{entity.lower()}"
    if question_id not in community.members:
        community.members.append(question_id)

    community.contradiction_debt += CONTRADICTION_INCREMENT
    community.contradiction_tolerance += TOLERANCE_LEARN_RATE
    community.contradictions.append(
        f"{entity}: expected {community.expectation}, observed {behavior}"
    )


def process_observation(
    engine: CuriosityEngine,
    world_model: WorldModel,
    repository: QuestionRepository,
    community_name: str,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    community = COMMUNITIES[community_name]
    behavior = behavior.lower()

    if behavior == community.expectation:
        observe(engine, world_model, entity, category, behavior)
        add_conforming_question(repository, community, entity, behavior, category)
        return

    record_contradiction(engine, world_model, repository, community_name, entity, category, behavior)


def should_split(community: Community) -> bool:
    return pressure_level(community) >= PRESSURE_SPLIT_LIMIT


def split_by_contradiction(repository: QuestionRepository, parent_name: str) -> list[str]:
    parent = COMMUNITIES[parent_name]
    conforming: list[str] = []
    contradicting: list[str] = []

    for question_id in parent.members:
        question = repository.get_question(question_id)
        if question is None:
            continue
        if question.observed_behavior == parent.expectation:
            conforming.append(question_id)
        else:
            contradicting.append(question_id)

    created: list[str] = []
    for suffix, member_ids, expectation in [
        ("Conforming", conforming, parent.expectation),
        ("Contradicting", contradicting, "anomaly"),
    ]:
        if not member_ids:
            continue
        child_name = f"{parent_name}.{suffix}"
        child = Community(
            name=child_name,
            expectation=expectation,
            contradiction_tolerance=parent.contradiction_tolerance,
            parent=parent_name,
            members=list(member_ids),
        )
        COMMUNITIES[child_name] = child
        parent.children.append(child_name)
        created.append(child_name)

    pressure = pressure_level(parent)
    SPECIATION_EVENTS.append(
        f"{parent_name} split -> {created} (pressure={pressure:.2f}, tolerance={parent.contradiction_tolerance:.2f})"
    )
    parent.members = []
    return created


def try_split_all(repository: QuestionRepository, label: str) -> None:
    for name in list(COMMUNITIES):
        community = COMMUNITIES[name]
        if community.members and should_split(community):
            split_by_contradiction(repository, name)
    log_tolerances(label)


def print_community_tolerances() -> None:
    print("Community tolerances:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        initial = INITIAL_TOLERANCES.get(name.split(".")[0], community.contradiction_tolerance)
        print(f"  {name}: current={community.contradiction_tolerance:.2f} (initial={initial:.2f})")
    print()

    print("Tolerance history:")
    for entry in TOLERANCE_LOG:
        parts = ", ".join(
            f"{n}: tol={entry['tolerances'][n]:.2f} debt={entry['debts'][n]:.1f} pressure={entry['pressures'][n]:.2f}"
            for n in sorted(entry["tolerances"])
            if n in entry["tolerances"]
        )
        print(f"  {entry['label']}: {parts}")
    print()


def print_contradiction_debt() -> None:
    print("Contradiction debt:")
    for name in sorted(COMMUNITIES):
        print(f"  {name}: {COMMUNITIES[name].contradiction_debt:.1f}")
    print()


def print_pressure_levels() -> None:
    print("Pressure levels:")
    for name in sorted(COMMUNITIES):
        level = pressure_level(COMMUNITIES[name])
        status = "SPLIT" if level >= PRESSURE_SPLIT_LIMIT else "stable"
        print(f"  {name}: {level:.2f} ({status})")
    print()


def print_speciation_events() -> None:
    print("Speciation events:")
    if not SPECIATION_EVENTS:
        print("  (none)")
    for event in SPECIATION_EVENTS:
        print(f"  {event}")
    print()


def print_community_structures() -> None:
    print("Community structures:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        members = ", ".join(community.members) if community.members else "(none)"
        print(f"  {name}: members=[{members}]")
    print()


def print_community_statistics(repository: QuestionRepository) -> None:
    print("Community statistics:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        member_debt = sum(
            repository.get_question(qid).curiosity_debt
            for qid in community.members
            if repository.get_question(qid) is not None
        )
        print(
            f"  {name}: tolerance={community.contradiction_tolerance:.2f} "
            f"members={len(community.members)} contradiction_debt={community.contradiction_debt:.1f} "
            f"member_curiosity_debt={member_debt:.1f} pressure={pressure_level(community):.2f}"
        )
    print()


def print_question_states(repository: QuestionRepository) -> None:
    print("Question states:")
    for question in sorted(repository.get_all_questions(), key=lambda q: q.id):
        print(f"  [{question.id}] {question.state} — {question.text}")
    print()


def main() -> None:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    bird_conforming = [
        ("Sparrow", "Bird", "fly"),
        ("Robin", "Bird", "fly"),
        ("Eagle", "Bird", "fly"),
        ("Falcon", "Bird", "fly"),
    ]

    bird_contradicting = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
    ]

    mammal_contradicting = [
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
    ]

    print("=== EXP-009 Adaptive Contradiction Tolerance ===\n")
    print(f"Initial tolerances: {INITIAL_TOLERANCES}")
    print(f"Tolerance learn rate: {TOLERANCE_LEARN_RATE}")
    print(f"Pressure split limit: {PRESSURE_SPLIT_LIMIT}\n")

    for entity, category, behavior in bird_conforming:
        process_observation(engine, world_model, repository, "Bird", entity, category, behavior)

    log_tolerances("after bird conforming")

    for entity, category, behavior in bird_contradicting:
        process_observation(engine, world_model, repository, "Bird", entity, category, behavior)

    try_split_all(repository, "after bird contradictions")

    for entity, category, behavior in mammal_contradicting:
        record_contradiction(engine, world_model, repository, "Mammal", entity, category, behavior)

    try_split_all(repository, "after mammal contradictions")

    print_community_tolerances()
    print_contradiction_debt()
    print_pressure_levels()
    print_speciation_events()
    print_community_structures()
    print_community_statistics(repository)
    print_question_states(repository)


if __name__ == "__main__":
    main()
