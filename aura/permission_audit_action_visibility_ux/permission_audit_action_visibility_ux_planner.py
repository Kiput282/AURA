from __future__ import annotations

from pathlib import Path
from typing import Any

from .permission_audit_action_visibility_ux_contract import (
    PermissionAuditActionVisibilityUxContract,
)


class PermissionAuditActionVisibilityUxPlanner:
    VERSION = "1.2.8"
    CURRENT_SPRINT = 268
    NEXT_SPRINT = 269
    BOUNDARY = "permission_audit_action_visibility_ux"
    NEXT_BOUNDARY = "daily_use_acceptance_rehearsal_and_release_harness"

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def snapshot(
        self,
    ) -> dict[str, Any]:
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )

        backend = AuraControlCenterBackendRuntimeManager(
            project_root=self.project_root
        )
        packet = backend.payload_for_route(
            "/api/control-center"
        )[
            "permission_audit_action_visibility_ux"
        ]
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "status": packet["status"],
            "section_count": packet["section_count"],
            "available_section_count": packet[
                "available_section_count"
            ],
            "section_ids": list(packet["sections"]),
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "new_http_route": False,
            "new_external_dependency": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
            "safe_idle": True,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        check = PermissionAuditActionVisibilityUxContract(
            project_root=self.project_root
        ).check()
        return {
            **self.snapshot(),
            "status": (
                "ready"
                if check["status_valid"]
                else "degraded"
            ),
            "status_valid": check[
                "status_valid"
            ],
            "alpha_ready": check["alpha_ready"],
            "assertion_count": check[
                "assertion_count"
            ],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check[
                "dimension_count"
            ],
            "finding_count": check[
                "finding_count"
            ],
        }

    def context(
        self,
    ) -> dict[str, Any]:
        return {
            **self.status(),
            "scope": (
                "Consolidate permission, audit, proposal, "
                "approval, action, and recovery visibility "
                "without adding execution controls."
            ),
            "next_scope": self.NEXT_BOUNDARY,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        return PermissionAuditActionVisibilityUxContract(
            project_root=self.project_root
        ).check()
