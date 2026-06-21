import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

COMMUNITY_ATTENTION_BUDGET = 2

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

COMMUNITY_STATES: dict[str, str] = {}
COMMUNITY_DEBT_LOG: list[dict] = []
ALLOCATION_LOG: list[dict] = []


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


def community_debt(repository: QuestionRepository, community_name: str) -> float:
    total = 0.0
    for question_id in COMMUNITIES[community_name]:
        question = repository.get_question(question_id)
        if question is not None:
            total += question.curiosity_debt
    return total


def community_fitness(repository: QuestionRepository, community_name: str) -> float:
    total = 0.0
    for question_id in COMMUNITIES[community_name]:
        question = repository.get_question(question_id)
        if question is not None:
            total += question.curiosity_debt * question.importance
    return total


def allocate_community_attention(repository: QuestionRepository, label: str) -> list[str]:
    ranked = sorted(
        COMMUNITIES.keys(),
        key=lambda name: (-community_fitness(repository, name), name),
    )

    active_communities = set(ranked[:COMMUNITY_ATTENTION_BUDGET])

    for name in COMMUNITIES:
        COMMUNITY_STATES[name] = "ACTIVE" if name in active_communities else "DORMANT"

    for name, member_ids in COMMUNITIES.items():
        state = COMMUNITY_STATES[name]
        for question_id in member_ids:
            question = repository.get_question(question_id)
            if question is not None:
                question.state = state

    debts = {name: community_debt(repository, name) for name in COMMUNITIES}
    COMMUNITY_DEBT_LOG.append({"label": label, "debts": debts})
    ALLOCATION_LOG.append({"label": label, "active": sorted(active_communities)})

    return sorted(active_communities)


def add_community_question(repository: QuestionRepository, question: Question) -> None:
    repository.add_question(question)


def run_observations(
    engine: CuriosityEngine,
    world_model: WorldModel,
    repository: QuestionRepository,
    observations: list[tuple[str, str, str]],
    label: str,
) -> None:
    for entity, category, behavior in observations:
        observe(engine, world_model, entity, category, behavior)
    allocate_community_attention(repository, label)


def print_community_attention_over_time() -> None:
    print("Community attention allocations over time:")
    for entry in ALLOCATION_LOG:
        active = ", ".join(entry["active"])
        print(f"  {entry['label']}: [{active}]")
    print()


def print_community_debt() -> None:
    print("Community debt:")
    for entry in COMMUNITY_DEBT_LOG:
        debts = entry["debts"]
        parts = ", ".join(f"{name}={debts[name]:.1f}" for name in sorted(debts))
        print(f"  {entry['label']}: {parts}")
    print()


def print_community_states() -> None:
    print("Community states:")
    for name in sorted(COMMUNITIES):
        print(f"  {name}: {COMMUNITY_STATES.get(name, 'UNKNOWN')}")
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


def print_community_statistics(repository: QuestionRepository) -> None:
    print("Community statistics:")
    for name, member_ids in COMMUNITIES.items():
        active = sum(
            1 for qid in member_ids
            if (q := repository.get_question(qid)) is not None and q.state == "ACTIVE"
        )
        dormant = sum(
            1 for qid in member_ids
            if (q := repository.get_question(qid)) is not None and q.state == "DORMANT"
        )
        debt = community_debt(repository, name)
        fitness = community_fitness(repository, name)
        print(
            f"  {name}: state={COMMUNITY_STATES.get(name)} "
            f"members={len(member_ids)} active={active} dormant={dormant} "
            f"debt={debt:.1f} fitness={fitness:.1f}"
        )
    print()


def main() -> None:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")
    world_model.add_rule("Cat", "meow")
    world_model.add_rule("Fish", "swim")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    bird_wave_1 = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
    ]

    bird_wave_2 = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
    ]

    mammal_wave_1 = [
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
    ]

    mammal_wave_2 = [
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
    ]

    print("=== EXP-006 Community Competition ===\n")
    print(f"Community attention budget: {COMMUNITY_ATTENTION_BUDGET}\n")

    add_community_question(
        repository,
        Question(
            id="q-bird-flightlessness",
            text="Why don't some birds fly?",
            category="Bird",
            curiosity_debt=2.0,
            importance=1.5,
        ),
    )

    add_community_question(
        repository,
        Question(
            id="q-mammal-capabilities",
            text="Why do some mammals gain unexpected capabilities?",
            category="Mammal",
            curiosity_debt=1.0,
            importance=1.5,
        ),
    )

    add_community_question(
        repository,
        Question(
            id="q-species-capabilities",
            text="Why do species gain or lose capabilities?",
            curiosity_debt=2.0,
            importance=1.5,
        ),
    )

    run_observations(engine, world_model, repository, bird_wave_1, "after bird wave 1")
    run_observations(engine, world_model, repository, bird_wave_2, "after bird wave 2")
    run_observations(engine, world_model, repository, mammal_wave_1, "after mammal wave 1")
    run_observations(engine, world_model, repository, mammal_wave_2, "after mammal wave 2")

    print_community_attention_over_time()
    print_community_debt()
    print_community_states()
    print_question_states(repository)
    print_community_statistics(repository)


if __name__ == "__main__":
    main()
