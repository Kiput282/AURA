from pathlib import Path
from typing import Any

from aura.actions.action_request_manager import ActionRequestManager
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.permissions.permission_manager import PermissionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager


class DesktopAssistantAlphaManager:
    """
    Desktop Assistant Alpha for AURA.

    Current phase:
    - prepare desktop action plans
    - prepare open app/browser/file plans
    - expose workspace context
    - map permissions and confirmation requirements
    - run sandbox checks only
    - never open apps automatically
    - never open browser automatically
    - never open files automatically
    - never click/type automatically
    - never write files automatically
    - never execute shell commands
    """

    name = "desktop_assistant_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.desktop_bridge = DesktopBridgeManager(project_root=self.project_root)
        self.permission_manager = PermissionManager()
        self.action_request_manager = ActionRequestManager()
        self.sandbox = ToolSandboxManager(project_root=self.project_root)

    def action_type_map(self) -> dict[str, dict[str, str]]:
        return {
            "open_app": {
                "permission_action": "open_app",
                "plugin_action": "app.open",
                "description": "Prepare opening an application.",
            },
            "open_browser": {
                "permission_action": "open_browser",
                "plugin_action": "browser.open",
                "description": "Prepare opening a browser or URL.",
            },
            "open_file": {
                "permission_action": "open_file",
                "plugin_action": "file.open",
                "description": "Prepare opening a file with a desktop app.",
            },
            "run_command": {
                "permission_action": "run_command",
                "plugin_action": "run_command",
                "description": "Prepare a command proposal with sandbox checks.",
            },
        }

    def normalize_action_type(self, action_type: str) -> str:
        return action_type.strip().lower().replace("-", "_").replace(".", "_")

    def dependency_check(self) -> dict[str, Any]:
        status = self.desktop_bridge.status()
        environment = status["environment"]

        return {
            "status": "checked",
            "desktop_bridge_ready": status["bridge_ready"],
            "execution_ready": False,
            "safe_action_execution": False,
            "environment": environment,
            "capability_count": status["capability_count"],
            "sandbox_ready": self.sandbox.status()["sandbox_ready"],
            "dry_run_ready": self.sandbox.status()["dry_run_ready"],
            "real_tool_execution": False,
            "note": "Passive desktop dependency/context check only. No app, browser, file, click, keyboard input, file write, or command execution was performed.",
        }

    def build_proposed_command(self, action_type: str, target: str) -> dict[str, Any]:
        normalized = self.normalize_action_type(action_type)
        cleaned_target = target.strip()

        if not cleaned_target:
            return {
                "available": False,
                "command": "",
                "reason": "No target was provided.",
            }

        if normalized == "open_app":
            return {
                "available": True,
                "command": cleaned_target,
                "reason": "Application launch command proposal prepared. It is not executed by AURA.",
            }

        if normalized == "open_browser":
            return {
                "available": True,
                "command": f"xdg-open {cleaned_target}",
                "reason": "Browser open command proposal prepared. It is not executed by AURA.",
            }

        if normalized == "open_file":
            return {
                "available": True,
                "command": f"xdg-open {cleaned_target}",
                "reason": "File open command proposal prepared. It is not executed by AURA.",
            }

        if normalized == "run_command":
            return {
                "available": True,
                "command": cleaned_target,
                "reason": "Command proposal prepared for sandbox checking only. It is not executed by AURA.",
            }

        return {
            "available": False,
            "command": "",
            "reason": f"Unknown desktop action type: {action_type}",
        }

    def status(self) -> dict[str, Any]:
        dependency = self.dependency_check()
        bridge_status = self.desktop_bridge.status()

        open_app_permission = self.permission_manager.check("open_app")
        open_browser_permission = self.permission_manager.check("open_browser")
        open_file_permission = self.permission_manager.check("open_file")
        run_command_permission = self.permission_manager.check("run_command")
        write_file_permission = self.permission_manager.check("write_file")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "alpha_ready": True,
            "action_plan_ready": True,
            "open_app_plan_ready": True,
            "open_browser_plan_ready": True,
            "open_file_plan_ready": True,
            "workspace_context_ready": True,
            "dependency_check_ready": True,
            "bridge_ready": bridge_status["bridge_ready"],
            "execution_ready": False,
            "safe_action_execution": False,
            "app_opened": False,
            "browser_opened": False,
            "file_opened": False,
            "click_performed": False,
            "keyboard_input_performed": False,
            "mouse_control": False,
            "command_execution": False,
            "file_write": False,
            "external_app_opened": False,
            "requires_open_app_confirmation": open_app_permission.requires_confirmation,
            "requires_open_browser_confirmation": open_browser_permission.requires_confirmation,
            "requires_open_file_confirmation": open_file_permission.requires_confirmation,
            "requires_run_command_confirmation": run_command_permission.requires_confirmation,
            "requires_write_file_confirmation": write_file_permission.requires_confirmation,
            "environment": dependency["environment"],
            "capability_count": bridge_status["capability_count"],
            "supported_action_types": list(self.action_type_map().keys()),
            "supported_action_type_count": len(self.action_type_map()),
            "sandbox_ready": dependency["sandbox_ready"],
            "sandbox_dry_run_ready": dependency["dry_run_ready"],
            "real_tool_execution": False,
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Desktop Assistant Alpha is online for safe desktop planning. It does not open apps, open browser, open files, click, type, write files, or execute commands automatically.",
        }

    def action_plan(self, action_type: str, target: str = "") -> dict[str, Any]:
        normalized = self.normalize_action_type(action_type)
        action_map = self.action_type_map()
        action_info = action_map.get(normalized)

        if action_info:
            permission_action = action_info["permission_action"]
            plugin_action = action_info["plugin_action"]
            action_description = action_info["description"]
        else:
            permission_action = normalized
            plugin_action = normalized
            action_description = "Unknown desktop action type."

        permission = self.permission_manager.check(permission_action)
        action_request = self.action_request_manager.build(plugin_action)
        command_plan = self.build_proposed_command(normalized, target)

        sandbox_check = (
            self.sandbox.check_command(command_plan["command"])
            if command_plan["command"]
            else None
        )

        if not action_info:
            plan_state = "unknown_action_type"
        elif not permission.allowed:
            plan_state = "restricted"
        elif permission.requires_confirmation:
            plan_state = "requires_confirmation_before_execution"
        else:
            plan_state = "proposal_ready"

        return {
            "status": "planned",
            "action_type": normalized,
            "target": target.strip(),
            "plan_state": plan_state,
            "supported": action_info is not None,
            "description": action_description,
            "plugin_action": plugin_action,
            "permission": permission.to_dict(),
            "action_request": action_request.to_dict(),
            "command_available": command_plan["available"],
            "proposed_command": command_plan["command"],
            "command_reason": command_plan["reason"],
            "sandbox_check": sandbox_check,
            "execution_ready": False,
            "executed": False,
            "app_opened": False,
            "browser_opened": False,
            "file_opened": False,
            "click_performed": False,
            "keyboard_input_performed": False,
            "mouse_control_performed": False,
            "external_app_opened": False,
            "command_execution_performed": False,
            "file_write_performed": False,
            "safety_notes": [
                "Desktop action plan is proposal-only.",
                "No application was opened.",
                "No browser was opened.",
                "No file was opened.",
                "No click or keyboard input was performed.",
                "No file was written.",
                "No command was executed.",
                "Real desktop actions still require explicit confirmation.",
            ],
        }

    def open_app_plan(self, app_name: str) -> dict[str, Any]:
        return self.action_plan("open_app", app_name)

    def open_browser_plan(self, url: str) -> dict[str, Any]:
        return self.action_plan("open_browser", url)

    def open_file_plan(self, file_path: str) -> dict[str, Any]:
        return self.action_plan("open_file", file_path)

    def workspace_context(self) -> dict[str, Any]:
        status = self.status()
        bridge_status = self.desktop_bridge.status()
        dependency_check = self.dependency_check()

        return {
            "status": self.status_name,
            "context_ready": True,
            "alpha_status": status,
            "desktop_bridge_status": bridge_status,
            "dependency_check": dependency_check,
            "environment": status["environment"],
            "safe_current_capabilities": [
                "desktop_alpha_status",
                "desktop_action_plan",
                "desktop_open_app_plan",
                "desktop_open_browser_plan",
                "desktop_open_file_plan",
                "desktop_workspace_context",
            ],
            "disabled_capabilities": [
                "automatic_app_open",
                "automatic_browser_open",
                "automatic_file_open",
                "automatic_mouse_click",
                "automatic_keyboard_input",
                "desktop_file_write",
                "command_execution",
            ],
            "write_performed": False,
            "command_execution_performed": False,
            "app_opened": False,
            "browser_opened": False,
            "file_opened": False,
            "click_performed": False,
            "keyboard_input_performed": False,
            "mouse_control_performed": False,
            "note": "Desktop workspace context is read-only and preparation-only.",
        }
