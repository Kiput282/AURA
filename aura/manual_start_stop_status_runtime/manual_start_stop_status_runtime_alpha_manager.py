from __future__ import annotations

from pathlib import Path
from typing import Any

from .manual_start_stop_status_runtime_executor import (
    ManualStartStopStatusRuntimeExecutor,
)
from .manual_start_stop_status_runtime_planner import (
    ManualStartStopStatusRuntimePlanner,
)


class ManualStartStopStatusRuntimeAlphaManager:
    def __init__(
        self,
        project_root: Path,
        *,
        state_path: str | Path | None = None,
        lock_path: str | Path | None = None,
        log_path: str | Path | None = None,
    ) -> None:
        self.planner = (
            ManualStartStopStatusRuntimePlanner(
                project_root=project_root
            )
        )
        self.executor = (
            ManualStartStopStatusRuntimeExecutor(
                project_root=project_root,
                state_path=state_path,
                lock_path=lock_path,
                log_path=log_path,
            )
        )

    def status(self) -> dict[str, Any]:
        packet = self.planner.status()
        packet["live_status"] = (
            self.executor.status(
                probe_health=True
            )
        )
        packet["status_observation_enabled"] = True
        packet["start_execution_enabled"] = True
        packet["stop_execution_enabled"] = True
        packet["restart_execution_enabled"] = False
        return packet

    def context(self) -> dict[str, Any]:
        packet = self.planner.context()
        packet["runtime_paths"] = {
            "state_path": str(
                self.executor.state_path
            ),
            "lock_path": str(
                self.executor.lock_path
            ),
            "log_path": str(
                self.executor.log_path
            ),
        }
        packet["runtime_commands"] = {
            "start": (
                "manual-start-stop-status-runtime-start "
                "--approve-start --confirm-localhost"
            ),
            "stop": (
                "manual-start-stop-status-runtime-stop "
                "--approve-stop"
            ),
            "status": (
                "manual-start-stop-status-runtime-status"
            ),
        }
        packet["permission_mode"] = (
            "explicit_cli_confirmation"
        )
        packet["audit_persistence_enabled"] = False
        packet["phase_b_activation_required"] = False
        return packet

    def review(self) -> dict[str, Any]:
        packet = self.planner.review()
        packet["executor_policy"] = {
            "canonical_child_command": list(
                self.executor.expected_argv
            ),
            "temporary_state_only": True,
            "state_path": str(
                self.executor.state_path
            ),
            "lock_path": str(
                self.executor.lock_path
            ),
            "log_path": str(
                self.executor.log_path
            ),
            "shell_execution": False,
            "systemd_execution": False,
            "autostart_execution": False,
            "non_loopback_binding": False,
            "owned_pid_required_for_signal": True,
            "proc_start_ticks_required": True,
            "exact_argv_required": True,
            "exact_cwd_required": True,
            "health_contract_required": True,
            "bounded_start_timeout_seconds": (
                self.executor.START_TIMEOUT_SECONDS
            ),
            "bounded_stop_timeout_seconds": (
                self.executor.STOP_TIMEOUT_SECONDS
            ),
            "bounded_kill_fallback": True,
        }
        return packet

    def check(self) -> dict[str, Any]:
        packet = self.planner.check()
        packet["runtime_executor_available"] = True
        packet["status_observer_available"] = True
        packet["manual_start_available"] = True
        packet["manual_stop_available"] = True
        packet["restart_available"] = False
        packet["autostart_available"] = False
        packet["systemd_available"] = False
        packet["ownership_record_scope"] = (
            "temporary_user_runtime"
        )
        packet["audit_persistence_enabled"] = False
        return packet

    def start(
        self,
        *,
        approved: bool,
        confirmed_localhost: bool,
    ) -> dict[str, Any]:
        return self.executor.start(
            approved=approved,
            confirmed_localhost=(
                confirmed_localhost
            ),
        )

    def stop(
        self,
        *,
        approved: bool,
    ) -> dict[str, Any]:
        return self.executor.stop(
            approved=approved
        )
