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
class CategorySpec:
    name: str
    group_a: list[tuple[str, str, str]]
    group_b: list[tuple[str, str, str]]
    reintro_a: list[tuple[str, str, str]]
    reintro_b: list[tuple[str, str, str]]
    resolution_note: str


@dataclass
class DomainSpec:
    domain_id: str
    label: str
    categories: list[CategorySpec]


@dataclass
class DomainState:
    spec: DomainSpec
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

    @property
    def question_ids(self) -> list[str]:
        return [question_id_for_category(category.name) for category in self.spec.categories]

    @property
    def tension_ids(self) -> list[str]:
        tensions = []
        for category in self.spec.categories:
            behavior_a = category.group_a[0][2].lower()
            behavior_b = category.group_b[0][2].lower()
            tensions.append(tension_id_for_category(category.name, behavior_a, behavior_b))
        return tensions


def behavior_key(behavior: str) -> str:
    return behavior.replace(" ", "_")


def tension_id_for_category(category: str, behavior_a: str, behavior_b: str) -> str:
    return f"t-{category.lower()}-{behavior_key(behavior_a)}-vs-{behavior_key(behavior_b)}"


def question_id_for_category(category: str) -> str:
    return f"eq-{category.lower()}"


def question_id_for_tension(tension: PersistentTension) -> str:
    return question_id_for_category(tension.category)


