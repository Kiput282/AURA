from __future__ import annotations

from pathlib import Path
from typing import Any

from .aura_service_lifecycle_runtime_manager import (
    AuraServiceLifecycleRuntimeManager,
)


class AuraServiceLifecycleDeterminismPlanner:
    """Canonical read-only Sprint 242 lifecycle determinism owner."""

    VERSION = "1.0.2-genesis"
    CANONICAL_ANCHOR_VERSION = "1.0.1-genesis"

    CURRENT_SPRINT = 242
    NEXT_SPRINT = 243

    BOUNDARY = "service_lifecycle_determinism"
    NEXT_BOUNDARY = "configuration_integrity"

    EXPECTED_ASSERTION_COUNT = 25

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        runtime_manager:
            AuraServiceLifecycleRuntimeManager | None = None,
    ) -> None:
        if project_root is None:
            project_root = Path(__file__).resolve().parents[2]

        self.project_root = Path(
            project_root
        ).resolve()

        self.runtime_manager = (
            runtime_manager
            if runtime_manager is not None
            else AuraServiceLifecycleRuntimeManager()
        )

    def contract(self) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version":
                self.CANONICAL_ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "title": "Service Lifecycle Determinism",
            "expected_assertion_count":
                self.EXPECTED_ASSERTION_COUNT,
            "startup_stop_policy":
                "reject_while_startup_in_progress",
            "stopped_stop_policy":
                "idempotent_already_stopped",
            "stopping_stop_policy":
                "idempotent_stop_already_in_progress",
            "historical_self_test_assertion_count": 41,
            "historical_self_test_json_only": True,
            "normal_access_log_preserved": True,
            "persistent_pid_file_allowed": False,
            "persistent_lifecycle_state_allowed": False,
            "systemd_action_allowed": False,
            "automatic_start_allowed": False,
            "background_daemon_allowed": False,
            "remote_lifecycle_control_allowed": False,
            "http_lifecycle_mutation_allowed": False,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def status(self) -> dict[str, Any]:
        snapshot = self.runtime_manager.snapshot()

        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version":
                self.CANONICAL_ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "state": snapshot["state"],
            "safe_idle": snapshot["safe_idle"],
            "listener_active":
                snapshot["listener_active"],
            "runtime_execution_features":
                snapshot["runtime_execution_features"],
            "determinism_check_ready": True,
            "startup_stop_guard_applied": True,
            "historical_json_output_hardened": True,
            "normal_access_log_preserved": True,
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }

    def context(self) -> dict[str, Any]:
        snapshot = self.runtime_manager.snapshot()

        return {
            **self.contract(),
            "project_root": str(self.project_root),
            "runtime_component":
                snapshot["name"],
            "runtime_component_version":
                snapshot["component_version"],
            "runtime_source_sprint":
                snapshot["sprint"],
            "lifecycle_state": snapshot["state"],
            "allowed_transitions":
                snapshot["allowed_transitions"],
            "process_owner":
                snapshot["process_owner"],
            "transition_count":
                snapshot["transition_count"],
            "listener_active":
                snapshot["listener_active"],
            "source_paths": [
                (
                    "aura/service_lifecycle_runtime/"
                    "aura_service_lifecycle_runtime_manager.py"
                ),
                (
                    "aura/service_lifecycle_runtime/"
                    "aura_service_lifecycle_runtime_cli.py"
                ),
                (
                    "aura/service_lifecycle_runtime/"
                    "aura_service_lifecycle_determinism_planner.py"
                ),
            ],
        }

    def plan(self) -> dict[str, Any]:
        return {
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "next_boundary": self.NEXT_BOUNDARY,
            "parts": [
                (
                    "reject stop requests while startup "
                    "is still in progress"
                ),
                (
                    "preserve deterministic repeated-stop "
                    "responses"
                ),
                (
                    "keep historical lifecycle self-test "
                    "machine-readable"
                ),
                (
                    "preserve access logging during normal "
                    "interactive runtime"
                ),
                (
                    "keep persistence, systemd, background, "
                    "and remote control boundaries closed"
                ),
            ],
            "runtime_activation_allowed": False,
            "runtime_ready": False,
        }

    def check(self) -> dict[str, Any]:
        packet = (
            self.runtime_manager.determinism_check()
        )

        failed_assertions = list(
            packet.get(
                "failed_assertions",
                [],
            )
        )

        assertion_count = int(
            packet.get(
                "assertion_count",
                0,
            )
        )

        failed_assertion_count = int(
            packet.get(
                "failed_assertion_count",
                len(failed_assertions),
            )
        )

        return {
            **packet,
            "name": self.BOUNDARY,
            "version": self.VERSION,
            "canonical_anchor_version":
                self.CANONICAL_ANCHOR_VERSION,
            "current_sprint": self.CURRENT_SPRINT,
            "next_sprint": self.NEXT_SPRINT,
            "boundary": self.BOUNDARY,
            "next_boundary": self.NEXT_BOUNDARY,
            "assertion_count": assertion_count,
            "failed_assertion_count":
                failed_assertion_count,
            "failed_assertions":
                failed_assertions,
            "expected_assertion_count":
                self.EXPECTED_ASSERTION_COUNT,
            "assertion_count_preserved": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
            ),
            "planning_ready": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
                and failed_assertion_count == 0
            ),
            "alpha_ready": (
                assertion_count
                == self.EXPECTED_ASSERTION_COUNT
                and failed_assertion_count == 0
            ),
            "runtime_activation_allowed": False,
            "release_gate_open": False,
            "runtime_ready": False,
        }
