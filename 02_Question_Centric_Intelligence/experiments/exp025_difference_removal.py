import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2

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

MAMMAL_FLY = [
    ("Bat", "Mammal", "fly"),
    ("Squirrel", "Mammal", "fly"),
]

MAMMAL_SWIM = [
    ("Whale", "Mammal", "swim"),
    ("Dolphin", "Mammal", "swim"),
]

INSECT_FLY = [
    ("Bee", "Insect", "fly"),
    ("Ant", "Insect", "fly"),
]

INSECT_CRAWL = [
    ("Beetle", "Insect", "crawl"),
    ("Spider", "Insect", "crawl"),
]

BIRD_REINTRO_CONFORMING = [
    ("Crow", "Bird", "fly"),
    ("Raven", "Bird", "fly"),
]

BIRD_REINTRO_CONTRADICTING = [
    ("Chicken", "Bird", "not fly"),
    ("Turkey", "Bird", "not fly"),
]

MAMMAL_REINTRO_FLY = [
    ("Mouse", "Mammal", "fly"),
    ("Shrew", "Mammal", "fly"),
]

MAMMAL_REINTRO_SWIM = [
    ("Otter", "Mammal", "swim"),
    ("Beaver", "Mammal", "swim"),
]

INSECT_REINTRO_FLY = [
    ("Wasp", "Insect", "fly"),
    ("Fly", "Insect", "fly"),
]

INSECT_REINTRO_CRAWL = [
    ("Centipede", "Insect", "crawl"),
    ("Mantis", "Insect", "crawl"),
]


@dataclass
class RawObservation:
    entity: str
    category: str
    behavior: str


@dataclass
class DifferenceGroup:
    name: str
    category: str
    behavior: str
    members: list[str] = field(default_factory=list)


@dataclass
class WorldState:
    label: str
    world_id: str
    differences_enabled: bool
    observations: list[RawObservation] = field(default_factory=list)
    raw_entities: list[str] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    phase_events: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_raw_entity(state: WorldState, entity: str) -> None:
    state.raw_entities.append(entity)


def register_observation(
    state: WorldState,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: WorldState, category: str) -> None:
    groups = state.category_index.get(category, {})
    if len(groups) < 2:
        return
    if not all(len(members) >= DIFFERENCE_MIN_PER_GROUP for members in groups.values()):
        return

    for behavior, members in sorted(groups.items()):
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            continue
        state.difference_groups[group_name] = DifferenceGroup(
            name=group_name,
            category=category,
            behavior=behavior,
            members=list(members),
        )