DOMAIN_SPECS = [
    DomainSpec(
        domain_id="animals",
        label="Animals",
        categories=[
            CategorySpec(
                name="Bird",
                group_a=[
                    ("Sparrow", "Bird", "fly"),
                    ("Robin", "Bird", "fly"),
                    ("Eagle", "Bird", "fly"),
                    ("Falcon", "Bird", "fly"),
                ],
                group_b=[
                    ("Penguin", "Bird", "not fly"),
                    ("Ostrich", "Bird", "not fly"),
                    ("Emu", "Bird", "not fly"),
                    ("Kiwi", "Bird", "not fly"),
                ],
                reintro_a=[("Crow", "Bird", "fly"), ("Raven", "Bird", "fly")],
                reintro_b=[("Chicken", "Bird", "not fly"), ("Turkey", "Bird", "not fly")],
                resolution_note="niche specialization resolves bird behavior conflict",
            ),
            CategorySpec(
                name="Mammal",
                group_a=[("Bat", "Mammal", "fly"), ("Squirrel", "Mammal", "fly")],
                group_b=[("Whale", "Mammal", "swim"), ("Dolphin", "Mammal", "swim")],
                reintro_a=[("Mouse", "Mammal", "fly"), ("Shrew", "Mammal", "fly")],
                reintro_b=[("Otter", "Mammal", "swim"), ("Beaver", "Mammal", "swim")],
                resolution_note="locomotion niche resolves mammal behavior conflict",
            ),
        ],
    ),
    DomainSpec(
        domain_id="software_bugs",
        label="Software Bugs",
        categories=[
            CategorySpec(
                name="Deadlock",
                group_a=[
                    ("LockA", "Deadlock", "blocking"),
                    ("LockB", "Deadlock", "blocking"),
                    ("LockC", "Deadlock", "blocking"),
                    ("LockD", "Deadlock", "blocking"),
                ],
                group_b=[
                    ("Mutex1", "Deadlock", "non-blocking"),
                    ("Mutex2", "Deadlock", "non-blocking"),
                    ("Mutex3", "Deadlock", "non-blocking"),
                    ("Mutex4", "Deadlock", "non-blocking"),
                ],
                reintro_a=[("LockE", "Deadlock", "blocking"), ("LockF", "Deadlock", "blocking")],
                reintro_b=[("Mutex5", "Deadlock", "non-blocking"), ("Mutex6", "Deadlock", "non-blocking")],
                resolution_note="timeout strategy resolves deadlock conflict",
            ),
            CategorySpec(
                name="MemoryLeak",
                group_a=[("HeapA", "MemoryLeak", "growing"), ("HeapB", "MemoryLeak", "growing")],
                group_b=[("PoolA", "MemoryLeak", "stable"), ("PoolB", "MemoryLeak", "stable")],
                reintro_a=[("HeapC", "MemoryLeak", "growing"), ("HeapD", "MemoryLeak", "growing")],
                reintro_b=[("PoolC", "MemoryLeak", "stable"), ("PoolD", "MemoryLeak", "stable")],
                resolution_note="gc cycle resolves memory leak conflict",
            ),
            CategorySpec(
                name="RaceCondition",
                group_a=[("ThreadA", "RaceCondition", "unordered"), ("ThreadB", "RaceCondition", "unordered")],
                group_b=[("ThreadC", "RaceCondition", "ordered"), ("ThreadD", "RaceCondition", "ordered")],
                reintro_a=[("ThreadE", "RaceCondition", "unordered"), ("ThreadF", "RaceCondition", "unordered")],
                reintro_b=[("ThreadG", "RaceCondition", "ordered"), ("ThreadH", "RaceCondition", "ordered")],
                resolution_note="locking resolves race condition conflict",
            ),
        ],
    ),
    DomainSpec(
        domain_id="scientific_theories",
        label="Scientific Theories",
        categories=[
            CategorySpec(
                name="WaveTheory",
                group_a=[
                    ("Photons", "WaveTheory", "continuous"),
                    ("Light", "WaveTheory", "continuous"),
                    ("Sound", "WaveTheory", "continuous"),
                    ("Ripple", "WaveTheory", "continuous"),
                ],
                group_b=[
                    ("Quantum", "WaveTheory", "discrete"),
                    ("Packet", "WaveTheory", "discrete"),
                    ("Pulse", "WaveTheory", "discrete"),
                    ("Grain", "WaveTheory", "discrete"),
                ],
                reintro_a=[("Laser", "WaveTheory", "continuous"), ("Radio", "WaveTheory", "continuous")],
                reintro_b=[("Quanta", "WaveTheory", "discrete"), ("Photon2", "WaveTheory", "discrete")],
                resolution_note="complementarity resolves wave conflict",
            ),
            CategorySpec(
                name="ParticleTheory",
                group_a=[("Electron", "ParticleTheory", "localized"), ("Proton", "ParticleTheory", "localized")],
                group_b=[("FieldA", "ParticleTheory", "diffuse"), ("FieldB", "ParticleTheory", "diffuse")],
                reintro_a=[("Neutron", "ParticleTheory", "localized"), ("Muon", "ParticleTheory", "localized")],
                reintro_b=[("FieldC", "ParticleTheory", "diffuse"), ("FieldD", "ParticleTheory", "diffuse")],
                resolution_note="field theory resolves particle conflict",
            ),
            CategorySpec(
                name="Relativity",
                group_a=[("FrameA", "Relativity", "relative"), ("FrameB", "Relativity", "relative")],
                group_b=[("FrameC", "Relativity", "absolute"), ("FrameD", "Relativity", "absolute")],
                reintro_a=[("FrameE", "Relativity", "relative"), ("FrameF", "Relativity", "relative")],
                reintro_b=[("FrameG", "Relativity", "absolute"), ("FrameH", "Relativity", "absolute")],
                resolution_note="invariant interval resolves relativity conflict",
            ),
        ],
    ),
    DomainSpec(
        domain_id="distributed_databases",
        label="Distributed Databases",
        categories=[
            CategorySpec(
                name="Consistency",
                group_a=[
                    ("NodeA", "Consistency", "strong"),
                    ("NodeB", "Consistency", "strong"),
                    ("NodeC", "Consistency", "strong"),
                    ("NodeD", "Consistency", "strong"),
                ],
                group_b=[
                    ("NodeE", "Consistency", "eventual"),
                    ("NodeF", "Consistency", "eventual"),
                    ("NodeG", "Consistency", "eventual"),
                    ("NodeH", "Consistency", "eventual"),
                ],
                reintro_a=[("NodeI", "Consistency", "strong"), ("NodeJ", "Consistency", "strong")],
                reintro_b=[("NodeK", "Consistency", "eventual"), ("NodeL", "Consistency", "eventual")],
                resolution_note="quorum resolves consistency conflict",
            ),
            CategorySpec(
                name="Availability",
                group_a=[("ReplicaA", "Availability", "up"), ("ReplicaB", "Availability", "up")],
                group_b=[("ReplicaC", "Availability", "down"), ("ReplicaD", "Availability", "down")],
                reintro_a=[("ReplicaE", "Availability", "up"), ("ReplicaF", "Availability", "up")],
                reintro_b=[("ReplicaG", "Availability", "down"), ("ReplicaH", "Availability", "down")],
                resolution_note="redundancy resolves availability conflict",
            ),
            CategorySpec(
                name="PartitionTolerance",
                group_a=[("ShardA", "PartitionTolerance", "tolerant"), ("ShardB", "PartitionTolerance", "tolerant")],
                group_b=[("ShardC", "PartitionTolerance", "intolerant"), ("ShardD", "PartitionTolerance", "intolerant")],
                reintro_a=[("ShardE", "PartitionTolerance", "tolerant"), ("ShardF", "PartitionTolerance", "tolerant")],
                reintro_b=[("ShardG", "PartitionTolerance", "intolerant"), ("ShardH", "PartitionTolerance", "intolerant")],
                resolution_note="cap tradeoff resolves partition conflict",
            ),
        ],
    ),
]


