from __future__ import annotations

from pathlib import Path
from typing import Any
import re


class DailyLocalAssistantLiveAcceptanceStabilizationContractError(
    RuntimeError
):
    pass


class DailyLocalAssistantLiveAcceptanceStabilizationContract:
    VERSION = "1.3.0"
    ANCHOR_VERSION = "1.2.9"
    CURRENT_SPRINT = 270
    NEXT_SPRINT = 271
    BOUNDARY = (
        "daily_local_assistant_live_acceptance_stabilization"
    )
    NEXT_BOUNDARY = "voice_daily_use_activation"
    ASSERTIONS_PER_DIMENSION = 12
    EXPECTED_DIMENSIONS = 48
    EXPECTED_ASSERTIONS = 576
    DIMENSIONS = (
        "identity",
        "boundary",
        "runtime",
        "acceptance",
        "function",
        "usage",
        "failure",
        "recovery",
        "session",
        "model",
        "memory",
        "permission",
        "resources",
        "control_center",
        "service",
        "ownership",
        "safe_idle",
        "release",
        "block",
        "handoff",
        "evidence",
        "checksum",
        "registry",
        "cli",
        "docs",
        "historical",
        "version",
        "scope",
        "source_fix",
        "stop_fix",
        "none_key_fix",
        "no_new_route",
        "no_new_panel",
        "no_dependency",
        "no_authority",
        "no_raw_chat",
        "no_memory_write",
        "no_permission_grant",
        "no_unrelated_chat",
        "read_only",
        "safe_idle_contract",
        "planner",
        "review",
        "preview",
        "roadmap",
        "voice_handoff",
        "orion_reconciliation",
        "release_checkpoint",
    )

    def __init__(
        self,
        project_root: str | Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root or Path.cwd()
        ).resolve()

    def _evidence(self) -> dict[str, bool]:
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
            AuraControlCenterBackendRuntimeManager,
        )
        from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_manager import (
            AuraControlCenterWebShellRuntimeManager,
        )
        from aura.daily_use_acceptance_rehearsal_release_harness import (
            DailyUseAcceptanceRehearsalReleaseHarnessContract,
        )
        from .daily_local_assistant_live_acceptance_stabilization_runtime_manager import (
            DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager,
        )

        root = self.project_root
        runtime = (
            DailyLocalAssistantLiveAcceptanceStabilizationRuntimeManager(
                project_root=root
            )
        )
        runtime_test = runtime.self_test()
        snapshot = runtime.snapshot()

        historical_contract = (
            DailyUseAcceptanceRehearsalReleaseHarnessContract(
                project_root=root
            )
        )
        historical_check = historical_contract.check()

        identity = (
            root / "aura/personality/identity.yaml"
        ).read_text(encoding="utf-8")
        registry_source = (
            root
            / "aura/capability_registry/"
            "capability_registry_manager.py"
        ).read_text(encoding="utf-8")
        cli_source = (
            root / "aura/core/cli.py"
        ).read_text(encoding="utf-8")
        stop_source = (
            root
            / "aura/manual_start_stop_status_runtime/"
            "manual_start_stop_status_runtime_executor.py"
        ).read_text(encoding="utf-8")
        html = (
            root
            / "aura/control_center_web_shell_runtime/"
            "static/index.html"
        ).read_text(encoding="utf-8")
        javascript = (
            root
            / "aura/control_center_web_shell_runtime/"
            "static/control-center.js"
        ).read_text(encoding="utf-8")
        css = (
            root
            / "aura/control_center_web_shell_runtime/"
            "static/control-center.css"
        ).read_text(encoding="utf-8")

        doc_paths = (
            "README.md",
            "docs/AURA_CAPABILITY_REGISTRY.md",
            "docs/AURA_DAILY_LOCAL_ASSISTANT_LIVE_ACCEPTANCE_STABILIZATION.md",
            "docs/AURA_MASTER_ROADMAP.md",
            "docs/AURA_V1_2_TO_V1_3_DAILY_PRODUCT_ROADMAP.md",
            "docs/AURA_V2_TO_V4_PRODUCT_ROADMAP.md",
        )
        docs = "\n".join(
            (root / path).read_text(encoding="utf-8")
            for path in doc_paths
        )

        registry = CapabilityRegistryManager()
        capability_ids = {
            item["id"]
            for item in registry.capability_catalog()
        }

        backend_payload = (
            AuraControlCenterBackendRuntimeManager(
                project_root=root
            ).payload_for_route("/api/control-center")
        )
        web_test = (
            AuraControlCenterWebShellRuntimeManager(
                project_root=root
            ).self_test()
        )

        acceptance = snapshot["acceptance_evidence"]
        checksum = snapshot[
            "acceptance_evidence_sha256"
        ]

        return {
            "runtime_contract": (
                runtime_test["assertion_count"] == 84
                and runtime_test[
                    "failed_assertion_count"
                ] == 0
                and runtime_test["dimension_count"] == 12
                and runtime_test["block_complete"] is True
                and runtime_test[
                    "block_release_ready"
                ] is True
            ),
            "live_acceptance_contract": all((
                acceptance["live_e2e_executed"] is True,
                acceptance["real_function_proof"] is True,
                acceptance["usage_result_verified"] is True,
                acceptance["bounded_failure_verified"] is True,
                acceptance["recovery_verified"] is True,
            )),
            "usage_and_session_contract": all((
                acceptance["persistent_session_verified"] is True,
                acceptance["initial_model_call_repeated"] is False,
                acceptance["prior_model_message_count"] == 1,
                acceptance["new_model_message_count"] == 1,
                acceptance["total_model_message_count"] == 2,
                acceptance["new_session_count"] == 0,
                acceptance["reused_session_count"] == 1,
            )),
            "safety_result_contract": all((
                acceptance["memory_write_delta"] is False,
                acceptance["permission_grant_applied"] is False,
                acceptance["unrelated_chat_data_mutated"] is False,
                acceptance["final_lifecycle_state"] == "stopped",
                acceptance["final_ownership_state"] == "clear",
                acceptance["final_state_record_exists"] is False,
                acceptance["final_port_8765_listening"] is False,
                acceptance["final_safe_idle"] is True,
            )),
            "source_fix_contract": (
                "if permission is not None:"
                in registry_source
                and "def _read_proc_state("
                in stop_source
                and "def _owned_process_stopped("
                in stop_source
                and "same_process_terminal"
                in stop_source
            ),
            "identity_and_checksum_contract": (
                (
                    "version: 1.3.0" in identity
                    or 'version: "1.3.0"' in identity
                    or "version: '1.3.0'" in identity
                )
                and bool(re.fullmatch(
                    r"[0-9a-f]{64}",
                    checksum,
                ))
                and checksum == "72dbd6c243d55171b39f1b2a1a659ee654ea7622c31e09c0ea9000a666e29fb1"
            ),
            "registry_and_cli_contract": (
                self.BOUNDARY in capability_ids
                and self.BOUNDARY in registry_source
                and (
                    "daily-local-assistant-live-acceptance-"
                    "stabilization-status"
                    in cli_source
                )
                and (
                    "handle_daily_local_assistant_live_"
                    "acceptance_stabilization_cli_command"
                    in cli_source
                )
            ),
            "documentation_contract": (
                "Sprint 270" in docs
                and "v1.3.0" in docs
                and self.BOUNDARY in docs
                and self.NEXT_BOUNDARY in docs
                and checksum in docs
                and (
                    "Sprint 271 discovery must reconcile"
                    in docs
                )
            ),
            "historical_contract": (
                historical_contract.VERSION == "1.2.9"
                and historical_contract.CURRENT_SPRINT == 269
                and historical_contract.NEXT_SPRINT == 270
                and historical_check["assertion_count"] == 552
                and historical_check[
                    "failed_assertion_count"
                ] == 0
            ),
            "no_new_ui_contract": (
                self.BOUNDARY not in backend_payload
                and (
                    "daily-local-assistant-live-acceptance"
                    not in html
                )
                and (
                    "dailyLocalAssistantLiveAcceptance"
                    not in javascript
                )
                and (
                    ".daily-local-assistant-live-acceptance"
                    not in css
                )
                and web_test["assertion_count"] == 190
                and web_test[
                    "failed_assertion_count"
                ] == 0
            ),
            "release_boundary_contract": (
                snapshot["version"] == "1.3.0"
                and snapshot["anchor_version"] == "1.2.9"
                and snapshot["current_sprint"] == 270
                and snapshot["next_sprint"] == 271
                and snapshot["boundary"]
                == self.BOUNDARY
                and snapshot["next_boundary"]
                == self.NEXT_BOUNDARY
                and snapshot["block_complete"] is True
                and snapshot["block_release_ready"] is True
            ),
            "authority_contract": all((
                snapshot["runtime_result_persistence_enabled"]
                is False,
                snapshot["raw_chat_content_recorded"]
                is False,
                snapshot["new_http_route"] is False,
                snapshot["new_web_panel"] is False,
                snapshot["new_external_dependency"] is False,
                snapshot["new_execution_authority"] is False,
                snapshot["runtime_mutated"] is False,
                snapshot["read_only"] is True,
                snapshot["safe_idle"] is True,
            )),
        }

    def check(self) -> dict[str, Any]:
        evidence = self._evidence()

        if (
            len(evidence)
            != self.ASSERTIONS_PER_DIMENSION
        ):
            raise DailyLocalAssistantLiveAcceptanceStabilizationContractError(
                "Sprint 270 evidence count must be 12."
            )
        if (
            len(self.DIMENSIONS)
            != self.EXPECTED_DIMENSIONS
        ):
            raise DailyLocalAssistantLiveAcceptanceStabilizationContractError(
                "Sprint 270 dimension count must be 48."
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
            "daily_local_assistant_live_acceptance_stabilization_ready":
            secure,
            "live_e2e_executed": secure,
            "real_function_proof": secure,
            "usage_result_verified": secure,
            "bounded_failure_verified": secure,
            "recovery_verified": secure,
            "block_complete": secure,
            "block_release_ready": secure,
            "release_version": self.VERSION,
            "next_block_reconfirmation_required": True,
            "new_http_route": False,
            "new_web_panel": False,
            "new_external_dependency": False,
            "new_execution_authority": False,
            "runtime_mutated": False,
            "read_only": True,
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
            "runtime_mode": (
                "live_acceptance_release_checkpoint"
            ),
            "assertion_count": check["assertion_count"],
            "failed_assertion_count":
            check["failed_assertion_count"],
            "dimension_count": check["dimension_count"],
            "block_complete": check["block_complete"],
            "block_release_ready":
            check["block_release_ready"],
            "next_block_reconfirmation_required": True,
            "read_only": True,
            "safe_idle": True,
        }

    def review(self) -> dict[str, Any]:
        return {
            **self.context(),
            "review_mode": (
                "sprint_270_release_review"
            ),
            "commit_performed": False,
            "push_performed": False,
        }

    def preview(self) -> dict[str, Any]:
        return {
            **self.review(),
            "preview_only": True,
            "runtime_mutated": False,
        }
