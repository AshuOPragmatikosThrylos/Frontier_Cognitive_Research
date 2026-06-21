from dataclasses import dataclass


@dataclass
class Observation:
    id: str
    content: str
    timestamp: float
