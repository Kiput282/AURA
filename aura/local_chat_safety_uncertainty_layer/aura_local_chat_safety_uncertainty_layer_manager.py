"""AURA Local Chat Safety + Uncertainty Layer.

Sprint 167.

This module adds a safety and uncertainty review layer for AURA local chat before
any real model request is allowed. It evaluates one user message in a local,
deterministic, non-model alpha path and returns a safe capability-honesty reply.

No model provider is called. No web search is performed. No network request is
sent. No credential is read. No memory item is written. No command/tool/plugin
action is executed. No arbitrary file path is mutated. No autonomous loop is
started.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class LocalChatSafetyUncertaintyPacket:
    """Deterministic local safety + uncertainty packet for Sprint 167."""

    packet_id: str
    session_id: str
    message_id: str
    user_message: str
    safety_state: str
    uncertainty_state: str
    knowledge_boundary: str
    recommended_next_gate: str
    created_at: str
    session_mode: str = "local_cli_chat_safety_uncertainty_alpha"
    source: str = "AuraCLI"


class AuraLocalChatSafetyUncertaintyLayerManager:
    """Describe and run Sprint 167 chat safety + uncertainty alpha."""

    name = "aura_local_chat_safety_uncertainty_layer"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_safety_uncertainty_layer_status",
        "chat_safety_uncertainty_runtime_plan",
        "chat_safety_classifier_plan",
        "chat_uncertainty_classifier_plan",
        "capability_honesty_response_plan",
        "freshness_boundary_response_plan",
        "model_gate_safety_handoff_plan",
        "memory_command_boundary_plan",
        "safe_fallback_response_plan",
        "no_local_chat_safety_uncertainty_unsafe_runtime_plan",
        "local_chat_safety_uncertainty_context",
        "local_chat_safety_uncertainty_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "safety_uncertainty_runtime_items": [
            "manual_user_message_required", "single_turn_safety_review_supported", "deterministic_local_rules_only", "no_model_inference", "no_network_lookup",
            "safety_packet_created", "uncertainty_packet_created", "capability_honesty_reply_created", "permission_gate_handoff_preserved", "thin_runtime_alpha_only",
        ],
        "safety_classifier_items": [
            "dangerous_action_intent_detected", "desktop_action_request_detected", "command_execution_request_detected", "file_mutation_request_detected", "credential_request_detected",
            "network_request_intent_detected", "model_request_intent_detected", "unsafe_autonomy_intent_detected", "safe_chat_allowed", "human_confirmation_required_for_future_actions",
        ],
        "uncertainty_classifier_items": [
            "latest_current_recent_terms_detected", "today_tomorrow_yesterday_terms_detected", "external_fact_need_detected", "model_knowledge_boundary_declared", "no_fake_current_fact",
            "no_fake_model_capability", "no_hidden_web_search", "no_hidden_provider_call", "uncertain_answer_marked", "future_search_gate_handoff_declared",
        ],
        "capability_honesty_items": [
            "states_current_runtime_mode", "states_model_disabled", "states_voice_disabled", "states_vision_disabled", "states_desktop_action_disabled",
            "states_memory_runtime_disabled", "states_command_execution_disabled", "states_permission_required_for_future_model", "states_safe_local_alpha_scope", "does_not_overclaim_ability",
        ],
        "freshness_boundary_items": [
            "current_event_request_requires_external_source_future", "software_version_request_requires_verification_future", "price_law_schedule_request_requires_verification_future", "repository_state_request_requires_local_git_check", "personal_project_state_uses_checkpoint_context",
            "absolute_date_clarification_required_future", "no_training_cutoff_claim_as_live_fact", "no_current_web_access_in_local_alpha", "safe_uncertainty_message_allowed", "model_gate_not_bypassed",
        ],
        "model_gate_handoff_items": [
            "permission_gate_from_sprint_166_preserved", "model_request_still_blocked_without_grant", "safety_layer_runs_before_model_request", "uncertainty_layer_runs_before_model_request", "provider_candidate_not_dispatched",
            "request_envelope_may_be_tagged_future", "grant_not_created", "grant_not_applied", "audit_write_deferred", "sprint_168_history_viewer_ready",
        ],
        "memory_command_boundary_items": [
            "memory_write_disabled", "memory_read_disabled", "controlled_message_store_not_required", "command_execution_disabled", "tool_execution_disabled",
            "plugin_action_dispatch_disabled", "desktop_control_disabled", "arbitrary_file_read_disabled", "arbitrary_file_write_disabled", "autonomous_loop_disabled",
        ],
        "safe_fallback_items": [
            "safe_persona_reply_allowed", "capability_limitation_reply_allowed", "permission_missing_reply_allowed", "uncertainty_disclosure_reply_allowed", "ask_for_manual_confirmation_future_allowed",
            "no_background_retry", "no_background_monitor", "no_fake_completion", "no_silent_action", "no_unapproved_escalation",
        ],
        "no_safety_uncertainty_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_network_request", "no_credential_read", "no_permission_grant_apply",
            "no_memory_write", "no_memory_read", "no_audit_write", "no_command_execution", "no_arbitrary_file_mutation",
        ],
        "next_sprint_readiness_items": [
            "sprint_168_chat_history_viewer_contract_identified", "safety_packet_ready", "uncertainty_packet_ready", "capability_honesty_ready", "freshness_boundary_ready",
            "model_permission_gate_preserved", "history_viewer_must_be_read_only", "message_store_viewer_no_mutation", "model_runtime_still_disabled", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_memory_write", "runtime_memory_read",
        "runtime_audit_event_write", "runtime_audit_log_append", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch",
        "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control",
        "runtime_background_loop_start", "runtime_autonomous_message_send", "runtime_voice_input_start", "runtime_screen_capture_start", "runtime_control_center_server_start",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_safety_packets_created", "runtime_uncertainty_checks_completed", "runtime_capability_honesty_replies_created", "runtime_safety_blocks_triggered", "runtime_model_requests_dispatched",
        "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read", "runtime_permission_grants_applied", "runtime_memory_writes",
        "runtime_memory_reads", "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched",
        "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_execution_features",
    ]

    CURRENT_HINTS = ("terbaru", "latest", "recent", "hari ini", "today", "besok", "tomorrow", "kemarin", "yesterday", "sekarang", "current", "harga", "price", "jadwal", "schedule")
    ACTION_HINTS = ("buka", "open ", "jalankan", "run ", "hapus", "delete", "buat folder", "create folder", "install", "download", "credential", "api key", "token")
    MODEL_HINTS = ("pakai model", "gunakan model", "call model", "ollama", "api model", "llm")

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
            "local_chat_safety_uncertainty_only": True,
            "thin_runtime_alpha": True,
            "chat_safety_uncertainty_layer_enabled": True,
            "safety_classifier_runtime_enabled": True,
            "uncertainty_classifier_runtime_enabled": True,
            "capability_honesty_runtime_enabled": True,
            "freshness_boundary_runtime_enabled": True,
            "model_request_dispatch_blocked_without_grant": True,
            "model_request_dispatch_disabled": True,
            "model_response_runtime_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "permission_grant_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "audit_write_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "desktop_action_disabled": True,
            "release_gate_closed": True,
            "sprint_168_history_viewer_contract_required": True,
        }
        boundary.update(self._runtime_zero_map())
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        packet = self._boundary()
        packet.update({
            "module": self.name,
            "version": "0.167.0-genesis",
            "status": self.status_name,
            "local_chat_safety_uncertainty_layer_ready": True,
            "local_chat_safety_uncertainty_layer_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_safety_uncertainty_layer_blueprint_count": self._blueprint_count(),
            "plans": list(self.PLAN_TYPES),
            "blueprints": self.BLUEPRINTS,
            "next_sprint": "Sprint 168 — Chat History Viewer Contract",
        })
        return packet

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.167.0-genesis",
            "purpose": "Review one local chat message for safety and uncertainty before any future model request.",
            "safe_to_try_command": 'python3 main.py local-chat-safety-alpha "Aura apakah info ini terbaru?"',
            "current_runtime_state": "deterministic_safety_uncertainty_alpha_only",
            **self._boundary(),
        }

    def _plan(self, plan_name: str, key: str, target: str) -> dict[str, Any]:
        return {"plan": plan_name, "target": target, "items": self.BLUEPRINTS[key], "item_count": len(self.BLUEPRINTS[key]), **self._boundary()}

    def chat_safety_uncertainty_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_safety_uncertainty_runtime_plan", "safety_uncertainty_runtime_items", target)
    def chat_safety_classifier_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_safety_classifier_plan", "safety_classifier_items", target)
    def chat_uncertainty_classifier_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_uncertainty_classifier_plan", "uncertainty_classifier_items", target)
    def capability_honesty_response_plan(self, target: str) -> dict[str, Any]: return self._plan("capability_honesty_response_plan", "capability_honesty_items", target)
    def freshness_boundary_response_plan(self, target: str) -> dict[str, Any]: return self._plan("freshness_boundary_response_plan", "freshness_boundary_items", target)
    def model_gate_safety_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("model_gate_safety_handoff_plan", "model_gate_handoff_items", target)
    def memory_command_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_command_boundary_plan", "memory_command_boundary_items", target)
    def safe_fallback_response_plan(self, target: str) -> dict[str, Any]: return self._plan("safe_fallback_response_plan", "safe_fallback_items", target)
    def no_local_chat_safety_uncertainty_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_local_chat_safety_uncertainty_unsafe_runtime_plan", "no_safety_uncertainty_unsafe_runtime_items", target)
    def local_chat_safety_uncertainty_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._plan("local_chat_safety_uncertainty_next_sprint_readiness_plan", "next_sprint_readiness_items", target)

    def _classify(self, user_message: str) -> tuple[str, str, str, str]:
        message = user_message.lower()
        action_like = any(hint in message for hint in self.ACTION_HINTS)
        model_like = any(hint in message for hint in self.MODEL_HINTS)
        current_like = any(hint in message for hint in self.CURRENT_HINTS)
        if action_like:
            safety_state = "action_requires_future_permission"
            recommended_next_gate = "deny_action_in_local_chat_alpha"
        elif model_like:
            safety_state = "model_request_requires_permission_gate"
            recommended_next_gate = "blocked_no_permission_grant"
        else:
            safety_state = "safe_chat_alpha_allowed"
            recommended_next_gate = "safe_persona_reply"
        if current_like:
            uncertainty_state = "current_information_requires_future_verification"
            knowledge_boundary = "local_alpha_cannot_verify_latest_external_facts"
        else:
            uncertainty_state = "no_current_fact_claim_required"
            knowledge_boundary = "local_alpha_can_answer_only_from static boundary rules"
        return safety_state, uncertainty_state, knowledge_boundary, recommended_next_gate

    def create_safety_uncertainty_packet(self, user_message: str) -> dict[str, Any]:
        now = datetime.now(timezone.utc).isoformat()
        safety_state, uncertainty_state, knowledge_boundary, recommended_next_gate = self._classify(user_message)
        packet_model = LocalChatSafetyUncertaintyPacket(
            packet_id=f"safety-{uuid4().hex[:12]}",
            session_id=f"session-{uuid4().hex[:12]}",
            message_id=f"message-{uuid4().hex[:12]}",
            user_message=user_message.strip(),
            safety_state=safety_state,
            uncertainty_state=uncertainty_state,
            knowledge_boundary=knowledge_boundary,
            recommended_next_gate=recommended_next_gate,
            created_at=now,
        )
        if safety_state == "action_requires_future_permission":
            response = "Aku menangkap permintaan aksi lokal. Di Sprint 167 aku hanya bisa memberi safety review; command execution, desktop action, dan file mutation masih nonaktif sampai permission/action runtime dibuat nanti."
        elif safety_state == "model_request_requires_permission_gate":
            response = "Aku menangkap kebutuhan model, tetapi model request tetap diblokir tanpa grant eksplisit. Sprint 166 gate masih aktif, jadi tidak ada model lokal/API yang dipanggil."
        elif uncertainty_state == "current_information_requires_future_verification":
            response = "Aku bisa menandai bahwa pertanyaan ini membutuhkan verifikasi terbaru. Di local alpha ini aku tidak melakukan web search atau model call, jadi aku tidak akan berpura-pura tahu fakta terkini."
        else:
            response = "Chat Safety + Uncertainty Layer aktif. Pesan ini aman untuk balasan persona lokal, sambil tetap menjaga batas: tanpa model call, network, memory write, command execution, atau file mutation bebas."
        packet: dict[str, Any] = {
            "title": "AURA Local Chat Safety + Uncertainty Alpha",
            "version": "0.167.0-genesis",
            "session_mode": packet_model.session_mode,
            "safety_checks": 1,
            "uncertainty_checks": 1,
            "capability_honesty_replies": 1,
            "safety_state": packet_model.safety_state,
            "uncertainty_state": packet_model.uncertainty_state,
            "knowledge_boundary": packet_model.knowledge_boundary,
            "recommended_next_gate": packet_model.recommended_next_gate,
            "message_accepted": 1,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "permission_grants": 0,
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
            "aura_response": response,
            "packet": packet_model.__dict__,
            **self._boundary(),
        }
        packet["runtime_safety_packets_created"] = 1
        packet["runtime_uncertainty_checks_completed"] = 1
        packet["runtime_capability_honesty_replies_created"] = 1
        if safety_state != "safe_chat_alpha_allowed":
            packet["runtime_safety_blocks_triggered"] = 1
        return packet

    def render_safety_alpha(self, user_message: str) -> str:
        packet = self.create_safety_uncertainty_packet(user_message)
        lines = [
            "AURA Local Chat Safety + Uncertainty Alpha",
            f"Version              : {packet['version']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Safety Checks        : {packet['safety_checks']}",
            f"Uncertainty Checks   : {packet['uncertainty_checks']}",
            f"Capability Replies   : {packet['capability_honesty_replies']}",
            f"Safety State         : {packet['safety_state']}",
            f"Uncertainty State    : {packet['uncertainty_state']}",
            f"Knowledge Boundary   : {packet['knowledge_boundary']}",
            f"Recommended Gate     : {packet['recommended_next_gate']}",
            f"Message Accepted     : {packet['message_accepted']}",
            f"Model Requests       : {packet['model_requests']}",
            f"Model Responses      : {packet['model_responses']}",
            f"Network Requests     : {packet['network_requests']}",
            f"Credentials Read     : {packet['credentials_read']}",
            f"Permission Grants    : {packet['permission_grants']}",
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
