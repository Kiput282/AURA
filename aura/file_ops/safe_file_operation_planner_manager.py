from pathlib import Path
from typing import Any

import yaml

from aura.local_task.local_task_planner_alpha_manager import LocalTaskPlannerAlphaManager
from aura.permissions.permission_manager import PermissionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class SafeFileOperationPlannerManager:
    """
    AURA Safe File Operation Planner.

    Current phase:
    - prepare safe file read plans
    - prepare file write plan proposals
    - prepare file edit plan proposals
    - prepare move/copy/delete risk reviews
    - prepare file operation checklists
    - expose file operation context
    - integrate local task planner, workspace awareness, workspace memory link, and tool sandbox
    - never writes files automatically
    - never deletes files automatically
    - never moves or copies files automatically
    - never opens files automatically
    - never executes commands automatically
    """

    name = "safe_file_operation_planner"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.local_task_planner = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
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

    def file_operation_types(self) -> list[str]:
        return [
            "file_read_plan",
            "file_write_plan_proposal",
            "file_edit_plan_proposal",
            "file_move_copy_delete_risk_review",
            "file_operation_checklist",
            "file_operation_context",
            "safety_boundary",
        ]

    def infer_file_tags(self, text: str) -> list[str]:
        lowered = text.lower()
        tags: list[str] = []

        keyword_map = {
            "read": "read",
            "open": "open_file",
            "write": "write",
            "edit": "edit",
            "modify": "edit",
            "move": "move",
            "copy": "copy",
            "delete": "delete",
            "remove": "delete",
            "rename": "move",
            "backup": "copy",
            "config": "config_file",
            "yaml": "config_file",
            "json": "data_file",
            "py": "python_file",
            "python": "python_file",
            "md": "document_file",
            "doc": "document_file",
            "safe": "safety",
            "risk": "risk",
            "command": "command",
            "shell": "command",
        }

        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)

        if not tags:
            tags.extend(["file_operation", "planning"])

        return tags[:8]

    def operation_priority(self, tags: list[str]) -> str:
        high_risk = {"write", "edit", "move", "copy", "delete", "open_file", "command", "risk"}

        if any(tag in high_risk for tag in tags):
            return "safety_first_file_operation_planning"

        if "read" in tags:
            return "safe_file_read_planning"

        return "file_operation_planning"

    def important_file_paths(self) -> list[str]:
        return [
            item["path"]
            for item in self.workspace_awareness.important_files()
            if item["exists"]
        ]

    def classify_target_path(self, target: str) -> dict[str, Any]:
        cleaned = self.normalize_text(target)
        lowered = cleaned.lower()
        important_files = self.important_file_paths()

        matched_important = [
            item
            for item in important_files
            if item.lower() in lowered or Path(item).name.lower() in lowered
        ]

        traversal_detected = ".." in cleaned.replace("\\\\", "/").split("/")
        absolute_path_hint = cleaned.startswith("/") or ":\\\\" in cleaned or cleaned.startswith("~")
        runtime_hint = any(part in lowered for part in [".git", ".venv", "__pycache__", "data/", "logs/"])

        return {
            "target": cleaned or "<unspecified>",
            "matched_important_files": matched_important[:8],
            "matched_important_file_count": len(matched_important),
            "path_traversal_detected": traversal_detected,
            "absolute_path_hint": absolute_path_hint,
            "runtime_path_hint": runtime_hint,
            "path_risk": "higher" if traversal_detected or absolute_path_hint or runtime_hint else "normal",
            "project_root": str(self.project_root),
            "metadata_only": True,
            "path_opened": False,
            "path_written": False,
            "path_deleted": False,
            "path_moved": False,
            "path_copied": False,
        }

    def integration_context(self, target: str) -> dict[str, Any]:
        return {
            "local_task_status": self.local_task_planner.status(),
            "local_task_risk_review": self.local_task_planner.task_risk_review(target),
            "workspace_status": self.workspace_awareness.status(),
            "workspace_context": self.workspace_awareness.context(),
            "workspace_memory_status": self.workspace_memory_link.status(),
            "workspace_memory_summary": self.workspace_memory_link.summary(),
            "tool_sandbox_status": self.tool_sandbox.status(),
            "tool_sandbox_dry_run": self.tool_sandbox.dry_run("echo safe-file-operation-planner-dry-run"),
        }

    def build_step(self, title: str, description: str, risk: str = "low") -> dict[str, Any]:
        return {
            "title": title,
            "description": description,
            "risk": risk,
            "ready": True,
            "requires_confirmation": risk in {"medium", "high"},
            "executed": False,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
        }

    def base_plan(
        self,
        plan_type: str,
        target: str,
        recommended_steps: list[dict[str, Any]],
        checklist: list[str],
        operation_risk: str,
    ) -> dict[str, Any]:
        cleaned_target = self.normalize_text(target) or "<unspecified>"
        tags = self.infer_file_tags(cleaned_target)
        path_classification = self.classify_target_path(cleaned_target)
        context = self.integration_context(cleaned_target)

        read_project_permission = self.permission_manager.check("read_project")
        read_file_permission = self.permission_manager.check("read_file")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_file_permission = self.permission_manager.check("open_file")
        write_permission = self.permission_manager.check("write_file")
        delete_permission = self.permission_manager.check("delete_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": cleaned_target,
            "plan_state": "proposal_ready",
            "operation_risk": operation_risk,
            "file_tags": tags,
            "operation_priority": self.operation_priority(tags),
            "path_classification": path_classification,
            "local_task_risk_priority": context["local_task_risk_review"]["task_priority"],
            "workspace_summary": context["workspace_context"]["workspace_summary"],
            "workspace_memory_summary": context["workspace_memory_summary"]["summary"],
            "important_file_count": context["workspace_status"]["important_file_count"],
            "tool_sandbox_ready": context["tool_sandbox_status"]["sandbox_ready"],
            "tool_sandbox_dry_run_ready": context["tool_sandbox_dry_run"]["dry_run_ready"],
            "tool_sandbox_real_execution_ready": context["tool_sandbox_status"]["real_execution_ready"],
            "recommended_steps": recommended_steps,
            "step_count": len(recommended_steps),
            "checklist": checklist,
            "checklist_count": len(checklist),
            "permissions": {
                "read_project": read_project_permission.to_dict(),
                "read_file": read_file_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "open_file": open_file_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "delete_file": delete_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "proposal_only": True,
            "metadata_only": True,
            "read_only": True,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "real_tool_execution_performed": False,
            "safety_notes": [
                "File operation plan is proposal-only.",
                "No file was read from disk by this planner.",
                "No file was opened.",
                "No file was written or edited.",
                "No file was moved, copied, or deleted.",
                "No command was executed.",
                "Future real file operations must go through explicit confirmation and validation.",
            ],
        }

    def file_read_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="file_read_plan",
            target=target,
            operation_risk="low",
            recommended_steps=[
                self.build_step("Clarify read target", "Identify the exact file or document that may need reading."),
                self.build_step("Validate project scope", "Confirm the target is inside the AURA project workspace."),
                self.build_step("Check sensitivity", "Avoid opening secrets, credentials, runtime data, or unrelated personal files.", "medium"),
                self.build_step("Prepare read-only review", "Keep the operation as a read plan until user explicitly requests reading."),
            ],
            checklist=[
                "Read target is clear.",
                "Target is within expected project scope.",
                "Sensitive/runtime paths are reviewed.",
                "No file is opened automatically.",
                "No file content is read by this planner.",
            ],
        )

    def file_write_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="file_write_plan_proposal",
            target=target,
            operation_risk="medium",
            recommended_steps=[
                self.build_step("Clarify write purpose", "Define the exact intended file output or modification.", "medium"),
                self.build_step("Prepare patch proposal", "Describe the proposed content without writing it.", "medium"),
                self.build_step("Validate target path", "Confirm the destination path and avoid runtime or ignored directories.", "medium"),
                self.build_step("Require confirmation", "Require explicit approval before any future file write.", "high"),
                self.build_step("Prepare post-write validation", "Plan py_compile, status, git diff, or other safe validation steps."),
            ],
            checklist=[
                "Write purpose is clear.",
                "Target path is validated.",
                "Patch/content is proposal-only.",
                "No file is written automatically.",
                "User confirmation is required.",
                "Post-write validation is planned.",
            ],
        )

    def file_edit_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="file_edit_plan_proposal",
            target=target,
            operation_risk="medium",
            recommended_steps=[
                self.build_step("Clarify edit target", "Identify the file and exact section to change.", "medium"),
                self.build_step("Prepare before/after plan", "Describe intended edit as a reviewable proposal.", "medium"),
                self.build_step("Check dependencies", "Identify tests or commands needed later, without running them."),
                self.build_step("Require confirmation", "Do not edit until user confirms the proposal.", "high"),
                self.build_step("Prepare rollback note", "Plan how to inspect or revert future changes if needed."),
            ],
            checklist=[
                "Edit target is clear.",
                "Before/after intent is documented.",
                "Dependencies and validation are known.",
                "No edit is applied automatically.",
                "Rollback/review note is prepared.",
            ],
        )

    def file_move_copy_delete_risk_review(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="file_move_copy_delete_risk_review",
            target=target,
            operation_risk="high",
            recommended_steps=[
                self.build_step("Classify destructive risk", "Determine whether the operation moves, copies, renames, or deletes files.", "high"),
                self.build_step("Check target scope", "Confirm source and destination stay inside approved project scope.", "high"),
                self.build_step("Check delete restriction", "Deletion remains restricted and is not allowed by this planner.", "high"),
                self.build_step("Prepare backup/rollback notes", "Plan verification and rollback before any future operation.", "medium"),
                self.build_step("Require explicit approval", "Require user confirmation and separate validation before any real file operation.", "high"),
            ],
            checklist=[
                "Move/copy/delete intent is classified.",
                "Source and destination scope are reviewed.",
                "Delete remains restricted.",
                "No file is moved.",
                "No file is copied.",
                "No file is deleted.",
                "Explicit confirmation is required.",
            ],
        )

    def file_operation_checklist(self, target: str) -> dict[str, Any]:
        return self.base_plan(
            plan_type="file_operation_checklist",
            target=target,
            operation_risk="medium",
            recommended_steps=[
                self.build_step("Confirm operation type", "Confirm read, write, edit, move, copy, or delete intent.", "medium"),
                self.build_step("Confirm path", "Confirm source and destination paths before action.", "medium"),
                self.build_step("Confirm permissions", "Review read/write/delete/command permission state.", "medium"),
                self.build_step("Confirm validation", "Prepare py_compile, git diff, status, or content checks as appropriate."),
                self.build_step("Confirm user approval", "Require explicit approval before any real operation.", "high"),
            ],
            checklist=[
                "Operation type confirmed.",
                "Path scope confirmed.",
                "Permissions checked.",
                "Sandbox checked.",
                "User approval required.",
                "Validation prepared.",
                "No real operation performed.",
            ],
        )

    def context(self) -> dict[str, Any]:
        status = self.status()
        context = self.integration_context("safe file operation planner context")

        return {
            "status": self.status_name,
            "context_ready": True,
            "planner_status": status,
            "identity": self.load_identity(),
            "local_task_context": self.local_task_planner.context(),
            "workspace_context": self.workspace_awareness.context(),
            "workspace_memory_context": self.workspace_memory_link.context(),
            "tool_sandbox_status": context["tool_sandbox_status"],
            "tool_sandbox_policy": self.tool_sandbox.policy_dict(),
            "safe_current_capabilities": [
                "safe_file_operation_status",
                "safe_file_read_plan",
                "safe_file_write_plan",
                "safe_file_edit_plan",
                "safe_file_move_copy_delete_risk_review",
                "safe_file_operation_checklist",
                "safe_file_operation_context",
            ],
            "disabled_capabilities": [
                "automatic_file_read",
                "automatic_file_open",
                "automatic_file_write",
                "automatic_file_edit",
                "automatic_file_move",
                "automatic_file_copy",
                "automatic_file_delete",
                "command_execution",
                "external_action_execution",
                "real_tool_execution",
            ],
            "read_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "write_performed": False,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "real_tool_execution_performed": False,
            "note": "Safe File Operation Planner context is metadata-only and proposal-only.",
        }

    def status(self) -> dict[str, Any]:
        local_task_status = self.local_task_planner.status()
        workspace_status = self.workspace_awareness.status()
        workspace_memory_status = self.workspace_memory_link.status()
        sandbox_status = self.tool_sandbox.status()

        read_project_permission = self.permission_manager.check("read_project")
        read_file_permission = self.permission_manager.check("read_file")
        prepare_permission = self.permission_manager.check("prepare_file")
        open_file_permission = self.permission_manager.check("open_file")
        write_permission = self.permission_manager.check("write_file")
        delete_permission = self.permission_manager.check("delete_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "file_read_plan_ready": True,
            "file_write_plan_ready": True,
            "file_edit_plan_ready": True,
            "file_move_copy_delete_risk_review_ready": True,
            "file_operation_checklist_ready": True,
            "context_ready": True,
            "local_task_integration_ready": local_task_status["planner_ready"],
            "workspace_awareness_integration_ready": workspace_status["awareness_ready"],
            "workspace_memory_link_integration_ready": workspace_memory_status["link_ready"],
            "tool_sandbox_integration_ready": sandbox_status["sandbox_ready"],
            "tool_sandbox_dry_run_ready": sandbox_status["dry_run_ready"],
            "tool_sandbox_real_execution_ready": sandbox_status["real_execution_ready"],
            "file_operation_types": len(self.file_operation_types()),
            "important_file_count": workspace_status["important_file_count"],
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_read_file_confirmation": read_file_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_open_file_confirmation": open_file_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_delete_confirmation": delete_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "file_read": False,
            "file_opened": False,
            "file_write": False,
            "file_edit": False,
            "file_delete": False,
            "file_move": False,
            "file_copy": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Safe File Operation Planner is online for metadata-only file operation planning. It does not read, open, write, edit, move, copy, delete files, or execute commands automatically.",
        }
