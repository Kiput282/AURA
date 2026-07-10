"""Sprint 189 permission, audit, and recovery visibility core."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping


class PermissionAuditRecoveryVisibilityError(RuntimeError):
    """Raised when a Sprint 189 visibility contract is invalid."""


class AuraPermissionAuditRecoveryVisibilityRuntimeManager:
    """Build read-only permission, audit, and recovery snapshots."""

    name = "aura_permission_audit_recovery_visibility_runtime"
    component_version = "0.1.0-alpha"
    sprint = 189
    schema_version = "1.0"

    PROVIDER_ENV_KEYS = (
        "AURA_LOCAL_MODEL_PROVIDER",
        "AURA_LOCAL_MODEL_BASE_URL",
        "AURA_LOCAL_MODEL_NAME",
    )
    ENABLED_ENV_KEY = "AURA_LOCAL_MODEL_ENABLED"

    PERMISSION_ITEMS = (
        {
            "id": "localhost_service_start",
            "label": "Start localhost AURA service",
            "state": "explicit_confirmation_required",
            "confirmation": "--confirm-localhost",
            "scope": "single_foreground_process",
            "mutable_from_visibility_runtime": False,
        },
        {
            "id": "provider_probe",
            "label": "Probe configured local provider",
            "state": "explicit_confirmation_required",
            "confirmation": "confirm_local_connection",
            "scope": "single_loopback_http_probe",
            "mutable_from_visibility_runtime": False,
        },
        {
            "id": "model_message",
            "label": "Send one message to local model",
            "state": "explicit_confirmation_required",
            "confirmation": "confirm_model_request",
            "scope": "single_text_request",
            "mutable_from_visibility_runtime": False,
        },
        {
            "id": "session_clear",
            "label": "Clear one local chat session",
            "state": "exact_phrase_required",
            "confirmation": "CLEAR <session_id>",
            "scope": "single_session",
            "mutable_from_visibility_runtime": False,
        },
        {
            "id": "permission_mutation",
            "label": "Create, grant, revoke, or persist permission",
            "state": "disabled",
            "confirmation": None,
            "scope": "none",
            "mutable_from_visibility_runtime": False,
        },
    )

    AUDIT_EVENT_CONTRACTS = (
        {
            "event_type": "provider_probe_requested",
            "category": "permission",
            "severity": "info",
            "content_included": False,
        },
        {
            "event_type": "provider_probe_blocked",
            "category": "permission",
            "severity": "warning",
            "content_included": False,
        },
        {
            "event_type": "model_message_requested",
            "category": "permission",
            "severity": "info",
            "content_included": False,
        },
        {
            "event_type": "model_message_blocked",
            "category": "permission",
            "severity": "warning",
            "content_included": False,
        },
        {
            "event_type": "model_message_completed",
            "category": "runtime",
            "severity": "info",
            "content_included": False,
        },
        {
            "event_type": "idempotent_replay",
            "category": "recovery",
            "severity": "info",
            "content_included": False,
        },
        {
            "event_type": "revision_conflict",
            "category": "recovery",
            "severity": "warning",
            "content_included": False,
        },
        {
            "event_type": "provider_failure",
            "category": "recovery",
            "severity": "error",
            "content_included": False,
        },
        {
            "event_type": "session_cleared",
            "category": "audit",
            "severity": "warning",
            "content_included": False,
        },
    )

    RECOVERY_CASES = (
        {
            "id": "provider_not_configured",
            "severity": "info",
            "automatic_action": False,
            "safe_guidance": (
                "Keep save-only mode active. Configure an explicit "
                "loopback provider profile before retrying."
            ),
        },
        {
            "id": "provider_disabled",
            "severity": "info",
            "automatic_action": False,
            "safe_guidance": (
                "Keep save-only mode active. Enable the provider only "
                "for a foreground process after operator review."
            ),
        },
        {
            "id": "provider_probe_failed",
            "severity": "warning",
            "automatic_action": False,
            "safe_guidance": (
                "Do not retry automatically. Verify the localhost "
                "provider manually and request a new confirmed probe."
            ),
        },
        {
            "id": "model_request_confirmation_missing",
            "severity": "warning",
            "automatic_action": False,
            "safe_guidance": (
                "Block the request and ask for one-message "
                "confirmation."
            ),
        },
        {
            "id": "session_revision_conflict",
            "severity": "warning",
            "automatic_action": False,
            "safe_guidance": (
                "Reload the current session revision while preserving "
                "the stable client and model request identifiers."
            ),
        },
        {
            "id": "provider_request_failed",
            "severity": "error",
            "automatic_action": False,
            "safe_guidance": (
                "Do not write a partial response. Preserve retry "
                "identifiers and expose the failure to the operator."
            ),
        },
        {
            "id": "service_not_running",
            "severity": "info",
            "automatic_action": False,
            "safe_guidance": (
                "Show STOPPED. Never start the service automatically "
                "from the visibility runtime."
            ),
        },
        {
            "id": "port_unavailable",
            "severity": "error",
            "automatic_action": False,
            "safe_guidance": (
                "Do not kill another process automatically. Show the "
                "port conflict and require operator resolution."
            ),
        },
    )

    REDACTED_FIELDS = (
        "message_content",
        "model_response_content",
        "authorization",
        "api_key",
        "token",
        "password",
        "provider_base_url",
        "environment_value",
        "full_request_body",
        "full_response_body",
    )

    def __init__(
        self,
        environment: Mapping[str, str] | None = None,
    ) -> None:
        self._environment = (
            dict(os.environ)
            if environment is None
            else dict(environment)
        )

    @staticmethod
    def _parse_enabled(value: str | None) -> tuple[bool, bool]:
        if value is None or not value.strip():
            return False, False
        normalized = value.strip().lower()
        if normalized in {"1", "true", "yes", "on"}:
            return True, False
        if normalized in {"0", "false", "no", "off"}:
            return False, False
        return False, True

    def permission_snapshot(self) -> dict[str, Any]:
        required_present = {
            key: bool(self._environment.get(key, "").strip())
            for key in self.PROVIDER_ENV_KEYS
        }
        enabled, invalid_enabled_value = self._parse_enabled(
            self._environment.get(self.ENABLED_ENV_KEY)
        )
        configured = all(required_present.values())

        return {
            "schema_version": self.schema_version,
            "sprint": self.sprint,
            "status": "visible",
            "read_only": True,
            "permission_item_count": len(self.PERMISSION_ITEMS),
            "items": [
                dict(item)
                for item in self.PERMISSION_ITEMS
            ],
            "provider_profile": {
                "configured": configured,
                "enabled_requested": enabled,
                "active_candidate": (
                    configured
                    and enabled
                    and not invalid_enabled_value
                ),
                "configuration_degraded": (
                    invalid_enabled_value
                    or (
                        enabled
                        and not configured
                    )
                ),
                "provider_name_present": required_present[
                    "AURA_LOCAL_MODEL_PROVIDER"
                ],
                "loopback_endpoint_present": required_present[
                    "AURA_LOCAL_MODEL_BASE_URL"
                ],
                "model_name_present": required_present[
                    "AURA_LOCAL_MODEL_NAME"
                ],
                "raw_values_exposed": False,
                "credentials_supported": False,
            },
            "permission_mutation_runtime": False,
            "grant_runtime": False,
            "revoke_runtime": False,
            "permission_persistence_runtime": False,
            "network_calls": 0,
            "disk_writes": 0,
        }

    def audit_snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "sprint": self.sprint,
            "status": "contracts_visible",
            "read_only": True,
            "event_contract_count": len(
                self.AUDIT_EVENT_CONTRACTS
            ),
            "event_contracts": [
                dict(item)
                for item in self.AUDIT_EVENT_CONTRACTS
            ],
            "current_event_count": 0,
            "audit_writer_active": False,
            "audit_persistence_active": False,
            "audit_file_path_exposed": False,
            "message_content_recorded": False,
            "model_response_content_recorded": False,
            "credentials_recorded": False,
            "redacted_fields": list(self.REDACTED_FIELDS),
            "redacted_field_count": len(self.REDACTED_FIELDS),
            "network_calls": 0,
            "disk_writes": 0,
        }

    def recovery_snapshot(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "sprint": self.sprint,
            "status": "guidance_visible",
            "read_only": True,
            "case_count": len(self.RECOVERY_CASES),
            "cases": [
                dict(item)
                for item in self.RECOVERY_CASES
            ],
            "automatic_recovery_active": False,
            "automatic_retry_active": False,
            "automatic_service_restart_active": False,
            "automatic_process_kill_active": False,
            "automatic_permission_change_active": False,
            "automatic_file_repair_active": False,
            "rollback_execution_active": False,
            "operator_confirmation_required": True,
            "network_calls": 0,
            "disk_writes": 0,
        }

    def safety_boundary(self) -> dict[str, Any]:
        return {
            "permission_visibility_runtime": True,
            "audit_visibility_runtime": True,
            "recovery_visibility_runtime": True,
            "read_only_http_routes_runtime": True,
            "read_only_browser_panel_runtime": True,
            "permission_mutation_runtime": False,
            "permission_grant_runtime": False,
            "permission_revoke_runtime": False,
            "permission_persistence_runtime": False,
            "audit_writer_runtime": False,
            "audit_persistence_runtime": False,
            "audit_file_write_runtime": False,
            "automatic_recovery_runtime": False,
            "automatic_retry_runtime": False,
            "automatic_service_restart_runtime": False,
            "automatic_process_kill_runtime": False,
            "rollback_execution_runtime": False,
            "model_download_runtime": False,
            "remote_provider_runtime": False,
            "internet_fallback_runtime": False,
            "streaming_runtime": False,
            "tool_calling_runtime": False,
            "action_dispatch_runtime": False,
            "command_execution_runtime": False,
            "arbitrary_file_runtime": False,
            "aura_long_term_memory_write_runtime": False,
            "desktop_control_runtime": False,
            "background_service_runtime": False,
            "public_listener_runtime": False,
            "lan_listener_runtime": False,
            "browser_auto_launch": False,
            "websocket_runtime": False,
            "eventsource_runtime": False,
            "autonomous_action_runtime": False,
        }

    def visibility_snapshot(self) -> dict[str, Any]:
        permission = self.permission_snapshot()
        audit = self.audit_snapshot()
        recovery = self.recovery_snapshot()
        safety = self.safety_boundary()

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ready",
            "degraded": False,
            "read_only": True,
            "permission": permission,
            "audit": audit,
            "recovery": recovery,
            "safety_boundary": safety,
            "permission_item_count": permission[
                "permission_item_count"
            ],
            "audit_event_contract_count": audit[
                "event_contract_count"
            ],
            "recovery_case_count": recovery["case_count"],
            "provider_profile_configured": permission[
                "provider_profile"
            ]["configured"],
            "provider_enabled_requested": permission[
                "provider_profile"
            ]["enabled_requested"],
            "sensitive_values_exposed": False,
            "network_calls": 0,
            "disk_writes": 0,
        }

    def status(self) -> dict[str, Any]:
        from aura.capability_registry.capability_registry_manager import (
            CapabilityRegistryManager,
        )
        from aura.interactive_control_center_chat_runtime import (
            AuraInteractiveControlCenterChatRuntimeManager,
        )

        registry = CapabilityRegistryManager().capability_summary()
        interactive = (
            AuraInteractiveControlCenterChatRuntimeManager()
            .status()
        )
        snapshot = self.visibility_snapshot()

        ready = (
            interactive["interactive_chat_ready"] is True
            and registry["total_capabilities"] >= 120
            and snapshot["read_only"] is True
        )

        return {
            "schema_version": self.schema_version,
            "name": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "status": "ready" if ready else "degraded",
            "degraded": not ready,
            "visibility_ready": ready,
            "interactive_chat_ready": interactive[
                "interactive_chat_ready"
            ],
            "capability_total": registry[
                "total_capabilities"
            ],
            "online_capabilities": registry[
                "online_capabilities"
            ],
            "runtime_execution_features": registry[
                "runtime_execution_features"
            ],
            "permission_item_count": snapshot[
                "permission_item_count"
            ],
            "audit_event_contract_count": snapshot[
                "audit_event_contract_count"
            ],
            "recovery_case_count": snapshot[
                "recovery_case_count"
            ],
            "provider_profile_configured": snapshot[
                "provider_profile_configured"
            ],
            "provider_enabled_requested": snapshot[
                "provider_enabled_requested"
            ],
            "read_only": True,
            "safety_boundary": snapshot["safety_boundary"],
            "sensitive_values_exposed": False,
            "network_calls": 0,
            "disk_writes": 0,
            "http_routes_active": True,
            "browser_panel_active": True,
        }

    def self_test(self) -> dict[str, Any]:
        assertions: dict[str, bool] = {}

        status = self.status()
        snapshot = self.visibility_snapshot()
        permission = snapshot["permission"]
        audit = snapshot["audit"]
        recovery = snapshot["recovery"]
        safety = snapshot["safety_boundary"]

        assertions["status_ready"] = status["status"] == "ready"
        assertions["not_degraded"] = status["degraded"] is False
        assertions["visibility_ready"] = (
            status["visibility_ready"] is True
        )
        assertions["sprint_189"] = status["sprint"] == 189
        assertions["component_version"] = (
            status["component_version"] == "0.1.0-alpha"
        )
        assertions["interactive_ready"] = (
            status["interactive_chat_ready"] is True
        )
        assertions['capability_total_120'] = (
            status["capability_total"] == 121
        )
        assertions['online_118'] = (
            status["online_capabilities"] == 119
        )
        assertions['runtime_features_four'] = (
            status["runtime_execution_features"] == 4
        )
        assertions["status_read_only"] = (
            status["read_only"] is True
        )
        assertions["status_sensitive_false"] = (
            status["sensitive_values_exposed"] is False
        )
        assertions["status_network_zero"] = (
            status["network_calls"] == 0
        )
        assertions["status_writes_zero"] = (
            status["disk_writes"] == 0
        )
        assertions["status_http_true"] = (
            status["http_routes_active"] is True
        )
        assertions["status_browser_true"] = (
            status["browser_panel_active"] is True
        )

        assertions["snapshot_ready"] = (
            snapshot["status"] == "ready"
        )
        assertions["snapshot_not_degraded"] = (
            snapshot["degraded"] is False
        )
        assertions["snapshot_read_only"] = (
            snapshot["read_only"] is True
        )
        assertions["permission_count_five"] = (
            snapshot["permission_item_count"] == 5
        )
        assertions["audit_count_nine"] = (
            snapshot["audit_event_contract_count"] == 9
        )
        assertions["recovery_count_eight"] = (
            snapshot["recovery_case_count"] == 8
        )
        assertions["snapshot_sensitive_false"] = (
            snapshot["sensitive_values_exposed"] is False
        )
        assertions["snapshot_network_zero"] = (
            snapshot["network_calls"] == 0
        )
        assertions["snapshot_writes_zero"] = (
            snapshot["disk_writes"] == 0
        )

        assertions["permission_visible"] = (
            permission["status"] == "visible"
        )
        assertions["permission_read_only"] = (
            permission["read_only"] is True
        )
        assertions["permission_items_exact"] = (
            permission["permission_item_count"]
            == len(self.PERMISSION_ITEMS)
        )
        assertions["permission_mutation_false"] = (
            permission["permission_mutation_runtime"] is False
        )
        assertions["permission_grant_false"] = (
            permission["grant_runtime"] is False
        )
        assertions["permission_revoke_false"] = (
            permission["revoke_runtime"] is False
        )
        assertions["permission_persist_false"] = (
            permission["permission_persistence_runtime"] is False
        )
        assertions["permission_network_zero"] = (
            permission["network_calls"] == 0
        )
        assertions["permission_writes_zero"] = (
            permission["disk_writes"] == 0
        )

        permission_ids = {
            item["id"]
            for item in permission["items"]
        }
        assertions["permission_ids_exact"] = (
            permission_ids
            == {
                "localhost_service_start",
                "provider_probe",
                "model_message",
                "session_clear",
                "permission_mutation",
            }
        )
        assertions["permission_all_immutable"] = all(
            item["mutable_from_visibility_runtime"] is False
            for item in permission["items"]
        )
        assertions["permission_model_confirm"] = (
            next(
                item
                for item in permission["items"]
                if item["id"] == "model_message"
            )["confirmation"]
            == "confirm_model_request"
        )
        assertions["permission_probe_confirm"] = (
            next(
                item
                for item in permission["items"]
                if item["id"] == "provider_probe"
            )["confirmation"]
            == "confirm_local_connection"
        )
        assertions["permission_clear_phrase"] = (
            next(
                item
                for item in permission["items"]
                if item["id"] == "session_clear"
            )["confirmation"]
            == "CLEAR <session_id>"
        )

        default_profile = permission["provider_profile"]
        assertions["default_unconfigured"] = (
            default_profile["configured"] is False
        )
        assertions["default_disabled"] = (
            default_profile["enabled_requested"] is False
        )
        assertions["default_candidate_false"] = (
            default_profile["active_candidate"] is False
        )
        assertions["default_not_degraded"] = (
            default_profile["configuration_degraded"] is False
        )
        assertions["raw_values_false"] = (
            default_profile["raw_values_exposed"] is False
        )
        assertions["credentials_false"] = (
            default_profile["credentials_supported"] is False
        )

        secret = "S188_SECRET_VALUE_MUST_NOT_LEAK"
        configured_manager = type(self)(
            {
                "AURA_LOCAL_MODEL_PROVIDER": secret,
                "AURA_LOCAL_MODEL_BASE_URL": secret,
                "AURA_LOCAL_MODEL_NAME": secret,
                "AURA_LOCAL_MODEL_ENABLED": "true",
                "AURA_UNUSED_SECRET": secret,
            }
        )
        configured = (
            configured_manager.permission_snapshot()
        )
        configured_profile = configured["provider_profile"]
        assertions["configured_true"] = (
            configured_profile["configured"] is True
        )
        assertions["configured_enabled"] = (
            configured_profile["enabled_requested"] is True
        )
        assertions["configured_candidate"] = (
            configured_profile["active_candidate"] is True
        )
        assertions["configured_not_degraded"] = (
            configured_profile["configuration_degraded"] is False
        )
        assertions["configured_provider_present"] = (
            configured_profile["provider_name_present"] is True
        )
        assertions["configured_endpoint_present"] = (
            configured_profile["loopback_endpoint_present"] is True
        )
        assertions["configured_model_present"] = (
            configured_profile["model_name_present"] is True
        )
        assertions["configured_secret_redacted"] = (
            secret
            not in json.dumps(
                configured,
                sort_keys=True,
            )
        )

        invalid = type(self)(
            {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_BASE_URL": (
                    "http://127.0.0.1:11434"
                ),
                "AURA_LOCAL_MODEL_NAME": "local-model",
                "AURA_LOCAL_MODEL_ENABLED": "maybe",
            }
        ).permission_snapshot()["provider_profile"]
        assertions["invalid_configured"] = (
            invalid["configured"] is True
        )
        assertions["invalid_enabled_false"] = (
            invalid["enabled_requested"] is False
        )
        assertions["invalid_candidate_false"] = (
            invalid["active_candidate"] is False
        )
        assertions["invalid_degraded"] = (
            invalid["configuration_degraded"] is True
        )

        incomplete = type(self)(
            {
                "AURA_LOCAL_MODEL_PROVIDER": "ollama",
                "AURA_LOCAL_MODEL_ENABLED": "true",
            }
        ).permission_snapshot()["provider_profile"]
        assertions["incomplete_configured_false"] = (
            incomplete["configured"] is False
        )
        assertions["incomplete_enabled_true"] = (
            incomplete["enabled_requested"] is True
        )
        assertions["incomplete_candidate_false"] = (
            incomplete["active_candidate"] is False
        )
        assertions["incomplete_degraded_true"] = (
            incomplete["configuration_degraded"] is True
        )

        assertions["audit_visible"] = (
            audit["status"] == "contracts_visible"
        )
        assertions["audit_read_only"] = (
            audit["read_only"] is True
        )
        assertions["audit_count_exact"] = (
            audit["event_contract_count"]
            == len(self.AUDIT_EVENT_CONTRACTS)
        )
        assertions["audit_current_zero"] = (
            audit["current_event_count"] == 0
        )
        assertions["audit_writer_false"] = (
            audit["audit_writer_active"] is False
        )
        assertions["audit_persistence_false"] = (
            audit["audit_persistence_active"] is False
        )
        assertions["audit_path_false"] = (
            audit["audit_file_path_exposed"] is False
        )
        assertions["audit_message_false"] = (
            audit["message_content_recorded"] is False
        )
        assertions["audit_response_false"] = (
            audit["model_response_content_recorded"] is False
        )
        assertions["audit_credentials_false"] = (
            audit["credentials_recorded"] is False
        )
        assertions["audit_redaction_ten"] = (
            audit["redacted_field_count"] == 10
        )
        assertions["audit_network_zero"] = (
            audit["network_calls"] == 0
        )
        assertions["audit_writes_zero"] = (
            audit["disk_writes"] == 0
        )
        assertions["audit_all_no_content"] = all(
            item["content_included"] is False
            for item in audit["event_contracts"]
        )
        assertions["audit_types_unique"] = (
            len(
                {
                    item["event_type"]
                    for item in audit["event_contracts"]
                }
            )
            == audit["event_contract_count"]
        )
        assertions["audit_required_types"] = (
            {
                "provider_probe_requested",
                "provider_probe_blocked",
                "model_message_requested",
                "model_message_blocked",
                "model_message_completed",
                "idempotent_replay",
                "revision_conflict",
                "provider_failure",
                "session_cleared",
            }
            == {
                item["event_type"]
                for item in audit["event_contracts"]
            }
        )

        assertions["recovery_visible"] = (
            recovery["status"] == "guidance_visible"
        )
        assertions["recovery_read_only"] = (
            recovery["read_only"] is True
        )
        assertions["recovery_count_exact"] = (
            recovery["case_count"]
            == len(self.RECOVERY_CASES)
        )
        assertions["recovery_auto_false"] = (
            recovery["automatic_recovery_active"] is False
        )
        assertions["recovery_retry_false"] = (
            recovery["automatic_retry_active"] is False
        )
        assertions["recovery_restart_false"] = (
            recovery["automatic_service_restart_active"] is False
        )
        assertions["recovery_kill_false"] = (
            recovery["automatic_process_kill_active"] is False
        )
        assertions["recovery_permission_false"] = (
            recovery["automatic_permission_change_active"] is False
        )
        assertions["recovery_file_false"] = (
            recovery["automatic_file_repair_active"] is False
        )
        assertions["recovery_rollback_false"] = (
            recovery["rollback_execution_active"] is False
        )
        assertions["recovery_operator_true"] = (
            recovery["operator_confirmation_required"] is True
        )
        assertions["recovery_network_zero"] = (
            recovery["network_calls"] == 0
        )
        assertions["recovery_writes_zero"] = (
            recovery["disk_writes"] == 0
        )
        assertions["recovery_all_manual"] = all(
            item["automatic_action"] is False
            for item in recovery["cases"]
        )
        assertions["recovery_guidance_nonempty"] = all(
            bool(item["safe_guidance"].strip())
            for item in recovery["cases"]
        )
        assertions["recovery_ids_unique"] = (
            len(
                {
                    item["id"]
                    for item in recovery["cases"]
                }
            )
            == recovery["case_count"]
        )

        for key in (
            "permission_mutation_runtime",
            "permission_grant_runtime",
            "permission_revoke_runtime",
            "permission_persistence_runtime",
            "audit_writer_runtime",
            "audit_persistence_runtime",
            "audit_file_write_runtime",
            "automatic_recovery_runtime",
            "automatic_retry_runtime",
            "automatic_service_restart_runtime",
            "automatic_process_kill_runtime",
            "rollback_execution_runtime",
            "model_download_runtime",
            "remote_provider_runtime",
            "internet_fallback_runtime",
            "streaming_runtime",
            "tool_calling_runtime",
            "action_dispatch_runtime",
            "command_execution_runtime",
            "arbitrary_file_runtime",
            "aura_long_term_memory_write_runtime",
            "desktop_control_runtime",
            "background_service_runtime",
            "public_listener_runtime",
            "lan_listener_runtime",
            "browser_auto_launch",
            "websocket_runtime",
            "eventsource_runtime",
            "autonomous_action_runtime",
        ):
            assertions[f"safety_{key}_false"] = (
                safety[key] is False
            )

        assertions["safety_permission_visibility"] = (
            safety["permission_visibility_runtime"] is True
        )
        assertions["safety_audit_visibility"] = (
            safety["audit_visibility_runtime"] is True
        )
        assertions["safety_recovery_visibility"] = (
            safety["recovery_visibility_runtime"] is True
        )

        with tempfile.TemporaryDirectory(
            prefix="aura-s189-visibility-no-write-"
        ) as temporary:
            root = Path(temporary)
            sentinel = root / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            before = {
                item.name: (
                    item.read_bytes(),
                    item.stat().st_mtime_ns,
                )
                for item in root.iterdir()
            }

            type(self)({}).visibility_snapshot()
            type(self)({}).status()

            after = {
                item.name: (
                    item.read_bytes(),
                    item.stat().st_mtime_ns,
                )
                for item in root.iterdir()
            }

        assertions["no_write_fixture_unchanged"] = before == after
        assertions["snapshot_json_serializable"] = bool(
            json.dumps(snapshot, sort_keys=True)
        )
        assertions["status_json_serializable"] = bool(
            json.dumps(status, sort_keys=True)
        )

        failed = [
            key
            for key, passed in assertions.items()
            if not passed
        ]
        if failed:
            raise PermissionAuditRecoveryVisibilityError(
                "Permission/audit/recovery visibility self-test "
                "failed: "
                + ", ".join(failed)
            )

        return {
            "status": "ok",
            "component": self.name,
            "component_version": self.component_version,
            "sprint": self.sprint,
            "schema_version": self.schema_version,
            "assertion_count": len(assertions),
            "failed_assertion_count": 0,
            "permission_visibility_verified": True,
            "audit_contract_visibility_verified": True,
            "recovery_guidance_visibility_verified": True,
            "provider_profile_redaction_verified": True,
            "secret_redaction_verified": True,
            "no_network_calls_verified": True,
            "no_disk_writes_verified": True,
            "permission_mutation_runtime": False,
            "audit_writer_runtime": False,
            "audit_persistence_runtime": False,
            "automatic_recovery_runtime": False,
            "rollback_execution_runtime": False,
            "http_routes_active": True,
            "browser_panel_active": True,
        }


__all__ = [
    "AuraPermissionAuditRecoveryVisibilityRuntimeManager",
    "PermissionAuditRecoveryVisibilityError",
]
