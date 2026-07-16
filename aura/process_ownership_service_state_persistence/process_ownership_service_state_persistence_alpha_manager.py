from __future__ import annotations

from pathlib import Path
from typing import Any

from .process_ownership_service_state_persistence_planner import (
    ProcessOwnershipServiceStatePersistencePlanner,
)


class ProcessOwnershipServiceStatePersistenceAlphaManager:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.planner = (
            ProcessOwnershipServiceStatePersistencePlanner(
                project_root=project_root
            )
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def inspect(self) -> dict[str, Any]:
        return self.planner.inspect()

    def recovery_preview(self) -> dict[str, Any]:
        return self.planner.recovery_preview()
