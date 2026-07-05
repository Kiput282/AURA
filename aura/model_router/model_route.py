from dataclasses import dataclass, field
from typing import Any


@dataclass
class ModelRoute:
    """
    Metadata-only model route for AURA.

    Current phase:
    - recommends provider/model per role or task
    - does not download models
    - does not switch runtime automatically
    """

    name: str
    role: str
    provider: str
    model: str
    status: str
    description: str
    use_cases: list[str] = field(default_factory=list)
    candidate_models: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "role": self.role,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "description": self.description,
            "use_cases": self.use_cases,
            "candidate_models": self.candidate_models,
            "safety_notes": self.safety_notes,
            "metadata": self.metadata,
        }
