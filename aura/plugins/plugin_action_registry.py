from aura.permissions.permission_manager import PermissionManager
from aura.permissions.permission_request import PermissionCheckResult
from aura.plugins.plugin_action import PluginAction


class PluginActionRegistry:
    """
    Registry for plugin actions.

    Plugin actions describe what plugins can expose to AURA.
    Current phase only registers and checks actions.
    Actual execution will come later.
    """

    def __init__(self):
        self.actions: dict[str, PluginAction] = {}

    def register(self, action: PluginAction) -> None:
        self.actions[action.name] = action

    def get(self, name: str) -> PluginAction | None:
        normalized_name = name.strip()
        return self.actions.get(normalized_name)

    def list_actions(self) -> list[PluginAction]:
        return list(self.actions.values())

    def list_by_plugin(self, plugin: str) -> list[PluginAction]:
        return [
            action
            for action in self.list_actions()
            if action.plugin == plugin
        ]

    def count(self) -> int:
        return len(self.actions)

    def check_permission(self, action: PluginAction) -> PermissionCheckResult:
        permission_manager = PermissionManager()
        return permission_manager.check(action=action.permission_action)
