"""AURA Local Chat Model Adapter Boundary.

Sprint 165.

This module defines the first safe model-adapter boundary for AURA local chat.
It intentionally does not call a model provider. Instead, it creates a dry-run
adapter packet that validates provider metadata, prompt envelope structure,
permission handoff expectations, and zero-runtime counters.

The boundary is intentionally narrow: no local LLM is called, no remote API is
called, no network request is sent, no credential is read, no memory item is
written, no command/tool/plugin action is executed, no arbitrary file path is
mutated, and no autonomous loop is started.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
import os


@dataclass(frozen=True)
class LocalChatModelAdapterPacket:
    """A dry-run model adapter packet for Sprint 165."""

    packet_id: str
    session_id: str
    prompt_id: str
    user_message: str
    provider_candidate: str
    adapter_mode: str
    created_at: str
    permission_state: str = "not_requested"
    session_mode: str = "local_cli_model_adapter_boundary_dry_run"
    source: str = "AuraCLI"


class AuraLocalChatModelAdapterBoundaryManager:
    """Describe and dry-run Sprint 165 model adapter boundary."""

    name = "aura_local_chat_model_adapter_boundary"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_model_adapter_boundary_status",
        "local_chat_model_adapter_boundary_runtime_plan",
        "model_adapter_provider_contract_plan",
        "model_prompt_envelope_contract_plan",
        "model_permission_handoff_plan",
        "model_response_envelope_contract_plan",
        "model_error_boundary_plan",
        "model_network_credential_boundary_plan",
        "model_memory_command_boundary_plan",
        "no_local_chat_model_adapter_unsafe_runtime_plan",
        "local_chat_model_adapter_boundary_context",
        "local_chat_model_adapter_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "model_adapter_boundary_runtime_items": [
            "dry_run_adapter_packet_created", "manual_user_message_required", "single_turn_prompt_envelope_supported", "provider_candidate_metadata_supported", "adapter_mode_declared",
            "permission_state_declared", "model_request_dispatch_disabled", "model_response_receive_disabled", "network_request_disabled", "thin_runtime_alpha_only",
        ],
        "provider_contract_items": [
            "provider_id_required", "provider_kind_declared", "provider_transport_declared", "provider_locality_declared", "provider_permission_profile_declared",
            "provider_credential_policy_declared", "provider_network_policy_declared", "provider_timeout_policy_declared", "provider_disabled_by_default", "provider_registry_dry_run_only",
        ],
        "prompt_envelope_items": [
            "prompt_id_required", "session_id_required", "source_message_required", "persona_context_reference_allowed", "system_boundary_summary_required",
            "no_secret_injection", "no_tool_schema_injection", "no_command_request_execution", "no_file_path_execution", "prompt_preview_metadata_only",
        ],
        "permission_handoff_items": [
            "model_request_requires_future_permission", "provider_selection_requires_future_permission", "credential_access_requires_future_permission", "network_provider_requires_future_permission", "local_model_process_requires_future_permission",
            "permission_gate_handoff_to_sprint_166", "no_permission_request_created_yet", "no_permission_grant_applied", "no_permission_mutation", "manual_confirmation_required_future",
        ],
        "response_envelope_items": [
            "response_id_reserved", "provider_response_schema_declared", "token_usage_schema_declared", "latency_schema_declared", "safety_flags_schema_declared",
            "no_response_received_in_sprint_165", "fallback_persona_response_allowed", "response_storage_deferred", "response_audit_deferred", "response_validation_deferred",
        ],
        "model_error_boundary_items": [
            "provider_unavailable_error_declared", "permission_missing_error_declared", "credential_missing_error_declared", "network_disabled_error_declared", "timeout_error_declared",
            "invalid_response_error_declared", "safe_fallback_declared", "no_retry_loop_started", "no_background_recovery", "no_exception_escalation_to_action",
        ],
        "network_credential_boundary_items": [
            "network_runtime_disabled", "remote_api_disabled", "local_socket_disabled", "credential_read_disabled", "environment_secret_read_disabled",
            "api_key_storage_disabled", "provider_config_write_disabled", "external_endpoint_disabled", "public_network_disabled", "no_model_download_runtime",
        ],
        "memory_command_boundary_items": [
            "memory_runtime_disabled", "memory_write_counter_zero", "memory_read_counter_zero", "command_execution_disabled", "tool_execution_disabled",
            "plugin_action_disabled", "desktop_control_disabled", "file_mutation_disabled", "autonomous_action_disabled", "message_store_not_model_memory",
        ],
        "no_model_adapter_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_local_llm_process_start", "no_remote_api_call", "no_network_request",
            "no_credential_read", "no_memory_write", "no_command_execution", "no_arbitrary_file_mutation", "no_background_loop",
        ],
        "next_sprint_readiness_items": [
            "sprint_166_permission_gated_model_request_identified", "adapter_boundary_ready", "provider_contract_ready", "prompt_envelope_ready", "permission_handoff_ready",
            "response_envelope_ready", "error_boundary_ready", "credential_boundary_ready", "model_runtime_still_disabled", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_environment_secret_read", "runtime_provider_config_write", "runtime_permission_request_create", "runtime_permission_grant_apply",
        "runtime_permission_mutation", "runtime_memory_write", "runtime_memory_read", "runtime_command_execution", "runtime_tool_execution",
        "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete",
        "runtime_desktop_control", "runtime_voice_input_start", "runtime_screen_capture_start", "runtime_control_center_server_start", "runtime_http_listener_start",
        "runtime_socket_open", "runtime_port_binding", "runtime_background_loop_start", "runtime_autonomous_message_send", "runtime_model_download",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_adapter_packets_created", "runtime_prompt_envelopes_created", "runtime_provider_candidates_selected", "runtime_model_requests_dispatched", "runtime_model_responses_received",
        "runtime_local_llm_processes_started", "runtime_remote_api_calls", "runtime_network_requests", "runtime_credentials_read", "runtime_environment_secrets_read",
        "runtime_provider_configs_written", "runtime_permission_requests_created", "runtime_permission_grants_applied", "runtime_permission_mutations", "runtime_memory_writes",
        "runtime_memory_reads", "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read",
        "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_desktop_control_actions", "runtime_model_downloads",
        "runtime_background_loops_started", "runtime_autonomous_messages_sent", "runtime_execution_features",
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
            "local_chat_model_adapter_boundary_only": True,
            "thin_runtime_alpha": True,
            "model_adapter_boundary_enabled": True,
            "dry_model_adapter_packet_runtime_enabled": True,
            "provider_registry_dry_run_enabled": True,
            "prompt_envelope_contract_runtime_enabled": True,
            "model_request_dispatch_disabled": True,
            "model_response_runtime_disabled": True,
            "local_llm_process_runtime_disabled": True,
            "remote_api_runtime_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "permission_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "desktop_action_disabled": True,
            "release_gate_closed": True,
            "manual_approval_required_for_future_model_runtime": True,
            "sprint_166_permission_gate_required": True,
        }
        boundary.update(self._runtime_zero_map())
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        packet = self._boundary()
        packet.update({
            "module": self.name,
            "version": "0.165.0-genesis",
            "status": self.status_name,
            "local_chat_model_adapter_boundary_ready": True,
            "local_chat_model_adapter_boundary_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_model_adapter_boundary_blueprint_count": self._blueprint_count(),
            "plans": list(self.PLAN_TYPES),
            "blueprints": self.BLUEPRINTS,
            "next_sprint": "Sprint 166 — Permission-Gated Model Request",
        })
        return packet

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.165.0-genesis",
            "purpose": "Define a safe model adapter boundary for AURA local chat without dispatching any model request.",
            "provider_candidates": ["local_disabled_adapter", "ollama_future_adapter", "api_future_adapter"],
            "current_runtime_state": "dry_run_boundary_only",
            "safe_to_try_command": 'python3 main.py local-chat-model-adapter-dry-run "Aura coba model adapter"',
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

    def local_chat_model_adapter_boundary_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("local_chat_model_adapter_boundary_runtime_plan", "model_adapter_boundary_runtime_items", target)
    def model_adapter_provider_contract_plan(self, target: str) -> dict[str, Any]: return self._plan("model_adapter_provider_contract_plan", "provider_contract_items", target)
    def model_prompt_envelope_contract_plan(self, target: str) -> dict[str, Any]: return self._plan("model_prompt_envelope_contract_plan", "prompt_envelope_items", target)
    def model_permission_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("model_permission_handoff_plan", "permission_handoff_items", target)
    def model_response_envelope_contract_plan(self, target: str) -> dict[str, Any]: return self._plan("model_response_envelope_contract_plan", "response_envelope_items", target)
    def model_error_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("model_error_boundary_plan", "model_error_boundary_items", target)
    def model_network_credential_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("model_network_credential_boundary_plan", "network_credential_boundary_items", target)
    def model_memory_command_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("model_memory_command_boundary_plan", "memory_command_boundary_items", target)
    def no_local_chat_model_adapter_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_local_chat_model_adapter_unsafe_runtime_plan", "no_model_adapter_unsafe_runtime_items", target)
    def local_chat_model_adapter_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._plan("local_chat_model_adapter_next_sprint_readiness_plan", "next_sprint_readiness_items", target)

    def create_dry_run_packet(self, user_message: str, provider_candidate: str = "local_disabled_adapter") -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        model_packet = LocalChatModelAdapterPacket(
            packet_id=f"adapter-{uuid4().hex[:12]}",
            session_id=f"session-{uuid4().hex[:12]}",
            prompt_id=f"prompt-{uuid4().hex[:12]}",
            user_message=user_message.strip(),
            provider_candidate=provider_candidate,
            adapter_mode="dry_run_no_dispatch",
            created_at=now,
        )
        packet: dict[str, Any] = {
            "title": "AURA Local Chat Model Adapter Boundary Dry Run",
            "version": "0.165.0-genesis",
            "session_mode": model_packet.session_mode,
            "adapter_packet_created": 1,
            "prompt_envelope_created": 1,
            "provider_candidate": model_packet.provider_candidate,
            "permission_state": model_packet.permission_state,
            "prompt_accepted": 1,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "memory_writes": 0,
            "commands_executed": 0,
            "arbitrary_files_wrote": 0,
            "runtime_execution": 0,
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "credential_runtime": "disabled",
            "memory_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_write": "disabled",
            "aura_response": (
                "Model Adapter Boundary aktif dalam mode dry-run. Aku bisa membentuk paket prompt dan metadata provider, "
                "tetapi belum memanggil model lokal/API, belum membaca credential, belum memakai network, belum menulis memory, "
                "dan belum menjalankan command. Sprint 166 harus menambahkan permission gate sebelum model request nyata diizinkan."
            ),
            "packet": model_packet.__dict__,
            **self._boundary(),
        }
        packet["runtime_adapter_packets_created"] = 1
        packet["runtime_prompt_envelopes_created"] = 1
        packet["runtime_provider_candidates_selected"] = 1
        return packet

    def render_dry_run(self, user_message: str, provider_candidate: str = "local_disabled_adapter") -> str:
        packet = self.create_dry_run_packet(user_message, provider_candidate)
        lines = [
            "AURA Local Chat Model Adapter Boundary Dry Run",
            f"Version              : {packet['version']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Adapter Packet Created: {packet['adapter_packet_created']}",
            f"Prompt Envelope      : {packet['prompt_envelope_created']}",
            f"Provider Candidate   : {packet['provider_candidate']}",
            f"Permission State     : {packet['permission_state']}",
            f"Prompt Accepted      : {packet['prompt_accepted']}",
            f"Model Requests       : {packet['model_requests']}",
            f"Model Responses      : {packet['model_responses']}",
            f"Network Requests     : {packet['network_requests']}",
            f"Credentials Read     : {packet['credentials_read']}",
            f"Memory Writes        : {packet['memory_writes']}",
            f"Commands Executed    : {packet['commands_executed']}",
            f"Arbitrary Files Wrote: {packet['arbitrary_files_wrote']}",
            f"Runtime Execution    : {packet['runtime_execution']}",
            f"Model Runtime        : {packet['model_runtime']}",
            f"Network Runtime      : {packet['network_runtime']}",
            f"Credential Runtime   : {packet['credential_runtime']}",
            f"Memory Runtime       : {packet['memory_runtime']}",
            f"Command Execution    : {packet['command_execution']}",
            f"Arbitrary File Write : {packet['arbitrary_file_write']}",
            f"AURA: {packet['aura_response']}",
        ]
        return "\n".join(lines)
