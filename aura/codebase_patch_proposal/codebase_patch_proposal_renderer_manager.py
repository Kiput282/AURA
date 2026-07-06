from pathlib import Path
from typing import Any

from aura.codebase_change.codebase_change_planner_manager import CodebaseChangePlannerManager
from aura.file_ops.safe_file_operation_planner_manager import SafeFileOperationPlannerManager
from aura.local_task.local_task_planner_alpha_manager import LocalTaskPlannerAlphaManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class CodebasePatchProposalRendererManager:
    name = "codebase_patch_proposal_renderer"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.codebase_change = CodebaseChangePlannerManager(project_root=self.project_root)
        self.safe_file_ops = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.project_intent = ProjectIntentPlannerManager(project_root=self.project_root)
        self.local_task_planner = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)

    def safe_status(self, manager: Any) -> dict[str, Any]:
        try:
            status = manager.status()
        except Exception as exc:
            return {"status": "unknown", "ready": False, "error": str(exc)}
        return status if isinstance(status, dict) else {"status": "unknown", "ready": False}

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(text.strip().split())
        return normalized[:700].rstrip() + "..." if len(normalized) > 700 else normalized

    def proposal_sections(self) -> list[str]:
        return [
            "change_summary",
            "target_classification",
            "candidate_surfaces",
            "patch_outline",
            "review_checklist",
            "validation_plan",
            "rollback_plan",
            "safety_boundary",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "codebase_patch_proposal_status",
            "codebase_patch_proposal_render",
            "codebase_patch_review_packet",
            "codebase_patch_safety_packet",
            "codebase_patch_validation_packet",
            "codebase_patch_rollback_packet",
            "codebase_patch_proposal_context",
            "proposal_only_patch_rendering",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "automatic_file_read",
            "automatic_file_open",
            "automatic_file_write",
            "automatic_file_edit",
            "automatic_patch_apply",
            "automatic_file_move",
            "automatic_file_copy",
            "automatic_file_delete",
            "command_execution",
            "test_execution",
            "git_commit",
            "git_push",
            "external_action_execution",
            "real_tool_execution",
        ]

    def candidate_surfaces(self, target: str) -> list[dict[str, Any]]:
        lowered = target.lower()
        candidates = [
            ("identity", "aura/personality/identity.yaml", ["version", "sprint_state"]),
            ("skills", "aura/skills/builtin_skills.py", ["skill_registry", "capabilities"]),
            ("plugins", "aura/plugins/builtin/plugin_actions.py", ["plugin_actions", "permissions"]),
            ("status", "aura/status/system_status_manager.py", ["runtime_status", "summary"]),
            ("cli", "aura/core/cli.py", ["command_surface", "manual_invocation"]),
            ("readme", "README.md", ["docs", "sprint_notes"]),
        ]

        output: list[dict[str, Any]] = []
        for name, path, tags in candidates:
            relevance = "medium" if any(token in lowered for token in [name, path.lower(), *tags]) else "low"
            if "codebase" in lowered or "patch" in lowered or "proposal" in lowered:
                relevance = "medium"
            output.append(
                {
                    "name": name,
                    "path_hint": path,
                    "tags": tags,
                    "relevance": relevance,
                    "read_performed": False,
                    "write_performed": False,
                }
            )
        return output

    def patch_outline(self, target: str) -> list[dict[str, Any]]:
        normalized = self.normalize_text(target)
        return [
            {
                "index": 1,
                "title": "Confirm change intent",
                "description": f"Use the user-provided request as the source of truth: {normalized}",
                "risk": "low",
                "requires_confirmation": False,
            },
            {
                "index": 2,
                "title": "Classify candidate surfaces",
                "description": "List likely files/components without opening or reading their contents.",
                "risk": "medium",
                "requires_confirmation": False,
            },
            {
                "index": 3,
                "title": "Prepare minimal patch proposal",
                "description": "Describe proposed files, purpose, and expected behavior before any real edit.",
                "risk": "medium",
                "requires_confirmation": True,
            },
            {
                "index": 4,
                "title": "Prepare validation packet",
                "description": "Define py_compile, registry, manager, system-status, git diff, and smoke checks.",
                "risk": "low",
                "requires_confirmation": False,
            },
            {
                "index": 5,
                "title": "Prepare rollback packet",
                "description": "Define restore/rollback boundary before commit or push.",
                "risk": "medium",
                "requires_confirmation": True,
            },
            {
                "index": 6,
                "title": "Keep execution disabled",
                "description": "No file reads, writes, command execution, commit, or push are performed by this renderer.",
                "risk": "low",
                "requires_confirmation": False,
            },
        ]

    def review_checklist(self) -> list[str]:
        return [
            "Patch proposal has a clear goal.",
            "Candidate files/components are listed as hints only.",
            "No target file content was read automatically.",
            "No patch file was generated automatically.",
            "No patch was applied automatically.",
            "Validation commands are proposed but not executed.",
            "Rollback boundary is proposed before commit/push.",
            "User confirmation is required before any real edit or command.",
        ]

    def validation_packet(self) -> list[str]:
        return [
            "python3 -m py_compile for new/changed Python files",
            "manager.status() safety flag assertions",
            "proposal render assertions",
            "skill registry lookup",
            "plugin action registry lookup",
            "system-status smoke check when integrated",
            "git diff review before commit",
            "git status --short after validation",
        ]

    def rollback_packet(self) -> list[str]:
        return [
            "Review git diff before staging.",
            "Use git restore <file> for uncommitted file rollback.",
            "Use git restore --staged <file> for staged rollback.",
            "Avoid git reset --hard unless explicitly approved.",
            "Avoid force-push unless explicitly approved.",
            "Keep commit boundaries small and sprint-scoped.",
        ]

    def safety_notes(self) -> list[str]:
        return [
            "Patch proposal renderer is proposal-only.",
            "No target file content was read.",
            "No file was opened.",
            "No file was written or edited.",
            "No patch was applied.",
            "No shell command was executed.",
            "No git commit or push was performed.",
            "Future real codebase changes must go through explicit confirmation and validation.",
        ]

    def render_proposal(self, target: str) -> dict[str, Any]:
        normalized = self.normalize_text(target)
        change_plan = self.codebase_change.patch_plan(normalized)
        codebase_change_status = self.safe_status(self.codebase_change)
        safe_file_status = self.safe_status(self.safe_file_ops)
        project_intent_status = self.safe_status(self.project_intent)
        local_task_status = self.safe_status(self.local_task_planner)
        workspace_status = self.safe_status(self.workspace_awareness)
        workspace_memory_status = self.safe_status(self.workspace_memory_link)
        sandbox_status = self.safe_status(self.tool_sandbox)
        candidates = self.candidate_surfaces(normalized)
        outline = self.patch_outline(normalized)
        checklist = self.review_checklist()

        return {
            "status": "rendered",
            "proposal_type": "codebase_patch_proposal",
            "target": normalized,
            "proposal_state": "review_ready",
            "proposal_only": True,
            "metadata_only": True,
            "read_only": True,
            "execution_ready": False,
            "executed": False,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "patch_apply_performed": False,
            "file_delete_performed": False,
            "file_move_performed": False,
            "file_copy_performed": False,
            "command_execution_performed": False,
            "test_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "section_count": len(self.proposal_sections()),
            "candidate_surface_count": len(candidates),
            "patch_outline_count": len(outline),
            "review_checklist_count": len(checklist),
            "codebase_change_ready": bool(codebase_change_status.get("planner_ready", codebase_change_status.get("status") == "online")),
            "safe_file_operation_ready": bool(safe_file_status.get("planner_ready", safe_file_status.get("status") == "online")),
            "project_intent_ready": bool(project_intent_status.get("intent_ready", project_intent_status.get("status") == "online")),
            "local_task_planner_ready": bool(local_task_status.get("planner_ready", local_task_status.get("status") == "online")),
            "workspace_awareness_ready": bool(workspace_status.get("awareness_ready", workspace_status.get("status") == "online")),
            "workspace_memory_link_ready": bool(workspace_memory_status.get("link_ready", workspace_memory_status.get("status") == "online")),
            "tool_sandbox_ready": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            "tool_sandbox_dry_run_ready": bool(sandbox_status.get("dry_run_ready", False)),
            "tool_sandbox_real_execution_ready": bool(sandbox_status.get("real_execution_ready", False)),
            "change_plan": change_plan,
            "candidate_surfaces": candidates,
            "patch_outline": outline,
            "review_checklist": checklist,
            "validation_packet": self.validation_packet(),
            "rollback_packet": self.rollback_packet(),
            "safety_notes": self.safety_notes(),
        }

    def status(self) -> dict[str, Any]:
        read_project_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        codebase_change_status = self.safe_status(self.codebase_change)
        safe_file_status = self.safe_status(self.safe_file_ops)
        sandbox_status = self.safe_status(self.tool_sandbox)

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "renderer_ready": True,
            "proposal_render_ready": True,
            "review_packet_ready": True,
            "safety_packet_ready": True,
            "validation_packet_ready": True,
            "rollback_packet_ready": True,
            "context_ready": True,
            "section_count": len(self.proposal_sections()),
            "codebase_change_integration_ready": bool(codebase_change_status.get("planner_ready", codebase_change_status.get("status") == "online")),
            "safe_file_operation_integration_ready": bool(safe_file_status.get("planner_ready", safe_file_status.get("status") == "online")),
            "tool_sandbox_integration_ready": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            "tool_sandbox_dry_run_ready": bool(sandbox_status.get("dry_run_ready", False)),
            "tool_sandbox_real_execution_ready": bool(sandbox_status.get("real_execution_ready", False)),
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
            "patch_apply": False,
            "file_delete": False,
            "file_move": False,
            "file_copy": False,
            "command_execution": False,
            "test_execution": False,
            "git_commit": False,
            "git_push": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "project_root": str(self.project_root),
            "note": "Codebase Patch Proposal Renderer is online for proposal-only patch review packets. It does not read, open, write, edit, apply patches, execute commands, commit, or push automatically.",
        }

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
            "patch_apply_performed": False,
            "command_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "renderer_status": status,
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "proposal_sections": self.proposal_sections(),
            "note": "Patch proposal context is metadata-only and proposal-only.",
        }
