from pathlib import Path
from typing import Any

import yaml

from aura.briefing.daily_briefing import DailyBriefing
from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.model_router.model_router import ModelRouter
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager


class DailyBriefingManager:
    """
    Daily Project Briefing.

    Current phase:
    - read project identity
    - read journal and reflection
    - summarize current project status
    - summarize safety state
    - recommend next steps
    - no file writes
    - no memory writes
    - no command execution
    """

    name = "daily_project_briefing"
    version = "0.1.0"
    status_name = "online"

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.memory_store = MemoryStore(project_root=self.project_root)
        self.project_journal = ProjectJournal(project_root=self.project_root)
        self.memory_reflection = MemoryReflectionManager(project_root=self.project_root)
        self.tool_sandbox = ToolSandboxManager(project_root=self.project_root)
        self.project_coding = ProjectCodingManager(project_root=self.project_root)
        self.model_router = ModelRouter(project_root=self.project_root)

    def load_identity(self) -> dict[str, Any]:
        if not self.identity_path.exists():
            return {}

        content = self.identity_path.read_text(encoding="utf-8")
        data = yaml.safe_load(content)

        if not isinstance(data, dict):
            return {}

        return data

    def latest_milestone(self) -> dict[str, Any] | None:
        milestones = self.memory_reflection.extract_milestones(journal_limit=500)

        if not milestones:
            return None

        return milestones[-1]

    def safety_state(self) -> dict[str, Any]:
        sandbox_status = self.tool_sandbox.status()
        project_coding_status = self.project_coding.status()
        reflection_status = self.memory_reflection.status()

        return {
            "tool_sandbox": sandbox_status["status"],
            "tool_sandbox_ready": sandbox_status["sandbox_ready"],
            "real_tool_execution": sandbox_status["real_execution_ready"],
            "project_coding": project_coding_status["status"],
            "project_patch_planning": project_coding_status["patch_planning_ready"],
            "project_file_write": project_coding_status["file_write_ready"],
            "memory_reflection": reflection_status["status"],
            "memory_reflection_write": reflection_status["automatic_memory_write"],
            "memory_reflection_delete": reflection_status["automatic_memory_delete"],
            "memory_reflection_merge": reflection_status["automatic_memory_merge"],
            "safe_action_execution": False,
        }

    def status(self) -> dict[str, Any]:
        identity = self.load_identity()
        reflection_status = self.memory_reflection.status()
        sandbox_status = self.tool_sandbox.status()
        project_coding_status = self.project_coding.status()
        latest_milestone = self.latest_milestone()

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "briefing_ready": True,
            "compact_ready": True,
            "context_ready": True,
            "journal_read_ready": True,
            "reflection_read_ready": reflection_status["reflection_ready"],
            "system_summary_ready": True,
            "automatic_file_write": False,
            "automatic_memory_write": False,
            "automatic_journal_write": False,
            "command_execution": False,
            "aura_version": identity.get("version", "unknown"),
            "memory_count": reflection_status["memory_count"],
            "journal_count": reflection_status["journal_count"],
            "milestone_count": reflection_status["milestone_count"],
            "latest_milestone": latest_milestone["title"] if latest_milestone else "",
            "project_python_files": project_coding_status["python_files"],
            "real_tool_execution": sandbox_status["real_execution_ready"],
            "briefing_sections": 7,
            "project_root": str(self.project_root),
            "note": "Daily Project Briefing is online for read-only project summaries. It does not write files, write memory, write journal entries, or execute commands.",
        }

    def project_summary(self) -> str:
        status = self.status()
        latest = status["latest_milestone"] or "no milestone yet"

        return (
            f"AURA {status['aura_version']} is in Genesis phase with "
            f"{status['journal_count']} journal entries, "
            f"{status['milestone_count']} detected milestones, "
            f"{status['memory_count']} memory records, and latest milestone {latest}."
        )

    def recommended_next_steps(self, latest_milestone: dict[str, Any] | None) -> list[str]:
        steps = [
            "Review the latest milestone and reflection insights before starting the next sprint.",
            "Keep real tool execution disabled until confirmation and sandbox execution rules are mature.",
            "Use Project Coding Assistant v2 for patch planning before code changes.",
            "Use Memory Reflection to keep important context visible.",
            "Validate CLI, shell, system-status, boot, journal, git commit, and remote sync before closing each sprint.",
        ]

        if latest_milestone and "Sprint 44.0" in latest_milestone["title"]:
            steps.insert(
                0,
                "Complete Sprint 45.0 by validating Daily Project Briefing across CLI, shell, system-status, and journal.",
            )

        return steps

    def build(self, limit: int = 6) -> dict[str, Any]:
        limit = max(1, min(limit, 30))
        identity = self.load_identity()
        reflection = self.memory_reflection.reflect(limit=limit)
        latest_milestone = self.latest_milestone()
        safety = self.safety_state()

        briefing = DailyBriefing(
            title="AURA Daily Project Briefing",
            status=self.status_name,
            version=identity.get("version", "unknown"),
            project_summary=self.project_summary(),
            latest_milestone=latest_milestone,
            recent_milestones=reflection["recent_milestones"],
            memory_highlights=reflection["memory_highlights"],
            project_insights=reflection["project_insights"],
            safety_state=safety,
            recommended_next_steps=self.recommended_next_steps(latest_milestone),
            safety_notes=[
                "Briefing is read-only.",
                "No file was written.",
                "No memory was written.",
                "No journal entry was written.",
                "No command was executed.",
            ],
            metadata={
                "limit": limit,
                "write_performed": False,
                "memory_write_performed": False,
                "journal_write_performed": False,
                "command_execution_performed": False,
            },
        )

        return briefing.to_dict()

    def compact(self, limit: int = 4) -> dict[str, Any]:
        briefing = self.build(limit=limit)

        return {
            "title": briefing["title"],
            "status": briefing["status"],
            "version": briefing["version"],
            "project_summary": briefing["project_summary"],
            "latest_milestone": briefing["latest_milestone"],
            "top_insights": briefing["project_insights"][:3],
            "next_steps": briefing["recommended_next_steps"][:3],
            "safety_state": briefing["safety_state"],
            "write_performed": False,
            "command_execution_performed": False,
        }

    def context(self, limit: int = 5) -> dict[str, Any]:
        limit = max(1, min(limit, 20))
        briefing = self.build(limit=limit)

        return {
            "status": self.status_name,
            "context_ready": True,
            "project_summary": briefing["project_summary"],
            "latest_milestone": briefing["latest_milestone"],
            "recent_milestones": briefing["recent_milestones"],
            "memory_highlights": briefing["memory_highlights"],
            "project_insights": briefing["project_insights"],
            "safety_state": briefing["safety_state"],
            "recommended_next_steps": briefing["recommended_next_steps"],
            "write_performed": False,
            "command_execution_performed": False,
            "note": "Daily briefing context is prepared for future reasoning, but it does not modify files, memory, or journal.",
        }
