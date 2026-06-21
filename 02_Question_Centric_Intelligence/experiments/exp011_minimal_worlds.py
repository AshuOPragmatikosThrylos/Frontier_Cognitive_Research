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
DIFFERENCE_MIN_PER_GROUP = 2

INITIAL_TOLERANCES: dict[str, float] = {
    "Bird": 1.5,
    "Mammal": 4.0,
}

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
class Community:
    name: str
    expectation: str
    contradiction_tolerance: float
    parent: str | None = None
    children: list[str] = field(default_factory=list)
    members: list[str] = field(default_factory=list)
    contradiction_debt: float = 0.0
    contradictions: list[str] = field(default_factory=list)


@dataclass
class BehaviorGroup:
    name: str
    category: str
    behavior: str
    members: list[str] = field(default_factory=list)


@dataclass
class WorldResult:
    label: str
    world_id: str
    communities: dict[str, Community] = field(default_factory=dict)
    behavior_groups: dict[str, BehaviorGroup] = field(default_factory=dict)
    speciation_events: list[str] = field(default_factory=list)
    repository: QuestionRepository | None = None
    observations: list[str] = field(default_factory=list)


def make_initial_communities() -> dict[str, Community]:
    return {
        "Bird": Community(
            name="Bird",
            expectation="fly",
            contradiction_tolerance=INITIAL_TOLERANCES["Bird"],
        ),
        "Mammal": Community(
            name="Mammal",
            expectation="ground",
            contradiction_tolerance=INITIAL_TOLERANCES["Mammal"],
        ),
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


def pressure_level(community: Community) -> float:
    return max(0.0, community.contradiction_debt - community.contradiction_tolerance)


def add_conforming_question(
    repository: QuestionRepository,
    community: Community,
    entity: str,
    observed: str,
    category: str,
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
    communities: dict[str, Community],
    community_name: str,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    community = communities[community_name]
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


def process_ecosystem_observation(
    engine: CuriosityEngine,
    world_model: WorldModel,
    repository: QuestionRepository,
    communities: dict[str, Community],
    community_name: str,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    community = communities[community_name]
    behavior = behavior.lower()

    if behavior == community.expectation:
        observe(engine, world_model, entity, category, behavior)
        add_conforming_question(repository, community, entity, behavior, category)
        return

    record_contradiction(
        engine, world_model, repository, communities, community_name, entity, category, behavior
    )


def split_by_contradiction(
    repository: QuestionRepository,
    communities: dict[str, Community],
    speciation_events: list[str],
    parent_name: str,
) -> list[str]:
    parent = communities[parent_name]
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
        communities[child_name] = child
        parent.children.append(child_name)
        created.append(child_name)

    pressure = pressure_level(parent)
    speciation_events.append(
        f"{parent_name} split -> {created} (pressure={pressure:.2f}, "
        f"tolerance={parent.contradiction_tolerance:.2f})"
    )
    parent.members = []
    return created


def try_ecosystem_splits(
    repository: QuestionRepository,
    communities: dict[str, Community],
    speciation_events: list[str],
) -> None:
    for name in list(communities):
        community = communities[name]
        if community.members and pressure_level(community) >= PRESSURE_SPLIT_LIMIT:
            split_by_contradiction(repository, communities, speciation_events, name)


def run_ecosystem_world() -> WorldResult:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)
    communities = make_initial_communities()
    speciation_events: list[str] = []

    for entity, category, behavior in BIRD_CONFORMING:
        process_ecosystem_observation(
            engine, world_model, repository, communities, "Bird", entity, category, behavior
        )

    for entity, category, behavior in BIRD_CONTRADICTING:
        process_ecosystem_observation(
            engine, world_model, repository, communities, "Bird", entity, category, behavior
        )
    try_ecosystem_splits(repository, communities, speciation_events)

    for entity, category, behavior in MAMMAL_CONTRADICTING:
        record_contradiction(
            engine, world_model, repository, communities, "Mammal", entity, category, behavior
        )
    try_ecosystem_splits(repository, communities, speciation_events)

    return WorldResult(
        label="World A (Ecosystem)",
        world_id="A",
        communities=communities,
        speciation_events=speciation_events,
        repository=repository,
    )


def add_flat_question(
    repository: QuestionRepository,
    entity: str,
    category: str,
    behavior: str,
) -> Question:
    behavior = behavior.lower()
    question = Question(
        id=f"q-{entity.lower()}",
        text=f"How does {entity} {behavior}?",
        state="ACTIVE",
        category=category,
        observed_behavior=behavior,
        curiosity_debt=1.0,
    )
    repository.add_question(question)
    return question


def run_no_communities_world() -> WorldResult:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)

    for entity, category, behavior in ALL_OBSERVATIONS:
        observe(engine, world_model, entity, category, behavior)
        add_flat_question(repository, entity, category, behavior)

    return WorldResult(
        label="World B (No Communities)",
        world_id="B",
        speciation_events=[],
        repository=repository,
    )


def run_no_questions_world() -> WorldResult:
    observations: list[str] = []

    for entity, category, behavior in ALL_OBSERVATIONS:
        observations.append(f"{entity} ({category}): {behavior.lower()}")

    return WorldResult(
        label="World C (No Questions)",
        world_id="C",
        speciation_events=[],
        observations=observations,
    )


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_behavior(
    category_index: dict[str, dict[str, list[str]]],
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def try_difference_split(
    category_index: dict[str, dict[str, list[str]]],
    behavior_groups: dict[str, BehaviorGroup],
    speciation_events: list[str],
    category: str,
) -> None:
    groups = category_index.get(category, {})
    if len(groups) < 2:
        return
    if not all(len(members) >= DIFFERENCE_MIN_PER_GROUP for members in groups.values()):
        return

    created: list[str] = []
    for behavior, members in sorted(groups.items()):
        group_name = f"{category}.{behavior_key(behavior)}"
        behavior_groups[group_name] = BehaviorGroup(
            name=group_name,
            category=category,
            behavior=behavior,
            members=list(members),
        )
        created.append(group_name)

    speciation_events.append(
        f"{category} difference split -> {created} (min_per_group={DIFFERENCE_MIN_PER_GROUP})"
    )


def run_difference_world() -> WorldResult:
    category_index: dict[str, dict[str, list[str]]] = {}
    behavior_groups: dict[str, BehaviorGroup] = {}
    speciation_events: list[str] = []

    for entity, category, behavior in BIRD_CONFORMING:
        register_behavior(category_index, entity, category, behavior)

    for entity, category, behavior in BIRD_CONTRADICTING:
        register_behavior(category_index, entity, category, behavior)
    try_difference_split(category_index, behavior_groups, speciation_events, "Bird")

    for entity, category, behavior in MAMMAL_CONTRADICTING:
        register_behavior(category_index, entity, category, behavior)
    try_difference_split(category_index, behavior_groups, speciation_events, "Mammal")

    return WorldResult(
        label="World D (Difference)",
        world_id="D",
        behavior_groups=behavior_groups,
        speciation_events=speciation_events,
    )


def question_count(result: WorldResult) -> int:
    if result.repository is None:
        return 0
    return len(result.repository.get_all_questions())


def question_state_counts(result: WorldResult) -> dict[str, int]:
    counts: dict[str, int] = {}
    if result.repository is None:
        return counts
    for question in result.repository.get_all_questions():
        counts[question.state] = counts.get(question.state, 0) + 1
    return counts


def state_diversity(result: WorldResult) -> int:
    if result.repository is None:
        return 0
    return len(question_state_counts(result))


def structure_count(result: WorldResult) -> int:
    if result.communities:
        return len(result.communities)
    if result.behavior_groups:
        return len(result.behavior_groups)
    if result.observations:
        return 1
    if result.repository and question_count(result) > 0:
        return 1
    return 0


def leaf_structures(result: WorldResult) -> list[str]:
    if result.communities:
        return sorted(
            name for name, community in result.communities.items() if community.members
        )
    if result.behavior_groups:
        return sorted(result.behavior_groups)
    if result.observations:
        return ["observation_log"]
    if result.repository and question_count(result) > 0:
        return ["flat_questions"]
    return []


def organization_label(result: WorldResult) -> str:
    if result.world_id == "A":
        if any("Bird" in event for event in result.speciation_events):
            return "semantic speciation (pressure)"
        return "unorganized"
    if result.world_id == "B":
        return "flat questions (no structure)"
    if result.world_id == "C":
        return "raw observations only"
    if result.world_id == "D":
        if result.speciation_events:
            return "semantic groups (behavior difference)"
        return "unpartitioned"
    return "unknown"


def print_world_header(results: list[WorldResult]) -> None:
    columns = "  ".join(f"{result.world_id}: {result.label.split('(')[1].rstrip(')')}" for result in results)
    print(columns)


def print_comparison_row(label: str, values: list[str], width: int = 18) -> None:
    formatted = "  ".join(f"{value:<{width}}" for value in values)
    print(f"  {label:<22} {formatted}")


def print_structures_comparison(results: list[WorldResult]) -> None:
    print("=== Side-by-Side: Structures ===\n")
    print_comparison_row(
        "Metric",
        [result.world_id for result in results],
        width=18,
    )
    print_comparison_row(
        "Structure count",
        [str(structure_count(result)) for result in results],
    )
    print_comparison_row(
        "Leaf structures",
        [", ".join(leaf_structures(result)) or "(none)" for result in results],
    )
    print_comparison_row(
        "Questions",
        [str(question_count(result)) for result in results],
    )
    print_comparison_row(
        "Observations",
        [str(len(result.observations)) for result in results],
    )
    print()


def print_state_diversity_comparison(results: list[WorldResult]) -> None:
    print("=== Side-by-Side: State Diversity ===\n")
    all_states: set[str] = set()
    counts_per_world = [question_state_counts(result) for result in results]
    for counts in counts_per_world:
        all_states.update(counts)

    print_comparison_row(
        "Metric",
        [result.world_id for result in results],
    )
    print_comparison_row(
        "Distinct states",
        [str(state_diversity(result)) for result in results],
    )

    for state in sorted(all_states):
        print_comparison_row(
            state,
            [str(counts.get(state, 0)) for counts in counts_per_world],
        )
    print()


def print_speciation_comparison(results: list[WorldResult]) -> None:
    print("=== Side-by-Side: Speciation-like Events ===\n")
    print_comparison_row(
        "Metric",
        [result.world_id for result in results],
    )
    print_comparison_row(
        "Event count",
        [str(len(result.speciation_events)) for result in results],
    )
    print()

    max_events = max(len(result.speciation_events) for result in results)
    if max_events == 0:
        print("  (no speciation-like events in any world)")
        print()
        return

    for index in range(max_events):
        print(f"  Event {index + 1}:")
        for result in results:
            if index < len(result.speciation_events):
                print(f"    {result.world_id}: {result.speciation_events[index]}")
            else:
                print(f"    {result.world_id}: (none)")
    print()


def print_organization_comparison(results: list[WorldResult]) -> None:
    print("=== Side-by-Side: Organization ===\n")
    print_comparison_row(
        "Metric",
        [result.world_id for result in results],
    )
    print_comparison_row(
        "Organization",
        [organization_label(result) for result in results],
    )
    print()

    for result in results:
        print(f"  {result.world_id} detail:")
        if result.communities:
            for name in sorted(result.communities):
                community = result.communities[name]
                members = ", ".join(community.members) if community.members else "(none)"
                print(f"    {name}: [{members}]")
        elif result.behavior_groups:
            for name in sorted(result.behavior_groups):
                group = result.behavior_groups[name]
                members = ", ".join(group.members)
                print(f"    {name}: [{members}]")
        elif result.observations:
            for entry in result.observations:
                print(f"    - {entry}")
        elif result.repository:
            for question in sorted(result.repository.get_all_questions(), key=lambda q: q.id):
                print(f"    [{question.id}] {question.state} — {question.text}")
        else:
            print("    (empty)")
    print()


def print_summary_statistics(results: list[WorldResult]) -> None:
    print("=== Summary Statistics ===\n")

    ecosystem = next(result for result in results if result.world_id == "A")
    difference = next(result for result in results if result.world_id == "D")

    a_bird_split = any("Bird" in event for event in ecosystem.speciation_events)
    d_bird_split = any("Bird" in event for event in difference.speciation_events)

    print("  Minimal ingredient comparison:")
    print_comparison_row(
        "Property",
        [result.world_id for result in results],
    )
    print_comparison_row(
        "Communities",
        [
            "yes" if result.communities else "no"
            for result in results
        ],
    )
    print_comparison_row(
        "Questions",
        [
            "yes" if question_count(result) > 0 else "no"
            for result in results
        ],
    )
    print_comparison_row(
        "Bird partition",
        [
            "yes" if any("Bird" in event for event in result.speciation_events) else "no"
            for result in results
        ],
    )
    print()

    print(f"  Bird speciation (A vs D): A={a_bird_split}  D={d_bird_split}")
    print(f"  Observations processed: {len(ALL_OBSERVATIONS)} (identical across all worlds)")
    print()


def print_overall_observations(results: list[WorldResult]) -> None:
    print("=== Overall Observations ===\n")

    ecosystem = next(result for result in results if result.world_id == "A")
    no_communities = next(result for result in results if result.world_id == "B")
    no_questions = next(result for result in results if result.world_id == "C")
    difference = next(result for result in results if result.world_id == "D")

    print("  1. World A (ecosystem) requires communities, questions, pressure, and tolerance.")
    print("  2. World B (no communities) retains questions but produces no speciation or hierarchy.")
    print("  3. World C (no questions) stores only raw observations — zero cognitive structure.")
    print("  4. World D (difference) achieves Bird partitioning with minimal behavior comparison only.")

    if a_bird := any("Bird" in event for event in ecosystem.speciation_events):
        d_bird = any("Bird" in event for event in difference.speciation_events)
        if a_bird and d_bird:
            print("  5. Bird semantic partition reproduced by both ecosystem and difference worlds.")
        elif a_bird:
            print("  5. Bird partition appears only under ecosystem mechanisms.")

    print(
        f"  6. Question count: A={question_count(ecosystem)} B={question_count(no_communities)} "
        f"C={question_count(no_questions)} D={question_count(difference)}"
    )
    print(
        f"  7. State diversity: A={state_diversity(ecosystem)} B={state_diversity(no_communities)} "
        f"C={state_diversity(no_questions)} D={state_diversity(difference)}"
    )
    print(
        f"  8. Speciation events: A={len(ecosystem.speciation_events)} "
        f"B={len(no_communities.speciation_events)} C={len(no_questions.speciation_events)} "
        f"D={len(difference.speciation_events)}"
    )
    print()
    print("  Interpretation:")
    print("    Communities and pressure are sufficient but not necessary for Bird partitioning.")
    print("    Questions alone (World B) do not produce organization.")
    print("    Observations alone (World C) cannot support speciation-like events.")
    print("    Minimal difference detection (World D) isolates the smallest organizing principle tested.")
    print()


def main() -> None:
    print("=== EXP-011 Minimal Worlds ===\n")
    print("World A: full ecosystem (communities + questions + adaptive pressure)")
    print("World B: questions only, no communities")
    print("World C: observations only, no questions")
    print("World D: minimal difference-based grouping")
    print(f"Shared observation sequence: {len(ALL_OBSERVATIONS)} observations\n")

    results = [
        run_ecosystem_world(),
        run_no_communities_world(),
        run_no_questions_world(),
        run_difference_world(),
    ]

    print_structures_comparison(results)
    print_state_diversity_comparison(results)
    print_speciation_comparison(results)
    print_organization_comparison(results)
    print_summary_statistics(results)
    print_overall_observations(results)


if __name__ == "__main__":
    main()
