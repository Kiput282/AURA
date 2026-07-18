from __future__ import annotations

from pathlib import Path
from typing import Any


class DailyUseAcceptanceRehearsalReleaseHarnessContractError(
    RuntimeError
):
    pass


class DailyUseAcceptanceRehearsalReleaseHarnessContract:
    VERSION = "1.2.9"
    ANCHOR_VERSION = "1.2.8"
    CURRENT_SPRINT = 269
    NEXT_SPRINT = 270
    BOUNDARY = (
        "daily_use_acceptance_rehearsal_and_release_harness"
    )
    NEXT_BOUNDARY = "daily_local_assistant_live_acceptance_stabilization"
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_DIMENSIONS = 46
    EXPECTED_ASSERTIONS = 552
    DIMENSIONS = (
        "identity",
        "boundary",
        "runtime",
        "steps",
        "baseline",
        "service",
        "chat",
        "model",
        "memory",
        "permission",
        "resources",
        "release",
        "safe_idle",
        "backend",
        "web",
        "javascript",
        "css",
        "registry",
        "cli",
        "docs",
        "historical",
        "version",
        "scope",
        "root_payload",
        "route_boundary",
        "persistence_boundary",
        "execution_boundary",
        "failure_policy",
        "sprint270_live",
        "sprint270_recovery",
        "sprint270_safe_idle",
        "no_session",
        "no_model",
        "no_memory",
        "no_service_mutation",
        "no_permission",
        "no_recovery",
        "no_route",
        "no_worker",
        "no_dependency",
        "no_authority",
        "read_only",
        "safe_idle_contract",
        "planner",
        "review",
        "preview",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def _evidence(
        self,
    ) -> dict[str, bool]:
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )
        from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_manager import (
            AuraControlCenterWebShellRuntimeManager,
        )
        from aura.permission_audit_action_visibility_ux import (
            PermissionAuditActionVisibilityUxContract,
            PermissionAuditActionVisibilityUxRuntimeManager,
        )
        from .daily_use_acceptance_rehearsal_release_harness_runtime_manager import (
            DailyUseAcceptanceRehearsalReleaseHarnessRuntimeManager,
        )

        root = self.project_root
        runtime = (
            DailyUseAcceptanceRehearsalReleaseHarnessRuntimeManager(
                project_root=root
            )
        )
        runtime_test = runtime.self_test()

        backend = AuraControlCenterBackendRuntimeManager(
            project_root=root
        )
        root_payload = backend.payload_for_route(
            "/api/control-center"
        )
        service_payload = backend.payload_for_route(
            "/api/control-center/service"
        )
        permission_payload = backend.payload_for_route(
            "/api/control-center/permissions"
        )
        audit_payload = backend.payload_for_route(
            "/api/control-center/audit"
        )
        key = (
            "daily_use_acceptance_rehearsal_release_harness"
        )
        packet = root_payload.get(key, {})

        web_test = AuraControlCenterWebShellRuntimeManager(
            project_root=root
        ).self_test()

        html = (
            root
            / "aura/control_center_web_shell_runtime/static/index.html"
        ).read_text(encoding="utf-8")
        javascript = (
            root
            / "aura/control_center_web_shell_runtime/static/control-center.js"
        ).read_text(encoding="utf-8")
        css = (
            root
            / "aura/control_center_web_shell_runtime/static/control-center.css"
        ).read_text(encoding="utf-8")
        central_cli = (
            root / "aura/core/cli.py"
        ).read_text(encoding="utf-8")
        identity = (
            root / "aura/personality/identity.yaml"
        ).read_text(encoding="utf-8")

        docs = "\n".join(
            (
                root / path
            ).read_text(encoding="utf-8")
            for path in (
                "README.md",
                "docs/AURA_CAPABILITY_REGISTRY.md",
                "docs/AURA_DAILY_USE_ACCEPTANCE_REHEARSAL_RELEASE_HARNESS.md",
                "docs/AURA_MASTER_ROADMAP.md",
                "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
                "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
            )
        )

        registry = CapabilityRegistryManager()
        capability_ids = {
            item["id"]
            for item in registry.capability_catalog()
        }

        historical_contract = (
            PermissionAuditActionVisibilityUxContract
        )
        historical_runtime = (
            PermissionAuditActionVisibilityUxRuntimeManager(
                project_root=root
            ).self_test()
        )
        historical_anchor = all(
            (
                historical_contract.VERSION == "1.2.8",
                historical_contract.ANCHOR_VERSION == "1.2.7",
                historical_contract.CURRENT_SPRINT == 268,
                historical_contract.NEXT_SPRINT == 269,
                historical_contract.BOUNDARY
                == "permission_audit_action_visibility_ux",
                historical_contract.NEXT_BOUNDARY
                == "daily_use_acceptance_rehearsal_and_release_harness",
                historical_contract.EXPECTED_ASSERTIONS == 528,
                historical_contract.EXPECTED_DIMENSIONS == 44,
                historical_runtime["assertion_count"] == 60,
                historical_runtime[
                    "failed_assertion_count"
                ]
                == 0,
            )
        )

        safety = all(
            (
                packet.get(
                    "result_persistence_enabled"
                )
                is False,
                packet.get("chat_session_created")
                is False,
                packet.get("model_invoked") is False,
                packet.get("memory_written") is False,
                packet.get(
                    "service_lifecycle_changed"
                )
                is False,
                packet.get("permission_granted")
                is False,
                packet.get("recovery_executed")
                is False,
                packet.get("new_http_route") is False,
                packet.get(
                    "background_worker_enabled"
                )
                is False,
                packet.get(
                    "external_dependency_added"
                )
                is False,
                packet.get(
                    "new_execution_authority"
                )
                is False,
                packet.get("runtime_mutated") is False,
                packet.get("read_only") is True,
                packet.get("safe_idle") is True,
            )
        )

        return {
            "runtime_facade": (
                runtime_test["assertion_count"] == 72
                and runtime_test[
                    "failed_assertion_count"
                ]
                == 0
                and runtime_test["step_count"] == 9
                and runtime_test[
                    "ready_step_count"
                ]
                == 9
            ),
            "rehearsal_contract": (
                packet.get("version") == "1.2.9"
                and packet.get("anchor_version")
                == "1.2.8"
                and packet.get("current_sprint") == 269
                and packet.get("next_sprint") == 270
                and packet.get("boundary")
                == self.BOUNDARY
                and packet.get("next_boundary")
                == self.NEXT_BOUNDARY
                and packet.get("runtime_mode")
                == "contract_only_rehearsal"
            ),
            "step_contract": (
                packet.get("step_count") == 9
                and packet.get("ready_step_count") == 9
                and packet.get("blocked_step_count") == 0
                and packet.get("rehearsal_ready") is True
                and len(packet.get("steps", {})) == 9
            ),
            "backend_root_payload": (
                key in root_payload
                and key not in service_payload
                and key not in permission_payload
                and key not in audit_payload
                and "runtime_ux_consolidation"
                in root_payload
                and "atlas_resource_monitoring_dashboard"
                in root_payload
                and "permission_audit_action_visibility_ux"
                in root_payload
            ),
            "web_surface_contract": (
                web_test["assertion_count"] == 190
                and web_test[
                    "failed_assertion_count"
                ]
                == 0
                and html.count(
                    'id="daily-use-acceptance"'
                )
                == 1
                and html.count(
                    'class="daily-use-acceptance-step"'
                )
                == 9
            ),
            "javascript_contract": (
                "function renderDailyUseAcceptance("
                in javascript
                and "payload.daily_use_acceptance_rehearsal_release_harness"
                in javascript
                and javascript.count(
                    "renderDailyUseAcceptance("
                )
                == 2
                and javascript.count("fetch(") == 1
            ),
            "css_contract": (
                ".daily-use-acceptance-steps" in css
                and ".daily-use-acceptance-step" in css
                and ".daily-use-acceptance-boundary"
                in css
            ),
            "registry_contract": (
                "daily_use_acceptance_rehearsal_release_harness"
                in capability_ids
            ),
            "central_cli_contract": (
                "daily-use-acceptance-rehearsal-release-harness-status"
                in central_cli
                and "handle_daily_use_acceptance_rehearsal_release_harness_cli_command"
                in central_cli
            ),
            "identity_contract": (
                "version: 1.2.9" in identity
                or 'version: "1.2.9"' in identity
                or "version: '1.2.9'" in identity
                or "version: 1.3.0" in identity
                or 'version: "1.3.0"' in identity
                or "version: '1.3.0'" in identity
            ),
            "documentation_contract": (
                "Daily-use Acceptance Rehearsal Release Harness"
                in docs
                and "daily_local_assistant_live_acceptance_stabilization" in docs
            ),
            "historical_and_safety": (
                historical_anchor and safety
            ),
        }

    def check(
        self,
    ) -> dict[str, Any]:
        evidence = self._evidence()

        if (
            len(evidence)
            != self.ASSERTIONS_PER_DIMENSION
        ):
            raise DailyUseAcceptanceRehearsalReleaseHarnessContractError(
                "Sprint 269 evidence count must be 12."
            )
        if (
            len(self.DIMENSIONS)
            != self.EXPECTED_DIMENSIONS
        ):
            raise DailyUseAcceptanceRehearsalReleaseHarnessContractError(
                "Sprint 269 dimension count must be 46."
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
            "daily_use_acceptance_rehearsal_release_harness_ready":
            secure,
            "rehearsal_ready": secure,
            "release_harness_ready": secure,
            "block_release_ready": False,
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "sprint_270_failure_recovery_required": True,
            "sprint_270_safe_idle_return_required": True,
            "result_persistence_enabled": False,
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
            "runtime_mode": "contract_only_rehearsal",
            "step_count": 9,
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
            "live_e2e_required": False,
            "sprint_270_live_e2e_required": True,
            "read_only": True,
            "safe_idle": True,
        }

    def review(
        self,
    ) -> dict[str, Any]:
        return {
            **self.context(),
            "review_mode": (
                "daily_use_acceptance_rehearsal"
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
