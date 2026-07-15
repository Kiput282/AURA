"""Sprint 245 alpha owner."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_log_rotation_storage_cleanup_planner import (
    AuraLogRotationStorageCleanupPlanner,
)


class AuraLogRotationStorageCleanupAlphaManager:
    def __init__(self, project_root: Path) -> None:
        self.planner = AuraLogRotationStorageCleanupPlanner(project_root)

    def status(self) -> dict[str, Any]:
        return self.planner.status()

    def context(self) -> dict[str, Any]:
        return self.planner.context()

    def cleanup_preview(self) -> dict[str, Any]:
        return self.planner.cleanup_preview()

    def check(self) -> dict[str, Any]:
        return self.planner.check()
