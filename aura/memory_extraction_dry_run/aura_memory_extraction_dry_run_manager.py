"""Sprint 173 Memory Extraction Dry Run.

This module performs deterministic, rule-based extraction of one explicit
memory candidate from user-supplied text. The extraction result exists only in
process memory as a review preview. It does not call a model, persist a
candidate, apply a permission grant, or write the memory store.
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
class MemoryExtractionDryRunPacket:
    packet_id: str
    candidate_id: str
    candidate_fingerprint: str
    created_at: str
    session_mode: str = "local_cli_memory_extraction_dry_run_alpha"


class AuraMemoryExtractionDryRunManager:
    """Extract one reviewable memory candidate without persistence."""

    name = "memory_extraction_dry_run"
    status_name = "online"
    version = "0.173.0-genesis"

    PLAN_TYPES = [
        "memory_extraction_dry_run_status",
        "memory_explicit_trigger_detection_plan",
        "memory_candidate_normalization_plan",
        "memory_candidate_classification_plan",
        "memory_sensitive_pattern_screen_plan",
        "memory_candidate_fingerprint_handoff_plan",
        "memory_permission_gate_handoff_plan",
        "memory_manual_review_handoff_plan",
        "memory_extraction_failure_boundary_plan",
        "memory_control_center_extraction_preview_plan",
        "no_memory_extraction_unsafe_runtime_plan",
        "memory_extraction_next_sprint_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "extraction_contract_items": [
            "memory_extraction_dry_run_enabled", "single_candidate_dry_run", "user_supplied_text_only", "deterministic_rules_only", "no_model_summary",
            "explicit_trigger_preferred", "candidate_preview_only", "permission_gate_required", "manual_review_required", "memory_write_still_disabled",
        ],
        "trigger_detection_items": [
            "remember_that_trigger", "remember_trigger", "ingat_bahwa_trigger", "ingat_trigger", "catat_bahwa_trigger",
            "catat_trigger", "save_that_trigger", "store_that_trigger", "explicit_request_detected", "implicit_background_extraction_disabled",
        ],
        "normalization_items": [
            "trim_outer_whitespace", "collapse_internal_whitespace", "remove_explicit_trigger_prefix", "preserve_user_meaning", "preserve_original_language",
            "bounded_candidate_length", "empty_candidate_rejected", "no_semantic_rewrite", "no_model_paraphrase", "normalized_text_preview",
        ],
        "classification_items": [
            "explicit_user_memory_candidate", "user_preference_candidate", "project_fact_candidate", "identity_fact_candidate", "workflow_rule_candidate",
            "general_fact_candidate", "unknown_candidate_kind", "classification_rule_visible", "classification_confidence_preview", "classification_requires_review",
        ],
        "sensitive_screen_items": [
            "email_pattern_screen", "phone_pattern_screen", "credential_keyword_screen", "api_key_keyword_screen", "password_keyword_screen",
            "private_key_marker_screen", "token_keyword_screen", "sensitive_state_visible", "privacy_review_always_required", "no_sensitive_value_logging",
        ],
        "fingerprint_handoff_items": [
            "normalized_text_hash", "candidate_kind_bound", "source_kind_bound", "candidate_id_bound", "fingerprint_preview_only",
            "permission_scope_memory_write_single_candidate", "exact_candidate_match_required", "candidate_change_invalidates", "no_cross_candidate_reuse", "no_fingerprint_persistence",
        ],
        "permission_review_items": [
            "memory_write_gate_dependency_ready", "decision_state_required_not_granted", "gate_decision_blocked", "write_authorized_false", "approve_once_future_only",
            "manual_review_required", "privacy_review_required", "candidate_edit_future", "candidate_reject_future", "candidate_persist_disabled",
        ],
        "failure_boundary_items": [
            "empty_input_rejected", "trigger_only_input_rejected", "oversize_input_bounded", "unsupported_source_rejected", "ambiguous_candidate_review_required",
            "sensitive_candidate_flagged", "model_unavailable_not_error", "permission_missing_blocks", "store_unavailable_not_accessed", "no_silent_extraction",
        ],
        "control_center_handoff_items": [
            "extraction_preview_card_ready", "candidate_text_preview_ready", "candidate_kind_badge_ready", "confidence_badge_ready", "sensitive_state_badge_ready",
            "fingerprint_badge_ready", "permission_state_badge_ready", "review_required_badge_ready", "approve_once_button_future", "write_button_disabled",
        ],
        "no_unsafe_runtime_items": [
            "no_candidate_persist", "no_permission_grant_apply", "no_memory_write", "no_store_mutation", "no_memory_delete",
            "no_memory_export", "no_model_request", "no_network_request", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_memory_candidate_persist", "runtime_permission_request_persist", "runtime_permission_grant_apply", "runtime_permission_deny_apply", "runtime_permission_scope_activation",
        "runtime_permission_grant_consume", "runtime_memory_write", "runtime_memory_store_mutation", "runtime_memory_delete", "runtime_memory_export",
        "runtime_memory_import", "runtime_automatic_memory_extraction", "runtime_background_memory_loop", "runtime_model_summary", "runtime_model_request_dispatch",
        "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request", "runtime_credential_read",
        "runtime_audit_event_write", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_full_memory_runtime_open",
        "runtime_full_chat_runtime_open",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_extraction_attempts_persisted", "runtime_memory_candidates_persisted", "runtime_permission_requests_persisted", "runtime_permission_grants_applied", "runtime_permission_denials_applied",
        "runtime_permission_scopes_activated", "runtime_permission_grants_consumed", "runtime_memory_writes", "runtime_memory_store_mutations", "runtime_memory_deletes",
        "runtime_memory_exports", "runtime_memory_imports", "runtime_model_requests_dispatched", "runtime_model_responses_received", "runtime_network_requests",
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
        ("save_that", re.compile(r"^\s*save\s+that\s+", re.IGNORECASE)),
        ("store_that", re.compile(r"^\s*store\s+that\s+", re.IGNORECASE)),
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
            "memory_extraction_dry_run_only": True,
            "thin_runtime_alpha": True,
            "memory_extraction_dry_run_enabled": True,
            "memory_runtime_foundation_dependency_ready": True,
            "memory_write_permission_gate_dependency_ready": True,
            "deterministic_rule_extraction_enabled": True,
            "explicit_memory_trigger_detection_enabled": True,
            "candidate_normalization_enabled": True,
            "candidate_classification_enabled": True,
            "sensitive_pattern_screen_enabled": True,
            "candidate_fingerprint_runtime_enabled": True,
            "no_model_summary_required": True,
            "permission_gate_required": True,
            "manual_review_required": True,
            "privacy_review_required": True,
            "candidate_persist_runtime_disabled": True,
            "permission_grant_apply_disabled": True,
            "memory_write_runtime_disabled": True,
            "memory_store_mutation_disabled": True,
            "automatic_memory_extraction_disabled": True,
            "background_memory_loop_disabled": True,
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
            "next_sprint_174_memory_importance_pinning_policy_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "memory_extraction_dry_run_ready": True,
            "memory_extraction_dry_run_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_memory_extraction_dry_run_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "source_contract": "user_supplied_message_only",
            "extraction_method": "deterministic_rule_based_no_model",
            "permission_scope": "memory.write.single_candidate",
            "persistence_mode": "disabled",
            "next_sprint": "Sprint 174 Memory Importance and Pinning Policy",
        }

    @staticmethod
    def _normalize_whitespace(value: str) -> str:
        return " ".join(str(value or "").strip().split())

    def _extract_candidate_text(self, source_text: str) -> tuple[str, str, bool]:
        normalized = self._normalize_whitespace(source_text)
        for trigger_name, pattern in self.TRIGGER_PATTERNS:
            match = pattern.match(normalized)
            if match:
                candidate = self._normalize_whitespace(normalized[match.end():])
                return candidate[:1000], trigger_name, True
        return normalized[:1000], "no_explicit_trigger", False

    @staticmethod
    def _classify_candidate(candidate_text: str) -> tuple[str, str]:
        lowered = candidate_text.casefold()
        preference_markers = ("i prefer", "saya suka", "saya lebih suka", "preferensi", "my preference")
        project_markers = ("aura", "project", "proyek", "sprint", "atlas", "orion")
        workflow_markers = ("from now on", "mulai sekarang", "selalu", "jangan", "workflow", "aturan")
        identity_markers = ("my name", "nama saya", "i am", "saya adalah")
        if any(marker in lowered for marker in preference_markers):
            return "user_preference", "medium"
        if any(marker in lowered for marker in workflow_markers):
            return "workflow_rule", "medium"
        if any(marker in lowered for marker in identity_markers):
            return "identity_fact", "medium"
        if any(marker in lowered for marker in project_markers):
            return "project_fact", "medium"
        return "general_user_asserted_fact", "low"

    def _screen_sensitive_patterns(self, candidate_text: str) -> tuple[str, list[str]]:
        matches = [name for name, pattern in self.SENSITIVE_PATTERNS.items() if pattern.search(candidate_text)]
        if matches:
            return "sensitive_pattern_detected_review_required", matches
        return "no_common_sensitive_pattern_detected", []

    @staticmethod
    def _safe_preview(candidate_text: str, sensitive_matches: list[str]) -> str:
        if sensitive_matches:
            return "[redacted: sensitive pattern requires privacy review]"
        return candidate_text[:160]

    @staticmethod
    def _fingerprint(candidate_text: str, candidate_kind: str, source_kind: str) -> str:
        material = f"{source_kind}|{candidate_kind}|{candidate_text.casefold()}"
        return sha256(material.encode("utf-8")).hexdigest()[:16]

    def run_extraction_dry_run(self, source_text: str) -> dict[str, Any]:
        original = str(source_text or "")
        candidate_text, trigger, explicit_trigger = self._extract_candidate_text(original)
        candidate_valid = bool(candidate_text)
        candidate_kind, confidence = self._classify_candidate(candidate_text) if candidate_valid else ("invalid_empty_candidate", "none")
        sensitive_state, sensitive_matches = self._screen_sensitive_patterns(candidate_text) if candidate_valid else ("not_screened_empty_candidate", [])
        source_kind = "user_supplied_message"
        candidate_id = f"memory-candidate-{uuid4().hex[:12]}"
        fingerprint = self._fingerprint(candidate_text, candidate_kind, source_kind) if candidate_valid else "not_generated"
        packet = MemoryExtractionDryRunPacket(
            packet_id=f"memory-extraction-{uuid4().hex[:12]}",
            candidate_id=candidate_id,
            candidate_fingerprint=fingerprint,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        extraction_state = "candidate_preview_ready" if candidate_valid else "rejected_empty_candidate"
        return {
            "version": self.version,
            "session_mode": packet.session_mode,
            "extraction_packet_id": packet.packet_id,
            "candidate_id": packet.candidate_id,
            "candidate_fingerprint": packet.candidate_fingerprint,
            "source_kind": source_kind,
            "extraction_attempts": 1,
            "candidates_extracted": 1 if candidate_valid else 0,
            "extraction_method": "deterministic_rule_based_no_model",
            "trigger_detected": trigger,
            "explicit_memory_request": explicit_trigger,
            "candidate_kind": candidate_kind,
            "classification_confidence": confidence,
            "candidate_text_preview": self._safe_preview(candidate_text, sensitive_matches) if candidate_valid else "[empty candidate rejected]",
            "sensitive_state": sensitive_state,
            "sensitive_match_count": len(sensitive_matches),
            "extraction_state": extraction_state,
            "permission_scope": "memory.write.single_candidate",
            "permission_state": "required_not_granted",
            "gate_decision": "blocked_no_explicit_grant",
            "write_authorized": False,
            "candidate_persisted": False,
            "memory_state": "dry_run_preview_only_not_saved",
            "manual_review_required": True,
            "privacy_review_required": True,
            "next_sprint": "Sprint 174 Memory Importance and Pinning Policy",
            "extraction_attempts_persisted": 0,
            "permission_requests_persisted": 0,
            "permission_grants": 0,
            "memory_writes": 0,
            "memory_store_mutations": 0,
            "memory_deletes": 0,
            "memory_exports": 0,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "audit_events_written": 0,
            "commands_executed": 0,
            "arbitrary_files_read": 0,
            "arbitrary_files_wrote": 0,
            "runtime_execution": 0,
            "candidate_persist_runtime": "disabled",
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
            "aura_reply": (
                "Memory Extraction Dry Run selesai secara lokal dengan aturan deterministik tanpa model. Kandidat hanya ditampilkan sebagai preview untuk review manual dan privacy review. "
                "Permission tetap required_not_granted, sehingga kandidat tidak dipersist dan memory store tidak ditulis."
            ),
        }

    def render_extraction_dry_run(self, source_text: str) -> str:
        data = self.run_extraction_dry_run(source_text)
        labels = [
            ("Version", "version"), ("Session Mode", "session_mode"), ("Extraction Packet ID", "extraction_packet_id"),
            ("Candidate ID", "candidate_id"), ("Candidate Fingerprint", "candidate_fingerprint"), ("Source Kind", "source_kind"),
            ("Extraction Attempts", "extraction_attempts"), ("Candidates Extracted", "candidates_extracted"), ("Extraction Method", "extraction_method"),
            ("Trigger Detected", "trigger_detected"), ("Explicit Memory Request", "explicit_memory_request"), ("Candidate Kind", "candidate_kind"),
            ("Classification Confidence", "classification_confidence"), ("Candidate Text Preview", "candidate_text_preview"), ("Sensitive State", "sensitive_state"),
            ("Sensitive Match Count", "sensitive_match_count"), ("Extraction State", "extraction_state"), ("Permission Scope", "permission_scope"),
            ("Permission State", "permission_state"), ("Gate Decision", "gate_decision"), ("Write Authorized", "write_authorized"),
            ("Candidate Persisted", "candidate_persisted"), ("Memory State", "memory_state"), ("Manual Review Required", "manual_review_required"),
            ("Privacy Review Required", "privacy_review_required"), ("Next Sprint", "next_sprint"), ("Extraction Attempts Persisted", "extraction_attempts_persisted"),
            ("Permission Requests Persisted", "permission_requests_persisted"), ("Permission Grants", "permission_grants"), ("Memory Writes", "memory_writes"),
            ("Memory Store Mutations", "memory_store_mutations"), ("Memory Deletes", "memory_deletes"), ("Memory Exports", "memory_exports"),
            ("Model Requests", "model_requests"), ("Model Responses", "model_responses"), ("Network Requests", "network_requests"),
            ("Credentials Read", "credentials_read"), ("Audit Events Written", "audit_events_written"), ("Commands Executed", "commands_executed"),
            ("Arbitrary Files Read", "arbitrary_files_read"), ("Arbitrary Files Wrote", "arbitrary_files_wrote"), ("Runtime Execution", "runtime_execution"),
            ("Candidate Persist Runtime", "candidate_persist_runtime"), ("Permission Grant Runtime", "permission_grant_runtime"), ("Memory Write Runtime", "memory_write_runtime"),
            ("Memory Store Mutation", "memory_store_mutation"), ("Model Runtime", "model_runtime"), ("Network Runtime", "network_runtime"),
            ("Credential Runtime", "credential_runtime"), ("Audit Write Runtime", "audit_write_runtime"), ("Command Execution", "command_execution"),
            ("Arbitrary File Read", "arbitrary_file_read"), ("Arbitrary File Write", "arbitrary_file_write"), ("Full Memory Runtime", "full_memory_runtime"),
        ]
        lines = ["[memory-extraction] AURA Memory Extraction Dry Run Alpha"]
        for label, key in labels:
            lines.append(f"[memory-extraction] {label:<29}: {data[key]}")
        lines.append(f"[memory-extraction] AURA: {data['aura_reply']}")
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": self._normalize_whitespace(target) or "AURA memory extraction dry run",
            "items": [{"id": item, "preview_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def memory_explicit_trigger_detection_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_explicit_trigger_detection_plan", target, "trigger_detection_items")

    def memory_candidate_normalization_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_candidate_normalization_plan", target, "normalization_items")

    def memory_candidate_classification_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_candidate_classification_plan", target, "classification_items")

    def memory_sensitive_pattern_screen_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_sensitive_pattern_screen_plan", target, "sensitive_screen_items")

    def memory_candidate_fingerprint_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_candidate_fingerprint_handoff_plan", target, "fingerprint_handoff_items")

    def memory_permission_gate_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_gate_handoff_plan", target, "permission_review_items")

    def memory_manual_review_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_manual_review_handoff_plan", target, "permission_review_items")

    def memory_extraction_failure_boundary_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_extraction_failure_boundary_plan", target, "failure_boundary_items")

    def memory_control_center_extraction_preview_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_control_center_extraction_preview_plan", target, "control_center_handoff_items")

    def no_memory_extraction_unsafe_runtime_plan(self, target: str) -> dict[str, Any]:
        return self._plan("no_memory_extraction_unsafe_runtime_plan", target, "no_unsafe_runtime_items")

    def memory_extraction_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        packet = self._plan("memory_extraction_next_sprint_readiness_plan", target, "extraction_contract_items")
        packet.update({
            "sprint_173_complete_candidate": True,
            "next_sprint": "Sprint 174 Memory Importance and Pinning Policy",
            "importance_scoring_must_remain_preview_only": True,
            "memory_write_must_remain_blocked": True,
        })
        return packet
