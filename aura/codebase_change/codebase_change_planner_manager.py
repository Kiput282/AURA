from pathlib import Path
from typing import Any

import yaml

from aura.file_ops.safe_file_operation_planner_manager import SafeFileOperationPlannerManager
from aura.local_task.local_task_planner_alpha_manager import LocalTaskPlannerAlphaManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class CodebaseChangePlannerManager:
    # Metadata-only planner. It prepares codebase change proposals but never reads,
    # writes, edits, deletes, executes commands, commits, or pushes automatically.

    name = "codebase_change_planner"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.project_intent = ProjectIntentPlannerManager(project_root=self.project_root)
        self.local_task_planner = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.safe_file_ops = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}
        content = self.identity_path.read_text(encoding="utf-8", errors="replace")
        data = yaml.safe_load(content)
        return data if isinstance(data, dict) else {}

    def safe_status(self, manager: Any) -> dict[str, Any]:
        try:
            status = manager.status()
        except Exception as exc:
            return {"status": "unknown", "ready": False, "error": str(exc)}
        return status if isinstance(status, dict) else {"status": "unknown", "ready": False}

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())
        return normalized[:500].rstrip() + "..." if len(normalized) > 500 else normalized

    def change_plan_types(self) -> list[str]:
        return [
            "change_intent_plan",
            "change_impact_plan",
            "patch_plan",
            "validation_plan",
            "rollback_plan",
            "change_context",
            "safety_boundary",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "codebase_change_status",
            "codebase_change_intent_plan",
            "codebase_change_impact_plan",
            "codebase_patch_plan",
            "codebase_validation_plan",
            "codebase_rollback_plan",
            "codebase_change_context",
            "metadata_only_codebase_change_planning",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "automatic_file_read",
            "automatic_file_open",
            "automatic_file_write",
            "automatic_file_edit",
            "automatic_file_move",
            "automatic_file_copy",
            "automatic_file_delete",
            "command_execution",
            "git_commit",
            "git_push",
            "external_action_execution",
            "real_tool_execution",
        ]

    def infer_change_tags(self, target: str) -> list[str]:
        lowered = target.lower()
        tags: list[str] = []
        keyword_map = {
            "sprint": "sprint",
            "project": "project",
            "code": "coding",
            "coding": "coding",
            "python": "python",
            ".py": "python_file",
            "cli": "cli",
            "shell": "shell",
            "command": "command_surface",
            "plugin": "plugin_registry",
            "skill": "skill_registry",
            "status": "system_status",
            "manager": "manager",
            "planner": "planner",
            "file": "file_operation",
            "write": "file_operation",
            "edit": "file_operation",
            "delete": "destructive",
            "move": "destructive",
            "copy": "file_operation",
            "test": "validation",
            "validate": "validation",
            "rollback": "rollback",
            "safe": "safety",
            "safety": "safety",
        }
        for keyword, tag in keyword_map.items():
            if keyword in lowered and tag not in tags:
                tags.append(tag)
        if not tags:
            tags.extend(["codebase_change", "planning"])
        return tags[:10]

    def classify_target(self, target: str) -> dict[str, Any]:
        normalized = self.normalize_text(target)
        lowered = normalized.lower()
        tags = self.infer_change_tags(normalized)
        sensitive_markers = [
            ".env",
            "secret",
            "token",
            "credential",
            "password",
            "private",
            "data/",
            "logs/",
            ".git/",
            ".venv/",
            "__pycache__",
        ]
        important_file_candidates = [
            "README.md",
            "main.py",
            "requirements.txt",
            ".gitignore",
            "aura/personality/identity.yaml",
            "aura/config/settings.yaml",
            "aura/core/cli.py",
            "aura/core/shell.py",
            "aura/status/system_status_manager.py",
            "aura/plugins/builtin/plugin_actions.py",
            "aura/skills/builtin_skills.py",
            "docs/AURA_MASTER_ROADMAP.md",
            "docs/AURA_PRODUCT_VISION.md",
        ]
        matched = [candidate for candidate in important_file_candidates if candidate.lower() in lowered]
        risk = "low"
        if any(marker in lowered for marker in sensitive_markers):
            risk = "high"
        elif any(tag in tags for tag in ["destructive", "command_surface", "system_status", "plugin_registry", "skill_registry", "python_file", "file_operation"]):
            risk = "medium"
        return {
            "target": normalized,
            "target_risk": risk,
            "tags": tags,
            "matched_important_files": matched,
            "matched_important_file_count": len(matched),
            "path_traversal_detected": ".." in Path(normalized).parts or "../" in normalized,
            "absolute_path_hint": normalized.startswith("/"),
            "sensitive_hint": any(marker in lowered for marker in sensitive_markers),
            "runtime_path_hint": any(marker in lowered for marker in ["data/", "logs/", ".venv/", "__pycache__"]),
        }

    def workspace_summary_text(self) -> str:
        identity = self.load_identity()
        workspace_status = self.safe_status(self.workspace_awareness)
        version = identity.get("version", "unknown")
        codename = identity.get("codename", "unknown")
        python_files = workspace_status.get("project_python_files", workspace_status.get("python_files", "unknown"))
        important_files = workspace_status.get("important_file_count", "unknown")
        return (
            f"AURA workspace is at version {version} in {codename} phase. "
            f"Codebase change planning is metadata-only; tracked Python files: {python_files}; "
            f"important file candidates: {important_files}."
        )

    def workspace_memory_summary_text(self) -> str:
        status = self.safe_status(self.workspace_memory_link)
        return (
            f"Workspace memory link is available for proposal context with "
            f"{status.get('memory_count', 'unknown')} memories, "
            f"{status.get('journal_count', 'unknown')} journal entries, and "
            f"{status.get('milestone_count', 'unknown')} milestone candidates."
        )

    def recommended_steps(self) -> list[dict[str, Any]]:
        steps = [
            ("Clarify requested change", "low", False, "Normalize the codebase change goal and identify intended files or components."),
            ("Classify target risk", "medium", False, "Check important, runtime, sensitive, command, or destructive areas."),
            ("Map impacted surfaces", "medium", False, "List likely code, CLI, shell, skill, plugin, status, docs, and validation surfaces."),
            ("Prepare proposal-only patch boundary", "high", True, "Require explicit approval before file write, edit, commit, or push."),
            ("Prepare validation and rollback", "low", False, "Plan py_compile, CLI smoke tests, action-request checks, system-status checks, git diff, and rollback."),
            ("Keep execution disabled", "low", False, "No file read, file write, command execution, commit, push, or external action is performed by this planner."),
        ]
        return [
            {
                "index": index,
                "name": name,
                "risk": risk,
                "ready": True,
                "requires_confirmation": confirmation,
                "description": description,
            }
            for index, (name, risk, confirmation, description) in enumerate(steps, start=1)
        ]

    def checklist(self) -> list[str]:
        return [
            "Change intent is clear.",
            "Target scope is classified.",
            "Important/runtime/sensitive paths are reviewed.",
            "Patch remains proposal-only.",
            "Validation plan is prepared.",
            "Rollback boundary is prepared.",
            "No file is read automatically.",
            "No file is written or edited automatically.",
            "No command is executed automatically.",
            "No commit or push is performed automatically.",
        ]

    def safety_notes(self) -> list[str]:
        return [
            "Codebase change plan is proposal-only.",
            "No target file content was read by this planner.",
            "No file was opened.",
            "No file was written or edited.",
            "No file was moved, copied, or deleted.",
            "No shell command was executed.",
            "No git commit or push was performed.",
            "Future real codebase changes must go through explicit confirmation and validation.",
        ]

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target)
        classification = self.classify_target(normalized_target)
        project_intent_status = self.safe_status(self.project_intent)
        local_task_status = self.safe_status(self.local_task_planner)
        safe_file_status = self.safe_status(self.safe_file_ops)
        workspace_status = self.safe_status(self.workspace_awareness)
        workspace_memory_status = self.safe_status(self.workspace_memory_link)
        sandbox_status = self.safe_status(self.tool_sandbox)
        steps = self.recommended_steps()
        checklist = self.checklist()
        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "plan_state": "proposal_ready",
            "change_risk": classification["target_risk"],
            "change_priority": "safety_first_codebase_change_planning" if classification["target_risk"] == "high" else "codebase_change_planning",
            "change_tags": classification["tags"],
            "step_count": len(steps),
            "checklist_count": len(checklist),
            "change_plan_types": len(self.change_plan_types()),
            "project_intent_ready": bool(project_intent_status.get("intent_ready", project_intent_status.get("status") == "online")),
            "local_task_planner_ready": bool(local_task_status.get("planner_ready", local_task_status.get("status") == "online")),
            "safe_file_operation_planner_ready": bool(safe_file_status.get("planner_ready", safe_file_status.get("status") == "online")),
            "workspace_awareness_ready": bool(workspace_status.get("awareness_ready", workspace_status.get("status") == "online")),
            "workspace_memory_link_ready": bool(workspace_memory_status.get("link_ready", workspace_memory_status.get("status") == "online")),
            "tool_sandbox_ready": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            "tool_sandbox_dry_run_ready": bool(sandbox_status.get("dry_run_ready", False)),
            "tool_sandbox_real_execution_ready": bool(sandbox_status.get("real_execution_ready", False)),
            "execution_ready": False,
            "executed": False,
            "read_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "target_classification": classification,
            "workspace_summary": self.workspace_summary_text(),
            "workspace_memory_summary": self.workspace_memory_summary_text(),
            "recommended_steps": steps,
            "checklist": checklist,
            "safety_notes": self.safety_notes(),
        }

    def status(self) -> dict[str, Any]:
        read_project_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        workspace_status = self.safe_status(self.workspace_awareness)
        workspace_memory_status = self.safe_status(self.workspace_memory_link)
        project_intent_status = self.safe_status(self.project_intent)
        local_task_status = self.safe_status(self.local_task_planner)
        safe_file_status = self.safe_status(self.safe_file_ops)
        sandbox_status = self.safe_status(self.tool_sandbox)
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "planner_ready": True,
            "change_intent_plan_ready": True,
            "change_impact_plan_ready": True,
            "patch_plan_ready": True,
            "validation_plan_ready": True,
            "rollback_plan_ready": True,
            "context_ready": True,
            "project_intent_integration_ready": bool(project_intent_status.get("intent_ready", project_intent_status.get("status") == "online")),
            "local_task_integration_ready": bool(local_task_status.get("planner_ready", local_task_status.get("status") == "online")),
            "safe_file_operation_integration_ready": bool(safe_file_status.get("planner_ready", safe_file_status.get("status") == "online")),
            "workspace_awareness_integration_ready": bool(workspace_status.get("awareness_ready", workspace_status.get("status") == "online")),
            "workspace_memory_link_integration_ready": bool(workspace_memory_status.get("link_ready", workspace_memory_status.get("status") == "online")),
            "tool_sandbox_integration_ready": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            "tool_sandbox_dry_run_ready": bool(sandbox_status.get("dry_run_ready", False)),
            "tool_sandbox_real_execution_ready": bool(sandbox_status.get("real_execution_ready", False)),
            "change_plan_types": len(self.change_plan_types()),
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
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
            "git_commit": False,
            "git_push": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 7,
            "project_root": str(self.project_root),
            "note": "Codebase Change Planner is online for metadata-only planning. It does not read, open, write, edit, move, copy, delete files, execute commands, commit, or push automatically.",
        }

    def change_intent_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan("change_intent_plan", target)

    def change_impact_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan("change_impact_plan", target)

    def patch_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan("patch_plan", target)

    def validation_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan("validation_plan", target)

    def rollback_plan(self, target: str) -> dict[str, Any]:
        return self.base_plan("rollback_plan", target)

    def context(self) -> dict[str, Any]:
        status = self.status()
        return {
            "status": status["status"],
            "context_ready": True,
            "read_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "planner_status": status,
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "workspace_summary": self.workspace_summary_text(),
            "workspace_memory_summary": self.workspace_memory_summary_text(),
            "note": "Codebase Change Planner context is metadata-only and proposal-only.",
        }
