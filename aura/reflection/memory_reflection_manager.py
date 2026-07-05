import re
from pathlib import Path
from typing import Any

from aura.journal.project_journal import ProjectJournal
from aura.memory.memory_store import MemoryStore
from aura.reflection.reflection_summary import ReflectionSummary


class MemoryReflectionManager:
    """
    Memory Reflection System.

    Current phase:
    - read memory
    - read project journal
    - summarize milestones
    - generate lightweight insights
    - no automatic memory writes
    - no memory deletion or merging
    """

    name = "memory_reflection_system"
    version = "0.1.0"
    status_name = "online"

    MILESTONE_PATTERN = re.compile(r"Sprint\s+\d+(?:\.\d+)?", re.IGNORECASE)

    def __init__(self, project_root: Path):
        self.project_root = project_root.resolve()
        self.memory_store = MemoryStore(project_root=self.project_root)
        self.project_journal = ProjectJournal(project_root=self.project_root)

    def status(self) -> dict[str, Any]:
        memories = self.memory_store.list_all()
        journals = self.project_journal.list_all()
        pinned_memories = [
            memory
            for memory in memories
            if bool(memory.metadata.get("pinned", False))
        ]

        important_memories = [
            memory
            for memory in memories
            if int(memory.metadata.get("importance", 3)) >= 4
        ]

        milestones = self.extract_milestones(journal_limit=500)

        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "reflection_ready": True,
            "memory_read_ready": True,
            "journal_read_ready": True,
            "insight_generation_ready": True,
            "automatic_memory_write": False,
            "automatic_memory_delete": False,
            "automatic_memory_merge": False,
            "memory_count": len(memories),
            "journal_count": len(journals),
            "pinned_memory_count": len(pinned_memories),
            "important_memory_count": len(important_memories),
            "milestone_count": len(milestones),
            "project_root": str(self.project_root),
            "note": "Memory Reflection System is online for read-only reflection. It does not write, delete, or merge memories automatically.",
        }

    def extract_milestones(self, journal_limit: int = 20) -> list[dict[str, Any]]:
        entries = self.project_journal.list_recent(limit=journal_limit)
        milestones: list[dict[str, Any]] = []

        for entry in entries:
            title_match = self.MILESTONE_PATTERN.search(entry.title)
            content_match = self.MILESTONE_PATTERN.search(entry.content)

            if not title_match and not content_match:
                continue

            milestone_name = title_match.group(0) if title_match else content_match.group(0)

            milestones.append(
                {
                    "name": milestone_name,
                    "title": entry.title,
                    "content": entry.content,
                    "created_at": entry.created_at,
                    "journal_id": entry.id,
                }
            )

        return milestones

    def memory_highlights(self, limit: int = 8) -> list[dict[str, Any]]:
        memories = self.memory_store.list_all()

        sorted_memories = sorted(
            memories,
            key=lambda memory: (
                bool(memory.metadata.get("pinned", False)),
                int(memory.metadata.get("importance", 3)),
                memory.created_at,
            ),
            reverse=True,
        )

        highlights: list[dict[str, Any]] = []

        for memory in sorted_memories[: max(1, min(limit, 20))]:
            highlights.append(
                {
                    "id": memory.id,
                    "kind": memory.kind,
                    "content": memory.content,
                    "pinned": bool(memory.metadata.get("pinned", False)),
                    "importance": int(memory.metadata.get("importance", 3)),
                    "created_at": memory.created_at,
                }
            )

        return highlights

    def infer_project_themes(self, milestones: list[dict[str, Any]]) -> list[str]:
        text = " ".join(
            f"{milestone['title']} {milestone['content']}"
            for milestone in milestones
        ).lower()

        theme_keywords = {
            "memory": ["memory", "memori", "context", "reflection"],
            "safety": ["permission", "sandbox", "restricted", "safety", "safe"],
            "project_assistant": ["project", "coding", "code", "patch", "plugin"],
            "runtime": ["runtime", "voice", "vision", "avatar", "desktop"],
            "model": ["model", "router", "ollama", "llama"],
            "identity": ["identity", "motto", "creator", "aura"],
            "journal": ["journal", "milestone", "roadmap"],
        }

        themes: list[str] = []

        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                themes.append(theme)

        return themes

    def build_project_insights(
        self,
        milestones: list[dict[str, Any]],
        memory_highlights: list[dict[str, Any]],
    ) -> list[str]:
        insights: list[str] = []
        themes = self.infer_project_themes(milestones)

        if milestones:
            latest = milestones[-1]
            insights.append(
                f"Latest milestone detected: {latest['title']}."
            )

        if len(milestones) >= 5:
            insights.append(
                f"AURA has a sustained sprint history with {len(milestones)} milestone entries."
            )

        if "safety" in themes:
            insights.append(
                "Safety architecture is becoming a core project theme through permissions, sandboxing, and restricted execution."
            )

        if "project_assistant" in themes:
            insights.append(
                "Project assistance is evolving from read-only inspection toward structured coding plans."
            )

        if "runtime" in themes:
            insights.append(
                "Runtime capabilities are being planned in layers before real-world access is enabled."
            )

        if "model" in themes:
            insights.append(
                "Model routing is present as metadata foundation before real model switching."
            )

        pinned_count = sum(1 for memory in memory_highlights if memory["pinned"])
        if pinned_count:
            insights.append(
                f"{pinned_count} highlighted memory item(s) are pinned and should remain prominent in context."
            )

        if not insights:
            insights.append(
                "Not enough journal or memory data to infer strong project insights yet."
            )

        return insights

    def reflect(self, limit: int = 10) -> dict[str, Any]:
        limit = max(1, min(limit, 50))
        status = self.status()
        milestones = self.extract_milestones(journal_limit=limit)
        highlights = self.memory_highlights(limit=limit)
        insights = self.build_project_insights(
            milestones=milestones,
            memory_highlights=highlights,
        )

        summary = ReflectionSummary(
            title="AURA Memory Reflection",
            status=self.status_name,
            memory_count=status["memory_count"],
            journal_count=status["journal_count"],
            milestone_count=status["milestone_count"],
            recent_milestones=[
                f"{milestone['title']}: {milestone['content']}"
                for milestone in milestones
            ],
            memory_highlights=[
                memory["content"]
                for memory in highlights
            ],
            project_insights=insights,
            safety_notes=[
                "Reflection is read-only.",
                "No memory was written.",
                "No memory was deleted.",
                "No memory merge was performed.",
            ],
            metadata={
                "limit": limit,
                "pinned_memory_count": status["pinned_memory_count"],
                "important_memory_count": status["important_memory_count"],
                "automatic_memory_write": False,
            },
        )

        return summary.to_dict()

    def insights(self, limit: int = 12) -> dict[str, Any]:
        reflection = self.reflect(limit=limit)

        return {
            "status": self.status_name,
            "insights": reflection["project_insights"],
            "insight_count": len(reflection["project_insights"]),
            "safety_notes": reflection["safety_notes"],
            "write_performed": False,
            "delete_performed": False,
            "merge_performed": False,
        }

    def reflection_context(self, limit: int = 8) -> dict[str, Any]:
        limit = max(1, min(limit, 30))
        status = self.status()
        milestones = self.extract_milestones(journal_limit=limit)
        highlights = self.memory_highlights(limit=limit)

        return {
            "status": self.status_name,
            "memory_count": status["memory_count"],
            "journal_count": status["journal_count"],
            "milestones": milestones,
            "memory_highlights": highlights,
            "context_ready": True,
            "write_performed": False,
            "note": "Reflection context is prepared for future reasoning, but it does not modify memory.",
        }
