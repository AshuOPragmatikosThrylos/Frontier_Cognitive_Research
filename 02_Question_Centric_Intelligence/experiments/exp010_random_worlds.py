import random
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

RANDOM_SEED = 42
RANDOM_SPLIT_CHANCE = 0.25
RANDOM_STATE_CHANGE_CHANCE = 0.15
QUESTION_STATES = ["ACTIVE", "DORMANT", "PARTIALLY_RESOLVED", "NEW"]

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
class WorldResult:
    label: str
    communities: dict[str, Community]
    speciation_events: list[str]
    repository: QuestionRepository
    tolerance_log: list[dict] = field(default_factory=list)


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


def log_tolerances(communities: dict[str, Community], tolerance_log: list[dict], label: str) -> None:
    tolerance_log.append({
        "label": label,
        "tolerances": {name: communities[name].contradiction_tolerance for name in communities},
        "debts": {name: communities[name].contradiction_debt for name in communities},
        "pressures": {name: pressure_level(communities[name]) for name in communities},
    })


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


def process_observation(
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
    trigger: str,
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
        f"{parent_name} split -> {created} ({trigger}, pressure={pressure:.2f}, "
        f"tolerance={parent.contradiction_tolerance:.2f})"
    )
    parent.members = []
    return created


def try_pressure_splits(
    repository: QuestionRepository,
    communities: dict[str, Community],
    speciation_events: list[str],
    tolerance_log: list[dict],
    label: str,
) -> None:
    for name in list(communities):
        community = communities[name]
        if community.members and pressure_level(community) >= PRESSURE_SPLIT_LIMIT:
            split_by_contradiction(repository, communities, speciation_events, name, "pressure")
    log_tolerances(communities, tolerance_log, label)


def split_randomly(
    repository: QuestionRepository,
    communities: dict[str, Community],
    speciation_events: list[str],
    parent_name: str,
    rng: random.Random,
) -> list[str]:
    parent = communities[parent_name]
    members = list(parent.members)
    if len(members) < 2:
        return []

    rng.shuffle(members)
    midpoint = len(members) // 2
    groups = [members[:midpoint], members[midpoint:]]

    created: list[str] = []
    for index, member_ids in enumerate(groups, start=1):
        if not member_ids:
            continue
        child_name = f"{parent_name}.Random{index}"
        child = Community(
            name=child_name,
            expectation=parent.expectation,
            contradiction_tolerance=parent.contradiction_tolerance,
            parent=parent_name,
            members=list(member_ids),
        )
        communities[child_name] = child
        parent.children.append(child_name)
        created.append(child_name)

    speciation_events.append(
        f"{parent_name} split -> {created} (random, p={RANDOM_SPLIT_CHANCE})"
    )
    parent.members = []
    return created


def try_random_splits(
    repository: QuestionRepository,
    communities: dict[str, Community],
    speciation_events: list[str],
    tolerance_log: list[dict],
    label: str,
    rng: random.Random,
) -> None:
    for name in list(communities):
        community = communities[name]
        if community.members and rng.random() < RANDOM_SPLIT_CHANCE:
            split_randomly(repository, communities, speciation_events, name, rng)
    log_tolerances(communities, tolerance_log, label)


def apply_random_state_changes(repository: QuestionRepository, rng: random.Random) -> None:
    for question in repository.get_all_questions():
        if rng.random() < RANDOM_STATE_CHANGE_CHANCE:
            question.state = rng.choice(QUESTION_STATES)


def run_pressure_world() -> WorldResult:
    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)
    communities = make_initial_communities()
    speciation_events: list[str] = []
    tolerance_log: list[dict] = []

    for entity, category, behavior in BIRD_CONFORMING:
        process_observation(engine, world_model, repository, communities, "Bird", entity, category, behavior)
    log_tolerances(communities, tolerance_log, "after bird conforming")

    for entity, category, behavior in BIRD_CONTRADICTING:
        process_observation(engine, world_model, repository, communities, "Bird", entity, category, behavior)
    try_pressure_splits(repository, communities, speciation_events, tolerance_log, "after bird contradictions")

    for entity, category, behavior in MAMMAL_CONTRADICTING:
        record_contradiction(
            engine, world_model, repository, communities, "Mammal", entity, category, behavior
        )
    try_pressure_splits(repository, communities, speciation_events, tolerance_log, "after mammal contradictions")

    return WorldResult(
        label="World A (Pressure)",
        communities=communities,
        speciation_events=speciation_events,
        repository=repository,
        tolerance_log=tolerance_log,
    )


