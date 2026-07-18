from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import sys

from .permission_audit_action_visibility_ux_contract import (
    PermissionAuditActionVisibilityUxContract,
)
from .permission_audit_action_visibility_ux_planner import (
    PermissionAuditActionVisibilityUxPlanner,
)
from .permission_audit_action_visibility_ux_runtime_manager import (
    PermissionAuditActionVisibilityUxRuntimeManager,
)


class PermissionAuditActionVisibilityUxCLI:
    COMMANDS = (
        "permission-audit-action-visibility-ux-status",
        "permission-audit-action-visibility-ux-check",
        "permission-audit-action-visibility-ux-context",
        "permission-audit-action-visibility-ux-review",
        "permission-audit-action-visibility-ux-preview",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def run_command(
        self,
        command: str,
    ) -> dict[str, Any]:
        planner = PermissionAuditActionVisibilityUxPlanner(
            project_root=self.project_root
        )
        contract = PermissionAuditActionVisibilityUxContract(
            project_root=self.project_root
        )
        runtime = PermissionAuditActionVisibilityUxRuntimeManager(
            project_root=self.project_root
        )

        mapping = {
            "permission-audit-action-visibility-ux-status":
            planner.status,
            "permission-audit-action-visibility-ux-check":
            contract.check,
            "permission-audit-action-visibility-ux-context":
            planner.context,
            "permission-audit-action-visibility-ux-review":
            contract.review,
            "permission-audit-action-visibility-ux-preview":
            contract.preview,
        }
        if command not in mapping:
            raise ValueError(
                "Unknown Sprint 268 command: "
                + command
            )

        packet = mapping[command]()
        return {
            "command": command,
            "version": "1.2.8",
            "current_sprint": 268,
            "next_sprint": 269,
            "boundary": (
                "permission_audit_action_visibility_ux"
            ),
            "next_boundary": "daily_use_acceptance_rehearsal_and_release_harness",
            "runtime_status": runtime.status(),
            "packet": packet,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }


def main(
    argv: list[str] | None = None,
) -> int:
    arguments = list(
        argv
        if argv is not None
        else sys.argv[1:]
    )
    command = (
        arguments[0]
        if arguments
        else "permission-audit-action-visibility-ux-status"
    )
    packet = PermissionAuditActionVisibilityUxCLI().run_command(
        command
    )
    print(
        json.dumps(
            packet,
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
