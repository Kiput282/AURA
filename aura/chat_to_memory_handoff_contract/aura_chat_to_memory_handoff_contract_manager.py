"""Sprint 177 Chat-to-Memory Handoff Contract.

Builds a deterministic, preview-only handoff envelope from one directly
supplied user chat turn into the memory review pipeline. It does not scan chat
history, read the chat store, persist a queue item, apply a permission grant,
or write or mutate memory.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import re
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ChatToMemoryHandoffPacket:
    packet_id: str
    chat_turn_ref: str
    candidate_id: str
    candidate_fingerprint: str
    created_at: str
    session_mode: str = "local_cli_chat_to_memory_handoff_contract_alpha"


class AuraChatToMemoryHandoffContractManager:
    """Preview a bounded user-chat-to-memory handoff without side effects."""

    name = "chat_to_memory_handoff_contract"
    status_name = "online"
    version = "0.177.0-genesis"

    PLAN_TYPES = [
        "chat_to_memory_handoff_contract_status",
        "chat_source_binding_plan",
        "chat_memory_intent_gate_plan",
        "chat_memory_candidate_envelope_plan",
        "chat_memory_review_queue_handoff_plan",
        "chat_memory_permission_handoff_plan",
        "chat_memory_privacy_precheck_plan",
        "chat_memory_control_center_handoff_plan",
        "chat_memory_failure_boundary_plan",
        "chat_memory_lifecycle_plan",
        "no_chat_to_memory_unsafe_runtime_plan",
        "chat_to_memory_next_sprint_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "contract_items": [
            "chat_to_memory_handoff_contract_enabled", "single_user_turn_handoff", "direct_user_input_only", "handoff_packet_id", "chat_turn_reference",
            "candidate_id", "candidate_fingerprint", "source_role_visible", "manual_review_required", "no_automatic_memory_write",
        ],
        "source_binding_items": [
            "user_role_allowed", "assistant_role_blocked", "system_role_blocked", "tool_role_blocked", "external_event_role_blocked",
            "single_turn_exact_text_binding", "no_chat_history_scan", "no_chat_store_read", "no_latest_turn_guess", "source_binding_failure_visible",
        ],
        "intent_gate_items": [
            "explicit_memory_request_required", "remember_that_trigger", "remember_trigger", "ingat_bahwa_trigger", "ingat_trigger",
            "catat_bahwa_trigger", "catat_trigger", "implicit_memory_inference_disabled", "default_not_eligible", "intent_state_visible",
        ],
        "candidate_envelope_items": [
            "normalized_candidate_preview", "candidate_kind_preview", "candidate_fingerprint_bound", "source_message_hash", "extraction_method_visible",
            "candidate_not_persisted", "candidate_text_length_visible", "candidate_empty_hold", "one_candidate_per_handoff", "no_model_summary",
        ],
        "review_handoff_items": [
            "review_queue_destination_visible", "review_priority_future", "review_state_pending", "review_item_not_persisted", "review_decision_not_applied",
            "approve_once_future_option", "edit_then_review_future_option", "reject_future_option", "defer_future_option", "sprint_175_contract_compatible",
        ],
        "permission_handoff_items": [
            "memory_write_scope_visible", "single_candidate_scope", "permission_state_visible", "default_deny_preserved", "one_shot_grant_future",
            "grant_fingerprint_match_required", "permission_request_not_persisted", "permission_grant_not_applied", "write_authorized_false", "no_permission_bypass",
        ],
        "privacy_items": [
            "privacy_precheck_enabled", "sensitive_pattern_screen", "redacted_preview_on_hold", "no_sensitive_value_logging", "privacy_hold_visible",
            "privacy_review_required", "no_automatic_redaction_write", "no_model_privacy_classification", "sprint_178_handoff_ready", "unsafe_candidate_not_forwarded",
        ],
        "control_center_items": [
            "source_role_badge_ready", "intent_state_badge_ready", "candidate_kind_badge_ready", "privacy_hold_badge_ready", "permission_state_badge_ready",
            "review_destination_badge_ready", "handoff_state_badge_ready", "approve_button_disabled", "read_only_handoff_card_ready", "no_live_chat_binding",
        ],
        "failure_boundary_items": [
            "empty_message_hold", "non_user_source_hold", "no_explicit_trigger_hold", "sensitive_candidate_privacy_hold", "invalid_candidate_hold",
            "missing_permission_default_deny", "review_queue_unavailable_safe_idle", "no_partial_handoff_persist", "no_silent_write", "failure_reason_visible",
        ],
        "no_unsafe_runtime_items": [
            "no_chat_store_read", "no_chat_history_scan", "no_queue_persist", "no_permission_grant_apply", "no_memory_write",
            "no_store_mutation", "no_model_request", "no_network_request", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_chat_store_read", "runtime_chat_history_scan", "runtime_chat_turn_lookup", "runtime_chat_event_subscription", "runtime_automatic_chat_memory_handoff",
        "runtime_memory_candidate_persist", "runtime_review_queue_persist", "runtime_review_decision_apply", "runtime_permission_request_persist", "runtime_permission_grant_apply",
        "runtime_permission_scope_activation", "runtime_permission_grant_consume", "runtime_memory_write", "runtime_memory_store_mutation", "runtime_memory_pin",
        "runtime_memory_unpin", "runtime_memory_delete", "runtime_memory_export", "runtime_automatic_memory_extraction", "runtime_background_memory_loop",
        "runtime_model_summary", "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call",
        "runtime_network_request", "runtime_credential_read", "runtime_audit_event_write", "runtime_command_execution", "runtime_tool_execution",
        "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete",
        "runtime_desktop_control", "runtime_full_memory_runtime_open", "runtime_full_chat_runtime_open",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_chat_store_reads", "runtime_chat_history_scans", "runtime_chat_turn_lookups", "runtime_chat_events_consumed", "runtime_chat_memory_handoffs_persisted",
        "runtime_memory_candidates_persisted", "runtime_review_items_persisted", "runtime_review_decisions_applied", "runtime_permission_requests_persisted", "runtime_permission_grants_applied",
        "runtime_permission_scopes_activated", "runtime_permission_grants_consumed", "runtime_memory_writes", "runtime_memory_store_mutations", "runtime_memory_pins",
        "runtime_memory_unpins", "runtime_memory_deletes", "runtime_memory_exports", "runtime_model_requests_dispatched", "runtime_model_responses_received",
        "runtime_network_requests", "runtime_credentials_read", "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed",
        "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted",
        "runtime_execution_features",
    ]

    TRIGGER_PATTERNS = [
        ("remember_that", re.compile(r"^\s*remember\s+that\s+", re.IGNORECASE)),
        ("remember", re.compile(r"^\s*remember\s+", re.IGNORECASE)),
        ("ingat_bahwa", re.compile(r"^\s*ingat\s+bahwa\s+", re.IGNORECASE)),
        ("ingat", re.compile(r"^\s*ingat\s+", re.IGNORECASE)),
        ("catat_bahwa", re.compile(r"^\s*catat\s+bahwa\s+", re.IGNORECASE)),
        ("catat", re.compile(r"^\s*catat\s+", re.IGNORECASE)),
    ]
    SENSITIVE_PATTERNS = {
        "email_pattern_detected": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        "phone_pattern_detected": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)"),
        "credential_keyword_detected": re.compile(r"\b(?:password|passwd|credential|secret|api[_ -]?key|access[_ -]?token|private[_ -]?key)\b", re.IGNORECASE),
        "private_key_marker_detected": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", re.IGNORECASE),
    }

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
            "chat_to_memory_handoff_contract_only": True,
            "thin_runtime_alpha": True,
            "chat_to_memory_handoff_contract_enabled": True,
            "local_chat_runtime_stabilization_dependency_ready": True,
            "memory_extraction_dry_run_dependency_ready": True,
            "memory_review_queue_dependency_ready": True,
            "memory_write_permission_gate_dependency_ready": True,
            "explicit_user_memory_request_required": True,
            "single_user_turn_handoff_enabled": True,
            "chat_source_binding_enabled": True,
            "candidate_envelope_preview_enabled": True,
            "review_queue_handoff_preview_enabled": True,
            "permission_handoff_preview_enabled": True,
            "privacy_precheck_enabled": True,
            "manual_review_required": True,
            "privacy_review_required": True,
            "automatic_chat_scan_disabled": True,
            "assistant_message_handoff_disabled": True,
            "system_message_handoff_disabled": True,
            "tool_output_handoff_disabled": True,
            "chat_store_read_disabled": True,
            "chat_history_scan_disabled": True,
            "review_queue_persist_disabled": True,
            "candidate_persist_runtime_disabled": True,
            "permission_grant_apply_disabled": True,
            "memory_write_runtime_disabled": True,
            "memory_store_mutation_disabled": True,
            "model_request_dispatch_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "audit_write_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_read_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "full_memory_runtime_disabled": True,
            "full_chat_runtime_disabled": True,
            "release_gate_closed": True,
            "next_sprint_178_memory_privacy_redaction_layer_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "chat_to_memory_handoff_contract_ready": True,
            "chat_to_memory_handoff_contract_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_chat_to_memory_handoff_contract_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "source_contract": "one_directly_supplied_user_turn_only",
            "intent_contract": "explicit_memory_trigger_required",
            "candidate_contract": "deterministic_preview_no_model_no_persistence",
            "review_destination": "memory_review_queue_preview",
            "permission_scope": "memory.write.single_candidate",
            "next_sprint": "Sprint 178 Memory Privacy and Redaction Layer",
        }

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(str(value or "").strip().split())

    def _extract_candidate(self, message: str) -> tuple[str, str]:
        for name, pattern in self.TRIGGER_PATTERNS:
            if pattern.search(message):
                return name, self._normalize(pattern.sub("", message, count=1))
        return "none", ""

    def _sensitive(self, text: str) -> list[str]:
        return [name for name, pattern in self.SENSITIVE_PATTERNS.items() if pattern.search(text)]

    @staticmethod
    def _candidate_kind(text: str) -> str:
        lowered = text.casefold()
        if any(token in lowered for token in ("aura", "project", "sprint", "roadmap", "workflow", "policy", "local-first", "permission-gated")):
            return "project_fact"
        if any(token in lowered for token in ("i prefer", "saya suka", "saya lebih suka", "preferensi")):
            return "user_preference"
        return "general_fact"

    def run_handoff_preview(self, message: str, source_role: str = "user") -> dict[str, Any]:
        normalized_message = self._normalize(message)
        normalized_role = self._normalize(source_role).casefold() or "unknown"
        trigger, candidate_text = self._extract_candidate(normalized_message)
        explicit_request = trigger != "none"
        source_allowed = normalized_role == "user"
        message_valid = bool(normalized_message)
        candidate_valid = bool(candidate_text)
        sensitive_matches = self._sensitive(candidate_text) if candidate_valid else []
        privacy_hold = bool(sensitive_matches)
        eligible = source_allowed and message_valid and explicit_request and candidate_valid and not privacy_hold

        message_hash = sha256(normalized_message.casefold().encode("utf-8")).hexdigest()[:16] if message_valid else "not_generated"
        candidate_fingerprint = sha256(candidate_text.casefold().encode("utf-8")).hexdigest()[:16] if candidate_valid else "not_generated"
        packet = ChatToMemoryHandoffPacket(
            packet_id=f"chat-memory-handoff-{uuid4().hex[:12]}",
            chat_turn_ref=f"chat-turn-ref-{message_hash[:12]}" if message_valid else "not_generated",
            candidate_id=f"memory-candidate-{sha256(('candidate|' + candidate_text.casefold()).encode('utf-8')).hexdigest()[:12]}" if candidate_valid else "not_generated",
            candidate_fingerprint=candidate_fingerprint,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        if not source_allowed:
            handoff_state, failure_reason = "source_role_blocked", "only_direct_user_turn_is_allowed"
        elif not message_valid:
            handoff_state, failure_reason = "empty_message_hold", "direct_user_message_required"
        elif not explicit_request:
            handoff_state, failure_reason = "not_eligible_no_explicit_memory_request", "explicit_memory_trigger_required"
        elif not candidate_valid:
            handoff_state, failure_reason = "empty_candidate_hold", "memory_trigger_requires_candidate_text"
        elif privacy_hold:
            handoff_state, failure_reason = "privacy_hold_not_forwarded", "sensitive_pattern_requires_privacy_review"
        else:
            handoff_state, failure_reason = "candidate_handoff_preview_ready", "none"

        candidate_preview = "[redacted: sensitive pattern requires Sprint 178 privacy review]" if privacy_hold else (candidate_text[:180] if candidate_text else "not_available")
        return {
            "version": self.version,
            "session_mode": packet.session_mode,
            "handoff_packet_id": packet.packet_id,
            "chat_turn_reference": packet.chat_turn_ref,
            "source_message_hash": message_hash,
            "candidate_id": packet.candidate_id,
            "candidate_fingerprint": packet.candidate_fingerprint,
            "source_role": normalized_role,
            "source_allowed": source_allowed,
            "handoff_evaluations": 1,
            "handoff_method": "deterministic_direct_user_turn_preview_no_chat_store_no_model",
            "trigger_detected": trigger,
            "explicit_memory_request": explicit_request,
            "candidate_kind": self._candidate_kind(candidate_text) if candidate_valid else "not_classified",
            "candidate_text_preview": candidate_preview,
            "candidate_text_length": len(candidate_text),
            "privacy_hold": privacy_hold,
            "sensitive_match_count": len(sensitive_matches),
            "handoff_eligible": eligible,
            "handoff_state": handoff_state,
            "failure_reason": failure_reason,
            "review_destination": "memory_review_queue_preview" if eligible else "not_forwarded",
            "review_state": "pending_manual_review" if eligible else ("privacy_hold" if privacy_hold else "not_created"),
            "review_item_persisted": False,
            "permission_scope": "memory.write.single_candidate",
            "permission_state": "required_not_granted",
            "gate_decision": "blocked_pending_manual_review_and_permission" if eligible else "blocked_handoff_not_eligible",
            "write_authorized": False,
            "candidate_persisted": False,
            "chat_store_read_performed": False,
            "chat_history_scan_performed": False,
            "memory_state": "chat_handoff_preview_only_not_saved" if eligible else "no_memory_candidate_forwarded",
            "manual_review_required": True,
            "privacy_review_required": True,
            "next_sprint": "Sprint 178 Memory Privacy and Redaction Layer",
            "chat_store_reads": 0,
            "chat_history_scans": 0,
            "chat_turn_lookups": 0,
            "chat_events_consumed": 0,
            "handoffs_persisted": 0,
            "review_items_persisted": 0,
            "review_decisions_applied": 0,
            "permission_requests_persisted": 0,
            "permission_grants": 0,
            "memory_writes": 0,
            "memory_store_mutations": 0,
            "memory_pins": 0,
            "memory_deletes": 0,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "audit_events_written": 0,
            "commands_executed": 0,
            "arbitrary_files_read": 0,
            "arbitrary_files_wrote": 0,
            "runtime_execution": 0,
            "chat_store_read_runtime": "disabled",
            "chat_history_scan_runtime": "disabled",
            "automatic_handoff_runtime": "disabled",
            "review_queue_persist_runtime": "disabled",
            "permission_grant_runtime": "disabled",
            "memory_write_runtime": "disabled",
            "memory_store_mutation": "disabled",
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "credential_runtime": "disabled",
            "audit_write_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_read": "disabled",
            "arbitrary_file_write": "disabled",
            "full_memory_runtime": "disabled",
            "full_chat_runtime": "disabled",
            "aura_reply": (
                "Chat-to-Memory Handoff Contract selesai sebagai preview satu user turn. Handoff hanya eligible saat ada permintaan memory eksplisit, "
                "lolos privacy precheck, dan tetap diarahkan ke review queue dengan permission required_not_granted. Chat store tidak dibaca dan memory tidak ditulis."
            ),
        }

    def render_handoff_preview(self, message: str, source_role: str = "user") -> str:
        data = self.run_handoff_preview(message, source_role)
        labels = [
            ("Version", "version"), ("Session Mode", "session_mode"), ("Handoff Packet ID", "handoff_packet_id"),
            ("Chat Turn Reference", "chat_turn_reference"), ("Source Message Hash", "source_message_hash"), ("Candidate ID", "candidate_id"),
            ("Candidate Fingerprint", "candidate_fingerprint"), ("Source Role", "source_role"), ("Source Allowed", "source_allowed"),
            ("Handoff Evaluations", "handoff_evaluations"), ("Handoff Method", "handoff_method"), ("Trigger Detected", "trigger_detected"),
            ("Explicit Memory Request", "explicit_memory_request"), ("Candidate Kind", "candidate_kind"), ("Candidate Text Preview", "candidate_text_preview"),
            ("Candidate Text Length", "candidate_text_length"), ("Privacy Hold", "privacy_hold"), ("Sensitive Match Count", "sensitive_match_count"),
            ("Handoff Eligible", "handoff_eligible"), ("Handoff State", "handoff_state"), ("Failure Reason", "failure_reason"),
            ("Review Destination", "review_destination"), ("Review State", "review_state"), ("Review Item Persisted", "review_item_persisted"),
            ("Permission Scope", "permission_scope"), ("Permission State", "permission_state"), ("Gate Decision", "gate_decision"),
            ("Write Authorized", "write_authorized"), ("Candidate Persisted", "candidate_persisted"), ("Chat Store Read Performed", "chat_store_read_performed"),
            ("Chat History Scan Performed", "chat_history_scan_performed"), ("Memory State", "memory_state"),
            ("Manual Review Required", "manual_review_required"), ("Privacy Review Required", "privacy_review_required"), ("Next Sprint", "next_sprint"),
            ("Chat Store Reads", "chat_store_reads"), ("Chat History Scans", "chat_history_scans"), ("Chat Turn Lookups", "chat_turn_lookups"),
            ("Chat Events Consumed", "chat_events_consumed"), ("Handoffs Persisted", "handoffs_persisted"), ("Review Items Persisted", "review_items_persisted"),
            ("Review Decisions Applied", "review_decisions_applied"), ("Permission Requests Persisted", "permission_requests_persisted"),
            ("Permission Grants", "permission_grants"), ("Memory Writes", "memory_writes"), ("Memory Store Mutations", "memory_store_mutations"),
            ("Memory Pins", "memory_pins"), ("Memory Deletes", "memory_deletes"), ("Model Requests", "model_requests"),
            ("Model Responses", "model_responses"), ("Network Requests", "network_requests"), ("Credentials Read", "credentials_read"),
            ("Audit Events Written", "audit_events_written"), ("Commands Executed", "commands_executed"),
            ("Arbitrary Files Read", "arbitrary_files_read"), ("Arbitrary Files Wrote", "arbitrary_files_wrote"), ("Runtime Execution", "runtime_execution"),
            ("Chat Store Read Runtime", "chat_store_read_runtime"), ("Chat History Scan Runtime", "chat_history_scan_runtime"),
            ("Automatic Handoff Runtime", "automatic_handoff_runtime"), ("Review Queue Persist Runtime", "review_queue_persist_runtime"),
            ("Permission Grant Runtime", "permission_grant_runtime"), ("Memory Write Runtime", "memory_write_runtime"),
            ("Memory Store Mutation", "memory_store_mutation"), ("Model Runtime", "model_runtime"), ("Network Runtime", "network_runtime"),
            ("Credential Runtime", "credential_runtime"), ("Audit Write Runtime", "audit_write_runtime"), ("Command Execution", "command_execution"),
            ("Arbitrary File Read", "arbitrary_file_read"), ("Arbitrary File Write", "arbitrary_file_write"),
            ("Full Memory Runtime", "full_memory_runtime"), ("Full Chat Runtime", "full_chat_runtime"),
        ]
        lines = ["[chat-memory] AURA Chat-to-Memory Handoff Contract Alpha"]
        for label, key in labels:
            lines.append(f"[chat-memory] {label:<30}: {data[key]}")
        lines.append(f"[chat-memory] AURA: {data['aura_reply']}")
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name, "version": self.version, "status": "planned", "plan_type": plan_type,
            "target": self._normalize(target) or "AURA chat-to-memory handoff contract",
            "items": [{"id": item, "preview_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(), **self._runtime_zero_map(),
        }

    def chat_source_binding_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_source_binding_plan", target, "source_binding_items")
    def chat_memory_intent_gate_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_intent_gate_plan", target, "intent_gate_items")
    def chat_memory_candidate_envelope_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_candidate_envelope_plan", target, "candidate_envelope_items")
    def chat_memory_review_queue_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_review_queue_handoff_plan", target, "review_handoff_items")
    def chat_memory_permission_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_permission_handoff_plan", target, "permission_handoff_items")
    def chat_memory_privacy_precheck_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_privacy_precheck_plan", target, "privacy_items")
    def chat_memory_control_center_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_control_center_handoff_plan", target, "control_center_items")
    def chat_memory_failure_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_failure_boundary_plan", target, "failure_boundary_items")
    def chat_memory_lifecycle_plan(self, target: str) -> dict[str, Any]: return self._plan("chat_memory_lifecycle_plan", target, "contract_items")
    def no_chat_to_memory_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_chat_to_memory_unsafe_runtime_plan", target, "no_unsafe_runtime_items")
    def chat_to_memory_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        packet = self._plan("chat_to_memory_next_sprint_readiness_plan", target, "privacy_items")
        packet["next_sprint"] = "Sprint 178 Memory Privacy and Redaction Layer"
        return packet
