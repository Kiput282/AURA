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

    def vision_runtime_activation_contract(self) -> dict[str, Any]:
        screen_candidates = self.screen_capture_candidates()
        camera_candidates = self.camera_capture_candidates()
        model_candidates = self.vision_model_candidates()
        screen_permission = self.permission_manager.check("screen_analyze")
        camera_permission = self.permission_manager.check("camera_analyze")

        safety_blockers = [
            "screen_access",
            "camera_access",
            "screen_capture_active",
            "screenshot_capture_active",
            "camera_frame_capture_active",
            "image_capture_active",
            "video_capture_active",
            "webcam_runtime_active",
            "vision_runtime_active",
            "visual_context_runtime_active",
            "image_analysis_runtime_active",
            "object_detection_runtime_active",
            "ocr_runtime_active",
            "image_text_extraction_runtime_active",
            "continuous_watch_active",
            "background_watch_active",
            "silent_capture_enabled",
            "camera_activation_by_default_enabled",
            "biometric_identification_enabled",
            "face_recognition_enabled",
            "identity_recognition_enabled",
            "emotion_inference_from_face_enabled",
            "visual_context_to_action_bypass_enabled",
            "visual_action_execution_active",
            "visual_tool_execution_active",
            "command_execution_active",
            "file_mutation_active",
            "desktop_action_active",
            "network_action_active",
            "git_action_active",
            "memory_write_active",
            "cloud_vision_fallback_enabled",
            "external_upload_enabled",
        ]

        contract = {
            "sprint": 201,
            "name": "vision_runtime_activation_foundation",
            "vision_runtime_activation_contract_ready": True,
            "vision_runtime_activation_runtime_ready": False,
            "vision_runtime_activation_status": "activation_foundation_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 201,
            "vision_runtime_next_sprint": 202,
            "vision_runtime_next_boundary": "explicit_visual_input_state",
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "safe_idle_default": True,
            "local_first_required": True,
            "offline_first_preferred": True,
            "explicit_visual_input_required": True,
            "explicit_user_confirmation_required": True,
            "permission_required_before_screen": True,
            "permission_required_before_camera": True,
            "permission_required_before_image_analysis": True,
            "permission_required_before_visual_action": True,
            "user_provided_image_first": True,
            "screen_permission_action": "screen_analyze",
            "camera_permission_action": "camera_analyze",
            "screen_permission_allowed": screen_permission.allowed,
            "camera_permission_allowed": camera_permission.allowed,
            "screen_permission_requires_confirmation": screen_permission.requires_confirmation,
            "camera_permission_requires_confirmation": camera_permission.requires_confirmation,
            "screen_capture_candidate_count": len(screen_candidates),
            "camera_capture_candidate_count": len(camera_candidates),
            "vision_model_candidate_count": len(model_candidates),
            "screen_capture_candidates_ready": len(screen_candidates) > 0,
            "camera_capture_candidates_ready": len(camera_candidates) > 0,
            "vision_model_candidates_ready": len(model_candidates) > 0,
            "screen_access": False,
            "camera_access": False,
            "screen_capture_active": False,
            "screenshot_capture_active": False,
            "camera_frame_capture_active": False,
            "image_capture_active": False,
            "video_capture_active": False,
            "webcam_runtime_active": False,
            "vision_runtime_active": False,
            "visual_context_runtime_active": False,
            "image_analysis_runtime_active": False,
            "object_detection_runtime_active": False,
            "ocr_runtime_active": False,
            "image_text_extraction_runtime_active": False,
            "continuous_watch_active": False,
            "background_watch_active": False,
            "silent_capture_enabled": False,
            "camera_activation_by_default_enabled": False,
            "biometric_identification_enabled": False,
            "face_recognition_enabled": False,
            "identity_recognition_enabled": False,
            "emotion_inference_from_face_enabled": False,
            "visual_context_to_action_bypass_enabled": False,
            "visual_action_execution_active": False,
            "visual_tool_execution_active": False,
            "command_execution_active": False,
            "file_mutation_active": False,
            "desktop_action_active": False,
            "network_action_active": False,
            "git_action_active": False,
            "memory_write_active": False,
            "cloud_vision_fallback_enabled": False,
            "external_upload_enabled": False,
            "dependency_install_performed": False,
            "model_download_performed": False,
            "screen_capture_performed": False,
            "camera_frame_capture_performed": False,
            "image_file_read_performed": False,
            "ocr_performed": False,
            "visual_recognition_performed": False,
            "visual_action_performed": False,
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": True,
            "runtime_scope": "vision_runtime_activation_foundation_contract_only",
        }

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in safety_blockers
        )

        return contract

    def explicit_screenshot_capture_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        dependencies = self.dependency_check()
        screen_permission = self.permission_manager.check("screen_analyze")
        screenshot_candidates = self.screen_capture_candidates()
        safety_blockers = list(activation["safety_blockers"])

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 202,
            "name": "explicit_screenshot_capture",
            "explicit_screenshot_capture_contract_ready": True,
            "explicit_screenshot_capture_runtime_ready": False,
            "explicit_screenshot_capture_status": "explicit_screenshot_capture_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 202,
            "vision_runtime_next_sprint": 203,
            "vision_runtime_next_boundary": "screen_context_adapter",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_activation_status": activation["vision_runtime_activation_status"],
            "previous_activation_runtime_ready": activation["vision_runtime_activation_runtime_ready"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "explicit_screenshot_request_required": True,
            "explicit_screenshot_confirmation_required": True,
            "explicit_screenshot_permission_required": True,
            "permission_required_before_screenshot": True,
            "permission_required_before_screen": True,
            "permission_required_before_image_file_write": True,
            "permission_required_before_context_handoff": True,
            "redaction_required_before_context_handoff": True,
            "single_capture_only": True,
            "continuous_capture_allowed": False,
            "background_capture_allowed": False,
            "silent_capture_allowed": False,
            "automatic_capture_allowed": False,
            "scheduled_capture_allowed": False,
            "screen_permission_action": "screen_analyze",
            "screen_permission_allowed": screen_permission.allowed,
            "screen_permission_requires_confirmation": screen_permission.requires_confirmation,
            "screenshot_candidate_count": len(screenshot_candidates),
            "screenshot_candidates_ready": len(screenshot_candidates) > 0,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "screen_capture_runtime_ready": False,
            "screenshot_capture_runtime_ready": False,
            "screenshot_request_active": False,
            "screenshot_permission_request_active": False,
            "screenshot_confirmation_active": False,
            "screenshot_capture_allowed": False,
            "screenshot_capture_active": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_write_active": False,
            "screenshot_file_read_active": False,
            "screenshot_storage_persistence_enabled": False,
            "screenshot_metadata_persistence_enabled": False,
            "screenshot_to_context_handoff_active": False,
            "screen_context_adapter_active": False,
            "redaction_runtime_active": False,
            "vision_model_runtime_active": False,
            "ocr_runtime_active": False,
            "image_analysis_runtime_active": False,
            "object_detection_runtime_active": False,
            "visual_action_execution_active": False,
            "visual_tool_execution_active": False,
            "command_execution_active": False,
            "file_mutation_active": False,
            "desktop_action_active": False,
            "network_action_active": False,
            "git_action_active": False,
            "memory_write_active": False,
            "cloud_vision_fallback_enabled": False,
            "external_upload_enabled": False,
            "dependency_install_performed": False,
            "model_download_performed": False,
            "runtime_scope": "explicit_screenshot_capture_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": activation["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = activation[blocker]

        contract["screenshot_capture_active"] = False
        contract["screenshot_capture_performed"] = False
        contract["ocr_runtime_active"] = False
        contract["image_analysis_runtime_active"] = False
        contract["object_detection_runtime_active"] = False
        contract["visual_action_execution_active"] = False
        contract["command_execution_active"] = False
        contract["file_mutation_active"] = False
        contract["desktop_action_active"] = False
        contract["network_action_active"] = False
        contract["git_action_active"] = False
        contract["memory_write_active"] = False
        contract["cloud_vision_fallback_enabled"] = False
        contract["external_upload_enabled"] = False

        contract["all_safety_blockers_inactive"] = all(
            contract[blocker] is False for blocker in safety_blockers
        )

        return contract

    def status(self) -> dict[str, Any]:
        screen_candidates = self.screen_capture_candidates()
        camera_candidates = self.camera_capture_candidates()
        model_candidates = self.vision_model_candidates()
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()

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
            "vision_model_candidates": len(model_candidates),
            "candidate_count": len(screen_candidates) + len(camera_candidates) + len(model_candidates),
            "permissions": self.permission_map(),
            "vision_runtime_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "vision_runtime_activation_runtime_ready": activation["vision_runtime_activation_runtime_ready"],
            "vision_runtime_activation_status": activation["vision_runtime_activation_status"],
            "explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "explicit_screenshot_capture_runtime_ready": screenshot["explicit_screenshot_capture_runtime_ready"],
            "explicit_screenshot_capture_status": screenshot["explicit_screenshot_capture_status"],
            "vision_runtime_block_start": screenshot["vision_runtime_block_start"],
            "vision_runtime_block_end": screenshot["vision_runtime_block_end"],
            "vision_runtime_current_sprint": screenshot["vision_runtime_current_sprint"],
            "vision_runtime_next_sprint": screenshot["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": screenshot["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": screenshot["runtime_activation_allowed"],
            "vision_release_gate_open": screenshot["release_gate_open"],
            "vision_safe_idle_default": activation["safe_idle_default"],
            "vision_explicit_visual_input_required": activation["explicit_visual_input_required"],
            "vision_explicit_user_confirmation_required": activation["explicit_user_confirmation_required"],
            "vision_permission_required_before_screen": screenshot["permission_required_before_screen"],
            "vision_permission_required_before_camera": activation["permission_required_before_camera"],
            "vision_permission_required_before_image_analysis": activation["permission_required_before_image_analysis"],
            "vision_permission_required_before_visual_action": activation["permission_required_before_visual_action"],
            "vision_user_provided_image_first": activation["user_provided_image_first"],
            "vision_screen_permission_action": screenshot["screen_permission_action"],
            "vision_camera_permission_action": activation["camera_permission_action"],
            "explicit_screenshot_request_required": screenshot["explicit_screenshot_request_required"],
            "explicit_screenshot_confirmation_required": screenshot["explicit_screenshot_confirmation_required"],
            "permission_required_before_screenshot": screenshot["permission_required_before_screenshot"],
            "single_capture_only": screenshot["single_capture_only"],
            "continuous_capture_allowed": screenshot["continuous_capture_allowed"],
            "background_capture_allowed": screenshot["background_capture_allowed"],
            "silent_capture_allowed": screenshot["silent_capture_allowed"],
            "automatic_capture_allowed": screenshot["automatic_capture_allowed"],
            "screenshot_candidate_count": screenshot["screenshot_candidate_count"],
            "screenshot_capture_runtime_ready": screenshot["screenshot_capture_runtime_ready"],
            "screenshot_capture_active": screenshot["screenshot_capture_active"],
            "screenshot_capture_performed": screenshot["screenshot_capture_performed"],
            "screenshot_output_file_created": screenshot["screenshot_output_file_created"],
            "screenshot_to_context_handoff_active": screenshot["screenshot_to_context_handoff_active"],
            "vision_safety_blocker_count": screenshot["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": screenshot["all_safety_blockers_inactive"],
            "vision_runtime_activation_contract": activation,
            "explicit_screenshot_capture_contract": screenshot,
            "note": "Explicit screenshot capture contract is ready for Sprint 202; screenshot capture remains request-only and disabled by default, with no silent capture, background capture, continuous watching, OCR, vision model runtime, context handoff, visual action, file/desktop/network/git action, cloud fallback, or external upload enabled.",
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
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        assertions = {
            "vision_runtime_activation_contract_ready": activation["vision_runtime_activation_contract_ready"] is True,
            "vision_runtime_activation_runtime_not_ready": activation["vision_runtime_activation_runtime_ready"] is False,
            "vision_runtime_activation_status_ready": activation["vision_runtime_activation_status"] == "activation_foundation_ready",
            "explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"] is True,
            "explicit_screenshot_capture_runtime_not_ready": screenshot["explicit_screenshot_capture_runtime_ready"] is False,
            "explicit_screenshot_capture_status_ready": screenshot["explicit_screenshot_capture_status"] == "explicit_screenshot_capture_contract_ready",
            "vision_runtime_block_start_201": screenshot["vision_runtime_block_start"] == 201,
            "vision_runtime_block_end_210": screenshot["vision_runtime_block_end"] == 210,
            "vision_runtime_current_sprint_202": screenshot["vision_runtime_current_sprint"] == 202,
            "vision_runtime_next_sprint_203": screenshot["vision_runtime_next_sprint"] == 203,
            "vision_runtime_next_boundary_screen_context_adapter": screenshot["vision_runtime_next_boundary"] == "screen_context_adapter",
            "previous_activation_contract_ready": screenshot["previous_activation_contract_ready"] is True,
            "previous_activation_runtime_not_ready": screenshot["previous_activation_runtime_ready"] is False,
            "vision_runtime_not_ready": screenshot["runtime_ready"] is False,
            "vision_runtime_activation_not_allowed": screenshot["runtime_activation_allowed"] is False,
            "vision_release_gate_closed": screenshot["release_gate_open"] is False,
            "explicit_screenshot_request_required": screenshot["explicit_screenshot_request_required"] is True,
            "explicit_screenshot_confirmation_required": screenshot["explicit_screenshot_confirmation_required"] is True,
            "explicit_screenshot_permission_required": screenshot["explicit_screenshot_permission_required"] is True,
            "permission_required_before_screenshot": screenshot["permission_required_before_screenshot"] is True,
            "permission_required_before_screen": screenshot["permission_required_before_screen"] is True,
            "permission_required_before_image_file_write": screenshot["permission_required_before_image_file_write"] is True,
            "permission_required_before_context_handoff": screenshot["permission_required_before_context_handoff"] is True,
            "redaction_required_before_context_handoff": screenshot["redaction_required_before_context_handoff"] is True,
            "single_capture_only": screenshot["single_capture_only"] is True,
            "continuous_capture_not_allowed": screenshot["continuous_capture_allowed"] is False,
            "background_capture_not_allowed": screenshot["background_capture_allowed"] is False,
            "silent_capture_not_allowed": screenshot["silent_capture_allowed"] is False,
            "automatic_capture_not_allowed": screenshot["automatic_capture_allowed"] is False,
            "scheduled_capture_not_allowed": screenshot["scheduled_capture_allowed"] is False,
            "screen_permission_action": screenshot["screen_permission_action"] == "screen_analyze",
            "screenshot_candidates_ready": screenshot["screenshot_candidates_ready"] is True,
            "screen_capture_runtime_not_ready": screenshot["screen_capture_runtime_ready"] is False,
            "screenshot_capture_runtime_not_ready": screenshot["screenshot_capture_runtime_ready"] is False,
            "screenshot_request_inactive": screenshot["screenshot_request_active"] is False,
            "screenshot_permission_request_inactive": screenshot["screenshot_permission_request_active"] is False,
            "screenshot_confirmation_inactive": screenshot["screenshot_confirmation_active"] is False,
            "screenshot_capture_not_allowed": screenshot["screenshot_capture_allowed"] is False,
            "screenshot_capture_inactive": screenshot["screenshot_capture_active"] is False,
            "screenshot_capture_not_performed": screenshot["screenshot_capture_performed"] is False,
            "screenshot_output_file_not_created": screenshot["screenshot_output_file_created"] is False,
            "screenshot_file_write_inactive": screenshot["screenshot_file_write_active"] is False,
            "screenshot_file_read_inactive": screenshot["screenshot_file_read_active"] is False,
            "screenshot_storage_persistence_disabled": screenshot["screenshot_storage_persistence_enabled"] is False,
            "screenshot_metadata_persistence_disabled": screenshot["screenshot_metadata_persistence_enabled"] is False,
            "screenshot_to_context_handoff_inactive": screenshot["screenshot_to_context_handoff_active"] is False,
            "screen_context_adapter_inactive": screenshot["screen_context_adapter_active"] is False,
            "redaction_runtime_inactive": screenshot["redaction_runtime_active"] is False,
            "vision_model_runtime_inactive": screenshot["vision_model_runtime_active"] is False,
            "ocr_runtime_inactive": screenshot["ocr_runtime_active"] is False,
            "image_analysis_runtime_inactive": screenshot["image_analysis_runtime_active"] is False,
            "object_detection_runtime_inactive": screenshot["object_detection_runtime_active"] is False,
            "visual_action_execution_inactive": screenshot["visual_action_execution_active"] is False,
            "visual_tool_execution_inactive": screenshot["visual_tool_execution_active"] is False,
            "command_execution_inactive": screenshot["command_execution_active"] is False,
            "file_mutation_inactive": screenshot["file_mutation_active"] is False,
            "desktop_action_inactive": screenshot["desktop_action_active"] is False,
            "network_action_inactive": screenshot["network_action_active"] is False,
            "git_action_inactive": screenshot["git_action_active"] is False,
            "memory_write_inactive": screenshot["memory_write_active"] is False,
            "cloud_vision_fallback_disabled": screenshot["cloud_vision_fallback_enabled"] is False,
            "external_upload_disabled": screenshot["external_upload_enabled"] is False,
            "dependency_install_not_performed": screenshot["dependency_install_performed"] is False,
            "model_download_not_performed": screenshot["model_download_performed"] is False,
            "vision_safety_blocker_count": screenshot["safety_blocker_count"] == 33,
            "vision_all_safety_blockers_inactive": screenshot["all_safety_blockers_inactive"] is True,
        }

        for blocker in screenshot["safety_blockers"]:
            assertions[f"safety_blocker_{blocker}_inactive"] = screenshot[blocker] is False

        failed_assertions = [
            name for name, passed in assertions.items() if not passed
        ]

        return {
            "status": "checked",
            "runtime_ready": False,
            "planning_ready": True,
            "vision_runtime_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "vision_runtime_activation_runtime_ready": activation["vision_runtime_activation_runtime_ready"],
            "vision_runtime_activation_status": activation["vision_runtime_activation_status"],
            "explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "explicit_screenshot_capture_runtime_ready": screenshot["explicit_screenshot_capture_runtime_ready"],
            "explicit_screenshot_capture_status": screenshot["explicit_screenshot_capture_status"],
            "vision_runtime_block_start": screenshot["vision_runtime_block_start"],
            "vision_runtime_block_end": screenshot["vision_runtime_block_end"],
            "vision_runtime_current_sprint": screenshot["vision_runtime_current_sprint"],
            "vision_runtime_next_sprint": screenshot["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": screenshot["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": screenshot["runtime_activation_allowed"],
            "vision_release_gate_open": screenshot["release_gate_open"],
            "vision_safety_blocker_count": screenshot["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": screenshot["all_safety_blockers_inactive"],
            "assertions": assertions,
            "assertion_count": len(assertions),
            "failed_assertions": failed_assertions,
            "failed_assertion_count": len(failed_assertions),
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "dependencies": dependencies,
            "vision_runtime_activation_contract": activation,
            "explicit_screenshot_capture_contract": screenshot,
            "note": "Runtime is not enabled yet. This check prepared the Sprint 202 explicit screenshot capture contract without capturing the screen, accessing camera, writing screenshot files, reading image files, running OCR, running vision models, handing off screen context, executing tools/commands, writing memory, controlling desktop, using network/git, using cloud vision, uploading externally, or executing visual actions.",
        }
