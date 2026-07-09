"""AURA Local Chat History Viewer Contract.

Sprint 168.

This module adds a read-only viewer contract for AURA's local chat message store.
It can inspect the controlled AURA-owned JSONL chat store and display a limited
summary of recent turns. It does not accept arbitrary paths and does not mutate
the store.

No model provider is called. No web search is performed. No network request is
sent. No credential is read. No permission grant is created or applied. No memory
item is written. No audit event is written. No command/tool/plugin action is
executed. No arbitrary file path is read or mutated. No autonomous loop is
started.
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
class LocalChatHistoryViewPacket:
    """Read-only local chat history view packet for Sprint 168."""

    packet_id: str
    store_file: str
    store_exists: bool
    records_read: int
    turns_displayed: int
    messages_viewed: int
    created_at: str
    session_mode: str = "local_cli_chat_history_viewer_alpha"
    source: str = "AuraCLI"


class AuraLocalChatHistoryViewerContractManager:
    """Describe and run Sprint 168 read-only chat history viewer alpha."""

    name = "aura_local_chat_history_viewer_contract"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_history_viewer_contract_status",
        "chat_history_viewer_runtime_plan",
        "chat_history_store_read_policy_plan",
        "chat_history_schema_reader_plan",
        "chat_history_summary_renderer_plan",
        "chat_history_privacy_redaction_plan",
        "chat_history_pagination_contract_plan",
        "chat_history_safety_boundary_plan",
        "chat_history_control_center_handoff_plan",
        "no_local_chat_history_viewer_unsafe_runtime_plan",
        "local_chat_history_viewer_context",
        "local_chat_history_viewer_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "history_viewer_runtime_items": [
            "read_only_history_viewer_enabled", "manual_cli_history_view_required", "controlled_store_path_only", "jsonl_recent_turn_scan_supported", "bounded_record_limit_defined",
            "history_summary_packet_created", "no_store_mutation", "no_history_delete", "no_history_export", "thin_runtime_alpha_only",
        ],
        "store_read_policy_items": [
            "default_store_under_aura_runtime", "aura_chat_store_dir_override_supported", "store_file_name_fixed_messages_jsonl", "no_user_supplied_path", "path_traversal_blocked",
            "arbitrary_file_read_disabled", "controlled_message_store_read_allowed", "missing_store_handled_safely", "malformed_jsonl_skipped", "read_errors_reported_as_safe_summary",
        ],
        "schema_reader_items": [
            "schema_version_detected", "record_id_read", "created_at_read", "session_id_read", "message_id_read",
            "response_id_read", "user_message_preview_read", "aura_response_preview_read", "session_mode_read", "runtime_boundary_snapshot_ignored_for_actions",
        ],
        "summary_renderer_items": [
            "record_count_reported", "turn_count_reported", "message_count_reported", "latest_created_at_reported", "store_file_reported",
            "store_exists_reported", "empty_store_summary_supported", "recent_turn_preview_limited", "long_text_preview_clamped", "human_readable_cli_output",
        ],
        "privacy_redaction_items": [
            "preview_length_cap_defined", "line_breaks_normalized", "control_characters_removed", "no_secret_extraction", "no_profile_extraction",
            "no_memory_item_creation", "no_prompt_reconstruction_for_model", "no_hidden_upload", "no_background_indexing", "future_redaction_review_required",
        ],
        "pagination_contract_items": [
            "default_limit_three", "max_limit_ten", "negative_limit_blocked", "offset_deferred", "sort_latest_first",
            "pagination_token_deferred", "control_center_page_contract_ready", "history_filter_deferred", "session_filter_deferred", "search_deferred",
        ],
        "safety_boundary_items": [
            "model_request_dispatch_disabled", "model_response_runtime_disabled", "network_runtime_disabled", "credential_runtime_disabled", "permission_grant_runtime_disabled",
            "memory_write_disabled", "audit_write_disabled", "command_execution_disabled", "arbitrary_file_write_disabled", "desktop_action_disabled",
        ],
        "control_center_handoff_items": [
            "read_only_panel_contract_ready", "chat_history_card_ready", "store_status_card_ready", "recent_turns_table_ready", "no_delete_button_runtime",
            "no_export_button_runtime", "no_model_replay_button_runtime", "no_memory_promote_button_runtime", "viewer_route_deferred", "sprint_169_integration_review_ready",
        ],
        "no_history_viewer_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_network_request", "no_credential_read", "no_permission_grant_apply",
            "no_memory_write", "no_audit_write", "no_command_execution", "no_arbitrary_file_read", "no_arbitrary_file_write",
        ],
        "next_sprint_readiness_items": [
            "sprint_169_local_chat_integration_review_identified", "history_viewer_contract_ready", "message_store_read_path_ready", "safety_uncertainty_handoff_preserved", "permission_gate_handoff_preserved",
            "model_runtime_still_disabled", "memory_runtime_still_disabled", "history_viewer_no_mutation_confirmed", "control_center_handoff_ready", "genesis_final_alignment_confirmed",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_memory_write", "runtime_audit_event_write",
        "runtime_audit_log_append", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_background_loop_start",
        "runtime_autonomous_message_send", "runtime_voice_input_start", "runtime_screen_capture_start", "runtime_control_center_server_start", "runtime_history_delete",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_history_store_reads", "runtime_history_records_read", "runtime_history_turns_displayed", "runtime_history_messages_viewed", "runtime_history_summaries_rendered",
        "runtime_message_store_records_written", "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read",
        "runtime_permission_grants_applied", "runtime_memory_writes", "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed",
        "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted",
        "runtime_execution_features",
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

    def _boundary(self) -> dict[str, Any]:
        boundary: dict[str, Any] = {
            "local_chat_history_viewer_contract_only": True,
            "thin_runtime_alpha": True,
            "chat_history_viewer_contract_enabled": True,
            "controlled_message_store_read_runtime_enabled": True,
            "read_only_history_view_runtime_enabled": True,
            "history_summary_runtime_enabled": True,
            "message_store_write_runtime_disabled": True,
            "model_request_dispatch_blocked_without_grant": True,
            "model_request_dispatch_disabled": True,
            "model_response_runtime_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "permission_grant_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "audit_write_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_read_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "desktop_action_disabled": True,
            "release_gate_closed": True,
            "sprint_169_integration_review_required": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "module": self.name,
            "version": "0.168.0-genesis",
            "status": self.status_name,
            "local_chat_history_viewer_contract_ready": True,
            "local_chat_history_viewer_contract_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_history_viewer_contract_blueprint_count": self._blueprint_count(),
            "release_gate_closed": True,
            "thin_runtime_alpha": True,
            "chat_history_viewer_contract_enabled": True,
            "controlled_message_store_read_runtime_enabled": True,
            "read_only_history_view_runtime_enabled": True,
            "history_summary_runtime_enabled": True,
            "message_store_write_runtime_disabled": True,
            "model_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_read_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "next_sprint": "Sprint 169 — Local Chat Integration Review",
        }
        data.update(self._runtime_zero_map())
        data.update(self._boundary())
        return data

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.168.0-genesis",
            "status": self.status_name,
            "context_ready": True,
            "project_root": str(self.project_root),
            "store_dir": str(self.store_dir),
            "store_file": str(self.store_file),
            "sprint": "168",
            "block": "Sprint 161-170 — Local Chat Runtime",
            "goal": "Read-only inspection of controlled local chat message history before integration review.",
            "usable_alpha_commands": ["local-chat-history-alpha", "local-chat-history-viewer-contract-status", "no-local-chat-history-viewer-unsafe-runtime-plan"],
            "safe_current_capabilities": ["Read the controlled AURA message store path.", "Summarize recent chat turns.", "Clamp preview text.", "Report empty/missing store safely."],
            "disabled_capabilities": ["model_request_dispatch", "network_request", "credential_read", "permission_grant", "memory_write", "audit_write", "command_execution", "arbitrary_file_read", "arbitrary_file_mutation", "desktop_action"],
            "safety_boundary": self._boundary(),
        }

    def _packet(self, packet_type: str, target: str, items_key: str) -> dict[str, Any]:
        data = {
            "type": packet_type,
            "target": target,
            "status": self.status_name,
            "version": "0.168.0-genesis",
            "alpha_ready": True,
            "runtime_ready": False,
            "thin_runtime_alpha": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "blueprint_count": len(self.BLUEPRINTS[items_key]),
            "items": list(self.BLUEPRINTS[items_key]),
            "store_file": str(self.store_file),
            "safety_boundary": self._boundary(),
            "runtime_counters": self._runtime_zero_map(),
        }
        return data

    def _preview(self, value: Any, limit: int = 120) -> str:
        text = " ".join(str(value or "").replace("\r", " ").replace("\n", " ").split())
        if len(text) > limit:
            return text[: limit - 3] + "..."
        return text

    def _parse_limit(self, value: str | None) -> int:
        if not value:
            return 3
        try:
            limit = int(value)
        except ValueError:
            return 3
        return max(1, min(limit, 10))

    def _read_records(self, limit: int) -> list[dict[str, Any]]:
        if not self.store_file.exists():
            return []
        records: list[dict[str, Any]] = []
        try:
            with self.store_file.open("r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        item = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(item, dict):
                        records.append(item)
        except OSError:
            return []
        records = sorted(records, key=lambda r: str(r.get("created_at", "")), reverse=True)
        return records[:limit]

    def view_history(self, limit_text: str | None = None) -> dict[str, Any]:
        limit = self._parse_limit(limit_text)
        now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        records = self._read_records(limit)
        turns: list[dict[str, str]] = []
        for record in records:
            turns.append({
                "record_id": self._preview(record.get("record_id"), 40),
                "created_at": self._preview(record.get("created_at"), 40),
                "session_id": self._preview(record.get("session_id"), 40),
                "user_message": self._preview(record.get("user_message"), 120),
                "aura_response": self._preview(record.get("aura_response"), 120),
            })
        counters = self._runtime_zero_map()
        counters.update({
            "runtime_history_store_reads": 1,
            "runtime_history_records_read": len(records),
            "runtime_history_turns_displayed": len(turns),
            "runtime_history_messages_viewed": len(turns) * 2,
            "runtime_history_summaries_rendered": 1,
            "runtime_message_store_records_written": 0,
            "runtime_model_requests_dispatched": 0,
            "runtime_network_requests": 0,
            "runtime_credentials_read": 0,
            "runtime_memory_writes": 0,
            "runtime_audit_events_written": 0,
            "runtime_commands_executed": 0,
            "runtime_arbitrary_files_read": 0,
            "runtime_arbitrary_files_written": 0,
            "runtime_execution_features": 0,
        })
        packet = LocalChatHistoryViewPacket(
            packet_id=f"hist-{uuid4().hex[:12]}",
            store_file=str(self.store_file),
            store_exists=self.store_file.exists(),
            records_read=len(records),
            turns_displayed=len(turns),
            messages_viewed=len(turns) * 2,
            created_at=now,
        )
        return {
            "type": "local_chat_history_viewer_alpha",
            "status": self.status_name,
            "version": "0.168.0-genesis",
            "packet_id": packet.packet_id,
            "created_at": packet.created_at,
            "session_mode": packet.session_mode,
            "store_file": packet.store_file,
            "store_exists": packet.store_exists,
            "limit": limit,
            "turns": turns,
            "runtime_counters": counters,
            "safety_boundary": self._boundary(),
            "aura_response": "Chat History Viewer aktif dalam mode read-only. Aku hanya membaca controlled message store AURA, menampilkan ringkasan terbatas, dan tidak menulis history, memory, audit, menjalankan command, membaca arbitrary file, memakai network, credential, atau model.",
        }

    def render_history_alpha(self, limit_text: str | None = None) -> str:
        packet = self.view_history(limit_text)
        counters = packet["runtime_counters"]
        boundary = packet["safety_boundary"]
        lines = [
            "AURA Local Chat History Viewer Alpha",
            "====================================",
            "Version              : 0.168.0-genesis",
            f"Session Mode         : {packet['session_mode']}",
            f"Store File           : {packet['store_file']}",
            f"Store Exists         : {packet['store_exists']}",
            f"History Store Reads  : {counters['runtime_history_store_reads']}",
            f"History Records Read : {counters['runtime_history_records_read']}",
            f"History Turns Displayed: {counters['runtime_history_turns_displayed']}",
            f"History Messages Viewed: {counters['runtime_history_messages_viewed']}",
            f"History Summaries    : {counters['runtime_history_summaries_rendered']}",
            f"Store Writes         : {counters['runtime_message_store_records_written']}",
            f"Model Requests       : {counters['runtime_model_requests_dispatched']}",
            f"Network Requests     : {counters['runtime_network_requests']}",
            f"Credentials Read     : {counters['runtime_credentials_read']}",
            f"Memory Writes        : {counters['runtime_memory_writes']}",
            f"Audit Events Written : {counters['runtime_audit_events_written']}",
            f"Commands Executed    : {counters['runtime_commands_executed']}",
            f"Arbitrary Files Read : {counters['runtime_arbitrary_files_read']}",
            f"Arbitrary Files Wrote: {counters['runtime_arbitrary_files_written']}",
            f"Runtime Execution    : {counters['runtime_execution_features']}",
            f"Model Runtime        : {'disabled' if boundary['model_response_runtime_disabled'] else 'enabled'}",
            f"Network Runtime      : {'disabled' if boundary['network_runtime_disabled'] else 'enabled'}",
            f"Memory Runtime       : {'disabled' if boundary['memory_runtime_disabled'] else 'enabled'}",
            f"Command Execution    : {'disabled' if boundary['command_execution_disabled'] else 'enabled'}",
            f"Arbitrary File Read  : {'disabled' if boundary['arbitrary_file_read_disabled'] else 'enabled'}",
            f"Arbitrary File Write : {'disabled' if boundary['arbitrary_file_mutation_disabled'] else 'enabled'}",
        ]
        for index, turn in enumerate(packet["turns"], 1):
            lines.extend([
                f"Turn {index} Record ID   : {turn['record_id']}",
                f"Turn {index} User        : {turn['user_message']}",
                f"Turn {index} AURA        : {turn['aura_response']}",
            ])
        lines.extend(["", f"AURA: {packet['aura_response']}"])
        return "\n".join(lines)

    def chat_history_viewer_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_viewer_runtime_plan", target, "history_viewer_runtime_items")
    def chat_history_store_read_policy_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_store_read_policy_plan", target, "store_read_policy_items")
    def chat_history_schema_reader_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_schema_reader_plan", target, "schema_reader_items")
    def chat_history_summary_renderer_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_summary_renderer_plan", target, "summary_renderer_items")
    def chat_history_privacy_redaction_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_privacy_redaction_plan", target, "privacy_redaction_items")
    def chat_history_pagination_contract_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_pagination_contract_plan", target, "pagination_contract_items")
    def chat_history_safety_boundary_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_safety_boundary_plan", target, "safety_boundary_items")
    def chat_history_control_center_handoff_plan(self, target: str) -> dict[str, Any]: return self._packet("chat_history_control_center_handoff_plan", target, "control_center_handoff_items")
    def no_local_chat_history_viewer_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._packet("no_local_chat_history_viewer_unsafe_runtime_plan", target, "no_history_viewer_unsafe_runtime_items")
    def local_chat_history_viewer_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]: return self._packet("local_chat_history_viewer_next_sprint_readiness_plan", target, "next_sprint_readiness_items")
