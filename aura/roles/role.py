from dataclasses import dataclass, field
from typing import Any


@dataclass
class AuraRole:
    """
    Represents an internal role in AURA.

    A role is a responsibility area inside AURA.
    Later, each role can use different models, skills, and plugins.
    """

    name: str
    description: str
    provider: str
    model: str
    status: str = "planned"
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "provider": self.provider,
            "model": self.model,
            "status": self.status,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }
