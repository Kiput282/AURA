
"""Vision input runtime foundation for AURA Genesis.

Foundation-only vision input layer. It prepares metadata-only plans for future
camera permission, screen/image input boundaries, visual source selection,
image adapter planning, visual session flow, and vision safety without
accessing camera, screen capture, files, image runtime, network, commands,
tools, desktop control, or external actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class VisionInputRuntimeFoundationManager:
    """Prepare safe foundation-only vision input runtime plans."""

    name = "vision_input_runtime_foundation"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = Path(project_root)
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}
        with self.identity_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle) or {}

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def vision_input_plan_types(self) -> list[str]:
        return [
            "vision_input_status",
            "vision_input_permission_plan",
            "visual_capture_boundary_plan",
            "image_input_adapter_plan",
            "visual_source_plan",
            "visual_session_plan",
            "visual_action_gate_plan",
            "vision_input_safety_plan",
            "vision_input_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan future camera/screen/image permission flow.",
            "Plan safe visual capture boundaries without capturing images.",
            "Plan image input adapter selection without running vision runtime.",
            "Plan visual source selection for future camera, screenshot, or uploaded image input.",
            "Plan explicit visual sessions instead of always-watching behavior.",
            "Plan action gates for visual requests before future execution.",
            "Keep all outputs foundation-only, planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "camera_access",
            "screen_capture",
            "screenshot_capture",
            "image_capture",
            "video_capture",
            "webcam_runtime",
            "vision_runtime",
            "image_analysis_runtime",
            "object_detection_runtime",
            "ocr_runtime",
            "always_watching",
            "background_watching",
            "visual_command_execution",
            "visual_tool_execution",
            "action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]

    def infer_vision_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "permission": ["permission", "izin", "allow", "grant"],
            "camera": ["camera", "kamera", "webcam"],
            "screen": ["screen", "layar", "screenshot", "desktop"],
            "image": ["image", "gambar", "foto", "picture"],
            "video": ["video", "stream", "frame"],
            "action": ["click", "klik", "buka", "jalankan", "hapus", "ubah", "execute"],
            "privacy": ["private", "sensitive", "privacy", "rahasia"],
            "safety": ["safe", "risk", "aman", "bahaya"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_vision_mode(self, tags: list[str]) -> dict[str, str]:
        if "action" in tags:
            return {
                "mode": "visual_action_permission_gate",
                "focus": "confirm_visual_action_before_future_execution",
                "next_gate": "explicit_confirmation_required",
            }
        if "camera" in tags or "screen" in tags:
            return {
                "mode": "visual_device_permission_planning",
                "focus": "request_camera_or_screen_permission_before_runtime",
                "next_gate": "visual_input_permission_required",
            }
        if "image" in tags or "video" in tags:
            return {
                "mode": "visual_input_adapter_planning",
                "focus": "choose_safe_visual_source_and_adapter_without_runtime",
                "next_gate": "visual_source_review",
            }
        return {
            "mode": "general_vision_input_foundation",
            "focus": "prepare_seeing_foundation_without_device_access",
            "next_gate": "vision_permission_review",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "foundation_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "camera_access": False,
            "screen_capture": False,
            "screenshot_capture": False,
            "image_capture": False,
            "video_capture": False,
            "webcam_runtime": False,
            "vision_runtime": False,
            "image_analysis_runtime": False,
            "object_detection_runtime": False,
            "ocr_runtime": False,
            "always_watching": False,
            "background_watching": False,
            "visual_command_execution": False,
            "visual_tool_execution": False,
            "action_execution": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "internet_search": False,
            "network_action": False,
            "desktop_control": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general vision input foundation"
        tags = self.infer_vision_tags(normalized_target)
        identity = self.load_identity()
        boundary = self.safety_boundary()

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "creator": identity.get("creator", "Kiput"),
            "aura_name": identity.get("name", "AURA"),
            "motto": identity.get("motto", "Grow Together"),
            "essence": "AURA hidup ketika ia bisa berpikir, mendengar, dan melihat",
            "principle": "permission_first_vision_input",
            "tags": tags,
            "vision_mode": self.recommended_vision_mode(tags),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def vision_input_permission_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("vision_input_permission_plan", target)
        plan["permission_steps"] = [
            "Explain why camera, screen, or image access may be needed in a future runtime.",
            "Ask Kiput before enabling any visual input source.",
            "Limit visual input to explicit session scope.",
            "Keep camera, screen capture, and image runtime disabled in this sprint.",
        ]
        plan["permission_prompt_template"] = (
            "Kiput, agar AURA bisa melihat lewat kamera/layar/gambar, "
            "AURA perlu izin visual input terlebih dahulu. Mau aktifkan nanti?"
        )
        return plan

    def visual_capture_boundary_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_capture_boundary_plan", target)
        plan["capture_boundary_steps"] = [
            "Define when visual input may start and stop in a future runtime.",
            "Avoid always-watching behavior by default.",
            "Avoid background screen/camera watching without explicit permission.",
            "Do not capture camera, screen, screenshot, image, or video in this sprint.",
        ]
        return plan

    def image_input_adapter_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("image_input_adapter_plan", target)
        plan["adapter_steps"] = [
            "Plan future adapter choices for uploaded image, screenshot, camera frame, or video frame input.",
            "Prefer explicit user-provided image input before camera/screen access.",
            "Require permission and dependency/download notice before future visual runtime.",
            "Do not run image analysis, OCR, object detection, or vision model runtime in this sprint.",
        ]
        return plan

    def visual_source_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_source_plan", target)
        plan["source_steps"] = [
            "Identify whether the future source is uploaded image, screenshot, screen, camera, webcam, or video frame.",
            "Choose the least invasive source that can answer the request.",
            "Ask permission for camera/screen sources.",
            "Do not read files, capture screen, or access camera in this sprint.",
        ]
        return plan

    def visual_session_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_session_plan", target)
        plan["session_steps"] = [
            "Plan visual session states: idle, permission_requested, active, paused, stopped.",
            "Keep visual session explicit and visible.",
            "Prepare future one-shot image review before continuous visual mode.",
            "Do not enable live watching in this sprint.",
        ]
        return plan

    def visual_action_gate_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_action_gate_plan", target)
        plan["action_gate_steps"] = [
            "Detect whether visual input may lead to an action request.",
            "Separate observation from action.",
            "Require explicit confirmation before future visual command execution.",
            "Block tool, file, command, desktop, internet, network, memory, git, and external action execution.",
        ]
        plan["confirmation_template"] = (
            "Kiput, AURA melihat ini sebagai kemungkinan aksi: <aksi>. "
            "AURA belum akan menjalankan apa pun. Mau lanjut ke rencana aksi?"
        )
        return plan

    def vision_input_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("vision_input_safety_plan", target)
        plan["safety_steps"] = [
            "Never access camera, screen, screenshot, webcam, image capture, or video capture in this sprint.",
            "Never run vision runtime, OCR, image analysis, object detection, or visual command execution.",
            "Never watch continuously or in the background.",
            "Never execute tools, commands, files, desktop actions, internet search, network actions, memory writes, or git operations.",
            "Require explicit permission before future visual input, model runtime, download/install, or visual action execution.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        identity = self.load_identity()
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "identity_version": identity.get("version"),
            "vision_input_plan_types": self.vision_input_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "vision_input_permission_plan_ready": True,
            "visual_capture_boundary_plan_ready": True,
            "image_input_adapter_plan_ready": True,
            "visual_source_plan_ready": True,
            "visual_session_plan_ready": True,
            "visual_action_gate_plan_ready": True,
            "vision_input_safety_plan_ready": True,
            "context_ready": True,
            "vision_input_plan_types": self.vision_input_plan_types(),
            "plan_type_count": len(self.vision_input_plan_types()),
            **boundary,
        }
