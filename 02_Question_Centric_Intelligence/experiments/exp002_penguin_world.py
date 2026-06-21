import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question_merger import find_merge_candidates, merge_all_candidates
from src.question_repository import QuestionRepository
from src.world_model import WorldModel


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


def print_questions(title: str, questions: list) -> None:
    print(title)
    for question in sorted(questions, key=lambda q: q.id):
        print(f"  [{question.id}] {question.text}")
        print(f"    state: {question.state}")
        print(f"    curiosity_debt: {question.curiosity_debt}")
        print(f"    parent_questions: {question.parent_questions}")
        print(f"    child_questions: {question.child_questions}")
        print()


def print_genealogy(questions: list) -> None:
    print("Genealogy:")
    for question in questions:
        if question.parent_questions:
            parents = ", ".join(question.parent_questions)
            print(f"  [{question.id}] {question.text}")
            print(f"    parent_questions: [{parents}]")
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

    print("=== EXP-002 Penguin World — True Question Merge ===\n")

    for entity, category, behavior in normal_observations:
        observe(engine, world_model, entity, category, behavior)

    for entity, category, behavior in anomalies:
        observe(engine, world_model, entity, category, behavior)

    before = repository.get_all_questions()
    print_questions("Questions before merge:", before)

    candidates = find_merge_candidates(repository)
    print(f"Merge candidate groups: {len(candidates)}")
    for group in candidates:
        ids = [q.id for q in group]
        print(f"  group ({group[0].category}, {group[0].expected_behavior}, {group[0].observed_behavior}): {ids}")
    print()

    merged_abstracts, merge_count = merge_all_candidates(repository)

    after = repository.get_all_questions()
    print_questions("Questions after merge:", after)

    print(f"Merge count: {merge_count}")
    print(f"Abstract questions created: {len(merged_abstracts)}")
    print()

    print_genealogy(after)

    print("Final repository state:")
    print(f"  Total questions: {len(after)}")
    print(f"  Active questions: {len(repository.get_active_questions())}")
    print(f"  Total curiosity debt: {sum(q.curiosity_debt for q in after)}")


if __name__ == "__main__":
    main()
