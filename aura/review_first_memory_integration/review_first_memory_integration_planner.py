from __future__ import annotations

from pathlib import Path
from typing import Any

from .review_first_memory_integration_contract import (
    ReviewFirstMemoryIntegrationContract,
)


class ReviewFirstMemoryIntegrationPlanner:
    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.contract = ReviewFirstMemoryIntegrationContract(
            project_root=project_root
        )

    def status(self) -> dict[str, Any]:
        return self.contract.status()

    def context(self) -> dict[str, Any]:
        return self.contract.context()

    def check(self) -> dict[str, Any]:
        return self.contract.check()

    def review(self) -> dict[str, Any]:
        return self.contract.review()

    def preview(self) -> dict[str, Any]:
        return self.contract.preview()
