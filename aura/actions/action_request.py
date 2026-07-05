from dataclasses import dataclass
from typing import Any


@dataclass
class ActionRequest:
    """
    Represents a safe action request proposal.

    This is metadata/proposal only.
    It does not execute the action.
    """

    requested_action: str
    resolved_action: str
    plugin_action_found: bool
    plugin: str | None
    skill: str | None
    plugin_action_status: str
    permission_action: str
    permission_level: int
    permission_level_name: str
    permission_level_label: str
    allowed: bool
    requires_confirmation: bool
    request_state: str
    description: str
    reason: str
    note: str
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "requested_action": self.requested_action,
            "resolved_action": self.resolved_action,
            "plugin_action_found": self.plugin_action_found,
            "plugin": self.plugin,
            "skill": self.skill,
            "plugin_action_status": self.plugin_action_status,
            "permission_action": self.permission_action,
            "permission_level": self.permission_level,
            "permission_level_name": self.permission_level_name,
            "permission_level_label": self.permission_level_label,
            "allowed": self.allowed,
            "requires_confirmation": self.requires_confirmation,
            "request_state": self.request_state,
            "description": self.description,
            "reason": self.reason,
            "note": self.note,
            "metadata": self.metadata or {},
        }
