
"""Avatar interaction planner for AURA Genesis.

Planner-only layer. It does not render an avatar, play animation,
access motion capture, manipulate rigs, write files, or execute Blender.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class AvatarInteractionPlannerManager:
    """Plan safe avatar interaction behavior without avatar runtime execution."""

    name = "avatar_interaction_planner"
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

    def safe_import_status(self, candidates: list[tuple[str, str]]) -> dict[str, Any]:
        for module_name, class_name in candidates:
            try:
                module = importlib.import_module(module_name)
                manager_class = getattr(module, class_name)
                manager = manager_class(project_root=self.project_root)
                status = manager.status() if hasattr(manager, "status") else {}
                return {
                    "found": True,
                    "module": module_name,
                    "class": class_name,
                    "status": status.get("status", "available"),
                    "ready": bool(
                        status.get("planner_ready")
                        or status.get("context_ready")
                        or status.get("bridge_ready")
                        or status.get("expression_language_ready")
                        or status.get("renderer_ready")
                    ),
                }
            except Exception:
                continue

        return {
            "found": False,
            "module": None,
            "class": None,
            "status": "not_found",
            "ready": False,
        }

    def integration_context(self) -> dict[str, Any]:
        return {
            "expression_language_reference": self.safe_import_status([
                ("aura.expression.expression_language_manager", "ExpressionLanguageManager"),
                ("aura.expression.expression_language_runtime_manager", "ExpressionLanguageManager"),
            ]),
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "vision_context_reference": self.safe_import_status([
                ("aura.vision_context.vision_context_planner_manager", "VisionContextPlannerManager"),
            ]),
            "blender_bridge_reference": self.safe_import_status([
                ("aura.blender.blender_bridge_manager", "BlenderBridgeManager"),
                ("aura.blender_bridge.blender_bridge_manager", "BlenderBridgeManager"),
            ]),
            "creative_assistant_reference": self.safe_import_status([
                ("aura.creative.creative_assistant_manager", "CreativeAssistantManager"),
                ("aura.creative_assistant.creative_assistant_manager", "CreativeAssistantManager"),
            ]),
            "streaming_safety_reference": self.safe_import_status([
                ("aura.streaming.streaming_safety_manager", "StreamingSafetyManager"),
                ("aura.streaming_safety.streaming_safety_manager", "StreamingSafetyManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def avatar_plan_types(self) -> list[str]:
        return [
            "avatar_interaction_status",
            "avatar_expression_plan",
            "avatar_gesture_plan",
            "avatar_pose_plan",
            "avatar_streaming_presence_plan",
            "avatar_safety_plan",
            "avatar_interaction_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan avatar expressions from metadata only.",
            "Plan avatar gestures without animation playback.",
            "Plan avatar pose intent without rig manipulation.",
            "Plan streaming presence behavior without OBS or runtime avatar control.",
            "Connect avatar interaction with voice and vision planners.",
            "Keep all outputs planner-only and proposal-only.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "avatar_rendering",
            "animation_playback",
            "mocap_runtime",
            "camera_tracking",
            "face_tracking",
            "body_tracking",
            "rig_manipulation",
            "blendshape_control",
            "bone_control",
            "blender_execution",
            "obs_control",
            "desktop_action_execution",
            "app_opening",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]

    def infer_avatar_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "expression": ["expression", "face", "smile", "sad", "happy", "angry", "surprised"],
            "gesture": ["gesture", "wave", "point", "nod", "hand", "reaction"],
            "pose": ["pose", "idle", "stand", "sit", "body", "posture"],
            "streaming": ["stream", "live", "obs", "viewer", "chat"],
            "gaming": ["game", "gaming", "match", "boss", "quest"],
            "coding": ["code", "coding", "terminal", "sprint", "repo"],
            "creative": ["avatar", "character", "model", "blender", "texture", "outfit"],
            "safety": ["private", "sensitive", "permission", "risk", "unsafe"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_avatar_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "mode": "minimal_supportive_presence",
                "expression": "focused_friendly",
                "movement": "low_motion",
                "verbosity": "do_not_distract",
            }
        if "streaming" in tags:
            return {
                "mode": "expressive_stream_presence",
                "expression": "friendly_responsive",
                "movement": "moderate_reactive",
                "verbosity": "not_annoying",
            }
        if "gaming" in tags:
            return {
                "mode": "playful_companion_presence",
                "expression": "energetic_supportive",
                "movement": "quick_reaction",
                "verbosity": "short_reactive",
            }
        if "creative" in tags:
            return {
                "mode": "design_review_presence",
                "expression": "curious_supportive",
                "movement": "calm_observational",
                "verbosity": "structured",
            }
        return {
            "mode": "general_partner_presence",
            "expression": "friendly_neutral",
            "movement": "subtle",
            "verbosity": "balanced",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "avatar_rendering": False,
            "animation_playback": False,
            "mocap_runtime": False,
            "camera_tracking": False,
            "face_tracking": False,
            "body_tracking": False,
            "rig_manipulation": False,
            "blendshape_control": False,
            "bone_control": False,
            "blender_execution": False,
            "obs_control": False,
            "desktop_action_execution": False,
            "app_opened": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general avatar interaction"
        tags = self.infer_avatar_tags(normalized_target)
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
            "tags": tags,
            "avatar_mode": self.recommended_avatar_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def avatar_expression_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("avatar_expression_plan", target)
        plan["expression_steps"] = [
            "Infer intended emotional tone from metadata.",
            "Choose a safe expression category such as neutral, focused, happy, curious, surprised, or supportive.",
            "Keep expression as a planned metadata label only.",
            "Do not control blendshapes, face tracking, rendering, or avatar runtime.",
        ]
        return plan

    def avatar_gesture_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("avatar_gesture_plan", target)
        plan["gesture_steps"] = [
            "Identify whether a gesture would support the interaction.",
            "Choose a subtle non-distracting gesture style.",
            "Keep gesture output as descriptive metadata only.",
            "Do not play animations, control bones, or execute avatar runtime actions.",
        ]
        return plan

    def avatar_pose_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("avatar_pose_plan", target)
        plan["pose_steps"] = [
            "Identify whether the avatar should feel idle, focused, presenting, playful, or supportive.",
            "Map the pose to a metadata-only pose intent.",
            "Avoid rig, bone, blendshape, Blender, or file operations.",
            "Require future explicit runtime permission before pose execution.",
        ]
        return plan

    def avatar_streaming_presence_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("avatar_streaming_presence_plan", target)
        plan["presence_steps"] = [
            "Plan how AURA should behave as a stream companion without controlling OBS.",
            "Keep reactions expressive but not annoying.",
            "Avoid excessive motion during serious coding or focus work.",
            "Return only metadata for future avatar runtime handoff.",
        ]
        return plan

    def avatar_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("avatar_safety_plan", target)
        plan["safety_steps"] = [
            "Never render or animate the avatar in this planner sprint.",
            "Never access mocap, camera tracking, face tracking, or body tracking.",
            "Never manipulate rigs, bones, blendshapes, Blender, OBS, files, desktop, or external tools.",
            "Never execute commands or runtime avatar actions automatically.",
            "Require explicit permission before any future avatar runtime execution.",
            "Keep avatar planning local-first, permission-first, and proposal-only.",
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
            "avatar_plan_types": self.avatar_plan_types(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "integration_context": self.integration_context(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        integrations = self.integration_context()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "avatar_expression_plan_ready": True,
            "avatar_gesture_plan_ready": True,
            "avatar_pose_plan_ready": True,
            "avatar_streaming_presence_plan_ready": True,
            "avatar_safety_plan_ready": True,
            "context_ready": True,
            "avatar_plan_types": self.avatar_plan_types(),
            "plan_type_count": len(self.avatar_plan_types()),
            "expression_language_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "vision_context_reference_ready": True,
            "blender_bridge_reference_ready": True,
            "creative_assistant_reference_ready": True,
            "streaming_safety_reference_ready": True,
            "expression_language_manager_found": integrations["expression_language_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "vision_context_manager_found": integrations["vision_context_reference"]["found"],
            "blender_bridge_manager_found": integrations["blender_bridge_reference"]["found"],
            "creative_assistant_manager_found": integrations["creative_assistant_reference"]["found"],
            "streaming_safety_manager_found": integrations["streaming_safety_reference"]["found"],
            **boundary,
        }