def register_observation(state: DomainState, entity: str, category: str, behavior: str) -> None:
    behavior = behavior.lower()
    state.observations.append(RawObservation(entity=entity, category=category, behavior=behavior))
    state.category_index.setdefault(category, {}).setdefault(behavior, []).append(entity)


def form_difference_groups(state: DomainState, category: str) -> None:
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


def refresh_group_members(state: DomainState, category: str) -> None:
    groups = state.category_index.get(category, {})
    for behavior, members in groups.items():
        group_name = f"{category}.{behavior_key(behavior)}"
        if group_name in state.difference_groups:
            state.difference_groups[group_name].members = list(members)


def groups_for_category(state: DomainState, category: str) -> list[DifferenceGroup]:
    return sorted(
        (group for group in state.difference_groups.values() if group.category == category),
        key=lambda group: group.name,
    )


def detect_persistent_tensions(state: DomainState, category: str) -> list[PersistentTension]:
    groups = groups_for_category(state, category)
    tensions: list[PersistentTension] = []

    for index, group_a in enumerate(groups):
        for group_b in groups[index + 1:]:
            strength = float(min(len(group_a.members), len(group_b.members)))
            persistent = strength >= PERSISTENT_TENSION_MIN
            tension_id = tension_id_for_category(category, group_a.behavior, group_b.behavior)
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


def record_tensions(state: DomainState, category: str) -> None:
    existing_ids = {tension.id for tension in state.persistent_tensions}
    for tension in detect_persistent_tensions(state, category):
        if tension.id not in existing_ids:
            state.persistent_tensions.append(tension)
            existing_ids.add(tension.id)


def get_tension(state: DomainState, tension_id: str) -> PersistentTension | None:
    for tension in state.persistent_tensions:
        if tension.id == tension_id:
            return tension
    return None


def memory_trace_for_tension(state: DomainState, tension_id: str) -> MemoryTrace | None:
    for trace in state.memory_traces.values():
        if trace.tension_id == tension_id and trace.trace_strength > 0.0:
            return trace
    return None


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


def emerge_questions_from_tensions(state: DomainState) -> None:
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


def promote_emergent_questions(state: DomainState) -> None:
    for question in state.lifecycle_questions.values():
        if question.state != "EMERGENT":
            continue
        tension = get_tension(state, question.tension_id)
        if tension is None or tension.resolved:
            continue
        question.state = "ACTIVE"
        question.lifecycle_history.append("EMERGENT -> ACTIVE (promoted)")


def resolve_tension(state: DomainState, tension_id: str, note: str) -> None:
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


def apply_vitality_decay(state: DomainState, question_id: str) -> None:
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


def drive_question_to_extinction(state: DomainState, question_id: str) -> None:
    while True:
        question = state.lifecycle_questions.get(question_id)
        if question is None or question.state == "EXTINCT":
            return
        apply_vitality_decay(state, question_id)


