from src.question import Question
from src.question_repository import QuestionRepository

MERGEABLE_STATES = {"NEW", "ACTIVE", "INVESTIGATING"}


def similarity_key(question: Question) -> tuple[str, str, str] | None:
    if not question.category or not question.expected_behavior or not question.observed_behavior:
        return None
    return (question.category, question.expected_behavior, question.observed_behavior)


def find_merge_candidates(repository: QuestionRepository) -> list[list[Question]]:
    groups: dict[tuple[str, str, str], list[Question]] = {}

    for question in repository.get_all_questions():
        if question.state not in MERGEABLE_STATES:
            continue
        key = similarity_key(question)
        if key is None:
            continue
        groups.setdefault(key, []).append(question)

    return [members for members in groups.values() if len(members) >= 2]


def abstract_text(category: str, expected_behavior: str) -> str:
    return f"Why don't some {category.lower()}s {expected_behavior}?"


def merge_candidates(
    repository: QuestionRepository,
    candidates: list[Question],
    source_state: str = "PARTIALLY_RESOLVED",
) -> tuple[Question, int]:
    category, expected_behavior, _ = similarity_key(candidates[0])  # type: ignore[misc]
    abstract_id = f"q-abstract-{category.lower()}-{expected_behavior.replace(' ', '-')}"

    abstract = Question(
        id=abstract_id,
        text=abstract_text(category, expected_behavior),
        state="ACTIVE",
        category=category,
        expected_behavior=expected_behavior,
        observed_behavior=candidates[0].observed_behavior,
    )
    repository.add_question(abstract)

    merge_count = 0
    for source in candidates:
        repository.merge_questions(abstract.id, source.id, source_state=source_state)
        merge_count += 1

    return abstract, merge_count


def merge_all_candidates(repository: QuestionRepository) -> tuple[list[Question], int]:
    merged: list[Question] = []
    total_merges = 0

    for group in find_merge_candidates(repository):
        abstract, count = merge_candidates(repository, group)
        merged.append(abstract)
        total_merges += count

    return merged, total_merges
