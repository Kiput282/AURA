from __future__ import annotations

from pathlib import Path
from typing import Any

from .chat_history_recovery_ux_contract import (
    ChatHistoryRecoveryUxContract,
)


class ChatHistoryRecoveryUxPlanner:
    def __init__(
        self,
        *,
        project_root: str | Path | None = None,
    ) -> None:
        self.contract = ChatHistoryRecoveryUxContract(
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

    def runtime_status(self) -> dict[str, Any]:
        return self.contract.manager.runtime_status()

    def route_status(self) -> dict[str, Any]:
        return self.contract.manager.route_status()

    def web_surface_status(self) -> dict[str, Any]:
        return self.contract.manager.web_surface_status()

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.contract.manager.isolated_rehearsal()
