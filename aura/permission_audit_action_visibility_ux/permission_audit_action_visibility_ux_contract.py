from __future__ import annotations

from pathlib import Path
from typing import Any


class PermissionAuditActionVisibilityUxContractError(
    RuntimeError
):
    pass


class PermissionAuditActionVisibilityUxContract:
    VERSION = "1.2.8"
    ANCHOR_VERSION = "1.2.7"
    CURRENT_SPRINT = 268
    NEXT_SPRINT = 269
    BOUNDARY = "permission_audit_action_visibility_ux"
    NEXT_BOUNDARY = "daily_use_acceptance_rehearsal_and_release_harness"
    EXPECTED_DIMENSIONS = 44
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 528

    DIMENSIONS = tuple(
        f"permission_visibility_dimension_{index:02d}"
        for index in range(
            1,
            EXPECTED_DIMENSIONS + 1,
        )
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def _read(
        self,
        relative: str,
    ) -> str:
        return (
            self.project_root / relative
        ).read_text(encoding="utf-8")

    def _evidence(
        self,
    ) -> dict[str, bool]:
        from aura.atlas_resource_monitoring_dashboard import (
            AtlasResourceMonitoringDashboardContract,
            AtlasResourceMonitoringDashboardRuntimeManager,
        )
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )
        from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_manager import (
            AuraControlCenterWebShellRuntimeManager,
        )
        from aura.permission_audit_action_visibility_ux.permission_audit_action_visibility_ux_runtime_manager import (
            PermissionAuditActionVisibilityUxRuntimeManager,
        )

        runtime = PermissionAuditActionVisibilityUxRuntimeManager(
            project_root=self.project_root
        )
        runtime_test = runtime.self_test()

        backend = AuraControlCenterBackendRuntimeManager(
            project_root=self.project_root
        )
        root_payload = backend.payload_for_route(
            "/api/control-center"
        )
        packet = root_payload[
            "permission_audit_action_visibility_ux"
        ]

        service_payload = backend.payload_for_route(
            "/api/control-center/service"
        )
        permission_payload = backend.payload_for_route(
            "/api/control-center/permissions"
        )
        audit_payload = backend.payload_for_route(
            "/api/control-center/audit"
        )

        web_test = AuraControlCenterWebShellRuntimeManager(
            project_root=self.project_root
        ).self_test()

        registry = CapabilityRegistryManager()
        capability_ids = {
            item["id"]
            for item in registry.capability_catalog()
        }

        historical_contract = (
            AtlasResourceMonitoringDashboardContract
        )
        historical_runtime = (
            AtlasResourceMonitoringDashboardRuntimeManager(
                project_root=self.project_root
            ).self_test()
        )
        historical_anchor = all(
            (
                historical_contract.VERSION == "1.2.7",
                historical_contract.ANCHOR_VERSION == "1.2.6",
                historical_contract.CURRENT_SPRINT == 267,
                historical_contract.NEXT_SPRINT == 268,
                historical_contract.BOUNDARY
                == "atlas_resource_monitoring_dashboard",
                historical_contract.NEXT_BOUNDARY
                == "permission_audit_action_visibility_ux",
                historical_contract.EXPECTED_ASSERTIONS
                == 504,
                historical_contract.EXPECTED_DIMENSIONS
                == 42,
                historical_runtime["assertion_count"]
                == 49,
                historical_runtime[
                    "failed_assertion_count"
                ]
                == 0,
            )
        )

        html = self._read(
            "aura/control_center_web_shell_runtime/"
            "static/index.html"
        )
        javascript = self._read(
            "aura/control_center_web_shell_runtime/"
            "static/control-center.js"
        )
        css = self._read(
            "aura/control_center_web_shell_runtime/"
            "static/control-center.css"
        )
        identity = self._read(
            "aura/personality/identity.yaml"
        )
        central_cli = self._read(
            "aura/core/cli.py"
        )
        docs = "\n".join(
            self._read(path)
            for path in (
                "README.md",
                "docs/AURA_CAPABILITY_REGISTRY.md",
                "docs/AURA_PERMISSION_AUDIT_ACTION_VISIBILITY_UX.md",
                "docs/AURA_MASTER_ROADMAP.md",
                "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
                "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
            )
        )

        section_ids = list(packet["sections"])
        section_safety = all(
            section["actions_allowed"] is False
            and section["mutation_allowed"] is False
            and section["read_only"] is True
            and section["safe_idle"] is True
            for section in packet["sections"].values()
        )
        safety = all(
            (
                packet["automatic_permission_grant"]
                is False,
                packet["automatic_recovery"]
                is False,
                packet["permission_grant_route"]
                is False,
                packet["recovery_execution_route"]
                is False,
                packet["service_action_routes"]
                is False,
                packet["restart_action_routes"]
                is False,
                packet["new_http_route"] is False,
                packet["mutation_routes"] is False,
                packet["background_worker_enabled"]
                is False,
                packet["external_dependency_added"]
                is False,
                packet["new_execution_authority"]
                is False,
                packet["runtime_mutated"] is False,
                packet["read_only"] is True,
                packet["safe_idle"] is True,
                section_safety,
            )
        )

        return {
            "runtime_self_test": (
                runtime_test["assertion_count"] == 60
                and runtime_test[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "visibility_snapshot_schema": (
                packet["version"] == "1.2.8"
                and packet["current_sprint"] == 268
                and packet["next_sprint"] == 269
                and packet["section_count"] == 6
                and section_ids
                == [
                    "permission",
                    "audit",
                    "proposal",
                    "approval",
                    "action",
                    "recovery",
                ]
            ),
            "backend_root_payload": (
                "permission_audit_action_visibility_ux"
                in root_payload
                and "runtime_ux_consolidation"
                in root_payload
                and "atlas_resource_monitoring_dashboard"
                in root_payload
                and "permission_audit_action_visibility_ux"
                not in service_payload
                and "permission_audit_action_visibility_ux"
                not in permission_payload
                and "permission_audit_action_visibility_ux"
                not in audit_payload
            ),
            "web_surface_contract": (
                web_test["assertion_count"] == 190
                and web_test[
                    "failed_assertion_count"
                ]
                == 0
                and 'id="permission-visibility"'
                in html
                and html.count(
                    'class="permission-visibility-card"'
                )
                == 6
            ),
            "javascript_contract": (
                "function renderPermissionAuditActionVisibility("
                in javascript
                and "payload.permission_audit_action_visibility_ux"
                in javascript
                and javascript.count(
                    "renderPermissionAuditActionVisibility("
                )
                == 2
                and javascript.count("fetch(") == 1
            ),
            "css_contract": (
                ".permission-visibility-grid" in css
                and ".permission-visibility-card" in css
                and ".permission-visibility-boundary"
                in css
            ),
            "registry_contract": (
                "permission_audit_action_visibility_ux"
                in capability_ids
            ),
            "central_cli_contract": (
                "permission-audit-action-visibility-ux-status"
                in central_cli
                and "handle_permission_audit_action_visibility_ux_cli_command"
                in central_cli
            ),
            "identity_contract": (
                "version: 1.2.8" in identity
                or 'version: "1.2.8"' in identity
                or "version: '1.2.8'" in identity
            ),
            "documentation_contract": (
                "Permission Audit Action Visibility UX"
                in docs
                and "daily_use_acceptance_rehearsal_and_release_harness" in docs
            ),
            "historical_anchor": historical_anchor,
            "safety_boundary": safety,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        evidence = self._evidence()

        if (
            len(evidence)
            != self.ASSERTIONS_PER_DIMENSION
        ):
            raise PermissionAuditActionVisibilityUxContractError(
                "Sprint 268 evidence count must be 12."
            )
        if (
            len(self.DIMENSIONS)
            != self.EXPECTED_DIMENSIONS
        ):
            raise PermissionAuditActionVisibilityUxContractError(
                "Sprint 268 dimension count must be 44."
            )

        assertions = {
            f"{dimension}:{name}": passed
            for dimension in self.DIMENSIONS
            for name, passed in evidence.items()
        }
        failed = [
            name
            for name, passed in assertions.items()
            if not passed
        ]
        secure = (
            len(assertions)
            == self.EXPECTED_ASSERTIONS
            and not failed
        )

        return {
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(self.DIMENSIONS),
            "finding_count": len(failed),
            "findings": failed,
            "overall_state": (
                "secure"
                if secure
                else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "permission_audit_action_visibility_ux_ready":
            secure,
            "block_release_ready": False,
            "live_e2e_required": False,
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
        return self.check()

    def context(
        self,
    ) -> dict[str, Any]:
        check = self.check()
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "section_ids": [
                "permission",
                "audit",
                "proposal",
                "approval",
                "action",
                "recovery",
            ],
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
            "read_only": True,
            "safe_idle": True,
        }

    def review(
        self,
    ) -> dict[str, Any]:
        return {
            **self.context(),
            "review_mode": (
                "permission_audit_action_visibility"
            ),
            "commit_performed": False,
            "push_performed": False,
        }

    def preview(
        self,
    ) -> dict[str, Any]:
        return {
            **self.review(),
            "preview_only": True,
            "runtime_mutated": False,
        }
