import importlib.util
import shutil
from pathlib import Path
from typing import Any

from aura.permissions.permission_manager import PermissionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner


class VisionRuntimeAlphaManager:
    """
    Vision Runtime Alpha for AURA.

    Current phase:
    - prepare screen analysis plans
    - prepare camera analysis plans
    - check local dependency availability
    - map screen/camera permissions
    - never capture screen automatically
    - never access camera automatically
    - never execute shell commands
    """

    name = "vision_runtime_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.sandbox = ToolSandboxManager(project_root=self.project_root)
        self.planner = VisionRuntimePlanner(project_root=self.project_root)

    def detect_screen_backend(self) -> dict[str, Any]:
        python_candidates = [
            {
                "name": "mss",
                "type": "python_screen_capture",
                "priority": 1,
                "requires_file_write": False,
            },
            {
                "name": "pyautogui",
                "type": "python_screen_capture",
                "priority": 2,
                "requires_file_write": False,
            },
        ]

        for candidate in python_candidates:
            if importlib.util.find_spec(candidate["name"]) is not None:
                return {
                    **candidate,
                    "found": True,
                    "path": "",
                    "source": "python_package",
                }

        executable_candidates = [
            {
                "name": "grim",
                "type": "wayland_screenshot",
                "priority": 3,
                "requires_file_write": True,
            },
            {
                "name": "gnome-screenshot",
                "type": "desktop_screenshot",
                "priority": 4,
                "requires_file_write": True,
            },
            {
                "name": "scrot",
                "type": "x11_screenshot",
                "priority": 5,
                "requires_file_write": True,
            },
        ]

        for candidate in executable_candidates:
            path = shutil.which(candidate["name"])

            if path:
                return {
                    **candidate,
                    "found": True,
                    "path": path,
                    "source": "executable",
                }

        return {
            "name": "",
            "type": "",
            "priority": 0,
            "requires_file_write": False,
            "found": False,
            "path": "",
            "source": "",
        }

    def detect_camera_backend(self) -> dict[str, Any]:
        if importlib.util.find_spec("cv2") is not None:
            return {
                "name": "opencv-python",
                "type": "python_camera_capture",
                "priority": 1,
                "requires_file_write": False,
                "found": True,
                "path": "",
                "source": "python_package",
            }

        executable_candidates = [
            {
                "name": "v4l2-ctl",
                "type": "linux_camera_discovery",
                "priority": 2,
                "requires_file_write": False,
            },
            {
                "name": "ffmpeg",
                "type": "camera_capture_fallback",
                "priority": 3,
                "requires_file_write": True,
            },
            {
                "name": "libcamera-hello",
                "type": "libcamera_check",
                "priority": 4,
                "requires_file_write": False,
            },
        ]

        for candidate in executable_candidates:
            path = shutil.which(candidate["name"])

            if path:
                return {
                    **candidate,
                    "found": True,
                    "path": path,
                    "source": "executable",
                }

        return {
            "name": "",
            "type": "",
            "priority": 0,
            "requires_file_write": False,
            "found": False,
            "path": "",
            "source": "",
        }

    def status(self) -> dict[str, Any]:
        dependency_check = self.planner.check()
        activation = self.planner.vision_runtime_activation_contract()
        screenshot = self.planner.explicit_screenshot_capture_contract()
        screen_backend = self.detect_screen_backend()
        camera_backend = self.detect_camera_backend()
        screen_permission = self.permission_manager.check("screen_analyze")
        camera_permission = self.permission_manager.check("camera_analyze")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "alpha_ready": True,
            "sprint_201_vision_runtime_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "sprint_202_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "explicit_screenshot_capture_runtime_ready": screenshot["explicit_screenshot_capture_runtime_ready"],
            "explicit_screenshot_capture_status": screenshot["explicit_screenshot_capture_status"],
            "explicit_screenshot_request_required": screenshot["explicit_screenshot_request_required"],
            "explicit_screenshot_confirmation_required": screenshot["explicit_screenshot_confirmation_required"],
            "permission_required_before_screenshot": screenshot["permission_required_before_screenshot"],
            "screenshot_candidate_count": screenshot["screenshot_candidate_count"],
            "screenshot_capture_runtime_ready": screenshot["screenshot_capture_runtime_ready"],
            "screenshot_capture_active": screenshot["screenshot_capture_active"],
            "screenshot_capture_performed": screenshot["screenshot_capture_performed"],
            "screenshot_to_context_handoff_active": screenshot["screenshot_to_context_handoff_active"],
            "vision_runtime_activation_runtime_ready": activation["vision_runtime_activation_runtime_ready"],
            "vision_runtime_activation_status": activation["vision_runtime_activation_status"],
            "vision_runtime_block_start": activation["vision_runtime_block_start"],
            "vision_runtime_block_end": activation["vision_runtime_block_end"],
            "vision_runtime_next_sprint": screenshot["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": screenshot["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": screenshot["runtime_activation_allowed"],
            "vision_release_gate_open": screenshot["release_gate_open"],
            "vision_safety_blocker_count": screenshot["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": screenshot["all_safety_blockers_inactive"],
            "screen_plan_ready": True,
            "camera_plan_ready": True,
            "vision_context_ready": True,
            "dependency_check_ready": True,
            "vision_runtime_activation_contract": activation,
            "explicit_screenshot_capture_contract": screenshot,
            "screen_backend_found": screen_backend["found"],
            "screen_backend": screen_backend["name"],
            "screen_backend_path": screen_backend["path"],
            "camera_backend_found": camera_backend["found"],
            "camera_backend": camera_backend["name"],
            "camera_backend_path": camera_backend["path"],
            "screen_capture_ready": screen_backend["found"],
            "camera_capture_ready": camera_backend["found"],
            "vision_model_ready": False,
            "screen_access": False,
            "camera_access": False,
            "screenshot_capture": False,
            "camera_frame_capture": False,
            "command_execution": False,
            "image_file_write": False,
            "requires_screen_confirmation": screen_permission.requires_confirmation,
            "requires_camera_confirmation": camera_permission.requires_confirmation,
            "python_packages_installed": dependency_check["python_packages_installed"],
            "python_packages_total": dependency_check["python_packages_total"],
            "executables_found": dependency_check["executables_found"],
            "executables_total": dependency_check["executables_total"],
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Vision Runtime Alpha is online for Sprint 202 Explicit Screenshot Capture contract. It does not capture screen, access camera, read image files, run OCR, run vision models, write screenshot files, hand off context, or execute commands automatically.",
        }

    def build_screen_command(self) -> dict[str, Any]:
        backend = self.detect_screen_backend()

        if not backend["found"]:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No local screen capture backend was found. Install or configure mss, pyautogui, grim, gnome-screenshot, or scrot before real screen capture.",
            }

        if backend["source"] == "python_package":
            return {
                "available": True,
                "backend": backend,
                "command": f"python3 <screen_capture_with_{backend['name']}>",
                "reason": "Python screen capture plan prepared. It is not executed by AURA.",
            }

        command = f"{backend['path']} <output_image_path>"

        return {
            "available": True,
            "backend": backend,
            "command": command,
            "reason": "Executable screen capture proposal prepared. It is not executed by AURA and no image file was written.",
        }

    def build_camera_command(self) -> dict[str, Any]:
        backend = self.detect_camera_backend()

        if not backend["found"]:
            return {
                "available": False,
                "backend": backend,
                "command": "",
                "reason": "No local camera backend was found. Install or configure opencv-python, v4l2-ctl, ffmpeg, or libcamera before real camera access.",
            }

        if backend["source"] == "python_package":
            command = "python3 <camera_probe_with_opencv>"
        elif backend["name"] == "v4l2-ctl":
            command = f"{backend['path']} --list-devices"
        elif backend["name"] == "libcamera-hello":
            command = f"{backend['path']} --list-cameras"
        elif backend["name"] == "ffmpeg":
            command = f"{backend['path']} -f video4linux2 -list_formats all -i <camera_device>"
        else:
            command = ""

        return {
            "available": bool(command),
            "backend": backend,
            "command": command,
            "reason": "Camera planning command prepared. It is not executed by AURA.",
        }

    def screen_plan(self) -> dict[str, Any]:
        command_plan = self.build_screen_command()
        screen_permission = self.permission_manager.check("screen_analyze")

        sandbox_check = (
            self.sandbox.check_command(command_plan["command"])
            if command_plan["command"] and not command_plan["command"].startswith("python3 <")
            else None
        )

        return {
            "status": "planned",
            "command_available": command_plan["available"],
            "screen_backend": command_plan["backend"],
            "proposed_command": command_plan["command"],
            "command_reason": command_plan["reason"],
            "sandbox_check": sandbox_check,
            "screen_permission": screen_permission.to_dict(),
            "screen_access": False,
            "camera_access": False,
            "screenshot_capture_performed": False,
            "command_execution_performed": False,
            "file_write_performed": False,
            "safety_notes": [
                "Screen plan is proposal-only.",
                "No screenshot was captured.",
                "No screen content was read.",
                "No command was executed.",
                "Screen access still requires explicit confirmation.",
            ],
        }

    def camera_plan(self) -> dict[str, Any]:
        command_plan = self.build_camera_command()
        camera_permission = self.permission_manager.check("camera_analyze")

        sandbox_check = (
            self.sandbox.check_command(command_plan["command"])
            if command_plan["command"] and not command_plan["command"].startswith("python3 <")
            else None
        )

        return {
            "status": "planned",
            "command_available": command_plan["available"],
            "camera_backend": command_plan["backend"],
            "proposed_command": command_plan["command"],
            "command_reason": command_plan["reason"],
            "sandbox_check": sandbox_check,
            "camera_permission": camera_permission.to_dict(),
            "screen_access": False,
            "camera_access": False,
            "camera_frame_capture_performed": False,
            "command_execution_performed": False,
            "file_write_performed": False,
            "safety_notes": [
                "Camera plan is proposal-only.",
                "No camera device was opened.",
                "No camera frame was captured.",
                "No command was executed.",
                "Camera access still requires explicit confirmation.",
            ],
        }

    def context(self) -> dict[str, Any]:
        status = self.status()
        planner_status = self.planner.status()
        dependency_check = self.planner.check()

        return {
            "status": self.status_name,
            "context_ready": True,
            "alpha_status": status,
            "planner_status": planner_status,
            "dependency_check": dependency_check,
            "safe_current_capabilities": [
                "vision_runtime_alpha_status",
                "vision_screen_plan",
                "vision_camera_plan",
                "vision_runtime_context",
            ],
            "disabled_capabilities": [
                "automatic_screen_capture",
                "automatic_camera_access",
                "live_screen_reading",
                "live_camera_frame_capture",
                "real_vision_loop",
                "command_execution",
            ],
            "write_performed": False,
            "command_execution_performed": False,
            "screen_access_performed": False,
            "camera_access_performed": False,
            "screenshot_capture_performed": False,
            "camera_frame_capture_performed": False,
            "note": "Vision runtime context is read-only and preparation-only.",
        }
