import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2

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

ALL_TENSION_IDS = [
    "t-bird-fly-vs-not_fly",
    "t-insect-fly-vs-crawl",
    "t-mammal-fly-vs-swim",
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
class PersistentTension:
    id: str
    category: str
    group_a: str
    group_b: str
    behavior_a: str
    behavior_b: str
    strength: float
    persistent: bool
    resolved: bool = False
    resolution_note: str = ""


@dataclass
class WorldState:
    label: str
    world_id: str
    tensions_enabled: bool
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    phase_events: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


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


def groups_for_category(state: WorldState, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: WorldState, category: str) -> list[PersistentTension]:
    groups = groups_for_category(state, category)
    tensions: list[PersistentTension] = []

    for index, group_a in enumerate(groups):
        for group_b in groups[index + 1:]:
            strength = float(min(len(group_a.members), len(group_b.members)))
            persistent = strength >= PERSISTENT_TENSION_MIN
            tension_id = (
                f"t-{category.lower()}-{behavior_key(group_a.behavior)}-vs-{behavior_key(group_b.behavior)}"
            )
            tensions.append(PersistentTension(
                id=tension_id,
                category=category,
                group_a=group_a.name,
                group_b=group_b.name,
                behavior_a=group_a.behavior,
                behavior_b=group_b.behavior,
                strength=strength,
                persistent=persistent,
            ))

    return tensions


def record_tensions(state: WorldState, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: WorldState, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def reopen_tension(state: WorldState, tension_id: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None:
        return

    group_a = state.difference_groups.get(tension.group_a)
    group_b = state.difference_groups.get(tension.group_b)
    if group_a and group_b:
        tension.strength = float(min(len(group_a.members), len(group_b.members)))

    tension.resolved = False
    tension.resolution_note = ""
    tension.persistent = tension.strength >= PERSISTENT_TENSION_MIN


def ingest_category_observations(
    state: WorldState,
    category: str,
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            register_observation(state, entity, obs_category, behavior)
    form_difference_groups(state, category)
    if state.tensions_enabled:
        record_tensions(state, category)


def ingest_initial_observations(state: WorldState) -> None:
    ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
    ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
    ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])

    if state.tensions_enabled:
        state.phase_events.append(
            f"initial: {len(state.difference_groups)} difference groups, "
            f"{persistent_tension_count(state)} persistent tensions"
        )
        return

    state.phase_events.append(
        f"initial: {len(state.difference_groups)} difference groups, no tension layer"
    )


def ingest_reintroduction_observations(state: WorldState) -> None:
    ingest_category_observations(
        state,
        "Bird",
        [BIRD_REINTRO_CONFORMING, BIRD_REINTRO_CONTRADICTING],
    )
    refresh_group_members(state, "Bird")

    ingest_category_observations(
        state,
        "Mammal",
        [MAMMAL_REINTRO_FLY, MAMMAL_REINTRO_SWIM],
    )
    refresh_group_members(state, "Mammal")

    ingest_category_observations(
        state,
        "Insect",
        [INSECT_REINTRO_FLY, INSECT_REINTRO_CRAWL],
    )
    refresh_group_members(state, "Insect")


def reopen_all_tensions(state: WorldState) -> list[str]:
    reopened: list[str] = []
    for tension_id in ALL_TENSION_IDS:
        reopen_tension(state, tension_id)
        tension = get_tension(state, tension_id)
        if tension and tension.persistent:
            reopened.append(tension_id)
    return reopened


def process_tension_reintroduction(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reintroduction: {len(reopened_tension_ids)} tensions reopened, no question layer"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            continue
        state.phase_events.append(
            f"tension active: {tension_id} strength={tension.strength:.1f}"
        )


def process_difference_only_reintroduction(state: WorldState) -> None:
    state.phase_events.append(
        f"reintroduction: {len(state.difference_groups)} difference groups refreshed, "
        f"no tension layer"
    )

    for group_name in sorted(state.difference_groups):
        group = state.difference_groups[group_name]
        state.phase_events.append(
            f"difference active: {group_name} members={len(group.members)} "
            f"behavior={group.behavior}"
        )


def process_reintroduction(state: WorldState) -> None:
    ingest_reintroduction_observations(state)

    if state.tensions_enabled:
        reopened = reopen_all_tensions(state)
        process_tension_reintroduction(state, reopened)
        return

    process_difference_only_reintroduction(state)


def run_world(tensions_enabled: bool) -> WorldState:
    if tensions_enabled:
        state = WorldState(
            label="World A (Differences + Tensions)",
            world_id="A",
            tensions_enabled=True,
        )
    else:
        state = WorldState(
            label="World B (Differences Only)",
            world_id="B",
            tensions_enabled=False,
        )

    ingest_initial_observations(state)
    process_reintroduction(state)
    return state


def run_experiment() -> tuple[WorldState, WorldState]:
    world_a = run_world(tensions_enabled=True)
    world_b = run_world(tensions_enabled=False)
    return world_a, world_b


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<32} {value_a:<24} {value_b}")


def persistent_tension_count(state: WorldState) -> int:
    return sum(1 for tension in state.persistent_tensions if tension.persistent)


def organization_survives(state: WorldState) -> bool:
    if state.tensions_enabled:
        return len(state.difference_groups) > 0 and persistent_tension_count(state) > 0
    return len(state.difference_groups) > 0


def print_world_statistics(world_a: WorldState, world_b: WorldState) -> None:
    print("=== World Statistics ===\n")
    print_comparison_row("Metric", "World A (Tensions)", "World B (No Tensions)")
    print_comparison_row("Observations", str(len(world_a.observations)), str(len(world_b.observations)))
    print_comparison_row("Difference groups", str(len(world_a.difference_groups)), str(len(world_b.difference_groups)))
    print_comparison_row("Persistent tensions", str(persistent_tension_count(world_a)), str(persistent_tension_count(world_b)))
    print_comparison_row("Tension objects used", "True", "False")
    print_comparison_row("Tension IDs", "True", "False")
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
        f"{len(world_b.difference_groups)} groups",
    )
    print_comparison_row(
        "Tension structure",
        f"{persistent_tension_count(world_a)} persistent",
        "none",
    )
    print_comparison_row(
        "Structure without tensions",
        "False",
        str(organization_survives(world_b)),
    )
    print()

    print("  Difference groups (both worlds):")
    for group_name in sorted(world_a.difference_groups):
        group_a = world_a.difference_groups[group_name]
        group_b = world_b.difference_groups[group_name]
        print(
            f"    {group_name}: A members={len(group_a.members)} | "
            f"B members={len(group_b.members)}"
        )
    print()

    print("  Persistent tensions (World A only):")
    for tension_id in ALL_TENSION_IDS:
        tension = get_tension(world_a, tension_id)
        if tension is None:
            print(f"    {tension_id}: (absent)")
            continue
        print(
            f"    {tension_id}: strength={tension.strength:.1f} "
            f"persistent={tension.persistent}"
        )
    print()


def print_surviving_motifs(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Surviving Motifs ===\n")
    print_comparison_row("Motif", "World A", "World B")
    print_comparison_row(
        "Differences",
        str(len(world_a.difference_groups)),
        str(len(world_b.difference_groups)),
    )
    print_comparison_row(
        "Tensions",
        str(persistent_tension_count(world_a)),
        "0",
    )
    print_comparison_row(
        "Tension strength tracking",
        "True",
        "False",
    )
    print_comparison_row(
        "Questions",
        "0",
        "0",
    )
    print_comparison_row(
        "Difference-only structure",
        "False",
        str(len(world_b.difference_groups) > 0),
    )
    print()


def print_overall_observations(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds share identical observations and difference group formation.")
    print("  2. World A retains persistent tensions; no questions, memory, or reconstruction.")
    print("  3. World B removes tension objects, tension IDs, strength, and persistent tensions.")
    print(
        f"  4. Organization survives in both: "
        f"A={organization_survives(world_a)} B={organization_survives(world_b)}."
    )
    print(
        f"  5. Difference groups identical: {len(world_a.difference_groups)} in each world."
    )
    print(
        f"  6. World A persistent tensions after reintro: {persistent_tension_count(world_a)}; "
        f"World B tensions: {persistent_tension_count(world_b)}."
    )
    print(
        f"  7. World B maintains structure with difference groups alone: "
        f"{len(world_b.difference_groups)} groups active."
    )
    print()
    print("  Interpretation:")
    print("    Attack on tensions tests whether organization requires tension objects.")
    print("    World B shows difference groups alone maintain structural organization.")
    print("    Tensions pair and rank group conflicts — optional layer above differences.")
    print("    No questions, memory, persistence, or reconstruction in either world.")
    print()


def main() -> None:
    print("=== EXP-024 Tension Removal ===\n")
    print("Pipeline base: observations -> differences")
    print("World A: + persistent tensions (no questions, memory, reconstruction)")
    print("World B: differences only — no tension layer\n")

    world_a, world_b = run_experiment()

    print_world_statistics(world_a, world_b)
    print_organization_patterns(world_a, world_b)
    print_surviving_motifs(world_a, world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
