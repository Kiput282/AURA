"""AURA Sprint 182 deterministic service lifecycle runtime core.

This module wraps the Sprint 181 localhost web listener with a deterministic,
in-memory lifecycle state machine.

Implemented lifecycle states:

- stopped
- starting
- running
- stopping
- failed

Implemented runtime controls:

- explicit-confirmation foreground start
- deterministic transition validation
- same-process single-listener ownership
- operating-system port-conflict detection
- startup rollback to stopped
- clean programmatic stop
- clean KeyboardInterrupt and SIGTERM handling when run on the main thread
- bounded transition history
- read-only lifecycle snapshots

Still disabled:

- background daemon operation
- systemd installation or activation
- automatic startup
- persistent PID or lifecycle state files
- remote lifecycle control
- HTTP lifecycle mutation routes
- chat, models, memory writes, permission mutation, audit persistence
- commands, tools, actions, files, desktop, voice, vision, and autonomy
"""

from __future__ import annotations

import json
import signal
import socket
import threading
import time
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from aura.local_web_runtime_alpha import (
    AuraLocalWebRuntimeAlphaManager,
)


class LifecycleState(str, Enum):
    """Allowed deterministic lifecycle states."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    FAILED = "failed"


class LifecycleError(RuntimeError):
    """Base lifecycle runtime error."""


class LifecycleTransitionError(LifecycleError):
    """Raised when an invalid lifecycle transition is attempted."""


class LifecycleStartError(LifecycleError):
    """Raised when a foreground listener cannot start safely."""


class _LifecycleSignal(RuntimeError):
    """Internal exception used to unwind a foreground SIGTERM."""


@dataclass(frozen=True)
class LifecycleTransition:
    """One immutable lifecycle transition record."""

    sequence: int
    from_state: str
    to_state: str
    reason: str
    timestamp_utc: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "sequence": self.sequence,
            "from_state": self.from_state,
            "to_state": self.to_state,
            "reason": self.reason,
            "timestamp_utc": self.timestamp_utc,
        }


class AuraServiceLifecycleRuntimeManager:
    """Manage one foreground localhost listener lifecycle."""

    name = "aura_service_lifecycle_runtime"
    component_version = "0.1.0-alpha"
    sprint = 182

    _ALLOWED_TRANSITIONS = {
        LifecycleState.STOPPED: frozenset(
            {LifecycleState.STARTING}
        ),
        LifecycleState.STARTING: frozenset(
            {
                LifecycleState.RUNNING,
                LifecycleState.STOPPING,
                LifecycleState.FAILED,
            }
        ),
        LifecycleState.RUNNING: frozenset(
            {
                LifecycleState.STOPPING,
                LifecycleState.FAILED,
            }
        ),
        LifecycleState.STOPPING: frozenset(
            {
                LifecycleState.STOPPED,
                LifecycleState.FAILED,
            }
        ),
        LifecycleState.FAILED: frozenset(
            {LifecycleState.STOPPED}
        ),
    }

    _ownership_lock = threading.RLock()
    _active_owner_token: str | None = None
    _active_owner_name: str | None = None

    def __init__(
        self,
        web_runtime: AuraLocalWebRuntimeAlphaManager | None = None,
    ) -> None:
        self.web_runtime = (
            web_runtime
            if web_runtime is not None
            else AuraLocalWebRuntimeAlphaManager()
        )

        self._lock = threading.RLock()
        self._state = LifecycleState.STOPPED
        self._sequence = 0
        self._history: list[LifecycleTransition] = []
        self._server: Any | None = None
        self._owner_token: str | None = None
        self._bound_host: str | None = None
        self._bound_port: int | None = None
        self._started_at_utc: str | None = None
        self._running_since_monotonic: float | None = None
        self._running_since_utc: str | None = None
        self._stopped_at_utc: str | None = self._now_utc()
        self._last_error: str | None = None
        self._last_failure_phase: str | None = None
        self._startup_rollback_count = 0
        self._stop_request_count = 0
        self._last_stop_reason: str | None = None

    @staticmethod
    def _now_utc() -> str:
        return datetime.now(timezone.utc).isoformat()

    @classmethod
    def allowed_transitions(cls) -> dict[str, list[str]]:
        """Return a stable serializable transition contract."""

        return {
            state.value: sorted(
                target.value
                for target in targets
            )
            for state, targets in cls._ALLOWED_TRANSITIONS.items()
        }

    def safety_boundary(self) -> dict[str, Any]:
        """Return the explicit Sprint 182 lifecycle boundary."""

        return {
            "deterministic_state_machine": True,
            "foreground_lifecycle_runtime": True,
            "single_listener_enforced": True,
            "port_conflict_fail_closed": True,
            "startup_rollback_enabled": True,
            "clean_programmatic_stop": True,
            "clean_signal_unwind": True,
            "localhost_only": True,
            "safe_idle_default": True,
            "explicit_confirmation_required": True,
            "read_only_http_runtime": True,
            "background_daemon": False,
            "systemd_runtime": False,
            "automatic_start_runtime": False,
            "persistent_pid_file": False,
            "persistent_lifecycle_state": False,
            "remote_lifecycle_control": False,
            "http_lifecycle_mutation": False,
            "chat_runtime": False,
            "model_runtime": False,
            "memory_write_runtime": False,
            "permission_mutation_runtime": False,
            "audit_write_runtime": False,
            "command_execution": False,
            "tool_execution": False,
            "action_dispatch": False,
            "arbitrary_file_read": False,
            "arbitrary_file_write": False,
            "desktop_control": False,
            "voice_runtime": False,
            "vision_runtime": False,
            "autonomous_action": False,
        }

    def _transition(
        self,
        target: LifecycleState,
        *,
        reason: str,
    ) -> LifecycleTransition:
        with self._lock:
            current = self._state
            allowed = self._ALLOWED_TRANSITIONS[current]
            if target not in allowed:
                raise LifecycleTransitionError(
                    "Invalid lifecycle transition: "
                    f"{current.value} -> {target.value}"
                )

            self._sequence += 1
            transition = LifecycleTransition(
                sequence=self._sequence,
                from_state=current.value,
                to_state=target.value,
                reason=str(reason),
                timestamp_utc=self._now_utc(),
            )
            self._state = target
            self._history.append(transition)
            self._history = self._history[-32:]
            return transition

    def _acquire_ownership(self) -> str:
        token = uuid.uuid4().hex

        with type(self)._ownership_lock:
            if type(self)._active_owner_token is not None:
                raise LifecycleStartError(
                    "Single-listener guard blocked a second "
                    "same-process lifecycle owner."
                )

            type(self)._active_owner_token = token
            type(self)._active_owner_name = self.name
            self._owner_token = token
            return token

    def _release_ownership(self) -> None:
        with type(self)._ownership_lock:
            if (
                self._owner_token is not None
                and type(self)._active_owner_token
                == self._owner_token
            ):
                type(self)._active_owner_token = None
                type(self)._active_owner_name = None
            self._owner_token = None

    @classmethod
    def process_owner_status(cls) -> dict[str, Any]:
        with cls._ownership_lock:
            return {
                "active": cls._active_owner_token is not None,
                "owner_name": cls._active_owner_name,
            }

    def _uptime_seconds(self) -> float:
        with self._lock:
            if self._running_since_monotonic is None:
                return 0.0
            return round(
                max(
                    0.0,
                    time.monotonic()
                    - self._running_since_monotonic,
                ),
                6,
            )

    def snapshot(self) -> dict[str, Any]:
        """Return a read-only lifecycle snapshot."""

        with self._lock:
            state = self._state
            history = [
                item.as_dict()
                for item in self._history
            ]
            listener_active = (
                state == LifecycleState.RUNNING
                and self._server is not None
            )

            return {
                "name": self.name,
                "component_version": self.component_version,
                "sprint": self.sprint,
                "state": state.value,
                "safe_idle": state
                in {
                    LifecycleState.STOPPED,
                    LifecycleState.STARTING,
                    LifecycleState.STOPPING,
                    LifecycleState.FAILED,
                },
                "listener_active": listener_active,
                "bound_host": (
                    self._bound_host
                    if listener_active
                    else None
                ),
                "bound_port": (
                    self._bound_port
                    if listener_active
                    else None
                ),
                "transition_sequence": self._sequence,
                "transition_count": len(history),
                "transition_history": history,
                "allowed_transitions": self.allowed_transitions(),
                "started_at_utc": self._started_at_utc,
                "running_since_utc": self._running_since_utc,
                "stopped_at_utc": self._stopped_at_utc,
                "uptime_seconds": self._uptime_seconds(),
                "last_error": self._last_error,
                "last_failure_phase": self._last_failure_phase,
                "startup_rollback_count": (
                    self._startup_rollback_count
                ),
                "stop_request_count": self._stop_request_count,
                "last_stop_reason": self._last_stop_reason,
                "process_owner": self.process_owner_status(),
                "runtime_execution_features": (
                    1 if listener_active else 0
                ),
                **self.safety_boundary(),
            }

    def _record_failure(
        self,
        *,
        phase: str,
        error: BaseException,
    ) -> None:
        with self._lock:
            self._last_failure_phase = str(phase)
            self._last_error = (
                f"{type(error).__name__}: {error}"
            )

    def _startup_rollback(
        self,
        *,
        error: BaseException,
    ) -> None:
        self._record_failure(
            phase="startup",
            error=error,
        )

        with self._lock:
            current = self._state

        if current == LifecycleState.STARTING:
            self._transition(
                LifecycleState.FAILED,
                reason="startup_failed",
            )

        with self._lock:
            self._startup_rollback_count += 1
            server = self._server
            self._server = None
            self._bound_host = None
            self._bound_port = None

        if server is not None:
            try:
                server.server_close()
            except Exception:
                pass

        self._release_ownership()

        with self._lock:
            current = self._state

        if current == LifecycleState.FAILED:
            self._transition(
                LifecycleState.STOPPED,
                reason="startup_rollback_complete",
            )
            with self._lock:
                self._stopped_at_utc = self._now_utc()

    def _install_main_thread_signal_handlers(
        self,
    ) -> dict[int, Any]:
        if threading.current_thread() is not threading.main_thread():
            return {}

        previous: dict[int, Any] = {}

        def handle_sigterm(
            signum: int,
            frame: Any,
        ) -> None:
            del signum, frame
            raise _LifecycleSignal("SIGTERM")

        previous[signal.SIGTERM] = signal.getsignal(
            signal.SIGTERM
        )
        signal.signal(signal.SIGTERM, handle_sigterm)
        return previous

    @staticmethod
    def _restore_signal_handlers(
        previous: dict[int, Any],
    ) -> None:
        for signum, handler in previous.items():
            signal.signal(signum, handler)

    def run_foreground(
        self,
        *,
        confirmed: bool,
        port_override: int | None = None,
        ready_event: threading.Event | None = None,
    ) -> None:
        """Start and own one foreground listener until stopped."""

        config = self.web_runtime.load_config()
        if (
            config.require_explicit_confirmation
            and not confirmed
        ):
            raise LifecycleStartError(
                "Explicit confirmation is required for "
                "the Sprint 182 lifecycle runtime."
            )

        with self._lock:
            if self._state != LifecycleState.STOPPED:
                raise LifecycleStartError(
                    "Lifecycle start requires state stopped; "
                    f"current state is {self._state.value}."
                )
            self._last_error = None
            self._last_failure_phase = None
            self._last_stop_reason = None
            self._started_at_utc = self._now_utc()
            self._stopped_at_utc = None

        self._transition(
            LifecycleState.STARTING,
            reason="explicit_foreground_start",
        )

        try:
            self._acquire_ownership()
            server = self.web_runtime.create_server(
                port_override=port_override
            )
        except Exception as exc:
            self._startup_rollback(error=exc)
            if isinstance(exc, LifecycleStartError):
                raise
            raise LifecycleStartError(
                f"Lifecycle startup failed: {exc}"
            ) from exc

        bound_host, bound_port = server.server_address[:2]
        with self._lock:
            self._server = server
            self._bound_host = str(bound_host)
            self._bound_port = int(bound_port)
            self._running_since_monotonic = time.monotonic()
            self._running_since_utc = self._now_utc()

        self._transition(
            LifecycleState.RUNNING,
            reason="listener_bound_and_ready",
        )

        if ready_event is not None:
            ready_event.set()

        previous_handlers = (
            self._install_main_thread_signal_handlers()
        )

        try:
            server.serve_forever(poll_interval=0.05)
        except KeyboardInterrupt:
            with self._lock:
                self._last_stop_reason = "SIGINT"
        except _LifecycleSignal as exc:
            with self._lock:
                self._last_stop_reason = str(exc)
        except BaseException as exc:
            self._record_failure(
                phase="running",
                error=exc,
            )
            with self._lock:
                current = self._state
            if current == LifecycleState.RUNNING:
                self._transition(
                    LifecycleState.FAILED,
                    reason="runtime_failure",
                )
            raise
        finally:
            self._restore_signal_handlers(
                previous_handlers
            )

            with self._lock:
                current = self._state

            if current == LifecycleState.RUNNING:
                self._transition(
                    LifecycleState.STOPPING,
                    reason="foreground_unwind",
                )
            elif current == LifecycleState.FAILED:
                self._transition(
                    LifecycleState.STOPPED,
                    reason="failed_runtime_cleanup",
                )

            try:
                server.server_close()
            finally:
                with self._lock:
                    self._server = None
                    self._bound_host = None
                    self._bound_port = None
                    self._running_since_monotonic = None
                    self._running_since_utc = None

                self._release_ownership()

                with self._lock:
                    current = self._state

                if current == LifecycleState.STOPPING:
                    self._transition(
                        LifecycleState.STOPPED,
                        reason="listener_closed",
                    )

                with self._lock:
                    self._stopped_at_utc = self._now_utc()

    def request_stop(
        self,
        *,
        reason: str = "programmatic_stop",
    ) -> dict[str, Any]:
        """Request clean shutdown from another thread."""

        with self._lock:
            state = self._state
            server = self._server

            if state == LifecycleState.STOPPED:
                return {
                    "accepted": False,
                    "reason": "already_stopped",
                    "state": state.value,
                }

            if state == LifecycleState.FAILED:
                return {
                    "accepted": False,
                    "reason": "failed_state_requires_cleanup",
                    "state": state.value,
                }

            if state == LifecycleState.STOPPING:
                return {
                    "accepted": False,
                    "reason": "stop_already_in_progress",
                    "state": state.value,
                }

            self._stop_request_count += 1
            self._last_stop_reason = str(reason)

        self._transition(
            LifecycleState.STOPPING,
            reason=str(reason),
        )

        if server is not None:
            server.shutdown()

        return {
            "accepted": True,
            "reason": str(reason),
            "state": LifecycleState.STOPPING.value,
        }

    @staticmethod
    def _http_health(
        host: str,
        port: int,
    ) -> dict[str, Any]:
        with urllib.request.urlopen(
            f"http://{host}:{port}/health",
            timeout=2.0,
        ) as response:
            return json.loads(
                response.read().decode("utf-8")
            )

    @staticmethod
    def _wait_for_state(
        manager: "AuraServiceLifecycleRuntimeManager",
        state: LifecycleState,
        *,
        timeout: float = 3.0,
    ) -> dict[str, Any]:
        deadline = time.monotonic() + timeout

        while time.monotonic() < deadline:
            snapshot = manager.snapshot()
            if snapshot["state"] == state.value:
                return snapshot
            time.sleep(0.02)

        raise LifecycleError(
            f"Timed out waiting for lifecycle state {state.value}."
        )

    @staticmethod
    def _port_closed(
        host: str,
        port: int,
    ) -> bool:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        sock.settimeout(0.3)
        try:
            return sock.connect_ex((host, port)) != 0
        finally:
            sock.close()

    @staticmethod
    def _bind_port_blocker(
        host: str,
        port: int,
    ) -> socket.socket:
        blocker = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM,
        )
        blocker.setsockopt(
            socket.SOL_SOCKET,
            socket.SO_REUSEADDR,
            1,
        )
        blocker.bind((host, port))
        blocker.listen(1)
        return blocker

    def self_test(self) -> dict[str, Any]:
        """Exercise lifecycle, single-owner, and rollback behavior."""

        assertions: dict[str, bool] = {}

        baseline = self.snapshot()
        assertions["baseline_stopped"] = (
            baseline["state"] == "stopped"
        )
        assertions["baseline_safe_idle"] = (
            baseline["safe_idle"] is True
        )
        assertions["baseline_listener_inactive"] = (
            baseline["listener_active"] is False
        )
        assertions["baseline_runtime_features_zero"] = (
            baseline["runtime_execution_features"] == 0
        )
        assertions["transition_contract_has_five_states"] = (
            len(baseline["allowed_transitions"]) == 5
        )
        assertions["background_daemon_blocked"] = (
            baseline["background_daemon"] is False
        )
        assertions["systemd_blocked"] = (
            baseline["systemd_runtime"] is False
        )
        assertions["automatic_start_blocked"] = (
            baseline["automatic_start_runtime"] is False
        )
        assertions["chat_blocked"] = (
            baseline["chat_runtime"] is False
        )
        assertions["command_blocked"] = (
            baseline["command_execution"] is False
        )

        invalid_transition_blocked = False
        try:
            self._transition(
                LifecycleState.RUNNING,
                reason="invalid_test",
            )
        except LifecycleTransitionError:
            invalid_transition_blocked = True
        assertions["invalid_transition_blocked"] = (
            invalid_transition_blocked
        )

        ready = threading.Event()
        runtime_thread = threading.Thread(
            target=self.run_foreground,
            kwargs={
                "confirmed": True,
                "port_override": 0,
                "ready_event": ready,
            },
            name="aura-s182-lifecycle-self-test",
            daemon=True,
        )
        runtime_thread.start()

        if not ready.wait(timeout=3.0):
            raise LifecycleError(
                "Lifecycle self-test listener did not become ready."
            )

        running = self._wait_for_state(
            self,
            LifecycleState.RUNNING,
        )
        host = str(running["bound_host"])
        port = int(running["bound_port"])

        assertions["running_state_reached"] = (
            running["state"] == "running"
        )
        assertions["listener_active_running"] = (
            running["listener_active"] is True
        )
        assertions["runtime_feature_one_running"] = (
            running["runtime_execution_features"] == 1
        )
        assertions["bound_to_ipv4_localhost"] = (
            host == "127.0.0.1"
        )
        assertions["ephemeral_port_allocated"] = (
            port > 0
        )
        assertions["process_owner_active"] = (
            running["process_owner"]["active"] is True
        )

        health = self._http_health(host, port)
        assertions["health_endpoint_ok"] = (
            health.get("status") == "ok"
        )
        assertions["health_safe_idle"] = (
            health.get("safe_idle") is True
        )
        assertions["health_command_blocked"] = (
            health.get("command_execution") is False
        )

        second = AuraServiceLifecycleRuntimeManager(
            web_runtime=self.web_runtime
        )
        second_owner_blocked = False
        try:
            second.run_foreground(
                confirmed=True,
                port_override=0,
            )
        except LifecycleStartError:
            second_owner_blocked = True

        assertions["second_owner_blocked"] = (
            second_owner_blocked
        )
        second_snapshot = second.snapshot()
        assertions["second_owner_rolled_back"] = (
            second_snapshot["state"] == "stopped"
        )
        assertions["second_owner_rollback_count_one"] = (
            second_snapshot["startup_rollback_count"] == 1
        )

        stop_result = self.request_stop(
            reason="self_test_stop",
        )
        assertions["programmatic_stop_accepted"] = (
            stop_result["accepted"] is True
        )

        runtime_thread.join(timeout=3.0)
        assertions["runtime_thread_stopped"] = (
            not runtime_thread.is_alive()
        )

        stopped = self.snapshot()
        assertions["clean_final_stopped"] = (
            stopped["state"] == "stopped"
        )
        assertions["listener_inactive_after_stop"] = (
            stopped["listener_active"] is False
        )
        assertions["runtime_feature_zero_after_stop"] = (
            stopped["runtime_execution_features"] == 0
        )
        assertions["owner_released_after_stop"] = (
            stopped["process_owner"]["active"] is False
        )
        assertions["ephemeral_port_closed"] = (
            self._port_closed(host, port)
        )
        assertions["stop_request_recorded"] = (
            stopped["stop_request_count"] == 1
        )
        assertions["normal_transition_count_four"] = (
            stopped["transition_count"] == 4
        )
        assertions["normal_transition_sequence"] = (
            [
                item["to_state"]
                for item in stopped["transition_history"]
            ]
            == [
                "starting",
                "running",
                "stopping",
                "stopped",
            ]
        )

        config = self.web_runtime.load_config()
        blocker = self._bind_port_blocker(
            config.host,
            config.port,
        )

        conflict = AuraServiceLifecycleRuntimeManager(
            web_runtime=self.web_runtime
        )
        conflict_blocked = False
        try:
            conflict.run_foreground(
                confirmed=True,
            )
        except LifecycleStartError:
            conflict_blocked = True
        finally:
            blocker.close()

        assertions["configured_port_conflict_blocked"] = (
            conflict_blocked
        )

        conflict_snapshot = conflict.snapshot()
        assertions["conflict_rolled_back_stopped"] = (
            conflict_snapshot["state"] == "stopped"
        )
        assertions["conflict_failure_recorded"] = (
            conflict_snapshot["last_failure_phase"]
            == "startup"
        )
        assertions["conflict_error_visible"] = (
            bool(conflict_snapshot["last_error"])
        )
        assertions["conflict_rollback_count_one"] = (
            conflict_snapshot["startup_rollback_count"] == 1
        )
        assertions["conflict_transition_sequence"] = (
            [
                item["to_state"]
                for item in conflict_snapshot[
                    "transition_history"
                ]
            ]
            == [
                "starting",
                "failed",
                "stopped",
            ]
        )
        assertions["owner_released_after_conflict"] = (
            conflict_snapshot["process_owner"]["active"]
            is False
        )
        assertions["configured_port_closed_after_blocker"] = (
            self._port_closed(
                config.host,
                config.port,
            )
        )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise LifecycleError(
                "Lifecycle self-test failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "states": [
                state.value
                for state in LifecycleState
            ],
            "normal_transition_sequence": [
                "starting",
                "running",
                "stopping",
                "stopped",
            ],
            "failure_transition_sequence": [
                "starting",
                "failed",
                "stopped",
            ],
            "single_listener_enforced": True,
            "port_conflict_fail_closed": True,
            "startup_rollback_verified": True,
            "clean_programmatic_stop_verified": True,
            "configured_port": config.port,
            "configured_port_closed_after_test": True,
        }
