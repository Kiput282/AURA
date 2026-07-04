from dataclasses import dataclass, field
from typing import Any


@dataclass
class AuraSkill:
    """
    Represents a named ability that AURA currently has or plans to have.

    Skill sits between role, permission, and plugin/action systems.
    """

    name: str
    description: str
    role: str
    permission_action: str
    status: str = "planned"
    capabilities: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "role": self.role,
            "permission_action": self.permission_action,
            "status": self.status,
            "capabilities": self.capabilities,
            "metadata": self.metadata,
        }
