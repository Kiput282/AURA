import os
import platform
from pathlib import Path
from typing import Any

from aura.actions.action_request_manager import ActionRequestManager


class DesktopBridgeManager:
    """
    Desktop Bridge Foundation for AURA.

    Current phase:
    - detect OS and desktop environment
    - expose desktop capability metadata
    - prepare desktop action proposals
    - never execute desktop actions
    """

    name = "desktop_bridge"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.action_request_manager = ActionRequestManager()

    def detect_environment(self) -> dict[str, Any]:
        return {
            "os": platform.system() or "unknown",
            "os_release": platform.release() or "unknown",
            "os_version": platform.version() or "unknown",
            "machine": platform.machine() or "unknown",
            "desktop_environment": (
                os.environ.get("XDG_CURRENT_DESKTOP")
                or os.environ.get("DESKTOP_SESSION")
                or "unknown"
            ),
            "display": os.environ.get("DISPLAY") or "",
            "wayland_display": os.environ.get("WAYLAND_DISPLAY") or "",
            "user": os.environ.get("USER") or "unknown",
        }

    def capabilities(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "desktop.status",
                "status": "online",
                "permission_action": "think",
                "requires_confirmation": False,
                "execution_ready": False,
                "description": "Show desktop bridge foundation status.",
            },
            {
                "name": "desktop.capabilities",
                "status": "online",
                "permission_action": "think",
                "requires_confirmation": False,
                "execution_ready": False,
                "description": "List desktop bridge capabilities.",
            },
            {
                "name": "desktop.action",
                "status": "online",
                "permission_action": "think",
                "requires_confirmation": False,
                "execution_ready": False,
                "description": "Prepare a desktop action proposal without executing it.",
            },
            {
                "name": "app.open",
                "status": "foundation",
                "permission_action": "open_app",
                "requires_confirmation": True,
                "execution_ready": False,
                "description": "Placeholder for opening applications.",
            },
            {
                "name": "browser.open",
                "status": "foundation",
                "permission_action": "open_browser",
                "requires_confirmation": True,
                "execution_ready": False,
                "description": "Placeholder for opening browser or URL.",
            },
            {
                "name": "file.open",
                "status": "foundation",
                "permission_action": "open_file",
                "requires_confirmation": True,
                "execution_ready": False,
                "description": "Placeholder for opening a file with desktop apps.",
            },
        ]

    def status(self) -> dict[str, Any]:
        environment = self.detect_environment()
        capabilities = self.capabilities()

        return {
            "name": self.name,
            "version": self.version,
            "status": "foundation",
            "bridge_ready": True,
            "execution_ready": False,
            "safe_action_execution": False,
            "project_root": str(self.project_root),
            "environment": environment,
            "capabilities": capabilities,
            "capability_count": len(capabilities),
            "note": "Desktop bridge foundation is online, but real desktop action execution is not enabled yet.",
        }

    def action_request(self, action_name: str) -> dict[str, Any]:
        normalized_action = action_name.strip()
        capability_names = {
            capability["name"]
            for capability in self.capabilities()
        }

        action_request = self.action_request_manager.build(action_name=normalized_action)

        if not action_request.allowed:
            desktop_state = "restricted"
        elif action_request.requires_confirmation:
            desktop_state = "requires_confirmation"
        else:
            desktop_state = "proposal_ready"

        return {
            "requested_action": normalized_action,
            "desktop_capability_found": normalized_action in capability_names,
            "desktop_state": desktop_state,
            "execution_ready": False,
            "executed": False,
            "action_request": action_request,
            "note": "Desktop action proposal prepared only. No desktop action was executed.",
        }
