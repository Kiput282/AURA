import importlib.util
import shutil
from pathlib import Path
from typing import Any

from aura.avatar.avatar_manager import AvatarManager
from aura.permissions.permission_manager import PermissionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager


class AvatarRuntimeAlphaManager:
    """
    Avatar Runtime Alpha for AURA.

    Current phase:
    - prepare avatar runtime status
    - prepare expression plans
    - prepare gesture plans
    - expose avatar runtime context
    - check local rendering/runtime dependency availability
    - never render automatically
    - never write image/animation files automatically
    - never open external apps automatically
    - never execute shell commands
    """

    name = "avatar_runtime_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.avatar_manager = AvatarManager(project_root=self.project_root)
        self.permission_manager = PermissionManager()
        self.sandbox = ToolSandboxManager(project_root=self.project_root)

    def dependency_check(self) -> dict[str, Any]:
        python_packages = [
            {
                "name": "bpy",
                "purpose": "Blender Python avatar/render scripting",
                "installed": importlib.util.find_spec("bpy") is not None,
            },
            {
                "name": "PIL",
                "purpose": "image loading and avatar preview handling through Pillow",
                "installed": importlib.util.find_spec("PIL") is not None,
            },
            {
                "name": "numpy",
                "purpose": "image/frame buffer processing",
                "installed": importlib.util.find_spec("numpy") is not None,
            },
            {
                "name": "cv2",
                "purpose": "image/video frame processing through OpenCV",
                "installed": importlib.util.find_spec("cv2") is not None,
            },
        ]

        executables = [
            {
                "name": "blender",
                "purpose": "3D avatar authoring/render/runtime candidate",
                "found": shutil.which("blender") is not None,
            },
            {
                "name": "ffmpeg",
                "purpose": "avatar animation/video conversion candidate",
                "found": shutil.which("ffmpeg") is not None,
            },
            {
                "name": "magick",
                "purpose": "image conversion candidate",
                "found": shutil.which("magick") is not None,
            },
            {
                "name": "convert",
                "purpose": "ImageMagick image conversion fallback",
                "found": shutil.which("convert") is not None,
            },
        ]

        installed_python = sum(1 for item in python_packages if item["installed"])
        found_executables = sum(1 for item in executables if item["found"])

        return {
            "status": "checked",
            "runtime_ready": False,
            "python_packages": python_packages,
            "executables": executables,
            "python_packages_installed": installed_python,
            "python_packages_total": len(python_packages),
            "executables_found": found_executables,
            "executables_total": len(executables),
            "note": "This is a passive dependency check only. No avatar runtime, render command, external app, image write, or animation write was performed.",
        }

    def detect_render_backend(self) -> dict[str, Any]:
        if importlib.util.find_spec("bpy") is not None:
            return {
                "name": "bpy",
                "type": "python_blender_runtime",
                "priority": 1,
                "found": True,
                "path": "",
                "source": "python_package",
            }

        blender_path = shutil.which("blender")
        if blender_path:
            return {
                "name": "blender",
                "type": "external_3d_runtime",
                "priority": 2,
                "found": True,
                "path": blender_path,
                "source": "executable",
            }

        return {
            "name": "",
            "type": "",
            "priority": 0,
            "found": False,
            "path": "",
            "source": "",
        }

    def detect_media_backend(self) -> dict[str, Any]:
        for name in ["ffmpeg", "magick", "convert"]:
            path = shutil.which(name)
            if path:
                return {
                    "name": name,
                    "type": "media_conversion",
                    "priority": 1,
                    "found": True,
                    "path": path,
                    "source": "executable",
                }

        return {
            "name": "",
            "type": "",
            "priority": 0,
            "found": False,
            "path": "",
            "source": "",
        }

    def build_render_command(self) -> dict[str, Any]:
        backend = self.detect_render_backend()

        if not backend["found"]:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No local avatar render backend was found. Install or configure Blender/bpy before real avatar rendering.",
            }

        if backend["name"] == "bpy":
            command = "python3 <avatar_render_with_bpy>"
        elif backend["name"] == "blender":
            command = f"{backend['path']} --background <avatar_scene.blend> --python <avatar_render_script.py>"
        else:
            command = ""

        return {
            "available": bool(command),
            "backend": backend,
            "command": command,
            "reason": "Avatar render command proposal prepared. It is not executed by AURA.",
        }

    def status(self) -> dict[str, Any]:
        dependency_check = self.dependency_check()
        avatar_status = self.avatar_manager.status()
        avatar_state = self.avatar_manager.state()
        render_backend = self.detect_render_backend()
        media_backend = self.detect_media_backend()

        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        prepare_permission = self.permission_manager.check("prepare_file")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "alpha_ready": True,
            "expression_plan_ready": True,
            "gesture_plan_ready": True,
            "avatar_context_ready": True,
            "dependency_check_ready": True,
            "foundation_ready": avatar_status["foundation_ready"],
            "runtime_ready": False,
            "avatar_loaded": False,
            "model_loaded": avatar_state["model_loaded"],
            "tracking_connected": avatar_state["tracking_connected"],
            "voice_link_ready": avatar_state["voice_link_ready"],
            "vision_link_ready": avatar_state["vision_link_ready"],
            "motion_link_ready": avatar_state["motion_link_ready"],
            "render_backend_found": render_backend["found"],
            "render_backend": render_backend["name"],
            "render_backend_path": render_backend["path"],
            "media_backend_found": media_backend["found"],
            "media_backend": media_backend["name"],
            "media_backend_path": media_backend["path"],
            "expression_runtime_ready": False,
            "gesture_runtime_ready": False,
            "motion_runtime_ready": False,
            "render_runtime_ready": render_backend["found"],
            "render_performed": False,
            "expression_changed": False,
            "gesture_changed": False,
            "external_app_opened": False,
            "command_execution": False,
            "image_file_write": False,
            "animation_file_write": False,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "python_packages_installed": dependency_check["python_packages_installed"],
            "python_packages_total": dependency_check["python_packages_total"],
            "executables_found": dependency_check["executables_found"],
            "executables_total": dependency_check["executables_total"],
            "supported_expressions": len(avatar_state["supported_expressions"]),
            "supported_gestures": len(avatar_state["supported_gestures"]),
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Avatar Runtime Alpha is online for safe avatar planning. It does not render, open external apps, write image/animation files, or execute commands automatically.",
        }

    def expression_plan(self, expression: str) -> dict[str, Any]:
        request = self.avatar_manager.expression_request(expression)
        render_plan = self.build_render_command()
        permission = self.permission_manager.check("prepare_file")

        sandbox_check = (
            self.sandbox.check_command(render_plan["command"])
            if render_plan["command"] and not render_plan["command"].startswith("python3 <")
            else None
        )

        return {
            "status": "planned",
            "requested_expression": request["requested_expression"],
            "supported": request["supported"],
            "request_state": request["request_state"],
            "render_command_available": render_plan["available"],
            "render_backend": render_plan["backend"],
            "proposed_render_command": render_plan["command"],
            "render_command_reason": render_plan["reason"],
            "sandbox_check": sandbox_check,
            "permission": permission.to_dict(),
            "runtime_ready": False,
            "avatar_loaded": False,
            "expression_changed": False,
            "gesture_changed": False,
            "render_performed": False,
            "external_app_opened": False,
            "command_execution_performed": False,
            "image_file_write_performed": False,
            "animation_file_write_performed": False,
            "safety_notes": [
                "Expression plan is proposal-only.",
                "No avatar expression was changed.",
                "No render was performed.",
                "No external app was opened.",
                "No image or animation file was written.",
                "No command was executed.",
            ],
        }

    def gesture_plan(self, gesture: str) -> dict[str, Any]:
        request = self.avatar_manager.gesture_request(gesture)
        render_plan = self.build_render_command()
        permission = self.permission_manager.check("prepare_file")

        sandbox_check = (
            self.sandbox.check_command(render_plan["command"])
            if render_plan["command"] and not render_plan["command"].startswith("python3 <")
            else None
        )

        return {
            "status": "planned",
            "requested_gesture": request["requested_gesture"],
            "supported": request["supported"],
            "request_state": request["request_state"],
            "render_command_available": render_plan["available"],
            "render_backend": render_plan["backend"],
            "proposed_render_command": render_plan["command"],
            "render_command_reason": render_plan["reason"],
            "sandbox_check": sandbox_check,
            "permission": permission.to_dict(),
            "runtime_ready": False,
            "avatar_loaded": False,
            "expression_changed": False,
            "gesture_changed": False,
            "render_performed": False,
            "external_app_opened": False,
            "command_execution_performed": False,
            "image_file_write_performed": False,
            "animation_file_write_performed": False,
            "safety_notes": [
                "Gesture plan is proposal-only.",
                "No avatar gesture was changed.",
                "No render was performed.",
                "No external app was opened.",
                "No image or animation file was written.",
                "No command was executed.",
            ],
        }

    def context(self) -> dict[str, Any]:
        status = self.status()
        avatar_state = self.avatar_manager.state()
        dependency_check = self.dependency_check()

        return {
            "status": self.status_name,
            "context_ready": True,
            "alpha_status": status,
            "avatar_state": avatar_state,
            "dependency_check": dependency_check,
            "safe_current_capabilities": [
                "avatar_runtime_alpha_status",
                "avatar_expression_plan",
                "avatar_gesture_plan",
                "avatar_runtime_context",
            ],
            "disabled_capabilities": [
                "automatic_avatar_render",
                "automatic_external_app_open",
                "real_avatar_runtime_control",
                "real_expression_change",
                "real_gesture_change",
                "image_file_write",
                "animation_file_write",
                "command_execution",
            ],
            "write_performed": False,
            "command_execution_performed": False,
            "render_performed": False,
            "external_app_opened": False,
            "expression_changed": False,
            "gesture_changed": False,
            "image_file_write_performed": False,
            "animation_file_write_performed": False,
            "note": "Avatar runtime context is read-only and preparation-only.",
        }
