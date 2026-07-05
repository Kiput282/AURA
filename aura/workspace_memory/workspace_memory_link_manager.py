from pathlib import Path
from typing import Any

import yaml

from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.permissions.permission_manager import PermissionManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager


class WorkspaceMemoryLinkManager:
    """
    AURA Workspace Memory Link.

    Current phase:
    - connect workspace awareness with memory context safely
    - prepare workspace memory summaries
    - prepare project memory candidates
    - prepare important file memory candidates
    - prepare recent milestone memory candidates
    - expose safe memory link context
    - never writes memory automatically
    - never deletes memory automatically
    - never writes journal automatically
    - never writes files automatically
    - never executes commands
    """

    name = "workspace_memory_link"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.permission_manager = PermissionManager()
        self.workspace_awareness = WorkspaceAwarenessManager(project_root=self.project_root)
        self.memory_store = MemoryStore(project_root=self.project_root)
        self.project_journal = ProjectJournal(project_root=self.project_root)
        self.memory_reflection = MemoryReflectionManager(project_root=self.project_root)

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

    def candidate_types(self) -> list[str]:
        return [
            "project_state",
            "important_file",
            "recent_milestone",
            "workspace_context",
        ]

    def latest_milestone(self) -> dict[str, Any] | None:
        milestones = self.memory_reflection.extract_milestones(journal_limit=500)

        if not milestones:
            return None

        return milestones[-1]

    def recent_milestones(self, limit: int = 6) -> list[dict[str, Any]]:
        return self.memory_reflection.extract_milestones(journal_limit=max(1, min(limit, 20)))[-limit:]

    def memory_highlights(self, limit: int = 6) -> list[dict[str, Any]]:
        return self.memory_reflection.memory_highlights(limit=max(1, min(limit, 20)))

    def build_candidate(
        self,
        candidate_type: str,
        content: str,
        reason: str,
        importance: int = 3,
        pinned: bool = False,
        source: str = "workspace_memory_link",
    ) -> dict[str, Any]:
        return {
            "candidate_type": candidate_type,
            "kind": "workspace_memory_candidate",
            "content": content,
            "reason": reason,
            "metadata": {
                "source": source,
                "suggested_importance": max(1, min(importance, 5)),
                "suggested_pinned": pinned,
                "candidate_only": True,
                "requires_user_confirmation": True,
            },
            "write_ready": False,
            "written": False,
            "memory_write_performed": False,
            "memory_delete_performed": False,
        }

    def summary(self) -> dict[str, Any]:
        workspace_context = self.workspace_awareness.context()
        current_state = workspace_context["current_state"]
        reflection_status = self.memory_reflection.status()
        latest = self.latest_milestone()

        summary_text = (
            f"AURA workspace is at version {current_state['version']} "
            f"on branch {current_state['git_branch']} with "
            f"{current_state['python_files']} Python files, "
            f"{current_state['memory_records']} memory records, "
            f"{current_state['journal_entries']} journal entries, and "
            f"latest milestone {latest['title'] if latest else 'unknown'}."
        )

        return {
            "status": self.status_name,
            "summary_ready": True,
            "summary": summary_text,
            "workspace_summary": workspace_context["workspace_summary"],
            "current_state": current_state,
            "memory_count": self.memory_store.count(),
            "journal_count": self.project_journal.count(),
            "milestone_count": reflection_status["milestone_count"],
            "latest_milestone": latest,
            "memory_highlights": self.memory_highlights(limit=6),
            "read_only": True,
            "write_performed": False,
            "memory_write_performed": False,
            "memory_delete_performed": False,
            "journal_write_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Workspace memory summary is read-only. It prepares context but does not write memory, journal, files, or commands.",
        }

    def project_memory_candidates(self, topic: str) -> dict[str, Any]:
        cleaned_topic = self.normalize_text(topic) or "AURA project state"
        workspace_context = self.workspace_awareness.context()
        current_state = workspace_context["current_state"]
        latest = self.latest_milestone()

        candidates = [
            self.build_candidate(
                candidate_type="project_state",
                content=(
                    f"AURA workspace state: version {current_state['version']}, "
                    f"codename {current_state['codename']}, branch {current_state['git_branch']}, "
                    f"latest commit hint {current_state['latest_commit_hint']}, "
                    f"current sprint {current_state['current_sprint'] or 'unknown'}."
                ),
                reason="Keeps current workspace identity and sprint state available for future context.",
                importance=4,
                pinned=False,
            ),
            self.build_candidate(
                candidate_type="workspace_context",
                content=workspace_context["workspace_summary"],
                reason="Condenses workspace awareness into a memory candidate without writing it.",
                importance=3,
                pinned=False,
            ),
        ]

        if latest:
            candidates.append(
                self.build_candidate(
                    candidate_type="recent_milestone",
                    content=f"Latest AURA milestone: {latest['title']} — {latest['content']}",
                    reason="Keeps the most recent sprint milestone visible as a candidate.",
                    importance=4,
                    pinned=False,
                )
            )

        return self.base_candidate_result(
            plan_type="workspace_memory_candidates",
            target=cleaned_topic,
            candidates=candidates,
            recommended_steps=[
                "Review whether each candidate is useful for long-term project memory.",
                "Keep only stable project facts, not temporary terminal details.",
                "Prefer important milestones, pinned context, and durable architecture decisions.",
                "Do not write memory automatically.",
                "Use explicit memory commands later if Kiput approves saving a candidate.",
            ],
        )

    def file_memory_candidates(self, topic: str) -> dict[str, Any]:
        cleaned_topic = self.normalize_text(topic) or "important project files"
        important_files = self.workspace_awareness.important_files()

        candidates: list[dict[str, Any]] = []

        for item in important_files:
            if not item["exists"]:
                continue

            candidates.append(
                self.build_candidate(
                    candidate_type="important_file",
                    content=f"Important AURA project file: {item['path']} — {item['reason']}",
                    reason="Important project files are useful durable navigation context.",
                    importance=3,
                    pinned=False,
                    source="workspace_important_files",
                )
            )

        return self.base_candidate_result(
            plan_type="workspace_file_memory_candidates",
            target=cleaned_topic,
            candidates=candidates[:20],
            recommended_steps=[
                "Review important file candidates before deciding what belongs in memory.",
                "Keep only stable file roles that help future navigation.",
                "Avoid storing every file path if the workspace map already covers it.",
                "Do not write memory or files automatically.",
                "Use explicit memory save flow later if Kiput approves.",
            ],
        )

    def milestone_memory_candidates(self, topic: str) -> dict[str, Any]:
        cleaned_topic = self.normalize_text(topic) or "recent sprint milestones"
        milestones = self.recent_milestones(limit=8)

        candidates = [
            self.build_candidate(
                candidate_type="recent_milestone",
                content=f"{milestone['title']}: {milestone['content']}",
                reason="Recent sprint milestones are durable project progress context.",
                importance=4 if index >= len(milestones) - 3 else 3,
                pinned=False,
                source="project_journal",
            )
            for index, milestone in enumerate(milestones)
        ]

        return self.base_candidate_result(
            plan_type="workspace_milestone_memory_candidates",
            target=cleaned_topic,
            candidates=candidates,
            recommended_steps=[
                "Review milestone candidates for durable value.",
                "Prefer saving only milestone summaries that remain useful across sessions.",
                "Avoid duplicating journal content unless it should be elevated into memory.",
                "Do not write journal or memory automatically.",
                "Use explicit confirmation before creating any memory item.",
            ],
        )

    def base_candidate_result(
        self,
        plan_type: str,
        target: str,
        candidates: list[dict[str, Any]],
        recommended_steps: list[str],
    ) -> dict[str, Any]:
        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        prepare_permission = self.permission_manager.check("prepare_file")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "status": "planned",
            "plan_type": plan_type,
            "target": target,
            "plan_state": "proposal_ready",
            "candidate_count": len(candidates),
            "candidates": candidates,
            "recommended_steps": recommended_steps,
            "permissions": {
                "read_project": read_project_permission.to_dict(),
                "read_memory": read_memory_permission.to_dict(),
                "prepare_file": prepare_permission.to_dict(),
                "write_file": write_permission.to_dict(),
                "run_command": command_permission.to_dict(),
            },
            "execution_ready": False,
            "executed": False,
            "read_only": True,
            "memory_write_performed": False,
            "memory_delete_performed": False,
            "journal_write_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "safety_notes": [
                "Workspace memory link plan is proposal-only.",
                "No memory was written.",
                "No memory was deleted.",
                "No journal entry was written.",
                "No file was written.",
                "No command was executed.",
                "Future memory writes require explicit user confirmation.",
            ],
        }

    def context(self) -> dict[str, Any]:
        status = self.status()

        return {
            "status": self.status_name,
            "context_ready": True,
            "link_status": status,
            "identity": self.load_identity(),
            "workspace_context": self.workspace_awareness.context(),
            "summary": self.summary(),
            "reflection_context": self.memory_reflection.reflection_context(limit=8),
            "memory_highlights": self.memory_highlights(limit=8),
            "recent_milestones": self.recent_milestones(limit=8),
            "safe_current_capabilities": [
                "workspace_memory_link_status",
                "workspace_memory_summary",
                "workspace_memory_candidates",
                "workspace_file_memory_candidates",
                "workspace_milestone_memory_candidates",
                "workspace_memory_link_context",
            ],
            "disabled_capabilities": [
                "automatic_memory_write",
                "automatic_memory_delete",
                "automatic_journal_write",
                "automatic_file_write",
                "command_execution",
                "external_action_execution",
            ],
            "read_only": True,
            "write_performed": False,
            "memory_write_performed": False,
            "memory_delete_performed": False,
            "journal_write_performed": False,
            "file_write_performed": False,
            "command_execution_performed": False,
            "external_action_execution_performed": False,
            "note": "Workspace Memory Link context is read-only and candidate-only.",
        }

    def status(self) -> dict[str, Any]:
        workspace_status = self.workspace_awareness.status()
        reflection_status = self.memory_reflection.status()

        read_project_permission = self.permission_manager.check("read_project")
        read_memory_permission = self.permission_manager.check("read_memory")
        write_permission = self.permission_manager.check("write_file")
        command_permission = self.permission_manager.check("run_command")

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "link_ready": True,
            "summary_ready": True,
            "memory_candidates_ready": True,
            "file_memory_candidates_ready": True,
            "milestone_candidates_ready": True,
            "context_ready": True,
            "workspace_integration_ready": workspace_status["awareness_ready"],
            "memory_store_ready": True,
            "journal_integration_ready": True,
            "reflection_integration_ready": reflection_status["reflection_ready"],
            "memory_count": self.memory_store.count(),
            "journal_count": self.project_journal.count(),
            "milestone_count": reflection_status["milestone_count"],
            "important_file_count": workspace_status["important_file_count"],
            "candidate_types": len(self.candidate_types()),
            "requires_read_project_confirmation": read_project_permission.requires_confirmation,
            "requires_read_memory_confirmation": read_memory_permission.requires_confirmation,
            "requires_write_confirmation": write_permission.requires_confirmation,
            "requires_command_confirmation": command_permission.requires_confirmation,
            "runtime_ready": False,
            "read_only": True,
            "candidate_only": True,
            "memory_write": False,
            "memory_delete": False,
            "journal_write": False,
            "file_write": False,
            "command_execution": False,
            "external_action_execution": False,
            "real_tool_execution": False,
            "sections": 6,
            "project_root": str(self.project_root),
            "note": "Workspace Memory Link is online for safe workspace-memory candidate planning. It does not write memory, delete memory, write journal entries, write files, or execute commands automatically.",
        }
