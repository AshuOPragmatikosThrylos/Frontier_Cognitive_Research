import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_merger import find_merge_candidates, merge_candidates
from src.question_repository import QuestionRepository
from src.world_model import WorldModel

MERGEABLE_STATES = {"NEW", "ACTIVE", "INVESTIGATING"}
GENERATIONS: dict[str, int] = {}


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


def register_generation(question_id: str, generation: int) -> None:
    GENERATIONS[question_id] = generation


def find_mammal_cross_candidates(repository: QuestionRepository) -> list[Question]:
    candidates = []
    for question in repository.get_all_questions():
        if question.state not in MERGEABLE_STATES:
            continue
        if question.category == "Mammal" and not question.expected_behavior:
            candidates.append(question)
    return candidates


def merge_mammal_abstraction(repository: QuestionRepository, candidates: list[Question]) -> tuple[Question | None, int]:
    if len(candidates) < 2:
        return None, 0

    abstract = Question(
        id="q-abstract-mammal-capabilities",
        text="Why do some mammals gain unexpected capabilities?",
        state="ACTIVE",
        category="Mammal",
    )
    repository.add_question(abstract)
    register_generation(abstract.id, 1)

    merge_count = 0
    for source in candidates:
        if source.id not in GENERATIONS:
            register_generation(source.id, 0)
        repository.merge_questions(abstract.id, source.id, source_state="PARTIALLY_RESOLVED")
        merge_count += 1

    return abstract, merge_count


def merge_hierarchical_abstraction(
    repository: QuestionRepository,
    source_ids: list[str],
    target_id: str,
    target_text: str,
) -> tuple[Question, int]:
    abstract = Question(
        id=target_id,
        text=target_text,
        state="ACTIVE",
    )
    repository.add_question(abstract)
    register_generation(abstract.id, 2)

    merge_count = 0
    for source_id in source_ids:
        source = repository.get_question(source_id)
        if source is None:
            continue
        repository.merge_questions(abstract.id, source_id, source_state="PARTIALLY_RESOLVED")
        merge_count += 1

    return abstract, merge_count


def print_hierarchy(repository: QuestionRepository) -> None:
    top_id = "q-abstract-species-capabilities"
    top = repository.get_question(top_id)

    def walk(question: Question, indent: int = 0) -> None:
        generation = GENERATIONS.get(question.id, "?")
        prefix = "  " * indent
        print(f"{prefix}[gen {generation}] [{question.id}] {question.text}")
        print(f"{prefix}  state: {question.state}")
        print(f"{prefix}  parent_questions: {question.parent_questions}")
        print(f"{prefix}  child_questions: {question.child_questions}")
        for parent_id in question.parent_questions:
            parent = repository.get_question(parent_id)
            if parent is not None:
                walk(parent, indent + 1)

    print("Question hierarchy:")
    if top is not None:
        walk(top)
    else:
        for question in sorted(repository.get_all_questions(), key=lambda q: q.id):
            if not question.parent_questions:
                walk(question)
    print()


def print_generations(repository: QuestionRepository) -> None:
    print("Generation numbers:")
    for question in sorted(repository.get_all_questions(), key=lambda q: GENERATIONS.get(q.id, 99)):
        generation = GENERATIONS.get(question.id, 0)
        print(f"  gen {generation}: [{question.id}] {question.text}")
    print()


def main() -> None:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")
    world_model.add_rule("Cat", "meow")
    world_model.add_rule("Fish", "swim")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    normal_observations = [
        ("Sparrow", "Bird", "fly"),
        ("Robin", "Bird", "fly"),
        ("Dog", "Dog", "bark"),
        ("Cat", "Cat", "meow"),
        ("Salmon", "Fish", "swim"),
    ]

    anomalies = [
        ("Penguin", "Bird", "not fly"),
        ("Ostrich", "Bird", "not fly"),
        ("Emu", "Bird", "not fly"),
        ("Kiwi", "Bird", "not fly"),
        ("Bat", "Mammal", "fly"),
        ("Whale", "Mammal", "swim"),
    ]

    print("=== EXP-003 Hierarchical Question Evolution ===\n")

    for entity, category, behavior in normal_observations:
        observe(engine, world_model, entity, category, behavior)

    for entity, category, behavior in anomalies:
        observe(engine, world_model, entity, category, behavior)
        register_generation(f"q-{entity.lower()}", 0)

    stage1_merge_count = 0
    bird_abstract: Question | None = None

    for group in find_merge_candidates(repository):
        abstract, count = merge_candidates(repository, group)
        register_generation(abstract.id, 1)
        stage1_merge_count += count
        if abstract.id == "q-abstract-bird-fly":
            bird_abstract = abstract

    mammal_candidates = find_mammal_cross_candidates(repository)
    mammal_abstract, mammal_merge_count = merge_mammal_abstraction(repository, mammal_candidates)
    stage1_merge_count += mammal_merge_count

    print("Stage 1 merges:")
    print(f"  Bird abstraction: {bird_abstract.text if bird_abstract else 'none'}")
    print(f"  Mammal abstraction: {mammal_abstract.text if mammal_abstract else 'none'}")
    print(f"  Stage 1 merge count: {stage1_merge_count}\n")

    stage2_merge_count = 0
    meta_abstract: Question | None = None

    if bird_abstract and mammal_abstract:
        meta_abstract, stage2_merge_count = merge_hierarchical_abstraction(
            repository,
            [bird_abstract.id, mammal_abstract.id],
            "q-abstract-species-capabilities",
            "Why do species gain or lose capabilities?",
        )

    print("Stage 2 merge:")
    print(f"  Meta abstraction: {meta_abstract.text if meta_abstract else 'none'}")
    print(f"  Stage 2 merge count: {stage2_merge_count}\n")

    print_hierarchy(repository)
    print_generations(repository)

    all_questions = repository.get_all_questions()
    print("Merge counts:")
    print(f"  Stage 1: {stage1_merge_count}")
    print(f"  Stage 2: {stage2_merge_count}")
    print(f"  Total: {stage1_merge_count + stage2_merge_count}\n")

    print("Repository statistics:")
    print(f"  Total questions: {len(all_questions)}")
    print(f"  Active questions: {len(repository.get_active_questions())}")
    print(f"  Total curiosity debt: {sum(q.curiosity_debt for q in all_questions)}")
    by_state: dict[str, int] = {}
    for question in all_questions:
        by_state[question.state] = by_state.get(question.state, 0) + 1
    print(f"  By state: {by_state}")


if __name__ == "__main__":
    main()
