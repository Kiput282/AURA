import importlib.util
import os
import platform
import shutil
from pathlib import Path
from typing import Any

from aura.permissions.permission_manager import PermissionManager


class VisionRuntimePlanner:
    """
    Vision Runtime Planning for AURA.

    Current phase:
    - plan screen/camera capture candidates
    - plan local vision model candidates
    - check passive dependency availability
    - map permissions and confirmation requirements
    - never access screen or camera
    """

    name = "vision_runtime_planning"
    version = "0.1.0"

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.permission_manager = PermissionManager()

    def screen_capture_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "mss",
                "type": "screen_capture",
                "status": "candidate",
                "local_first": True,
                "description": "Cross-platform Python screen capture library.",
                "notes": "Good default candidate for screenshots once screen permission is enabled.",
            },
            {
                "name": "pyautogui.screenshot",
                "type": "screen_capture",
                "status": "candidate",
                "local_first": True,
                "description": "Simple Python screenshot interface.",
                "notes": "Useful fallback for basic screen capture.",
            },
            {
                "name": "grim",
                "type": "screen_capture",
                "status": "linux_wayland_candidate",
                "local_first": True,
                "description": "Wayland screenshot utility.",
                "notes": "Useful on Linux Wayland desktops.",
            },
            {
                "name": "scrot",
                "type": "screen_capture",
                "status": "linux_x11_candidate",
                "local_first": True,
                "description": "X11 screenshot utility.",
                "notes": "Useful on Linux X11 desktops.",
            },
        ]

    def camera_capture_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "opencv-python",
                "type": "camera_capture",
                "status": "candidate",
                "local_first": True,
                "description": "Camera frame capture through OpenCV.",
                "notes": "Good default candidate for local camera runtime.",
            },
            {
                "name": "v4l2-ctl",
                "type": "camera_discovery",
                "status": "linux_candidate",
                "local_first": True,
                "description": "Linux camera device discovery utility.",
                "notes": "Useful for passive camera capability listing after permission.",
            },
            {
                "name": "libcamera",
                "type": "camera_capture",
                "status": "linux_candidate",
                "local_first": True,
                "description": "Linux camera capture stack.",
                "notes": "Useful on systems using libcamera.",
            },
            {
                "name": "ffmpeg",
                "type": "camera_capture",
                "status": "fallback",
                "local_first": True,
                "description": "Can capture camera frames or convert media.",
                "notes": "Useful fallback for file/video based vision tests.",
            },
        ]

    def vision_model_candidates(self) -> list[dict[str, Any]]:
        return [
            {
                "name": "llava via ollama",
                "type": "image_understanding",
                "status": "candidate",
                "local_first": True,
                "description": "Local multimodal model candidate through Ollama.",
                "notes": "Good candidate for describing screenshots or images locally.",
            },
            {
                "name": "moondream",
                "type": "image_understanding",
                "status": "candidate",
                "local_first": True,
                "description": "Lightweight vision-language model candidate.",
                "notes": "Useful for efficient local image understanding.",
            },
            {
                "name": "clip",
                "type": "image_embedding",
                "status": "candidate",
                "local_first": True,
                "description": "Image-text embedding model candidate.",
                "notes": "Useful for image search, matching, and relevance.",
            },
        ]

    def dependency_check(self) -> dict[str, Any]:
        python_packages = [
            {
                "name": "PIL",
                "purpose": "image loading and screenshot/image handling through Pillow",
                "installed": importlib.util.find_spec("PIL") is not None,
            },
            {
                "name": "mss",
                "purpose": "candidate screen capture runtime",
                "installed": importlib.util.find_spec("mss") is not None,
            },
            {
                "name": "pyautogui",
                "purpose": "candidate screenshot fallback",
                "installed": importlib.util.find_spec("pyautogui") is not None,
            },
            {
                "name": "cv2",
                "purpose": "candidate camera capture through OpenCV",
                "installed": importlib.util.find_spec("cv2") is not None,
            },
            {
                "name": "numpy",
                "purpose": "image/frame buffer processing",
                "installed": importlib.util.find_spec("numpy") is not None,
            },
        ]

        executables = [
            {
                "name": "grim",
                "purpose": "Wayland screenshot candidate",
                "found": shutil.which("grim") is not None,
            },
            {
                "name": "scrot",
                "purpose": "X11 screenshot candidate",
                "found": shutil.which("scrot") is not None,
            },
            {
                "name": "gnome-screenshot",
                "purpose": "desktop screenshot fallback",
                "found": shutil.which("gnome-screenshot") is not None,
            },
            {
                "name": "v4l2-ctl",
                "purpose": "Linux camera device discovery",
                "found": shutil.which("v4l2-ctl") is not None,
            },
            {
                "name": "libcamera-hello",
                "purpose": "libcamera availability check",
                "found": shutil.which("libcamera-hello") is not None,
            },
            {
                "name": "ffmpeg",
                "purpose": "video/image conversion and camera fallback",
                "found": shutil.which("ffmpeg") is not None,
            },
        ]

        return {
            "python_packages": python_packages,
            "executables": executables,
            "environment": {
                "os": platform.system() or "unknown",
                "os_release": platform.release() or "unknown",
                "machine": platform.machine() or "unknown",
                "desktop_environment": (
                    os.environ.get("XDG_CURRENT_DESKTOP")
                    or os.environ.get("DESKTOP_SESSION")
                    or "unknown"
                ),
                "display": os.environ.get("DISPLAY") or "",
                "wayland_display": os.environ.get("WAYLAND_DISPLAY") or "",
                "xdg_runtime": os.environ.get("XDG_RUNTIME_DIR") or "",
            },
            "note": "This is a passive check only. No screen or camera was accessed.",
        }

    def permission_map(self) -> dict[str, Any]:
        screen = self.permission_manager.check("screen_analyze")
        camera = self.permission_manager.check("camera_analyze")

        return {
            "screen_analyze": screen.to_dict(),
            "camera_analyze": camera.to_dict(),
        }

    def status(self) -> dict[str, Any]:
        screen_candidates = self.screen_capture_candidates()
        camera_candidates = self.camera_capture_candidates()
        model_candidates = self.vision_model_candidates()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planning",
            "planning_ready": True,
            "runtime_ready": False,
            "screen_access": False,
            "camera_access": False,
            "screen_runtime_ready": False,
            "camera_runtime_ready": False,
            "vision_model_ready": False,
            "screen_candidates": len(screen_candidates),
            "camera_candidates": len(camera_candidates),
            "model_candidates": len(model_candidates),
            "candidate_count": len(screen_candidates) + len(camera_candidates) + len(model_candidates),
            "permissions": self.permission_map(),
            "note": "Vision runtime planning is online, but real screen/camera/model runtime is not enabled yet.",
        }

    def plan(self) -> dict[str, Any]:
        return {
            "recommended_path": {
                "screen_capture": "mss",
                "camera_capture": "opencv-python",
                "vision_model": "llava via ollama",
                "image_processing": "Pillow + numpy",
                "description": "Use local passive image/file tests first, then connect screen/camera only after explicit confirmation.",
            },
            "phases": [
                {
                    "phase": 1,
                    "name": "Runtime package planning",
                    "status": "ready_to_plan",
                    "description": "Choose screen/camera capture and vision model candidates.",
                },
                {
                    "phase": 2,
                    "name": "Passive dependency check",
                    "status": "ready",
                    "description": "Check installed packages and executables without accessing screen or camera.",
                },
                {
                    "phase": 3,
                    "name": "Image file dry run",
                    "status": "future",
                    "description": "Analyze a user-provided image file before live screen/camera input.",
                },
                {
                    "phase": 4,
                    "name": "Screen capture dry run",
                    "status": "future",
                    "description": "Capture screen only after explicit permission and confirmation.",
                },
                {
                    "phase": 5,
                    "name": "Camera device discovery",
                    "status": "future",
                    "description": "List camera devices only after user approval.",
                },
                {
                    "phase": 6,
                    "name": "Camera frame dry run",
                    "status": "future",
                    "description": "Capture a single camera frame only after explicit confirmation.",
                },
                {
                    "phase": 7,
                    "name": "Vision loop alpha",
                    "status": "future",
                    "description": "Connect see-think-respond loop with permission checks and runtime safety flags.",
                },
            ],
            "screen_capture_candidates": self.screen_capture_candidates(),
            "camera_capture_candidates": self.camera_capture_candidates(),
            "vision_model_candidates": self.vision_model_candidates(),
            "permissions": self.permission_map(),
            "safety_rules": [
                "Do not access screen without explicit user confirmation.",
                "Do not access camera without explicit user confirmation.",
                "Prefer user-provided image files before live screen or camera input.",
                "Keep all vision runtime actions local-first when possible.",
                "Keep runtime flags false until real screen/camera/model runtime is connected and tested.",
            ],
        }

    def check(self) -> dict[str, Any]:
        dependencies = self.dependency_check()

        installed_python = sum(
            1
            for package in dependencies["python_packages"]
            if package["installed"]
        )

        found_executables = sum(
            1
            for executable in dependencies["executables"]
            if executable["found"]
        )

        return {
            "status": "checked",
            "runtime_ready": False,
            "planning_ready": True,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "dependencies": dependencies,
            "note": "Runtime is not enabled yet. This check did not access screen or camera.",
        }
