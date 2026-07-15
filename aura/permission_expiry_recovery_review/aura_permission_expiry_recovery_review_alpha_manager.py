from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_permission_expiry_recovery_review_planner import (
    AuraPermissionExpiryRecoveryReviewPlanner,
)


class AuraPermissionExpiryRecoveryReviewAlphaManager:
    def __init__(self, project_root: Path) -> None:
        self.planner = AuraPermissionExpiryRecoveryReviewPlanner(
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

