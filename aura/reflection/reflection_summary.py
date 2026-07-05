from dataclasses import dataclass, field
from typing import Any


@dataclass
class ReflectionSummary:
    """
    Read-only reflection summary for AURA memory and project journal.
    """

    title: str
    status: str
    memory_count: int
    journal_count: int
    milestone_count: int
    recent_milestones: list[str] = field(default_factory=list)
    memory_highlights: list[str] = field(default_factory=list)
    project_insights: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "status": self.status,
            "memory_count": self.memory_count,
            "journal_count": self.journal_count,
            "milestone_count": self.milestone_count,
            "recent_milestones": self.recent_milestones,
            "memory_highlights": self.memory_highlights,
            "project_insights": self.project_insights,
            "safety_notes": self.safety_notes,
            "metadata": self.metadata,
        }
