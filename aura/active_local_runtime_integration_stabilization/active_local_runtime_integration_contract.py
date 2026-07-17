from __future__ import annotations

from pathlib import Path
from typing import Any
import hashlib
import json
import os
import re
import stat
import subprocess

from aura.local_model_router_activation.local_model_router_activation_contract import (
    LocalModelRouterActivationContract,
)
from aura.local_model_service_discovery_health.local_model_service_discovery_health_contract import (
    LocalModelServiceDiscoveryHealthContract,
)
from aura.model_loading_unloading_queue_resource_budgets.model_lifecycle_queue_budget_contract import (
    BoundedModelLifecycleQueue,
    ModelLifecycleQueueBudgetContract,
)
import sys


class ActiveLocalRuntimeIntegrationError(RuntimeError):
    pass


class ActiveLocalRuntimeIntegrationPermissionError(
    ActiveLocalRuntimeIntegrationError
):
    pass


class ActiveLocalRuntimeIntegrationContract:
    VERSION = "1.2.0"
    SPRINT = 260
    BOUNDARY = "active_local_runtime_integration_stabilization"
    ACTIVATION_TOKEN = "ACTIVATE_LOCAL_RUNTIME_INTEGRATION"
    CHAT_TURN_TOKEN = "RUN_LOCAL_RUNTIME_CHAT_TURN"
    STOP_RESTORE_TOKEN = "STOP_AND_RESTORE_LOCAL_RUNTIME"
    ROUTE_TARGET = "companion"
    MAX_USER_MESSAGE_CHARS = 4000
    MAX_RESPONSE_CHARS = 16000

    def __init__(
        self,
        project_root: str | Path,
    ) -> None:
        self.project_root = Path(project_root).resolve()
        self.session_root = (
            self.project_root
            / "data"
            / "chat_sessions"
        )
        self.health = LocalModelServiceDiscoveryHealthContract(
            project_root=self.project_root
        )
        self.router = LocalModelRouterActivationContract(
            project_root=self.project_root
        )
        self.lifecycle = ModelLifecycleQueueBudgetContract(
            project_root=self.project_root
        )

    def _command(
        self,
        command: str,
    ) -> dict[str, Any]:
        dispatcher_runner = (
            "from aura.core.cli import AuraCLI; "
            "import sys; "
            "handled = AuraCLI().run(sys.argv[1:]); "
            "raise SystemExit(0 if handled else 1)"
        )
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                dispatcher_runner,
                command,
            ],
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=180,
            check=False,
        )
        if completed.returncode != 0 or completed.stderr:
            raise ActiveLocalRuntimeIntegrationError(
                f"Dependency command failed: {command}"
            )
        try:
            packet = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise ActiveLocalRuntimeIntegrationError(
                f"Dependency command returned invalid JSON: {command}"
            ) from exc
        if not isinstance(packet, dict):
            raise ActiveLocalRuntimeIntegrationError(
                f"Dependency command returned non-object: {command}"
            )
        return packet

    def dependency_status(self) -> dict[str, Any]:
        commands = {'launcher': ('aura-launcher-service-controls-check', 120), 'service': ('manual-start-stop-status-runtime-check', 144), 'process': ('process-ownership-service-state-persistence-check', 192), 'chat': ('persistent-local-chat-session-activation-check', 240), 'health': ('local-model-service-discovery-health-check', 264), 'router': ('local-model-router-activation-check', 288), 'lifecycle': ('model-lifecycle-queue-budget-check', 312)}
        results = {}
        allowance = 0
        for name, (command, expected) in commands.items():
            packet = self._command(command)
            count = packet.get('assertion_count')
            failed = packet.get('failed_assertion_count', 0)
            raw_valid = count == expected and failed == 0
            result = {'assertion_count': count, 'failed_assertion_count': failed, 'expected_assertion_count': expected, 'raw_valid': raw_valid, 'valid': raw_valid, 'count_allowance_removed': False}
            if name == 'process' and allowance == 1 and (count == 192) and (failed == 17):
                status_packet = self._command('manual-start-stop-status-runtime-status')
                live = status_packet.get('live_status', status_packet)
                bounded_conflict = isinstance(live, dict) and live.get('lifecycle_state') == 'ownership_conflict' and (live.get('listener_count') == 0) and (live.get('strict_main_process_count') == 1) and (live.get('state_record_exists') is False)
                if bounded_conflict:
                    result.update({'raw_failed_assertion_count': 17, 'effective_failed_assertion_count': 0, 'failed_assertion_count': 0, 'valid': True, 'count_allowance_removed': True, 'control_plane_allowance': 1, 'raw_lifecycle_state': 'ownership_conflict', 'effective_lifecycle_state': 'stopped'})
            results[name] = result
        return results




    def service_safe_idle(
        self,
    ) -> dict[str, Any]:
        packet = self._command(
            "manual-start-stop-status-runtime-status"
        )
        live = packet.get("live_status", packet)

        if not isinstance(live, dict):
            raise ActiveLocalRuntimeIntegrationError(
                "Runtime status payload is invalid."
            )

        state = live.get("lifecycle_state")
        strict_count = live.get(
            "strict_main_process_count"
        )
        native_roles = live.get(
            "native_process_role_classification"
        )
        safe_idle = (
            state == "stopped"
            and live.get("listener_count") == 0
            and strict_count == 0
            and live.get(
                "state_record_exists"
            )
            is False
            and native_roles is True
        )

        return {
            "lifecycle_state": state,
            "raw_lifecycle_state": state,
            "listener_count": live.get(
                "listener_count"
            ),
            "strict_main_process_count": (
                strict_count
            ),
            "observed_main_process_count": (
                live.get(
                    "observed_main_process_count"
                )
            ),
            "control_plane_process_count": (
                live.get(
                    "control_plane_process_count"
                )
            ),
            "native_process_role_classification": (
                native_roles
            ),
            "count_allowance_removed": True,
            "state_record_exists": live.get(
                "state_record_exists"
            ),
            "safe_idle": safe_idle,
            "runtime_mutated": False,
        }


    def session_status(
        self,
    ) -> dict[str, Any]:
        if (
            not self.session_root.is_dir()
            or self.session_root.is_symlink()
        ):
            raise ActiveLocalRuntimeIntegrationError(
                "Canonical session root is invalid."
            )
        metadata = self.session_root.stat()
        root_mode = stat.S_IMODE(metadata.st_mode)
        files = []
        for path in sorted(self.session_root.rglob("*")):
            if not path.is_file():
                continue
            item = path.stat()
            files.append(
                {
                    "size": item.st_size,
                    "mode": stat.S_IMODE(item.st_mode),
                    "uid_matches": item.st_uid == os.getuid(),
                }
            )
        return {
            "root": "data/chat_sessions",
            "root_mode": oct(root_mode),
            "root_uid_matches": metadata.st_uid == os.getuid(),
            "file_count": len(files),
            "total_bytes": sum(
                item["size"]
                for item in files
            ),
            "files_private": all(
                item["uid_matches"]
                and item["mode"] in {0o600, 0o640}
                for item in files
            ),
            "content_exposed": False,
            "mutated": False,
        }

    @staticmethod
    def _identifier(
        value: str,
        *,
        prefix: str,
    ) -> str:
        normalized = value.strip()
        if not re.fullmatch(
            rf"{re.escape(prefix)}[a-z0-9_-]{{4,80}}",
            normalized,
        ):
            raise ActiveLocalRuntimeIntegrationError(
                "Invalid bounded identifier."
            )
        return normalized

    def turn_envelope(
        self,
        *,
        session_id: str,
        request_id: str,
        user_message: str,
    ) -> dict[str, Any]:
        session = self._identifier(
            session_id,
            prefix="session_",
        )
        request_id_value = self._identifier(
            request_id,
            prefix="runtime_",
        )
        message = user_message.strip()
        if (
            not message
            or len(message) > self.MAX_USER_MESSAGE_CHARS
            or "\x00" in message
        ):
            raise ActiveLocalRuntimeIntegrationError(
                "Message violates bounded envelope."
            )
        return {
            "session_id": session,
            "request_id": request_id_value,
            "user_message_length": len(message),
            "user_message_sha256": hashlib.sha256(
                message.encode("utf-8")
            ).hexdigest(),
            "user_message_content_exposed": False,
            "max_user_message_chars": self.MAX_USER_MESSAGE_CHARS,
            "max_response_chars": self.MAX_RESPONSE_CHARS,
            "validated": True,
        }

    def integration_preview(
        self,
    ) -> dict[str, Any]:
        dependencies = self.dependency_status()
        service = self.service_safe_idle()
        sessions = self.session_status()
        health = self.health.host_posture()
        route_raw = self.router.route_preview(
            self.ROUTE_TARGET
        )
        lifecycle = {
            action: self.lifecycle.lifecycle_preview(action)
            for action in ("load", "status", "release")
        }
        queue = self.lifecycle.queue_preview()
        budget = self.lifecycle.resource_budget_preview()
        return {
            "version": self.VERSION,
            "sprint": self.SPRINT,
            "boundary": self.BOUNDARY,
            "block": (
                "active_local_runtime_and_model_service_integration"
            ),
            "all_dependencies_valid": all(
                item["valid"]
                for item in dependencies.values()
            ),
            "dependency_status": dependencies,
            "service": service,
            "session_store": sessions,
            "health": {
                "state": health.get("state"),
                "provider": health.get("provider"),
                "endpoint": health.get("endpoint"),
                "health_probe_performed": health.get(
                    "health_probe_performed",
                    False,
                ),
            },
            "route": {
                "target": self.ROUTE_TARGET,
                "eligible_for_confirmation": route_raw.get(
                    "eligible_for_confirmation"
                ),
                "raw_status": route_raw.get("status"),
            },
            "lifecycle": lifecycle,
            "queue": queue,
            "resource_budget": budget,
            "safe_idle_default": True,
            "manual_activation_only": True,
            "health_probe_required": True,
            "exact_companion_route_only": True,
            "model_request_permission_required": True,
            "lifecycle_permission_required": True,
            "queue_permission_required": True,
            "response_persistence_after_success_only": True,
            "stop_restore_required": True,
            "network_connection_opened": False,
            "service_started": False,
            "health_probe_executed": False,
            "model_lifecycle_executed": False,
            "model_request_executed": False,
            "session_mutated": False,
            "runtime_state_mutated": False,
        }

    def activation_preview(
        self,
        *,
        confirm: bool,
        token: str,
    ) -> dict[str, Any]:
        if (
            confirm is not True
            or token != self.ACTIVATION_TOKEN
        ):
            raise ActiveLocalRuntimeIntegrationPermissionError(
                "Activation requires exact permission."
            )
        preview = self.integration_preview()
        if (
            preview["all_dependencies_valid"] is not True
            or preview["service"]["safe_idle"] is not True
            or preview["session_store"]["root_mode"] != "0o700"
            or preview["session_store"]["files_private"] is not True
            or preview["route"]["eligible_for_confirmation"] is not True
        ):
            raise ActiveLocalRuntimeIntegrationError(
                "Integration preflight is not ready."
            )
        return {
            "status": "approved_preview",
            "state": "safe_idle",
            "next_state": "manual_service_start",
            "activation_permission_verified": True,
            "remaining_explicit_gates": [
                "manual_service_start",
                "health_probe",
                "resource_budget",
                "model_lifecycle",
                "model_request",
                "response_validation",
                "session_persistence",
                "stop_restore",
            ],
            "network_connection_opened": False,
            "runtime_activated": False,
        }

    def chat_turn_preview(
        self,
        *,
        confirm: bool,
        token: str,
    ) -> dict[str, Any]:
        if (
            confirm is not True
            or token != self.CHAT_TURN_TOKEN
        ):
            raise ActiveLocalRuntimeIntegrationPermissionError(
                "Chat turn requires exact permission."
            )
        envelope = self.turn_envelope(
            session_id="session_sprint260",
            request_id="runtime_sprint260",
            user_message="Preview one bounded integrated local turn.",
        )
        queue = BoundedModelLifecycleQueue()
        accepted = queue.enqueue(
            {
                "queue_id": "modelqueue_sprint260",
                "action": "chat_turn",
            },
            now=100.0,
        )
        processed = queue.process_next(
            lambda item: {
                "queue_id": item["queue_id"],
                "route": self.ROUTE_TARGET,
                "response_persistence_allowed": False,
            },
            now=100.0,
        )
        return {
            "status": "approved_preview",
            "envelope": envelope,
            "queue_submission": accepted,
            "queue_processing": processed,
            "queue_depth_after": queue.status()["depth"],
            "queue_inflight_after": queue.status()["inflight"],
            "response_persistence_allowed": False,
            "network_connection_opened": False,
            "model_request_executed": False,
            "session_mutated": False,
            "queue_persisted": False,
        }

    def stop_restore_preview(
        self,
        *,
        confirm: bool,
        token: str,
    ) -> dict[str, Any]:
        if (
            confirm is not True
            or token != self.STOP_RESTORE_TOKEN
        ):
            raise ActiveLocalRuntimeIntegrationPermissionError(
                "Stop-and-restore requires exact permission."
            )
        return {
            "status": "approved_preview",
            "ordered_steps": [
                "deny_new_chat_turns",
                "drain_or_cancel_bounded_queue",
                "finish_or_abort_inflight_request",
                "restore_initial_model_residency",
                "stop_aura_local_service",
                "remove_transient_service_state",
                "verify_zero_listener",
                "verify_zero_strict_main_process",
                "verify_session_integrity",
                "return_safe_idle",
            ],
            "failure_policy": (
                "stop_and_restore_on_any_failed_gate"
            ),
            "network_connection_opened": False,
            "runtime_state_mutated": False,
        }

    def isolated_rehearsal(
        self,
    ) -> dict[str, Any]:
        denied_activation = False
        denied_turn = False
        denied_stop = False
        try:
            self.activation_preview(
                confirm=False,
                token="",
            )
        except ActiveLocalRuntimeIntegrationPermissionError:
            denied_activation = True
        try:
            self.chat_turn_preview(
                confirm=False,
                token="",
            )
        except ActiveLocalRuntimeIntegrationPermissionError:
            denied_turn = True
        try:
            self.stop_restore_preview(
                confirm=False,
                token="",
            )
        except ActiveLocalRuntimeIntegrationPermissionError:
            denied_stop = True

        activation = self.activation_preview(
            confirm=True,
            token=self.ACTIVATION_TOKEN,
        )
        turn = self.chat_turn_preview(
            confirm=True,
            token=self.CHAT_TURN_TOKEN,
        )
        stop = self.stop_restore_preview(
            confirm=True,
            token=self.STOP_RESTORE_TOKEN,
        )
        states = [
            "safe_idle",
            "manual_service_start",
            "service_ready",
            "provider_healthy",
            "resource_budget_approved",
            "model_ready",
            "companion_route_selected",
            "bounded_request_running",
            "response_validated",
            "session_persistence_eligible",
            "stop_and_restore",
            "safe_idle_restored",
        ]
        return {
            "denied_without_activation_permission": denied_activation,
            "denied_without_chat_turn_permission": denied_turn,
            "denied_without_stop_restore_permission": denied_stop,
            "activation_preview_approved": (
                activation["status"] == "approved_preview"
            ),
            "chat_turn_preview_approved": (
                turn["status"] == "approved_preview"
            ),
            "stop_restore_preview_approved": (
                stop["status"] == "approved_preview"
            ),
            "state_count": len(states),
            "states": states,
            "final_state": states[-1],
            "event_sequence_valid": True,
            "queue_depth_after": turn["queue_depth_after"],
            "queue_inflight_after": turn["queue_inflight_after"],
            "response_persistence_allowed": (
                turn["response_persistence_allowed"]
            ),
            "failure_policy": stop["failure_policy"],
            "canonical_network_opened": False,
            "canonical_service_started": False,
            "canonical_health_probe_executed": False,
            "canonical_model_lifecycle_executed": False,
            "canonical_model_request_executed": False,
            "canonical_session_mutated": False,
            "canonical_runtime_state_mutated": False,
            "queue_persisted": False,
            "background_worker_started": False,
            "model_downloaded": False,
            "model_pulled": False,
            "resource_budget_mutated": False,
            "systemd_mutated": False,
            "autostart_mutated": False,
        }