def trace_strength_from_tension(tension: PersistentTension | None) -> float:
    if tension is None:
        return 0.5
    return min(INITIAL_TRACE_STRENGTH, tension.strength / TRACE_STRENGTH_DIVISOR)


def archive_and_delete_extinct_questions(state: DomainState) -> None:
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


def reopen_tension(state: DomainState, tension_id: str) -> None:
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
    state: DomainState,
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


def ingest_category(state: DomainState, category_spec: CategorySpec) -> None:
    for entity, category, behavior in category_spec.group_a + category_spec.group_b:
        register_observation(state, entity, category, behavior)
    form_difference_groups(state, category_spec.name)
    record_tensions(state, category_spec.name)


def ingest_reintroduction(state: DomainState, category_spec: CategorySpec) -> None:
    for entity, category, behavior in category_spec.reintro_a + category_spec.reintro_b:
        register_observation(state, entity, category, behavior)
    refresh_group_members(state, category_spec.name)


def process_extinction_lifecycle(state: DomainState) -> None:
    emerge_questions_from_tensions(state)
    promote_emergent_questions(state)

    for category_spec in state.spec.categories:
        behavior_a = category_spec.group_a[0][2].lower()
        behavior_b = category_spec.group_b[0][2].lower()
        tension_id = tension_id_for_category(category_spec.name, behavior_a, behavior_b)
        resolve_tension(state, tension_id, category_spec.resolution_note)

    for question_id in state.question_ids:
        drive_question_to_extinction(state, question_id)


def run_memory_competition(state: DomainState, reopened_tension_ids: list[str]) -> None:
    prefix = f"[{state.spec.domain_id}]"
    candidates: list[MemoryTrace] = []

    for tension_id in reopened_tension_ids:
        tension = get_tension(state, tension_id)
        if tension is None or not tension.persistent:
            state.competition_events.append(f"{prefix} {tension_id}: skipped (not persistent)")
            continue

        trace = memory_trace_for_tension(state, tension_id)
        if trace is None:
            state.competition_events.append(f"{prefix} {tension_id}: skipped (no trace)")
            continue

        candidates.append(trace)

    candidates.sort(key=lambda trace: (-trace.trace_strength, trace.trace_id))

    state.competition_events.append(
        f"{prefix} competition start: {len(candidates)} candidates, budget={RECONSTRUCTION_BUDGET}"
    )
    for index, trace in enumerate(candidates):
        state.competition_events.append(
            f"{prefix}   rank {index + 1}: {trace.trace_id} "
            f"strength={trace.trace_strength:.2f} question={trace.question_id}"
        )

    winners = candidates[:RECONSTRUCTION_BUDGET]
    losers = candidates[RECONSTRUCTION_BUDGET:]

    for trace in losers:
        state.permanent_losses.append(trace.question_id)
        state.competition_events.append(
            f"{prefix} lost: {trace.trace_id} ({trace.question_id})"
        )

    for trace in winners:
        tension = get_tension(state, trace.tension_id)
        if tension is None:
            continue
        question_id = reconstruct_from_memory(state, trace, tension)
        state.reconstruction_winners.append(question_id)
        state.competition_events.append(
            f"{prefix} won: {trace.trace_id} -> {question_id}"
        )


def run_domain(spec: DomainSpec) -> DomainState:
    state = DomainState(spec=spec)

    for category_spec in spec.categories:
        ingest_category(state, category_spec)

    process_extinction_lifecycle(state)
    archive_and_delete_extinct_questions(state)

    for category_spec in spec.categories:
        ingest_reintroduction(state, category_spec)

    reopened: list[str] = []
    for tension_id in state.tension_ids:
        reopen_tension(state, tension_id)
        tension = get_tension(state, tension_id)
        if tension and tension.persistent:
            reopened.append(tension_id)

    run_memory_competition(state, reopened)
    return state


def run_experiment() -> list[DomainState]:
    return [run_domain(spec) for spec in DOMAIN_SPECS]


