"""Contract-only multi-interface state synchronization planning.

Sprint 226 composes deterministic metadata from the Sprint 225 personality
contract, canonical browser chat-session contract snapshot, chat-bridge state
schema, and stabilized local-interaction boundary.

No live state is propagated. No state store is created, read, or written.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from aura.browser_chat_session_runtime import (
    AuraBrowserChatSessionRuntimeManager,
)
from aura.chat_bridge.aura_chat_bridge_session_state_foundation_manager import (
    AuraChatBridgeSessionStateFoundationManager,
)
from aura.control_center_backend_runtime.aura_control_center_backend_runtime_manager import (
    AuraControlCenterBackendRuntimeManager,
)
from aura.local_interaction_runtime_stabilization.aura_local_interaction_runtime_stabilization_manager import (
    AuraLocalInteractionRuntimeStabilizationManager,
)

from .personality_consistency_runtime_alpha_manager import (
    PersonalityConsistencyRuntimeAlphaManager,
)


class MultiInterfaceStateSynchronizationPlanner:
    """Prepare the Sprint 226 metadata synchronization contract."""

    name = "multi_interface_state_synchronization"
    version = "0.1.0"

    current_sprint = 226
    next_sprint = 227
    next_boundary = "service_persistence_and_launcher"

    expected_assertion_count = 128

    upstream_owner = (
        "aura.partner_runtime."
        "personality_consistency_runtime_alpha_manager."
        "PersonalityConsistencyRuntimeAlphaManager"
    )

    canonical_session_owner = (
        "aura_browser_chat_session_runtime"
    )

    canonical_session_method = (
        "contract_snapshot"
    )

    interface_state_schema_owner = (
        "aura.chat_bridge."
        "aura_chat_bridge_session_state_foundation_manager."
        "AuraChatBridgeSessionStateFoundationManager"
    )

    local_interaction_owner = (
        "aura.local_interaction_runtime_stabilization."
        "aura_local_interaction_runtime_stabilization_manager."
        "AuraLocalInteractionRuntimeStabilizationManager"
    )

    control_center_reference = (
        "aura.control_center_backend_runtime."
        "aura_control_center_backend_runtime_manager."
        "AuraControlCenterBackendRuntimeManager"
    )

    interface_targets = (
        "browser_chat",
        "local_chat_cli",
        "control_center",
        "voice_metadata",
        "vision_metadata",
        "shell",
        "cli",
    )

    declared_state_fields = (
        "session_id_planned",
        "conversation_id_planned",
        "user_display_name",
        "aura_identity_version",
        "selected_channel",
        "safe_idle_mode",
        "permission_boundary_state",
        "last_user_message_metadata",
        "last_aura_response_metadata",
        "pending_action_request_metadata",
        "session_recovery_hint",
        "session_runtime_enabled",
    )

    declared_session_events = (
        "session_created_planned",
        "session_selected_planned",
        "message_received_planned",
        "response_rendered_planned",
        "permission_prompt_created_planned",
        "action_denied_planned",
        "session_recovery_requested_planned",
        "session_closed_planned",
    )

    canonical_sync_fields = (
        "aura_identity_version",
        "selected_channel",
        "safe_idle_mode",
        "permission_boundary_state",
        "session_recovery_hint",
        "session_runtime_enabled",
    )

    excluded_payload_adjacent_fields = (
        "session_id_planned",
        "conversation_id_planned",
        "user_display_name",
        "last_user_message_metadata",
        "last_aura_response_metadata",
        "pending_action_request_metadata",
    )

    allowed_browser_methods = (
        "contract_snapshot",
        "safety_boundary",
    )

    excluded_browser_methods = (
        "status",
        "load_session",
        "list_sessions",
        "create_session",
        "submit_message",
        "submit_local_model_message",
        "clear_session",
        "self_test",
    )

    canonical_state_defaults = {
        "aura_identity_version":
            "0.236.0-genesis",
        "selected_channel":
            "metadata_only",
        "safe_idle_mode":
            True,
        "permission_boundary_state":
            "default_deny",
        "session_recovery_hint":
            "manual_recovery_only",
        "session_runtime_enabled":
            False,
    }

    def __init__(
        self,
        project_root: str | Path | None = None,
        *,
        upstream_manager: (
            PersonalityConsistencyRuntimeAlphaManager
            | None
        ) = None,
        browser_manager: (
            AuraBrowserChatSessionRuntimeManager
            | None
        ) = None,
        schema_manager: (
            AuraChatBridgeSessionStateFoundationManager
            | None
        ) = None,
        local_interaction_manager: (
            AuraLocalInteractionRuntimeStabilizationManager
            | None
        ) = None,
    ) -> None:
        if project_root is None:
            project_root = (
                Path(__file__)
                .resolve()
                .parents[2]
            )

        self.project_root = (
            Path(project_root).resolve()
        )

        self.upstream_manager = (
            upstream_manager
            or PersonalityConsistencyRuntimeAlphaManager(
                project_root=self.project_root
            )
        )

        self.browser_manager = (
            browser_manager
            or AuraBrowserChatSessionRuntimeManager(
                project_root=self.project_root
            )
        )

        self.schema_manager = (
            schema_manager
            or AuraChatBridgeSessionStateFoundationManager(
                project_root=self.project_root
            )
        )

        self.local_interaction_manager = (
            local_interaction_manager
            or AuraLocalInteractionRuntimeStabilizationManager(
                project_root=self.project_root
            )
        )

    def _upstream_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            check = self.upstream_manager.check()
            context = self.upstream_manager.context()
        except Exception as exc:
            return {
                "available": False,
                "owner": self.upstream_owner,
                "assertion_count": 0,
                "failed_assertion_count": 1,
                "planning_ready": False,
                "runtime_ready": False,
                "current_sprint": None,
                "next_sprint": None,
                "next_boundary": None,
                "canonical_session_owner": None,
                "profile_ready": False,
                "profile_payload_free": False,
                "profile_deterministic": False,
                "interface_targets": [],
                "sync_deferred": False,
                "safety_closed": False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        profile = context.get(
            "personality_profile",
            {},
        )

        safety = context.get(
            "safety_boundary",
            {},
        )

        if not isinstance(profile, dict):
            profile = {}

        if not isinstance(safety, dict):
            safety = {}

        interface_targets = profile.get(
            "interface_targets",
            [],
        )

        if not isinstance(
            interface_targets,
            list,
        ):
            interface_targets = []

        safety_closed = (
            bool(safety)
            and all(
                value is False
                for value in safety.values()
            )
        )

        ready = all(
            (
                check.get(
                    "assertion_count"
                )
                == 96,
                check.get(
                    "failed_assertion_count"
                )
                == 0,
                check.get(
                    "planning_ready"
                )
                is True,
                check.get(
                    "runtime_ready"
                )
                is False,
                context.get(
                    "current_sprint"
                )
                == 225,
                context.get(
                    "next_sprint"
                )
                == 226,
                context.get(
                    "next_boundary"
                )
                == (
                    "multi_interface_"
                    "state_synchronization"
                ),
                context.get(
                    "canonical_session_owner"
                )
                == self.canonical_session_owner,
                profile.get("ready") is True,
                profile.get(
                    "payload_free"
                )
                is True,
                profile.get(
                    "deterministic"
                )
                is True,
                profile.get(
                    "multi_interface_state_"
                    "synchronization_deferred"
                )
                is True,
                interface_targets
                == list(
                    self.interface_targets
                ),
                safety_closed,
            )
        )

        return {
            "available": True,
            "owner": self.upstream_owner,
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
                context.get(
                    "current_sprint"
                ),
            "next_sprint":
                context.get(
                    "next_sprint"
                ),
            "next_boundary":
                context.get(
                    "next_boundary"
                ),
            "canonical_session_owner":
                context.get(
                    "canonical_session_owner"
                ),
            "profile_ready":
                profile.get("ready"),
            "profile_payload_free":
                profile.get(
                    "payload_free"
                ),
            "profile_deterministic":
                profile.get(
                    "deterministic"
                ),
            "interface_targets":
                interface_targets,
            "sync_deferred":
                profile.get(
                    "multi_interface_state_"
                    "synchronization_deferred"
                ),
            "safety_closed":
                safety_closed,
            "contract_ready":
                ready,
            "error": None,
        }

    def _browser_session_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            contract = (
                self.browser_manager
                .contract_snapshot()
            )

            boundary = (
                self.browser_manager
                .safety_boundary()
            )
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.canonical_session_owner,
                "method":
                    self.canonical_session_method,
                "name": None,
                "metadata_only": False,
                "inspection_read_only": False,
                "session_payloads_read": None,
                "session_metrics_inspected": None,
                "session_metrics_available": None,
                "error_count": 1,
                "degraded": True,
                "safe_idle": False,
                "command_execution": True,
                "tool_execution": True,
                "autonomous_action": True,
                "status_method_invoked": False,
                "payload_method_invoked": False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        ready = all(
            (
                contract.get("name")
                == self.canonical_session_owner,
                contract.get(
                    "metadata_only"
                )
                is True,
                contract.get(
                    "inspection_read_only"
                )
                is True,
                contract.get(
                    "session_payloads_read"
                )
                == 0,
                contract.get(
                    "session_metrics_inspected"
                )
                is False,
                contract.get(
                    "session_metrics_available"
                )
                is False,
                contract.get(
                    "error_count"
                )
                == 0,
                contract.get(
                    "degraded"
                )
                is False,
                boundary.get(
                    "safe_idle"
                )
                is True,
                boundary.get(
                    "command_execution"
                )
                is False,
                boundary.get(
                    "tool_execution"
                )
                is False,
                boundary.get(
                    "autonomous_action"
                )
                is False,
            )
        )

        return {
            "available": True,
            "owner":
                self.canonical_session_owner,
            "method":
                self.canonical_session_method,
            "name":
                contract.get("name"),
            "metadata_only":
                contract.get(
                    "metadata_only"
                ),
            "inspection_read_only":
                contract.get(
                    "inspection_read_only"
                ),
            "session_payloads_read":
                contract.get(
                    "session_payloads_read"
                ),
            "session_metrics_inspected":
                contract.get(
                    "session_metrics_inspected"
                ),
            "session_metrics_available":
                contract.get(
                    "session_metrics_available"
                ),
            "error_count":
                contract.get(
                    "error_count"
                ),
            "degraded":
                contract.get(
                    "degraded"
                ),
            "storage_exists":
                contract.get(
                    "storage_exists"
                ),
            "storage_is_directory":
                contract.get(
                    "storage_is_directory"
                ),
            "storage_is_symlink":
                contract.get(
                    "storage_is_symlink"
                ),
            "safe_idle":
                boundary.get(
                    "safe_idle"
                ),
            "command_execution":
                boundary.get(
                    "command_execution"
                ),
            "tool_execution":
                boundary.get(
                    "tool_execution"
                ),
            "autonomous_action":
                boundary.get(
                    "autonomous_action"
                ),
            "status_method_invoked":
                False,
            "payload_method_invoked":
                False,
            "contract_ready":
                ready,
            "error": None,
        }

    def _schema_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            state_fields = (
                self.schema_manager
                .session_state_fields()
            )

            session_events = (
                self.schema_manager
                .session_events()
            )

            identity = (
                self.schema_manager
                .chat_bridge_identity()
            )

            status = (
                self.schema_manager.status()
            )

            context = (
                self.schema_manager.context()
            )
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.interface_state_schema_owner,
                "name": None,
                "state_fields": [],
                "session_events": [],
                "identity_version": None,
                "runtime_mode": None,
                "auto_action_allowed": True,
                "bridge_ready": False,
                "state_foundation_ready": False,
                "planner_ready": False,
                "runtime_ready": True,
                "runtime_execution_features": 1,
                "metadata_only": False,
                "session_runtime": True,
                "session_persistence_runtime": True,
                "network_action": True,
                "command_execution": True,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        ready = all(
            (
                state_fields
                == list(
                    self.declared_state_fields
                ),
                session_events
                == list(
                    self.declared_session_events
                ),
                identity.get(
                    "identity_version"
                )
                == "0.236.0-genesis",
                identity.get(
                    "runtime_mode"
                )
                == "blueprint_only",
                identity.get(
                    "auto_action_allowed"
                )
                is False,
                status.get(
                    "chat_bridge_foundation_ready"
                )
                is True,
                status.get(
                    "session_state_foundation_ready"
                )
                is True,
                status.get(
                    "planner_ready"
                )
                is True,
                status.get(
                    "runtime_ready"
                )
                is False,
                status.get(
                    "runtime_execution_features"
                )
                == 0,
                context.get(
                    "metadata_only"
                )
                is True,
                context.get(
                    "session_runtime"
                )
                is False,
                context.get(
                    "session_persistence_runtime"
                )
                is False,
                context.get(
                    "network_action"
                )
                is False,
                context.get(
                    "command_execution"
                )
                is False,
            )
        )

        return {
            "available": True,
            "owner":
                self.interface_state_schema_owner,
            "name":
                status.get("name"),
            "state_fields":
                state_fields,
            "session_events":
                session_events,
            "identity_version":
                identity.get(
                    "identity_version"
                ),
            "runtime_mode":
                identity.get(
                    "runtime_mode"
                ),
            "auto_action_allowed":
                identity.get(
                    "auto_action_allowed"
                ),
            "bridge_ready":
                status.get(
                    "chat_bridge_foundation_ready"
                ),
            "state_foundation_ready":
                status.get(
                    "session_state_foundation_ready"
                ),
            "planner_ready":
                status.get(
                    "planner_ready"
                ),
            "runtime_ready":
                status.get(
                    "runtime_ready"
                ),
            "runtime_execution_features":
                status.get(
                    "runtime_execution_features"
                ),
            "metadata_only":
                context.get(
                    "metadata_only"
                ),
            "session_runtime":
                context.get(
                    "session_runtime"
                ),
            "session_persistence_runtime":
                context.get(
                    "session_persistence_runtime"
                ),
            "network_action":
                context.get(
                    "network_action"
                ),
            "command_execution":
                context.get(
                    "command_execution"
                ),
            "contract_ready":
                ready,
            "error": None,
        }

    def _local_interaction_snapshot(
        self,
    ) -> dict[str, Any]:
        try:
            status = (
                self.local_interaction_manager
                .status()
            )

            context = (
                self.local_interaction_manager
                .context()
            )
        except Exception as exc:
            return {
                "available": False,
                "owner":
                    self.local_interaction_owner,
                "name": None,
                "version": None,
                "ready": False,
                "components_present": 0,
                "components_expected": 0,
                "main_cli_present": False,
                "runtime_mutation_performed": True,
                "listener_started": True,
                "subprocess_started": True,
                "release_gate_closed": False,
                "contract_ready": False,
                "error": (
                    f"{type(exc).__name__}: {exc}"
                ),
            }

        ready = all(
            (
                status.get("module")
                == (
                    "local_interaction_"
                    "runtime_stabilization"
                ),
                status.get("version")
                == "0.190.0-genesis",
                status.get(
                    "local_interaction_runtime_"
                    "stabilization_ready"
                )
                is True,
                status.get(
                    "components_present"
                )
                == 9,
                status.get(
                    "components_expected"
                )
                == 9,
                status.get(
                    "main_cli_present"
                )
                is True,
                status.get(
                    "runtime_mutation_performed"
                )
                is False,
                status.get(
                    "listener_started_by_status"
                )
                is False,
                status.get(
                    "subprocess_started_by_status"
                )
                is False,
                status.get(
                    "release_gate_closed"
                )
                is True,
                context.get("block")
                == (
                    "181-190_local_interaction_"
                    "runtime_activation"
                ),
            )
        )

        return {
            "available": True,
            "owner":
                self.local_interaction_owner,
            "name":
                status.get("module"),
            "version":
                status.get("version"),
            "ready":
                status.get(
                    "local_interaction_runtime_"
                    "stabilization_ready"
                ),
            "components_present":
                status.get(
                    "components_present"
                ),
            "components_expected":
                status.get(
                    "components_expected"
                ),
            "main_cli_present":
                status.get(
                    "main_cli_present"
                ),
            "runtime_mutation_performed":
                status.get(
                    "runtime_mutation_performed"
                ),
            "listener_started":
                status.get(
                    "listener_started_by_status"
                ),
            "subprocess_started":
                status.get(
                    "subprocess_started_by_status"
                ),
            "release_gate_closed":
                status.get(
                    "release_gate_closed"
                ),
            "contract_ready":
                ready,
            "error": None,
        }

    def _control_center_reference_snapshot(
        self,
    ) -> dict[str, Any]:
        routes = list(
            AuraControlCenterBackendRuntimeManager
            .ROUTES
        )

        panel_ids = list(
            AuraControlCenterBackendRuntimeManager
            .PANEL_IDS
        )

        ready = all(
            (
                AuraControlCenterBackendRuntimeManager
                .name
                == (
                    "aura_control_center_"
                    "backend_runtime"
                ),
                AuraControlCenterBackendRuntimeManager
                .sprint
                == 184,
                AuraControlCenterBackendRuntimeManager
                .schema_version
                == "1.0",
                len(routes) == 9,
                len(panel_ids) == 8,
            )
        )

        return {
            "available": True,
            "owner":
                self.control_center_reference,
            "name":
                AuraControlCenterBackendRuntimeManager
                .name,
            "sprint":
                AuraControlCenterBackendRuntimeManager
                .sprint,
            "schema_version":
                AuraControlCenterBackendRuntimeManager
                .schema_version,
            "role":
                "static_reference_only",
            "snapshot_invoked":
                False,
            "snapshot_invocation_allowed":
                False,
            "routes":
                routes,
            "panel_ids":
                panel_ids,
            "contract_ready":
                ready,
        }

    def _state_vector_policy(
        self,
        upstream: dict[str, Any],
        schema: dict[str, Any],
    ) -> dict[str, Any]:
        interface_targets = list(
            upstream.get(
                "interface_targets",
                [],
            )
        )

        state_fields = list(
            schema.get(
                "state_fields",
                [],
            )
        )

        session_events = list(
            schema.get(
                "session_events",
                [],
            )
        )

        defaults = dict(
            self.canonical_state_defaults
        )

        matrix = {
            target: {
                "target": target,
                "synchronization_mode":
                    "metadata_contract_only",
                "canonical_sync_fields":
                    list(
                        self.canonical_sync_fields
                    ),
                "state_vector_template":
                    dict(defaults),
                "live_propagation_performed":
                    False,
                "state_store_created":
                    False,
                "event_dispatched":
                    False,
            }
            for target in interface_targets
        }

        canonical_set = set(
            self.canonical_sync_fields
        )

        excluded_set = set(
            self.excluded_payload_adjacent_fields
        )

        state_field_set = set(
            state_fields
        )

        ready = all(
            (
                interface_targets
                == list(
                    self.interface_targets
                ),
                state_fields
                == list(
                    self.declared_state_fields
                ),
                session_events
                == list(
                    self.declared_session_events
                ),
                canonical_set.issubset(
                    state_field_set
                ),
                excluded_set.issubset(
                    state_field_set
                ),
                canonical_set.isdisjoint(
                    excluded_set
                ),
                len(matrix)
                == len(
                    self.interface_targets
                ),
                defaults.get(
                    "aura_identity_version"
                )
                == "0.236.0-genesis",
                defaults.get(
                    "selected_channel"
                )
                == "metadata_only",
                defaults.get(
                    "safe_idle_mode"
                )
                is True,
                defaults.get(
                    "permission_boundary_state"
                )
                == "default_deny",
                defaults.get(
                    "session_recovery_hint"
                )
                == "manual_recovery_only",
                defaults.get(
                    "session_runtime_enabled"
                )
                is False,
            )
        )

        return {
            "name":
                "multi_interface_state_vector_policy",
            "scope":
                "deterministic_metadata_"
                "state_vector_only",
            "interface_targets":
                interface_targets,
            "declared_state_fields":
                state_fields,
            "declared_session_events":
                session_events,
            "canonical_sync_fields":
                list(
                    self.canonical_sync_fields
                ),
            "excluded_payload_adjacent_fields":
                list(
                    self.excluded_payload_adjacent_fields
                ),
            "canonical_state_defaults":
                defaults,
            "interface_matrix":
                matrix,
            "state_vector_template_declared":
                True,
            "live_state_vector_created":
                False,
            "state_vector_persisted":
                False,
            "live_state_propagation_performed":
                False,
            "event_dispatch_performed":
                False,
            "ready":
                ready,
        }

    def _safety_boundary(
        self,
    ) -> dict[str, Any]:
        return {
            "live_state_propagation_performed":
                False,
            "event_dispatch_performed":
                False,
            "interface_state_store_created":
                False,
            "interface_state_store_read":
                False,
            "interface_state_store_written":
                False,
            "session_payload_read":
                False,
            "chat_payload_read":
                False,
            "memory_read":
                False,
            "memory_write":
                False,
            "permission_mutation":
                False,
            "audit_write":
                False,
            "network_request":
                False,
            "command_execution":
                False,
            "tool_execution":
                False,
            "interface_process_launch":
                False,
            "background_service_start":
                False,
            "runtime_activation_allowed":
                False,
            "release_gate_open":
                False,
            "autonomous_state_propagation":
                False,
        }

    def multi_interface_state_synchronization_contract(
        self,
    ) -> dict[str, Any]:
        upstream = (
            self._upstream_snapshot()
        )

        browser = (
            self._browser_session_snapshot()
        )

        schema = (
            self._schema_snapshot()
        )

        local_interaction = (
            self._local_interaction_snapshot()
        )

        control_center = (
            self
            ._control_center_reference_snapshot()
        )

        policy = self._state_vector_policy(
            upstream,
            schema,
        )

        safety = self._safety_boundary()

        safety_closed = all(
            value is False
            for value in safety.values()
        )

        ready = all(
            (
                upstream.get(
                    "contract_ready"
                )
                is True,
                browser.get(
                    "contract_ready"
                )
                is True,
                schema.get(
                    "contract_ready"
                )
                is True,
                local_interaction.get(
                    "contract_ready"
                )
                is True,
                control_center.get(
                    "contract_ready"
                )
                is True,
                policy.get("ready") is True,
                safety_closed,
            )
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "multi_interface_state_"
                "synchronization_contract_ready"
                if ready
                else (
                    "multi_interface_state_"
                    "synchronization_contract_degraded"
                )
            ),
            "current_sprint":
                self.current_sprint,
            "current_boundary":
                self.name,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "contract_only":
                True,
            "preview_only":
                True,
            "metadata_only":
                True,
            "planning_ready":
                ready,
            "alpha_ready":
                ready,
            "runtime_ready":
                False,
            "synchronization_scope":
                (
                    "deterministic_metadata_"
                    "state_vector_only"
                ),
            "upstream_owner":
                self.upstream_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "canonical_session_method":
                self.canonical_session_method,
            "interface_state_schema_owner":
                self.interface_state_schema_owner,
            "local_interaction_role":
                "secondary_read_only_baseline",
            "control_center_role":
                "static_reference_only",
            "control_center_snapshot_invoked":
                False,
            "state_vector_created":
                False,
            "state_vector_persisted":
                False,
            "upstream_snapshot":
                upstream,
            "browser_session_snapshot":
                browser,
            "schema_snapshot":
                schema,
            "local_interaction_snapshot":
                local_interaction,
            "control_center_reference_snapshot":
                control_center,
            "state_vector_policy":
                policy,
            "safety_boundary":
                safety,
            "multi_interface_state_"
            "synchronization_contract_ready":
                ready,
        }

    def plan(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .multi_interface_state_synchronization_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "planning_ready":
                contract[
                    "planning_ready"
                ],
            "runtime_ready":
                False,
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "synchronization_scope":
                contract[
                    "synchronization_scope"
                ],
            "state_vector_policy":
                contract[
                    "state_vector_policy"
                ],
            "safety_boundary":
                contract[
                    "safety_boundary"
                ],
            "note": (
                "Sprint 226 declares one "
                "deterministic metadata state-vector "
                "template across interface targets. "
                "It does not read session payloads, "
                "invoke Control Center snapshots, "
                "persist interface state, dispatch "
                "events, propagate live state, or "
                "activate runtime authority."
            ),
        }

    def status(
        self,
    ) -> dict[str, Any]:
        check = self.check()

        contract = check[
            "multi_interface_state_"
            "synchronization_contract"
        ]

        return {
            "name": self.name,
            "version": self.version,
            "status":
                contract["status"],
            "current_sprint":
                self.current_sprint,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "planning_ready":
                contract[
                    "planning_ready"
                ],
            "alpha_ready":
                contract[
                    "alpha_ready"
                ],
            "runtime_ready":
                False,
            "assertion_count":
                check[
                    "assertion_count"
                ],
            "failed_assertion_count":
                check[
                    "failed_assertion_count"
                ],
            "contract_only":
                True,
            "metadata_only":
                True,
        }

    def context(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .multi_interface_state_synchronization_contract()
        )

        return {
            "name": self.name,
            "version": self.version,
            "status":
                contract["status"],
            "current_sprint":
                self.current_sprint,
            "current_boundary":
                self.name,
            "next_sprint":
                self.next_sprint,
            "next_boundary":
                self.next_boundary,
            "upstream_owner":
                self.upstream_owner,
            "canonical_session_owner":
                self.canonical_session_owner,
            "canonical_session_method":
                self.canonical_session_method,
            "interface_state_schema_owner":
                self.interface_state_schema_owner,
            "local_interaction_role":
                contract[
                    "local_interaction_role"
                ],
            "control_center_role":
                contract[
                    "control_center_role"
                ],
            "synchronization_scope":
                contract[
                    "synchronization_scope"
                ],
            "upstream_snapshot":
                contract[
                    "upstream_snapshot"
                ],
            "browser_session_snapshot":
                contract[
                    "browser_session_snapshot"
                ],
            "schema_snapshot":
                contract[
                    "schema_snapshot"
                ],
            "local_interaction_snapshot":
                contract[
                    "local_interaction_snapshot"
                ],
            "control_center_reference_snapshot":
                contract[
                    "control_center_reference_snapshot"
                ],
            "state_vector_policy":
                contract[
                    "state_vector_policy"
                ],
            "safety_boundary":
                contract[
                    "safety_boundary"
                ],
            "runtime_ready":
                False,
        }

    def check(
        self,
    ) -> dict[str, Any]:
        contract = (
            self
            .multi_interface_state_synchronization_contract()
        )

        upstream = contract[
            "upstream_snapshot"
        ]

        browser = contract[
            "browser_session_snapshot"
        ]

        schema = contract[
            "schema_snapshot"
        ]

        local = contract[
            "local_interaction_snapshot"
        ]

        control = contract[
            "control_center_reference_snapshot"
        ]

        policy = contract[
            "state_vector_policy"
        ]

        safety = contract[
            "safety_boundary"
        ]

        matrix = policy[
            "interface_matrix"
        ]

        defaults = policy[
            "canonical_state_defaults"
        ]

        assertions = {
            "project_root_available":
                self.project_root.is_dir(),
            "current_sprint_226":
                contract[
                    "current_sprint"
                ]
                == 226,
            "next_sprint_227":
                contract[
                    "next_sprint"
                ]
                == 227,
            "next_boundary_service_persistence_launcher":
                contract[
                    "next_boundary"
                ]
                == (
                    "service_persistence_"
                    "and_launcher"
                ),
            "contract_only_true":
                contract[
                    "contract_only"
                ]
                is True,
            "preview_only_true":
                contract[
                    "preview_only"
                ]
                is True,
            "metadata_only_true":
                contract[
                    "metadata_only"
                ]
                is True,
            "synchronization_scope_exact":
                contract[
                    "synchronization_scope"
                ]
                == (
                    "deterministic_metadata_"
                    "state_vector_only"
                ),
            "runtime_ready_false":
                contract[
                    "runtime_ready"
                ]
                is False,
            "state_vector_created_false":
                contract[
                    "state_vector_created"
                ]
                is False,
            "state_vector_persisted_false":
                contract[
                    "state_vector_persisted"
                ]
                is False,
            "control_center_snapshot_not_invoked":
                contract[
                    "control_center_snapshot_invoked"
                ]
                is False,

            "upstream_available":
                upstream[
                    "available"
                ]
                is True,
            "upstream_assertion_count_96":
                upstream[
                    "assertion_count"
                ]
                == 96,
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
            "upstream_current_sprint_225":
                upstream[
                    "current_sprint"
                ]
                == 225,
            "upstream_next_sprint_226":
                upstream[
                    "next_sprint"
                ]
                == 226,
            "upstream_next_boundary_sync":
                upstream[
                    "next_boundary"
                ]
                == (
                    "multi_interface_state_"
                    "synchronization"
                ),
            "upstream_session_owner_preserved":
                upstream[
                    "canonical_session_owner"
                ]
                == self.canonical_session_owner,
            "upstream_profile_ready":
                upstream[
                    "profile_ready"
                ]
                is True,
            "upstream_profile_payload_free":
                upstream[
                    "profile_payload_free"
                ]
                is True,
            "upstream_profile_deterministic":
                upstream[
                    "profile_deterministic"
                ]
                is True,
            "upstream_targets_exact":
                upstream[
                    "interface_targets"
                ]
                == list(
                    self.interface_targets
                ),
            "upstream_contract_ready":
                upstream[
                    "contract_ready"
                ]
                is True,
            "upstream_sync_deferred":
                upstream[
                    "sync_deferred"
                ]
                is True,
            "upstream_safety_closed":
                upstream[
                    "safety_closed"
                ]
                is True,

            "browser_available":
                browser[
                    "available"
                ]
                is True,
            "browser_name":
                browser["name"]
                == self.canonical_session_owner,
            "browser_method_contract_snapshot":
                browser[
                    "method"
                ]
                == "contract_snapshot",
            "browser_metadata_only":
                browser[
                    "metadata_only"
                ]
                is True,
            "browser_inspection_read_only":
                browser[
                    "inspection_read_only"
                ]
                is True,
            "browser_payloads_read_zero":
                browser[
                    "session_payloads_read"
                ]
                == 0,
            "browser_metrics_not_inspected":
                browser[
                    "session_metrics_inspected"
                ]
                is False,
            "browser_metrics_not_available":
                browser[
                    "session_metrics_available"
                ]
                is False,
            "browser_error_zero":
                browser[
                    "error_count"
                ]
                == 0,
            "browser_safe_idle":
                browser[
                    "safe_idle"
                ]
                is True,
            "browser_command_false":
                browser[
                    "command_execution"
                ]
                is False,
            "browser_tool_false":
                browser[
                    "tool_execution"
                ]
                is False,
            "browser_autonomous_false":
                browser[
                    "autonomous_action"
                ]
                is False,
            "browser_contract_ready":
                browser[
                    "contract_ready"
                ]
                is True,

            "schema_available":
                schema[
                    "available"
                ]
                is True,
            "schema_owner_name":
                schema["name"]
                == (
                    "aura_chat_bridge_"
                    "session_state_foundation"
                ),
            "schema_fields_exact":
                schema[
                    "state_fields"
                ]
                == list(
                    self.declared_state_fields
                ),
            "schema_field_count_12":
                len(
                    schema[
                        "state_fields"
                    ]
                )
                == 12,
            "schema_events_exact":
                schema[
                    "session_events"
                ]
                == list(
                    self.declared_session_events
                ),
            "schema_event_count_8":
                len(
                    schema[
                        "session_events"
                    ]
                )
                == 8,
            "schema_identity_version_226":
                schema[
                    "identity_version"
                ]
                == "0.236.0-genesis",
            "schema_runtime_mode_blueprint":
                schema[
                    "runtime_mode"
                ]
                == "blueprint_only",
            "schema_auto_action_false":
                schema[
                    "auto_action_allowed"
                ]
                is False,
            "schema_status_bridge_ready":
                schema[
                    "bridge_ready"
                ]
                is True,
            "schema_status_state_ready":
                schema[
                    "state_foundation_ready"
                ]
                is True,
            "schema_status_planner_ready":
                schema[
                    "planner_ready"
                ]
                is True,
            "schema_runtime_ready_false":
                schema[
                    "runtime_ready"
                ]
                is False,
            "schema_execution_features_zero":
                schema[
                    "runtime_execution_features"
                ]
                == 0,
            "schema_context_metadata_only":
                schema[
                    "metadata_only"
                ]
                is True,
            "schema_context_session_runtime_false":
                schema[
                    "session_runtime"
                ]
                is False,
            "schema_context_persistence_false":
                schema[
                    "session_persistence_runtime"
                ]
                is False,
            "schema_context_network_false":
                schema[
                    "network_action"
                ]
                is False,
            "schema_context_command_false":
                schema[
                    "command_execution"
                ]
                is False,
            "schema_contract_ready":
                schema[
                    "contract_ready"
                ]
                is True,

            "local_available":
                local[
                    "available"
                ]
                is True,
            "local_name":
                local["name"]
                == (
                    "local_interaction_"
                    "runtime_stabilization"
                ),
            "local_version_190":
                local[
                    "version"
                ]
                == "0.190.0-genesis",
            "local_status_ready":
                local[
                    "ready"
                ]
                is True,
            "local_components_present":
                local[
                    "components_present"
                ]
                == 9,
            "local_components_expected":
                local[
                    "components_expected"
                ]
                == 9,
            "local_main_cli_present":
                local[
                    "main_cli_present"
                ]
                is True,
            "local_mutation_false":
                local[
                    "runtime_mutation_performed"
                ]
                is False,
            "local_listener_false":
                local[
                    "listener_started"
                ]
                is False,
            "local_subprocess_false":
                local[
                    "subprocess_started"
                ]
                is False,
            "local_release_closed":
                local[
                    "release_gate_closed"
                ]
                is True,
            "local_contract_ready":
                local[
                    "contract_ready"
                ]
                is True,

            "control_available":
                control[
                    "available"
                ]
                is True,
            "control_static_name":
                control["name"]
                == (
                    "aura_control_center_"
                    "backend_runtime"
                ),
            "control_static_sprint":
                control[
                    "sprint"
                ]
                == 184,
            "control_schema_version":
                control[
                    "schema_version"
                ]
                == "1.0",
            "control_role_static":
                control[
                    "role"
                ]
                == "static_reference_only",
            "control_snapshot_invoked_false":
                control[
                    "snapshot_invoked"
                ]
                is False,
            "control_snapshot_allowed_false":
                control[
                    "snapshot_invocation_allowed"
                ]
                is False,
            "control_route_count_9":
                len(
                    control[
                        "routes"
                    ]
                )
                == 9,
            "control_panel_count_8":
                len(
                    control[
                        "panel_ids"
                    ]
                )
                == 8,
            "control_contract_ready":
                control[
                    "contract_ready"
                ]
                is True,

            "policy_interface_targets_exact":
                policy[
                    "interface_targets"
                ]
                == list(
                    self.interface_targets
                ),
            "policy_declared_fields_exact":
                policy[
                    "declared_state_fields"
                ]
                == list(
                    self.declared_state_fields
                ),
            "policy_events_exact":
                policy[
                    "declared_session_events"
                ]
                == list(
                    self.declared_session_events
                ),
            "policy_canonical_fields_exact":
                policy[
                    "canonical_sync_fields"
                ]
                == list(
                    self.canonical_sync_fields
                ),
            "policy_excluded_fields_exact":
                policy[
                    "excluded_payload_adjacent_fields"
                ]
                == list(
                    self.excluded_payload_adjacent_fields
                ),
            "policy_canonical_count_6":
                len(
                    policy[
                        "canonical_sync_fields"
                    ]
                )
                == 6,
            "policy_excluded_count_6":
                len(
                    policy[
                        "excluded_payload_adjacent_fields"
                    ]
                )
                == 6,
            "policy_fields_disjoint":
                set(
                    policy[
                        "canonical_sync_fields"
                    ]
                ).isdisjoint(
                    set(
                        policy[
                            "excluded_payload_adjacent_fields"
                        ]
                    )
                ),
            "policy_canonical_subset":
                set(
                    policy[
                        "canonical_sync_fields"
                    ]
                ).issubset(
                    set(
                        policy[
                            "declared_state_fields"
                        ]
                    )
                ),
            "policy_excluded_subset":
                set(
                    policy[
                        "excluded_payload_adjacent_fields"
                    ]
                ).issubset(
                    set(
                        policy[
                            "declared_state_fields"
                        ]
                    )
                ),
            "policy_template_declared":
                policy[
                    "state_vector_template_declared"
                ]
                is True,
            "policy_interface_matrix_count_7":
                len(matrix) == 7,
            "policy_matrix_fields_match":
                all(
                    item[
                        "canonical_sync_fields"
                    ]
                    == list(
                        self.canonical_sync_fields
                    )
                    for item in matrix.values()
                ),
            "policy_matrix_propagation_false":
                all(
                    item[
                        "live_propagation_performed"
                    ]
                    is False
                    for item in matrix.values()
                ),
            "policy_matrix_store_false":
                all(
                    item[
                        "state_store_created"
                    ]
                    is False
                    for item in matrix.values()
                ),
            "policy_matrix_event_false":
                all(
                    item[
                        "event_dispatched"
                    ]
                    is False
                    for item in matrix.values()
                ),
            "policy_selected_channel_default":
                defaults[
                    "selected_channel"
                ]
                == "metadata_only",
            "policy_safe_idle_default":
                defaults[
                    "safe_idle_mode"
                ]
                is True,
            "policy_permission_default":
                defaults[
                    "permission_boundary_state"
                ]
                == "default_deny",
            "policy_recovery_default":
                defaults[
                    "session_recovery_hint"
                ]
                == "manual_recovery_only",
            "policy_session_runtime_default":
                defaults[
                    "session_runtime_enabled"
                ]
                is False,
            "policy_identity_version_default":
                defaults[
                    "aura_identity_version"
                ]
                == "0.236.0-genesis",
            "policy_ready":
                policy["ready"] is True,
            "policy_contract_ready":
                contract[
                    "multi_interface_state_"
                    "synchronization_contract_ready"
                ]
                is True,
        }

        for key, value in safety.items():
            assertions[
                f"safety_{key}_false"
            ] = value is False

        assertions[
            "safety_all_false"
        ] = all(
            value is False
            for value in safety.values()
        )

        if (
            len(assertions)
            != self.expected_assertion_count
        ):
            raise RuntimeError(
                "Sprint 226 assertion schema "
                "count mismatch: "
                f"{len(assertions)} != "
                f"{self.expected_assertion_count}"
            )

        failed_assertions = [
            name
            for name, passed
            in assertions.items()
            if not passed
        ]

        return {
            "name": self.name,
            "version": self.version,
            "status": (
                "passed"
                if not failed_assertions
                else "failed"
            ),
            "planning_ready":
                not failed_assertions,
            "alpha_ready":
                not failed_assertions,
            "runtime_ready":
                False,
            "assertion_count":
                len(assertions),
            "failed_assertion_count":
                len(
                    failed_assertions
                ),
            "failed_assertions":
                failed_assertions,
            "assertions":
                assertions,
            "multi_interface_state_"
            "synchronization_contract":
                contract,
        }
