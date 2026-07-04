from aura.permissions.permission_level import PermissionLevel
from aura.permissions.permission_request import PermissionCheckResult


class PermissionManager:
    """
    Permission System Foundation for AURA.

    This does not execute actions yet.
    It only classifies actions and explains whether they are allowed,
    require confirmation, or are restricted.
    """

    ACTION_POLICIES = {
        "think": {
            "level": PermissionLevel.THINK_ONLY,
            "allowed": True,
            "requires_confirmation": False,
            "description": "Internal thinking or text-only reasoning.",
            "reason": "Safe text-only operation.",
        },
        "suggest": {
            "level": PermissionLevel.SUGGEST,
            "allowed": True,
            "requires_confirmation": False,
            "description": "Suggest an idea, warning, next step, or recommendation.",
            "reason": "Suggestions do not change the system.",
        },
        "read_file": {
            "level": PermissionLevel.READ,
            "allowed": True,
            "requires_confirmation": False,
            "description": "Read a permitted file or project document.",
            "reason": "Reading is allowed when the user asks or grants context.",
        },
        "read_project": {
            "level": PermissionLevel.READ,
            "allowed": True,
            "requires_confirmation": False,
            "description": "Read project files, logs, or status.",
            "reason": "Project reading is useful for development assistance.",
        },
        "screen_analyze": {
            "level": PermissionLevel.READ,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Analyze the user's screen.",
            "reason": "Screen access must be intentionally enabled.",
        },
        "camera_analyze": {
            "level": PermissionLevel.READ,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Analyze camera/environment input.",
            "reason": "Camera access must be intentionally enabled.",
        },
        "microphone_listen": {
            "level": PermissionLevel.READ,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Listen through microphone for voice input.",
            "reason": "Microphone access must be intentionally enabled.",
        },
        "prepare_file": {
            "level": PermissionLevel.PREPARE,
            "allowed": True,
            "requires_confirmation": False,
            "description": "Prepare a draft file, plan, or command proposal.",
            "reason": "Preparation does not directly modify important state.",
        },
        "write_file": {
            "level": PermissionLevel.ACT_WITH_CONFIRMATION,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Write or modify a file.",
            "reason": "File changes must be confirmed.",
        },
        "open_app": {
            "level": PermissionLevel.ACT_WITH_CONFIRMATION,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Open an application.",
            "reason": "Applications should only be opened when requested.",
        },
        "open_browser": {
            "level": PermissionLevel.ACT_WITH_CONFIRMATION,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Open a browser or URL.",
            "reason": "Browser actions should only happen with user intent.",
        },
        "run_command": {
            "level": PermissionLevel.ACT_WITH_CONFIRMATION,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Run a shell command.",
            "reason": "Commands can change the system and must be confirmed.",
        },
        "send_message": {
            "level": PermissionLevel.ACT_WITH_CONFIRMATION,
            "allowed": True,
            "requires_confirmation": True,
            "description": "Send a message, email, or external communication.",
            "reason": "Outbound communication must be confirmed.",
        },
        "delete_file": {
            "level": PermissionLevel.RESTRICTED,
            "allowed": False,
            "requires_confirmation": True,
            "description": "Delete a file.",
            "reason": "Deletion is destructive and requires special approval flow.",
        },
        "install_package": {
            "level": PermissionLevel.RESTRICTED,
            "allowed": False,
            "requires_confirmation": True,
            "description": "Install packages or modify system dependencies.",
            "reason": "Installation can affect the system and must be handled carefully.",
        },
        "wipe_data": {
            "level": PermissionLevel.RESTRICTED,
            "allowed": False,
            "requires_confirmation": True,
            "description": "Wipe, reset, or destroy data.",
            "reason": "Dangerous destructive action.",
        },
    }

    def list_actions(self) -> list[str]:
        return sorted(self.ACTION_POLICIES.keys())

    def check(self, action: str) -> PermissionCheckResult:
        normalized_action = action.strip().lower().replace("-", "_")

        policy = self.ACTION_POLICIES.get(normalized_action)

        if policy is None:
            return PermissionCheckResult(
                action=normalized_action,
                level=PermissionLevel.RESTRICTED,
                allowed=False,
                requires_confirmation=True,
                description="Unknown action.",
                reason="Unknown actions are restricted by default.",
                metadata={"known_actions": self.list_actions()},
            )

        return PermissionCheckResult(
            action=normalized_action,
            level=policy["level"],
            allowed=policy["allowed"],
            requires_confirmation=policy["requires_confirmation"],
            description=policy["description"],
            reason=policy["reason"],
        )

    def list_permissions(self) -> list[PermissionCheckResult]:
        return [
            self.check(action)
            for action in self.list_actions()
        ]
