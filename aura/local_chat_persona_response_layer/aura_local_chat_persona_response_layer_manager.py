"""AURA Persona Response Layer.

Sprint 164.

This module strengthens AURA's local chat alpha personality layer. It creates
one safe local chat turn with a deterministic AURA persona response, appends the
turn to the controlled local chat JSONL store, and reports clear boundaries.

The layer is intentionally narrow: no model provider is called, no memory item is
written, no command/tool/plugin action is executed, no arbitrary file path is
mutated, no desktop action is performed, no network request is sent, and no
background loop is started.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4
import json
import os


@dataclass(frozen=True)
class LocalChatPersonaTurn:
    """A controlled local persona response packet for Sprint 164."""

    session_id: str
    message_id: str
    response_id: str
    store_record_id: str
    user_message: str
    aura_response: str
    persona_mode: str
    created_at: str
    session_mode: str = "local_cli_persona_response_alpha"
    source: str = "AuraCLI"


class AuraLocalChatPersonaResponseLayerManager:
    """Run and describe Sprint 164 local AURA persona response alpha."""

    name = "aura_local_chat_persona_response_layer"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_persona_response_layer_status",
        "local_chat_persona_response_runtime_plan",
        "aura_persona_style_contract_plan",
        "persona_capability_honesty_plan",
        "persona_action_decline_plan",
        "persona_safety_boundary_plan",
        "persona_message_store_link_plan",
        "persona_model_boundary_plan",
        "persona_memory_boundary_plan",
        "no_local_chat_persona_unsafe_runtime_plan",
        "local_chat_persona_context",
        "local_chat_persona_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "local_chat_persona_response_runtime_items": [
            "persona_response_layer_alpha_enabled", "single_turn_persona_alpha_enabled", "manual_user_message_required", "transient_session_packet_created", "controlled_store_append_supported",
            "deterministic_persona_reply_created", "persona_mode_classification_supported", "capability_honesty_included", "runtime_boundary_summary_included", "thin_runtime_alpha_only",
        ],
        "aura_persona_style_contract_items": [
            "warm_ai_partner_tone", "clear_indonesian_default", "concise_but_supportive_style", "honest_capability_boundary", "no_false_autonomy_claims",
            "no_fake_model_claims", "no_fake_memory_claims", "project_aura_context_awareness", "safe_developer_assistant_identity", "genesis_final_alignment",
        ],
        "persona_capability_honesty_items": [
            "states_current_sprint_when_relevant", "states_model_runtime_disabled", "states_memory_runtime_disabled", "states_command_execution_disabled", "states_file_mutation_boundary",
            "states_voice_deferred_to_181_190", "states_vision_deferred_to_191_200", "states_action_deferred_to_201_210", "no_overpromising", "suggests_safe_next_step",
        ],
        "persona_action_decline_items": [
            "detects_app_launch_request_as_text", "detects_folder_create_request_as_text", "detects_shell_command_request_as_text", "detects_file_mutation_request_as_text", "declines_runtime_action_politely",
            "explains_future_action_block", "keeps_message_store_only", "does_not_dispatch_action", "does_not_request_permission_yet", "does_not_execute_command",
        ],
        "persona_safety_boundary_items": [
            "model_request_dispatch_disabled", "memory_write_disabled", "command_execution_disabled", "tool_execution_disabled", "plugin_action_disabled",
            "desktop_control_disabled", "network_request_disabled", "voice_runtime_disabled", "vision_runtime_disabled", "autonomous_action_disabled",
        ],
        "persona_message_store_link_items": [
            "uses_controlled_message_store_path", "jsonl_append_supported", "store_record_schema_v2_defined", "persona_mode_field_defined", "persona_policy_snapshot_field_defined",
            "no_user_supplied_output_path", "store_dir_env_override_supported", "aura_runtime_gitignored", "history_viewer_handoff_preserved", "message_store_not_memory_store",
        ],
        "persona_model_boundary_items": [
            "deterministic_local_response_only", "no_local_llm_called", "no_remote_llm_called", "no_network_prompt_sent", "model_adapter_handoff_to_sprint_165",
            "permission_gate_handoff_to_sprint_166", "no_prompt_inference_runtime", "no_token_counter_runtime", "no_model_credentials_needed", "model_counter_zero",
        ],
        "persona_memory_boundary_items": [
            "memory_runtime_disabled", "memory_write_counter_zero", "memory_read_counter_zero", "profile_update_disabled", "preference_extraction_disabled",
            "workspace_memory_disabled", "project_journal_disabled", "message_store_separate_from_memory", "memory_runtime_handoff_to_171_180", "memory_counter_zero",
        ],
        "no_local_chat_persona_unsafe_runtime_items": [
            "no_model_runtime", "no_memory_runtime", "no_permission_mutation_runtime", "no_audit_write_runtime", "no_command_execution_runtime",
            "no_tool_execution_runtime", "no_plugin_action_runtime", "no_desktop_control_runtime", "no_network_runtime", "no_arbitrary_file_mutation_runtime",
        ],
        "local_chat_persona_next_sprint_readiness_items": [
            "sprint_165_model_adapter_boundary_identified", "persona_layer_ready", "safe_decline_policy_ready", "capability_honesty_ready", "message_store_link_ready",
            "model_runtime_still_disabled", "memory_runtime_still_deferred", "permission_gated_model_request_handoff_preserved", "chat_safety_layer_handoff_to_sprint_167", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_memory_write", "runtime_memory_read", "runtime_permission_request_create",
        "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_audit_event_write", "runtime_audit_log_append", "runtime_command_execution",
        "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify",
        "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_app_launch", "runtime_folder_create", "runtime_voice_input_start",
        "runtime_voice_output_start", "runtime_screen_capture_start", "runtime_network_request", "runtime_control_center_server_start", "runtime_http_listener_start",
        "runtime_socket_open", "runtime_port_binding", "runtime_background_loop_start", "runtime_autonomous_message_send",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_memory_writes", "runtime_memory_reads", "runtime_permission_requests_created",
        "runtime_permission_grants_applied", "runtime_permission_mutations", "runtime_audit_events_written", "runtime_audit_logs_appended", "runtime_commands_executed",
        "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified",
        "runtime_arbitrary_files_deleted", "runtime_desktop_control_actions", "runtime_apps_launched", "runtime_folders_created", "runtime_voice_inputs_started",
        "runtime_voice_outputs_started", "runtime_screen_captures_started", "runtime_network_requests", "runtime_control_center_servers_started", "runtime_http_listeners_started",
        "runtime_ports_bound", "runtime_background_loops_started", "runtime_autonomous_messages_sent", "runtime_execution_features",
    ]

    def __init__(self, project_root: str | Path | None = None, store_dir: str | Path | None = None) -> None:
        self.project_root = Path(project_root or ".").resolve()
        env_store = os.environ.get("AURA_LOCAL_CHAT_STORE_DIR")
        self.store_dir = Path(store_dir or env_store or (self.project_root / ".aura_runtime" / "local_chat")).resolve()
        self.store_file = self.store_dir / "messages.jsonl"

    def _blueprint_count(self) -> int:
        return sum(len(items) for items in self.BLUEPRINTS.values())

    def _runtime_zero_map(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def _runtime_false_map(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _common_boundary(self) -> dict[str, Any]:
        boundary: dict[str, Any] = {
            "local_chat_persona_response_layer_only": True,
            "thin_runtime_alpha": True,
            "persona_response_layer_runtime_enabled": True,
            "single_turn_persona_alpha": True,
            "manual_user_message_required": True,
            "controlled_message_store_runtime_enabled": True,
            "jsonl_append_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
            "persona_capability_honesty_enabled": True,
            "persona_action_decline_enabled": True,
            "store_path_restricted_to_aura_runtime": True,
            "arbitrary_file_mutation_disabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "permission_runtime_disabled": True,
            "audit_runtime_disabled": True,
            "command_execution_disabled": True,
            "tool_execution_disabled": True,
            "desktop_control_disabled": True,
            "voice_runtime_disabled": True,
            "vision_runtime_disabled": True,
            "network_runtime_disabled": True,
            "control_center_runtime_disabled": True,
            "localhost_only_policy": True,
            "public_network_exposure_disabled": True,
            "external_access_disabled": True,
            "safe_idle_default": True,
            "controlled_store_write_contract": True,
            "release_gate_closed": True,
            "alpha_runtime_only": True,
            "manual_approval_required_for_future_model_runtime": True,
            "manual_approval_required_for_future_memory_runtime": True,
            "manual_approval_required_for_future_action_runtime": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def _packet(self, packet_type: str, target: str, items_key: str) -> dict[str, Any]:
        return {
            "type": packet_type,
            "target": target,
            "status": self.status_name,
            "version": self.version,
            "alpha_ready": True,
            "runtime_ready": False,
            "thin_runtime_alpha": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "blueprint_count": len(self.BLUEPRINTS[items_key]),
            "items": list(self.BLUEPRINTS[items_key]),
            "safety_boundary": self._common_boundary(),
            "runtime_counters": self._runtime_zero_map(),
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "note": "Sprint 164 adds deterministic AURA persona responses for local chat alpha. It does not use model runtime, memory runtime, command execution, arbitrary file mutation, desktop control, network access, or autonomous actions.",
        }

    def status(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "local_chat_persona_response_layer_ready": True,
            "local_chat_persona_response_layer_data_ready": True,
            "local_chat_persona_response_layer_status": self.status_name,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_persona_response_layer_blueprint_count": self._blueprint_count(),
            "release_gate_closed": True,
            "thin_runtime_alpha": True,
            "persona_response_layer_runtime_enabled": True,
            "controlled_message_store_runtime_enabled": True,
            "jsonl_append_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
            "persona_capability_honesty_enabled": True,
            "persona_action_decline_enabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "runtime_ready": False,
            "runtime_chat_sessions_created": 0,
            "runtime_chat_messages_accepted": 0,
            "runtime_chat_messages_persisted": 0,
            "runtime_aura_replies_generated": 0,
            "runtime_persona_responses_generated": 0,
            "runtime_persona_policy_checks": 0,
            "runtime_message_store_records_written": 0,
            "runtime_message_store_files_touched": 0,
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "next_sprint": "Sprint 165 — Model Adapter Boundary",
            "product_direction": "safe_local_chat_persona_before_model_adapter_runtime",
        }
        data.update(self._runtime_zero_map())
        data.update(self._runtime_false_map())
        return data

    def context(self) -> dict[str, Any]:
        return {
            "current_sprint": "164",
            "current_version": "0.164.0-genesis",
            "purpose": "Add a consistent AURA persona response layer for safe local CLI chat alpha.",
            "usable_alpha_commands": ["local-chat-persona-alpha <message>", "local-chat-persona-response-layer-status", "no-local-chat-persona-unsafe-runtime-plan"],
            "safe_current_capabilities": ["Accept one manual CLI message.", "Generate deterministic AURA persona response.", "Decline action requests honestly.", "Append controlled JSONL chat turn.", "Report persona and runtime boundary counters."],
            "disabled_capabilities": ["model_request_dispatch", "memory_write", "permission_mutation", "audit_write", "command_execution", "arbitrary_file_mutation", "desktop_control", "voice_input", "vision_capture", "network_request"],
            "safety_boundary": self._common_boundary(),
        }

    def _normalize_message(self, message: str) -> str:
        return " ".join(str(message or "").replace("\r", " ").replace("\n", " ").split())[:2000]

    def _is_action_request(self, message: str) -> bool:
        lowered = message.lower()
        action_markers = [
            "buka blender", "buka visual", "buka vscode", "open blender", "open vscode", "buat folder", "create folder",
            "jalankan", "run command", "hapus", "delete file", "ubah file", "edit file", "install", "download", "clone",
        ]
        return any(marker in lowered for marker in action_markers)

    def _persona_mode(self, message: str) -> str:
        lowered = message.lower()
        if not message:
            return "empty_message"
        if self._is_action_request(message):
            return "safe_action_decline"
        if any(term in lowered for term in ["siapa kamu", "kepribadian", "persona", "aura itu", "kamu siapa"]):
            return "identity_persona"
        if any(term in lowered for term in ["status", "aktif", "ready", "siap", "batas", "kemampuan"]):
            return "capability_status"
        if any(term in lowered for term in ["roadmap", "sprint", "genesis", "selanjutnya"]):
            return "roadmap_helper"
        return "supportive_chat"

    def generate_persona_response(self, message: str) -> tuple[str, str]:
        stripped = self._normalize_message(message)
        mode = self._persona_mode(stripped)
        if mode == "empty_message":
            return mode, "Pesan kosong. Kirim satu pesan teks agar aku bisa membalas dalam mode persona lokal AURA."
        if mode == "safe_action_decline":
            return mode, (
                "Aku paham permintaan aksi itu, tapi di Sprint 164 aku belum boleh membuka aplikasi, membuat folder, menjalankan command, "
                "atau mengubah file bebas. Aku hanya boleh membalas sebagai persona lokal AURA dan menyimpan turn chat ini ke store terkontrol. "
                "Aksi seperti buka Blender, buka VS Code, dan buat folder project dijadwalkan untuk block Local Action & Desktop Command Runtime sekitar Sprint 201-210."
            )
        if mode == "identity_persona":
            return mode, (
                "Aku AURA, partner AI lokal yang sedang dibangun bersama Kiput. Di mode ini aku berbicara dengan persona hangat, jujur, dan aman: "
                "aku bisa menerima pesan CLI, membalas secara lokal tanpa model, dan menjaga batas kemampuan dengan jelas."
            )
        if mode == "capability_status":
            return mode, (
                "Aku aktif dalam mode Local Chat Persona Response Alpha. Aku bisa menerima satu pesan manual, membalas dengan persona lokal AURA yang konsisten, "
                "dan menyimpan turn ke message store terkontrol. Model runtime, memory runtime, command execution, file mutation bebas, voice, vision, dan desktop action masih nonaktif."
            )
        if mode == "roadmap_helper":
            return mode, (
                "Arah roadmap saat ini adalah chat → memory → voice → vision → action. Sprint 164 memperkuat persona lokal; Sprint 165 berikutnya menyiapkan model adapter boundary tanpa langsung mengaktifkan model runtime."
            )
        return mode, (
            "Aku mendengar pesanmu. Dalam mode Sprint 164, aku akan menjawab dengan persona lokal AURA yang aman dan jujur, "
            "tanpa memanggil model, tanpa menulis memory runtime, tanpa menjalankan command, dan tanpa melakukan aksi desktop."
        )

    def run_persona_turn(self, message: str, *, source: str = "AuraCLI") -> dict[str, Any]:
        normalized = self._normalize_message(message)
        persona_mode, aura_response = self.generate_persona_response(normalized)
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        turn = LocalChatPersonaTurn(
            session_id=f"s164-{uuid4().hex[:12]}",
            message_id=f"msg-{uuid4().hex[:12]}",
            response_id=f"aura-{uuid4().hex[:12]}",
            store_record_id=f"persona-{uuid4().hex[:12]}",
            user_message=normalized,
            aura_response=aura_response,
            persona_mode=persona_mode,
            created_at=now,
            source=source,
        )
        record = {
            "record_id": turn.store_record_id,
            "schema_version": "aura.local_chat.persona_response.v1",
            "sprint": "164",
            "created_at": turn.created_at,
            "session_id": turn.session_id,
            "message_id": turn.message_id,
            "response_id": turn.response_id,
            "session_mode": turn.session_mode,
            "source": turn.source,
            "persona_mode": turn.persona_mode,
            "user_message": turn.user_message,
            "aura_response": turn.aura_response,
            "model_runtime": "disabled",
            "memory_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_mutation": "disabled",
            "runtime_execution_features": 0,
        }
        self.store_dir.mkdir(parents=True, exist_ok=True)
        with self.store_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
        counters = self._runtime_zero_map()
        counters.update({
            "runtime_chat_sessions_created": 1,
            "runtime_chat_messages_accepted": 1 if bool(normalized) else 0,
            "runtime_chat_messages_persisted": 2 if bool(normalized) else 0,
            "runtime_aura_replies_generated": 1,
            "runtime_persona_responses_generated": 1,
            "runtime_persona_policy_checks": 1,
            "runtime_message_store_records_written": 1,
            "runtime_message_store_files_touched": 1,
            "runtime_model_requests_dispatched": 0,
            "runtime_memory_writes": 0,
            "runtime_commands_executed": 0,
            "runtime_arbitrary_files_written": 0,
            "runtime_execution_features": 0,
        })
        return {
            "type": "local_chat_persona_response_turn",
            "status": self.status_name,
            "version": "0.164.0-genesis",
            "alpha_runtime": True,
            "session_id": turn.session_id,
            "message_id": turn.message_id,
            "response_id": turn.response_id,
            "store_record_id": turn.store_record_id,
            "created_at": turn.created_at,
            "session_mode": turn.session_mode,
            "source": turn.source,
            "persona_mode": turn.persona_mode,
            "store_file": str(self.store_file),
            "user_message": turn.user_message,
            "aura_response": turn.aura_response,
            "runtime_counters": counters,
            "safety_boundary": self._common_boundary(),
        }

    def render_persona_turn(self, message: str) -> str:
        packet = self.run_persona_turn(message)
        counters = packet["runtime_counters"]
        boundary = packet["safety_boundary"]
        lines = [
            "AURA Local Chat Persona Response Alpha",
            "======================================",
            "Version              : 0.164.0-genesis",
            f"Session ID           : {packet['session_id']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Persona Mode         : {packet['persona_mode']}",
            f"Store Record ID      : {packet['store_record_id']}",
            f"Store File           : {packet['store_file']}",
            f"Message Accepted     : {counters['runtime_chat_messages_accepted']}",
            f"Messages Persisted   : {counters['runtime_chat_messages_persisted']}",
            f"Persona Replies      : {counters['runtime_persona_responses_generated']}",
            f"Persona Policy Checks: {counters['runtime_persona_policy_checks']}",
            f"Store Records Written: {counters['runtime_message_store_records_written']}",
            f"Model Requests       : {counters['runtime_model_requests_dispatched']}",
            f"Memory Writes        : {counters['runtime_memory_writes']}",
            f"Commands Executed    : {counters['runtime_commands_executed']}",
            f"Arbitrary Files Wrote: {counters['runtime_arbitrary_files_written']}",
            f"Runtime Execution    : {counters['runtime_execution_features']}",
            f"Model Runtime        : {'disabled' if boundary['model_runtime_disabled'] else 'enabled'}",
            f"Memory Runtime       : {'disabled' if boundary['memory_runtime_disabled'] else 'enabled'}",
            f"Command Execution    : {'disabled' if boundary['command_execution_disabled'] else 'enabled'}",
            f"Arbitrary File Write : {'disabled' if boundary['arbitrary_file_mutation_disabled'] else 'enabled'}",
            "",
            f"User: {packet['user_message']}",
            f"AURA: {packet['aura_response']}",
        ]
        return "\n".join(lines)

    def local_chat_persona_response_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_persona_response_runtime_plan", target, "local_chat_persona_response_runtime_items")
    def aura_persona_style_contract_plan(self, target: str) -> dict[str, Any]: return self._packet("aura_persona_style_contract_plan", target, "aura_persona_style_contract_items")
    def persona_capability_honesty_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_capability_honesty_plan", target, "persona_capability_honesty_items")
    def persona_action_decline_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_action_decline_plan", target, "persona_action_decline_items")
    def persona_safety_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_safety_boundary_plan", target, "persona_safety_boundary_items")
    def persona_message_store_link_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_message_store_link_plan", target, "persona_message_store_link_items")
    def persona_model_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_model_boundary_plan", target, "persona_model_boundary_items")
    def persona_memory_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("persona_memory_boundary_plan", target, "persona_memory_boundary_items")
    def no_local_chat_persona_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("no_local_chat_persona_unsafe_runtime_plan", target, "no_local_chat_persona_unsafe_runtime_items")
    def local_chat_persona_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_persona_next_sprint_readiness_plan", target, "local_chat_persona_next_sprint_readiness_items")
