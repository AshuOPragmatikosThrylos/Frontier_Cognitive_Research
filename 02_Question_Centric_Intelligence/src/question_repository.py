from src.question import Question


class QuestionRepository:
    def __init__(self) -> None:
        self._questions: dict[str, Question] = {}

    def add_question(self, question: Question) -> None:
        self._questions[question.id] = question

    def get_question(self, question_id: str) -> Question | None:
        return self._questions.get(question_id)

    def get_active_questions(self) -> list[Question]:
        active_states = {"NEW", "ACTIVE", "INVESTIGATING", "PARTIALLY_RESOLVED"}
        return [q for q in self._questions.values() if q.state in active_states]

    def merge_questions(self, target_id: str, source_id: str) -> Question:
        target = self._questions[target_id]
        source = self._questions[source_id]

        target.curiosity_debt += source.curiosity_debt
        target.times_encountered += source.times_encountered
        target.related_observations.extend(source.related_observations)
        target.child_questions.extend(source.child_questions)

        del self._questions[source_id]
        return target
