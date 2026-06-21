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
RECONSTRUCTION_BUDGET = 1
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

BIRD_TENSION_ID = "t-bird-fly-vs-not_fly"
MAMMAL_TENSION_ID = "t-mammal-fly-vs-swim"
INSECT_TENSION_ID = "t-insect-fly-vs-crawl"

BIRD_QUESTION_ID = "eq-bird-fly-vs-not_fly"
MAMMAL_QUESTION_ID = "eq-mammal-fly-vs-swim"
INSECT_QUESTION_ID = "eq-insect-fly-vs-crawl"

ALL_TENSION_IDS = [BIRD_TENSION_ID, MAMMAL_TENSION_ID, INSECT_TENSION_ID]
ALL_QUESTION_IDS = [BIRD_QUESTION_ID, MAMMAL_QUESTION_ID, INSECT_QUESTION_ID]


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
class ExperimentState:
    observations: list[RawObservation] = field(default_factory=list)
    category_index: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    difference_groups: dict[str, DifferenceGroup] = field(default_factory=dict)
    persistent_tensions: list[PersistentTension] = field(default_factory=list)
    lifecycle_questions: dict[str, LifecycleQuestion] = field(default_factory=dict)
    memory_traces: dict[str, MemoryTrace] = field(default_factory=dict)
    deleted_questions: list[str] = field(default_factory=list)
    competition_events: list[str] = field(default_factory=list)
    reconstruction_winners: list[str] = field(default_factory=list)
    permanent_losses: list[str] = field(default_factory=list)


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def register_observation(
    state: ExperimentState,
    entity: str,
    category: str,
    behavior: str,
) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: ExperimentState, category: str) -> None:
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


def refresh_group_members(state: ExperimentState, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def groups_for_category(state: ExperimentState, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: ExperimentState, category: str) -> list[PersistentTension]:
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


def record_tensions(state: ExperimentState, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: ExperimentState, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def memory_trace_for_tension(state: ExperimentState, tension_id: str) -> MemoryTrace | None:
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


def emerge_questions_from_tensions(state: ExperimentState) -> None:
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


def promote_emergent_questions(state: ExperimentState) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: ExperimentState, tension_id: str, note: str) -> None:
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
            f"tension resolved -> vitality={question.vitality:.1f}, state={question.state} "
            f"({note})"
        )


def apply_vitality_decay(state: ExperimentState, question_id: str) -> None:
    question = state.lifecycle_questions.get(question_id)
    if question is None or question.state == "EXTINCT":
        return

    tension = get_tension(state, question.tension_id)
    tension_resolved = tension.resolved if tension else False

    question.vitality -= DECAY_VITALITY_REDUCTION
    previous_state = question.state
    apply_lifecycle_state(question, tension_resolved=tension_resolved)
    question.lifecycle_history.append(
        f"vitality decay {previous_state} -> {question.state} "
        f"(vitality={question.vitality:.1f})"
    )


def drive_question_to_extinction(state: ExperimentState, question_id: str) -> None:
    while True:
        question = state.lifecycle_questions.get(question_id)
        if question is None or question.state == "EXTINCT":
            return
        apply_vitality_decay(state, question_id)


def trace_strength_from_tension(tension: PersistentTension | None) -> float:
    if tension is None:
        return 0.5
    return min(INITIAL_TRACE_STRENGTH, tension.strength / TRACE_STRENGTH_DIVISOR)


def archive_and_delete_extinct_questions(state: ExperimentState) -> None:
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


def reopen_tension(state: ExperimentState, tension_id: str) -> None:
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
    state: ExperimentState,
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


def ingest_category_observations(
    state: ExperimentState,
    category: str,
    observation_groups: list[list[tuple[str, str, str]]],
) -> None:
    for group in observation_groups:
        for entity, obs_category, behavior in group:
            register_observation(state, entity, obs_category, behavior)
    form_difference_groups(state, category)
    record_tensions(state, category)


def ingest_initial_observations(state: ExperimentState) -> None:
    ingest_category_observations(state, "Bird", [BIRD_CONFORMING, BIRD_CONTRADICTING])
    ingest_category_observations(state, "Mammal", [MAMMAL_FLY, MAMMAL_SWIM])
    ingest_category_observations(state, "Insect", [INSECT_FLY, INSECT_CRAWL])


def process_extinction_lifecycle(state: ExperimentState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for tension_id, note in TENSION_RESOLUTIONS:
        resolve_tension(state, tension_id, note)

    for question_id in ALL_QUESTION_IDS:
        drive_question_to_extinction(state, question_id)


def process_memory_deletion(state: ExperimentState) -> None:
    archive_and_delete_extinct_questions(state)


def ingest_reintroduction_observations(state: ExperimentState) -> None:
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


def reopen_all_tensions(state: ExperimentState) -> list[str]:
    reopened: list[str] = []
    for tension_id in ALL_TENSION_IDS:
        reopen_tension(state, tension_id)
        tension = get_tension(state, tension_id)
        if tension and tension.persistent:
            reopened.append(tension_id)
    return reopened


def run_memory_competition(state: ExperimentState, reopened_tension_ids: list[str]) -> None:
    candidates: list[MemoryTrace] = []

    for tension_id in reopened_tension_ids:
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            state.competition_events.append(f"{tension_id}: skipped (not persistent)")
            continue
        if any(question.tension_id == tension_id for question in state.lifecycle_questions.values()):
            state.competition_events.append(f"{tension_id}: skipped (question already live)")
            continue

        trace = memory_trace_for_tension(state, tension_id)
        if trace is None:
            state.competition_events.append(f"{tension_id}: skipped (no trace)")
            continue

        candidates.append(trace)

    candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))

    state.competition_events.append(
        f"competition start: {len(candidates)} candidates, budget={RECONSTRUCTION_BUDGET}"
    )
    for index, trace in enumerate(candidates):
        state.competition_events.append(
            f"  rank {index + 1}: {trace.trace_id} "
            f"strength={trace.trace_strength:.2f} question={trace.question_id}"
        )

    winners = candidates[:RECONSTRUCTION_BUDGET]
    losers = candidates[RECONSTRUCTION_BUDGET:]

    for trace in losers:
        state.permanent_losses.append(trace.question_id)
        state.competition_events.append(
            f"lost: {trace.trace_id} ({trace.question_id}) — remains extinct"
        )

    for trace in winners:
        tension = get_tension(state, trace.tension_id)
        if tension is None:
            continue
        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstruction_winners.append(question_id)
        state.competition_events.append(
            f"won: {trace.trace_id} -> {question_id} (identity preserved={question_id == trace.question_id})"
        )