def run_random_world() -> WorldResult:
    rng = random.Random(RANDOM_SEED)

    world_model = WorldModel()
    world_model.add_rule("Bird", "fly")
    world_model.add_rule("Dog", "bark")

    repository = QuestionRepository()
    engine = CuriosityEngine(repository, world_model)
    communities = make_initial_communities()
    speciation_events: list[str] = []
    tolerance_log: list[dict] = []

    for entity, category, behavior in BIRD_CONFORMING:
        process_observation(engine, world_model, repository, communities, "Bird", entity, category, behavior)
        apply_random_state_changes(repository, rng)
    log_tolerances(communities, tolerance_log, "after bird conforming")

    for entity, category, behavior in BIRD_CONTRADICTING:
        process_observation(engine, world_model, repository, communities, "Bird", entity, category, behavior)
        apply_random_state_changes(repository, rng)
    try_random_splits(repository, communities, speciation_events, tolerance_log, "after bird contradictions", rng)

    for entity, category, behavior in MAMMAL_CONTRADICTING:
        record_contradiction(
            engine, world_model, repository, communities, "Mammal", entity, category, behavior
        )
        apply_random_state_changes(repository, rng)
    try_random_splits(repository, communities, speciation_events, tolerance_log, "after mammal contradictions", rng)

    return WorldResult(
        label="World B (Random)",
        communities=communities,
        speciation_events=speciation_events,
        repository=repository,
        tolerance_log=tolerance_log,
    )


def community_count(result: WorldResult) -> int:
    return len(result.communities)


def leaf_communities(result: WorldResult) -> list[str]:
    return sorted(
        name for name, community in result.communities.items() if community.members
    )


def question_state_counts(result: WorldResult) -> dict[str, int]:
    counts: dict[str, int] = {}
    for question in result.repository.get_all_questions():
        counts[question.state] = counts.get(question.state, 0) + 1
    return counts


def evolution_pattern(result: WorldResult) -> str:
    splits = len(result.speciation_events)
    leaves = len(leaf_communities(result))
    if splits == 0:
        return "stable (no speciation)"
    if splits == 1 and any("Bird" in event for event in result.speciation_events):
        return "selective speciation (Bird only)"
    if splits >= 2:
        return "multi-speciation"
    return f"{splits} speciation event(s)"


def print_side_by_side_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<28} {value_a:<22} {value_b}")


def print_comparison_header() -> None:
    print(f"  {'Metric':<28} {'World A (Pressure)':<22} World B (Random)")


def print_community_structures_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Community Structures ===\n")
    print_comparison_header()
    print_side_by_side_row("Community count", str(community_count(world_a)), str(community_count(world_b)))
    print_side_by_side_row(
        "Leaf communities",
        ", ".join(leaf_communities(world_a)) or "(none)",
        ", ".join(leaf_communities(world_b)) or "(none)",
    )
    print()

    all_names = sorted(set(world_a.communities) | set(world_b.communities))
    for name in all_names:
        a_members = world_a.communities[name].members if name in world_a.communities else []
        b_members = world_b.communities[name].members if name in world_b.communities else []
        a_text = ", ".join(a_members) if a_members else "(none)"
        b_text = ", ".join(b_members) if b_members else "(none)"
        print(f"  {name}:")
        print(f"    A: [{a_text}]")
        print(f"    B: [{b_text}]")
    print()


def print_speciation_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Speciation Events ===\n")
    print_comparison_header()
    print_side_by_side_row(
        "Speciation count",
        str(len(world_a.speciation_events)),
        str(len(world_b.speciation_events)),
    )
    print()

    max_events = max(len(world_a.speciation_events), len(world_b.speciation_events), 1)
    for index in range(max_events):
        a_event = world_a.speciation_events[index] if index < len(world_a.speciation_events) else "(none)"
        b_event = world_b.speciation_events[index] if index < len(world_b.speciation_events) else "(none)"
        print(f"  Event {index + 1}:")
        print(f"    A: {a_event}")
        print(f"    B: {b_event}")
    print()


def print_community_statistics_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Community Statistics ===\n")
    print_comparison_header()
    print()

    all_names = sorted(set(world_a.communities) | set(world_b.communities))
    for name in all_names:
        print(f"  {name}:")
        for label, result in [("A", world_a), ("B", world_b)]:
            if name not in result.communities:
                print(f"    {label}: (absent)")
                continue
            community = result.communities[name]
            member_debt = sum(
                result.repository.get_question(qid).curiosity_debt
                for qid in community.members
                if result.repository.get_question(qid) is not None
            )
            print(
                f"    {label}: tolerance={community.contradiction_tolerance:.2f} "
                f"members={len(community.members)} debt={community.contradiction_debt:.1f} "
                f"curiosity_debt={member_debt:.1f} pressure={pressure_level(community):.2f}"
            )
    print()


