from pathlib import Path
from typing import Any

import yaml

from aura.creative.creative_assistant_foundation_manager import CreativeAssistantFoundationManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class LocalTaskPlannerAlphaManager:
    """
    AURA Local Task Planner Alpha.

    Current phase:
    - prepare local task intent plans
    - prepare task breakdown plans
    - prepare task risk reviews
    - prepare task execution checklists
    - prepare local task context
    - integrate project intent planner, creative assistant, workspace memory link, and tool sandbox
    - never executes commands automatically
    - never writes files automatically
    - never opens apps automatically
    - never performs desktop actions automatically
    """

    name = "local_task_planner_alpha"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.project_intent = ProjectIntentPlannerManager(project_root=self.project_root)
        self.creative_assistant = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)

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

    def task_plan_types(self) -> list[str]:
        return [
            "task_intent",
            "task_breakdown",
            "task_risk_review",
            "task_execution_checklist",
            "task_context",
            "safety_boundary",
        ]

    def infer_task_tags(self, text: str) -> list[str]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "sprint": "sprint",
            "project": "project",
            "code": "coding",
            "coding": "coding",
            "creative": "creative",
            "asset": "creative",
            "file": "file_operation",
            "write": "file_operation",
            "command": "command",
            "shell": "command",
            "desktop": "desktop",
            "app": "desktop",
            "open": "desktop",
            "risk": "risk",
            "safe": "safety",
            "safety": "safety",
            "task": "task",
            "plan": "planning",
            "checklist": "checklist",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["task", "planning"])

        return tags[:8]

    def task_priority(self, tags: list[str]) -> str:
        if "safety" in tags or "risk" in tags or "command" in tags or "desktop" in tags or "file_operation" in tags:
            return "safety_first_task_planning"

        if "sprint" in tags or "coding" in tags:
            return "implementation_task_planning"

        if "creative" in tags:
            return "creative_task_planning"

        return "local_task_planning"

    def integration_context(self, target: str) -> dict[str, Any]:
        return {
            "project_intent_status": self.project_intent.status(),
            "project_intent_summary": self.project_intent.summary(target),
            "creative_status": self.creative_assistant.status(),
            "creative_brief": self.creative_assistant.brief_plan(target),
            "workspace_memory_status": self.workspace_memory_link.status(),
            "workspace_memory_summary": self.workspace_memory_link.summary(),
            "tool_sandbox_status": self.tool_sandbox.status(),
            "tool_sandbox_dry_run": self.tool_sandbox.dry_run("echo local-task-planner-dry-run"),
        }

    def build_step(self, title: str, description: str, risk: str = "low") -> dict[str, Any]:
        return {
            "title": title,
            "description": description,
            "risk": risk,
            "ready": True,
            "requires_confirmation": risk in {"medium", "high"},
            "executed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "app_opened": False,
            "desktop_action_performed": False,
        }

    def base_plan(
        self,
        plan_type: str,
        target: str,
        recommended_steps: list[dict[str, Any]],
        checklist: list[str],
    ) -> dict[str, Any]:
        cleaned_target = self.normalize_text(target) or "<unspecified>"
        tags = self.infer_task_tags(cleaned_target)
        context = self.integration_context(cleaned_target)

        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "task_tags": tags,
            "task_priority": self.task_priority(tags),
            "project_intent_summary": context["project_intent_summary"]["summary"],
            "creative_brief_focus": context["creative_brief"]["creative_direction"]["focus"],
            "workspace_memory_summary": context["workspace_memory_summary"]["summary"],
            "tool_sandbox_ready": context["tool_sandbox_status"]["sandbox_ready"],
            "tool_sandbox_dry_run_ready": context["tool_sandbox_dry_run"]["dry_run_ready"],
            "tool_sandbox_real_execution_ready": context["tool_sandbox_status"]["real_execution_ready"],
            "recommended_steps": recommended_steps,
            "step_count": len(recommended_steps),
            "checklist": checklist,
            "checklist_count": len(checklist),
            "permissions": {
                "read_project": read_project_permission.to_dict(),
                "read_memory": read_memory_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "open_app": open_app_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "proposal_only": True,
            "read_only": True,
            "file_write_performed": False,
            "command_execution_performed": False,
            "app_opened": False,
            "desktop_action_performed": False,
            "external_action_execution_performed": False,
            "real_tool_execution_performed": False,
            "safety_notes": [
                "Local task plan is proposal-only.",
                "No command was executed.",
                "No file was written.",
                "No app was opened.",
                "No desktop action was performed.",
                "Tool sandbox was used for planning metadata only.",
                "Future real execution must go through explicit confirmation.",
            ],
        }

    def task_intent_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="task_intent_plan",
            target=target,
            recommended_steps=[
                self.build_step("Clarify task outcome", "Define the task result in one clear sentence."),
                self.build_step("Map task context", "Connect task to project intent, creative context, and workspace memory."),
                self.build_step("Identify safety boundary", "Mark whether the task could write files, run commands, or open apps.", "medium"),
                self.build_step("Prepare only", "Keep the task in planning mode until explicit execution approval."),
            ],
            checklist=[
                "Task goal is clear.",
                "Task context is known.",
                "Risky actions are identified.",
                "No command is executed.",
                "No file is written.",
                "No app is opened.",
            ],
        )

    def task_breakdown_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="task_breakdown_plan",
            target=target,
            recommended_steps=[
                self.build_step("Break into phases", "Split the task into inspect, plan, patch, test, and review phases."),
                self.build_step("Define validation", "Attach a safe validation step to every task phase."),
                self.build_step("Separate proposal from execution", "Keep execution steps marked as pending confirmation.", "medium"),
                self.build_step("Prepare rollback notes", "Identify how to stop or revert if a future action is approved."),
            ],
            checklist=[
                "Task phases are ordered.",
                "Each phase has a validation step.",
                "Execution remains disabled.",
                "Rollback/review notes exist.",
                "User confirmation is required for real actions.",
            ],
        )

    def task_risk_review(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="task_risk_review",
            target=target,
            recommended_steps=[
                self.build_step("Classify write risk", "Check whether the task may modify files.", "medium"),
                self.build_step("Classify command risk", "Check whether the task may require shell commands.", "high"),
                self.build_step("Classify desktop risk", "Check whether the task may open apps or touch desktop state.", "high"),
                self.build_step("Apply sandbox boundary", "Keep commands as sandbox dry-run proposals only.", "medium"),
                self.build_step("Require confirmation", "Require explicit approval before any real action.", "high"),
            ],
            checklist=[
                "File-write risk reviewed.",
                "Command-execution risk reviewed.",
                "Desktop/app-opening risk reviewed.",
                "External action risk reviewed.",
                "All risky actions remain disabled.",
            ],
        )

    def task_execution_checklist(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="task_execution_checklist",
            target=target,
            recommended_steps=[
                self.build_step("Confirm target", "Confirm exact task target before any future execution."),
                self.build_step("Confirm scope", "Confirm affected files, commands, apps, or external systems."),
                self.build_step("Confirm safety", "Confirm permissions and sandbox result.", "medium"),
                self.build_step("Confirm user approval", "Ask for explicit approval before real execution.", "high"),
                self.build_step("Confirm validation", "Prepare post-action validation and git/status checks."),
            ],
            checklist=[
                "Target confirmed.",
                "Scope confirmed.",
                "Permissions checked.",
                "Sandbox checked.",
                "User approval required.",
                "Post-action validation prepared.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()
        context = self.integration_context("local task planner alpha context")

        return {
            "status": self.status_name,
            "context_ready": True,
            "planner_status": status,
            "identity": self.load_identity(),
            "project_intent_context": self.project_intent.context(),
            "creative_context": self.creative_assistant.context(),
            "workspace_memory_context": self.workspace_memory_link.context(),
            "tool_sandbox_status": context["tool_sandbox_status"],
            "tool_sandbox_policy": self.tool_sandbox.policy_dict(),
            "safe_current_capabilities": [
                "local_task_planner_status",
                "local_task_intent_plan",
                "local_task_breakdown_plan",
                "local_task_risk_review",
                "local_task_execution_checklist",
                "local_task_context",
            ],
            "disabled_capabilities": [
                "automatic_command_execution",
                "automatic_file_write",
                "automatic_app_open",
                "automatic_desktop_action",
                "external_action_execution",
                "real_tool_execution",
            ],
            "read_only": True,
            "proposal_only": True,
            "write_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "app_opened": False,
            "desktop_action_performed": False,
            "external_action_execution_performed": False,
            "real_tool_execution_performed": False,
            "note": "Local Task Planner Alpha context is read-only and proposal-only.",
        }

    def status(self) -> dict[str, Any]:
        project_intent_status = self.project_intent.status()
        creative_status = self.creative_assistant.status()
        workspace_memory_status = self.workspace_memory_link.status()
        sandbox_status = self.tool_sandbox.status()

        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_app_permission = self.permission_manager.check("open_app")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "task_intent_plan_ready": True,
            "task_breakdown_plan_ready": True,
            "task_risk_review_ready": True,
            "task_execution_checklist_ready": True,
            "context_ready": True,
            "project_intent_integration_ready": project_intent_status["intent_ready"],
            "creative_assistant_integration_ready": creative_status["assistant_ready"],
            "workspace_memory_link_integration_ready": workspace_memory_status["link_ready"],
            "tool_sandbox_integration_ready": sandbox_status["sandbox_ready"],
            "tool_sandbox_dry_run_ready": sandbox_status["dry_run_ready"],
            "tool_sandbox_real_execution_ready": sandbox_status["real_execution_ready"],
            "task_plan_types": len(self.task_plan_types()),
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_read_memory_confirmation": read_memory_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_open_app_confirmation": open_app_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "proposal_only": True,
            "file_write": False,
            "command_execution": False,
            "app_opened": False,
            "desktop_action_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Local Task Planner Alpha is online for safe local task planning. It does not execute commands, write files, open apps, perform desktop actions, or execute external actions automatically.",
        }
