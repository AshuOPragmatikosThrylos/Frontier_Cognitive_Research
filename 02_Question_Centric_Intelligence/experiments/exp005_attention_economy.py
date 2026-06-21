import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

ATTENTION_BUDGET = 4

COMMUNITIES: dict[str, list[str]] = {
    "Bird": [
        "q-penguin",
        "q-ostrich",
        "q-emu",
        "q-kiwi",
        "q-bird-flightlessness",
    ],
    "Mammal": [
        "q-bat",
        "q-whale",
        "q-mammal-capabilities",
    ],
    "Capability": [
        "q-species-capabilities",
    ],
}

REVIVED: list[str] = []
ALLOCATION_LOG: list[dict] = []


def fitness(question: Question) -> float:
    return question.curiosity_debt * question.importance


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


def allocate_attention(repository: QuestionRepository, label: str) -> list[str]:
    eligible = repository.get_all_questions()
    ranked = sorted(eligible, key=lambda q: (-fitness(q), q.id))

    active_ids = {q.id for q in ranked[:ATTENTION_BUDGET]}
    allocation: list[str] = []

    for question in eligible:
        if question.id in active_ids:
            question.state = "ACTIVE"
            allocation.append(question.id)
        else:
            question.state = "DORMANT"

    ALLOCATION_LOG.append({"label": label, "active": list(allocation)})
    return allocation


def observe_with_revival(
    engine: CuriosityEngine,
    world_model: WorldModel,
    repository: QuestionRepository,
    entity: str,
    category: str,
    behavior: str,
    label: str,
) -> None:
    question_id = f"q-{entity.lower()}"
    existing = repository.get_question(question_id)
    was_dormant = existing is not None and existing.state == "DORMANT"

    observe(engine, world_model, entity, category, behavior)

    if was_dormant:
        REVIVED.append(question_id)

    allocate_attention(repository, label)


def add_community_question(repository: QuestionRepository, question: Question) -> None:
    repository.add_question(question)


def community_of(question_id: str) -> str | None:
    for name, member_ids in COMMUNITIES.items():
        if question_id in member_ids:
            return name
    return None


def print_attention_allocation() -> None:
    print("Attention allocation:")
    for entry in ALLOCATION_LOG:
        print(f"  {entry['label']}:")
        for question_id in entry["active"]:
            print(f"    -> {question_id}")
    print()


def print_question_states(repository: QuestionRepository) -> None:
    print("Question states:")
    by_state: dict[str, list[str]] = {}
    for question in sorted(repository.get_all_questions(), key=lambda q: q.id):
        by_state.setdefault(question.state, []).append(question.id)
        print(f"  [{question.id}] {question.state} — {question.text}")

    print()
    print("  Summary by state:")
    for state, ids in sorted(by_state.items()):
        print(f"    {state}: {len(ids)}")
    print()


def print_dormant_questions(repository: QuestionRepository) -> None:
    dormant = [q for q in repository.get_all_questions() if q.state == "DORMANT"]
    print("Dormant questions:")
    if not dormant:
        print("  (none)")
    for question in sorted(dormant, key=lambda q: q.id):
        print(f"  [{question.id}] debt={question.curiosity_debt} — {question.text}")
    print()


def print_revived_questions() -> None:
    print("Revived questions:")
    if not REVIVED:
        print("  (none)")
    for question_id in REVIVED:
        print(f"  {question_id}")
    print()


def print_community_statistics(repository: QuestionRepository) -> None:
    print("Community statistics:")
    for name, member_ids in COMMUNITIES.items():
        active = 0
        dormant = 0
        total_debt = 0.0
        for question_id in member_ids:
            question = repository.get_question(question_id)
            if question is None:
                continue
            total_debt += question.curiosity_debt
            if question.state == "ACTIVE":
                active += 1
            elif question.state == "DORMANT":
                dormant += 1
        print(f"  {name}: members={len(member_ids)} active={active} dormant={dormant} debt={total_debt}")
    print()


def main() -> None:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")
    world_model.add_rule("Cat", "meow")
    world_model.add_rule("Fish", "swim")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    initial_observations = [
        ("Sparrow", "Bird", "fly"),
        ("Robin", "Bird", "fly"),
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
    ]

    revival_observations = [
        ("Penguin", "Bird", "not fly"),
        ("Whale", "Mammal", "swim"),
    ]

    print("=== EXP-005 Attention Economy ===\n")
    print(f"Attention budget: {ATTENTION_BUDGET}\n")

    for entity, category, behavior in initial_observations:
        observe(engine, world_model, entity, category, behavior)

    add_community_question(
        repository,
        Question(
            id="q-bird-flightlessness",
            text="Why don't some birds fly?",
            category="Bird",
            expected_behavior="fly",
            observed_behavior="not fly",
            curiosity_debt=4.0,
            importance=2.0,
        ),
    )

    add_community_question(
        repository,
        Question(
            id="q-mammal-capabilities",
            text="Why do some mammals gain unexpected capabilities?",
            category="Mammal",
            curiosity_debt=2.0,
            importance=2.0,
        ),
    )

    add_community_question(
        repository,
        Question(
            id="q-species-capabilities",
            text="Why do species gain or lose capabilities?",
            curiosity_debt=6.0,
            importance=3.0,
        ),
    )

    allocate_attention(repository, "initial")

    print("--- After initial allocation ---\n")
    print_attention_allocation()
    print_question_states(repository)
    print_dormant_questions(repository)

    for entity, category, behavior in revival_observations:
        observe_with_revival(
            engine,
            world_model,
            repository,
            entity,
            category,
            behavior,
            f"after revival: {entity}",
        )

    print("--- After revival observations ---\n")
    print_attention_allocation()
    print_question_states(repository)
    print_dormant_questions(repository)
    print_revived_questions()
    print_community_statistics(repository)


if __name__ == "__main__":
    main()
