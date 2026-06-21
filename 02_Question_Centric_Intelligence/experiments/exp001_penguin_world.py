import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
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

    print("=== EXP-001 Penguin World ===\n")

    print("Normal observations:")
    for entity, category, behavior in normal_observations:
        observe(engine, world_model, entity, category, behavior)
        print(f"  {entity} ({category}) -> {behavior}")

    print("\nAnomalies:")
    for entity, category, behavior in anomalies:
        observe(engine, world_model, entity, category, behavior)
        print(f"  {entity} ({category}) -> {behavior}")

    all_questions = list(repository._questions.values())

    print("\nGenerated questions:")
    for question in sorted(all_questions, key=lambda q: q.curiosity_debt, reverse=True):
        print(f"  [{question.id}] {question.text}")
        print(f"    state: {question.state}")
        print(f"    curiosity_debt: {question.curiosity_debt}")
        print(f"    times_encountered: {question.times_encountered}")
        print()

    print("Summary:")
    print(f"  Total questions: {len(all_questions)}")
    print(f"  Active questions: {len(repository.get_active_questions())}")
    print(f"  Total curiosity debt: {sum(q.curiosity_debt for q in all_questions)}")


if __name__ == "__main__":
    main()
