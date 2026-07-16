from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json

from .active_local_runtime_integration_contract import (
    ActiveLocalRuntimeIntegrationContract,
)


class ActiveLocalRuntimeIntegrationPlanner:
    VERSION = "1.2.0"
    ANCHOR_VERSION = "1.1.9"
    CURRENT_SPRINT = 260
    NEXT_SPRINT = 261
    BOUNDARY = "active_local_runtime_integration_stabilization"
    NEXT_BOUNDARY = (
        "roadmap_reconfirmation_required_after_v1_2_0"
    )
    EXPECTED_ASSERTION_COUNT = 336

    DIMENSIONS = (
        "release_boundary",
        "block_completion",
        "launcher_dependency",
        "service_dependency",
        "process_dependency",
        "chat_dependency",
        "health_dependency",
        "router_dependency",
        "lifecycle_dependency",
        "permission_dependency",
        "service_safe_idle",
        "session_privacy",
        "exact_companion_route",
        "loopback_provider",
        "explicit_activation",
        "explicit_chat_turn",
        "explicit_stop_restore",
        "bounded_queue",
        "resource_budget",
        "health_before_request",
        "lifecycle_before_request",
        "persistence_after_success",
        "stop_restore",
        "failure_restore",
        "no_automatic_activation",
        "no_unsafe_mutation",
        "isolated_end_to_end",
        "roadmap_reconfirmation",
    )

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.contract = ActiveLocalRuntimeIntegrationContract(
            project_root=self.project_root
        )

    @staticmethod
    def _digest(value: Any) -> str:
        return hashlib.sha256(
            json.dumps(
                value,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        ).hexdigest()

    def _assertions(self) -> list[tuple[str, bool]]:
        preview = self.contract.integration_preview()
        rehearsal = self.contract.isolated_rehearsal()
        dependencies = preview["dependency_status"]
        route = preview["route"]
        queue = preview["queue"]
        budget = preview["resource_budget"]
        lifecycle = preview["lifecycle"]

        primary = {
            "release_boundary": (
                self.VERSION == "1.2.0"
                and self.CURRENT_SPRINT == 260
                and self.BOUNDARY
                == "active_local_runtime_integration_stabilization"
            ),
            "block_completion": (
                preview["block"]
                == "active_local_runtime_and_model_service_integration"
            ),
            "launcher_dependency": dependencies["launcher"]["valid"],
            "service_dependency": dependencies["service"]["valid"],
            "process_dependency": dependencies["process"]["valid"],
            "chat_dependency": dependencies["chat"]["valid"],
            "health_dependency": dependencies["health"]["valid"],
            "router_dependency": dependencies["router"]["valid"],
            "lifecycle_dependency": dependencies["lifecycle"]["valid"],
            "permission_dependency": (
                preview["model_request_permission_required"]
                and preview["lifecycle_permission_required"]
                and preview["queue_permission_required"]
            ),
            "service_safe_idle": preview["service"]["safe_idle"],
            "session_privacy": (
                preview["session_store"]["root_mode"] == "0o700"
                and preview["session_store"]["files_private"]
                and not preview["session_store"]["content_exposed"]
            ),
            "exact_companion_route": (
                route["target"] == "companion"
                and route["eligible_for_confirmation"] is True
            ),
            "loopback_provider": (
                preview["health"]["endpoint"]
                in {
                    "http://127.0.0.1:11434",
                    "http://localhost:11434",
                }
            ),
            "explicit_activation": (
                rehearsal["denied_without_activation_permission"]
                and rehearsal["activation_preview_approved"]
            ),
            "explicit_chat_turn": (
                rehearsal["denied_without_chat_turn_permission"]
                and rehearsal["chat_turn_preview_approved"]
            ),
            "explicit_stop_restore": (
                rehearsal["denied_without_stop_restore_permission"]
                and rehearsal["stop_restore_preview_approved"]
            ),
            "bounded_queue": (
                queue["max_depth"] == 4
                and queue["max_inflight"] == 1
                and queue["timeout_seconds"] == 120.0
                and rehearsal["queue_depth_after"] == 0
                and rehearsal["queue_inflight_after"] == 0
            ),
            "resource_budget": (
                budget["memory_reserve_ratio"] == 0.20
                and budget["threshold_mutated"] is False
            ),
            "health_before_request": (
                preview["health_probe_required"] is True
                and preview["health"]["health_probe_performed"] is False
            ),
            "lifecycle_before_request": (
                lifecycle["load"]["model_lifecycle_executed"] is False
                and lifecycle["release"]["model_lifecycle_executed"] is False
            ),
            "persistence_after_success": (
                preview["response_persistence_after_success_only"] is True
                and rehearsal["response_persistence_allowed"] is False
            ),
            "stop_restore": (
                rehearsal["final_state"] == "safe_idle_restored"
                and rehearsal["failure_policy"]
                == "stop_and_restore_on_any_failed_gate"
            ),
            "failure_restore": (
                rehearsal["state_count"] == 12
                and rehearsal["event_sequence_valid"]
            ),
            "no_automatic_activation": (
                preview["safe_idle_default"]
                and preview["manual_activation_only"]
            ),
            "no_unsafe_mutation": all(
                rehearsal[key] is False
                for key in (
                    "canonical_network_opened",
                    "canonical_service_started",
                    "canonical_health_probe_executed",
                    "canonical_model_lifecycle_executed",
                    "canonical_model_request_executed",
                    "canonical_session_mutated",
                    "canonical_runtime_state_mutated",
                    "queue_persisted",
                    "background_worker_started",
                    "model_downloaded",
                    "model_pulled",
                    "resource_budget_mutated",
                    "systemd_mutated",
                    "autostart_mutated",
                )
            ),
            "isolated_end_to_end": (
                rehearsal["activation_preview_approved"]
                and rehearsal["chat_turn_preview_approved"]
                and rehearsal["stop_restore_preview_approved"]
            ),
            "roadmap_reconfirmation": (
                self.NEXT_SPRINT == 261
                and self.NEXT_BOUNDARY
                == "roadmap_reconfirmation_required_after_v1_2_0"
            ),
        }

        shared = [
            self.VERSION == "1.2.0",
            self.ANCHOR_VERSION == "1.1.9",
            self.CURRENT_SPRINT == 260,
            self.NEXT_SPRINT == 261,
            preview["all_dependencies_valid"] is True,
            preview["network_connection_opened"] is False,
            preview["service_started"] is False,
            preview["health_probe_executed"] is False,
            preview["model_lifecycle_executed"] is False,
            preview["model_request_executed"] is False,
            preview["session_mutated"] is False,
        ]

        assertions = []
        for dimension in self.DIMENSIONS:
            values = [primary[dimension], *shared]
            if len(values) != 12:
                raise RuntimeError(
                    "Each dimension requires twelve assertions."
                )
            assertions.extend(
                (
                    f"{dimension}.{index:02d}",
                    bool(passed),
                )
                for index, passed in enumerate(values, start=1)
            )
        return assertions

    def check(self) -> dict[str, Any]:
        assertions = self._assertions()
        failed = [
            name
            for name, passed in assertions
            if not passed
        ]
        return {
            "owner": "ActiveLocalRuntimeIntegrationPlanner",
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "explicit_manual_end_to_end_preview_and_stabilization"
            ),
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(self.DIMENSIONS),
            "finding_count": len(failed),
            "overall_state": "secure" if not failed else "review",
            "alpha_ready": not failed,
            "block_release_ready": not failed,
            "status_valid": (
                len(assertions) == self.EXPECTED_ASSERTION_COUNT
                and not failed
            ),
            "assertions": [
                {"name": name, "passed": passed}
                for name, passed in assertions
            ],
        }

    def status(self) -> dict[str, Any]:
        check = self.check()
        preview = self.contract.integration_preview()
        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "block_release_ready",
                    "status_valid",
                )
            },
            "block": preview["block"],
            "service_safe_idle": preview["service"]["safe_idle"],
            "session_root_mode": preview["session_store"]["root_mode"],
            "provider": "ollama",
            "route": "companion",
            "queue_max_depth": 4,
            "max_inflight": 1,
            "safe_idle_default": True,
            "manual_activation_only": True,
            "network_connection_opened": False,
            "runtime_activated": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "block": (
                "active_local_runtime_and_model_service_integration"
            ),
            "provider": "ollama",
            "route": "companion",
            "safe_idle_default": True,
            "manual_activation_only": True,
            "failure_policy": (
                "stop_and_restore_on_any_failed_gate"
            ),
            "roadmap_reconfirmation_required": True,
        }

    def review(self) -> dict[str, Any]:
        check = self.check()
        return {
            "ok": check["failed_assertion_count"] == 0,
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check[
                "failed_assertion_count"
            ],
            "dimension_count": check["dimension_count"],
            "overall_state": check["overall_state"],
            "block_release_ready": check["block_release_ready"],
            "review_digest": self._digest(check["assertions"]),
            "blocked_surfaces": {
                "automatic_service_start": True,
                "automatic_health_probe": True,
                "automatic_model_load": True,
                "automatic_model_request": True,
                "automatic_session_write": True,
                "automatic_model_release": True,
                "queue_persistence": True,
                "background_worker": True,
                "model_download_pull": True,
                "non_loopback_network": True,
                "credentials": True,
                "resource_threshold_mutation": True,
                "systemd_mutation": True,
                "autostart_mutation": True,
            },
        }

    def integration_preview(self) -> dict[str, Any]:
        return self.contract.integration_preview()

    def chat_turn_preview(self) -> dict[str, Any]:
        return self.contract.chat_turn_preview(
            confirm=True,
            token=self.contract.CHAT_TURN_TOKEN,
        )

    def stop_restore_preview(self) -> dict[str, Any]:
        return self.contract.stop_restore_preview(
            confirm=True,
            token=self.contract.STOP_RESTORE_TOKEN,
        )

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.contract.isolated_rehearsal()
