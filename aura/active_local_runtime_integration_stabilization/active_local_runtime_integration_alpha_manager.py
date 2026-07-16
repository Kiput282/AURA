from __future__ import annotations

from pathlib import Path
from typing import Any

from .active_local_runtime_integration_planner import (
    ActiveLocalRuntimeIntegrationPlanner,
)


class ActiveLocalRuntimeIntegrationAlphaManager:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.planner = ActiveLocalRuntimeIntegrationPlanner(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def check(self) -> dict[str, Any]:
        return self.planner.check()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def integration_preview(self) -> dict[str, Any]:
        return self.planner.integration_preview()

    def chat_turn_preview(self) -> dict[str, Any]:
        return self.planner.chat_turn_preview()

    def stop_restore_preview(self) -> dict[str, Any]:
        return self.planner.stop_restore_preview()

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.planner.isolated_rehearsal()
