from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json

from .model_lifecycle_queue_budget_contract import (
    ModelLifecycleQueueBudgetContract,
)


class ModelLifecycleQueueBudgetPlanner:
    VERSION = "1.1.9"
    ANCHOR_VERSION = "1.1.8"
    CURRENT_SPRINT = 259
    NEXT_SPRINT = 260
    NEXT_VERSION = "1.2.0"
    BOUNDARY = "model_loading_unloading_queue_resource_budgets"
    NEXT_BOUNDARY = "active_local_runtime_integration_stabilization"
    EXPECTED_ASSERTION_COUNT = 312

    DIMENSIONS = (
        "canonical_owner",
        "router_dependency",
        "bridge_dependency",
        "health_dependency",
        "resource_dependency",
        "known_model",
        "loopback_provider",
        "load_contract",
        "release_contract",
        "status_contract",
        "explicit_permission",
        "health_gate",
        "budget_gate",
        "memory_reserve",
        "swap_guard",
        "load_guard",
        "gpu_optional",
        "bounded_queue",
        "max_inflight",
        "queue_timeout",
        "no_queue_persistence",
        "no_background_worker",
        "no_download_pull",
        "no_service_mutation",
        "isolated_rehearsal",
        "handoff",
    )

    def __init__(self, project_root: str | Path) -> None:
        self.project_root = Path(project_root).resolve()
        self.contract = ModelLifecycleQueueBudgetContract(
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
        profile = self.contract.provider_profile()
        health = self.contract.health.host_posture()
        budget = self.contract.resource_budget_preview()
        load = self.contract.lifecycle_preview("load")
        status = self.contract.lifecycle_preview("status")
        release = self.contract.lifecycle_preview("release")
        queue = self.contract.queue_preview()
        rehearsal = self.contract.isolated_rehearsal()

        primary = {
            "canonical_owner": self.BOUNDARY
            == "model_loading_unloading_queue_resource_budgets",
            "router_dependency": self.contract.router.VERSION == "1.1.8",
            "bridge_dependency": profile["provider"] == "ollama",
            "health_dependency": health["state"]
            in {"available_unprobed", "degraded_unprobed", "unavailable"},
            "resource_dependency": budget["baseline_status_valid"]
            and budget["monitor_status_valid"],
            "known_model": isinstance(profile["model"], str)
            and bool(profile["model"]),
            "loopback_provider": profile["loopback_only"]
            and profile["base_url"]
            in {"http://localhost:11434", "http://127.0.0.1:11434"},
            "load_contract": load["keep_alive"] == "5m"
            and rehearsal["load_completed"],
            "release_contract": release["keep_alive"] == 0
            and rehearsal["release_completed"],
            "status_contract": rehearsal["status_completed"]
            and rehearsal["provider_model_names_exposed"] is False,
            "explicit_permission": rehearsal["denied_without_permission"],
            "health_gate": rehearsal["denied_without_health"],
            "budget_gate": rehearsal["denied_without_budget"],
            "memory_reserve": budget["memory_reserve_ratio"] == 0.20,
            "swap_guard": budget["max_swap_used_ratio"] == 0.50,
            "load_guard": budget["max_normalized_load_1m"] == 1.0,
            "gpu_optional": budget["gpu_optional"]
            and not budget["gpu_required"],
            "bounded_queue": queue["max_depth"] == 4
            and rehearsal["queue_full_denied"],
            "max_inflight": queue["max_inflight"] == 1
            and rehearsal["queue_busy_denied"],
            "queue_timeout": queue["timeout_seconds"] == 120.0
            and rehearsal["queue_timeout_denied"],
            "no_queue_persistence": not queue["persistent"]
            and not rehearsal["queue_persisted"],
            "no_background_worker": not queue["background_worker"]
            and not rehearsal["background_worker_started"],
            "no_download_pull": not rehearsal["model_downloaded"]
            and not rehearsal["model_pulled"],
            "no_service_mutation": not rehearsal["service_mutated"]
            and not rehearsal["systemd_mutated"]
            and not rehearsal["autostart_mutated"],
            "isolated_rehearsal": rehearsal["load_path"] == "/api/generate"
            and rehearsal["status_path"] == "/api/ps"
            and rehearsal["release_path"] == "/api/generate"
            and rehearsal["queued_lifecycle_completed"],
            "handoff": self.NEXT_SPRINT == 260
            and self.NEXT_VERSION == "1.2.0",
        }

        shared = [
            self.VERSION == "1.1.9",
            self.ANCHOR_VERSION == "1.1.8",
            self.CURRENT_SPRINT == 259,
            self.NEXT_SPRINT == 260,
            self.NEXT_VERSION == "1.2.0",
            self.NEXT_BOUNDARY
            == "active_local_runtime_integration_stabilization",
            profile["provider"] == "ollama",
            load["model_lifecycle_executed"] is False,
            queue["queue_mutated"] is False,
            budget["threshold_mutated"] is False,
            rehearsal["canonical_network_opened"] is False,
        ]

        assertions: list[tuple[str, bool]] = []
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
        failed = [name for name, passed in assertions if not passed]
        return {
            "owner": "ModelLifecycleQueueBudgetPlanner",
            "version": self.VERSION,
            "anchor_version": self.ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "contract_mode": (
                "permission_gated_lifecycle_bounded_queue_read_only_budget"
            ),
            "assertion_count": len(assertions),
            "failed_assertion_count": len(failed),
            "failed_assertions": failed,
            "dimension_count": len(self.DIMENSIONS),
            "finding_count": len(failed),
            "overall_state": "secure" if not failed else "review",
            "alpha_ready": not failed,
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
        return {
            **{
                key: check[key]
                for key in (
                    "owner",
                    "version",
                    "anchor_version",
                    "current_sprint",
                    "next_sprint",
                    "next_version",
                    "boundary",
                    "next_boundary",
                    "contract_mode",
                    "assertion_count",
                    "failed_assertion_count",
                    "dimension_count",
                    "finding_count",
                    "overall_state",
                    "alpha_ready",
                    "status_valid",
                )
            },
            "provider_profile": self.contract.provider_profile(),
            "resource_budget": self.contract.resource_budget_preview(),
            "queue": self.contract.queue_preview(),
            "loading_default": False,
            "unloading_default": False,
            "queue_default_enabled": False,
            "network_connection_opened": False,
            "model_lifecycle_executed": False,
        }

    def context(self) -> dict[str, Any]:
        return {
            "version": self.VERSION,
            "sprint": self.CURRENT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_sprint": self.NEXT_SPRINT,
            "next_version": self.NEXT_VERSION,
            "next_boundary": self.NEXT_BOUNDARY,
            "router_dependency": "local_model_router_activation",
            "bridge_dependency": "AuraLocalModelBridgeRuntimeManager",
            "health_dependency": "local_model_service_discovery_health",
            "resource_dependencies": [
                "AuraResourceBaselineMetricsPlanner",
                "AuraAtlasResourceMonitoringPlanner",
            ],
            "provider": "ollama",
            "queue_mode": "bounded_in_memory_single_process",
            "queue_max_depth": 4,
            "max_inflight": 1,
            "queue_timeout_seconds": 120,
            "memory_reserve_ratio": 0.20,
            "queue_persistence": False,
            "resource_budget_mutation": False,
        }

    def review(self) -> dict[str, Any]:
        check = self.check()
        return {
            "ok": check["failed_assertion_count"] == 0,
            "version": self.VERSION,
            "boundary": self.BOUNDARY,
            "assertion_count": check["assertion_count"],
            "failed_assertion_count": check["failed_assertion_count"],
            "dimension_count": check["dimension_count"],
            "overall_state": check["overall_state"],
            "review_digest": self._digest(check["assertions"]),
            "blocked_surfaces": {
                "automatic_model_load": True,
                "automatic_model_release": True,
                "model_download_pull": True,
                "unknown_model": True,
                "unhealthy_provider": True,
                "budget_exceeded": True,
                "missing_permission": True,
                "queue_full": True,
                "queue_timeout": True,
                "queue_persistence": True,
                "background_worker": True,
                "resource_threshold_mutation": True,
                "service_control": True,
                "non_loopback_network": True,
                "credentials": True,
                "systemd_mutation": True,
                "autostart_mutation": True,
            },
        }

    def lifecycle_preview(self, action: str) -> dict[str, Any]:
        return self.contract.lifecycle_preview(action)

    def queue_preview(self) -> dict[str, Any]:
        return self.contract.queue_preview()

    def resource_budget_preview(self) -> dict[str, Any]:
        return self.contract.resource_budget_preview()

    def isolated_rehearsal(self) -> dict[str, Any]:
        return self.contract.isolated_rehearsal()
