import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0

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

TENSION_RESOLUTIONS = [
    ("t-bird-fly-vs-not_fly", "niche specialization resolves bird behavior conflict"),
    ("t-mammal-fly-vs-swim", "locomotion niche resolves mammal behavior conflict"),
    ("t-insect-fly-vs-crawl", "body plan resolves insect behavior conflict"),
]

ALL_TENSION_IDS = [
    "t-bird-fly-vs-not_fly",
    "t-insect-fly-vs-crawl",
    "t-mammal-fly-vs-swim",
]

ALL_QUESTION_IDS = [
    "eq-bird-fly-vs-not_fly",
    "eq-insect-fly-vs-crawl",
    "eq-mammal-fly-vs-swim",
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
class LifecycleQuestion:
    id: str
    text: str
    category: str
    source_groups: list[str]
    tension_id: str
    state: str = "EMERGENT"
    vitality: float = 0.0
    lifecycle_history: list[str] = field(default_factory=list)


@dataclass
class WorldState:
    label: str
    world_id: str
    questions_enabled: bool
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    phase_events: list[str] = field(default_factory=list)
    emergent_questions: list[str] = field(default_factory=list)


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


def question_id_for_tension(tension: PersistentTension) -> str:
    return (
        f"eq-{tension.category.lower()}-{behavior_key(tension.behavior_a)}-vs-"
        f"{behavior_key(tension.behavior_b)}"
    )


def apply_lifecycle_state(question: LifecycleQuestion, tension_resolved: bool) -> None:
    if question.vitality <= 0.0:
        question.state = "EXTINCT"
    elif question.vitality <= DORMANT_VITALITY_THRESHOLD:
        question.state = "DORMANT"
    elif tension_resolved:
        question.state = "RESOLVED"
    elif question.state == "EMERGENT":
        pass
    else:
        question.state = "ACTIVE"


def emerge_questions_from_tensions(state: WorldState) -> None:
    for tension in state.persistent_tensions:
        if not tension.persistent:
            continue
        if tension.id in {question.tension_id for question in state.lifecycle_questions.values()}:
            continue

        question_id = question_id_for_tension(tension)
        question = LifecycleQuestion(
            id=question_id,
            text=(
                f"Why do {tension.category} entities both {tension.behavior_a} "
                f"and {tension.behavior_b}?"
            ),
            category=tension.category,
            source_groups=[tension.group_a, tension.group_b],
            tension_id=tension.id,
            vitality=tension.strength,
        )
        question.lifecycle_history.append(
            f"EMERGENT (vitality={question.vitality:.1f}, tension={tension.id})"
        )
        state.lifecycle_questions[question_id] = question


def promote_emergent_questions(state: WorldState) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: WorldState, tension_id: str, note: str) -> None:
    tension = get_tension(state, tension_id)
    if tension is None or tension.resolved:
        return

    tension.resolved = True
    tension.resolution_note = note

    for question in state.lifecycle_questions.values():
        if question.tension_id != tension_id:
            continue
        question.vitality -= RESOLUTION_VITALITY_REDUCTION
        apply_lifecycle_state(question, tension_resolved=True)
        question.lifecycle_history.append(
            f"tension resolved -> vitality={question.vitality:.1f}, state={question.state} ({note})"
        )


def apply_vitality_decay(state: WorldState, question_id: str) -> None:
    question = state.lifecycle_questions.get(question_id)
    if question is None or question.state == "EXTINCT":
        return

    tension = get_tension(state, question.tension_id)
    tension_resolved = tension.resolved if tension else False

    question.vitality -= DECAY_VITALITY_REDUCTION
    previous_state = question.state
    apply_lifecycle_state(question, tension_resolved=tension_resolved)
    question.lifecycle_history.append(
        f"vitality decay {previous_state} -> {question.state} (vitality={question.vitality:.1f})"
    )


def drive_question_to_extinction(state: WorldState, question_id: str) -> None:
    while True:
        question = state.lifecycle_questions.get(question_id)
        if question is None or question.state == "EXTINCT":
            return
        apply_vitality_decay(state, question_id)


def delete_extinct_questions(state: WorldState) -> None:
    for question_id, question in list(state.lifecycle_questions.items()):
        if question.state != "EXTINCT":
            continue
        del state.lifecycle_questions[question_id]
        state.deleted_questions.append(question_id)

    state.phase_events.append(
        f"deleted {len(state.deleted_questions)} extinct questions (no memory traces)"
    )


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


def emerge_fresh_question(state: WorldState, tension: PersistentTension) -> str:
    question_id = question_id_for_tension(tension)
    question = LifecycleQuestion(
        id=question_id,
        text=(
            f"Why do {tension.category} entities both {tension.behavior_a} "
            f"and {tension.behavior_b}?"
        ),
        category=tension.category,
        source_groups=[tension.group_a, tension.group_b],
        tension_id=tension.id,
        vitality=tension.strength,
    )
    question.lifecycle_history.append(
        f"EMERGENT (fresh, vitality={question.vitality:.1f}, tension={tension.id})"
    )
    question.state = "ACTIVE"
    question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")
    state.lifecycle_questions[question_id] = question
    return question_id


def ingest_category_observations(
    state: WorldState,
    category: str,
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            register_observation(state, entity, obs_category, behavior)
    form_difference_groups(state, category)
    record_tensions(state, category)


def ingest_initial_observations(state: WorldState) -> None:
    ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
    ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
    ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])


