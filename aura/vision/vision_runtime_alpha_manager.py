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
        screen_context = self.planner.screen_context_adapter_contract()
        local_model = self.planner.local_vision_model_adapter_contract()
        permission_redaction = self.planner.vision_permission_and_redaction_contract()
        workspace_visual = self.planner.workspace_visual_understanding_contract()
        vision_to_chat = self.planner.vision_to_chat_context_handoff_contract()
        control_center_vision_panel = self.planner.control_center_vision_panel_contract()
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
            "sprint_203_screen_context_adapter_contract_ready": screen_context["screen_context_adapter_contract_ready"],
            "sprint_204_local_vision_model_adapter_contract_ready": local_model["local_vision_model_adapter_contract_ready"],
            "sprint_205_vision_permission_redaction_contract_ready": permission_redaction["vision_permission_redaction_contract_ready"],
            "sprint_206_workspace_visual_understanding_contract_ready": workspace_visual["workspace_visual_understanding_contract_ready"],
            "sprint_207_vision_to_chat_context_handoff_contract_ready": vision_to_chat["vision_to_chat_context_handoff_contract_ready"],
            "sprint_208_control_center_vision_panel_contract_ready": control_center_vision_panel["control_center_vision_panel_contract_ready"],
            "control_center_vision_panel_runtime_ready": control_center_vision_panel["control_center_vision_panel_runtime_ready"],
            "control_center_vision_panel_status": control_center_vision_panel["control_center_vision_panel_status"],
            "read_only_panel_contract_ready": control_center_vision_panel["read_only_panel_contract_ready"],
            "display_only_panel_contract_ready": control_center_vision_panel["display_only_panel_contract_ready"],
            "vision_status_panel_schema_ready": control_center_vision_panel["vision_status_panel_schema_ready"],
            "vision_safety_panel_schema_ready": control_center_vision_panel["vision_safety_panel_schema_ready"],
            "vision_dependency_panel_schema_ready": control_center_vision_panel["vision_dependency_panel_schema_ready"],
            "vision_handoff_panel_schema_ready": control_center_vision_panel["vision_handoff_panel_schema_ready"],
            "vision_panel_route_contract_ready": control_center_vision_panel["vision_panel_route_contract_ready"],
            "vision_panel_view_model_contract_ready": control_center_vision_panel["vision_panel_view_model_contract_ready"],
            "vision_panel_no_mutation_contract_ready": control_center_vision_panel["vision_panel_no_mutation_contract_ready"],
            "vision_panel_no_capture_contract_ready": control_center_vision_panel["vision_panel_no_capture_contract_ready"],
            "no_permission_mutation_from_panel": control_center_vision_panel["no_permission_mutation_from_panel"],
            "no_screenshot_trigger_from_panel": control_center_vision_panel["no_screenshot_trigger_from_panel"],
            "no_camera_trigger_from_panel": control_center_vision_panel["no_camera_trigger_from_panel"],
            "no_model_request_trigger_from_panel": control_center_vision_panel["no_model_request_trigger_from_panel"],
            "no_chat_handoff_trigger_from_panel": control_center_vision_panel["no_chat_handoff_trigger_from_panel"],
            "no_memory_write_from_panel": control_center_vision_panel["no_memory_write_from_panel"],
            "no_external_upload_from_panel": control_center_vision_panel["no_external_upload_from_panel"],
            "control_center_vision_panel_runtime_active": control_center_vision_panel["control_center_vision_panel_runtime_active"],
            "control_center_vision_panel_rendered": control_center_vision_panel["control_center_vision_panel_rendered"],
            "control_center_vision_panel_route_created": control_center_vision_panel["control_center_vision_panel_route_created"],
            "control_center_vision_panel_api_endpoint_created": control_center_vision_panel["control_center_vision_panel_api_endpoint_created"],
            "control_center_vision_panel_data_fetch_active": control_center_vision_panel["control_center_vision_panel_data_fetch_active"],
            "control_center_vision_panel_auto_refresh_active": control_center_vision_panel["control_center_vision_panel_auto_refresh_active"],
            "panel_permission_mutation_active": control_center_vision_panel["panel_permission_mutation_active"],
            "panel_audit_write_active": control_center_vision_panel["panel_audit_write_active"],
            "panel_screenshot_control_active": control_center_vision_panel["panel_screenshot_control_active"],
            "panel_chat_handoff_control_active": control_center_vision_panel["panel_chat_handoff_control_active"],
            "vision_to_chat_context_handoff_runtime_ready": vision_to_chat["vision_to_chat_context_handoff_runtime_ready"],
            "vision_to_chat_context_handoff_status": vision_to_chat["vision_to_chat_context_handoff_status"],
            "chat_safe_visual_context_packet_schema_ready": vision_to_chat["chat_safe_visual_context_packet_schema_ready"],
            "chat_safe_visual_summary_schema_ready": vision_to_chat["chat_safe_visual_summary_schema_ready"],
            "chat_context_handoff_packet_schema_ready": vision_to_chat["chat_context_handoff_packet_schema_ready"],
            "chat_source_attribution_schema_ready": vision_to_chat["chat_source_attribution_schema_ready"],
            "chat_limitation_schema_ready": vision_to_chat["chat_limitation_schema_ready"],
            "chat_uncertainty_schema_ready": vision_to_chat["chat_uncertainty_schema_ready"],
            "chat_handoff_preview_schema_ready": vision_to_chat["chat_handoff_preview_schema_ready"],
            "explicit_user_request_required_for_handoff": vision_to_chat["explicit_user_request_required_for_handoff"],
            "explicit_confirmation_required_for_handoff": vision_to_chat["explicit_confirmation_required_for_handoff"],
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
            "workspace_visual_understanding_runtime_ready": workspace_visual["workspace_visual_understanding_runtime_ready"],
            "workspace_visual_understanding_status": workspace_visual["workspace_visual_understanding_status"],
            "provided_redacted_visual_context_required": workspace_visual["provided_redacted_visual_context_required"],
            "provided_workspace_metadata_required": workspace_visual["provided_workspace_metadata_required"],
            "provided_user_question_required": workspace_visual["provided_user_question_required"],
            "redaction_proof_required": workspace_visual["redaction_proof_required"],
            "workspace_visual_summary_schema_ready": workspace_visual["workspace_visual_summary_schema_ready"],
            "workspace_layout_schema_ready": workspace_visual["workspace_layout_schema_ready"],
            "active_window_schema_ready": workspace_visual["active_window_schema_ready"],
            "visual_element_schema_ready": workspace_visual["visual_element_schema_ready"],
            "workspace_risk_schema_ready": workspace_visual["workspace_risk_schema_ready"],
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
            "workspace_risk_assessment_created": workspace_visual["workspace_risk_assessment_created"],
            "workspace_to_chat_handoff_active": workspace_visual["workspace_to_chat_handoff_active"],
            "vision_permission_redaction_runtime_ready": permission_redaction["vision_permission_redaction_runtime_ready"],
            "vision_permission_redaction_status": permission_redaction["vision_permission_redaction_status"],
            "explicit_visual_permission_required": permission_redaction["explicit_visual_permission_required"],
            "explicit_visual_confirmation_required": permission_redaction["explicit_visual_confirmation_required"],
            "foreground_only_required": permission_redaction["foreground_only_required"],
            "per_request_permission_required": permission_redaction["per_request_permission_required"],
            "permission_packet_schema_ready": permission_redaction["permission_packet_schema_ready"],
            "permission_scope_schema_ready": permission_redaction["permission_scope_schema_ready"],
            "permission_decision_schema_ready": permission_redaction["permission_decision_schema_ready"],
            "audit_event_schema_ready": permission_redaction["audit_event_schema_ready"],
            "redaction_policy_schema_ready": permission_redaction["redaction_policy_schema_ready"],
            "redaction_preview_schema_ready": permission_redaction["redaction_preview_schema_ready"],
            "sensitive_region_redaction_required": permission_redaction["sensitive_region_redaction_required"],
            "window_title_redaction_required": permission_redaction["window_title_redaction_required"],
            "url_redaction_required": permission_redaction["url_redaction_required"],
            "clipboard_exclusion_required": permission_redaction["clipboard_exclusion_required"],
            "redaction_runtime_active": permission_redaction["redaction_runtime_active"],
            "redaction_preview_created": permission_redaction["redaction_preview_created"],
            "redacted_context_created": permission_redaction["redacted_context_created"],
            "permission_prompt_runtime_active": permission_redaction["permission_prompt_runtime_active"],
            "permission_grant_mutation_active": permission_redaction["permission_grant_mutation_active"],
            "redaction_audit_write_active": permission_redaction["redaction_audit_write_active"],
            "no_raw_screenshot_to_chat": permission_redaction["no_raw_screenshot_to_chat"],
            "no_unredacted_context_to_chat": permission_redaction["no_unredacted_context_to_chat"],
            "no_clipboard_capture": permission_redaction["no_clipboard_capture"],
            "local_vision_model_adapter_runtime_ready": local_model["local_vision_model_adapter_runtime_ready"],
            "local_vision_model_adapter_status": local_model["local_vision_model_adapter_status"],
            "local_first_required": local_model["local_first_required"],
            "offline_first_required": local_model["offline_first_required"],
            "local_provider_contract_ready": local_model["local_provider_contract_ready"],
            "supported_local_provider_count": local_model["supported_local_provider_count"],
            "local_vision_model_candidate_count": local_model["local_vision_model_candidate_count"],
            "local_vision_model_candidates_ready": local_model["local_vision_model_candidates_ready"],
            "local_vision_model_default_candidate": local_model["local_vision_model_default_candidate"],
            "model_request_schema_ready": local_model["model_request_schema_ready"],
            "model_response_schema_ready": local_model["model_response_schema_ready"],
            "permission_required_before_model_request": local_model["permission_required_before_model_request"],
            "redaction_required_before_model_request": local_model["redaction_required_before_model_request"],
            "model_download_required_now": local_model["model_download_required_now"],
            "model_download_performed": local_model["model_download_performed"],
            "local_vision_model_adapter_active": local_model["local_vision_model_adapter_active"],
            "local_model_provider_probe_active": local_model["local_model_provider_probe_active"],
            "local_model_request_active": local_model["local_model_request_active"],
            "local_model_inference_active": local_model["local_model_inference_active"],
            "local_model_response_created": local_model["local_model_response_created"],
            "model_to_chat_handoff_active": local_model["model_to_chat_handoff_active"],
            "cloud_vision_fallback_enabled": local_model["cloud_vision_fallback_enabled"],
            "external_upload_enabled": local_model["external_upload_enabled"],
            "screen_context_adapter_runtime_ready": screen_context["screen_context_adapter_runtime_ready"],
            "screen_context_adapter_status": screen_context["screen_context_adapter_status"],
            "provided_screenshot_context_required": screen_context["provided_screenshot_context_required"],
            "provided_screen_metadata_required": screen_context["provided_screen_metadata_required"],
            "placeholder_context_only": screen_context["placeholder_context_only"],
            "screen_context_input_schema_ready": screen_context["screen_context_input_schema_ready"],
            "screen_context_packet_schema_ready": screen_context["screen_context_packet_schema_ready"],
            "screen_context_summary_contract_ready": screen_context["screen_context_summary_contract_ready"],
            "redaction_required_before_context_adapter": screen_context["redaction_required_before_context_adapter"],
            "screen_context_adapter_active": screen_context["screen_context_adapter_active"],
            "screen_context_input_received": screen_context["screen_context_input_received"],
            "screen_context_packet_created": screen_context["screen_context_packet_created"],
            "screen_context_handoff_active": screen_context["screen_context_handoff_active"],
            "screen_context_to_chat_handoff_active": screen_context["screen_context_to_chat_handoff_active"],
            "redaction_runtime_active": screen_context["redaction_runtime_active"],
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
            "vision_runtime_next_sprint": control_center_vision_panel["vision_runtime_next_sprint"],
            "vision_runtime_next_boundary": control_center_vision_panel["vision_runtime_next_boundary"],
            "vision_runtime_activation_allowed": control_center_vision_panel["runtime_activation_allowed"],
            "vision_release_gate_open": control_center_vision_panel["release_gate_open"],
            "vision_safety_blocker_count": control_center_vision_panel["safety_blocker_count"],
            "vision_all_safety_blockers_inactive": control_center_vision_panel["all_safety_blockers_inactive"],
            "screen_plan_ready": True,
            "camera_plan_ready": True,
            "vision_context_ready": True,
            "dependency_check_ready": True,
            "vision_runtime_activation_contract": activation,
            "explicit_screenshot_capture_contract": screenshot,
            "screen_context_adapter_contract": screen_context,
            "local_vision_model_adapter_contract": local_model,
            "vision_permission_redaction_contract": permission_redaction,
            "workspace_visual_understanding_contract": workspace_visual,
            "vision_to_chat_context_handoff_contract": vision_to_chat,
            "control_center_vision_panel_contract": control_center_vision_panel,
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
            "sections": 13,
            "project_root": str(self.project_root),
            "note": "Vision Runtime Alpha is online for Sprint 208 Control Center Vision Panel contract. It defines read-only vision panel status, safety, dependency, permission, redaction, and handoff visibility without rendering panels, creating routes/API endpoints, fetching data, mutating permissions, writing audit events, triggering capture/model/chat controls, uploading externally, or executing commands automatically.",
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
