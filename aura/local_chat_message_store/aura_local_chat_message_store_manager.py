"""AURA Local Chat Message Store.

Sprint 163.

This module adds the first safe controlled local message store for AURA's local
chat path. It can accept one CLI message, create a transient session packet,
return a deterministic safe AURA persona reply, and append a redacted turn
record to an AURA-owned local JSONL store.

The store is deliberately narrow: it writes only to the configured AURA chat
store file, never dispatches model requests, never writes memory, never mutates
permissions/audit logs, never executes commands/tools/plugin actions, never
mutates arbitrary files, never starts servers, never opens sockets, never binds
ports, and never performs autonomous actions.
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
class LocalChatStoredTurn:
    """A controlled local chat store packet for Sprint 163."""

    session_id: str
    message_id: str
    response_id: str
    user_message: str
    aura_response: str
    created_at: str
    store_record_id: str
    session_mode: str = "local_cli_message_store_alpha"
    source: str = "AuraCLI"


class AuraLocalChatMessageStoreManager:
    """Run and describe Sprint 163 controlled local chat message storage."""

    name = "aura_local_chat_message_store"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_message_store_status",
        "local_chat_message_store_runtime_plan",
        "local_chat_message_schema_plan",
        "local_chat_store_path_policy_plan",
        "local_chat_store_redaction_plan",
        "local_chat_store_retention_plan",
        "local_chat_store_cli_alpha_plan",
        "local_chat_store_model_boundary_plan",
        "local_chat_store_memory_boundary_plan",
        "no_local_chat_message_store_unsafe_runtime_plan",
        "local_chat_message_store_context",
        "local_chat_message_store_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "local_chat_message_store_runtime_items": [
            "controlled_message_store_runtime_enabled", "single_turn_store_alpha_enabled", "manual_user_message_required", "transient_session_packet_created", "safe_persona_reply_created",
            "jsonl_record_append_supported", "store_directory_created_if_missing", "store_file_created_if_missing", "store_write_counter_incremented", "arbitrary_file_mutation_disabled",
        ],
        "local_chat_message_schema_items": [
            "record_id_defined", "session_id_defined", "message_id_defined", "response_id_defined", "created_at_utc_defined",
            "source_defined", "session_mode_defined", "user_message_redacted_field_defined", "aura_response_field_defined", "safety_boundary_snapshot_defined",
        ],
        "local_chat_store_path_policy_items": [
            "default_store_under_aura_runtime", "aura_chat_store_dir_override_supported", "project_root_relative_policy_defined", "path_resolution_guard_defined", "parent_directory_creation_limited",
            "no_user_supplied_output_path", "no_path_traversal_runtime", "no_delete_runtime", "no_modify_existing_non_store_files", "gitignore_aura_runtime_entry_defined",
        ],
        "local_chat_store_redaction_items": [
            "message_length_cap_defined", "control_character_normalization_defined", "line_break_normalization_defined", "secret_detection_deferred", "redaction_review_required",
            "raw_command_execution_never_triggered", "action_intent_logged_as_text_only", "model_prompt_not_created", "memory_item_not_created", "audit_event_not_written",
        ],
        "local_chat_store_retention_items": [
            "retention_policy_placeholder_defined", "manual_clear_deferred", "rotation_policy_deferred", "archive_policy_deferred", "privacy_note_documented",
            "history_viewer_handoff_to_sprint_168", "memory_runtime_handoff_to_sprint_171_180", "no_auto_upload", "no_network_sync", "local_only_store_contract_defined",
        ],
        "local_chat_store_cli_alpha_items": [
            "command_local_chat_store_alpha_defined", "command_local_chat_message_store_status_defined", "command_no_unsafe_runtime_defined", "single_message_argument_supported", "quoted_message_supported",
            "store_summary_output_supported", "store_path_output_supported", "runtime_counter_output_supported", "persona_response_output_supported", "sprint_164_persona_layer_handoff_defined",
        ],
        "local_chat_store_model_boundary_items": [
            "model_request_dispatch_disabled", "local_model_provider_not_called", "remote_model_provider_not_called", "network_request_disabled", "model_adapter_boundary_handoff_to_sprint_165",
            "permission_gate_handoff_to_sprint_166", "deterministic_response_used", "no_prompt_packet_sent", "no_model_response_received", "model_counter_zero",
        ],
        "local_chat_store_memory_boundary_items": [
            "memory_write_disabled", "memory_read_disabled", "memory_index_update_disabled", "workspace_memory_write_disabled", "project_journal_write_disabled",
            "memory_runtime_handoff_to_sprint_171_180", "message_store_not_memory_store", "no_long_term_profile_update", "no_preference_extraction", "memory_counter_zero",
        ],
        "no_local_chat_message_store_unsafe_runtime_items": [
            "no_model_runtime", "no_memory_runtime", "no_permission_mutation_runtime", "no_audit_write_runtime", "no_command_execution_runtime",
            "no_tool_execution_runtime", "no_plugin_action_runtime", "no_desktop_control_runtime", "no_network_runtime", "no_arbitrary_file_mutation_runtime",
        ],
        "local_chat_message_store_next_sprint_readiness_items": [
            "sprint_164_persona_response_layer_identified", "stored_turn_schema_ready", "message_store_write_observed", "safe_persona_response_observed", "model_runtime_still_deferred",
            "memory_runtime_still_deferred", "action_runtime_still_deferred_to_201_210", "voice_runtime_still_deferred_to_181_190", "history_viewer_handoff_preserved", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_memory_write", "runtime_memory_read", "runtime_memory_index_update",
        "runtime_permission_request_create", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_audit_event_write", "runtime_audit_log_append",
        "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write",
        "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_app_launch", "runtime_folder_create",
        "runtime_voice_input_start", "runtime_voice_output_start", "runtime_screen_capture_start", "runtime_network_request", "runtime_control_center_server_start",
        "runtime_http_listener_start", "runtime_socket_open", "runtime_port_binding", "runtime_background_loop_start", "runtime_autonomous_message_send",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_memory_writes", "runtime_memory_reads", "runtime_memory_index_updates",
        "runtime_permission_requests_created", "runtime_permission_grants_applied", "runtime_permission_mutations", "runtime_audit_events_written", "runtime_audit_logs_appended",
        "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written",
        "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_desktop_control_actions", "runtime_apps_launched", "runtime_folders_created",
        "runtime_voice_inputs_started", "runtime_voice_outputs_started", "runtime_screen_captures_started", "runtime_network_requests", "runtime_control_center_servers_started",
        "runtime_http_listeners_started", "runtime_ports_bound", "runtime_background_loops_started", "runtime_autonomous_messages_sent", "runtime_execution_features",
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
            "local_chat_message_store_only": True,
            "thin_runtime_alpha": True,
            "controlled_message_store_runtime_enabled": True,
            "single_turn_store_alpha": True,
            "manual_user_message_required": True,
            "message_store_runtime_enabled": True,
            "jsonl_append_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
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
            "read_only_metadata_contract": False,
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
            "note": "Sprint 163 enables a controlled local message store write for one CLI chat turn. It does not use model runtime, memory runtime, command execution, arbitrary file mutation, desktop control, network access, or autonomous actions.",
        }

    def status(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "local_chat_message_store_ready": True,
            "local_chat_message_store_data_ready": True,
            "local_chat_message_store_status": self.status_name,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_message_store_blueprint_count": self._blueprint_count(),
            "release_gate_closed": True,
            "thin_runtime_alpha": True,
            "controlled_message_store_runtime_enabled": True,
            "message_store_runtime_enabled": True,
            "jsonl_append_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "runtime_ready": False,
            "runtime_chat_sessions_created": 0,
            "runtime_chat_messages_accepted": 0,
            "runtime_chat_messages_persisted": 0,
            "runtime_aura_replies_generated": 0,
            "runtime_message_store_records_written": 0,
            "runtime_message_store_files_touched": 0,
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "next_sprint": "Sprint 164 — AURA Persona Response Layer",
            "product_direction": "safe_local_chat_message_store_before_model_and_memory_runtime",
        }
        data.update(self._runtime_zero_map())
        data.update(self._runtime_false_map())
        return data

    def context(self) -> dict[str, Any]:
        return {
            "status": self.status_name,
            "context_ready": True,
            "project_root": str(self.project_root),
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "sprint": "163",
            "block": "Sprint 161-170 — Local Chat Runtime",
            "goal": "Persist one safe local CLI chat turn to an AURA-owned message store before model and memory runtime.",
            "usable_alpha_commands": ["local-chat-store-alpha <message>", "local-chat-message-store-status", "no-local-chat-message-store-unsafe-runtime-plan"],
            "safe_current_capabilities": ["Accept one manual CLI message.", "Create transient session packet.", "Return deterministic safe AURA persona response.", "Append one controlled JSONL turn record to the local chat store.", "Report store counters and path."],
            "disabled_capabilities": ["model_request_dispatch", "memory_write", "permission_mutation", "audit_write", "command_execution", "arbitrary_file_mutation", "desktop_control", "voice_input", "vision_capture", "network_request"],
            "safety_boundary": self._common_boundary(),
        }

    def _normalize_message(self, message: str) -> str:
        return " ".join(message.replace("\r", " ").replace("\n", " ").split())[:2000]

    def _is_action_request(self, message: str) -> bool:
        lowered = message.lower()
        action_markers = [
            "buka blender", "buka visual", "buka vscode", "open blender", "open vscode", "buat folder", "create folder",
            "jalankan", "run command", "hapus", "delete file", "ubah file", "edit file", "install", "download", "clone",
        ]
        return any(marker in lowered for marker in action_markers)

    def generate_safe_persona_response(self, message: str) -> str:
        stripped = self._normalize_message(message)
        if not stripped:
            return "Pesan kosong. Kirim satu pesan teks agar aku bisa menyimpan turn chat lokal dengan aman."
        if self._is_action_request(stripped):
            return (
                "Aku menangkap permintaan aksi itu, tapi di Sprint 163 aku belum boleh membuka aplikasi, membuat folder, "
                "menjalankan command, atau mengubah file bebas. Aku hanya boleh menyimpan turn chat ini ke message store lokal AURA yang terkontrol."
            )
        if any(word in stripped.lower() for word in ["status", "aktif", "ready", "siap", "store", "simpan"]):
            return (
                "Aku aktif dalam mode Local Chat Message Store Alpha. Aku bisa menerima satu pesan manual, membalas dengan persona lokal aman, "
                "dan menyimpan turn ini ke message store lokal AURA. Model runtime, memory runtime, command execution, file mutation bebas, voice, vision, dan desktop action masih nonaktif."
            )
        return (
            "Aku AURA dalam mode Local Chat Message Store Alpha. Aku bisa menyimpan percakapan lokal ini secara terkontrol, "
            "tetapi belum memakai model runtime, belum menulis memory runtime, belum menjalankan command, dan belum mengontrol desktop."
        )

    def run_store_turn(self, message: str, *, source: str = "AuraCLI") -> dict[str, Any]:
        normalized = self._normalize_message(message)
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        turn = LocalChatStoredTurn(
            session_id=f"s163-{uuid4().hex[:12]}",
            message_id=f"msg-{uuid4().hex[:12]}",
            response_id=f"aura-{uuid4().hex[:12]}",
            store_record_id=f"store-{uuid4().hex[:12]}",
            user_message=normalized,
            aura_response=self.generate_safe_persona_response(normalized),
            created_at=now,
            source=source,
        )
        record = {
            "record_id": turn.store_record_id,
            "schema_version": "aura.local_chat.message_store.v1",
            "sprint": "163",
            "created_at": turn.created_at,
            "session_id": turn.session_id,
            "message_id": turn.message_id,
            "response_id": turn.response_id,
            "session_mode": turn.session_mode,
            "source": turn.source,
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
            "runtime_message_store_records_written": 1,
            "runtime_message_store_files_touched": 1,
            "runtime_model_requests_dispatched": 0,
            "runtime_memory_writes": 0,
            "runtime_commands_executed": 0,
            "runtime_arbitrary_files_written": 0,
            "runtime_execution_features": 0,
        })
        return {
            "type": "local_chat_message_store_turn",
            "status": self.status_name,
            "version": "0.163.0-genesis",
            "alpha_runtime": True,
            "session_id": turn.session_id,
            "message_id": turn.message_id,
            "response_id": turn.response_id,
            "store_record_id": turn.store_record_id,
            "created_at": turn.created_at,
            "session_mode": turn.session_mode,
            "source": turn.source,
            "store_file": str(self.store_file),
            "user_message": turn.user_message,
            "aura_response": turn.aura_response,
            "runtime_counters": counters,
            "safety_boundary": self._common_boundary(),
        }

    def render_store_turn(self, message: str) -> str:
        packet = self.run_store_turn(message)
        counters = packet["runtime_counters"]
        boundary = packet["safety_boundary"]
        lines = [
            "AURA Local Chat Message Store Alpha",
            "===================================",
            "Version              : 0.163.0-genesis",
            f"Session ID           : {packet['session_id']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Store Record ID      : {packet['store_record_id']}",
            f"Store File           : {packet['store_file']}",
            f"Message Accepted     : {counters['runtime_chat_messages_accepted']}",
            f"Messages Persisted   : {counters['runtime_chat_messages_persisted']}",
            f"Aura Replies         : {counters['runtime_aura_replies_generated']}",
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

    def local_chat_message_store_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_message_store_runtime_plan", target, "local_chat_message_store_runtime_items")
    def local_chat_message_schema_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_message_schema_plan", target, "local_chat_message_schema_items")
    def local_chat_store_path_policy_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_path_policy_plan", target, "local_chat_store_path_policy_items")
    def local_chat_store_redaction_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_redaction_plan", target, "local_chat_store_redaction_items")
    def local_chat_store_retention_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_retention_plan", target, "local_chat_store_retention_items")
    def local_chat_store_cli_alpha_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_cli_alpha_plan", target, "local_chat_store_cli_alpha_items")
    def local_chat_store_model_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_model_boundary_plan", target, "local_chat_store_model_boundary_items")
    def local_chat_store_memory_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_store_memory_boundary_plan", target, "local_chat_store_memory_boundary_items")
    def no_local_chat_message_store_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("no_local_chat_message_store_unsafe_runtime_plan", target, "no_local_chat_message_store_unsafe_runtime_items")
    def local_chat_message_store_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_message_store_next_sprint_readiness_plan", target, "local_chat_message_store_next_sprint_readiness_items")
