import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

DIFFERENCE_MIN_PER_GROUP = 2
PERSISTENT_TENSION_MIN = 2
RESOLUTION_VITALITY_REDUCTION = 2.0
DORMANT_VITALITY_THRESHOLD = 1.0
DECAY_VITALITY_REDUCTION = 1.0
INITIAL_TRACE_STRENGTH = 1.0
TRACE_STRENGTH_DIVISOR = 4.0

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
    reconstructed_from_memory: bool = False


@dataclass
class MemoryTrace:
    trace_id: str
    tension_id: str
    question_id: str
    category: str
    behavior_a: str
    behavior_b: str
    source_groups: list[str]
    text: str
    lifecycle_history: list[str]
    final_vitality: float
    final_state: str
    trace_strength: float = INITIAL_TRACE_STRENGTH


@dataclass
class WorldState:
    label: str
    world_id: str
    persistent_memory: bool
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    phase_events: list[str] = field(default_factory=list)
    decay_events: list[str] = field(default_factory=list)
    reconstructed_questions: list[str] = field(default_factory=list)
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


def memory_trace_for_tension(state: WorldState, tension_id: str) -> MemoryTrace | None:
    for trace in state.memory_traces.values():
        if trace.tension_id == tension_id and trace.trace_strength > 0.0:
            return trace
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


def trace_strength_from_tension(tension: PersistentTension | None) -> float:
    if tension is None:
        return 0.5
    return min(INITIAL_TRACE_STRENGTH, tension.strength / TRACE_STRENGTH_DIVISOR)


def archive_persistent_traces(state: WorldState) -> None:
    for question_id, question in list(state.lifecycle_questions.items()):
        if question.state != "EXTINCT":
            continue

        tension = get_tension(state, question.tension_id)
        trace_id = f"mem-{question_id}"
        state.memory_traces[trace_id] = MemoryTrace(
            trace_id=trace_id,
            tension_id=question.tension_id,
            question_id=question.id,
            category=question.category,
            behavior_a=tension.behavior_a if tension else "",
            behavior_b=tension.behavior_b if tension else "",
            source_groups=list(question.source_groups),
            text=question.text,
            lifecycle_history=list(question.lifecycle_history),
            final_vitality=question.vitality,
            final_state=question.state,
            trace_strength=trace_strength_from_tension(tension),
        )
        del state.lifecycle_questions[question_id]
        state.deleted_questions.append(question_id)

    state.phase_events.append(
        f"archived {len(state.memory_traces)} persistent traces"
    )


def decay_transient_traces(state: WorldState) -> None:
    for question_id, question in list(state.lifecycle_questions.items()):
        if question.state != "EXTINCT":
            continue

        trace_id = f"mem-{question_id}"
        state.decay_events.append(
            f"transient: {trace_id} formed from {question_id} and decayed immediately"
        )
        del state.lifecycle_questions[question_id]
        state.deleted_questions.append(question_id)

    state.phase_events.append(
        "transient memory: no traces retained (immediate decay after use)"
    )


def process_memory_traces(state: WorldState) -> None:
    if state.persistent_memory:
        archive_persistent_traces(state)
        return

    decay_transient_traces(state)


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


