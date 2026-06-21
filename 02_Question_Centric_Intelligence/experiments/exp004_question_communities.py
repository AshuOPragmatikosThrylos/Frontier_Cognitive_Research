import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.curiosity_engine import CuriosityEngine
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel


@dataclass
class Relationship:
    source_id: str
    target_id: str
    rel_type: str


@dataclass
class QuestionGraph:
    supports: list[Relationship] = field(default_factory=list)
    depends_on: list[Relationship] = field(default_factory=list)
    cooperates_with: list[Relationship] = field(default_factory=list)

    def add(self, source_id: str, target_id: str, rel_type: str) -> None:
        rel = Relationship(source_id, target_id, rel_type)
        if rel_type == "supports":
            self.supports.append(rel)
        elif rel_type == "depends_on":
            self.depends_on.append(rel)
        elif rel_type == "cooperates_with":
            self.cooperates_with.append(rel)

    def all_relationships(self) -> list[Relationship]:
        return self.supports + self.depends_on + self.cooperates_with

    def count_by_type(self) -> dict[str, int]:
        return {
            "supports": len(self.supports),
            "depends_on": len(self.depends_on),
            "cooperates_with": len(self.cooperates_with),
        }


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


def add_community_question(repository: QuestionRepository, question: Question) -> None:
    question.state = "ACTIVE"
    repository.add_question(question)


def build_graph(repository: QuestionRepository) -> QuestionGraph:
    graph = QuestionGraph()

    bird_entities = ["q-penguin", "q-ostrich", "q-emu", "q-kiwi"]
    mammal_entities = ["q-bat", "q-whale"]

    for entity_id in bird_entities:
        graph.add(entity_id, "q-bird-flightlessness", "supports")

    for entity_id in mammal_entities:
        graph.add(entity_id, "q-mammal-capabilities", "supports")

    graph.add("q-bird-flightlessness", "q-species-capabilities", "depends_on")
    graph.add("q-mammal-capabilities", "q-species-capabilities", "depends_on")

    graph.add("q-bird-flightlessness", "q-mammal-capabilities", "cooperates_with")
    graph.add("q-bird-flightlessness", "q-species-capabilities", "cooperates_with")
    graph.add("q-mammal-capabilities", "q-species-capabilities", "cooperates_with")

    return graph


def print_communities(repository: QuestionRepository) -> None:
    print("Communities:")
    for name, member_ids in COMMUNITIES.items():
        print(f"  {name}:")
        for question_id in member_ids:
            question = repository.get_question(question_id)
            if question is not None:
                print(f"    [{question.id}] {question.text}")
    print()


def print_relationship_counts(graph: QuestionGraph) -> None:
    print("Relationship counts:")
    for rel_type, count in graph.count_by_type().items():
        print(f"  {rel_type}: {count}")
    print(f"  total: {len(graph.all_relationships())}")
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


def print_graph_statistics(repository: QuestionRepository, graph: QuestionGraph) -> None:
    questions = repository.get_all_questions()
    active = [q for q in questions if q.state == "ACTIVE"]

    cross_community = 0
    for rel in graph.cooperates_with + graph.depends_on:
        source_comm = community_of(rel.source_id)
        target_comm = community_of(rel.target_id)
        if source_comm and target_comm and source_comm != target_comm:
            cross_community += 1

    print("Question graph statistics:")
    print(f"  Nodes: {len(questions)}")
    print(f"  Edges: {len(graph.all_relationships())}")
    print(f"  ACTIVE nodes: {len(active)}")
    print(f"  Communities: {len(COMMUNITIES)}")
    print(f"  Cross-community edges: {cross_community}")
    print(f"  Avg edges per node: {len(graph.all_relationships()) / len(questions):.2f}")

    for name, member_ids in COMMUNITIES.items():
        internal = 0
        for rel in graph.all_relationships():
            if rel.source_id in member_ids and rel.target_id in member_ids:
                internal += 1
        print(f"  {name} community internal edges: {internal}")
    print()


def community_of(question_id: str) -> str | None:
    for name, member_ids in COMMUNITIES.items():
        if question_id in member_ids:
            return name
    return None


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

    print("=== EXP-004 Question Communities ===\n")

    for entity, category, behavior in normal_observations:
        observe(engine, world_model, entity, category, behavior)

    for entity, category, behavior in anomalies:
        observe(engine, world_model, entity, category, behavior)

    for question in repository.get_all_questions():
        question.state = "ACTIVE"

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

    graph = build_graph(repository)

    print_communities(repository)
    print_relationship_counts(graph)
    print_question_states(repository)
    print_graph_statistics(repository, graph)


if __name__ == "__main__":
    main()
