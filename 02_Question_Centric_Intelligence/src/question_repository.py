from src.question import Question


class QuestionRepository:
    def __init__(self) -> None:
        self._questions: dict[str, Question] = {}

    def add_question(self, question: Question) -> None:
        self._questions[question.id] = question

    def get_question(self, question_id: str) -> Question | None:
        return self._questions.get(question_id)

    def get_all_questions(self) -> list[Question]:
        return list(self._questions.values())

    def get_active_questions(self) -> list[Question]:
        active_states = {"NEW", "ACTIVE", "INVESTIGATING", "PARTIALLY_RESOLVED"}
        return [q for q in self._questions.values() if q.state in active_states]

    def merge_questions(
        self,
        target_id: str,
        source_id: str,
        source_state: str = "DORMANT",
    ) -> Question:
        target = self._questions[target_id]
        source = self._questions[source_id]

        target.curiosity_debt += source.curiosity_debt
        target.times_encountered += source.times_encountered
        target.related_observations.extend(source.related_observations)

        if source_id not in target.parent_questions:
            target.parent_questions.append(source_id)
        if target_id not in source.child_questions:
            source.child_questions.append(target_id)

        source.state = source_state
        return target