def process_question_lifecycle(state: WorldState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in ALL_QUESTION_IDS:
        drive_question_to_extinction(state, question_id)

    delete_extinct_questions(state)


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


def process_question_reintroduction(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reintroduction: {len(reopened_tension_ids)} tensions reopened, fresh emergence enabled"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            continue

        question_id = emerge_fresh_question(state, tension)
        state.emergent_questions.append(question_id)
        state.phase_events.append(f"fresh emergence: {question_id} from {tension_id}")


def process_tension_only_reintroduction(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reintroduction: {len(reopened_tension_ids)} tensions reopened, no question layer"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            state.phase_events.append(f"{tension_id}: not persistent")
            continue
        state.phase_events.append(
            f"tension active: {tension_id} strength={tension.strength:.1f} (no question object)"
        )


def process_reintroduction(state: WorldState) -> None:
    ingest_reintroduction_observations(state)
    reopened = reopen_all_tensions(state)

    if state.questions_enabled:
        process_question_reintroduction(state, reopened)
        return

    process_tension_only_reintroduction(state, reopened)


def run_world(questions_enabled: bool) -> WorldState:
    if questions_enabled:
        state = WorldState(
            label="World A (Questions + Fresh Emergence)",
            world_id="A",
            questions_enabled=True,
        )
    else:
        state = WorldState(
            label="World B (Differences + Tensions Only)",
            world_id="B",
            questions_enabled=False,
        )

    ingest_initial_observations(state)

    if state.questions_enabled:
        process_question_lifecycle(state)

    process_reintroduction(state)
    return state


def run_experiment() -> tuple[WorldState, WorldState]:
    world_a = run_world(questions_enabled=True)
    world_b = run_world(questions_enabled=False)
    return world_a, world_b


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<32} {value_a:<24} {value_b}")


def persistent_tension_count(state: WorldState) -> int:
    return sum(1 for tension in state.persistent_tensions if tension.persistent)


def organization_survives(state: WorldState) -> bool:
    return len(state.difference_groups) > 0 and persistent_tension_count(state) > 0


def print_world_statistics(world_a: WorldState, world_b: WorldState) -> None:
    print("=== World Statistics ===\n")
    print_comparison_row("Metric", "World A (Questions)", "World B (No Questions)")
    print_comparison_row("Observations", str(len(world_a.observations)), str(len(world_b.observations)))
    print_comparison_row("Difference groups", str(len(world_a.difference_groups)), str(len(world_b.difference_groups)))
    print_comparison_row("Persistent tensions", str(persistent_tension_count(world_a)), str(persistent_tension_count(world_b)))
    print_comparison_row("Live questions", str(len(world_a.lifecycle_questions)), str(len(world_b.lifecycle_questions)))
    print_comparison_row("Question objects used", "True", "False")
    print_comparison_row("Memory traces", "0", "0")
    print_comparison_row("Fresh emergences", str(len(world_a.emergent_questions)), "0")
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
        f"{persistent_tension_count(world_b)} persistent",
    )
    print_comparison_row(
        "Question layer",
        f"{len(world_a.lifecycle_questions)} live",
        "none",
    )
    print_comparison_row(
        "Structure without questions",
        "False",
        str(organization_survives(world_b)),
    )
    print()

    print("  Persistent tensions (both worlds):")
    for tension_id in ALL_TENSION_IDS:
        tension_a = get_tension(world_a, tension_id)
        tension_b = get_tension(world_b, tension_id)
        strength_a = f"{tension_a.strength:.1f}" if tension_a else "n/a"
        strength_b = f"{tension_b.strength:.1f}" if tension_b else "n/a"
        persistent_a = tension_a.persistent if tension_a else False
        persistent_b = tension_b.persistent if tension_b else False
        print(
            f"    {tension_id}: A strength={strength_a} persistent={persistent_a} | "
            f"B strength={strength_b} persistent={persistent_b}"
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
        str(persistent_tension_count(world_b)),
    )
    print_comparison_row(
        "Questions",
        str(len(world_a.lifecycle_questions)),
        "0",
    )
    print_comparison_row(
        "Fresh emergence",
        str(len(world_a.emergent_questions)),
        "0",
    )
    print_comparison_row(
        "Question IDs",
        "True",
        "False",
    )
    print_comparison_row(
        "Question states",
        "True",
        "False",
    )
    print()


def print_overall_observations(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds share identical observations, difference groups, and tension records.")
    print("  2. World A runs the question lifecycle and fresh emergence on reintroduction.")
    print("  3. World B removes question objects, question IDs, states, and memory entirely.")
    print(
        f"  4. Organization survives in both: "
        f"A={organization_survives(world_a)} B={organization_survives(world_b)}."
    )
    print(
        f"  5. Tensions alone maintain structure in World B: "
        f"{persistent_tension_count(world_b)} persistent tensions, "
        f"{len(world_b.difference_groups)} difference groups."
    )
    print(
        f"  6. World A live questions after reintro: {len(world_a.lifecycle_questions)}; "
        f"World B live questions: {len(world_b.lifecycle_questions)}."
    )
    print(
        f"  7. Difference groups identical: {len(world_a.difference_groups)} in each world."
    )
    print()
    print("  Interpretation:")
    print("    Attack on questions tests whether organization requires question objects.")
    print("    World B shows differences and tensions maintain structure without questions.")
    print("    Questions compress tensions into live objects — optional, not structural.")
    print("    Fresh emergence in World A re-derives questions; World B needs no derivation.")
    print()


def main() -> None:
    print("=== EXP-023 Question Removal ===\n")
    print("Pipeline base: observations -> differences -> tensions")
    print("World A: + questions + fresh emergence (no memory traces)")
    print("World B: differences and tensions only — no question layer\n")

    world_a, world_b = run_experiment()

    print_world_statistics(world_a, world_b)
    print_organization_patterns(world_a, world_b)
    print_surviving_motifs(world_a, world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
