import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

DIVERSITY_SPLIT_THRESHOLD = 2


@dataclass
class Community:
    name: str
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)


COMMUNITIES: dict[str, Community] = {
    "Bird": Community(name="Bird"),
}


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


def add_flying_bird_question(
    repository: QuestionRepository,
    community_name: str,
    entity: str,
) -> Question:
    question = Question(
        id=f"q-{entity.lower()}",
        text=f"How does {entity} fly?",
        state="ACTIVE",
        category="Bird",
        expected_behavior="fly",
        observed_behavior="fly",
        curiosity_debt=1.0,
    )
    repository.add_question(question)
    COMMUNITIES[community_name].members.append(question.id)
    return question


def assign_to_community(community_name: str, question_id: str) -> None:
    if question_id not in COMMUNITIES[community_name].members:
        COMMUNITIES[community_name].members.append(question_id)


def behavior_groups(repository: QuestionRepository, community: Community) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = {}
    for question_id in community.members:
        question = repository.get_question(question_id)
        if question is None or not question.observed_behavior:
            continue
        groups.setdefault(question.observed_behavior, []).append(question_id)
    return groups


def diversity_metrics(repository: QuestionRepository, community: Community) -> dict:
    groups = behavior_groups(repository, community)
    return {
        "behavior_types": len(groups),
        "members": len(community.members),
        "groups": {behavior: len(ids) for behavior, ids in sorted(groups.items())},
    }


def should_split(repository: QuestionRepository, community: Community) -> bool:
    groups = behavior_groups(repository, community)
    if len(groups) < 2:
        return False
    return all(len(ids) >= DIVERSITY_SPLIT_THRESHOLD for ids in groups.values())


def split_community(repository: QuestionRepository, parent_name: str) -> list[str]:
    parent = COMMUNITIES[parent_name]
    groups = behavior_groups(repository, parent)

    created: list[str] = []
    for behavior, member_ids in sorted(groups.items()):
        suffix = "Flying" if behavior == "fly" else "Flightless"
        child_name = f"{parent_name}.{suffix}"

        child = Community(name=child_name, parent=parent_name, members=list(member_ids))
        COMMUNITIES[child_name] = child
        parent.children.append(child_name)
        created.append(child_name)

    parent.members = []
    return created


def print_community_structures() -> None:
    print("Community structures:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        members = ", ".join(community.members) if community.members else "(none)"
        print(f"  {name}: members=[{members}]")
    print()


def print_parent_child_relationships() -> None:
    print("Parent-child community relationships:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        parent = community.parent if community.parent else "none"
        children = ", ".join(community.children) if community.children else "none"
        print(f"  {name}: parent={parent} children=[{children}]")
    print()


def print_community_statistics(repository: QuestionRepository) -> None:
    print("Community statistics:")
    for name in sorted(COMMUNITIES):
        community = COMMUNITIES[name]
        debt = sum(
            repository.get_question(qid).curiosity_debt
            for qid in community.members
            if repository.get_question(qid) is not None
        )
        print(
            f"  {name}: members={len(community.members)} "
            f"children={len(community.children)} debt={debt:.1f}"
        )
    print()


def print_diversity_metrics(repository: QuestionRepository) -> None:
    print("Community diversity metrics:")
    for name in sorted(COMMUNITIES):
        metrics = diversity_metrics(repository, COMMUNITIES[name])
        groups = metrics["groups"]
        group_str = ", ".join(f"{k}={v}" for k, v in groups.items()) if groups else "none"
        print(
            f"  {name}: behavior_types={metrics['behavior_types']} "
            f"members={metrics['members']} groups=({group_str})"
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

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    flying_observations = [
        ("Sparrow", "Bird", "fly"),
        ("Robin", "Bird", "fly"),
        ("Eagle", "Bird", "fly"),
        ("Falcon", "Bird", "fly"),
    ]

    flightless_observations = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
    ]

    print("=== EXP-007 Community Speciation ===\n")

    print("Phase 1: Flying bird observations")
    for entity, category, behavior in flying_observations:
        observe(engine, world_model, entity, category, behavior)
        add_flying_bird_question(repository, "Bird", entity)

    print("Phase 2: Flightless bird observations")
    for entity, category, behavior in flightless_observations:
        observe(engine, world_model, entity, category, behavior)
        assign_to_community("Bird", f"q-{entity.lower()}")

    bird = COMMUNITIES["Bird"]
    print(f"Bird community before split: {len(bird.members)} members")
    print(f"Diversity: {diversity_metrics(repository, bird)}\n")

    if should_split(repository, bird):
        children = split_community(repository, "Bird")
        print(f"Split triggered: {bird.name} -> {children}\n")
    else:
        print("Split not triggered.\n")

    print_community_structures()
    print_parent_child_relationships()
    print_community_statistics(repository)
    print_diversity_metrics(repository)
    print_question_states(repository)


if __name__ == "__main__":
    main()
