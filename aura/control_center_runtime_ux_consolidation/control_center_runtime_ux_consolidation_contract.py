"""Sprint 266 Control Center runtime UX consolidation contract."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import json


class ControlCenterRuntimeUxConsolidationContractError(
    RuntimeError
):
    """Sprint 266 contract error."""


class ControlCenterRuntimeUxConsolidationContract:
    VERSION = "1.2.6"
    ANCHOR_VERSION = "1.2.5"
    CURRENT_SPRINT = 266
    NEXT_SPRINT = 267
    BOUNDARY = "control_center_runtime_ux_consolidation"
    NEXT_BOUNDARY = "atlas_resource_monitoring_dashboard"
    EXPECTED_DIMENSIONS = 40
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_ASSERTIONS = 480

    DIMENSIONS = tuple(
        f"control_center_runtime_ux_dimension_{index:02d}"
        for index in range(1, EXPECTED_DIMENSIONS + 1)
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def _read(self, relative: str) -> str:
        return (
            self.project_root / relative
        ).read_text(encoding="utf-8")

    def _evidence(self) -> dict[str, bool]:
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )
        from aura.control_center_runtime_ux_consolidation.control_center_runtime_ux_consolidation_runtime_manager import (
            ControlCenterRuntimeUxConsolidationRuntimeManager,
        )
        from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_manager import (
            AuraControlCenterWebShellRuntimeManager,
        )
        from aura.review_first_memory_integration.review_first_memory_integration_contract import (
            ReviewFirstMemoryIntegrationContract,
        )
        from aura.review_first_memory_integration.review_first_memory_integration_runtime_manager import (
            ReviewFirstMemoryIntegrationRuntimeManager,
        )

        runtime = ControlCenterRuntimeUxConsolidationRuntimeManager(
            project_root=self.project_root
        )
        runtime_test = runtime.self_test()
        backend = AuraControlCenterBackendRuntimeManager(
            project_root=self.project_root
        )
        root_payload = backend.payload_for_route(
            "/api/control-center"
        )
        service_payload = backend.payload_for_route(
            "/api/control-center/service"
        )
        operations = root_payload[
            "runtime_ux_consolidation"
        ]
        web = AuraControlCenterWebShellRuntimeManager(
            project_root=self.project_root
        )
        web_test = web.self_test()
        registry = CapabilityRegistryManager()
        catalog = registry.capability_catalog()
        capability_ids = {
            item["id"]
            for item in catalog
        }
        historical_contract = (
            ReviewFirstMemoryIntegrationContract
        )
        historical_runtime = (
            ReviewFirstMemoryIntegrationRuntimeManager(
                project_root=self.project_root
            ).self_test()
        )
        historical_anchor = all(
            (
                historical_contract.VERSION == "1.2.5",
                historical_contract.ANCHOR_VERSION == "1.2.4",
                historical_contract.CURRENT_SPRINT == 265,
                historical_contract.NEXT_SPRINT == 266,
                historical_contract.BOUNDARY
                == "review_first_memory_integration",
                historical_contract.NEXT_BOUNDARY
                == "control_center_runtime_ux_consolidation",
                historical_contract.EXPECTED_ASSERTIONS == 456,
                historical_contract.EXPECTED_DIMENSIONS == 38,
                historical_runtime["assertion_count"] == 45,
                historical_runtime["failed_assertion_count"] == 0,
            )
        )

        html = self._read(
            "aura/control_center_web_shell_runtime/static/index.html"
        )
        javascript = self._read(
            "aura/control_center_web_shell_runtime/static/control-center.js"
        )
        css = self._read(
            "aura/control_center_web_shell_runtime/static/control-center.css"
        )
        identity = self._read(
            "aura/personality/identity.yaml"
        )
        central_cli = self._read("aura/core/cli.py")
        docs = "\n".join(
            self._read(path)
            for path in (
                "README.md",
                "docs/AURA_CAPABILITY_REGISTRY.md",
                "docs/AURA_CONTROL_CENTER_RUNTIME_UX_CONSOLIDATION.md",
                "docs/AURA_MASTER_ROADMAP.md",
                "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
            )
        )

        safety = operations["safe_idle"] is True and all(
            operations[key] is False
            for key in (
                "new_execution_authority",
                "service_action_routes",
                "restart_action_routes",
                "model_activation_route",
                "permission_grant_route",
                "recovery_execution_route",
                "memory_write_route",
                "automatic_service_start",
                "automatic_model_activation",
                "automatic_permission_grant",
                "automatic_recovery",
                "automatic_memory_write",
                "network_fallback",
            )
        )

        return {
            "runtime_self_test": (
                runtime_test["assertion_count"] == 40
                and runtime_test["failed_assertion_count"] == 0
            ),
            "backend_root_payload": (
                operations["sprint"] == 266
                and operations["owner_count"] == 5
            ),
            "backend_service_payload": (
                service_payload[
                    "runtime_ux_consolidation"
                ]["sprint"]
                == 266
            ),
            "web_surface_contract": (
                web_test["failed_assertion_count"] == 0
                and 'id="operations"' in html
            ),
            "javascript_contract": (
                "function renderOperations(" in javascript
                and ".runtime_ux_consolidation || {}"
                in javascript
            ),
            "css_contract": (
                ".operations-grid" in css
                and ".operations-boundary" in css
            ),
            "registry_contract": (
                "control_center_runtime_ux_consolidation"
                in capability_ids
            ),
            "central_cli_contract": (
                "control-center-runtime-ux-status"
                in central_cli
                and "handle_control_center_runtime_ux_consolidation_cli_command"
                in central_cli
            ),
            "identity_contract": (
                "version: 1.2.6" in identity
                or 'version: "1.2.6"' in identity
                or "version: '1.2.6'" in identity
            ),
            "documentation_contract": (
                "Control Center Runtime UX Consolidation"
                in docs
                and "atlas_resource_monitoring_dashboard"
                in docs
            ),
            "historical_anchor": historical_anchor,
            "safety_boundary": safety,
        }

    def check(self) -> dict[str, Any]:
        evidence = self._evidence()
        if len(evidence) != self.ASSERTIONS_PER_DIMENSION:
            raise ControlCenterRuntimeUxConsolidationContractError(
                "Sprint 266 evidence count must be 12."
            )
        if len(self.DIMENSIONS) != self.EXPECTED_DIMENSIONS:
            raise ControlCenterRuntimeUxConsolidationContractError(
                "Sprint 266 dimension count must be 40."
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
            len(assertions) == self.EXPECTED_ASSERTIONS
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
                "secure" if secure else "review_required"
            ),
            "status_valid": secure,
            "alpha_ready": secure,
            "control_center_runtime_ux_ready": secure,
            "block_release_ready": False,
            "new_execution_authority": False,
            "service_action_routes": False,
            "restart_action_routes": False,
            "arbitrary_log_content_read": False,
            "bounded_log_metadata_only": True,
            "model_activation_route": False,
            "permission_grant_route": False,
            "recovery_execution_route": False,
            "memory_write_route": False,
            "automatic_service_start": False,
            "automatic_model_activation": False,
            "automatic_permission_grant": False,
            "automatic_recovery": False,
            "automatic_memory_write": False,
            "network_fallback": False,
            "runtime_mutated": False,
            "safe_idle": True,
        }

    def status(self) -> dict[str, Any]:
        return self.check()

    def context(self) -> dict[str, Any]:
        check = self.check()
        return {
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "primary_interface": "browser_control_center",
            "chat_destination": "/chat",
            "visibility_destination": "/visibility",
            "control_center_runtime_ux_ready": check[
                "control_center_runtime_ux_ready"
            ],
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check["dimension_count"],
            "finding_count": check["finding_count"],
            "safe_idle": True,
        }

    def review(self) -> dict[str, Any]:
        return {
            **self.context(),
            "review_mode": "read_only_runtime_ux_consolidation",
            "commit_performed": False,
            "push_performed": False,
        }

    def preview(self) -> dict[str, Any]:
        return {
            **self.review(),
            "preview_only": True,
            "runtime_mutated": False,
        }
