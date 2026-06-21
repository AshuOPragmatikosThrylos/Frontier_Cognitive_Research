import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

PRESSURE_SPLIT_LIMIT = 4.0
CONTRADICTION_INCREMENT = 1.0


@dataclass
class Community:
    name: str
    expectation: str
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    contradiction_debt: float = 0.0
    contradictions: list[str] = field(default_factory=list)


COMMUNITIES: dict[str, Community] = {
    "Bird": Community(name="Bird", expectation="fly"),
}

SPECIATION_EVENTS: list[str] = []


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


def add_conforming_question(
    repository: QuestionRepository,
    community: Community,
    entity: str,
    observed: str,
) -> Question:
    question = Question(
        id=f"q-{entity.lower()}",
        text=f"How does {entity} {observed}?",
        state="ACTIVE",
        category="Bird",
        expected_behavior=community.expectation,
        observed_behavior=observed,
        curiosity_debt=1.0,
    )
    repository.add_question(question)
    community.members.append(question.id)
    return question


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
        add_conforming_question(repository, community, entity, behavior)
        return

    observe(engine, world_model, entity, category, behavior)
    question_id = f"q-{entity.lower()}"
    if question_id not in community.members:
        community.members.append(question_id)

    community.contradiction_debt += CONTRADICTION_INCREMENT
    community.contradictions.append(
        f"{entity}: expected {community.expectation}, observed {behavior}"
    )


def pressure_level(community: Community) -> float:
    return community.contradiction_debt


def should_split_by_pressure(community: Community) -> bool:
    return community.contradiction_debt >= PRESSURE_SPLIT_LIMIT


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
    splits = [
        ("Conforming", conforming, parent.expectation),
        ("Contradicting", contradicting, "anomaly"),
    ]

    for suffix, member_ids, expectation in splits:
        if not member_ids:
            continue
        child_name = f"{parent_name}.{suffix}"
        child = Community(
            name=child_name,
            expectation=expectation,
            parent=parent_name,
            members=list(member_ids),
        )
        COMMUNITIES[child_name] = child
        parent.children.append(child_name)
        created.append(child_name)

    event = f"{parent_name} split -> {created} (pressure={parent.contradiction_debt:.1f})"
    SPECIATION_EVENTS.append(event)

    parent.members = []
    return created


def print_community_expectations() -> None:
    print("Community expectations:")
    for name in sorted(COMMUNITIES):
        print(f"  {name}: {COMMUNITIES[name].expectation}")
    print()


def print_contradictions_encountered() -> None:
    print("Contradictions encountered:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        if not community.contradictions:
            print(f"  {name}: (none)")
            continue
        print(f"  {name}:")
        for entry in community.contradictions:
            print(f"    - {entry}")
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
        print(f"  {name}: {level:.1f} ({status})")
    print()


def print_community_structures() -> None:
    print("Community structures:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        members = ", ".join(community.members) if community.members else "(none)"
        print(f"  {name}: members=[{members}]")
    print()


def print_speciation_events() -> None:
    print("Speciation events:")
    if not SPECIATION_EVENTS:
        print("  (none)")
    for event in SPECIATION_EVENTS:
        print(f"  {event}")
    print()


def print_question_states(repository: QuestionRepository) -> None:
    print("Question states:")
    for question in sorted(repository.get_all_questions(), key=lambda q: q.id):
        print(f"  [{question.id}] {question.state} — {question.text}")
    print()


def main() -> None:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    conforming_observations = [
        ("Sparrow", "Bird", "fly"),
        ("Robin", "Bird", "fly"),
        ("Eagle", "Bird", "fly"),
        ("Falcon", "Bird", "fly"),
    ]

    contradicting_observations = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
    ]

    print("=== EXP-008 Contradiction Pressure ===\n")
    print(f"Pressure split limit: {PRESSURE_SPLIT_LIMIT}\n")

    print("Phase 1: Conforming observations")
    for entity, category, behavior in conforming_observations:
        process_observation(engine, world_model, repository, "Bird", entity, category, behavior)

    print("Phase 2: Contradicting observations")
    for entity, category, behavior in contradicting_observations:
        process_observation(engine, world_model, repository, "Bird", entity, category, behavior)

    bird = COMMUNITIES["Bird"]
    if should_split_by_pressure(bird):
        split_by_contradiction(repository, "Bird")

    print_community_expectations()
    print_contradictions_encountered()
    print_contradiction_debt()
    print_pressure_levels()
    print_community_structures()
    print_speciation_events()
    print_question_states(repository)


if __name__ == "__main__":
    main()
