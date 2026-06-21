import time

from src.observation import Observation
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel


class CuriosityEngine:
    DEBT_INCREMENT = 1.0

    def __init__(self, repository: QuestionRepository, world_model: WorldModel) -> None:
        self.repository = repository
        self.world_model = world_model

    def process_prediction_failure(
        self,
        entity: str,
        category: str,
        observed_behavior: str,
        content: str,
    ) -> Question:
        observed = observed_behavior.lower()
        expected = self.world_model.predict(category)
        observation = Observation(
            id=f"obs-{entity.lower()}-{observed.replace(' ', '-')}",
            content=content,
            timestamp=time.time(),
        )

        if expected and observed != expected:
            text = f"Why doesn't {entity} {expected}?"
            question_id = f"q-{entity.lower()}"
            question_category = category
            expected_behavior = expected
            observed_behavior = observed
        else:
            owner = self._behavior_owner(observed)
            text = f"Why does {entity} {observed} like a {owner}?"
            question_id = f"q-{entity.lower()}"
            question_category = category
            expected_behavior = ""
            observed_behavior = observed

        existing = self.repository.get_question(question_id)
        if existing is not None:
            existing.times_encountered += 1
            existing.curiosity_debt += self.DEBT_INCREMENT * existing.times_encountered
            existing.related_observations.append(observation.id)
            existing.state = "ACTIVE"
            return existing

        question = Question(
            id=question_id,
            text=text,
            curiosity_debt=self.DEBT_INCREMENT,
            times_encountered=1,
            related_observations=[observation.id],
            state="NEW",
            category=question_category,
            expected_behavior=expected_behavior,
            observed_behavior=observed_behavior,
        )
        self.repository.add_question(question)
        return question

    def _behavior_owner(self, behavior: str) -> str:
        for category, rule_behavior in self.world_model.rules.items():
            if rule_behavior == behavior:
                return category
        return "unknown"
