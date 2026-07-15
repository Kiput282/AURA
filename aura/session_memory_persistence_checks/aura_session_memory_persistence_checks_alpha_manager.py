"""Sprint 244 persistence-check owner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_session_memory_persistence_checks_planner import (
    AuraSessionMemoryPersistenceChecksPlanner,
)


class AuraSessionMemoryPersistenceChecksAlphaManager:
    """Expose the read-only Sprint 244 contract."""

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.planner = (
            AuraSessionMemoryPersistenceChecksPlanner(
                project_root=project_root
            )
        )

    def status(
        self,
    ) -> dict[str, Any]:
        return self.planner.status()

    def context(
        self,
    ) -> dict[str, Any]:
        return self.planner.context()

    def check(
        self,
    ) -> dict[str, Any]:
        packet = self.planner.check()
        packet["alpha_ready"] = (
            packet["planning_ready"]
            and packet[
                "failed_assertion_count"
            ]
            == 0
        )
        return packet


__all__ = [
    "AuraSessionMemoryPersistenceChecksAlphaManager",
]
