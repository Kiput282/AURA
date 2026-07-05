from pathlib import Path
from typing import Any

import yaml

from aura.blender.blender_bridge_foundation_manager import BlenderBridgeFoundationManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class CreativeAssistantFoundationManager:
    """
    AURA Creative Assistant Foundation.

    Current phase:
    - prepare creative briefs
    - prepare character concept plans
    - prepare visual asset plans
    - prepare content idea plans
    - prepare creative review plans
    - integrate project intent planner, workspace memory link, media understanding, expression language, and Blender bridge
    - never generates images automatically
    - never opens media files automatically
    - never writes files automatically
    - never executes commands automatically
    """

    name = "creative_assistant_foundation"
    version = "0.1.0"
    status_name = "foundation"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.project_intent = ProjectIntentPlannerManager(project_root=self.project_root)
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.media_understanding = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.expression_language = ExpressionLanguageManager(project_root=self.project_root)
        self.blender_bridge = BlenderBridgeFoundationManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())

        if len(normalized) > 500:
            return normalized[:500].rstrip() + "..."

        return normalized

    def creative_plan_types(self) -> list[str]:
        return [
            "creative_brief",
            "character_concept",
            "visual_asset",
            "content_idea",
            "creative_review",
            "style_alignment",
            "safety_boundary",
        ]

    def infer_creative_tags(self, text: str) -> list[str]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "aura": "aura_brand",
            "virtual": "virtual_identity",
            "avatar": "character_design",
            "character": "character_design",
            "chibi": "character_design",
            "banner": "visual_asset",
            "youtube": "platform_content",
            "stream": "streaming_content",
            "streaming": "streaming_content",
            "content": "content_idea",
            "idea": "content_idea",
            "visual": "visual_asset",
            "asset": "visual_asset",
            "design": "design_review",
            "review": "design_review",
            "consistency": "style_consistency",
            "blender": "3d_asset",
            "texture": "texture_planning",
            "safe": "safety",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["creative_planning", "aura_brand"])

        return tags[:8]

    def creative_direction(self, target: str) -> dict[str, Any]:
        tags = self.infer_creative_tags(target)

        if "character_design" in tags:
            focus = "character_identity"
        elif "visual_asset" in tags:
            focus = "visual_brand_asset"
        elif "streaming_content" in tags:
            focus = "streaming_channel_content"
        elif "design_review" in tags or "style_consistency" in tags:
            focus = "creative_consistency_review"
        else:
            focus = "creative_foundation"

        return {
            "focus": focus,
            "tags": tags,
            "brand_anchor": "AURA Virtual / Grow Together / Genesis",
            "safety_priority": "proposal_only_no_generation_no_file_write",
        }

    def integration_context(self) -> dict[str, Any]:
        return {
            "project_intent_status": self.project_intent.status(),
            "project_intent_summary": self.project_intent.summary("creative assistant foundation"),
            "workspace_memory_summary": self.workspace_memory_link.summary(),
            "media_status": self.media_understanding.status(),
            "media_asset_summary": self.media_understanding.asset_summary(),
            "expression_status": self.expression_language.status(),
            "expression_state": self.expression_language.expression_state(),
            "blender_status": self.blender_bridge.status(),
            "blender_asset_summary": self.blender_bridge.asset_summary(),
        }

    def base_plan(
        self,
        plan_type: str,
        target: str,
        recommended_steps: list[str],
        creative_outputs: list[str],
    ) -> dict[str, Any]:
        cleaned_target = self.normalize_text(target) or "<unspecified>"
        context = self.integration_context()
        direction = self.creative_direction(cleaned_target)

        read_project_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_file_permission = self.permission_manager.check("open_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        expression_plan = self.expression_language.expression_plan(cleaned_target)

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "creative_direction": direction,
            "creative_outputs": creative_outputs,
            "creative_output_count": len(creative_outputs),
            "project_intent_summary": context["project_intent_summary"]["summary"],
            "workspace_memory_summary": context["workspace_memory_summary"]["summary"],
            "media_candidate_count": context["media_asset_summary"]["candidate_count"],
            "media_metadata_only": context["media_asset_summary"]["metadata_only"],
            "expression_plan": expression_plan,
            "expression_mood": expression_plan["mood"],
            "expression_tags": expression_plan["emotion_tags"],
            "blender_asset_candidate_count": context["blender_asset_summary"]["candidate_count"],
            "recommended_steps": recommended_steps,
            "permissions": {
                "read_project": read_project_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "open_file": open_file_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "proposal_only": True,
            "read_only": True,
            "image_generation_performed": False,
            "media_file_opened": False,
            "pixel_read": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Creative assistant plan is proposal-only.",
                "No image was generated.",
                "No media file was opened.",
                "No image pixels were read.",
                "No file was written.",
                "No command was executed.",
                "Future real generation, media opening, or file writing must go through explicit confirmation.",
            ],
        }

    def brief_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="creative_brief",
            target=target,
            creative_outputs=[
                "brand intent",
                "audience direction",
                "style keywords",
                "asset needs",
                "safety boundary",
            ],
            recommended_steps=[
                "Clarify creative purpose, audience, platform, and tone.",
                "Anchor the concept to AURA Virtual, Grow Together, and Genesis.",
                "Identify required assets without generating or opening files.",
                "Plan mood, style, colors, and usage constraints.",
                "Keep image generation, file writing, and commands disabled.",
            ],
        )

    def character_concept_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="character_concept",
            target=target,
            creative_outputs=[
                "character identity",
                "silhouette notes",
                "hair and face notes",
                "outfit/accessory direction",
                "expression and gesture hints",
            ],
            recommended_steps=[
                "Define the character role and personality traits.",
                "Plan silhouette, face, hairstyle, color language, outfit, and accessories.",
                "Connect expression hints to AURA's expression language.",
                "Connect future 3D planning to Blender Bridge without opening Blender.",
                "Keep generated images, texture writing, and avatar changes disabled.",
            ],
        )

    def visual_asset_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="visual_asset",
            target=target,
            creative_outputs=[
                "asset list",
                "layout direction",
                "safe area notes",
                "brand consistency notes",
                "future export checklist",
            ],
            recommended_steps=[
                "Clarify target asset type: banner, avatar, thumbnail, overlay, logo, or texture.",
                "Plan layout, composition, readability, safe areas, and platform constraints.",
                "Use media understanding metadata only for asset awareness.",
                "Prepare review criteria before any image generation or editing.",
                "Keep media opening, image generation, file writing, and commands disabled.",
            ],
        )

    def content_idea_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="content_idea",
            target=target,
            creative_outputs=[
                "content pillars",
                "stream segment ideas",
                "short-form ideas",
                "audience interaction ideas",
                "tone and boundary notes",
            ],
            recommended_steps=[
                "Clarify channel identity, target audience, and platform.",
                "Prepare content pillars that match AURA's personality and safety boundaries.",
                "Plan streaming-friendly segments without reading live chat automatically.",
                "Connect content tone to expression language hints.",
                "Keep posting, browser opening, file writing, and command execution disabled.",
            ],
        )

    def review_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="creative_review",
            target=target,
            creative_outputs=[
                "consistency checklist",
                "brand alignment checklist",
                "character design checklist",
                "asset quality checklist",
                "revision questions",
            ],
            recommended_steps=[
                "Clarify what is being reviewed and what success means.",
                "Check consistency across character identity, colors, hairstyle, outfit, logo, and channel assets.",
                "Prepare questions before requiring visual file opening.",
                "Use media metadata only unless user explicitly approves image review.",
                "Keep edits, file writes, and commands disabled.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()
        integration = self.integration_context()

        return {
            "status": self.status_name,
            "context_ready": True,
            "creative_status": status,
            "identity": self.load_identity(),
            "project_intent_context": self.project_intent.context(),
            "workspace_memory_context": self.workspace_memory_link.context(),
            "media_context": self.media_understanding.context(),
            "expression_context": self.expression_language.context(),
            "blender_context": self.blender_bridge.context(),
            "integration_summary": {
                "project_intent_ready": integration["project_intent_status"]["intent_ready"],
                "workspace_memory_ready": self.workspace_memory_link.status()["link_ready"],
                "media_understanding_ready": integration["media_status"]["understanding_ready"],
                "expression_language_ready": integration["expression_status"]["language_ready"],
                "blender_bridge_ready": integration["blender_status"]["bridge_ready"],
            },
            "safe_current_capabilities": [
                "creative_assistant_status",
                "creative_brief_plan",
                "creative_character_concept_plan",
                "creative_visual_asset_plan",
                "creative_content_idea_plan",
                "creative_review_plan",
                "creative_context",
            ],
            "disabled_capabilities": [
                "automatic_image_generation",
                "automatic_media_file_open",
                "automatic_pixel_read",
                "automatic_file_write",
                "command_execution",
                "external_action_execution",
            ],
            "read_only": True,
            "proposal_only": True,
            "write_performed": False,
            "image_generation_performed": False,
            "media_file_opened": False,
            "pixel_read": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Creative Assistant Foundation context is read-only and proposal-only.",
        }

    def status(self) -> dict[str, Any]:
        project_intent_status = self.project_intent.status()
        workspace_memory_status = self.workspace_memory_link.status()
        media_status = self.media_understanding.status()
        expression_status = self.expression_language.status()
        blender_status = self.blender_bridge.status()

        read_project_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_file_permission = self.permission_manager.check("open_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "assistant_ready": True,
            "brief_plan_ready": True,
            "character_concept_ready": True,
            "visual_asset_plan_ready": True,
            "content_idea_plan_ready": True,
            "review_plan_ready": True,
            "context_ready": True,
            "project_intent_integration_ready": project_intent_status["intent_ready"],
            "workspace_memory_link_integration_ready": workspace_memory_status["link_ready"],
            "media_understanding_integration_ready": media_status["understanding_ready"],
            "expression_language_integration_ready": expression_status["language_ready"],
            "blender_bridge_integration_ready": blender_status["bridge_ready"],
            "creative_plan_types": len(self.creative_plan_types()),
            "media_candidate_count": media_status["candidate_count"],
            "blender_asset_candidate_count": blender_status["asset_candidate_count"],
            "expression_mood_states": expression_status["mood_states"],
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_open_file_confirmation": open_file_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "proposal_only": True,
            "image_generation": False,
            "media_file_opened": False,
            "pixel_read": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Creative Assistant Foundation is online for safe creative planning. It does not generate images, open media files, write files, execute commands, or perform external actions automatically.",
        }