def reconstruct_from_memory(
    state: WorldState,
    trace: MemoryTrace,
    tension: PersistentTension,
) -> str:
    question = LifecycleQuestion(
        id=trace.question_id,
        text=trace.text,
        category=trace.category,
        source_groups=list(trace.source_groups),
        tension_id=tension.id,
        vitality=tension.strength,
        reconstructed_from_memory=True,
        lifecycle_history=list(trace.lifecycle_history),
    )
    question.lifecycle_history.append(
        f"RECONSTRUCTED from memory (vitality={question.vitality:.1f}, trace={trace.trace_id})"
    )
    question.state = "ACTIVE"
    question.lifecycle_history.append("RECONSTRUCTED -> ACTIVE (promoted)")
    state.lifecycle_questions[question.id] = question
    return question.id


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
        reconstructed_from_memory=False,
    )
    question.lifecycle_history.append(
        f"EMERGENT (fresh, vitality={question.vitality:.1f}, tension={tension.id}, no trace)"
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


def process_persistent_reintroduction(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reintroduction: {len(reopened_tension_ids)} tensions reopened, reconstruction enabled"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            continue

        trace = memory_trace_for_tension(state, tension_id)
        if trace is None:
            state.phase_events.append(f"{tension_id}: skipped (no persistent trace)")
            continue

        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstructed_questions.append(question_id)
        state.phase_events.append(
            f"reconstructed: {trace.trace_id} -> {question_id} (identity preserved)"
        )


def process_transient_reintroduction(state: WorldState, reopened_tension_ids: list[str]) -> None:
    state.phase_events.append(
        f"reintroduction: {len(reopened_tension_ids)} tensions reopened, "
        f"no reconstruction (traces decayed)"
    )

    for tension_id in sorted(reopened_tension_ids):
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            continue

        if memory_trace_for_tension(state, tension_id) is not None:
            state.phase_events.append(f"{tension_id}: unexpected trace remains")
            continue

        question_id = emerge_fresh_question(state, tension)
        state.emergent_questions.append(question_id)
        state.phase_events.append(
            f"fresh emergence: {question_id} (no identity preservation, no reconstruction)"
        )


def process_reintroduction(state: WorldState) -> None:
    ingest_reintroduction_observations(state)
    reopened = reopen_all_tensions(state)

    if state.persistent_memory:
        process_persistent_reintroduction(state, reopened)
        return

    process_transient_reintroduction(state, reopened)


def run_world(persistent_memory: bool) -> WorldState:
    if persistent_memory:
        state = WorldState(
            label="World A (Persistence)",
            world_id="A",
            persistent_memory=True,
        )
    else:
        state = WorldState(
            label="World B (Transient)",
            world_id="B",
            persistent_memory=False,
        )

    ingest_initial_observations(state)
    process_question_lifecycle(state)
    process_memory_traces(state)
    process_reintroduction(state)
    return state


def run_experiment() -> tuple[WorldState, WorldState]:
    world_a = run_world(persistent_memory=True)
    world_b = run_world(persistent_memory=False)
    return world_a, world_b


def print_comparison_row(label: str, value_a: str, value_b: str) -> None:
    print(f"  {label:<32} {value_a:<24} {value_b}")


def persistent_tension_count(state: WorldState) -> int:
    return sum(1 for tension in state.persistent_tensions if tension.persistent)


def identity_preserved_count(state: WorldState) -> int:
    return sum(
        1 for question in state.lifecycle_questions.values()
        if question.reconstructed_from_memory and len(question.lifecycle_history) > 2
    )


def organization_survives(state: WorldState) -> bool:
    return (
        len(state.difference_groups) > 0
        and persistent_tension_count(state) > 0
    )


def print_world_statistics(world_a: WorldState, world_b: WorldState) -> None:
    print("=== World Statistics ===\n")
    print_comparison_row("Metric", "World A (Persistence)", "World B (Transient)")
    print_comparison_row("Observations", str(len(world_a.observations)), str(len(world_b.observations)))
    print_comparison_row("Difference groups", str(len(world_a.difference_groups)), str(len(world_b.difference_groups)))
    print_comparison_row("Persistent tensions", str(persistent_tension_count(world_a)), str(persistent_tension_count(world_b)))
    print_comparison_row("Memory traces", str(len(world_a.memory_traces)), str(len(world_b.memory_traces)))
    print_comparison_row("Live questions", str(len(world_a.lifecycle_questions)), str(len(world_b.lifecycle_questions)))
    print_comparison_row("Decay events", str(len(world_a.decay_events)), str(len(world_b.decay_events)))
    print_comparison_row("Organization survives", str(organization_survives(world_a)), str(organization_survives(world_b)))
    print()


def print_persistence_patterns(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Persistence Patterns ===\n")
    print_comparison_row("Metric", "World A", "World B")
    print_comparison_row("Stable traces", str(len(world_a.memory_traces) > 0), str(len(world_b.memory_traces) > 0))
    print_comparison_row("Trace count", str(len(world_a.memory_traces)), str(len(world_b.memory_traces)))
    print_comparison_row("Reconstruction", str(len(world_a.reconstructed_questions) > 0), "False")
    print_comparison_row("Identity preserved", str(identity_preserved_count(world_a) > 0), "False")
    print_comparison_row("Immediate trace decay", "False", str(len(world_b.decay_events) > 0))
    print()

    print("  World A traces:")
    for trace_id in sorted(world_a.memory_traces):
        trace = world_a.memory_traces[trace_id]
        print(f"    {trace_id}: strength={trace.trace_strength:.2f} stable=True")
    if not world_a.memory_traces:
        print("    (none)")
    print()

    print("  World B decay events:")
    for event in world_b.decay_events:
        print(f"    {event}")
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
        "Questions reappear",
        str(len(world_a.reconstructed_questions) > 0),
        str(len(world_b.emergent_questions) > 0),
    )
    print_comparison_row(
        "Reconstruction motif",
        str(len(world_a.reconstructed_questions) > 0),
        "False",
    )
    print_comparison_row(
        "Fresh emergence motif",
        "False",
        str(len(world_b.emergent_questions) > 0),
    )
    print()

    for question_id in ALL_QUESTION_IDS:
        live_a = question_id in world_a.lifecycle_questions
        live_b = question_id in world_b.lifecycle_questions
        origin_a = "reconstructed" if live_a and world_a.lifecycle_questions[question_id].reconstructed_from_memory else "absent"
        origin_b = "fresh" if live_b and not world_b.lifecycle_questions[question_id].reconstructed_from_memory else "absent"
        print(f"  {question_id}:")
        print(f"    A: live={live_a} origin={origin_a}")
        print(f"    B: live={live_b} origin={origin_b}")
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
        f"{len(world_b.lifecycle_questions)} live",
    )
    print_comparison_row(
        "Memory layer",
        f"{len(world_a.memory_traces)} traces",
        f"{len(world_b.memory_traces)} traces",
    )
    print_comparison_row(
        "Structure without memory",
        "False",
        str(organization_survives(world_b)),
    )
    print()

    print("  Difference groups (both worlds identical):")
    for group_name in sorted(world_a.difference_groups):
        group = world_a.difference_groups[group_name]
        print(f"    {group_name}: {len(group.members)} members")
    print()


def print_overall_observations(world_a: WorldState, world_b: WorldState) -> None:
    print("=== Overall Observations ===\n")

    print("  1. Both worlds share identical observations, differences, and tensions through initial lifecycle.")
    print("  2. World A retains stable memory traces; reconstruction with identity preservation enabled.")
    print("  3. World B removes stable memory, identity preservation, and reconstruction — traces decay immediately.")
    print(
        f"  4. Organization survives in both: "
        f"A={organization_survives(world_a)} B={organization_survives(world_b)}."
    )
    print(
        f"  5. Questions reappear: A via reconstruction ({len(world_a.reconstructed_questions)}), "
        f"B via fresh emergence ({len(world_b.emergent_questions)})."
    )
    print(
        f"  6. Tensions remain in both worlds after reintroduction: "
        f"A={persistent_tension_count(world_a)} B={persistent_tension_count(world_b)}."
    )
    print(
        f"  7. Difference groups alone maintain structure: "
        f"{len(world_a.difference_groups)} groups in each world."
    )
    print()
    print("  Interpretation:")
    print("    Persistence enables reconstruction and identity continuity.")
    print("    Without persistence, organization survives at difference and tension layers.")
    print("    Questions reappear through fresh emergence, not memory reconstruction.")
    print("    Attack on persistence reveals which motifs depend on stable traces.")
    print()


def main() -> None:
    print("=== EXP-022 Persistence Removal ===\n")
    print("Pipeline: observations -> differences -> tensions -> questions -> memory traces")
    print("World A: persistent traces, identity preserved, reconstruction enabled")
    print("World B: transient traces, no identity, no reconstruction, immediate decay\n")

    world_a, world_b = run_experiment()

    print_world_statistics(world_a, world_b)
    print_persistence_patterns(world_a, world_b)
    print_surviving_motifs(world_a, world_b)
    print_organization_patterns(world_a, world_b)
    print_overall_observations(world_a, world_b)


if __name__ == "__main__":
    main()
