"""Sprint 178 Memory Privacy and Redaction Layer.

Performs deterministic, local, preview-only privacy screening and redaction for
one directly supplied memory candidate. Original and redacted candidates are
not persisted, permission grants are not applied, and memory is not written.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
import re
from typing import Any, Callable
from uuid import uuid4


@dataclass(frozen=True)
class MemoryPrivacyPacket:
    packet_id: str
    candidate_id: str
    original_fingerprint: str
    redacted_fingerprint: str
    created_at: str
    session_mode: str = "local_cli_memory_privacy_redaction_layer_alpha"


class AuraMemoryPrivacyRedactionLayerManager:
    """Preview privacy screening and deterministic redaction without side effects."""

    name = "memory_privacy_redaction_layer"
    status_name = "online"
    version = "0.178.0-genesis"

    PLAN_TYPES = [
        "memory_privacy_redaction_status",
        "memory_privacy_classification_plan",
        "memory_sensitive_pattern_screen_plan",
        "memory_redaction_preview_plan",
        "memory_secret_block_plan",
        "memory_privacy_review_handoff_plan",
        "memory_privacy_permission_handoff_plan",
        "memory_privacy_control_center_plan",
        "memory_privacy_failure_boundary_plan",
        "memory_privacy_lifecycle_plan",
        "no_memory_privacy_unsafe_runtime_plan",
        "memory_privacy_next_sprint_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "layer_items": [
            "memory_privacy_redaction_layer_enabled", "single_candidate_screening", "direct_input_only", "privacy_packet_id", "candidate_fingerprint_binding",
            "deterministic_local_rules", "no_model_classification", "manual_review_required", "privacy_review_required", "no_memory_write",
        ],
        "classification_items": [
            "clear_state", "redaction_review_state", "secret_block_state", "unknown_pattern_hold", "risk_level_visible",
            "category_count_visible", "match_count_visible", "highest_severity_visible", "classification_reason_visible", "no_hidden_classification",
        ],
        "pattern_items": [
            "email_address_pattern", "phone_number_pattern", "ipv4_address_pattern", "credential_assignment_pattern", "bearer_token_pattern",
            "private_key_marker_pattern", "payment_card_like_pattern", "government_id_like_pattern_future", "pattern_span_binding", "pattern_order_deterministic",
        ],
        "redaction_items": [
            "email_mask_preview", "phone_mask_preview", "ipv4_mask_preview", "payment_card_mask_preview", "stable_placeholder_labels",
            "overlap_safe_redaction", "redacted_fingerprint", "original_value_not_rendered", "redaction_not_persisted", "no_automatic_redacted_write",
        ],
        "secret_block_items": [
            "credential_value_block", "bearer_token_block", "private_key_block", "secret_candidate_not_forwarded", "secret_value_not_rendered",
            "secret_fingerprint_only", "manual_reentry_required_future", "no_secret_storage", "no_secret_queue_payload", "default_deny_secret_handling",
        ],
        "review_handoff_items": [
            "privacy_hold_destination", "redacted_preview_destination", "clear_candidate_destination", "manual_review_state", "review_reason_visible",
            "review_item_not_persisted", "decision_not_applied", "sprint_175_queue_compatible", "sprint_177_handoff_compatible", "sprint_179_integration_ready",
        ],
        "permission_items": [
            "write_scope_visible", "single_candidate_scope", "permission_required_after_privacy", "permission_state_visible", "default_deny_preserved",
            "grant_not_applied", "permission_request_not_persisted", "redaction_not_permission_bypass", "secret_block_overrides_write", "write_authorized_false",
        ],
        "control_center_items": [
            "privacy_state_badge_ready", "risk_badge_ready", "category_badge_ready", "redacted_preview_card_ready", "original_hidden_badge_ready",
            "review_destination_badge_ready", "permission_state_badge_ready", "approve_button_disabled", "read_only_privacy_panel_ready", "no_live_store_binding",
        ],
        "failure_boundary_items": [
            "empty_candidate_hold", "oversized_candidate_hold", "unsupported_encoding_future_hold", "redaction_overlap_safe_hold", "unknown_secret_pattern_hold",
            "no_partial_redaction_persist", "no_original_fallback_render", "no_silent_forward", "failure_reason_visible", "safe_idle_on_error",
        ],
        "no_unsafe_runtime_items": [
            "no_candidate_persist", "no_redacted_candidate_persist", "no_review_queue_persist", "no_permission_grant_apply", "no_memory_write",
            "no_store_mutation", "no_model_request", "no_network_request", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_original_candidate_persist", "runtime_redacted_candidate_persist", "runtime_sensitive_value_log", "runtime_privacy_review_persist", "runtime_review_queue_persist",
        "runtime_review_decision_apply", "runtime_permission_request_persist", "runtime_permission_grant_apply", "runtime_permission_scope_activation", "runtime_permission_grant_consume",
        "runtime_memory_write", "runtime_memory_store_mutation", "runtime_memory_pin", "runtime_memory_unpin", "runtime_memory_delete",
        "runtime_memory_export", "runtime_automatic_memory_extraction", "runtime_background_memory_loop", "runtime_model_privacy_classification", "runtime_model_summary",
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_audit_event_write", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch",
        "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control",
        "runtime_full_memory_runtime_open", "runtime_full_chat_runtime_open",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_privacy_evaluations_persisted", "runtime_original_candidates_persisted", "runtime_redacted_candidates_persisted", "runtime_sensitive_values_logged", "runtime_privacy_reviews_persisted",
        "runtime_review_items_persisted", "runtime_review_decisions_applied", "runtime_permission_requests_persisted", "runtime_permission_grants_applied", "runtime_permission_scopes_activated",
        "runtime_permission_grants_consumed", "runtime_memory_writes", "runtime_memory_store_mutations", "runtime_memory_pins", "runtime_memory_unpins",
        "runtime_memory_deletes", "runtime_memory_exports", "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_network_requests",
        "runtime_credentials_read", "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched",
        "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_execution_features",
    ]

    TRIGGER_PATTERNS = [
        ("remember_that", re.compile(r"^\s*remember\s+that\s+", re.IGNORECASE)),
        ("remember", re.compile(r"^\s*remember\s+", re.IGNORECASE)),
        ("ingat_bahwa", re.compile(r"^\s*ingat\s+bahwa\s+", re.IGNORECASE)),
        ("ingat", re.compile(r"^\s*ingat\s+", re.IGNORECASE)),
        ("catat_bahwa", re.compile(r"^\s*catat\s+bahwa\s+", re.IGNORECASE)),
        ("catat", re.compile(r"^\s*catat\s+", re.IGNORECASE)),
    ]

    # Ordered highest-severity patterns first so overlapping spans are handled predictably.
    SECRET_PATTERNS = [
        ("private_key", "critical", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----.*?(?:-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|$)", re.IGNORECASE | re.DOTALL), "[BLOCKED_PRIVATE_KEY]"),
        ("bearer_token", "critical", re.compile(r"\bBearer\s+[A-Za-z0-9._~+\-/]+=*", re.IGNORECASE), "[BLOCKED_BEARER_TOKEN]"),
        ("credential_assignment", "high", re.compile(r"\b(password|passwd|secret|api[_ -]?key|access[_ -]?token|private[_ -]?key)\s*[:=]\s*([^\s,;]+)", re.IGNORECASE), "[BLOCKED_CREDENTIAL]"),
    ]
    REDACT_PATTERNS = [
        ("email_address", "medium", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE), "[REDACTED_EMAIL]"),
        ("phone_number", "medium", re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)"), "[REDACTED_PHONE]"),
        ("payment_card_like", "high", re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)"), "[REDACTED_PAYMENT_CARD]"),
        ("ipv4_address", "low", re.compile(r"(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)"), "[REDACTED_IPV4]"),
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
            "memory_privacy_redaction_layer_only": True,
            "thin_runtime_alpha": True,
            "memory_privacy_redaction_layer_enabled": True,
            "chat_to_memory_handoff_dependency_ready": True,
            "memory_review_queue_dependency_ready": True,
            "memory_write_permission_gate_dependency_ready": True,
            "deterministic_sensitive_pattern_screen_enabled": True,
            "deterministic_redaction_preview_enabled": True,
            "secret_block_boundary_enabled": True,
            "original_value_render_disabled": True,
            "original_candidate_persist_disabled": True,
            "redacted_candidate_persist_disabled": True,
            "sensitive_value_log_disabled": True,
            "privacy_review_required": True,
            "manual_review_required": True,
            "permission_required_after_privacy_review": True,
            "review_queue_persist_disabled": True,
            "review_decision_apply_disabled": True,
            "permission_grant_apply_disabled": True,
            "memory_write_runtime_disabled": True,
            "memory_store_mutation_disabled": True,
            "model_privacy_classification_disabled": True,
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
            "next_sprint_179_memory_runtime_integration_review_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "memory_privacy_redaction_layer_ready": True,
            "memory_privacy_redaction_layer_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_memory_privacy_redaction_layer_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "screening_contract": "deterministic_local_pattern_screen_no_model",
            "redaction_contract": "preview_only_stable_placeholders_original_hidden",
            "secret_contract": "block_do_not_forward_do_not_persist",
            "review_contract": "manual_privacy_review_before_permission_review",
            "permission_scope": "memory.write.single_candidate",
            "next_sprint": "Sprint 179 Memory Runtime Integration Review",
        }

    @staticmethod
    def _normalize(value: str) -> str:
        return " ".join(str(value or "").strip().split())

    def _extract_candidate(self, message: str) -> tuple[str, str]:
        for name, pattern in self.TRIGGER_PATTERNS:
            if pattern.search(message):
                return name, self._normalize(pattern.sub("", message, count=1))
        return "direct_candidate", self._normalize(message)

    @staticmethod
    def _fingerprint(text: str) -> str:
        return sha256(text.casefold().encode("utf-8")).hexdigest()[:16] if text else "not_generated"

    @staticmethod
    def _severity_rank(value: str) -> int:
        return {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}.get(value, 0)

    def _scan(self, text: str) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for mode, patterns in (("block", self.SECRET_PATTERNS), ("redact", self.REDACT_PATTERNS)):
            for category, severity, pattern, placeholder in patterns:
                for found in pattern.finditer(text):
                    matches.append({
                        "category": category,
                        "severity": severity,
                        "mode": mode,
                        "start": found.start(),
                        "end": found.end(),
                        "placeholder": placeholder,
                    })
        return sorted(matches, key=lambda item: (item["start"], -(item["end"] - item["start"]), 0 if item["mode"] == "block" else 1))

    @staticmethod
    def _non_overlapping(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
        accepted: list[dict[str, Any]] = []
        cursor = -1
        for item in matches:
            if item["start"] < cursor:
                continue
            accepted.append(item)
            cursor = item["end"]
        return accepted

    def _redact(self, text: str, matches: list[dict[str, Any]]) -> str:
        accepted = self._non_overlapping(matches)
        if not accepted:
            return text
        parts: list[str] = []
        cursor = 0
        for item in accepted:
            parts.append(text[cursor:item["start"]])
            parts.append(item["placeholder"])
            cursor = item["end"]
        parts.append(text[cursor:])
        return "".join(parts)

    def run_privacy_preview(self, message: str) -> dict[str, Any]:
        normalized_message = self._normalize(message)
        trigger, candidate_text = self._extract_candidate(normalized_message)
        candidate_valid = bool(candidate_text)
        matches = self._scan(candidate_text) if candidate_valid else []
        accepted_matches = self._non_overlapping(matches)
        categories = sorted({item["category"] for item in accepted_matches})
        block_matches = [item for item in accepted_matches if item["mode"] == "block"]
        redact_matches = [item for item in accepted_matches if item["mode"] == "redact"]
        highest_severity = max((item["severity"] for item in accepted_matches), key=self._severity_rank, default="none")
        redacted_text = self._redact(candidate_text, accepted_matches) if candidate_valid else ""

        original_fingerprint = self._fingerprint(candidate_text)
        redacted_fingerprint = self._fingerprint(redacted_text)
        packet = MemoryPrivacyPacket(
            packet_id=f"memory-privacy-{uuid4().hex[:12]}",
            candidate_id=f"memory-candidate-{sha256(('candidate|' + candidate_text.casefold()).encode('utf-8')).hexdigest()[:12]}" if candidate_valid else "not_generated",
            original_fingerprint=original_fingerprint,
            redacted_fingerprint=redacted_fingerprint,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        if not candidate_valid:
            privacy_state = "empty_candidate_hold"
            redaction_action = "none"
            failure_reason = "candidate_text_required"
            review_destination = "not_forwarded"
            review_state = "not_created"
            handoff_eligible = False
            gate_decision = "blocked_invalid_candidate"
            memory_state = "no_privacy_candidate_forwarded"
        elif block_matches:
            privacy_state = "blocked_sensitive_secret"
            redaction_action = "block_and_hide_sensitive_secret_preview"
            failure_reason = "secret_pattern_must_not_enter_memory_pipeline"
            review_destination = "memory_privacy_manual_secret_hold"
            review_state = "privacy_secret_hold"
            handoff_eligible = False
            gate_decision = "blocked_sensitive_secret"
            memory_state = "secret_block_preview_only_not_saved"
        elif redact_matches:
            privacy_state = "redaction_review_required"
            redaction_action = "mask_sensitive_segments_preview"
            failure_reason = "none"
            review_destination = "memory_review_queue_privacy_hold"
            review_state = "pending_privacy_review"
            handoff_eligible = False
            gate_decision = "blocked_privacy_review_and_permission"
            memory_state = "redaction_preview_only_not_saved"
        else:
            privacy_state = "clear_no_common_sensitive_pattern"
            redaction_action = "none_required"
            failure_reason = "none"
            review_destination = "memory_review_queue_preview"
            review_state = "pending_manual_review"
            handoff_eligible = True
            gate_decision = "blocked_pending_manual_review_and_permission"
            memory_state = "privacy_clear_preview_only_not_saved"

        # Only the redacted form is rendered. For clear candidates it is identical to the input candidate.
        rendered_preview = redacted_text[:220] if redacted_text else "not_available"
        return {
            "version": self.version,
            "session_mode": packet.session_mode,
            "privacy_packet_id": packet.packet_id,
            "candidate_id": packet.candidate_id,
            "original_candidate_fingerprint": packet.original_fingerprint,
            "redacted_candidate_fingerprint": packet.redacted_fingerprint,
            "source_kind": "direct_user_supplied_memory_candidate",
            "privacy_evaluations": 1,
            "screening_method": "deterministic_local_pattern_screen_no_model",
            "trigger_detected": trigger,
            "candidate_length": len(candidate_text),
            "original_candidate_rendered": False,
            "redacted_candidate_preview": rendered_preview,
            "sensitive_match_count": len(accepted_matches),
            "redaction_match_count": len(redact_matches),
            "secret_block_match_count": len(block_matches),
            "sensitive_categories": ", ".join(categories) if categories else "none",
            "highest_severity": highest_severity,
            "privacy_state": privacy_state,
            "redaction_action": redaction_action,
            "failure_reason": failure_reason,
            "review_destination": review_destination,
            "review_state": review_state,
            "handoff_eligible": handoff_eligible,
            "permission_scope": "memory.write.single_candidate",
            "permission_state": "required_not_granted",
            "gate_decision": gate_decision,
            "write_authorized": False,
            "original_candidate_persisted": False,
            "redacted_candidate_persisted": False,
            "review_item_persisted": False,
            "redaction_applied_to_store": False,
            "sensitive_value_logged": False,
            "memory_state": memory_state,
            "manual_review_required": True,
            "privacy_review_required": True,
            "next_sprint": "Sprint 179 Memory Runtime Integration Review",
            "privacy_evaluations_persisted": 0,
            "original_candidates_persisted": 0,
            "redacted_candidates_persisted": 0,
            "sensitive_values_logged": 0,
            "privacy_reviews_persisted": 0,
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
            "original_candidate_persist_runtime": "disabled",
            "redacted_candidate_persist_runtime": "disabled",
            "sensitive_value_log_runtime": "disabled",
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
                "Memory Privacy and Redaction Layer selesai sebagai preview lokal deterministik. Hanya bentuk yang sudah disamarkan yang ditampilkan; "
                "nilai asli tidak dipersist atau dicatat. Secret berisiko tinggi diblokir, sedangkan data yang dapat disamarkan tetap menunggu privacy review dan permission eksplisit."
            ),
        }

    def render_privacy_preview(self, message: str) -> str:
        data = self.run_privacy_preview(message)
        labels = [
            ("Version", "version"), ("Session Mode", "session_mode"), ("Privacy Packet ID", "privacy_packet_id"),
            ("Candidate ID", "candidate_id"), ("Original Candidate Fingerprint", "original_candidate_fingerprint"),
            ("Redacted Candidate Fingerprint", "redacted_candidate_fingerprint"), ("Source Kind", "source_kind"),
            ("Privacy Evaluations", "privacy_evaluations"), ("Screening Method", "screening_method"), ("Trigger Detected", "trigger_detected"),
            ("Candidate Length", "candidate_length"), ("Original Candidate Rendered", "original_candidate_rendered"),
            ("Redacted Candidate Preview", "redacted_candidate_preview"), ("Sensitive Match Count", "sensitive_match_count"),
            ("Redaction Match Count", "redaction_match_count"), ("Secret Block Match Count", "secret_block_match_count"),
            ("Sensitive Categories", "sensitive_categories"), ("Highest Severity", "highest_severity"), ("Privacy State", "privacy_state"),
            ("Redaction Action", "redaction_action"), ("Failure Reason", "failure_reason"), ("Review Destination", "review_destination"),
            ("Review State", "review_state"), ("Handoff Eligible", "handoff_eligible"), ("Permission Scope", "permission_scope"),
            ("Permission State", "permission_state"), ("Gate Decision", "gate_decision"), ("Write Authorized", "write_authorized"),
            ("Original Candidate Persisted", "original_candidate_persisted"), ("Redacted Candidate Persisted", "redacted_candidate_persisted"),
            ("Review Item Persisted", "review_item_persisted"), ("Redaction Applied To Store", "redaction_applied_to_store"),
            ("Sensitive Value Logged", "sensitive_value_logged"), ("Memory State", "memory_state"),
            ("Manual Review Required", "manual_review_required"), ("Privacy Review Required", "privacy_review_required"), ("Next Sprint", "next_sprint"),
            ("Privacy Evaluations Persisted", "privacy_evaluations_persisted"), ("Original Candidates Persisted", "original_candidates_persisted"),
            ("Redacted Candidates Persisted", "redacted_candidates_persisted"), ("Sensitive Values Logged", "sensitive_values_logged"),
            ("Privacy Reviews Persisted", "privacy_reviews_persisted"), ("Review Items Persisted", "review_items_persisted"),
            ("Review Decisions Applied", "review_decisions_applied"), ("Permission Requests Persisted", "permission_requests_persisted"),
            ("Permission Grants", "permission_grants"), ("Memory Writes", "memory_writes"), ("Memory Store Mutations", "memory_store_mutations"),
            ("Memory Pins", "memory_pins"), ("Memory Deletes", "memory_deletes"), ("Model Requests", "model_requests"),
            ("Model Responses", "model_responses"), ("Network Requests", "network_requests"), ("Credentials Read", "credentials_read"),
            ("Audit Events Written", "audit_events_written"), ("Commands Executed", "commands_executed"),
            ("Arbitrary Files Read", "arbitrary_files_read"), ("Arbitrary Files Wrote", "arbitrary_files_wrote"), ("Runtime Execution", "runtime_execution"),
            ("Original Candidate Persist Runtime", "original_candidate_persist_runtime"), ("Redacted Candidate Persist Runtime", "redacted_candidate_persist_runtime"),
            ("Sensitive Value Log Runtime", "sensitive_value_log_runtime"), ("Review Queue Persist Runtime", "review_queue_persist_runtime"),
            ("Permission Grant Runtime", "permission_grant_runtime"), ("Memory Write Runtime", "memory_write_runtime"),
            ("Memory Store Mutation", "memory_store_mutation"), ("Model Runtime", "model_runtime"), ("Network Runtime", "network_runtime"),
            ("Credential Runtime", "credential_runtime"), ("Audit Write Runtime", "audit_write_runtime"), ("Command Execution", "command_execution"),
            ("Arbitrary File Read", "arbitrary_file_read"), ("Arbitrary File Write", "arbitrary_file_write"),
            ("Full Memory Runtime", "full_memory_runtime"), ("Full Chat Runtime", "full_chat_runtime"),
        ]
        lines = ["[memory-privacy] AURA Memory Privacy and Redaction Layer Alpha"]
        for label, key in labels:
            lines.append(f"[memory-privacy] {label:<34}: {data[key]}")
        lines.append(f"[memory-privacy] AURA: {data['aura_reply']}")
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name, "version": self.version, "status": "planned", "plan_type": plan_type,
            "target": self._normalize(target) or "AURA memory privacy and redaction layer",
            "items": [{"id": item, "preview_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(), **self._runtime_zero_map(),
        }

    def memory_privacy_classification_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_classification_plan", target, "classification_items")
    def memory_sensitive_pattern_screen_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_sensitive_pattern_screen_plan", target, "pattern_items")
    def memory_redaction_preview_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_redaction_preview_plan", target, "redaction_items")
    def memory_secret_block_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_secret_block_plan", target, "secret_block_items")
    def memory_privacy_review_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_review_handoff_plan", target, "review_handoff_items")
    def memory_privacy_permission_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_permission_handoff_plan", target, "permission_items")
    def memory_privacy_control_center_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_control_center_plan", target, "control_center_items")
    def memory_privacy_failure_boundary_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_failure_boundary_plan", target, "failure_boundary_items")
    def memory_privacy_lifecycle_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_privacy_lifecycle_plan", target, "layer_items")
    def no_memory_privacy_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_memory_privacy_unsafe_runtime_plan", target, "no_unsafe_runtime_items")
    def memory_privacy_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        packet = self._plan("memory_privacy_next_sprint_readiness_plan", target, "review_handoff_items")
        packet["next_sprint"] = "Sprint 179 Memory Runtime Integration Review"
        return packet
