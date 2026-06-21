import time
import uuid

from src.observation import Observation
from src.question import Question
from src.question_repository import QuestionRepository
from src.world_model import WorldModel


class CuriosityEngine:
    DEBT_INCREMENT = 1.0

    def __init__(self, repository: QuestionRepository, world_model: WorldModel) -> None:
        self.repository = repository
        self.world_model = world_model
        self._question_keys: dict[str, str] = {}

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
            id=str(uuid.uuid4())[:8],
            content=content,
            timestamp=time.time(),
        )

        if expected and observed != expected:
            question_key = f"{category}:{expected}"
            text = f"Why doesn't {entity} {expected}?"
        else:
            owner = self._behavior_owner(observed)
            question_key = f"{category}:cross:{observed}"
            text = f"Why does {entity} {observed} like a {owner}?"

        question_id = self._question_keys.get(question_key)
        if question_id:
            question = self.repository.get_question(question_id)
            assert question is not None
            question.times_encountered += 1
            question.curiosity_debt += self.DEBT_INCREMENT * question.times_encountered
            question.related_observations.append(observation.id)
            question.state = "ACTIVE"
            if expected and question.times_encountered >= 2:
                question.text = f"Why don't some {category.lower()}s {expected}?"
            return question

        question = Question(
            id=str(uuid.uuid4())[:8],
            text=text,
            curiosity_debt=self.DEBT_INCREMENT,
            times_encountered=1,
            related_observations=[observation.id],
            state="NEW",
        )
        self.repository.add_question(question)
        self._question_keys[question_key] = question.id
        return question

    def _behavior_owner(self, behavior: str) -> str:
        for category, rule_behavior in self.world_model.rules.items():
            if rule_behavior == behavior:
                return category
        return "unknown"
