class WorldModel:
    def __init__(self) -> None:
        self.rules: dict[str, str] = {}

    def add_rule(self, category: str, behavior: str) -> None:
        self.rules[category] = behavior.lower()

    def predict(self, category: str) -> str | None:
        return self.rules.get(category)
