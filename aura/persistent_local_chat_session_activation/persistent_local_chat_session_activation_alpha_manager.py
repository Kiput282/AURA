from __future__ import annotations

from pathlib import Path
from typing import Any

from .persistent_local_chat_session_activation_planner import (
    PersistentLocalChatSessionActivationPlanner,
)


class PersistentLocalChatSessionActivationAlphaManager:
    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.planner = (
            PersistentLocalChatSessionActivationPlanner(
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

    def storage_posture(
        self,
    ) -> dict[str, Any]:
        return self.planner.storage_posture()

    def history_preview(
        self,
    ) -> dict[str, Any]:
        return self.planner.history_preview()

    def migration_preview(
        self,
    ) -> dict[str, Any]:
        return self.planner.migration_preview()

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        return self.planner.isolated_rehearsal()
