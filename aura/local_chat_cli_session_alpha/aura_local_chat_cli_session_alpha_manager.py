"""AURA Local Chat CLI Session Alpha.

Sprint 162.

This is the first safe thin runtime for local chat. It accepts one CLI message,
creates an in-memory/transient chat session packet, returns a deterministic AURA
persona response, and reports runtime counters for the alpha turn. It does not
persist chat history, dispatch model requests, write memory, mutate permissions,
write audit logs, execute commands/tools/plugin actions, mutate files, start
servers, open sockets, bind ports, use voice, capture screens, or perform
autonomous actions.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class LocalChatAlphaTurn:
    """A transient single-turn chat packet for Sprint 162."""

    session_id: str
    message_id: str
    response_id: str
    user_message: str
    aura_response: str
    created_at: str
    session_mode: str = "transient_cli_alpha"
    source: str = "AuraCLI"


class AuraLocalChatCliSessionAlphaManager:
    """Run and describe the Sprint 162 local chat CLI alpha."""

    name = "aura_local_chat_cli_session_alpha"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_cli_session_alpha_status",
        "local_chat_alpha_session_runtime_plan",
        "local_chat_alpha_message_acceptance_plan",
        "local_chat_alpha_persona_response_plan",
        "local_chat_alpha_transient_history_plan",
        "local_chat_alpha_command_safety_plan",
        "local_chat_alpha_model_runtime_boundary_plan",
        "local_chat_alpha_permission_audit_boundary_plan",
        "local_chat_alpha_cli_usage_plan",
        "no_local_chat_cli_alpha_unsafe_runtime_plan",
        "local_chat_cli_session_alpha_context",
        "local_chat_alpha_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "local_chat_alpha_session_runtime_items": [
            "transient_session_id_created", "session_created_at_recorded", "session_mode_cli_alpha_recorded", "session_state_safe_local_turn_recorded", "session_storage_disabled_marker_recorded",
            "session_project_root_context_recorded", "session_source_cli_recorded", "session_no_background_loop_recorded", "session_no_autonomous_turn_recorded", "session_exit_after_single_turn_recorded",
        ],
        "local_chat_alpha_message_acceptance_items": [
            "user_message_text_accepted", "message_trim_validation_applied", "empty_message_guard_defined", "message_id_created", "message_role_user_recorded",
            "message_source_cli_recorded", "message_timestamp_recorded", "message_runtime_counter_incremented", "message_no_file_write_confirmed", "message_no_command_parse_execution_confirmed",
        ],
        "local_chat_alpha_persona_response_items": [
            "aura_persona_response_generated", "local_mode_disclosure_included", "capability_limitation_included", "command_request_deflection_included", "model_runtime_disclosure_included",
            "memory_runtime_disclosure_included", "safe_next_step_hint_included", "indonesian_default_tone_supported", "response_id_created", "response_runtime_counter_incremented",
        ],
        "local_chat_alpha_transient_history_items": [
            "history_transient_only_defined", "message_history_write_disabled", "conversation_store_write_disabled", "memory_store_write_disabled", "jsonl_write_disabled",
            "sqlite_write_disabled", "audit_log_write_disabled", "history_view_handoff_to_sprint_163", "no_persistence_counter_zero", "manual_user_copy_allowed",
        ],
        "local_chat_alpha_command_safety_items": [
            "command_execution_disabled", "tool_execution_disabled", "plugin_action_dispatch_disabled", "desktop_control_disabled", "file_mutation_disabled",
            "app_launch_disabled", "folder_creation_disabled", "shell_command_disabled", "action_allowlist_deferred_to_201_210", "voice_to_action_deferred_to_209_plus",
        ],
        "local_chat_alpha_model_runtime_boundary_items": [
            "model_request_dispatch_disabled", "network_request_disabled", "local_model_provider_not_called", "remote_model_provider_not_called", "model_adapter_boundary_handoff_to_sprint_165",
            "permission_gate_handoff_to_sprint_166", "fallback_persona_response_used", "no_prompt_packet_sent", "no_response_packet_received", "model_counter_zero",
        ],
        "local_chat_alpha_permission_audit_boundary_items": [
            "permission_request_create_disabled", "permission_grant_apply_disabled", "permission_mutation_disabled", "audit_event_write_disabled", "audit_log_append_disabled",
            "audit_link_write_disabled", "manual_approval_language_preserved", "permission_panel_future_link_recorded", "audit_panel_future_link_recorded", "no_runtime_gate_opened",
        ],
        "local_chat_alpha_cli_usage_items": [
            "command_local_chat_alpha_defined", "command_local_chat_cli_alpha_status_defined", "command_no_runtime_plan_defined", "single_message_argument_supported", "quoted_message_supported",
            "safe_response_output_supported", "runtime_counter_output_supported", "no_interactive_loop_in_sprint_162", "sprint_163_message_store_handoff_defined", "sprint_164_persona_layer_handoff_defined",
        ],
        "no_local_chat_cli_alpha_unsafe_runtime_items": [
            "no_message_persistence_runtime", "no_model_runtime", "no_memory_runtime", "no_permission_mutation_runtime", "no_audit_write_runtime",
            "no_command_execution_runtime", "no_tool_execution_runtime", "no_file_mutation_runtime", "no_desktop_control_runtime", "no_network_runtime",
        ],
        "local_chat_alpha_next_sprint_readiness_items": [
            "sprint_163_local_chat_message_store_identified", "transient_session_packet_ready", "message_schema_runtime_observed", "safe_persona_response_observed", "history_persistence_still_deferred",
            "model_runtime_still_deferred", "memory_runtime_still_deferred", "action_runtime_still_deferred_to_201_210", "voice_runtime_still_deferred_to_181_190", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_chat_message_persist", "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_memory_write", "runtime_memory_read",
        "runtime_permission_request_create", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_audit_event_write", "runtime_audit_log_append",
        "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_file_read", "runtime_file_write",
        "runtime_file_modify", "runtime_file_delete", "runtime_desktop_control", "runtime_app_launch", "runtime_folder_create",
        "runtime_voice_input_start", "runtime_voice_output_start", "runtime_screen_capture_start", "runtime_network_request", "runtime_control_center_server_start",
        "runtime_http_listener_start", "runtime_socket_open", "runtime_port_binding", "runtime_background_loop_start", "runtime_autonomous_message_send",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_chat_messages_persisted", "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_memory_writes", "runtime_memory_reads",
        "runtime_permission_requests_created", "runtime_permission_grants_applied", "runtime_permission_mutations", "runtime_audit_events_written", "runtime_audit_logs_appended",
        "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_files_read", "runtime_files_written",
        "runtime_files_modified", "runtime_files_deleted", "runtime_desktop_control_actions", "runtime_apps_launched", "runtime_folders_created",
        "runtime_voice_inputs_started", "runtime_voice_outputs_started", "runtime_screen_captures_started", "runtime_network_requests", "runtime_control_center_servers_started",
        "runtime_http_listeners_started", "runtime_ports_bound", "runtime_background_loops_started", "runtime_autonomous_messages_sent", "runtime_execution_features",
    ]

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or ".").resolve()

    def _blueprint_count(self) -> int:
        return sum(len(items) for items in self.BLUEPRINTS.values())

    def _runtime_zero_map(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def _runtime_false_map(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _common_boundary(self) -> dict[str, Any]:
        boundary: dict[str, Any] = {
            "local_chat_cli_session_alpha_only": True,
            "thin_runtime_alpha": True,
            "single_turn_cli_alpha": True,
            "transient_session_only": True,
            "safe_persona_response_only": True,
            "local_chat_cli_alpha_runtime_enabled": True,
            "transient_chat_session_runtime_enabled": True,
            "message_acceptance_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
            "interactive_loop_runtime_disabled": True,
            "message_persistence_runtime_disabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "permission_runtime_disabled": True,
            "audit_runtime_disabled": True,
            "command_execution_disabled": True,
            "tool_execution_disabled": True,
            "file_mutation_disabled": True,
            "desktop_control_disabled": True,
            "voice_runtime_disabled": True,
            "vision_runtime_disabled": True,
            "network_runtime_disabled": True,
            "control_center_runtime_disabled": True,
            "localhost_only_policy": True,
            "public_network_exposure_disabled": True,
            "external_access_disabled": True,
            "safe_idle_default": True,
            "read_only_metadata_contract": True,
            "manual_user_message_required": True,
            "release_gate_closed": True,
            "foundation_only": False,
            "alpha_runtime_only": True,
            "manual_approval_required_for_future_model_runtime": True,
            "manual_approval_required_for_future_message_persistence": True,
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
            "note": "Sprint 162 enables a safe transient one-turn CLI chat alpha. It does not persist history, dispatch model requests, write memory/audit, execute commands, mutate files, launch apps, start servers, bind ports, or perform autonomous actions.",
        }

    def status(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "local_chat_cli_session_alpha_ready": True,
            "local_chat_cli_session_alpha_data_ready": True,
            "local_chat_cli_session_alpha_status": self.status_name,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_cli_session_alpha_blueprint_count": self._blueprint_count(),
            "release_gate_closed": True,
            "thin_runtime_alpha": True,
            "local_chat_cli_alpha_runtime_enabled": True,
            "transient_chat_session_runtime_enabled": True,
            "message_acceptance_runtime_enabled": True,
            "safe_persona_reply_runtime_enabled": True,
            "interactive_loop_runtime_disabled": True,
            "message_persistence_runtime_disabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "command_execution_disabled": True,
            "file_mutation_disabled": True,
            "runtime_ready": False,
            "runtime_chat_sessions_created": 0,
            "runtime_chat_messages_accepted": 0,
            "runtime_aura_replies_generated": 0,
            "next_sprint": "Sprint 163 — Local Chat Message Store",
            "product_direction": "safe_local_chat_cli_alpha_first_usable_turn",
        }
        data.update(self._runtime_zero_map())
        data.update(self._runtime_false_map())
        return data

    def context(self) -> dict[str, Any]:
        return {
            "status": self.status_name,
            "context_ready": True,
            "project_root": str(self.project_root),
            "sprint": "162",
            "block": "Sprint 161-170 — Local Chat Runtime",
            "goal": "Provide a safe one-turn CLI chat alpha before message persistence and model runtime.",
            "usable_alpha_commands": ["local-chat-alpha <message>", "local-chat-cli-session-alpha-status", "no-local-chat-cli-alpha-unsafe-runtime-plan"],
            "safe_current_capabilities": ["Accept one manual CLI message.", "Create transient in-memory session packet.", "Return deterministic safe AURA persona response.", "Report runtime counters for the alpha turn.", "Refuse/deflect command and file mutation requests."],
            "disabled_capabilities": ["message_persistence", "model_request_dispatch", "memory_write", "permission_mutation", "audit_write", "command_execution", "file_mutation", "desktop_control", "voice_input", "vision_capture", "network_request"],
            "safety_boundary": self._common_boundary(),
        }

    def _is_action_request(self, message: str) -> bool:
        lowered = message.lower()
        action_markers = [
            "buka blender", "buka visual", "buka vscode", "open blender", "open vscode", "buat folder", "create folder",
            "jalankan", "run command", "hapus", "delete file", "ubah file", "edit file", "install", "download", "clone",
        ]
        return any(marker in lowered for marker in action_markers)

    def _detect_language(self, message: str) -> str:
        lowered = message.lower()
        if any(word in lowered for word in ["apa", "bagaimana", "buka", "buat", "status", "kamu", "aura", "lanjut"]):
            return "id"
        if any(word in lowered for word in ["what", "how", "open", "create", "status", "hello"]):
            return "en"
        return "id"

    def generate_safe_persona_response(self, message: str) -> str:
        language = self._detect_language(message)
        stripped = message.strip()

        if not stripped:
            return "Pesan kosong. Kirim satu pesan teks agar aku bisa merespons dalam Local Chat CLI Alpha."

        if self._is_action_request(stripped):
            if language == "en":
                return (
                    "I heard the request, but in Sprint 162 I cannot open apps, create folders, run commands, "
                    "or modify files yet. I am active only as a safe local CLI chat alpha. Those actions are planned "
                    "later for the Local Action & Desktop Command Runtime block with permission and audit gates."
                )
            return (
                "Aku menangkap permintaan itu, tapi di Sprint 162 aku belum boleh membuka aplikasi, membuat folder, "
                "menjalankan command, atau mengubah file. Saat ini aku hanya aktif sebagai Local Chat CLI Alpha yang aman. "
                "Aksi seperti itu nanti masuk block Local Action & Desktop Command Runtime dengan permission dan audit gate."
            )

        if any(word in stripped.lower() for word in ["status", "aktif", "ready", "siap"]):
            return (
                "Aku aktif dalam mode Local Chat CLI Alpha. Aku bisa menerima satu pesan manual dan membalas dengan persona lokal aman. "
                "Model runtime, memory write, command execution, file mutation, voice, vision, dan desktop action masih nonaktif."
            )

        if language == "en":
            return (
                "I am AURA in Local Chat CLI Alpha mode. I can respond safely to this single local CLI message, "
                "but I do not use model runtime, memory persistence, commands, file mutation, voice, vision, or desktop control yet."
            )

        return (
            "Aku AURA dalam mode Local Chat CLI Alpha. Aku bisa membalas pesan lokal ini secara aman, "
            "tetapi belum memakai model runtime, belum menyimpan memori, belum menjalankan command, belum mengubah file, "
            "dan belum mengontrol desktop."
        )

    def run_alpha_turn(self, message: str, *, source: str = "AuraCLI") -> dict[str, Any]:
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        turn = LocalChatAlphaTurn(
            session_id=f"s162-{uuid4().hex[:12]}",
            message_id=f"msg-{uuid4().hex[:12]}",
            response_id=f"aura-{uuid4().hex[:12]}",
            user_message=message.strip(),
            aura_response=self.generate_safe_persona_response(message),
            created_at=now,
            source=source,
        )
        counters = self._runtime_zero_map()
        counters.update({
            "runtime_chat_sessions_created": 1,
            "runtime_chat_messages_accepted": 1 if bool(message.strip()) else 0,
            "runtime_aura_replies_generated": 1,
            "runtime_chat_messages_persisted": 0,
            "runtime_model_requests_dispatched": 0,
            "runtime_memory_writes": 0,
            "runtime_commands_executed": 0,
            "runtime_files_written": 0,
            "runtime_execution_features": 0,
        })
        return {
            "type": "local_chat_alpha_turn",
            "status": self.status_name,
            "version": self.version,
            "alpha_runtime": True,
            "session_id": turn.session_id,
            "message_id": turn.message_id,
            "response_id": turn.response_id,
            "created_at": turn.created_at,
            "session_mode": turn.session_mode,
            "source": turn.source,
            "user_message": turn.user_message,
            "aura_response": turn.aura_response,
            "runtime_counters": counters,
            "safety_boundary": self._common_boundary(),
        }

    def render_alpha_turn(self, message: str) -> str:
        packet = self.run_alpha_turn(message)
        counters = packet["runtime_counters"]
        boundary = packet["safety_boundary"]
        lines = [
            "AURA Local Chat CLI Alpha",
            "===========================",
            f"Version              : 0.162.0-genesis",
            f"Session ID           : {packet['session_id']}",
            f"Session Mode         : {packet['session_mode']}",
            f"Message Accepted     : {counters['runtime_chat_messages_accepted']}",
            f"Aura Replies         : {counters['runtime_aura_replies_generated']}",
            f"Messages Persisted   : {counters['runtime_chat_messages_persisted']}",
            f"Model Requests       : {counters['runtime_model_requests_dispatched']}",
            f"Commands Executed    : {counters['runtime_commands_executed']}",
            f"Files Written        : {counters['runtime_files_written']}",
            f"Runtime Execution    : {counters['runtime_execution_features']}",
            f"Model Runtime        : {'disabled' if boundary['model_runtime_disabled'] else 'enabled'}",
            f"Memory Runtime       : {'disabled' if boundary['memory_runtime_disabled'] else 'enabled'}",
            f"Command Execution    : {'disabled' if boundary['command_execution_disabled'] else 'enabled'}",
            f"File Mutation        : {'disabled' if boundary['file_mutation_disabled'] else 'enabled'}",
            "",
            f"User: {packet['user_message']}",
            f"AURA: {packet['aura_response']}",
        ]
        return "\n".join(lines)

    def local_chat_alpha_session_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_session_runtime_plan", target, "local_chat_alpha_session_runtime_items")
    def local_chat_alpha_message_acceptance_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_message_acceptance_plan", target, "local_chat_alpha_message_acceptance_items")
    def local_chat_alpha_persona_response_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_persona_response_plan", target, "local_chat_alpha_persona_response_items")
    def local_chat_alpha_transient_history_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_transient_history_plan", target, "local_chat_alpha_transient_history_items")
    def local_chat_alpha_command_safety_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_command_safety_plan", target, "local_chat_alpha_command_safety_items")
    def local_chat_alpha_model_runtime_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_model_runtime_boundary_plan", target, "local_chat_alpha_model_runtime_boundary_items")
    def local_chat_alpha_permission_audit_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_permission_audit_boundary_plan", target, "local_chat_alpha_permission_audit_boundary_items")
    def local_chat_alpha_cli_usage_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_cli_usage_plan", target, "local_chat_alpha_cli_usage_items")
    def no_local_chat_cli_alpha_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("no_local_chat_cli_alpha_unsafe_runtime_plan", target, "no_local_chat_cli_alpha_unsafe_runtime_items")
    def local_chat_alpha_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_alpha_next_sprint_readiness_plan", target, "local_chat_alpha_next_sprint_readiness_items")
