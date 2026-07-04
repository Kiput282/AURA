from dataclasses import dataclass, field
from typing import Any


@dataclass
class PluginAction:
    """
    Represents an action exposed by a plugin.

    This is metadata only for now.
    Execution will be added in a later sprint.
    """

    name: str
    plugin: str
    description: str
    permission_action: str
    status: str = "planned"
    skill: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "plugin": self.plugin,
            "description": self.description,
            "permission_action": self.permission_action,
            "status": self.status,
            "skill": self.skill,
            "metadata": self.metadata,
        }
