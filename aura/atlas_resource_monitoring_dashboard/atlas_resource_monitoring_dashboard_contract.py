from __future__ import annotations

from pathlib import Path
from typing import Any


class AtlasResourceMonitoringDashboardContractError(
    RuntimeError
):
    pass


class AtlasResourceMonitoringDashboardContract:
    VERSION = "1.2.7"
    ANCHOR_VERSION = "1.2.6"
    CURRENT_SPRINT = 267
    NEXT_SPRINT = 268
    BOUNDARY = "atlas_resource_monitoring_dashboard"
    NEXT_BOUNDARY = "permission_audit_action_visibility_ux"
    EXPECTED_DIMENSIONS = 42
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 504

    DIMENSIONS = tuple(
        f"atlas_resource_dashboard_dimension_{index:02d}"
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
        from aura.atlas_resource_monitoring_dashboard.atlas_resource_monitoring_dashboard_runtime_manager import (
            AtlasResourceMonitoringDashboardRuntimeManager,
        )
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )
        from aura.control_center_runtime_ux_consolidation.control_center_runtime_ux_consolidation_contract import (
            ControlCenterRuntimeUxConsolidationContract,
        )
        from aura.control_center_runtime_ux_consolidation.control_center_runtime_ux_consolidation_runtime_manager import (
            ControlCenterRuntimeUxConsolidationRuntimeManager,
        )
        from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_manager import (
            AuraControlCenterWebShellRuntimeManager,
        )

        runtime = (
            AtlasResourceMonitoringDashboardRuntimeManager(
                project_root=self.project_root
            )
        )
        runtime_test = runtime.self_test()
        snapshot = runtime.snapshot()

        backend = (
            AuraControlCenterBackendRuntimeManager(
                project_root=self.project_root
            )
        )
        root_payload = backend.payload_for_route(
            "/api/control-center"
        )
        resource = root_payload[
            "atlas_resource_monitoring_dashboard"
        ]

        web_test = (
            AuraControlCenterWebShellRuntimeManager(
                project_root=self.project_root
            ).self_test()
        )

        registry = CapabilityRegistryManager()
        capability_ids = {
            item["id"]
            for item in registry.capability_catalog()
        }

        historical_contract = (
            ControlCenterRuntimeUxConsolidationContract
        )
        historical_runtime = (
            ControlCenterRuntimeUxConsolidationRuntimeManager(
                project_root=self.project_root
            ).self_test()
        )
        historical_anchor = all(
            (
                historical_contract.VERSION == "1.2.6",
                historical_contract.ANCHOR_VERSION == "1.2.5",
                historical_contract.CURRENT_SPRINT == 266,
                historical_contract.NEXT_SPRINT == 267,
                historical_contract.BOUNDARY
                == "control_center_runtime_ux_consolidation",
                historical_contract.NEXT_BOUNDARY
                == "atlas_resource_monitoring_dashboard",
                historical_contract.EXPECTED_ASSERTIONS
                == 480,
                historical_contract.EXPECTED_DIMENSIONS
                == 40,
                historical_runtime["assertion_count"]
                == 40,
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
                "docs/AURA_ATLAS_RESOURCE_MONITORING_DASHBOARD.md",
                "docs/AURA_MASTER_ROADMAP.md",
                "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
                "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
            )
        )

        current = snapshot["current"]
        safety = all(
            (
                snapshot["background_sampler_enabled"]
                is False,
                snapshot["history_persistence_enabled"]
                is False,
                snapshot["network_access_enabled"]
                is False,
                snapshot["process_control_enabled"]
                is False,
                snapshot["command_execution_enabled"]
                is False,
                snapshot["systemd_mutation_enabled"]
                is False,
                snapshot["threshold_mutation_enabled"]
                is False,
                snapshot["new_execution_authority"]
                is False,
                snapshot["runtime_mutated"]
                is False,
                snapshot["read_only"] is True,
                snapshot["safe_idle"] is True,
            )
        )

        return {
            "runtime_self_test": (
                runtime_test["assertion_count"] == 49
                and runtime_test[
                    "failed_assertion_count"
                ]
                == 0
            ),
            "live_snapshot_schema": (
                snapshot["version"] == "1.2.7"
                and snapshot["current_sprint"] == 267
                and snapshot["rolling_windows_minutes"]
                == [5, 15, 60]
                and snapshot["mount_points"]
                == ["/", "/home", "/mnt/aura-data"]
                and len(current["storage"]) == 3
                and snapshot["sample_interval_seconds"]
                == 1.0
                and snapshot["ui_refresh_seconds"] == 1
            ),
            "backend_root_payload": (
                resource["version"] == "1.2.7"
                and resource["current_sprint"] == 267
                and resource["read_only"] is True
                and resource["safe_idle"] is True
                and "runtime_ux_consolidation"
                in root_payload
            ),
            "web_surface_contract": (
                web_test["assertion_count"] == 160
                and web_test[
                    "failed_assertion_count"
                ]
                == 0
                and 'id="resources"' in html
                and 'id="resource-storage-list"'
                in html
            ),
            "javascript_contract": (
                "function renderResources("
                in javascript
                and "function renderResourceChart("
                in javascript
                and "function renderResourceStorage("
                in javascript
                and "atlas_resource_monitoring_dashboard"
                in javascript
                and "RESOURCE_REFRESH_INTERVAL_MS = 1000"
                in javascript
                and "REFRESH_INTERVAL_MS = 5000"
                in javascript
            ),
            "css_contract": (
                ".resource-summary-grid" in css
                and ".resource-chart-line" in css
                and ".resource-storage-list" in css
            ),
            "registry_contract": (
                "atlas_resource_monitoring_dashboard"
                in capability_ids
            ),
            "central_cli_contract": (
                "atlas-resource-monitoring-dashboard-status"
                in central_cli
                and "handle_atlas_resource_monitoring_dashboard_cli_command"
                in central_cli
            ),
            "identity_contract": (
                "version: 1.2.7" in identity
                or 'version: "1.2.7"' in identity
                or "version: '1.2.7'" in identity
            ),
            "documentation_contract": (
                "ATLAS Resource Monitoring Dashboard"
                in docs
                and "permission_audit_action_visibility_ux" in docs
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
            raise AtlasResourceMonitoringDashboardContractError(
                "Sprint 267 evidence count must be 12."
            )
        if (
            len(self.DIMENSIONS)
            != self.EXPECTED_DIMENSIONS
        ):
            raise AtlasResourceMonitoringDashboardContractError(
                "Sprint 267 dimension count must be 42."
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
            "atlas_resource_monitoring_dashboard_ready": secure,
            "block_release_ready": False,
            "live_e2e_required": False,
            "background_sampler_enabled": False,
            "history_persistence_enabled": False,
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
            "mount_points": [
                "/",
                "/home",
                "/mnt/aura-data",
            ],
            "sample_interval_seconds": 1,
            "ui_refresh_seconds": 1,
            "rolling_windows_minutes": [
                5,
                15,
                60,
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
                "read_only_atlas_resource_dashboard"
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