def refresh_group_members(state: WorldState, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def ingest_observation_batch(
    state: WorldState,
    observation_groups: list[list[tuple[str, str, str]]],
    category: str | None = None,
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            if state.differences_enabled:
                register_observation(state, entity, obs_category, behavior)
            else:
                register_raw_entity(state, entity)

    if not state.differences_enabled:
        return

    if category is not None:
        form_difference_groups(state, category)


def ingest_initial_observations(state: WorldState) -> None:
    ingest_observation_batch(state, [BIRD_CONFORMING, BIRD_CONTRADICTING], "Bird")
    ingest_observation_batch(state, [MAMMAL_FLY, MAMMAL_SWIM], "Mammal")
    ingest_observation_batch(state, [INSECT_FLY, INSECT_CRAWL], "Insect")

    if state.differences_enabled:
        state.phase_events.append(
            f"initial: {len(state.difference_groups)} difference groups, no higher layers"
        )
        return

    state.phase_events.append(
        f"initial: {len(state.raw_entities)} raw observations, no difference layer"
    )


def ingest_reintroduction_observations(state: WorldState) -> None:
    ingest_observation_batch(
        state,
        [BIRD_REINTRO_CONFORMING, BIRD_REINTRO_CONTRADICTING],
        "Bird",
    )
    if state.differences_enabled:
        refresh_group_members(state, "Bird")

    ingest_observation_batch(
        state,
        [MAMMAL_REINTRO_FLY, MAMMAL_REINTRO_SWIM],
        "Mammal",
    )
    if state.differences_enabled:
        refresh_group_members(state, "Mammal")

    ingest_observation_batch(
        state,
        [INSECT_REINTRO_FLY, INSECT_REINTRO_CRAWL],
        "Insect",
    )
    if state.differences_enabled:
        refresh_group_members(state, "Insect")


def process_difference_reintroduction(state: WorldState) -> None:
    state.phase_events.append(
        f"reintroduction: {len(state.difference_groups)} difference groups refreshed"
    )

    for group_name in sorted(state.difference_groups):
        group = state.difference_groups[group_name]
        state.phase_events.append(
            f"difference active: {group_name} members={len(group.members)} "
            f"behavior={group.behavior}"
        )


def process_raw_reintroduction(state: WorldState) -> None:
    state.phase_events.append(
        f"reintroduction: {len(state.raw_entities)} raw observations, no difference layer"
    )

    for entity in state.raw_entities[-12:]:
        state.phase_events.append(f"raw observation: {entity}")


def process_reintroduction(state: WorldState) -> None:
    ingest_reintroduction_observations(state)

    if state.differences_enabled:
        process_difference_reintroduction(state)
        return

    process_raw_reintroduction(state)


def run_world(differences_enabled: bool) -> WorldState:
    if differences_enabled:
        state = WorldState(
            label="World A (Difference Groups)",
            world_id="A",
            differences_enabled=True,
        )
    else:
        state = WorldState(
            label="World B (Raw Observations Only)",
            world_id="B",
            differences_enabled=False,
        )

    ingest_initial_observations(state)
    process_reintroduction(state)
    return state


def run_experiment() -> tuple[WorldState, WorldState]:
    world_a = run_world(differences_enabled=True)
    world_b = run_world(differences_enabled=False)
    return world_a, world_b


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<32} {value_a:<24} {value_b}")


def observation_count(state: WorldState) -> int:
    if state.differences_enabled:
        return len(state.observations)
    return len(state.raw_entities)


def category_count(state: WorldState) -> int:
    if not state.differences_enabled:
        return 0
    return len(state.category_index)


def organization_survives(state: WorldState) -> bool:
    if not state.differences_enabled:
        return False
    return len(state.difference_groups) > 0


def print_world_statistics(world_a: WorldState, world_b: WorldState) -> None:
    print("=== World Statistics ===\n")
    print_comparison_row("Metric", "World A (Differences)", "World B (Raw Only)")
    print_comparison_row("Observations", str(observation_count(world_a)), str(observation_count(world_b)))
    print_comparison_row("Difference groups", str(len(world_a.difference_groups)), str(len(world_b.difference_groups)))
    print_comparison_row("Categories", str(category_count(world_a)), str(category_count(world_b)))
    print_comparison_row("Partitions", str(len(world_a.difference_groups)), "0")
    print_comparison_row("Distinction objects", "True", "False")
    print_comparison_row("Tensions", "0", "0")
    print_comparison_row("Questions", "0", "0")
    print_comparison_row("Memory traces", "0", "0")
    print_comparison_row("Organization survives", str(organization_survives(world_a)), str(organization_survives(world_b)))
    print()


def print_organization_patterns(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Organization Patterns ===\n")
    print_comparison_row("Layer", "World A", "World B")
    print_comparison_row(
        "Difference structure",
        f"{len(world_a.difference_groups)} groups",
        "none",
    )
    print_comparison_row(
        "Category structure",
        f"{category_count(world_a)} categories",
        "none",
    )
    print_comparison_row(
        "Raw observation stream",
        "structured",
        f"{observation_count(world_b)} flat entries",
    )
    print_comparison_row(
        "Structure without differences",
        "False",
        str(organization_survives(world_b)),
    )
    print()

    print("  Difference groups (World A only):")
    for group_name in sorted(world_a.difference_groups):
        group = world_a.difference_groups[group_name]
        print(
            f"    {group_name}: members={len(group.members)} behavior={group.behavior}"
        )
    print()

    print("  Raw observations (World B only, last 6):")
    for entity in world_b.raw_entities[-6:]:
        print(f"    {entity}")
    print()


def print_surviving_motifs(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Surviving Motifs ===\n")
    print_comparison_row("Motif", "World A", "World B")
    print_comparison_row(
        "Differences",
        str(len(world_a.difference_groups)),
        "0",
    )
    print_comparison_row(
        "Categories",
        str(category_count(world_a)),
        "0",
    )
    print_comparison_row(
        "Partitions",
        str(len(world_a.difference_groups)),
        "0",
    )
    print_comparison_row(
        "Raw entities",
        str(observation_count(world_a)),
        str(observation_count(world_b)),
    )
    print_comparison_row(
        "Tensions",
        "0",
        "0",
    )
    print_comparison_row(
        "Questions",
        "0",
        "0",
    )
    print_comparison_row(
        "Difference-only structure",
        str(len(world_a.difference_groups) > 0),
        "False",
    )
    print()


def print_overall_observations(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds receive identical entity streams through the pipeline.")
    print("  2. World A forms difference groups; no tensions, questions, memory, or reconstruction.")
    print("  3. World B stores raw entities only — no groups, labels, categories, or partitions.")
    print(
        f"  4. Organization survives: "
        f"A={organization_survives(world_a)} B={organization_survives(world_b)}."
    )
    print(
        f"  5. World A difference groups: {len(world_a.difference_groups)}; "
        f"World B difference groups: {len(world_b.difference_groups)}."
    )
    print(
        f"  6. Observation counts match: A={observation_count(world_a)} B={observation_count(world_b)}."
    )
    print(
        f"  7. World B has no organizational structure beyond flat observation list."
    )
    print()
    print("  Interpretation:")
    print("    Attack on differences tests whether organization requires difference groups.")
    print("    World A shows difference groups maintain structural organization.")
    print("    World B shows raw observations alone do not produce organization.")
    print("    Differences appear necessary for organization in this pipeline.")
    print("    No tensions, questions, memory, persistence, selection, or reconstruction.")
    print()


def main() -> None:
    print("=== EXP-025 Difference Removal ===\n")
    print("Pipeline base: observations")
    print("World A: difference groups only (no tensions, questions, memory, reconstruction)")
    print("World B: raw observations only — no difference layer\n")

    world_a, world_b = run_experiment()

    print_world_statistics(world_a, world_b)
    print_organization_patterns(world_a, world_b)
    print_surviving_motifs(world_a, world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
