from aura.actions.action_request import ActionRequest
from aura.permissions.permission_manager import PermissionManager
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.plugin_action import PluginAction


class ActionRequestManager:
    """
    Builds safe action request proposals.

    Current phase:
    - resolve plugin action metadata when available
    - check permission policy
    - explain allowed/restricted/confirmation state
    - never execute the requested action
    """

    def __init__(self):
        self.plugin_action_registry = build_builtin_plugin_action_registry()
        self.permission_manager = PermissionManager()

    def build(self, action_name: str) -> ActionRequest:
        requested_action = action_name.strip()
        plugin_action = self.plugin_action_registry.get(requested_action)

        if plugin_action:
            return self.build_from_plugin_action(
                requested_action=requested_action,
                plugin_action=plugin_action,
            )

        return self.build_from_permission_action(requested_action=requested_action)

    def build_from_plugin_action(
        self,
        requested_action: str,
        plugin_action: PluginAction,
    ) -> ActionRequest:
        permission = self.plugin_action_registry.check_permission(plugin_action)
        state = self.determine_state(
            allowed=permission.allowed,
            requires_confirmation=permission.requires_confirmation,
            plugin_action_status=plugin_action.status,
        )

        return ActionRequest(
            requested_action=requested_action,
            resolved_action=plugin_action.name,
            plugin_action_found=True,
            plugin=plugin_action.plugin,
            skill=plugin_action.skill,
            plugin_action_status=plugin_action.status,
            permission_action=plugin_action.permission_action,
            permission_level=int(permission.level),
            permission_level_name=permission.level.name,
            permission_level_label=permission.level.label,
            allowed=permission.allowed,
            requires_confirmation=permission.requires_confirmation,
            request_state=state,
            description=plugin_action.description,
            reason=permission.reason,
            note="Action request prepared only. No action was executed.",
            metadata={
                "permission_description": permission.description,
                "plugin_action_metadata": plugin_action.metadata,
            },
        )

    def build_from_permission_action(self, requested_action: str) -> ActionRequest:
        permission = self.permission_manager.check(action=requested_action)
        state = self.determine_state(
            allowed=permission.allowed,
            requires_confirmation=permission.requires_confirmation,
            plugin_action_status="permission_only",
        )

        return ActionRequest(
            requested_action=requested_action,
            resolved_action=permission.action,
            plugin_action_found=False,
            plugin=None,
            skill=None,
            plugin_action_status="permission_only",
            permission_action=permission.action,
            permission_level=int(permission.level),
            permission_level_name=permission.level.name,
            permission_level_label=permission.level.label,
            allowed=permission.allowed,
            requires_confirmation=permission.requires_confirmation,
            request_state=state,
            description=permission.description,
            reason=permission.reason,
            note="Permission-only action request prepared. No plugin action was found and no action was executed.",
            metadata=permission.metadata or {},
        )

    def determine_state(
        self,
        *,
        allowed: bool,
        requires_confirmation: bool,
        plugin_action_status: str,
    ) -> str:
        if not allowed:
            return "restricted"

        if plugin_action_status == "planned":
            return "planned"

        if plugin_action_status == "foundation":
            if requires_confirmation:
                return "foundation_requires_confirmation"

            return "foundation_ready"

        if requires_confirmation:
            return "requires_confirmation"

        return "ready"
