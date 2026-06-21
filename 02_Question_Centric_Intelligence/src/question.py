from dataclasses import dataclass, field


@dataclass
class Question:
    id: str
    text: str
    curiosity_debt: float = 0.0
    importance: float = 1.0
    confidence: float = 0.0
    state: str = "NEW"
    parent_questions: list[str] = field(default_factory=list)
    child_questions: list[str] = field(default_factory=list)
    times_encountered: int = 0
    related_observations: list[str] = field(default_factory=list)