def process_reintroduction_and_competition(state: ExperimentState) -> None:
    ingest_reintroduction_observations(state)
    reopened = reopen_all_tensions(state)
    run_memory_competition(state, reopened)


def run_experiment() -> ExperimentState:
    state = ExperimentState()
    ingest_initial_observations(state)
    process_extinction_lifecycle(state)
    process_memory_deletion(state)
    process_reintroduction_and_competition(state)
    return state


def identity_preserved(state: ExperimentState, question_id: str) -> bool:
    question = state.lifecycle_questions.get(question_id)
    if question is None:
        return False
    return question.reconstructed_from_memory and question.id == question_id


def print_memory_traces(state: ExperimentState) -> None:
    print("=== Memory Traces ===\n")
    if not state.memory_traces:
        print("  (none)")
        print()
        return

    for trace_id in sorted(state.memory_traces):
        trace = state.memory_traces[trace_id]
        print(f"  {trace_id}:")
        print(f"    question_id={trace.question_id}")
        print(f"    tension_id={trace.tension_id}")
        print(f"    strength={trace.trace_strength:.2f}")
        print(f"    final_state={trace.final_state}")
    print()


def print_competition_events(state: ExperimentState) -> None:
    print("=== Competition Events ===\n")
    if not state.competition_events:
        print("  (none)")
        print()
        return

    for event in state.competition_events:
        print(f"  {event}")
    print()


def print_reconstruction_winners(state: ExperimentState) -> None:
    print("=== Reconstruction Winners ===\n")
    if not state.reconstruction_winners:
        print("  (none)")
        print()
        return

    for question_id in state.reconstruction_winners:
        question = state.lifecycle_questions.get(question_id)
        origin = "reconstructed" if question and question.reconstructed_from_memory else "unknown"
        print(f"  {question_id} ({origin})")
    print()


def print_permanent_losses(state: ExperimentState) -> None:
    print("=== Permanent Losses ===\n")
    if not state.permanent_losses:
        print("  (none)")
        print()
        return

    for question_id in state.permanent_losses:
        trace_id = f"mem-{question_id}"
        trace = state.memory_traces.get(trace_id)
        strength = f"{trace.trace_strength:.2f}" if trace else "n/a"
        live = question_id in state.lifecycle_questions
        print(f"  {question_id}: trace={trace_id} strength={strength} live={live}")
    print()


def print_question_statistics(state: ExperimentState) -> None:
    print("=== Question Statistics ===\n")
    print(f"  Deleted (archived): {len(state.deleted_questions)}")
    print(f"  Live after competition: {len(state.lifecycle_questions)}")
    print(f"  Reconstruction winners: {len(state.reconstruction_winners)}")
    print(f"  Permanent losses: {len(state.permanent_losses)}")
    print()

    for question_id in ALL_QUESTION_IDS:
        question = state.lifecycle_questions.get(question_id)
        if question:
            print(
                f"  {question_id}: LIVE state={question.state} "
                f"vitality={question.vitality:.1f} "
                f"reconstructed={question.reconstructed_from_memory}"
            )
        elif question_id in state.permanent_losses:
            print(f"  {question_id}: EXTINCT (lost competition)")
        else:
            print(f"  {question_id}: EXTINCT (archived only)")
    print()


def print_overall_organization(state: ExperimentState) -> None:
    print("=== Overall Organization ===\n")
    print(f"  Observations: {len(state.observations)}")
    print(f"  Difference groups: {len(state.difference_groups)}")
    print(f"  Persistent tensions: {sum(1 for t in state.persistent_tensions if t.persistent)}")
    print(f"  Memory traces: {len(state.memory_traces)}")
    print(f"  Reconstruction budget: {RECONSTRUCTION_BUDGET}")
    print()

    print("  Identity preservation:")
    for question_id in ALL_QUESTION_IDS:
        preserved = identity_preserved(state, question_id)
        status = "preserved" if preserved else "not reconstructed"
        print(f"    {question_id}: {status}")
    print()

    print("  Observations:")
    print("    Three categories extincted and archived; all tensions reopened at reintroduction.")
    print("    Traces ranked by strength; budget allows one reconstruction winner.")
    print("    Weaker traces remain in memory but do not become live questions.")
    print()


def main() -> None:
    print("=== EXP-017 Memory Trace Competition ===\n")
    print("Pipeline: observations -> differences -> tensions -> questions -> extinction -> traces")
    print(f"Reconstruction budget: {RECONSTRUCTION_BUDGET} (limited resources)\n")

    state = run_experiment()

    print_memory_traces(state)
    print_competition_events(state)
    print_reconstruction_winners(state)
    print_permanent_losses(state)
    print_question_statistics(state)
    print_overall_organization(state)


if __name__ == "__main__":
    main()
