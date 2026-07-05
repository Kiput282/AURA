from pathlib import Path
from typing import Any

from aura.avatar.avatar_provider import AvatarProvider
from aura.permissions.permission_manager import PermissionManager


class AvatarManager:
    """
    Avatar Foundation for AURA.

    Current phase:
    - exposes avatar foundation status
    - tracks placeholder avatar state
    - prepares expression/gesture proposals
    - does not control a real avatar runtime yet
    """

    name = "avatar_foundation"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.permission_manager = PermissionManager()
        self.providers = [
            AvatarProvider(
                name="avatar_state_placeholder",
                provider_type="state_manager",
                status="foundation",
                description="Placeholder provider for avatar state metadata.",
                state_supported=True,
            ),
            AvatarProvider(
                name="expression_placeholder",
                provider_type="expression_controller",
                status="foundation",
                description="Placeholder provider for future avatar facial expression control.",
                expression_supported=True,
            ),
            AvatarProvider(
                name="gesture_placeholder",
                provider_type="gesture_controller",
                status="foundation",
                description="Placeholder provider for future avatar gesture control.",
                gesture_supported=True,
            ),
            AvatarProvider(
                name="vrm_placeholder",
                provider_type="avatar_runtime",
                status="planned",
                description="Placeholder provider for future VRM/VRoid runtime integration.",
                runtime_supported=True,
                metadata={
                    "candidate_formats": ["VRM", "VRoid", "glTF"],
                    "candidate_engines": ["VSeeFace", "Unity", "Godot", "Blender"],
                },
            ),
        ]

    def expression_options(self) -> list[str]:
        return [
            "neutral",
            "smile",
            "happy",
            "thinking",
            "surprised",
            "concerned",
            "focused",
        ]

    def gesture_options(self) -> list[str]:
        return [
            "idle",
            "wave",
            "nod",
            "point",
            "thinking_pose",
            "present",
            "celebrate",
        ]

    def status(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "foundation",
            "foundation_ready": True,
            "runtime_ready": False,
            "avatar_loaded": False,
            "expression_runtime_ready": False,
            "gesture_runtime_ready": False,
            "motion_runtime_ready": False,
            "providers": len(self.providers),
            "expressions": len(self.expression_options()),
            "gestures": len(self.gesture_options()),
            "note": "Avatar foundation is online, but real 3D avatar runtime is not connected yet.",
        }

    def state(self) -> dict[str, Any]:
        return {
            "avatar_name": "AURA",
            "avatar_format": "planned_vrm",
            "runtime": "not_connected",
            "body_state": "standby",
            "pose": "neutral_idle",
            "expression": "neutral",
            "gesture": "idle",
            "model_loaded": False,
            "tracking_connected": False,
            "voice_link_ready": False,
            "vision_link_ready": False,
            "motion_link_ready": False,
            "supported_expressions": self.expression_options(),
            "supported_gestures": self.gesture_options(),
            "planning": {
                "preferred_format": "VRM",
                "authoring_tools": ["VRoid Studio", "Blender"],
                "runtime_candidates": ["VSeeFace", "Unity", "Godot"],
                "future_links": ["voice", "vision", "motion_capture", "streaming"],
            },
            "note": "This is a placeholder avatar state. No real avatar was loaded or controlled.",
        }

    def list_providers(self) -> list[AvatarProvider]:
        return self.providers

    def expression_request(self, expression: str) -> dict[str, Any]:
        requested = expression.strip().lower()
        supported = requested in self.expression_options()
        permission = self.permission_manager.check("prepare_file")

        return {
            "requested_expression": requested,
            "supported": supported,
            "request_state": "proposal_ready" if supported else "unknown_expression",
            "permission": permission.to_dict(),
            "runtime_ready": False,
            "executed": False,
            "note": "Expression proposal prepared only. No avatar expression was changed.",
        }

    def gesture_request(self, gesture: str) -> dict[str, Any]:
        requested = gesture.strip().lower()
        supported = requested in self.gesture_options()
        permission = self.permission_manager.check("prepare_file")

        return {
            "requested_gesture": requested,
            "supported": supported,
            "request_state": "proposal_ready" if supported else "unknown_gesture",
            "permission": permission.to_dict(),
            "runtime_ready": False,
            "executed": False,
            "note": "Gesture proposal prepared only. No avatar gesture was changed.",
        }
