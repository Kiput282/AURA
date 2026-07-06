
"""Visual context understanding layer for AURA Genesis.

Planner-only layer for future visual context understanding. It prepares how
AURA should understand scene context, objects, relations, text-in-image
intent, uncertainty, clarification needs, and safe visual response planning
without camera access, screen capture, image analysis runtime, OCR runtime,
object detection runtime, face recognition, command execution, tool
execution, file operations, network actions, desktop control, or external
actions.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class VisualContextUnderstandingManager:
    """Prepare safe planner-only visual context understanding plans."""

    name = "visual_context_understanding"
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

    def visual_context_plan_types(self) -> list[str]:
        return [
            "visual_context_status",
            "visual_scene_understanding_plan",
            "visual_object_relation_plan",
            "visual_text_context_plan",
            "visual_uncertainty_plan",
            "visual_clarification_plan",
            "visual_response_context_plan",
            "visual_context_safety_plan",
            "visual_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan future scene/context understanding from visual input metadata.",
            "Plan future object and relation understanding without object detection runtime.",
            "Plan future text-in-image/OCR interpretation without OCR runtime.",
            "Plan visual uncertainty handling and confidence boundaries.",
            "Plan clarification questions when visual context is ambiguous.",
            "Plan safe visual responses without acting on visual observations.",
            "Keep all outputs planner-only, proposal-only, metadata-only, and human-reviewable.",
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
            "visual_context_runtime",
            "image_analysis_runtime",
            "object_detection_runtime",
            "ocr_runtime",
            "image_text_extraction_runtime",
            "face_recognition",
            "biometric_identification",
            "identity_recognition",
            "emotion_inference_from_face",
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

    def infer_visual_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "scene": ["scene", "situasi", "konteks", "ruangan", "environment", "sekitar"],
            "object": ["object", "objek", "barang", "benda", "item"],
            "relation": ["relation", "hubungan", "posisi", "di atas", "di bawah", "sebelah"],
            "text": ["text", "teks", "ocr", "tulisan", "label", "caption"],
            "uncertainty": ["unclear", "ambigu", "tidak jelas", "blur", "buram", "mungkin"],
            "person": ["person", "orang", "wajah", "face", "manusia"],
            "action": ["click", "klik", "buka", "jalankan", "hapus", "ubah", "execute"],
            "safety": ["safe", "risk", "aman", "bahaya", "private", "privacy", "rahasia"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_visual_mode(self, tags: list[str]) -> dict[str, str]:
        if "person" in tags:
            return {
                "mode": "visual_person_safety_boundary",
                "focus": "avoid_identity_face_biometric_or_sensitive_inference",
                "next_gate": "person_image_safety_review",
            }
        if "action" in tags:
            return {
                "mode": "visual_action_gate",
                "focus": "separate_visual_observation_from_future_action",
                "next_gate": "explicit_confirmation_required",
            }
        if "uncertainty" in tags:
            return {
                "mode": "visual_uncertainty_review",
                "focus": "state_limits_and_request_clarification",
                "next_gate": "clarification_required",
            }
        if "text" in tags:
            return {
                "mode": "visual_text_context_planning",
                "focus": "plan_text_in_image_interpretation_without_ocr_runtime",
                "next_gate": "ocr_runtime_permission_required",
            }
        if "scene" in tags or "object" in tags or "relation" in tags:
            return {
                "mode": "visual_context_planning",
                "focus": "plan_scene_object_relation_understanding_without_runtime",
                "next_gate": "visual_input_required",
            }
        return {
            "mode": "general_visual_context_understanding",
            "focus": "prepare_safe_visual_context_reasoning_without_image_runtime",
            "next_gate": "visual_context_review",
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
            "visual_context_runtime": False,
            "image_analysis_runtime": False,
            "object_detection_runtime": False,
            "ocr_runtime": False,
            "image_text_extraction_runtime": False,
            "face_recognition": False,
            "biometric_identification": False,
            "identity_recognition": False,
            "emotion_inference_from_face": False,
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
        normalized_target = self.normalize_text(target) or "general visual context understanding"
        tags = self.infer_visual_tags(normalized_target)
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
            "principle": "observe_understand_clarify_before_action",
            "tags": tags,
            "visual_mode": self.recommended_visual_mode(tags),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def visual_scene_understanding_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_scene_understanding_plan", target)
        plan["scene_steps"] = [
            "Plan how to describe visible scene context when future visual input is explicitly provided.",
            "Separate observation, interpretation, and uncertainty.",
            "Avoid claiming details that are not visible or not provided.",
            "Do not access camera, screen, screenshot, image, video, or vision runtime in this sprint.",
        ]
        return plan

    def visual_object_relation_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_object_relation_plan", target)
        plan["object_relation_steps"] = [
            "Plan how to identify object categories from future visual input without object detection runtime.",
            "Plan spatial relation language such as near, beside, above, below, inside, and behind.",
            "Mark uncertain object or relation claims as uncertain.",
            "Do not run object detection, image analysis, OCR, or visual runtime in this sprint.",
        ]
        return plan

    def visual_text_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_text_context_plan", target)
        plan["text_context_steps"] = [
            "Plan future text-in-image/OCR interpretation only after explicit visual input and permission.",
            "Separate exact readable text from inferred meaning.",
            "Ask clarification when text is blurry, cropped, hidden, or incomplete.",
            "Do not run OCR, image text extraction, file read, screenshot capture, or vision runtime in this sprint.",
        ]
        return plan

    def visual_uncertainty_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_uncertainty_plan", target)
        plan["uncertainty_steps"] = [
            "Plan how to state visual uncertainty clearly.",
            "Use confidence labels such as visible, likely, unclear, not enough evidence, and not visible.",
            "Ask follow-up questions when visual context is ambiguous.",
            "Avoid overclaiming identity, emotion, hidden intent, private details, or unavailable visual evidence.",
        ]
        return plan

    def visual_clarification_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_clarification_plan", target)
        plan["clarification_steps"] = [
            "Ask what visual source should be used in a future runtime.",
            "Ask whether the user wants scene description, object relation, text interpretation, or action planning.",
            "Ask for a clearer image or more context when visual details are insufficient.",
            "Do not proceed to action planning without explicit confirmation.",
        ]
        return plan

    def visual_response_context_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_response_context_plan", target)
        plan["response_steps"] = [
            "Plan concise visual responses that separate what is visible from what is inferred.",
            "Mention uncertainty and missing information naturally.",
            "Offer safe next steps without executing them.",
            "Avoid identity recognition, biometric inference, emotion-from-face claims, or sensitive personal inference.",
        ]
        return plan

    def visual_context_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("visual_context_safety_plan", target)
        plan["safety_steps"] = [
            "Never access camera, screen, screenshot, image capture, video capture, webcam, or visual runtime in this sprint.",
            "Never run image analysis, object detection, OCR, image text extraction, face recognition, biometric identification, or identity recognition.",
            "Never watch continuously or in the background.",
            "Never execute visual commands, tools, files, commands, desktop actions, internet search, network actions, memory writes, git operations, or external actions.",
            "Require explicit permission before future visual input, runtime, dependency download/install, or visual action execution.",
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
            "visual_context_plan_types": self.visual_context_plan_types(),
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
            "visual_scene_understanding_plan_ready": True,
            "visual_object_relation_plan_ready": True,
            "visual_text_context_plan_ready": True,
            "visual_uncertainty_plan_ready": True,
            "visual_clarification_plan_ready": True,
            "visual_response_context_plan_ready": True,
            "visual_context_safety_plan_ready": True,
            "context_ready": True,
            "visual_context_plan_types": self.visual_context_plan_types(),
            "plan_type_count": len(self.visual_context_plan_types()),
            **boundary,
        }
