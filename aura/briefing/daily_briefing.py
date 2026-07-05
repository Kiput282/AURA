from dataclasses import dataclass, field
from typing import Any


@dataclass
class DailyBriefing:
    """
    Read-only daily project briefing for AURA.
    """

    title: str
    status: str
    version: str
    project_summary: str
    latest_milestone: dict[str, Any] | None = None
    recent_milestones: list[str] = field(default_factory=list)
    memory_highlights: list[str] = field(default_factory=list)
    project_insights: list[str] = field(default_factory=list)
    safety_state: dict[str, Any] = field(default_factory=dict)
    recommended_next_steps: list[str] = field(default_factory=list)
    safety_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "status": self.status,
            "version": self.version,
            "project_summary": self.project_summary,
            "latest_milestone": self.latest_milestone,
            "recent_milestones": self.recent_milestones,
            "memory_highlights": self.memory_highlights,
            "project_insights": self.project_insights,
            "safety_state": self.safety_state,
            "recommended_next_steps": self.recommended_next_steps,
            "safety_notes": self.safety_notes,
            "metadata": self.metadata,
        }