def print_question_states_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Question States ===\n")
    states_a = question_state_counts(world_a)
    states_b = question_state_counts(world_b)
    all_states = sorted(set(states_a) | set(states_b))

    print_comparison_header()
    for state in all_states:
        print_side_by_side_row(state, str(states_a.get(state, 0)), str(states_b.get(state, 0)))
    print()

    all_questions = sorted(
        {q.id for q in world_a.repository.get_all_questions()}
        | {q.id for q in world_b.repository.get_all_questions()}
    )
    for question_id in all_questions:
        q_a = world_a.repository.get_question(question_id)
        q_b = world_b.repository.get_question(question_id)
        state_a = q_a.state if q_a else "(missing)"
        state_b = q_b.state if q_b else "(missing)"
        if state_a != state_b:
            print(f"  {question_id}: A={state_a}, B={state_b}")
    print()


def print_evolution_patterns_comparison(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Side-by-Side: Evolution Patterns ===\n")
    print_comparison_header()
    print_side_by_side_row("Pattern", evolution_pattern(world_a), evolution_pattern(world_b))
    print()

    print("  Tolerance history (World A vs World B):")
    for entry_a, entry_b in zip(world_a.tolerance_log, world_b.tolerance_log):
        print(f"    {entry_a['label']}:")
        names = sorted(set(entry_a["tolerances"]) | set(entry_b["tolerances"]))
        for name in names:
            if name not in entry_a["tolerances"] or name not in entry_b["tolerances"]:
                continue
            print(
                f"      {name}: A pressure={entry_a['pressures'][name]:.2f} "
                f"B pressure={entry_b['pressures'][name]:.2f}"
            )
    print()


def print_summary_statistics(world_a: WorldResult, world_b: WorldResult) -> None:
    print("=== Summary Statistics ===\n")

    a_bird_split = any("Bird" in event for event in world_a.speciation_events)
    b_bird_split = any("Bird" in event for event in world_b.speciation_events)
    a_mammal_split = any("Mammal" in event for event in world_a.speciation_events)
    b_mammal_split = any("Mammal" in event for event in world_b.speciation_events)

    print(f"  Random seed (World B): {RANDOM_SEED}")
    print(f"  Random split chance: {RANDOM_SPLIT_CHANCE}")
    print(f"  Random state change chance: {RANDOM_STATE_CHANGE_CHANCE}")
    print()

    print("  Phenomenon reproduction:")
    print(f"    Bird speciation:     A={a_bird_split}  B={b_bird_split}  match={a_bird_split == b_bird_split}")
    print(f"    Mammal stability:    A={not a_mammal_split}  B={not b_mammal_split}  match={(not a_mammal_split) == (not b_mammal_split)}")
    print(f"    Total speciations:   A={len(world_a.speciation_events)}  B={len(world_b.speciation_events)}")
    print()

    states_a = question_state_counts(world_a)
    states_b = question_state_counts(world_b)
    print(f"  Question state diversity: A={len(states_a)} distinct states  B={len(states_b)} distinct states")
    print(f"  Active questions:         A={states_a.get('ACTIVE', 0)}  B={states_b.get('ACTIVE', 0)}")
    print()

    print("  Interpretation:")
    if a_bird_split != b_bird_split or a_mammal_split != b_mammal_split:
        print("    Random mechanisms did not reproduce pressure-world speciation pattern.")
    else:
        print("    Random mechanisms reproduced pressure-world speciation pattern (coincidence or alignment).")
    if len(states_b) > len(states_a):
        print("    Random world produced more question-state diversity than pressure world.")
    print()


def main() -> None:
    print("=== EXP-010 Random Worlds Comparison ===\n")
    print("World A: contradiction-pressure-based (adaptive tolerance from EXP-009)")
    print("World B: probabilistic splitting and state changes")
    print(f"Shared observation sequence: {len(BIRD_CONFORMING + BIRD_CONTRADICTING + MAMMAL_CONTRADICTING)} observations\n")

    world_a = run_pressure_world()
    world_b = run_random_world()

    print_community_structures_comparison(world_a, world_b)
    print_speciation_comparison(world_a, world_b)
    print_community_statistics_comparison(world_a, world_b)
    print_question_states_comparison(world_a, world_b)
    print_evolution_patterns_comparison(world_a, world_b)
    print_summary_statistics(world_a, world_b)


if __name__ == "__main__":
    main()
