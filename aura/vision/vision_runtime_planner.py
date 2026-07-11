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

    def screen_context_adapter_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()
        dependencies = self.dependency_check()
        safety_blockers = list(screenshot["safety_blockers"])

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 203,
            "name": "screen_context_adapter",
            "screen_context_adapter_contract_ready": True,
            "screen_context_adapter_runtime_ready": False,
            "screen_context_adapter_status": "screen_context_adapter_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 203,
            "vision_runtime_next_sprint": 204,
            "vision_runtime_next_boundary": "local_vision_model_adapter",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "previous_explicit_screenshot_capture_status": screenshot["explicit_screenshot_capture_status"],
            "previous_explicit_screenshot_capture_runtime_ready": screenshot["explicit_screenshot_capture_runtime_ready"],
            "previous_screenshot_capture_performed": screenshot["screenshot_capture_performed"],
            "previous_screenshot_to_context_handoff_active": screenshot["screenshot_to_context_handoff_active"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "screen_context_adapter_contract_only": True,
            "provided_screenshot_context_required": True,
            "provided_screen_metadata_required": True,
            "provided_user_prompt_required": True,
            "provided_redaction_notes_required": True,
            "placeholder_context_only": True,
            "contract_input_only": True,
            "image_file_read_allowed": False,
            "screenshot_capture_required_now": False,
            "screenshot_file_read_required_now": False,
            "screen_context_input_schema_ready": True,
            "screen_context_metadata_schema_ready": True,
            "screen_context_packet_schema_ready": True,
            "screen_context_summary_contract_ready": True,
            "screen_context_source_metadata_required": True,
            "screen_context_uncertainty_required": True,
            "screen_context_no_visual_claims_without_model": True,
            "screen_context_no_ocr_claims_without_ocr": True,
            "screen_context_no_identity_claims": True,
            "screen_context_no_action_bypass": True,
            "permission_required_before_screen_context_adapter": True,
            "permission_required_before_context_handoff": True,
            "permission_required_before_chat_handoff": True,
            "redaction_required_before_context_adapter": True,
            "redaction_required_before_context_packet": True,
            "redaction_required_before_chat_handoff": True,
            "sensitive_region_redaction_required": True,
            "window_title_redaction_required": True,
            "url_redaction_required": True,
            "clipboard_exclusion_required": True,
            "screen_context_runtime_ready": False,
            "screen_context_adapter_active": False,
            "screen_context_input_received": False,
            "screen_context_metadata_received": False,
            "screen_context_packet_created": False,
            "screen_context_summary_created": False,
            "screen_context_handoff_active": False,
            "screen_context_to_chat_handoff_active": False,
            "screenshot_to_context_handoff_active": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_write_active": False,
            "screenshot_file_read_active": False,
            "screenshot_storage_persistence_enabled": False,
            "screenshot_metadata_persistence_enabled": False,
            "redaction_runtime_active": False,
            "redacted_context_created": False,
            "context_persistence_enabled": False,
            "metadata_persistence_enabled": False,
            "screen_context_memory_write_enabled": False,
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
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "runtime_scope": "screen_context_adapter_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": screenshot["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = screenshot[blocker]

        contract["screen_context_adapter_active"] = False
        contract["screenshot_to_context_handoff_active"] = False
        contract["redaction_runtime_active"] = False
        contract["vision_model_runtime_active"] = False
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

    def local_vision_model_adapter_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()
        screen_context = self.screen_context_adapter_contract()
        dependencies = self.dependency_check()
        model_candidates = self.vision_model_candidates()
        model_candidate_names = [candidate["name"] for candidate in model_candidates]
        safety_blockers = list(screen_context["safety_blockers"])

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 204,
            "name": "local_vision_model_adapter",
            "local_vision_model_adapter_contract_ready": True,
            "local_vision_model_adapter_runtime_ready": False,
            "local_vision_model_adapter_status": "local_vision_model_adapter_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 204,
            "vision_runtime_next_sprint": 205,
            "vision_runtime_next_boundary": "vision_permission_and_redaction",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "previous_screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "previous_screen_context_adapter_runtime_ready": screen_context["screen_context_adapter_runtime_ready"],
            "previous_screen_context_packet_created": screen_context["screen_context_packet_created"],
            "previous_screen_context_handoff_active": screen_context["screen_context_handoff_active"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "local_vision_model_adapter_contract_only": True,
            "local_first_required": True,
            "offline_first_required": True,
            "local_provider_required": True,
            "local_provider_contract_ready": True,
            "supported_local_providers": ["ollama", "openai_compatible_loopback"],
            "supported_local_provider_count": 2,
            "local_vision_model_candidates": model_candidates,
            "local_vision_model_candidate_names": model_candidate_names,
            "local_vision_model_candidate_count": len(model_candidates),
            "local_vision_model_candidates_ready": len(model_candidates) > 0,
            "local_vision_model_default_candidate": model_candidate_names[0] if model_candidate_names else "none",
            "adapter_selection_schema_ready": True,
            "model_request_schema_ready": True,
            "model_response_schema_ready": True,
            "model_capability_schema_ready": True,
            "visual_prompt_contract_ready": True,
            "provided_screen_context_required": True,
            "provided_screen_metadata_required": True,
            "provided_user_prompt_required": True,
            "redacted_context_required": True,
            "source_metadata_required": True,
            "uncertainty_required": True,
            "permission_required_before_model_adapter": True,
            "permission_required_before_model_probe": True,
            "permission_required_before_model_request": True,
            "permission_required_before_model_execution": True,
            "redaction_required_before_model_request": True,
            "redaction_required_before_model_response": True,
            "no_raw_screenshot_to_model": True,
            "no_unredacted_context_to_model": True,
            "image_file_read_allowed": False,
            "screenshot_capture_required_now": False,
            "screenshot_file_read_required_now": False,
            "ocr_required_now": False,
            "cloud_vision_fallback_allowed": False,
            "external_upload_allowed": False,
            "model_download_required_now": False,
            "model_download_performed": False,
            "dependency_install_performed": False,
            "local_vision_model_adapter_active": False,
            "local_model_provider_probe_active": False,
            "local_model_request_active": False,
            "local_model_inference_active": False,
            "local_model_response_created": False,
            "local_model_response_persistence_enabled": False,
            "visual_description_created": False,
            "visual_classification_created": False,
            "visual_reasoning_created": False,
            "screen_context_to_model_handoff_active": False,
            "model_to_chat_handoff_active": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_write_active": False,
            "screenshot_file_read_active": False,
            "screen_context_packet_created": False,
            "screen_context_handoff_active": False,
            "redaction_runtime_active": False,
            "redacted_context_created": False,
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
            "visual_context_to_action_bypass_enabled": False,
            "no_tool_use_from_model": True,
            "no_autonomous_action": True,
            "no_identity_claims": True,
            "no_biometric_identification": True,
            "no_emotion_inference_from_face": True,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "runtime_scope": "local_vision_model_adapter_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": screen_context["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = screen_context[blocker]

        contract["vision_model_runtime_active"] = False
        contract["ocr_runtime_active"] = False
        contract["image_analysis_runtime_active"] = False
        contract["object_detection_runtime_active"] = False
        contract["visual_context_to_action_bypass_enabled"] = False
        contract["visual_action_execution_active"] = False
        contract["visual_tool_execution_active"] = False
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

    def vision_permission_and_redaction_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()
        screen_context = self.screen_context_adapter_contract()
        local_model = self.local_vision_model_adapter_contract()
        dependencies = self.dependency_check()
        safety_blockers = list(local_model["safety_blockers"])

        screen_permission = self.permission_manager.check("screen_analyze")
        camera_permission = self.permission_manager.check("camera_analyze")

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 205,
            "name": "vision_permission_and_redaction",
            "vision_permission_redaction_contract_ready": True,
            "vision_permission_redaction_runtime_ready": False,
            "vision_permission_redaction_status": "vision_permission_and_redaction_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 205,
            "vision_runtime_next_sprint": 206,
            "vision_runtime_next_boundary": "workspace_visual_understanding",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "previous_screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "previous_local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "previous_local_vision_model_adapter_runtime_ready": local_model["local_vision_model_adapter_runtime_ready"],
            "previous_local_model_request_active": local_model["local_model_request_active"],
            "previous_local_model_inference_active": local_model["local_model_inference_active"],
            "previous_model_to_chat_handoff_active": local_model["model_to_chat_handoff_active"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "vision_permission_redaction_contract_only": True,
            "permission_actions": ["screen_analyze", "camera_analyze"],
            "screen_permission_action": "screen_analyze",
            "camera_permission_action": "camera_analyze",
            "screen_permission_allowed": screen_permission.allowed,
            "camera_permission_allowed": camera_permission.allowed,
            "screen_permission_requires_confirmation": screen_permission.requires_confirmation,
            "camera_permission_requires_confirmation": camera_permission.requires_confirmation,
            "explicit_visual_permission_required": True,
            "explicit_visual_confirmation_required": True,
            "foreground_only_required": True,
            "single_capture_permission_scope": True,
            "per_request_permission_required": True,
            "permission_packet_schema_ready": True,
            "permission_scope_schema_ready": True,
            "permission_decision_schema_ready": True,
            "permission_expiry_schema_ready": True,
            "audit_event_schema_ready": True,
            "redaction_policy_schema_ready": True,
            "redaction_preview_schema_ready": True,
            "redaction_scope_schema_ready": True,
            "sensitive_region_redaction_required": True,
            "window_title_redaction_required": True,
            "url_redaction_required": True,
            "clipboard_exclusion_required": True,
            "secret_token_redaction_required": True,
            "personal_identifier_redaction_required": True,
            "visible_text_redaction_required": True,
            "permission_required_before_visual_input": True,
            "permission_required_before_screenshot": True,
            "permission_required_before_screen_context": True,
            "permission_required_before_model_adapter": True,
            "permission_required_before_model_request": True,
            "permission_required_before_chat_handoff": True,
            "permission_required_before_visual_action": True,
            "redaction_required_before_context_adapter": True,
            "redaction_required_before_context_packet": True,
            "redaction_required_before_model_request": True,
            "redaction_required_before_model_response": True,
            "redaction_required_before_chat_handoff": True,
            "redaction_required_before_memory_write": True,
            "no_raw_screenshot_to_model": True,
            "no_raw_screenshot_to_chat": True,
            "no_unredacted_context_to_model": True,
            "no_unredacted_context_to_chat": True,
            "no_clipboard_capture": True,
            "no_sensitive_window_title_exposure": True,
            "no_url_exposure": True,
            "no_identity_claims": True,
            "no_biometric_identification": True,
            "no_face_recognition": True,
            "no_emotion_inference_from_face": True,
            "no_visual_context_to_action_bypass": True,
            "image_file_read_allowed": False,
            "screenshot_capture_required_now": False,
            "screenshot_file_read_required_now": False,
            "ocr_required_now": False,
            "cloud_vision_fallback_allowed": False,
            "external_upload_allowed": False,
            "model_download_required_now": False,
            "dependency_install_performed": False,
            "permission_prompt_runtime_active": False,
            "permission_grant_mutation_active": False,
            "redaction_runtime_active": False,
            "redaction_preview_created": False,
            "redacted_context_created": False,
            "redaction_audit_write_active": False,
            "screen_capture_runtime_ready": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_read_active": False,
            "screen_context_packet_created": False,
            "screen_context_handoff_active": False,
            "local_vision_model_adapter_active": False,
            "local_model_provider_probe_active": False,
            "local_model_request_active": False,
            "local_model_inference_active": False,
            "model_to_chat_handoff_active": False,
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
            "visual_context_to_action_bypass_enabled": False,
            "no_tool_use_from_visual_context": True,
            "no_autonomous_action": True,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "runtime_scope": "vision_permission_and_redaction_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": local_model["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = local_model[blocker]

        contract["redaction_runtime_active"] = False
        contract["vision_model_runtime_active"] = False
        contract["ocr_runtime_active"] = False
        contract["image_analysis_runtime_active"] = False
        contract["object_detection_runtime_active"] = False
        contract["visual_context_to_action_bypass_enabled"] = False
        contract["visual_action_execution_active"] = False
        contract["visual_tool_execution_active"] = False
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

    def workspace_visual_understanding_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()
        screen_context = self.screen_context_adapter_contract()
        local_model = self.local_vision_model_adapter_contract()
        permission_redaction = self.vision_permission_and_redaction_contract()
        dependencies = self.dependency_check()
        safety_blockers = list(permission_redaction["safety_blockers"])

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 206,
            "name": "workspace_visual_understanding",
            "workspace_visual_understanding_contract_ready": True,
            "workspace_visual_understanding_runtime_ready": False,
            "workspace_visual_understanding_status": "workspace_visual_understanding_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 206,
            "vision_runtime_next_sprint": 207,
            "vision_runtime_next_boundary": "vision_to_chat_context_handoff",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "previous_screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "previous_local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "previous_vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"],
            "previous_vision_permission_redaction_runtime_ready": permission_redaction["vision_permission_redaction_runtime_ready"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "workspace_visual_understanding_contract_only": True,
            "provided_redacted_visual_context_required": True,
            "provided_screen_metadata_required": True,
            "provided_workspace_metadata_required": True,
            "provided_user_question_required": True,
            "provided_permission_packet_required": True,
            "redaction_proof_required": True,
            "source_metadata_required": True,
            "uncertainty_required": True,
            "workspace_visual_summary_schema_ready": True,
            "workspace_layout_schema_ready": True,
            "active_window_schema_ready": True,
            "visible_region_schema_ready": True,
            "visual_element_schema_ready": True,
            "attention_target_schema_ready": True,
            "workspace_risk_schema_ready": True,
            "limitation_schema_ready": True,
            "workspace_overview_contract_ready": True,
            "window_layout_contract_ready": True,
            "visible_region_contract_ready": True,
            "ui_element_hint_contract_ready": True,
            "task_context_contract_ready": True,
            "risk_summary_contract_ready": True,
            "uncertainty_summary_contract_ready": True,
            "permission_required_before_workspace_understanding": True,
            "permission_required_before_context_handoff": True,
            "permission_required_before_chat_handoff": True,
            "redaction_required_before_workspace_understanding": True,
            "redaction_required_before_workspace_summary": True,
            "redaction_required_before_context_handoff": True,
            "redaction_required_before_chat_handoff": True,
            "no_raw_screenshot_to_workspace": True,
            "no_raw_screenshot_to_chat": True,
            "no_unredacted_context_to_workspace": True,
            "no_unredacted_context_to_chat": True,
            "no_ocr_claims_without_ocr": True,
            "no_model_claims_without_model": True,
            "no_identity_claims": True,
            "no_biometric_identification": True,
            "no_face_recognition": True,
            "no_emotion_inference_from_face": True,
            "no_action_recommendation_without_permission": True,
            "no_visual_context_to_action_bypass": True,
            "image_file_read_allowed": False,
            "screenshot_capture_required_now": False,
            "screenshot_file_read_required_now": False,
            "ocr_required_now": False,
            "cloud_vision_fallback_allowed": False,
            "external_upload_allowed": False,
            "model_download_required_now": False,
            "dependency_install_performed": False,
            "workspace_visual_understanding_runtime_active": False,
            "workspace_visual_summary_created": False,
            "workspace_layout_created": False,
            "visual_element_list_created": False,
            "attention_target_created": False,
            "workspace_risk_assessment_created": False,
            "workspace_to_chat_handoff_active": False,
            "permission_prompt_runtime_active": False,
            "permission_grant_mutation_active": False,
            "redaction_runtime_active": False,
            "redaction_preview_created": False,
            "redacted_context_created": False,
            "redaction_audit_write_active": False,
            "screen_capture_runtime_ready": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_read_active": False,
            "screen_context_packet_created": False,
            "screen_context_handoff_active": False,
            "local_vision_model_adapter_active": False,
            "local_model_provider_probe_active": False,
            "local_model_request_active": False,
            "local_model_inference_active": False,
            "model_to_chat_handoff_active": False,
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
            "visual_context_to_action_bypass_enabled": False,
            "no_tool_use_from_visual_context": True,
            "no_autonomous_action": True,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "runtime_scope": "workspace_visual_understanding_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": permission_redaction["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = permission_redaction[blocker]

        contract["vision_runtime_active"] = False
        contract["visual_context_runtime_active"] = False
        contract["image_analysis_runtime_active"] = False
        contract["object_detection_runtime_active"] = False
        contract["ocr_runtime_active"] = False
        contract["visual_context_to_action_bypass_enabled"] = False
        contract["visual_action_execution_active"] = False
        contract["visual_tool_execution_active"] = False
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

    def vision_to_chat_context_handoff_contract(self) -> dict[str, Any]:
        activation = self.vision_runtime_activation_contract()
        screenshot = self.explicit_screenshot_capture_contract()
        screen_context = self.screen_context_adapter_contract()
        local_model = self.local_vision_model_adapter_contract()
        permission_redaction = self.vision_permission_and_redaction_contract()
        workspace_visual = self.workspace_visual_understanding_contract()
        dependencies = self.dependency_check()
        safety_blockers = list(workspace_visual["safety_blockers"])

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        contract = {
            "sprint": 207,
            "name": "vision_to_chat_context_handoff",
            "vision_to_chat_context_handoff_contract_ready": True,
            "vision_to_chat_context_handoff_runtime_ready": False,
            "vision_to_chat_context_handoff_status": "vision_to_chat_context_handoff_contract_ready",
            "vision_runtime_block_start": 201,
            "vision_runtime_block_end": 210,
            "vision_runtime_current_sprint": 207,
            "vision_runtime_next_sprint": 208,
            "vision_runtime_next_boundary": "control_center_vision_panel",
            "previous_activation_contract_ready": activation["vision_runtime_activation_contract_ready"],
            "previous_explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"],
            "previous_screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "previous_local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "previous_vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"],
            "previous_workspace_visual_understanding_contract_ready": workspace_visual["workspace_visual_understanding_contract_ready"],
            "previous_workspace_visual_understanding_runtime_ready": workspace_visual["workspace_visual_understanding_runtime_ready"],
            "previous_workspace_to_chat_handoff_active": workspace_visual["workspace_to_chat_handoff_active"],
            "runtime_ready": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "vision_to_chat_context_handoff_contract_only": True,
            "provided_redacted_visual_context_required": True,
            "provided_workspace_visual_summary_required": True,
            "provided_workspace_metadata_required": True,
            "provided_user_question_required": True,
            "provided_permission_packet_required": True,
            "redaction_proof_required": True,
            "source_metadata_required": True,
            "uncertainty_required": True,
            "chat_safe_visual_context_packet_schema_ready": True,
            "chat_safe_visual_summary_schema_ready": True,
            "chat_safe_workspace_summary_schema_ready": True,
            "chat_context_handoff_packet_schema_ready": True,
            "chat_source_attribution_schema_ready": True,
            "chat_limitation_schema_ready": True,
            "chat_uncertainty_schema_ready": True,
            "chat_risk_notice_schema_ready": True,
            "chat_handoff_preview_schema_ready": True,
            "chat_visible_disclosure_contract_ready": True,
            "chat_render_boundary_contract_ready": True,
            "permission_required_before_chat_handoff": True,
            "permission_required_before_chat_context_injection": True,
            "permission_required_before_chat_session_write": True,
            "redaction_required_before_chat_handoff": True,
            "redaction_required_before_chat_context_packet": True,
            "redaction_required_before_chat_session_write": True,
            "explicit_user_request_required_for_handoff": True,
            "explicit_confirmation_required_for_handoff": True,
            "foreground_chat_session_required": True,
            "no_raw_screenshot_to_chat": True,
            "no_unredacted_context_to_chat": True,
            "no_hidden_visual_context_injection": True,
            "no_automatic_chat_handoff": True,
            "no_chat_model_request_without_user_message": True,
            "no_memory_write_from_visual_handoff": True,
            "no_action_recommendation_without_permission": True,
            "no_ocr_claims_without_ocr": True,
            "no_model_claims_without_model": True,
            "no_identity_claims": True,
            "no_biometric_identification": True,
            "no_face_recognition": True,
            "no_emotion_inference_from_face": True,
            "image_file_read_allowed": False,
            "screenshot_capture_required_now": False,
            "screenshot_file_read_required_now": False,
            "ocr_required_now": False,
            "cloud_vision_fallback_allowed": False,
            "external_upload_allowed": False,
            "model_download_required_now": False,
            "dependency_install_performed": False,
            "vision_to_chat_context_handoff_runtime_active": False,
            "chat_context_packet_created": False,
            "chat_safe_visual_summary_created": False,
            "chat_source_attribution_created": False,
            "chat_handoff_preview_created": False,
            "chat_message_injection_active": False,
            "chat_session_write_active": False,
            "chat_model_request_active": False,
            "chat_response_generation_active": False,
            "workspace_to_chat_handoff_active": False,
            "workspace_visual_summary_created": False,
            "redaction_runtime_active": False,
            "redacted_context_created": False,
            "redaction_audit_write_active": False,
            "screen_capture_runtime_ready": False,
            "screenshot_capture_performed": False,
            "screenshot_output_file_created": False,
            "screenshot_file_read_active": False,
            "screen_context_packet_created": False,
            "screen_context_handoff_active": False,
            "local_vision_model_adapter_active": False,
            "local_model_request_active": False,
            "local_model_inference_active": False,
            "model_to_chat_handoff_active": False,
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
            "visual_context_to_action_bypass_enabled": False,
            "no_tool_use_from_visual_context": True,
            "no_autonomous_action": True,
            "python_packages_installed": installed_python,
            "python_packages_total": len(dependencies["python_packages"]),
            "executables_found": found_executables,
            "executables_total": len(dependencies["executables"]),
            "runtime_scope": "vision_to_chat_context_handoff_contract_only",
            "safety_blockers": safety_blockers,
            "safety_blocker_count": len(safety_blockers),
            "all_safety_blockers_inactive": workspace_visual["all_safety_blockers_inactive"],
        }

        for blocker in safety_blockers:
            contract[blocker] = workspace_visual[blocker]

        contract["vision_runtime_active"] = False
        contract["visual_context_runtime_active"] = False
        contract["image_analysis_runtime_active"] = False
        contract["object_detection_runtime_active"] = False
        contract["ocr_runtime_active"] = False
        contract["visual_context_to_action_bypass_enabled"] = False
        contract["visual_action_execution_active"] = False
        contract["visual_tool_execution_active"] = False
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
        screen_context = self.screen_context_adapter_contract()
        local_model = self.local_vision_model_adapter_contract()
        permission_redaction = self.vision_permission_and_redaction_contract()
        workspace_visual = self.workspace_visual_understanding_contract()
        vision_to_chat = self.vision_to_chat_context_handoff_contract()

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
            "screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "screen_context_adapter_runtime_ready": screen_context["screen_context_adapter_runtime_ready"],
            "screen_context_adapter_status": screen_context["screen_context_adapter_status"],
            "local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "local_vision_model_adapter_runtime_ready": local_model["local_vision_model_adapter_runtime_ready"],
            "local_vision_model_adapter_status": local_model["local_vision_model_adapter_status"],
            "vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"],
            "vision_permission_redaction_runtime_ready": permission_redaction["vision_permission_redaction_runtime_ready"],
            "vision_permission_redaction_status": permission_redaction["vision_permission_redaction_status"],
            "workspace_visual_understanding_contract_ready": workspace_visual["workspace_visual_understanding_contract_ready"],
            "workspace_visual_understanding_runtime_ready": workspace_visual["workspace_visual_understanding_runtime_ready"],
            "workspace_visual_understanding_status": workspace_visual["workspace_visual_understanding_status"],
            "vision_to_chat_context_handoff_contract_ready": vision_to_chat["vision_to_chat_context_handoff_contract_ready"],
            "vision_to_chat_context_handoff_runtime_ready": vision_to_chat["vision_to_chat_context_handoff_runtime_ready"],
            "vision_to_chat_context_handoff_status": vision_to_chat["vision_to_chat_context_handoff_status"],
            "vision_runtime_block_start": vision_to_chat["vision_runtime_block_start"],
            "vision_runtime_block_end": vision_to_chat["vision_runtime_block_end"],
            "vision_runtime_current_sprint": vision_to_chat["vision_runtime_current_sprint"],
            "vision_runtime_next_sprint": vision_to_chat["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": vision_to_chat["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": vision_to_chat["runtime_activation_allowed"],
            "vision_release_gate_open": vision_to_chat["release_gate_open"],
            "vision_safe_idle_default": activation["safe_idle_default"],
            "vision_explicit_visual_input_required": activation["explicit_visual_input_required"],
            "vision_explicit_user_confirmation_required": activation["explicit_user_confirmation_required"],
            "explicit_screenshot_request_required": screenshot["explicit_screenshot_request_required"],
            "explicit_screenshot_confirmation_required": screenshot["explicit_screenshot_confirmation_required"],
            "permission_required_before_screenshot": permission_redaction["permission_required_before_screenshot"],
            "vision_permission_required_before_screen": screenshot["permission_required_before_screen"],
            "vision_permission_required_before_camera": activation["permission_required_before_camera"],
            "vision_permission_required_before_image_analysis": activation["permission_required_before_image_analysis"],
            "vision_permission_required_before_visual_action": permission_redaction["permission_required_before_visual_action"],
            "vision_user_provided_image_first": activation["user_provided_image_first"],
            "single_capture_only": screenshot["single_capture_only"],
            "continuous_capture_allowed": screenshot["continuous_capture_allowed"],
            "background_capture_allowed": screenshot["background_capture_allowed"],
            "silent_capture_allowed": screenshot["silent_capture_allowed"],
            "automatic_capture_allowed": screenshot["automatic_capture_allowed"],
            "vision_screen_permission_action": permission_redaction["screen_permission_action"],
            "vision_camera_permission_action": permission_redaction["camera_permission_action"],
            "screenshot_candidate_count": screenshot["screenshot_candidate_count"],
            "screenshot_capture_runtime_ready": screenshot["screenshot_capture_runtime_ready"],
            "screenshot_capture_active": workspace_visual["screenshot_capture_active"],
            "screenshot_capture_performed": workspace_visual["screenshot_capture_performed"],
            "screenshot_output_file_created": workspace_visual["screenshot_output_file_created"],
            "screenshot_to_context_handoff_active": screen_context["screenshot_to_context_handoff_active"],
            "provided_screenshot_context_required": screen_context["provided_screenshot_context_required"],
            "provided_screen_metadata_required": workspace_visual["provided_screen_metadata_required"],
            "placeholder_context_only": screen_context["placeholder_context_only"],
            "screen_context_input_schema_ready": screen_context["screen_context_input_schema_ready"],
            "screen_context_packet_schema_ready": screen_context["screen_context_packet_schema_ready"],
            "screen_context_summary_contract_ready": screen_context["screen_context_summary_contract_ready"],
            "redaction_required_before_context_adapter": permission_redaction["redaction_required_before_context_adapter"],
            "redaction_required_before_context_packet": permission_redaction["redaction_required_before_context_packet"],
            "screen_context_adapter_active": screen_context["screen_context_adapter_active"],
            "screen_context_input_received": screen_context["screen_context_input_received"],
            "screen_context_packet_created": workspace_visual["screen_context_packet_created"],
            "screen_context_handoff_active": workspace_visual["screen_context_handoff_active"],
            "screen_context_to_chat_handoff_active": screen_context["screen_context_to_chat_handoff_active"],
            "local_first_required": local_model["local_first_required"],
            "offline_first_required": local_model["offline_first_required"],
            "local_provider_contract_ready": local_model["local_provider_contract_ready"],
            "supported_local_provider_count": local_model["supported_local_provider_count"],
            "local_vision_model_candidate_count": local_model["local_vision_model_candidate_count"],
            "local_vision_model_candidates_ready": local_model["local_vision_model_candidates_ready"],
            "local_vision_model_default_candidate": local_model["local_vision_model_default_candidate"],
            "model_request_schema_ready": local_model["model_request_schema_ready"],
            "model_response_schema_ready": local_model["model_response_schema_ready"],
            "permission_required_before_model_request": permission_redaction["permission_required_before_model_request"],
            "redaction_required_before_model_request": permission_redaction["redaction_required_before_model_request"],
            "no_raw_screenshot_to_model": permission_redaction["no_raw_screenshot_to_model"],
            "no_unredacted_context_to_model": permission_redaction["no_unredacted_context_to_model"],
            "model_download_required_now": local_model["model_download_required_now"],
            "model_download_performed": local_model["model_download_performed"],
            "local_vision_model_adapter_active": workspace_visual["local_vision_model_adapter_active"],
            "local_model_provider_probe_active": workspace_visual["local_model_provider_probe_active"],
            "local_model_request_active": workspace_visual["local_model_request_active"],
            "local_model_inference_active": workspace_visual["local_model_inference_active"],
            "local_model_response_created": local_model["local_model_response_created"],
            "model_to_chat_handoff_active": workspace_visual["model_to_chat_handoff_active"],
            "explicit_visual_permission_required": permission_redaction["explicit_visual_permission_required"],
            "explicit_visual_confirmation_required": permission_redaction["explicit_visual_confirmation_required"],
            "foreground_only_required": permission_redaction["foreground_only_required"],
            "per_request_permission_required": permission_redaction["per_request_permission_required"],
            "permission_packet_schema_ready": permission_redaction["permission_packet_schema_ready"],
            "permission_scope_schema_ready": permission_redaction["permission_scope_schema_ready"],
            "permission_decision_schema_ready": permission_redaction["permission_decision_schema_ready"],
            "permission_expiry_schema_ready": permission_redaction["permission_expiry_schema_ready"],
            "audit_event_schema_ready": permission_redaction["audit_event_schema_ready"],
            "redaction_policy_schema_ready": permission_redaction["redaction_policy_schema_ready"],
            "redaction_preview_schema_ready": permission_redaction["redaction_preview_schema_ready"],
            "redaction_scope_schema_ready": permission_redaction["redaction_scope_schema_ready"],
            "sensitive_region_redaction_required": permission_redaction["sensitive_region_redaction_required"],
            "window_title_redaction_required": permission_redaction["window_title_redaction_required"],
            "url_redaction_required": permission_redaction["url_redaction_required"],
            "clipboard_exclusion_required": permission_redaction["clipboard_exclusion_required"],
            "secret_token_redaction_required": permission_redaction["secret_token_redaction_required"],
            "personal_identifier_redaction_required": permission_redaction["personal_identifier_redaction_required"],
            "visible_text_redaction_required": permission_redaction["visible_text_redaction_required"],
            "permission_prompt_runtime_active": workspace_visual["permission_prompt_runtime_active"],
            "permission_grant_mutation_active": workspace_visual["permission_grant_mutation_active"],
            "redaction_runtime_active": workspace_visual["redaction_runtime_active"],
            "redaction_preview_created": workspace_visual["redaction_preview_created"],
            "redacted_context_created": workspace_visual["redacted_context_created"],
            "redaction_audit_write_active": workspace_visual["redaction_audit_write_active"],
            "no_raw_screenshot_to_chat": permission_redaction["no_raw_screenshot_to_chat"],
            "no_unredacted_context_to_chat": permission_redaction["no_unredacted_context_to_chat"],
            "no_clipboard_capture": permission_redaction["no_clipboard_capture"],
            "no_sensitive_window_title_exposure": permission_redaction["no_sensitive_window_title_exposure"],
            "no_url_exposure": permission_redaction["no_url_exposure"],
            "provided_redacted_visual_context_required": workspace_visual["provided_redacted_visual_context_required"],
            "provided_workspace_metadata_required": workspace_visual["provided_workspace_metadata_required"],
            "provided_user_question_required": workspace_visual["provided_user_question_required"],
            "provided_permission_packet_required": workspace_visual["provided_permission_packet_required"],
            "redaction_proof_required": workspace_visual["redaction_proof_required"],
            "workspace_visual_summary_schema_ready": workspace_visual["workspace_visual_summary_schema_ready"],
            "workspace_layout_schema_ready": workspace_visual["workspace_layout_schema_ready"],
            "active_window_schema_ready": workspace_visual["active_window_schema_ready"],
            "visible_region_schema_ready": workspace_visual["visible_region_schema_ready"],
            "visual_element_schema_ready": workspace_visual["visual_element_schema_ready"],
            "attention_target_schema_ready": workspace_visual["attention_target_schema_ready"],
            "workspace_risk_schema_ready": workspace_visual["workspace_risk_schema_ready"],
            "limitation_schema_ready": workspace_visual["limitation_schema_ready"],
            "workspace_overview_contract_ready": workspace_visual["workspace_overview_contract_ready"],
            "window_layout_contract_ready": workspace_visual["window_layout_contract_ready"],
            "visible_region_contract_ready": workspace_visual["visible_region_contract_ready"],
            "ui_element_hint_contract_ready": workspace_visual["ui_element_hint_contract_ready"],
            "task_context_contract_ready": workspace_visual["task_context_contract_ready"],
            "risk_summary_contract_ready": workspace_visual["risk_summary_contract_ready"],
            "uncertainty_summary_contract_ready": workspace_visual["uncertainty_summary_contract_ready"],
            "permission_required_before_workspace_understanding": workspace_visual["permission_required_before_workspace_understanding"],
            "redaction_required_before_workspace_understanding": workspace_visual["redaction_required_before_workspace_understanding"],
            "redaction_required_before_workspace_summary": workspace_visual["redaction_required_before_workspace_summary"],
            "no_raw_screenshot_to_workspace": workspace_visual["no_raw_screenshot_to_workspace"],
            "no_unredacted_context_to_workspace": workspace_visual["no_unredacted_context_to_workspace"],
            "no_ocr_claims_without_ocr": workspace_visual["no_ocr_claims_without_ocr"],
            "no_model_claims_without_model": workspace_visual["no_model_claims_without_model"],
            "workspace_visual_understanding_runtime_active": workspace_visual["workspace_visual_understanding_runtime_active"],
            "workspace_visual_summary_created": workspace_visual["workspace_visual_summary_created"],
            "workspace_layout_created": workspace_visual["workspace_layout_created"],
            "visual_element_list_created": workspace_visual["visual_element_list_created"],
            "attention_target_created": workspace_visual["attention_target_created"],
            "workspace_risk_assessment_created": workspace_visual["workspace_risk_assessment_created"],
            "workspace_to_chat_handoff_active": workspace_visual["workspace_to_chat_handoff_active"],
            "chat_safe_visual_context_packet_schema_ready": vision_to_chat["chat_safe_visual_context_packet_schema_ready"],
            "chat_safe_visual_summary_schema_ready": vision_to_chat["chat_safe_visual_summary_schema_ready"],
            "chat_safe_workspace_summary_schema_ready": vision_to_chat["chat_safe_workspace_summary_schema_ready"],
            "chat_context_handoff_packet_schema_ready": vision_to_chat["chat_context_handoff_packet_schema_ready"],
            "chat_source_attribution_schema_ready": vision_to_chat["chat_source_attribution_schema_ready"],
            "chat_limitation_schema_ready": vision_to_chat["chat_limitation_schema_ready"],
            "chat_uncertainty_schema_ready": vision_to_chat["chat_uncertainty_schema_ready"],
            "chat_risk_notice_schema_ready": vision_to_chat["chat_risk_notice_schema_ready"],
            "chat_handoff_preview_schema_ready": vision_to_chat["chat_handoff_preview_schema_ready"],
            "chat_visible_disclosure_contract_ready": vision_to_chat["chat_visible_disclosure_contract_ready"],
            "chat_render_boundary_contract_ready": vision_to_chat["chat_render_boundary_contract_ready"],
            "permission_required_before_chat_context_injection": vision_to_chat["permission_required_before_chat_context_injection"],
            "permission_required_before_chat_session_write": vision_to_chat["permission_required_before_chat_session_write"],
            "redaction_required_before_chat_context_packet": vision_to_chat["redaction_required_before_chat_context_packet"],
            "redaction_required_before_chat_session_write": vision_to_chat["redaction_required_before_chat_session_write"],
            "explicit_user_request_required_for_handoff": vision_to_chat["explicit_user_request_required_for_handoff"],
            "explicit_confirmation_required_for_handoff": vision_to_chat["explicit_confirmation_required_for_handoff"],
            "foreground_chat_session_required": vision_to_chat["foreground_chat_session_required"],
            "no_hidden_visual_context_injection": vision_to_chat["no_hidden_visual_context_injection"],
            "no_automatic_chat_handoff": vision_to_chat["no_automatic_chat_handoff"],
            "no_chat_model_request_without_user_message": vision_to_chat["no_chat_model_request_without_user_message"],
            "no_memory_write_from_visual_handoff": vision_to_chat["no_memory_write_from_visual_handoff"],
            "vision_to_chat_context_handoff_runtime_active": vision_to_chat["vision_to_chat_context_handoff_runtime_active"],
            "chat_context_packet_created": vision_to_chat["chat_context_packet_created"],
            "chat_safe_visual_summary_created": vision_to_chat["chat_safe_visual_summary_created"],
            "chat_source_attribution_created": vision_to_chat["chat_source_attribution_created"],
            "chat_handoff_preview_created": vision_to_chat["chat_handoff_preview_created"],
            "chat_message_injection_active": vision_to_chat["chat_message_injection_active"],
            "chat_session_write_active": vision_to_chat["chat_session_write_active"],
            "chat_model_request_active": vision_to_chat["chat_model_request_active"],
            "chat_response_generation_active": vision_to_chat["chat_response_generation_active"],
            "vision_model_runtime_active": workspace_visual["vision_model_runtime_active"],
            "ocr_runtime_active": workspace_visual["ocr_runtime_active"],
            "cloud_vision_fallback_enabled": workspace_visual["cloud_vision_fallback_enabled"],
            "external_upload_enabled": workspace_visual["external_upload_enabled"],
            "vision_safety_blocker_count": vision_to_chat["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": vision_to_chat["all_safety_blockers_inactive"],
            "vision_runtime_activation_contract": activation,
            "explicit_screenshot_capture_contract": screenshot,
            "screen_context_adapter_contract": screen_context,
            "local_vision_model_adapter_contract": local_model,
            "vision_permission_redaction_contract": permission_redaction,
            "workspace_visual_understanding_contract": workspace_visual,
            "vision_to_chat_context_handoff_contract": vision_to_chat,
            "note": "Vision-to-chat context handoff contract is ready for Sprint 207; it defines chat-safe visual context packets and handoff gates while keeping chat context injection, chat session writes, model requests, response generation, memory writes, screenshot capture, image file read, OCR, visual actions, cloud fallback, and external upload disabled.",
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
        screen_context = self.screen_context_adapter_contract()
        local_model = self.local_vision_model_adapter_contract()
        permission_redaction = self.vision_permission_and_redaction_contract()
        workspace_visual = self.workspace_visual_understanding_contract()
        vision_to_chat = self.vision_to_chat_context_handoff_contract()

        installed_python = sum(
            1 for package in dependencies["python_packages"] if package["installed"]
        )
        found_executables = sum(
            1 for executable in dependencies["executables"] if executable["found"]
        )

        assertions = {
            "vision_runtime_activation_contract_ready": activation["vision_runtime_activation_contract_ready"] is True,
            "vision_runtime_activation_runtime_not_ready": activation["vision_runtime_activation_runtime_ready"] is False,
            "explicit_screenshot_capture_contract_ready": screenshot["explicit_screenshot_capture_contract_ready"] is True,
            "explicit_screenshot_capture_runtime_not_ready": screenshot["explicit_screenshot_capture_runtime_ready"] is False,
            "screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"] is True,
            "screen_context_adapter_runtime_not_ready": screen_context["screen_context_adapter_runtime_ready"] is False,
            "local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"] is True,
            "local_vision_model_adapter_runtime_not_ready": local_model["local_vision_model_adapter_runtime_ready"] is False,
            "vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"] is True,
            "vision_permission_redaction_runtime_not_ready": permission_redaction["vision_permission_redaction_runtime_ready"] is False,
            "workspace_visual_understanding_contract_ready": workspace_visual["workspace_visual_understanding_contract_ready"] is True,
            "workspace_visual_understanding_runtime_not_ready": workspace_visual["workspace_visual_understanding_runtime_ready"] is False,
            "vision_to_chat_context_handoff_contract_ready": vision_to_chat["vision_to_chat_context_handoff_contract_ready"] is True,
            "vision_to_chat_context_handoff_runtime_not_ready": vision_to_chat["vision_to_chat_context_handoff_runtime_ready"] is False,
            "vision_to_chat_context_handoff_status_ready": vision_to_chat["vision_to_chat_context_handoff_status"] == "vision_to_chat_context_handoff_contract_ready",
            "vision_runtime_block_start_201": vision_to_chat["vision_runtime_block_start"] == 201,
            "vision_runtime_block_end_210": vision_to_chat["vision_runtime_block_end"] == 210,
            "vision_runtime_current_sprint_207": vision_to_chat["vision_runtime_current_sprint"] == 207,
            "vision_runtime_next_sprint_208": vision_to_chat["vision_runtime_next_sprint"] == 208,
            "vision_runtime_next_boundary_control_center_vision_panel": vision_to_chat["vision_runtime_next_boundary"] == "control_center_vision_panel",
            "previous_activation_contract_ready": vision_to_chat["previous_activation_contract_ready"] is True,
            "previous_screenshot_contract_ready": vision_to_chat["previous_explicit_screenshot_capture_contract_ready"] is True,
            "previous_screen_context_contract_ready": vision_to_chat["previous_screen_context_adapter_contract_ready"] is True,
            "previous_local_model_contract_ready": vision_to_chat["previous_local_vision_model_adapter_contract_ready"] is True,
            "previous_permission_redaction_contract_ready": vision_to_chat["previous_vision_permission_redaction_contract_ready"] is True,
            "previous_workspace_visual_contract_ready": vision_to_chat["previous_workspace_visual_understanding_contract_ready"] is True,
            "previous_workspace_visual_runtime_not_ready": vision_to_chat["previous_workspace_visual_understanding_runtime_ready"] is False,
            "previous_workspace_to_chat_handoff_inactive": vision_to_chat["previous_workspace_to_chat_handoff_active"] is False,
            "runtime_not_ready": vision_to_chat["runtime_ready"] is False,
            "runtime_activation_not_allowed": vision_to_chat["runtime_activation_allowed"] is False,
            "release_gate_closed": vision_to_chat["release_gate_open"] is False,
            "contract_only": vision_to_chat["vision_to_chat_context_handoff_contract_only"] is True,
            "provided_redacted_visual_context_required": vision_to_chat["provided_redacted_visual_context_required"] is True,
            "provided_workspace_visual_summary_required": vision_to_chat["provided_workspace_visual_summary_required"] is True,
            "provided_workspace_metadata_required": vision_to_chat["provided_workspace_metadata_required"] is True,
            "provided_user_question_required": vision_to_chat["provided_user_question_required"] is True,
            "provided_permission_packet_required": vision_to_chat["provided_permission_packet_required"] is True,
            "redaction_proof_required": vision_to_chat["redaction_proof_required"] is True,
            "source_metadata_required": vision_to_chat["source_metadata_required"] is True,
            "uncertainty_required": vision_to_chat["uncertainty_required"] is True,
            "chat_safe_visual_context_packet_schema_ready": vision_to_chat["chat_safe_visual_context_packet_schema_ready"] is True,
            "chat_safe_visual_summary_schema_ready": vision_to_chat["chat_safe_visual_summary_schema_ready"] is True,
            "chat_safe_workspace_summary_schema_ready": vision_to_chat["chat_safe_workspace_summary_schema_ready"] is True,
            "chat_context_handoff_packet_schema_ready": vision_to_chat["chat_context_handoff_packet_schema_ready"] is True,
            "chat_source_attribution_schema_ready": vision_to_chat["chat_source_attribution_schema_ready"] is True,
            "chat_limitation_schema_ready": vision_to_chat["chat_limitation_schema_ready"] is True,
            "chat_uncertainty_schema_ready": vision_to_chat["chat_uncertainty_schema_ready"] is True,
            "chat_risk_notice_schema_ready": vision_to_chat["chat_risk_notice_schema_ready"] is True,
            "chat_handoff_preview_schema_ready": vision_to_chat["chat_handoff_preview_schema_ready"] is True,
            "chat_visible_disclosure_contract_ready": vision_to_chat["chat_visible_disclosure_contract_ready"] is True,
            "chat_render_boundary_contract_ready": vision_to_chat["chat_render_boundary_contract_ready"] is True,
            "permission_required_before_chat_handoff": vision_to_chat["permission_required_before_chat_handoff"] is True,
            "permission_required_before_chat_context_injection": vision_to_chat["permission_required_before_chat_context_injection"] is True,
            "permission_required_before_chat_session_write": vision_to_chat["permission_required_before_chat_session_write"] is True,
            "redaction_required_before_chat_handoff": vision_to_chat["redaction_required_before_chat_handoff"] is True,
            "redaction_required_before_chat_context_packet": vision_to_chat["redaction_required_before_chat_context_packet"] is True,
            "redaction_required_before_chat_session_write": vision_to_chat["redaction_required_before_chat_session_write"] is True,
            "explicit_user_request_required_for_handoff": vision_to_chat["explicit_user_request_required_for_handoff"] is True,
            "explicit_confirmation_required_for_handoff": vision_to_chat["explicit_confirmation_required_for_handoff"] is True,
            "foreground_chat_session_required": vision_to_chat["foreground_chat_session_required"] is True,
            "no_raw_screenshot_to_chat": vision_to_chat["no_raw_screenshot_to_chat"] is True,
            "no_unredacted_context_to_chat": vision_to_chat["no_unredacted_context_to_chat"] is True,
            "no_hidden_visual_context_injection": vision_to_chat["no_hidden_visual_context_injection"] is True,
            "no_automatic_chat_handoff": vision_to_chat["no_automatic_chat_handoff"] is True,
            "no_chat_model_request_without_user_message": vision_to_chat["no_chat_model_request_without_user_message"] is True,
            "no_memory_write_from_visual_handoff": vision_to_chat["no_memory_write_from_visual_handoff"] is True,
            "no_action_recommendation_without_permission": vision_to_chat["no_action_recommendation_without_permission"] is True,
            "no_ocr_claims_without_ocr": vision_to_chat["no_ocr_claims_without_ocr"] is True,
            "no_model_claims_without_model": vision_to_chat["no_model_claims_without_model"] is True,
            "no_identity_claims": vision_to_chat["no_identity_claims"] is True,
            "no_biometric_identification": vision_to_chat["no_biometric_identification"] is True,
            "no_face_recognition": vision_to_chat["no_face_recognition"] is True,
            "no_emotion_inference_from_face": vision_to_chat["no_emotion_inference_from_face"] is True,
            "image_file_read_not_allowed": vision_to_chat["image_file_read_allowed"] is False,
            "screenshot_capture_not_required_now": vision_to_chat["screenshot_capture_required_now"] is False,
            "screenshot_file_read_not_required_now": vision_to_chat["screenshot_file_read_required_now"] is False,
            "ocr_not_required_now": vision_to_chat["ocr_required_now"] is False,
            "cloud_vision_fallback_not_allowed": vision_to_chat["cloud_vision_fallback_allowed"] is False,
            "external_upload_not_allowed": vision_to_chat["external_upload_allowed"] is False,
            "model_download_not_required_now": vision_to_chat["model_download_required_now"] is False,
            "dependency_install_not_performed": vision_to_chat["dependency_install_performed"] is False,
            "vision_to_chat_context_handoff_runtime_inactive": vision_to_chat["vision_to_chat_context_handoff_runtime_active"] is False,
            "chat_context_packet_not_created": vision_to_chat["chat_context_packet_created"] is False,
            "chat_safe_visual_summary_not_created": vision_to_chat["chat_safe_visual_summary_created"] is False,
            "chat_source_attribution_not_created": vision_to_chat["chat_source_attribution_created"] is False,
            "chat_handoff_preview_not_created": vision_to_chat["chat_handoff_preview_created"] is False,
            "chat_message_injection_inactive": vision_to_chat["chat_message_injection_active"] is False,
            "chat_session_write_inactive": vision_to_chat["chat_session_write_active"] is False,
            "chat_model_request_inactive": vision_to_chat["chat_model_request_active"] is False,
            "chat_response_generation_inactive": vision_to_chat["chat_response_generation_active"] is False,
            "workspace_to_chat_handoff_inactive": vision_to_chat["workspace_to_chat_handoff_active"] is False,
            "workspace_visual_summary_not_created": vision_to_chat["workspace_visual_summary_created"] is False,
            "redaction_runtime_inactive": vision_to_chat["redaction_runtime_active"] is False,
            "redacted_context_not_created": vision_to_chat["redacted_context_created"] is False,
            "redaction_audit_write_inactive": vision_to_chat["redaction_audit_write_active"] is False,
            "screenshot_capture_not_performed": vision_to_chat["screenshot_capture_performed"] is False,
            "screenshot_file_read_inactive": vision_to_chat["screenshot_file_read_active"] is False,
            "screen_context_packet_not_created": vision_to_chat["screen_context_packet_created"] is False,
            "screen_context_handoff_inactive": vision_to_chat["screen_context_handoff_active"] is False,
            "local_model_adapter_inactive": vision_to_chat["local_vision_model_adapter_active"] is False,
            "local_model_request_inactive": vision_to_chat["local_model_request_active"] is False,
            "local_model_inference_inactive": vision_to_chat["local_model_inference_active"] is False,
            "model_to_chat_handoff_inactive": vision_to_chat["model_to_chat_handoff_active"] is False,
            "vision_model_runtime_inactive": vision_to_chat["vision_model_runtime_active"] is False,
            "ocr_runtime_inactive": vision_to_chat["ocr_runtime_active"] is False,
            "image_analysis_runtime_inactive": vision_to_chat["image_analysis_runtime_active"] is False,
            "object_detection_runtime_inactive": vision_to_chat["object_detection_runtime_active"] is False,
            "visual_action_execution_inactive": vision_to_chat["visual_action_execution_active"] is False,
            "visual_tool_execution_inactive": vision_to_chat["visual_tool_execution_active"] is False,
            "command_execution_inactive": vision_to_chat["command_execution_active"] is False,
            "file_mutation_inactive": vision_to_chat["file_mutation_active"] is False,
            "desktop_action_inactive": vision_to_chat["desktop_action_active"] is False,
            "network_action_inactive": vision_to_chat["network_action_active"] is False,
            "git_action_inactive": vision_to_chat["git_action_active"] is False,
            "memory_write_inactive": vision_to_chat["memory_write_active"] is False,
            "cloud_vision_fallback_disabled": vision_to_chat["cloud_vision_fallback_enabled"] is False,
            "external_upload_disabled": vision_to_chat["external_upload_enabled"] is False,
            "no_tool_use_from_visual_context": vision_to_chat["no_tool_use_from_visual_context"] is True,
            "no_autonomous_action": vision_to_chat["no_autonomous_action"] is True,
            "safety_blocker_count_33": vision_to_chat["safety_blocker_count"] == 33,
            "all_safety_blockers_inactive": vision_to_chat["all_safety_blockers_inactive"] is True,
        }

        for blocker in vision_to_chat["safety_blockers"]:
            assertions[f"safety_blocker_{blocker}_inactive"] = vision_to_chat[blocker] is False

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
            "screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "screen_context_adapter_runtime_ready": screen_context["screen_context_adapter_runtime_ready"],
            "screen_context_adapter_status": screen_context["screen_context_adapter_status"],
            "local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "local_vision_model_adapter_runtime_ready": local_model["local_vision_model_adapter_runtime_ready"],
            "local_vision_model_adapter_status": local_model["local_vision_model_adapter_status"],
            "vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"],
            "vision_permission_redaction_runtime_ready": permission_redaction["vision_permission_redaction_runtime_ready"],
            "vision_permission_redaction_status": permission_redaction["vision_permission_redaction_status"],
            "workspace_visual_understanding_contract_ready": workspace_visual["workspace_visual_understanding_contract_ready"],
            "workspace_visual_understanding_runtime_ready": workspace_visual["workspace_visual_understanding_runtime_ready"],
            "workspace_visual_understanding_status": workspace_visual["workspace_visual_understanding_status"],
            "vision_to_chat_context_handoff_contract_ready": vision_to_chat["vision_to_chat_context_handoff_contract_ready"],
            "vision_to_chat_context_handoff_runtime_ready": vision_to_chat["vision_to_chat_context_handoff_runtime_ready"],
            "vision_to_chat_context_handoff_status": vision_to_chat["vision_to_chat_context_handoff_status"],
            "vision_runtime_block_start": vision_to_chat["vision_runtime_block_start"],
            "vision_runtime_block_end": vision_to_chat["vision_runtime_block_end"],
            "vision_runtime_current_sprint": vision_to_chat["vision_runtime_current_sprint"],
            "vision_runtime_next_sprint": vision_to_chat["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": vision_to_chat["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": vision_to_chat["runtime_activation_allowed"],
            "vision_release_gate_open": vision_to_chat["release_gate_open"],
            "vision_safety_blocker_count": vision_to_chat["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": vision_to_chat["all_safety_blockers_inactive"],
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
            "screen_context_adapter_contract": screen_context,
            "local_vision_model_adapter_contract": local_model,
            "vision_permission_redaction_contract": permission_redaction,
            "workspace_visual_understanding_contract": workspace_visual,
            "vision_to_chat_context_handoff_contract": vision_to_chat,
            "note": "Runtime is not enabled yet. This check prepared the Sprint 207 vision-to-chat context handoff contract without injecting visual context into chat, writing chat sessions, requesting models, generating responses, writing memory, reading screenshots or image files, running OCR, executing tools/commands, controlling desktop, using network/git, cloud vision, external upload, or visual actions.",
        }
