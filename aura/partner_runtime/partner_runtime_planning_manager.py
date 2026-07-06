
"""Partner runtime planning layer for AURA Genesis.

Planner-only coordination layer. It does not run autonomous actions,
execute tools, read/write files, control desktop, access devices, or execute commands.
"""
from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import yaml


class PartnerRuntimePlanningManager:
    """Plan safe partner runtime coordination without runtime execution."""

    name = "partner_runtime_planning_layer"
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
                        or status.get("runtime_ready")
                        or status.get("workflow_ready")
                        or status.get("validation_ready")
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
            "local_task_reference": self.safe_import_status([
                ("aura.task_planner.local_task_planner_manager", "LocalTaskPlannerManager"),
                ("aura.local_task.local_task_planner_manager", "LocalTaskPlannerManager"),
            ]),
            "safe_file_operation_reference": self.safe_import_status([
                ("aura.file_ops.safe_file_operation_planner_manager", "SafeFileOperationPlannerManager"),
            ]),
            "codebase_change_reference": self.safe_import_status([
                ("aura.codebase_change.codebase_change_planner_manager", "CodebaseChangePlannerManager"),
            ]),
            "codebase_patch_reference": self.safe_import_status([
                ("aura.codebase_patch_proposal.codebase_patch_proposal_renderer_manager", "CodebasePatchProposalRendererManager"),
            ]),
            "codebase_validation_reference": self.safe_import_status([
                ("aura.codebase_validation.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
                ("aura.codebase_validation_gate.codebase_validation_gate_planner_manager", "CodebaseValidationGatePlannerManager"),
            ]),
            "voice_conversation_reference": self.safe_import_status([
                ("aura.voice_conversation.voice_conversation_planner_manager", "VoiceConversationPlannerManager"),
            ]),
            "vision_context_reference": self.safe_import_status([
                ("aura.vision_context.vision_context_planner_manager", "VisionContextPlannerManager"),
            ]),
            "avatar_interaction_reference": self.safe_import_status([
                ("aura.avatar_interaction.avatar_interaction_planner_manager", "AvatarInteractionPlannerManager"),
            ]),
            "desktop_workflow_reference": self.safe_import_status([
                ("aura.desktop_workflow.desktop_workflow_planner_manager", "DesktopWorkflowPlannerManager"),
            ]),
        }

    def normalize_text(self, text: str) -> str:
        return " ".join(str(text or "").strip().split())

    def partner_plan_types(self) -> list[str]:
        return [
            "partner_runtime_status",
            "partner_runtime_mode_plan",
            "partner_session_plan",
            "partner_multimodal_handoff_plan",
            "partner_tool_permission_plan",
            "partner_growth_cycle_plan",
            "partner_runtime_safety_plan",
            "partner_runtime_context",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "Plan partner runtime mode from metadata only.",
            "Plan session flow without autonomous execution.",
            "Plan handoff between voice, vision, avatar, desktop, and codebase planners.",
            "Plan tool permission gates without using tools.",
            "Plan growth-cycle review checkpoints.",
            "Keep all outputs planner-only, proposal-only, and human-reviewable.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "autonomous_runtime",
            "background_agent_loop",
            "scheduled_self_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "desktop_control",
            "app_opening",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "network_action",
            "git_commit",
            "git_push",
        ]

    def infer_partner_tags(self, target: str) -> list[str]:
        target_lower = self.normalize_text(target).lower()
        tags: list[str] = []

        keyword_map = {
            "coding": ["code", "repo", "sprint", "patch", "commit", "validation"],
            "voice": ["voice", "talk", "conversation", "speech"],
            "vision": ["vision", "screen", "camera", "image"],
            "avatar": ["avatar", "character", "gesture", "expression"],
            "desktop": ["desktop", "app", "window", "workflow"],
            "files": ["file", "folder", "document"],
            "streaming": ["stream", "obs", "live"],
            "growth": ["memory", "learn", "roadmap", "checkpoint", "review"],
            "safety": ["permission", "risk", "safe", "private", "sensitive"],
        }

        for tag, keywords in keyword_map.items():
            if any(keyword in target_lower for keyword in keywords):
                tags.append(tag)

        if not tags:
            tags.append("general")

        return tags

    def recommended_partner_mode(self, tags: list[str]) -> dict[str, str]:
        if "coding" in tags:
            return {
                "mode": "developer_partner_planning",
                "focus": "plan_patch_validate_commit_sequence",
                "handoff": "codebase_and_desktop_planners",
                "permission_gate": "required_before_execution",
            }
        if "streaming" in tags or "avatar" in tags:
            return {
                "mode": "streaming_avatar_partner_planning",
                "focus": "presence_expression_and_safety",
                "handoff": "voice_vision_avatar_desktop_planners",
                "permission_gate": "required_before_runtime",
            }
        if "growth" in tags:
            return {
                "mode": "growth_checkpoint_planning",
                "focus": "review_progress_and_next_roadmap",
                "handoff": "journal_memory_and_roadmap_discussion",
                "permission_gate": "human_review",
            }
        return {
            "mode": "general_partner_runtime_planning",
            "focus": "safe_session_coordination",
            "handoff": "best_available_planner",
            "permission_gate": "ask_before_action",
        }

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "autonomous_runtime": False,
            "background_agent_loop": False,
            "scheduled_self_execution": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "file_read": False,
            "file_write": False,
            "command_execution": False,
            "desktop_control": False,
            "app_opening": False,
            "screen_capture": False,
            "camera_access": False,
            "microphone_access": False,
            "speaker_output": False,
            "avatar_rendering": False,
            "network_action": False,
            "git_commit": False,
            "git_push": False,
        }

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "general partner runtime planning"
        tags = self.infer_partner_tags(normalized_target)
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
            "codename": identity.get("codename", "Genesis"),
            "tags": tags,
            "partner_mode": self.recommended_partner_mode(tags),
            "integration_context": self.integration_context(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def partner_runtime_mode_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_runtime_mode_plan", target)
        plan["mode_steps"] = [
            "Identify the intended partner mode from metadata.",
            "Select a safe planner handoff path.",
            "Separate planning from runtime execution.",
            "Require explicit permission before any future runtime action.",
        ]
        return plan

    def partner_session_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_session_plan", target)
        plan["session_steps"] = [
            "Clarify the user goal and active context.",
            "Choose relevant planners for voice, vision, avatar, desktop, file, or codebase flow.",
            "Return a human-reviewable session sequence.",
            "Do not execute actions, tools, commands, file operations, device access, or git operations.",
        ]
        return plan

    def partner_multimodal_handoff_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_multimodal_handoff_plan", target)
        plan["handoff_steps"] = [
            "Map user intent to voice, vision, avatar, desktop, and codebase planners.",
            "Keep all cross-system handoffs as metadata only.",
            "Avoid accessing microphone, camera, screen, desktop, avatar runtime, files, or tools.",
            "Prepare future permission gates for each runtime handoff.",
        ]
        return plan

    def partner_tool_permission_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_tool_permission_plan", target)
        plan["permission_steps"] = [
            "Identify which tools would be needed in a future runtime.",
            "Mark all tool usage as disabled in this sprint.",
            "Require human confirmation before file, command, desktop, network, git, or device action.",
            "Keep the output as a permission review plan only.",
        ]
        return plan

    def partner_growth_cycle_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_growth_cycle_plan", target)
        plan["growth_steps"] = [
            "Summarize completed planner capabilities.",
            "Identify foundation-only features that are not runtime-active.",
            "Identify active planner integrations and safety boundaries.",
            "Prepare roadmap discussion for the next sprint block.",
        ]
        return plan

    def partner_runtime_safety_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("partner_runtime_safety_plan", target)
        plan["safety_steps"] = [
            "Never run autonomous background loops in this sprint.",
            "Never execute tools, commands, file operations, desktop actions, network actions, or git operations.",
            "Never access microphone, speaker output, camera, screen capture, or avatar rendering.",
            "Never perform real tool execution automatically.",
            "Require explicit future permission before any runtime action.",
            "Keep partner runtime planning local-first, permission-first, and proposal-only.",
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
            "partner_plan_types": self.partner_plan_types(),
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
            "partner_runtime_mode_plan_ready": True,
            "partner_session_plan_ready": True,
            "partner_multimodal_handoff_plan_ready": True,
            "partner_tool_permission_plan_ready": True,
            "partner_growth_cycle_plan_ready": True,
            "partner_runtime_safety_plan_ready": True,
            "context_ready": True,
            "partner_plan_types": self.partner_plan_types(),
            "plan_type_count": len(self.partner_plan_types()),
            "local_task_reference_ready": True,
            "safe_file_operation_reference_ready": True,
            "codebase_change_reference_ready": True,
            "codebase_patch_reference_ready": True,
            "codebase_validation_reference_ready": True,
            "voice_conversation_reference_ready": True,
            "vision_context_reference_ready": True,
            "avatar_interaction_reference_ready": True,
            "desktop_workflow_reference_ready": True,
            "local_task_manager_found": integrations["local_task_reference"]["found"],
            "safe_file_operation_manager_found": integrations["safe_file_operation_reference"]["found"],
            "codebase_change_manager_found": integrations["codebase_change_reference"]["found"],
            "codebase_patch_manager_found": integrations["codebase_patch_reference"]["found"],
            "codebase_validation_manager_found": integrations["codebase_validation_reference"]["found"],
            "voice_conversation_manager_found": integrations["voice_conversation_reference"]["found"],
            "vision_context_manager_found": integrations["vision_context_reference"]["found"],
            "avatar_interaction_manager_found": integrations["avatar_interaction_reference"]["found"],
            "desktop_workflow_manager_found": integrations["desktop_workflow_reference"]["found"],
            **boundary,
        }
