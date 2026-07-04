from dataclasses import dataclass, field
from typing import Any


@dataclass
class AuraRole:
    """
    Represents an internal role in AURA.

    A role is a specialized responsibility area.
    Later, each role can be connected to a different model/provider.
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
