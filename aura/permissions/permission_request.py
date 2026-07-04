from dataclasses import dataclass
from typing import Any

from aura.permissions.permission_level import PermissionLevel


@dataclass
class PermissionCheckResult:
    """
    Result of checking whether AURA may perform an action.
    """

    action: str
    level: PermissionLevel
    allowed: bool
    requires_confirmation: bool
    description: str
    reason: str
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "level": int(self.level),
            "level_name": self.level.name,
            "level_label": self.level.label,
            "allowed": self.allowed,
            "requires_confirmation": self.requires_confirmation,
            "description": self.description,
            "reason": self.reason,
            "metadata": self.metadata or {},
        }
