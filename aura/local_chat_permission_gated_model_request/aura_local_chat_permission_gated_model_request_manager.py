"""AURA Local Chat Permission-Gated Model Request.

Sprint 166.

This module adds a safe permission-gated model request dry-run layer for AURA
Local Chat. It intentionally does not dispatch a model request. Instead, it
creates a permission preview packet, request envelope, and blocked gate decision
that prove future model calls must pass explicit permission approval first.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class LocalChatPermissionModelRequestPacket:
    """Dry-run permission-gated model request packet for Sprint 166."""

    packet_id: str
    session_id: str
    prompt_id: str
    permission_preview_id: str
    request_envelope_id: str
    user_message: str
    provider_candidate: str
    gate_state: str
    gate_decision: str
    created_at: str
    session_mode: str = "local_cli_permission_gated_model_request_dry_run"
    source: str = "AuraCLI"


class AuraLocalChatPermissionGatedModelRequestManager:
    """Describe and dry-run Sprint 166 permission-gated model request boundary."""

    name = "aura_local_chat_permission_gated_model_request"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_permission_gated_model_request_status",
        "permission_gated_model_request_runtime_plan",
        "model_permission_preview_packet_plan",
        "model_request_envelope_gate_plan",
        "model_provider_selection_gate_plan",
        "model_credential_network_gate_plan",
        "model_grant_decision_boundary_plan",
        "model_audit_memory_boundary_plan",
        "model_denial_fallback_plan",
        "no_local_chat_permission_model_unsafe_runtime_plan",
        "local_chat_permission_gated_model_request_context",
        "local_chat_permission_model_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "permission_gated_model_runtime_items": [
            "manual_user_prompt_required", "permission_preview_packet_created", "permission_state_required_not_granted", "request_envelope_created", "gate_decision_blocked_without_grant",
            "provider_candidate_metadata_only", "model_dispatch_disabled", "model_response_receive_disabled", "single_turn_dry_run_only", "thin_runtime_alpha_only",
        ],
        "permission_preview_items": [
            "permission_preview_id_required", "permission_scope_model_request", "permission_reason_required", "provider_candidate_declared", "network_need_declared",
            "credential_need_declared", "memory_write_need_declared", "command_need_declared_false", "grant_not_created", "grant_not_applied",
        ],
        "request_envelope_gate_items": [
            "request_envelope_id_required", "prompt_id_required", "session_id_required", "persona_context_allowed", "system_boundary_summary_required",
            "permission_reference_required", "provider_reference_required", "dispatch_flag_false", "response_storage_deferred", "audit_write_deferred",
        ],
        "provider_selection_gate_items": [
            "provider_candidate_local_disabled_adapter", "ollama_future_adapter_requires_permission", "api_future_adapter_requires_permission", "provider_switch_requires_confirmation", "provider_runtime_disabled_by_default",
            "local_process_start_disabled", "remote_api_call_disabled", "network_request_disabled", "provider_config_write_disabled", "model_download_disabled",
        ],
        "credential_network_gate_items": [
            "credential_read_disabled", "environment_secret_read_disabled", "api_key_read_disabled", "network_runtime_disabled", "remote_endpoint_disabled",
            "localhost_socket_disabled", "public_network_disabled", "tls_context_create_disabled", "external_access_disabled", "network_permission_required_future",
        ],
        "grant_decision_boundary_items": [
            "gate_state_required_not_granted", "gate_decision_blocked", "grant_apply_disabled", "grant_revoke_disabled", "permission_mutation_disabled",
            "expiry_timer_disabled", "manual_approval_required_future", "deny_fallback_required", "no_background_retry", "no_autonomous_escalation",
        ],
        "audit_memory_boundary_items": [
            "audit_preview_allowed", "audit_event_write_disabled", "audit_log_append_disabled", "memory_read_disabled", "memory_write_disabled",
            "message_store_is_not_memory_runtime", "chat_history_append_not_triggered_by_model", "redaction_review_required_future", "no_secret_persistence", "no_prompt_persistence_by_default",
        ],
        "denial_fallback_items": [
            "safe_persona_fallback_allowed", "capability_honesty_required", "permission_missing_explanation_required", "model_disabled_explanation_required", "no_fake_model_response",
            "no_hidden_provider_call", "no_partial_response_stream", "no_retry_loop", "no_background_task", "next_sprint_safety_layer_ready",
        ],
        "no_permission_model_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_local_llm_process_start", "no_remote_api_call", "no_network_request",
            "no_credential_read", "no_permission_grant_apply", "no_memory_write", "no_command_execution", "no_arbitrary_file_mutation",
        ],
        "next_sprint_readiness_items": [
            "sprint_167_chat_safety_uncertainty_layer_identified", "permission_gate_preview_ready", "request_envelope_ready", "blocked_gate_decision_ready", "provider_gate_ready",
            "credential_network_gate_ready", "deny_fallback_ready", "model_runtime_still_disabled", "permission_required_before_real_model", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_environment_secret_read", "runtime_provider_config_write", "runtime_permission_grant_apply", "runtime_permission_grant_revoke",
        "runtime_permission_mutation", "runtime_permission_expiry_timer_start", "runtime_memory_write", "runtime_memory_read", "runtime_audit_event_write",
        "runtime_audit_log_append", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_model_download",
        "runtime_background_loop_start", "runtime_autonomous_message_send", "runtime_voice_input_start", "runtime_screen_capture_start", "runtime_control_center_server_start",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_permission_preview_packets_created", "runtime_model_request_envelopes_created", "runtime_gate_decisions_blocked", "runtime_model_requests_dispatched", "runtime_model_responses_received",
        "runtime_local_llm_processes_started", "runtime_remote_api_calls", "runtime_network_requests", "runtime_credentials_read", "runtime_environment_secrets_read",
        "runtime_provider_configs_written", "runtime_permission_grants_applied", "runtime_permission_grants_revoked", "runtime_permission_mutations", "runtime_memory_writes",
        "runtime_memory_reads", "runtime_audit_events_written", "runtime_audit_logs_appended", "runtime_commands_executed", "runtime_tools_executed",
        "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted",
        "runtime_model_downloads", "runtime_background_loops_started", "runtime_autonomous_messages_sent", "runtime_execution_features",
    ]

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or ".").resolve()

    def _blueprint_count(self) -> int:
        return sum(len(items) for items in self.BLUEPRINTS.values())

    def _runtime_zero_map(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def _runtime_false_map(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _boundary(self) -> dict[str, Any]:
        boundary: dict[str, Any] = {
            "local_chat_permission_gated_model_request_only": True,
            "thin_runtime_alpha": True,
            "permission_gated_model_request_enabled": True,
            "permission_preview_packet_runtime_enabled": True,
            "model_request_envelope_runtime_enabled": True,
            "model_gate_decision_runtime_enabled": True,
            "model_request_dispatch_blocked_without_grant": True,
            "model_request_dispatch_disabled": True,
            "model_response_runtime_disabled": True,
            "local_llm_process_runtime_disabled": True,
            "remote_api_runtime_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "permission_grant_runtime_disabled": True,
            "permission_mutation_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "audit_write_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "desktop_action_disabled": True,
            "release_gate_closed": True,
            "manual_approval_required_for_future_model_runtime": True,
            "sprint_167_safety_uncertainty_layer_required": True,
        }
        boundary.update(self._runtime_zero_map())
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        packet = self._boundary()
        packet.update({
            "module": self.name,
            "version": "0.166.0-genesis",
            "status": self.status_name,
            "local_chat_permission_gated_model_request_ready": True,
            "local_chat_permission_gated_model_request_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_permission_gated_model_request_blueprint_count": self._blueprint_count(),
            "plans": list(self.PLAN_TYPES),
            "blueprints": self.BLUEPRINTS,
            "next_sprint": "Sprint 167 — Chat Safety + Uncertainty Layer",
        })
        return packet

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.166.0-genesis",
            "purpose": "Preview a permission-gated model request without dispatching a model call.",
            "safe_to_try_command": 'python3 main.py local-chat-permission-model-dry-run "Aura boleh pakai model?"',
            "provider_candidates": ["local_disabled_adapter", "ollama_future_adapter", "api_future_adapter"],
            "current_runtime_state": "permission_preview_dry_run_only",
            **self._boundary(),
        }

    def _plan(self, plan_name: str, key: str, target: str) -> dict[str, Any]:
        return {
            "plan": plan_name,
            "target": target,
            "items": self.BLUEPRINTS[key],
            "item_count": len(self.BLUEPRINTS[key]),
            **self._boundary(),
        }

    def permission_gated_model_request_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("permission_gated_model_request_runtime_plan", "permission_gated_model_runtime_items", target)
    def model_permission_preview_packet_plan(self, target: str) -> dict[str, Any]: return self._plan("model_permission_preview_packet_plan", "permission_preview_items", target)
    def model_request_envelope_gate_plan(self, target: str) -> dict[str, Any]: return self._plan("model_request_envelope_gate_plan", "request_envelope_gate_items", target)
    def model_provider_selection_gate_plan(self, target: str) -> dict[str, Any]: return self._plan("model_provider_selection_gate_plan", "provider_selection_gate_items", target)
    def model_credential_network_gate_plan(self, target: str) -> dict[str, Any]: return self._plan("model_credential_network_gate_plan", "credential_network_gate_items", target)
    def model_grant_decision_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("model_grant_decision_boundary_plan", "grant_decision_boundary_items", target)
    def model_audit_memory_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("model_audit_memory_boundary_plan", "audit_memory_boundary_items", target)
    def model_denial_fallback_plan(self, target: str) -> dict[str, Any]: return self._plan("model_denial_fallback_plan", "denial_fallback_items", target)
    def no_local_chat_permission_model_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_local_chat_permission_model_unsafe_runtime_plan", "no_permission_model_unsafe_runtime_items", target)
    def local_chat_permission_model_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._plan("local_chat_permission_model_next_sprint_readiness_plan", "next_sprint_readiness_items", target)

    def create_permission_model_dry_run_packet(self, user_message: str, provider_candidate: str = "local_disabled_adapter") -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        model_packet = LocalChatPermissionModelRequestPacket(
            packet_id=f"permission-model-{uuid4().hex[:12]}",
            session_id=f"session-{uuid4().hex[:12]}",
            prompt_id=f"prompt-{uuid4().hex[:12]}",
            permission_preview_id=f"permission-preview-{uuid4().hex[:12]}",
            request_envelope_id=f"request-envelope-{uuid4().hex[:12]}",
            user_message=user_message.strip(),
            provider_candidate=provider_candidate,
            gate_state="required_not_granted",
            gate_decision="blocked_no_permission_grant",
            created_at=now,
        )
        packet: dict[str, Any] = {
            "title": "AURA Local Chat Permission-Gated Model Request Dry Run",
            "version": "0.166.0-genesis",
            "session_mode": model_packet.session_mode,
            "permission_preview_packet": 1,
            "request_envelope": 1,
            "provider_candidate": model_packet.provider_candidate,
            "permission_state": model_packet.gate_state,
            "gate_decision": model_packet.gate_decision,
            "prompt_accepted": 1,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "permission_grants_applied": 0,
            "memory_writes": 0,
            "audit_events_written": 0,
            "commands_executed": 0,
            "arbitrary_files_wrote": 0,
            "runtime_execution": 0,
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "credential_runtime": "disabled",
            "permission_grant_runtime": "disabled",
            "memory_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_write": "disabled",
            "aura_response": (
                "Permission-Gated Model Request aktif dalam mode dry-run. Aku bisa membuat permission preview dan request envelope, "
                "tetapi gate menahan model request karena belum ada grant eksplisit. Tidak ada model lokal/API yang dipanggil, "
                "tidak ada credential/network yang dipakai, tidak ada memory write, command execution, atau file mutation bebas."
            ),
            "packet": model_packet.__dict__,
            **self._boundary(),
        }
        packet["runtime_permission_preview_packets_created"] = 1
        packet["runtime_model_request_envelopes_created"] = 1
        packet["runtime_gate_decisions_blocked"] = 1
        return packet

    def render_permission_model_dry_run(self, user_message: str, provider_candidate: str = "local_disabled_adapter") -> str:
        packet = self.create_permission_model_dry_run_packet(user_message, provider_candidate)
        lines = [
            "AURA Local Chat Permission-Gated Model Request Dry Run",
            f"Version              : {packet['version']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Permission Preview   : {packet['permission_preview_packet']}",
            f"Request Envelope     : {packet['request_envelope']}",
            f"Provider Candidate   : {packet['provider_candidate']}",
            f"Permission State     : {packet['permission_state']}",
            f"Gate Decision        : {packet['gate_decision']}",
            f"Prompt Accepted      : {packet['prompt_accepted']}",
            f"Model Requests       : {packet['model_requests']}",
            f"Model Responses      : {packet['model_responses']}",
            f"Network Requests     : {packet['network_requests']}",
            f"Credentials Read     : {packet['credentials_read']}",
            f"Permission Grants    : {packet['permission_grants_applied']}",
            f"Memory Writes        : {packet['memory_writes']}",
            f"Audit Events Written : {packet['audit_events_written']}",
            f"Commands Executed    : {packet['commands_executed']}",
            f"Arbitrary Files Wrote: {packet['arbitrary_files_wrote']}",
            f"Runtime Execution    : {packet['runtime_execution']}",
            f"Model Runtime        : {packet['model_runtime']}",
            f"Network Runtime      : {packet['network_runtime']}",
            f"Credential Runtime   : {packet['credential_runtime']}",
            f"Permission Grant     : {packet['permission_grant_runtime']}",
            f"Memory Runtime       : {packet['memory_runtime']}",
            f"Command Execution    : {packet['command_execution']}",
            f"Arbitrary File Write : {packet['arbitrary_file_write']}",
            f"AURA: {packet['aura_response']}",
        ]
        return "\n".join(lines)
