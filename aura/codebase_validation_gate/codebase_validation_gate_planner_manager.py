from pathlib import Path
from typing import Any

from aura.codebase_change.codebase_change_planner_manager import CodebaseChangePlannerManager
from aura.codebase_patch_proposal.codebase_patch_proposal_renderer_manager import CodebasePatchProposalRendererManager
from aura.file_ops.safe_file_operation_planner_manager import SafeFileOperationPlannerManager
from aura.permissions.permission_manager import PermissionManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager


class CodebaseValidationGatePlannerManager:
    name = "codebase_validation_gate_planner"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.permission_manager = PermissionManager()
        self.codebase_change = CodebaseChangePlannerManager(project_root=self.project_root)
        self.patch_proposal = CodebasePatchProposalRendererManager(project_root=self.project_root)
        self.safe_file_ops = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.project_intent = ProjectIntentPlannerManager(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
        self.workspace_memory_link = WorkspaceMemoryLinkManager(project_root=self.project_root)

    def safe_status(self, manager: Any) -> dict[str, Any]:
        try:
            status = manager.status()
        except Exception as exc:
            return {"status": "unknown", "ready": False, "error": str(exc)}
        return status if isinstance(status, dict) else {"status": "unknown", "ready": False}

    def normalize_text(self, text: str) -> str:
        normalized = " ".join(str(text).strip().split())
        return normalized[:900].rstrip() + "..." if len(normalized) > 900 else normalized

    def gate_types(self) -> list[str]:
        return [
            "preflight_gate",
            "static_validation_gate",
            "registry_validation_gate",
            "runtime_smoke_gate",
            "diff_review_gate",
            "rollback_gate",
            "commit_push_gate",
            "safety_boundary_gate",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "codebase_validation_gate_status",
            "codebase_validation_gate_plan",
            "codebase_preflight_gate",
            "codebase_static_validation_gate",
            "codebase_registry_validation_gate",
            "codebase_runtime_smoke_gate",
            "codebase_diff_review_gate",
            "codebase_rollback_gate",
            "codebase_commit_push_gate",
            "codebase_validation_gate_context",
            "proposal_only_validation_gating",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "automatic_file_read",
            "automatic_file_open",
            "automatic_file_write",
            "automatic_file_edit",
            "automatic_patch_apply",
            "automatic_command_execution",
            "automatic_test_execution",
            "automatic_git_commit",
            "automatic_git_push",
            "external_action_execution",
            "real_tool_execution",
        ]

    def base_gate(self, name: str, title: str, purpose: str, commands: list[str], required: bool = True) -> dict[str, Any]:
        return {
            "name": name,
            "title": title,
            "purpose": purpose,
            "required": required,
            "proposal_only": True,
            "metadata_only": True,
            "read_only": True,
            "execution_ready": False,
            "executed": False,
            "commands_proposed": commands,
            "commands_executed": [],
            "file_read_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "test_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "result": "not_run",
        }

    def proposed_gates(self, target: str) -> list[dict[str, Any]]:
        normalized = self.normalize_text(target)
        return [
            self.base_gate(
                "preflight_gate",
                "Preflight Gate",
                f"Confirm clean tree, intended sprint scope, and target context before any change: {normalized}",
                ["git status --short", "git pull --ff-only origin main"],
            ),
            self.base_gate(
                "static_validation_gate",
                "Static Validation Gate",
                "Compile changed Python files and fail fast on syntax/import issues.",
                ["python3 -m py_compile <changed-python-files>"],
            ),
            self.base_gate(
                "registry_validation_gate",
                "Registry Validation Gate",
                "Confirm new skills and plugin actions are discoverable.",
                [
                    "python3 - <<'PY' # import and inspect build_builtin_skill_registry/build_builtin_plugin_action_registry",
                    "PY",
                ],
            ),
            self.base_gate(
                "runtime_smoke_gate",
                "Runtime Smoke Gate",
                "Instantiate the new manager and assert safety flags remain disabled.",
                [
                    "python3 - <<'PY' # manager.status(), plan/render/context assertions",
                    "PY",
                ],
            ),
            self.base_gate(
                "diff_review_gate",
                "Diff Review Gate",
                "Review the exact source changes before staging or committing.",
                ["git diff -- README.md aura | sed -n '1,260p'", "git status --short"],
            ),
            self.base_gate(
                "rollback_gate",
                "Rollback Gate",
                "Keep reversible restore commands ready before commit/push.",
                ["git restore <file>", "git restore --staged <file>"],
            ),
            self.base_gate(
                "commit_push_gate",
                "Commit/Push Gate",
                "Commit and push only after validation and human review.",
                ["git add README.md aura", "git commit -m '<message>'", "git push origin main"],
                required=False,
            ),
            self.base_gate(
                "safety_boundary_gate",
                "Safety Boundary Gate",
                "Confirm no automatic read/write/execute/commit/push was performed by this planner.",
                [],
            ),
        ]

    def safety_assertions(self) -> dict[str, bool]:
        return {
            "proposal_only": True,
            "metadata_only": True,
            "read_only": True,
            "runtime_ready": False,
            "file_read": False,
            "file_opened": False,
            "file_write": False,
            "file_edit": False,
            "patch_apply": False,
            "command_execution": False,
            "test_execution": False,
            "git_commit": False,
            "git_push": False,
            "external_action_execution": False,
            "real_tool_execution": False,
        }

    def validation_gate_plan(self, target: str) -> dict[str, Any]:
        normalized = self.normalize_text(target)
        patch_packet = self.patch_proposal.render_proposal(normalized)
        codebase_change_status = self.safe_status(self.codebase_change)
        patch_proposal_status = self.safe_status(self.patch_proposal)
        safe_file_status = self.safe_status(self.safe_file_ops)
        project_intent_status = self.safe_status(self.project_intent)
        sandbox_status = self.safe_status(self.tool_sandbox)
        workspace_status = self.safe_status(self.workspace_awareness)
        workspace_memory_status = self.safe_status(self.workspace_memory_link)
        gates = self.proposed_gates(normalized)
        safety = self.safety_assertions()

        return {
            "status": "planned",
            "plan_type": "codebase_validation_gate_plan",
            "target": normalized,
            "plan_state": "review_ready",
            "gate_count": len(gates),
            "gate_types": self.gate_types(),
            "gates": gates,
            "patch_packet_summary": {
                "status": patch_packet.get("status"),
                "proposal_type": patch_packet.get("proposal_type"),
                "proposal_only": patch_packet.get("proposal_only"),
                "metadata_only": patch_packet.get("metadata_only"),
                "file_read_performed": patch_packet.get("file_read_performed"),
                "file_write_performed": patch_packet.get("file_write_performed"),
                "command_execution_performed": patch_packet.get("command_execution_performed"),
                "candidate_surface_count": patch_packet.get("candidate_surface_count"),
                "patch_outline_count": patch_packet.get("patch_outline_count"),
            },
            "integration_ready": {
                "codebase_change": bool(codebase_change_status.get("planner_ready", codebase_change_status.get("status") == "online")),
                "patch_proposal": bool(patch_proposal_status.get("renderer_ready", patch_proposal_status.get("status") == "online")),
                "safe_file_operation": bool(safe_file_status.get("planner_ready", safe_file_status.get("status") == "online")),
                "project_intent": bool(project_intent_status.get("intent_ready", project_intent_status.get("status") == "online")),
                "workspace_awareness": bool(workspace_status.get("awareness_ready", workspace_status.get("status") == "online")),
                "workspace_memory_link": bool(workspace_memory_status.get("link_ready", workspace_memory_status.get("status") == "online")),
                "tool_sandbox": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            },
            **safety,
            "file_read_performed": False,
            "file_opened": False,
            "file_write_performed": False,
            "file_edit_performed": False,
            "patch_apply_performed": False,
            "command_execution_performed": False,
            "test_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "review_notes": [
                "This planner proposes gates only.",
                "No validation commands are executed automatically.",
                "No files are opened or modified automatically.",
                "Commit/push remain human-controlled and explicit.",
            ],
        }

    def preflight_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][0]

    def static_validation_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][1]

    def registry_validation_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][2]

    def runtime_smoke_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][3]

    def diff_review_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][4]

    def rollback_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][5]

    def commit_push_gate(self, target: str) -> dict[str, Any]:
        return self.validation_gate_plan(target)["gates"][6]

    def status(self) -> dict[str, Any]:
        read_project_permission = self.permission_manager.check("read_project")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")
        patch_status = self.safe_status(self.patch_proposal)
        change_status = self.safe_status(self.codebase_change)
        sandbox_status = self.safe_status(self.tool_sandbox)
        safety = self.safety_assertions()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "gate_planner_ready": True,
            "planner_ready": True,
            "validation_gate_plan_ready": True,
            "preflight_gate_ready": True,
            "static_validation_gate_ready": True,
            "registry_validation_gate_ready": True,
            "runtime_smoke_gate_ready": True,
            "diff_review_gate_ready": True,
            "rollback_gate_ready": True,
            "commit_push_gate_ready": True,
            "context_ready": True,
            "gate_count": len(self.gate_types()),
            "gate_types": self.gate_types(),
            "patch_proposal_integration_ready": bool(patch_status.get("renderer_ready", patch_status.get("status") == "online")),
            "codebase_change_integration_ready": bool(change_status.get("planner_ready", change_status.get("status") == "online")),
            "tool_sandbox_integration_ready": bool(sandbox_status.get("sandbox_ready", sandbox_status.get("status") in {"foundation", "online"})),
            "tool_sandbox_dry_run_ready": bool(sandbox_status.get("dry_run_ready", False)),
            "tool_sandbox_real_execution_ready": bool(sandbox_status.get("real_execution_ready", False)),
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_prepare_confirmation": prepare_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            **safety,
            "project_root": str(self.project_root),
            "note": "Codebase Validation Gate Planner is online for proposal-only validation gates. It does not read, open, write, edit, apply patches, execute commands, run tests, commit, or push automatically.",
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
            "test_execution_performed": False,
            "git_commit_performed": False,
            "git_push_performed": False,
            "external_action_performed": False,
            "real_tool_execution_performed": False,
            "gate_planner_status": status,
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            "gate_types": self.gate_types(),
            "note": "Validation gate context is metadata-only and proposal-only.",
        }