def winner_strength(state: DomainState) -> float:
    if not state.reconstruction_winners:
        return 0.0
    winner_id = state.reconstruction_winners[0]
    trace_id = f"mem-{winner_id}"
    trace = state.memory_traces.get(trace_id)
    return trace.trace_strength if trace else 0.0


def strongest_category_name(state: DomainState) -> str:
    if not state.reconstruction_winners:
        return "(none)"
    return state.reconstruction_winners[0].replace("eq-", "")


def print_domain_statistics(states: list[DomainState]) -> None:
    print("=== Domain Statistics ===\n")
    print(f"  {'Domain':<24} {'Categories':<12} {'Traces':<8} {'Winners':<8} {'Losers':<8}")
    for state in states:
        print(
            f"  {state.spec.label:<24} "
            f"{len(state.spec.categories):<12} "
            f"{len(state.memory_traces):<8} "
            f"{len(state.reconstruction_winners):<8} "
            f"{len(state.permanent_losses):<8}"
        )
    print()


def print_competition_events(states: list[DomainState]) -> None:
    print("=== Competition Events ===\n")
    for state in states:
        print(f"  --- {state.spec.label} ---")
        domain_events = [
            event for event in state.competition_events
            if event.startswith(f"[{state.spec.domain_id}]")
        ]
        for event in domain_events:
            print(f"  {event}")
        print()


def print_selection_outcomes(states: list[DomainState]) -> None:
    print("=== Selection Outcomes ===\n")
    for state in states:
        winner = state.reconstruction_winners[0] if state.reconstruction_winners else "(none)"
        print(f"  {state.spec.label}:")
        print(f"    winner: {winner}")
        print(f"    losers: {state.permanent_losses or ['(none)']}")
        print(f"    selection emerged: {len(state.reconstruction_winners) > 0}")
        print(f"    competition occurred: {len(state.competition_events) > 0}")
    print()


def print_cross_domain_similarities(states: list[DomainState]) -> None:
    print("=== Cross-Domain Similarities ===\n")

    winners = [strongest_category_name(state) for state in states]
    winner_counts = len(set(winners))
    all_have_winners = all(state.reconstruction_winners for state in states)
    all_have_losers = all(state.permanent_losses for state in states)
    budget = RECONSTRUCTION_BUDGET

    print(f"  All domains produced winners: {all_have_winners}")
    print(f"  All domains produced losers: {all_have_losers}")
    print(f"  Reconstruction budget (shared): {budget}")
    print(f"  Winner pattern: strongest trace (strength 1.00) in each domain")
    print()

    for state in states:
        traces = sorted(state.memory_traces.values(), key=lambda t: -t.trace_strength)
        strengths = [f"{t.category}={t.trace_strength:.2f}" for t in traces]
        print(f"  {state.spec.label}: trace strengths [{', '.join(strengths)}]")
    print()


def print_overall_observations(states: list[DomainState]) -> None:
    print("=== Overall Observations ===\n")
    print("  1. Identical rules applied across all four domains.")
    print("  2. Each domain: observations -> differences -> tensions -> questions -> extinction -> traces -> competition.")
    print("  3. Selection reproduced when trace strength differentiated winners from losers.")
    print("  4. Domains with one strong (4+4) and weak (2+2) categories show same selection pattern.")
    print()

    for index, state in enumerate(states, start=1):
        print(
            f"  Domain {index} ({state.spec.label}): "
            f"winner={state.reconstruction_winners[0] if state.reconstruction_winners else 'none'}, "
            f"losers={len(state.permanent_losses)}"
        )
    print()


def main() -> None:
    print("=== EXP-020 Cross-Domain Selection Reproduction ===\n")
    print("Domains: Animals, Software Bugs, Scientific Theories, Distributed Databases")
    print("Pipeline: observations -> differences -> tensions -> questions -> extinction -> traces -> competition")
    print(f"Shared rules: budget={RECONSTRUCTION_BUDGET}, strength=min(1.0, tension/4.0)\n")

    states = run_experiment()

    print_domain_statistics(states)
    print_competition_events(states)
    print_selection_outcomes(states)
    print_cross_domain_similarities(states)
    print_overall_observations(states)


if __name__ == "__main__":
    main()
