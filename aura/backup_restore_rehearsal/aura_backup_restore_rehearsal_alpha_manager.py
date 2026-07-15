from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_backup_restore_rehearsal_planner import (
    AuraBackupRestoreRehearsalPlanner,
)


class AuraBackupRestoreRehearsalAlphaManager:
    def __init__(self, project_root: Path) -> None:
        self.planner = AuraBackupRestoreRehearsalPlanner(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def review(self) -> dict[str, Any]:
        return self.planner.review()

    def check(self) -> dict[str, Any]:
        return self.planner.check()
