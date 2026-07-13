"""Sprint 227 service persistence and launcher contract.

This module defines metadata-only contracts for future AURA service
persistence, lifecycle visibility, recovery metadata, and launcher surfaces.

It does not instantiate the active service lifecycle runtime and does not
start, stop, persist, install, bind, spawn, launch, or enable anything.
"""

from __future__ import annotations

import inspect
from pathlib import Path
from typing import Any

from aura.launcher_monitor.aura_launcher_health_monitor_foundation_manager import (
    AuraLauncherHealthMonitorFoundationManager,
)
from aura.local_service_runtime_foundation.aura_local_service_runtime_foundation_manager import (
    AuraLocalServiceRuntimeFoundationManager,
)
from aura.partner_runtime.multi_interface_state_synchronization_alpha_manager import (
    MultiInterfaceStateSynchronizationAlphaManager,
)
from aura.runtime_service.aura_runtime_service_foundation_manager import (
    AuraRuntimeServiceFoundationManager,
)
from aura.service_lifecycle_runtime.aura_service_lifecycle_runtime_manager import (
    AuraServiceLifecycleRuntimeManager,
    LifecycleState,
)


class ServicePersistenceAndLauncherPlanner:
    """Build the deterministic Sprint 227 metadata contract."""

    name = "service_persistence_and_launcher"
    version = "0.1.0-alpha"
    sprint = 227

    expected_assertion_count = 208

    canonical_lifecycle_owner = (
        "aura.service_lifecycle_runtime."
        "AuraServiceLifecycleRuntimeManager"
    )

    canonical_lifecycle_access_mode = (
        "static_contract_metadata_only"
    )

    launcher_foundation_owner = (
        "aura.launcher_monitor."
        "AuraLauncherHealthMonitorFoundationManager"
    )

    runtime_service_blueprint_owner = (
        "aura.runtime_service."
        "AuraRuntimeServiceFoundationManager"
    )

    local_service_foundation_owner = (
        "aura.local_service_runtime_foundation."
        "AuraLocalServiceRuntimeFoundationManager"
    )

    required_lifecycle_methods = (
        "allowed_transitions",
        "safety_boundary",
        "process_owner_status",
        "snapshot",
        "run_foreground",
        "request_stop",
        "self_test",
    )

    excluded_lifecycle_methods = (
        "_transition",
        "_acquire_ownership",
        "_release_ownership",
        "process_owner_status",
        "snapshot",
        "_record_failure",
        "_startup_rollback",
        "_install_main_thread_signal_handlers",
        "_restore_signal_handlers",
        "run_foreground",
        "request_stop",
        "_http_health",
        "_wait_for_state",
        "_port_closed",
        "_bind_port_blocker",
        "self_test",
    )

    lifecycle_states = (
        "stopped",
        "starting",
        "running",
        "stopping",
        "failed",
    )

    service_state_fields = (
        "service_name",
        "identity_version",
        "lifecycle_state",
        "boot_mode",
        "launch_mode",
        "safe_idle_required",
        "runtime_actions_locked",
        "health_state",
        "recovery_hint",
        "pid_file_status",
        "state_file_status",
        "systemd_unit_status",
        "last_transition_metadata",
        "persistence_runtime_enabled",
        "launcher_runtime_enabled",
    )

    excluded_runtime_payload_fields = (
        "process_id",
        "process_handle",
        "server_instance",
        "socket_handle",
        "thread_handle",
        "service_log_payload",
        "environment_payload",
        "command_result_payload",
    )

    persistence_artifacts = (
        "service_state_file_planned",
        "pid_file_planned",
        "launcher_log_file_planned",
        "systemd_user_unit_planned",
    )

    launcher_actions = (
        "status_planned",
        "start_planned",
        "stop_planned",
        "restart_planned",
        "logs_planned",
        "health_check_planned",
    )

    recovery_states = (
        "manual_recovery_only",
        "safe_idle_fallback",
        "operator_review_required",
        "automatic_restart_disabled",
    )

    safety_false_flags = (
        "service_state_written",
        "pid_file_written",
        "state_file_written",
        "systemd_unit_written",
        "systemd_unit_installed",
        "systemctl_called",
        "service_started",
        "service_stopped",
        "listener_started",
        "socket_opened",
        "thread_started",
        "subprocess_started",
        "launcher_executed",
        "browser_auto_launched",
        "auto_start_enabled",
        "background_daemon_started",
        "network_binding_performed",
        "runtime_activation_allowed",
        "release_gate_open",
        "autonomous_recovery_performed",
    )

    zero_counter_fields = (
        "service_state_writes",
        "pid_file_writes",
        "state_file_writes",
        "systemd_unit_writes",
        "systemd_unit_installs",
        "systemctl_calls",
        "services_started",
        "services_stopped",
        "listeners_started",
        "sockets_opened",
        "threads_started",
        "subprocesses_started",
        "launchers_executed",
        "browsers_auto_launched",
        "auto_start_enables",
        "background_daemons_started",
        "network_bindings",
        "autonomous_recoveries",
        "runtime_execution_features",
    )

    def __init__(
        self,
        project_root: Path | None = None,
    ) -> None:
        self.project_root = Path(
            project_root
            or Path.cwd()
        ).resolve()

    def _upstream_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            check = (
                MultiInterfaceStateSynchronizationAlphaManager(
                    project_root=self.project_root
                ).check()
            )
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    (
                        "aura.partner_runtime."
                        "MultiInterfaceStateSynchronizationAlphaManager"
                    ),
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "planning_ready": False,
                "runtime_ready": False,
                "current_sprint": None,
                "next_sprint": None,
                "next_boundary": None,
                "error":
                    (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
            }

        contract = check.get(
            "multi_interface_state_"
            "synchronization_contract",
            {},
        )

        return {
            "available": True,
            "owner":
                (
                    "aura.partner_runtime."
                    "MultiInterfaceStateSynchronizationAlphaManager"
                ),
            "assertion_count":
                check.get(
                    "assertion_count"
                ),
            "failed_assertion_count":
                check.get(
                    "failed_assertion_count"
                ),
            "planning_ready":
                check.get(
                    "planning_ready"
                ),
            "runtime_ready":
                check.get(
                    "runtime_ready"
                ),
            "current_sprint":
                contract.get(
                    "current_sprint"
                ),
            "next_sprint":
                contract.get(
                    "next_sprint"
                ),
            "next_boundary":
                contract.get(
                    "next_boundary"
                ),
            "browser_session_payloads_read":
                contract.get(
                    "browser_session_snapshot",
                    {},
                ).get(
                    "session_payloads_read"
                ),
            "control_center_snapshot_invoked":
                contract.get(
                    "control_center_snapshot_invoked"
                ),
            "contract_ready":
                contract.get(
                    "multi_interface_state_"
                    "synchronization_contract_ready"
                ),
            "error": None,
        }

    def _lifecycle_static_snapshot(
        self,
    ) -> dict[str, Any]:
        owner = (
            AuraServiceLifecycleRuntimeManager
        )

        declared_methods = sorted(
            name
            for name, value
            in vars(owner).items()
            if (
                callable(value)
                or isinstance(
                    value,
                    (
                        classmethod,
                        staticmethod,
                        property,
                    ),
                )
            )
        )

        states = [
            item.value
            for item in LifecycleState
        ]

        required_present = all(
            method in declared_methods
            for method
            in self.required_lifecycle_methods
        )

        excluded_present = all(
            method in declared_methods
            for method
            in self.excluded_lifecycle_methods
        )

        metadata = {
            "name":
                getattr(
                    owner,
                    "name",
                    None,
                ),
            "sprint":
                getattr(
                    owner,
                    "sprint",
                    None,
                ),
            "component_version":
                getattr(
                    owner,
                    "component_version",
                    None,
                ),
        }

        contract_ready = all(
            (
                states
                == list(
                    self.lifecycle_states
                ),
                required_present,
                excluded_present,
                metadata["name"]
                == "aura_service_lifecycle_runtime",
                metadata["sprint"] == 182,
                metadata["component_version"]
                == "0.1.0-alpha",
            )
        )

        return {
            "available": True,
            "owner":
                self.canonical_lifecycle_owner,
            "access_mode":
                self.canonical_lifecycle_access_mode,
            "constructor_signature":
                str(
                    inspect.signature(
                        owner
                    )
                ),
            "class_metadata":
                metadata,
            "lifecycle_states":
                states,
            "declared_methods":
                declared_methods,
            "required_methods":
                list(
                    self.required_lifecycle_methods
                ),
            "required_methods_present":
                required_present,
            "excluded_methods":
                list(
                    self.excluded_lifecycle_methods
                ),
            "excluded_methods_present":
                excluded_present,
            "instance_created": False,
            "method_invocation_allowed":
                False,
            "runtime_methods_invoked": [],
            "listener_started": False,
            "socket_opened": False,
            "thread_started": False,
            "foreground_start_performed":
                False,
            "stop_request_performed":
                False,
            "self_test_invoked": False,
            "contract_ready":
                contract_ready,
        }

    def _launcher_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            manager = (
                AuraLauncherHealthMonitorFoundationManager(
                    project_root=self.project_root
                )
            )

            status = manager.status()
            context = manager.context()
            safety = manager.safety_boundary()
            summary = manager.launcher_summary()

            modes = manager.launcher_modes()
            actions = manager.launcher_actions()
            health_states = (
                manager.health_states()
            )
            monitor_fields = (
                manager.monitor_fields()
            )
            identity = (
                context.get(
                    "launcher_identity",
                    {},
                )
            )

            ready = all(
                (
                    status.get(
                        "planner_ready"
                    )
                    is True,
                    status.get(
                        "runtime_ready"
                    )
                    is False,
                    safety.get(
                        "launcher_runtime"
                    )
                    is False,
                    safety.get(
                        "process_start"
                    )
                    is False,
                    safety.get(
                        "process_stop"
                    )
                    is False,
                    safety.get(
                        "process_restart"
                    )
                    is False,
                    safety.get(
                        "systemctl_execution"
                    )
                    is False,
                    safety.get(
                        "auto_boot_runtime"
                    )
                    is False,
                    safety.get(
                        "port_binding"
                    )
                    is False,
                    summary.get(
                        "runtime_execution_features"
                    )
                    == 0,
                    summary.get(
                        "processes_started"
                    )
                    == 0,
                    summary.get(
                        "processes_stopped"
                    )
                    == 0,
                    summary.get(
                        "processes_restarted"
                    )
                    == 0,
                    summary.get(
                        "systemctl_commands_executed"
                    )
                    == 0,
                )
            )

            return {
                "available": True,
                "owner":
                    self.launcher_foundation_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "metadata_owner"
                    ),
                "name":
                    status.get(
                        "name"
                    ),
                "version":
                    status.get(
                        "version"
                    ),
                "identity_version":
                    identity.get(
                        "identity_version"
                    ),
                "launcher_modes":
                    modes,
                "launcher_actions":
                    actions,
                "health_states":
                    health_states,
                "monitor_fields":
                    monitor_fields,
                "summary":
                    summary,
                "runtime_ready":
                    status.get(
                        "runtime_ready"
                    ),
                "safety_boundary":
                    safety,
                "contract_ready":
                    ready,
                "error": None,
            }

        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.launcher_foundation_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "metadata_owner"
                    ),
                "name": None,
                "version": None,
                "identity_version": None,
                "launcher_modes": [],
                "launcher_actions": [],
                "health_states": [],
                "monitor_fields": [],
                "summary": {},
                "runtime_ready": False,
                "safety_boundary": {},
                "contract_ready": False,
                "error":
                    (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
            }

    def _runtime_service_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            manager = (
                AuraRuntimeServiceFoundationManager(
                    project_root=self.project_root
                )
            )

            status = manager.status()
            context = manager.context()
            safety = manager.safety_boundary()
            summary = manager.service_summary()

            plan_types = (
                manager.service_plan_types()
            )
            boot_modes = (
                manager.boot_modes()
            )
            lifecycle_states = (
                manager.lifecycle_states()
            )
            health_fields = (
                manager.health_check_fields()
            )
            identity = context.get(
                "service_identity",
                {},
            )

            ready = all(
                (
                    status.get(
                        "planner_ready"
                    )
                    is True,
                    status.get(
                        "runtime_ready"
                    )
                    is False,
                    safety.get(
                        "service_runtime"
                    )
                    is False,
                    safety.get(
                        "systemd_unit_creation"
                    )
                    is False,
                    safety.get(
                        "systemd_enable"
                    )
                    is False,
                    safety.get(
                        "systemd_start"
                    )
                    is False,
                    safety.get(
                        "background_process_start"
                    )
                    is False,
                    safety.get(
                        "auto_boot_runtime"
                    )
                    is False,
                    safety.get(
                        "port_binding"
                    )
                    is False,
                    summary.get(
                        "runtime_execution_features"
                    )
                    == 0,
                    summary.get(
                        "runtime_enabled_services"
                    )
                    == 0,
                    summary.get(
                        "systemd_units_created"
                    )
                    == 0,
                    summary.get(
                        "background_processes_started"
                    )
                    == 0,
                    summary.get(
                        "auto_boot_runtime_enabled"
                    )
                    == 0,
                )
            )

            return {
                "available": True,
                "owner":
                    self.runtime_service_blueprint_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "blueprint_reference"
                    ),
                "name":
                    status.get(
                        "name"
                    ),
                "version":
                    status.get(
                        "version"
                    ),
                "identity_version":
                    identity.get(
                        "identity_version"
                    ),
                "service_plan_types":
                    plan_types,
                "boot_modes":
                    boot_modes,
                "lifecycle_states":
                    lifecycle_states,
                "health_check_fields":
                    health_fields,
                "summary":
                    summary,
                "runtime_ready":
                    status.get(
                        "runtime_ready"
                    ),
                "safety_boundary":
                    safety,
                "contract_ready":
                    ready,
                "error": None,
            }

        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.runtime_service_blueprint_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "blueprint_reference"
                    ),
                "name": None,
                "version": None,
                "identity_version": None,
                "service_plan_types": [],
                "boot_modes": [],
                "lifecycle_states": [],
                "health_check_fields": [],
                "summary": {},
                "runtime_ready": False,
                "safety_boundary": {},
                "contract_ready": False,
                "error":
                    (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
            }

    def _local_service_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            manager = (
                AuraLocalServiceRuntimeFoundationManager(
                    project_root=self.project_root
                )
            )

            status = manager.status()
            context = manager.context()
            safety = manager.safety_boundary()
            summary = manager.summary()

            ready = all(
                (
                    status.get(
                        "local_service_runtime_"
                        "foundation_ready"
                    )
                    is True,
                    status.get(
                        "runtime_execution_features"
                    )
                    == 0,
                    safety.get(
                        "local_service_runtime"
                    )
                    is False,
                    safety.get(
                        "runtime_service_process_start"
                    )
                    is False,
                    safety.get(
                        "runtime_service_process_stop"
                    )
                    is False,
                    safety.get(
                        "runtime_service_process_restart"
                    )
                    is False,
                    safety.get(
                        "runtime_socket_open"
                    )
                    is False,
                    safety.get(
                        "runtime_port_binding"
                    )
                    is False,
                    safety.get(
                        "runtime_background_worker_start"
                    )
                    is False,
                    safety.get(
                        "runtime_systemd_unit_create"
                    )
                    is False,
                    safety.get(
                        "runtime_systemd_unit_enable"
                    )
                    is False,
                    safety.get(
                        "release_gate_closed"
                    )
                    is True,
                    summary.get(
                        "runtime_execution_features"
                    )
                    == 0,
                    summary.get(
                        "runtime_services_started"
                    )
                    == 0,
                    summary.get(
                        "runtime_services_stopped"
                    )
                    == 0,
                    summary.get(
                        "runtime_services_restarted"
                    )
                    == 0,
                )
            )

            return {
                "available": True,
                "owner":
                    self.local_service_foundation_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "safety_baseline"
                    ),
                "name":
                    status.get(
                        "name"
                    ),
                "version":
                    status.get(
                        "version"
                    ),
                "summary":
                    summary,
                "runtime_ready":
                    False,
                "safety_boundary":
                    safety,
                "context_metadata_only":
                    context.get(
                        "metadata_only"
                    ),
                "contract_ready":
                    ready,
                "error": None,
            }

        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.local_service_foundation_owner,
                "role":
                    (
                        "secondary_read_only_"
                        "safety_baseline"
                    ),
                "name": None,
                "version": None,
                "summary": {},
                "runtime_ready": False,
                "safety_boundary": {},
                "context_metadata_only":
                    False,
                "contract_ready": False,
                "error":
                    (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
            }

    def service_state_schema(
        self,
    ) -> dict[str, Any]:
        fields = list(
            self.service_state_fields
        )

        excluded = list(
            self.excluded_runtime_payload_fields
        )

        defaults = {
            "service_name":
                "aura.service",
            "identity_version":
                "0.231.0-genesis",
            "lifecycle_state":
                "stopped",
            "boot_mode":
                "safe_idle",
            "launch_mode":
                "manual_only",
            "safe_idle_required":
                True,
            "runtime_actions_locked":
                True,
            "health_state":
                "unknown_planned",
            "recovery_hint":
                "manual_recovery_only",
            "pid_file_status":
                "not_written",
            "state_file_status":
                "not_written",
            "systemd_unit_status":
                "not_written",
            "last_transition_metadata":
                None,
            "persistence_runtime_enabled":
                False,
            "launcher_runtime_enabled":
                False,
        }

        ready = all(
            (
                list(
                    defaults.keys()
                )
                == fields,
                set(fields).isdisjoint(
                    set(excluded)
                ),
                defaults[
                    "identity_version"
                ]
                == "0.231.0-genesis",
                defaults[
                    "lifecycle_state"
                ]
                == "stopped",
                defaults[
                    "boot_mode"
                ]
                == "safe_idle",
                defaults[
                    "launch_mode"
                ]
                == "manual_only",
                defaults[
                    "safe_idle_required"
                ]
                is True,
                defaults[
                    "runtime_actions_locked"
                ]
                is True,
                defaults[
                    "persistence_runtime_enabled"
                ]
                is False,
                defaults[
                    "launcher_runtime_enabled"
                ]
                is False,
            )
        )

        return {
            "fields":
                fields,
            "field_count":
                len(fields),
            "excluded_runtime_payload_fields":
                excluded,
            "excluded_field_count":
                len(excluded),
            "defaults":
                defaults,
            "payload_free":
                True,
            "schema_only":
                True,
            "state_created":
                False,
            "state_loaded":
                False,
            "state_written":
                False,
            "ready":
                ready,
        }

    def persistence_schema(
        self,
    ) -> dict[str, Any]:
        artifacts = {
            "service_state_file_planned": {
                "artifact_role":
                    "service_state_metadata",
                "write_allowed":
                    False,
                "read_allowed":
                    False,
                "created":
                    False,
            },
            "pid_file_planned": {
                "artifact_role":
                    "process_identity_metadata",
                "write_allowed":
                    False,
                "read_allowed":
                    False,
                "created":
                    False,
            },
            "launcher_log_file_planned": {
                "artifact_role":
                    "launcher_visibility_metadata",
                "write_allowed":
                    False,
                "read_allowed":
                    False,
                "created":
                    False,
            },
            "systemd_user_unit_planned": {
                "artifact_role":
                    "future_service_unit_metadata",
                "write_allowed":
                    False,
                "read_allowed":
                    False,
                "created":
                    False,
            },
        }

        ready = all(
            (
                list(
                    artifacts.keys()
                )
                == list(
                    self.persistence_artifacts
                ),
                all(
                    packet[
                        "write_allowed"
                    ]
                    is False
                    for packet
                    in artifacts.values()
                ),
                all(
                    packet[
                        "read_allowed"
                    ]
                    is False
                    for packet
                    in artifacts.values()
                ),
                all(
                    packet[
                        "created"
                    ]
                    is False
                    for packet
                    in artifacts.values()
                ),
            )
        )

        return {
            "scope":
                (
                    "declarative_persistence_"
                    "artifact_schema_only"
                ),
            "artifacts":
                artifacts,
            "artifact_count":
                len(artifacts),
            "atomic_write_policy_declared":
                True,
            "ownership_policy_declared":
                True,
            "permission_policy_declared":
                True,
            "recovery_metadata_declared":
                True,
            "filesystem_access_performed":
                False,
            "ready":
                ready,
        }

    def launcher_policy(
        self,
    ) -> dict[str, Any]:
        actions = list(
            self.launcher_actions
        )

        return {
            "actions":
                actions,
            "action_count":
                len(actions),
            "default_mode":
                "safe_idle",
            "operator_start_required":
                True,
            "manual_confirmation_required":
                True,
            "status_surface":
                "metadata_only",
            "start_execution_allowed":
                False,
            "stop_execution_allowed":
                False,
            "restart_execution_allowed":
                False,
            "log_read_allowed":
                False,
            "health_probe_allowed":
                False,
            "browser_auto_launch_allowed":
                False,
            "process_spawn_allowed":
                False,
            "systemctl_allowed":
                False,
            "auto_start_allowed":
                False,
            "runtime_ready":
                False,
            "ready":
                (
                    actions
                    == list(
                        self.launcher_actions
                    )
                ),
        }

    def recovery_policy(
        self,
    ) -> dict[str, Any]:
        states = list(
            self.recovery_states
        )

        return {
            "states":
                states,
            "state_count":
                len(states),
            "default_recovery":
                "manual_recovery_only",
            "safe_idle_fallback":
                True,
            "operator_review_required":
                True,
            "automatic_restart_allowed":
                False,
            "automatic_rollback_allowed":
                False,
            "autonomous_recovery_allowed":
                False,
            "state_file_recovery_allowed":
                False,
            "pid_file_recovery_allowed":
                False,
            "runtime_ready":
                False,
            "ready":
                (
                    states
                    == list(
                        self.recovery_states
                    )
                ),
        }

    def safety_boundary(
        self,
    ) -> dict[str, bool]:
        return {
            name: False
            for name
            in self.safety_false_flags
        }

    def zero_counters(
        self,
    ) -> dict[str, int]:
        return {
            name: 0
            for name
            in self.zero_counter_fields
        }

    def service_persistence_and_launcher_contract(
        self,
    ) -> dict[str, Any]:
        upstream = (
            self._upstream_snapshot()
        )

        lifecycle = (
            self._lifecycle_static_snapshot()
        )

        launcher = (
            self._launcher_snapshot()
        )

        runtime_service = (
            self._runtime_service_snapshot()
        )

        local_service = (
            self._local_service_snapshot()
        )

        state_schema = (
            self.service_state_schema()
        )

        persistence = (
            self.persistence_schema()
        )

        launcher_policy = (
            self.launcher_policy()
        )

        recovery = (
            self.recovery_policy()
        )

        safety = (
            self.safety_boundary()
        )

        counters = (
            self.zero_counters()
        )

        contract_ready = all(
            (
                upstream.get(
                    "available"
                )
                is True,
                upstream.get(
                    "assertion_count"
                )
                == 128,
                upstream.get(
                    "failed_assertion_count"
                )
                == 0,
                upstream.get(
                    "planning_ready"
                )
                is True,
                upstream.get(
                    "runtime_ready"
                )
                is False,
                upstream.get(
                    "next_sprint"
                )
                == 227,
                upstream.get(
                    "next_boundary"
                )
                == "service_persistence_and_launcher",
                lifecycle.get(
                    "contract_ready"
                )
                is True,
                launcher.get(
                    "contract_ready"
                )
                is True,
                runtime_service.get(
                    "contract_ready"
                )
                is True,
                local_service.get(
                    "contract_ready"
                )
                is True,
                state_schema.get(
                    "ready"
                )
                is True,
                persistence.get(
                    "ready"
                )
                is True,
                launcher_policy.get(
                    "ready"
                )
                is True,
                recovery.get(
                    "ready"
                )
                is True,
                all(
                    value is False
                    for value
                    in safety.values()
                ),
                all(
                    value == 0
                    for value
                    in counters.values()
                ),
            )
        )

        return {
            "name":
                self.name,
            "version":
                self.version,
            "current_sprint":
                227,
            "next_sprint":
                228,
            "boundary":
                "service_persistence_and_launcher",
            "next_boundary":
                "safe_auto_start_evaluation",
            "block":
                (
                    "Sprint 221-230 Unified "
                    "Partner Runtime Integration"
                ),
            "contract_only":
                True,
            "metadata_only":
                True,
            "scope":
                (
                    "contract_only_service_"
                    "persistence_launcher_metadata"
                ),
            "upstream_snapshot":
                upstream,
            "canonical_lifecycle_snapshot":
                lifecycle,
            "launcher_foundation_snapshot":
                launcher,
            "runtime_service_blueprint_snapshot":
                runtime_service,
            "local_service_foundation_snapshot":
                local_service,
            "service_state_schema":
                state_schema,
            "persistence_schema":
                persistence,
            "launcher_policy":
                launcher_policy,
            "recovery_policy":
                recovery,
            "safety_boundary":
                safety,
            "zero_counters":
                counters,
            "service_state_schema_declared":
                True,
            "launcher_contract_declared":
                True,
            "persistence_schema_declared":
                True,
            "recovery_metadata_declared":
                True,
            "runtime_ready":
                False,
            "release_gate_open":
                False,
            "service_persistence_and_"
            "launcher_contract_ready":
                contract_ready,
        }

    def status(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.service_persistence_and_launcher_contract()
        )

        state_schema = contract[
            "service_state_schema"
        ]

        persistence = contract[
            "persistence_schema"
        ]

        launcher_policy = contract[
            "launcher_policy"
        ]

        return {
            "name":
                self.name,
            "version":
                self.version,
            "current_sprint": 227,
            "next_sprint": 228,
            "boundary":
                "service_persistence_and_launcher",
            "next_boundary":
                "safe_auto_start_evaluation",
            "contract_only": True,
            "metadata_only": True,
            "canonical_lifecycle_owner":
                self.canonical_lifecycle_owner,
            "canonical_lifecycle_access_mode":
                self.canonical_lifecycle_access_mode,
            "service_state_field_count":
                state_schema[
                    "field_count"
                ],
            "excluded_payload_field_count":
                state_schema[
                    "excluded_field_count"
                ],
            "persistence_artifact_count":
                persistence[
                    "artifact_count"
                ],
            "launcher_action_count":
                launcher_policy[
                    "action_count"
                ],
            "planning_ready":
                contract[
                    "service_persistence_and_"
                    "launcher_contract_ready"
                ],
            "alpha_ready":
                contract[
                    "service_persistence_and_"
                    "launcher_contract_ready"
                ],
            "runtime_ready": False,
            "release_gate_open": False,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.service_persistence_and_launcher_contract()
        )

        lifecycle = contract[
            "canonical_lifecycle_snapshot"
        ]

        return {
            "name":
                self.name,
            "current_sprint": 227,
            "next_sprint": 228,
            "boundary":
                "service_persistence_and_launcher",
            "scope":
                contract[
                    "scope"
                ],
            "canonical_lifecycle_owner":
                lifecycle[
                    "owner"
                ],
            "canonical_lifecycle_access_mode":
                lifecycle[
                    "access_mode"
                ],
            "lifecycle_instance_created":
                lifecycle[
                    "instance_created"
                ],
            "lifecycle_method_invocation_allowed":
                lifecycle[
                    "method_invocation_allowed"
                ],
            "launcher_role":
                contract[
                    "launcher_foundation_snapshot"
                ][
                    "role"
                ],
            "runtime_service_role":
                contract[
                    "runtime_service_blueprint_snapshot"
                ][
                    "role"
                ],
            "local_service_role":
                contract[
                    "local_service_foundation_snapshot"
                ][
                    "role"
                ],
            "service_state_schema_declared":
                contract[
                    "service_state_schema_declared"
                ],
            "persistence_schema_declared":
                contract[
                    "persistence_schema_declared"
                ],
            "launcher_contract_declared":
                contract[
                    "launcher_contract_declared"
                ],
            "recovery_metadata_declared":
                contract[
                    "recovery_metadata_declared"
                ],
            "runtime_ready": False,
            "release_gate_open": False,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.service_persistence_and_launcher_contract()
        )

        return {
            "name":
                self.name,
            "plan_type":
                (
                    "service_persistence_and_"
                    "launcher_contract_plan"
                ),
            "current_sprint": 227,
            "next_sprint": 228,
            "next_boundary":
                "safe_auto_start_evaluation",
            "contract":
                contract,
            "planning_ready":
                contract[
                    "service_persistence_and_"
                    "launcher_contract_ready"
                ],
            "runtime_ready": False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        contract = (
            self.service_persistence_and_launcher_contract()
        )

        upstream = contract[
            "upstream_snapshot"
        ]

        lifecycle = contract[
            "canonical_lifecycle_snapshot"
        ]

        launcher = contract[
            "launcher_foundation_snapshot"
        ]

        runtime_service = contract[
            "runtime_service_blueprint_snapshot"
        ]

        local_service = contract[
            "local_service_foundation_snapshot"
        ]

        state_schema = contract[
            "service_state_schema"
        ]

        persistence = contract[
            "persistence_schema"
        ]

        launcher_policy = contract[
            "launcher_policy"
        ]

        recovery = contract[
            "recovery_policy"
        ]

        safety = contract[
            "safety_boundary"
        ]

        counters = contract[
            "zero_counters"
        ]

        assertions: dict[str, bool] = {
            "project_root_available":
                self.project_root.is_dir(),

            "current_sprint_227":
                contract[
                    "current_sprint"
                ]
                == 227,

            "next_sprint_228":
                contract[
                    "next_sprint"
                ]
                == 228,

            "boundary_exact":
                contract[
                    "boundary"
                ]
                == "service_persistence_and_launcher",

            "next_boundary_safe_auto_start":
                contract[
                    "next_boundary"
                ]
                == "safe_auto_start_evaluation",

            "contract_only_true":
                contract[
                    "contract_only"
                ]
                is True,

            "metadata_only_true":
                contract[
                    "metadata_only"
                ]
                is True,

            "scope_exact":
                contract[
                    "scope"
                ]
                == (
                    "contract_only_service_"
                    "persistence_launcher_metadata"
                ),

            "runtime_ready_false":
                contract[
                    "runtime_ready"
                ]
                is False,

            "release_gate_closed":
                contract[
                    "release_gate_open"
                ]
                is False,

            "upstream_available":
                upstream[
                    "available"
                ]
                is True,

            "upstream_assertions_128":
                upstream[
                    "assertion_count"
                ]
                == 128,

            "upstream_failed_zero":
                upstream[
                    "failed_assertion_count"
                ]
                == 0,

            "upstream_planning_ready":
                upstream[
                    "planning_ready"
                ]
                is True,

            "upstream_runtime_closed":
                upstream[
                    "runtime_ready"
                ]
                is False,

            "upstream_current_sprint_226":
                upstream[
                    "current_sprint"
                ]
                == 226,

            "upstream_next_sprint_227":
                upstream[
                    "next_sprint"
                ]
                == 227,

            "upstream_next_boundary":
                upstream[
                    "next_boundary"
                ]
                == "service_persistence_and_launcher",

            "upstream_payload_reads_zero":
                upstream[
                    "browser_session_payloads_read"
                ]
                == 0,

            "upstream_control_snapshot_false":
                upstream[
                    "control_center_snapshot_invoked"
                ]
                is False,

            "upstream_contract_ready":
                upstream[
                    "contract_ready"
                ]
                is True,

            "lifecycle_available":
                lifecycle[
                    "available"
                ]
                is True,

            "lifecycle_owner_exact":
                lifecycle[
                    "owner"
                ]
                == self.canonical_lifecycle_owner,

            "lifecycle_access_mode_exact":
                lifecycle[
                    "access_mode"
                ]
                == self.canonical_lifecycle_access_mode,

            "lifecycle_states_exact":
                lifecycle[
                    "lifecycle_states"
                ]
                == list(
                    self.lifecycle_states
                ),

            "lifecycle_required_methods_present":
                lifecycle[
                    "required_methods_present"
                ]
                is True,

            "lifecycle_excluded_methods_present":
                lifecycle[
                    "excluded_methods_present"
                ]
                is True,

            "lifecycle_instance_not_created":
                lifecycle[
                    "instance_created"
                ]
                is False,

            "lifecycle_method_invocation_false":
                lifecycle[
                    "method_invocation_allowed"
                ]
                is False,

            "lifecycle_runtime_methods_empty":
                lifecycle[
                    "runtime_methods_invoked"
                ]
                == [],

            "lifecycle_listener_false":
                lifecycle[
                    "listener_started"
                ]
                is False,

            "lifecycle_socket_false":
                lifecycle[
                    "socket_opened"
                ]
                is False,

            "lifecycle_thread_false":
                lifecycle[
                    "thread_started"
                ]
                is False,

            "lifecycle_foreground_false":
                lifecycle[
                    "foreground_start_performed"
                ]
                is False,

            "lifecycle_stop_false":
                lifecycle[
                    "stop_request_performed"
                ]
                is False,

            "lifecycle_self_test_false":
                lifecycle[
                    "self_test_invoked"
                ]
                is False,

            "lifecycle_contract_ready":
                lifecycle[
                    "contract_ready"
                ]
                is True,

            "launcher_available":
                launcher[
                    "available"
                ]
                is True,

            "launcher_role_exact":
                launcher[
                    "role"
                ]
                == (
                    "secondary_read_only_"
                    "metadata_owner"
                ),

            "launcher_identity_version":
                launcher[
                    "identity_version"
                ]
                == "0.231.0-genesis",

            "launcher_runtime_closed":
                launcher[
                    "runtime_ready"
                ]
                is False,

            "launcher_contract_ready":
                launcher[
                    "contract_ready"
                ]
                is True,

            "runtime_service_available":
                runtime_service[
                    "available"
                ]
                is True,

            "runtime_service_role_exact":
                runtime_service[
                    "role"
                ]
                == (
                    "secondary_read_only_"
                    "blueprint_reference"
                ),

            "runtime_service_identity_version":
                runtime_service[
                    "identity_version"
                ]
                == "0.231.0-genesis",

            "runtime_service_closed":
                runtime_service[
                    "runtime_ready"
                ]
                is False,

            "runtime_service_contract_ready":
                runtime_service[
                    "contract_ready"
                ]
                is True,

            "local_service_available":
                local_service[
                    "available"
                ]
                is True,

            "local_service_role_exact":
                local_service[
                    "role"
                ]
                == (
                    "secondary_read_only_"
                    "safety_baseline"
                ),

            "local_service_metadata_only":
                local_service[
                    "context_metadata_only"
                ]
                is True,

            "local_service_runtime_closed":
                local_service[
                    "runtime_ready"
                ]
                is False,

            "local_service_contract_ready":
                local_service[
                    "contract_ready"
                ]
                is True,

            "state_fields_exact":
                state_schema[
                    "fields"
                ]
                == list(
                    self.service_state_fields
                ),

            "state_field_count_exact":
                state_schema[
                    "field_count"
                ]
                == len(
                    self.service_state_fields
                ),

            "excluded_fields_exact":
                state_schema[
                    "excluded_runtime_payload_fields"
                ]
                == list(
                    self.excluded_runtime_payload_fields
                ),

            "excluded_field_count_exact":
                state_schema[
                    "excluded_field_count"
                ]
                == len(
                    self.excluded_runtime_payload_fields
                ),

            "state_fields_disjoint":
                set(
                    state_schema[
                        "fields"
                    ]
                ).isdisjoint(
                    set(
                        state_schema[
                            "excluded_runtime_payload_fields"
                        ]
                    )
                ),

            "state_payload_free":
                state_schema[
                    "payload_free"
                ]
                is True,

            "state_schema_only":
                state_schema[
                    "schema_only"
                ]
                is True,

            "state_not_created":
                state_schema[
                    "state_created"
                ]
                is False,

            "state_not_loaded":
                state_schema[
                    "state_loaded"
                ]
                is False,

            "state_not_written":
                state_schema[
                    "state_written"
                ]
                is False,

            "state_schema_ready":
                state_schema[
                    "ready"
                ]
                is True,

            "persistence_artifacts_exact":
                list(
                    persistence[
                        "artifacts"
                    ].keys()
                )
                == list(
                    self.persistence_artifacts
                ),

            "persistence_artifact_count":
                persistence[
                    "artifact_count"
                ]
                == len(
                    self.persistence_artifacts
                ),

            "persistence_no_filesystem_access":
                persistence[
                    "filesystem_access_performed"
                ]
                is False,

            "persistence_ready":
                persistence[
                    "ready"
                ]
                is True,

            "launcher_actions_exact":
                launcher_policy[
                    "actions"
                ]
                == list(
                    self.launcher_actions
                ),

            "launcher_action_count":
                launcher_policy[
                    "action_count"
                ]
                == len(
                    self.launcher_actions
                ),

            "launcher_safe_idle":
                launcher_policy[
                    "default_mode"
                ]
                == "safe_idle",

            "launcher_operator_start":
                launcher_policy[
                    "operator_start_required"
                ]
                is True,

            "launcher_manual_confirmation":
                launcher_policy[
                    "manual_confirmation_required"
                ]
                is True,

            "launcher_runtime_closed":
                launcher_policy[
                    "runtime_ready"
                ]
                is False,

            "launcher_policy_ready":
                launcher_policy[
                    "ready"
                ]
                is True,

            "recovery_states_exact":
                recovery[
                    "states"
                ]
                == list(
                    self.recovery_states
                ),

            "recovery_default_manual":
                recovery[
                    "default_recovery"
                ]
                == "manual_recovery_only",

            "recovery_safe_idle":
                recovery[
                    "safe_idle_fallback"
                ]
                is True,

            "recovery_operator_review":
                recovery[
                    "operator_review_required"
                ]
                is True,

            "recovery_runtime_closed":
                recovery[
                    "runtime_ready"
                ]
                is False,

            "recovery_ready":
                recovery[
                    "ready"
                ]
                is True,

            "contract_ready":
                contract[
                    "service_persistence_and_"
                    "launcher_contract_ready"
                ]
                is True,
        }

        for method in (
            self.required_lifecycle_methods
        ):
            assertions[
                (
                    "lifecycle_required_method_"
                    + method
                )
            ] = (
                method
                in lifecycle[
                    "declared_methods"
                ]
            )

        for method in (
            self.excluded_lifecycle_methods
        ):
            assertions[
                (
                    "lifecycle_excluded_method_"
                    + method
                )
            ] = (
                method
                in lifecycle[
                    "declared_methods"
                ]
            )

        defaults = state_schema[
            "defaults"
        ]

        for field in (
            self.service_state_fields
        ):
            assertions[
                (
                    "state_default_present_"
                    + field
                )
            ] = field in defaults

        for field in (
            self.excluded_runtime_payload_fields
        ):
            assertions[
                (
                    "excluded_payload_absent_"
                    + field
                )
            ] = field not in defaults

        for name in (
            self.persistence_artifacts
        ):
            packet = persistence[
                "artifacts"
            ][name]

            assertions[
                (
                    "artifact_not_written_"
                    + name
                )
            ] = (
                packet[
                    "write_allowed"
                ]
                is False
            )

            assertions[
                (
                    "artifact_not_read_"
                    + name
                )
            ] = (
                packet[
                    "read_allowed"
                ]
                is False
            )

            assertions[
                (
                    "artifact_not_created_"
                    + name
                )
            ] = (
                packet[
                    "created"
                ]
                is False
            )

        for name in (
            self.safety_false_flags
        ):
            assertions[
                "safety_false_" + name
            ] = (
                safety[name]
                is False
            )

        for name in (
            self.zero_counter_fields
        ):
            assertions[
                "counter_zero_" + name
            ] = (
                counters[name]
                == 0
            )

        launcher_safety = launcher[
            "safety_boundary"
        ]

        for name in (
            "launcher_runtime",
            "process_start",
            "process_stop",
            "process_restart",
            "systemctl_execution",
            "auto_boot_runtime",
            "port_binding",
            "background_process_start",
        ):
            assertions[
                (
                    "launcher_owner_false_"
                    + name
                )
            ] = (
                launcher_safety.get(
                    name
                )
                is False
            )

        runtime_safety = runtime_service[
            "safety_boundary"
        ]

        for name in (
            "service_runtime",
            "systemd_unit_creation",
            "systemd_enable",
            "systemd_start",
            "systemd_stop",
            "systemd_restart",
            "background_process_start",
            "auto_boot_runtime",
            "port_binding",
            "launcher_runtime",
        ):
            assertions[
                (
                    "runtime_service_false_"
                    + name
                )
            ] = (
                runtime_safety.get(
                    name
                )
                is False
            )

        local_safety = local_service[
            "safety_boundary"
        ]

        for name in (
            "runtime_service_process_start",
            "runtime_service_process_stop",
            "runtime_service_process_restart",
            "runtime_socket_open",
            "runtime_port_binding",
            "runtime_background_worker_start",
            "runtime_systemd_unit_create",
            "runtime_systemd_unit_enable",
            "runtime_file_read",
            "runtime_file_write",
            "runtime_command_execution",
            "runtime_tool_execution",
        ):
            assertions[
                (
                    "local_service_false_"
                    + name
                )
            ] = (
                local_safety.get(
                    name
                )
                is False
            )

        assertions[
            "assertion_count_contract"
        ] = (
            self.expected_assertion_count
            in (
                0,
                len(assertions) + 1,
            )
        )

        failed = [
            name
            for name, passed
            in assertions.items()
            if passed is not True
        ]

        return {
            "name":
                self.name,
            "version":
                self.version,
            "current_sprint": 227,
            "next_sprint": 228,
            "next_boundary":
                "safe_auto_start_evaluation",
            "planning_ready":
                not failed,
            "alpha_ready":
                not failed,
            "runtime_ready":
                False,
            "assertion_count":
                len(assertions),
            "expected_assertion_count":
                self.expected_assertion_count,
            "failed_assertion_count":
                len(failed),
            "failed_assertions":
                failed,
            "assertions":
                assertions,
            "service_persistence_and_"
            "launcher_contract":
                contract,
        }
