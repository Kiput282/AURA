"""Sprint 174 Memory Importance and Pinning Policy.

This module evaluates one user-supplied memory candidate with deterministic,
explainable importance and durability rules. It may recommend that a candidate
be reviewed for long-term retention or future pinning, but it does not persist
the candidate, apply permission grants, pin or unpin memory, or mutate the
memory store.
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
class MemoryImportancePinningPolicyPacket:
    packet_id: str
    candidate_id: str
    candidate_fingerprint: str
    created_at: str
    session_mode: str = "local_cli_memory_importance_pinning_policy_alpha"


class AuraMemoryImportancePinningPolicyManager:
    """Preview importance and pinning recommendations without persistence."""

    name = "memory_importance_pinning_policy"
    status_name = "online"
    version = "0.174.0-genesis"

    PLAN_TYPES = [
        "memory_importance_pinning_policy_status",
        "memory_importance_scoring_plan",
        "memory_durability_signal_plan",
        "memory_temporary_signal_plan",
        "memory_retention_recommendation_plan",
        "memory_pin_eligibility_plan",
        "memory_pin_permission_boundary_plan",
        "memory_importance_manual_review_handoff_plan",
        "memory_importance_sensitive_boundary_plan",
        "memory_control_center_importance_preview_plan",
        "no_memory_importance_pinning_unsafe_runtime_plan",
        "memory_importance_next_sprint_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "policy_contract_items": [
            "memory_importance_pinning_policy_enabled", "single_candidate_policy_preview", "deterministic_scoring_only", "explainable_score_factors", "candidate_preview_only",
            "no_automatic_pin", "no_pin_mutation", "permission_gate_required", "manual_review_required", "memory_write_still_disabled",
        ],
        "importance_scoring_items": [
            "candidate_kind_base_score", "explicit_memory_request_bonus", "durability_signal_bonus", "temporary_signal_penalty", "sensitive_state_review_override",
            "score_clamped_zero_to_one_hundred", "importance_ephemeral_band", "importance_normal_band", "importance_important_band", "importance_critical_review_band",
        ],
        "durability_signal_items": [
            "project_policy_signal", "workflow_rule_signal", "long_term_signal", "always_signal", "from_now_on_signal",
            "local_first_signal", "permission_gated_signal", "stable_preference_signal", "durability_reason_visible", "no_model_inference",
        ],
        "temporary_signal_items": [
            "today_signal", "tomorrow_signal", "this_week_signal", "temporary_signal", "one_time_signal",
            "current_session_signal", "short_lived_candidate_penalty", "temporary_reason_visible", "ephemeral_recommendation_available", "no_silent_discard",
        ],
        "retention_recommendation_items": [
            "ephemeral_review_recommendation", "normal_retention_review", "long_term_retention_review", "critical_manual_review", "sensitive_candidate_hold",
            "retention_reason_visible", "retention_not_applied", "candidate_not_persisted", "review_queue_handoff_ready", "user_override_future",
        ],
        "pin_eligibility_items": [
            "pin_candidate_threshold", "durable_candidate_required", "temporary_candidate_not_eligible", "sensitive_candidate_not_auto_eligible", "explicit_pin_request_detected",
            "pin_recommendation_preview", "pin_state_not_pinned", "automatic_pin_false", "pin_mutation_disabled", "unpin_mutation_disabled",
        ],
        "permission_boundary_items": [
            "memory_write_scope_required", "future_pin_scope_separate", "write_permission_required_not_granted", "pin_permission_not_requested", "default_deny_preserved",
            "one_shot_write_grant_required", "manual_review_required", "privacy_review_required", "candidate_fingerprint_bound", "no_permission_bypass",
        ],
        "sensitive_boundary_items": [
            "email_pattern_screen", "phone_pattern_screen", "credential_keyword_screen", "private_key_marker_screen", "sensitive_preview_redacted",
            "sensitive_candidate_hold", "pin_eligibility_false_when_sensitive", "privacy_review_always_required", "no_sensitive_value_logging", "no_model_sensitive_classification",
        ],
        "control_center_handoff_items": [
            "importance_score_badge_ready", "importance_band_badge_ready", "durability_badge_ready", "retention_recommendation_card_ready", "pin_eligibility_badge_ready",
            "pin_recommendation_card_ready", "permission_state_badge_ready", "manual_review_badge_ready", "review_queue_handoff_ready", "pin_button_disabled",
        ],
        "no_unsafe_runtime_items": [
            "no_candidate_persist", "no_permission_grant_apply", "no_memory_write", "no_store_mutation", "no_pin_operation",
            "no_unpin_operation", "no_model_request", "no_network_request", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_importance_policy_persist", "runtime_memory_candidate_persist", "runtime_permission_request_persist", "runtime_permission_grant_apply", "runtime_permission_deny_apply",
        "runtime_permission_scope_activation", "runtime_permission_grant_consume", "runtime_memory_write", "runtime_memory_store_mutation", "runtime_memory_pin",
        "runtime_memory_unpin", "runtime_memory_delete", "runtime_memory_export", "runtime_memory_import", "runtime_automatic_memory_extraction",
        "runtime_background_memory_loop", "runtime_model_summary", "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start",
        "runtime_remote_api_call", "runtime_network_request", "runtime_credential_read", "runtime_audit_event_write", "runtime_command_execution",
        "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify",
        "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_full_memory_runtime_open", "runtime_full_chat_runtime_open",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_policy_evaluations_persisted", "runtime_memory_candidates_persisted", "runtime_permission_requests_persisted", "runtime_permission_grants_applied", "runtime_permission_denials_applied",
        "runtime_permission_scopes_activated", "runtime_permission_grants_consumed", "runtime_memory_writes", "runtime_memory_store_mutations", "runtime_memory_pins",
        "runtime_memory_unpins", "runtime_memory_deletes", "runtime_memory_exports", "runtime_memory_imports", "runtime_model_requests_dispatched",
        "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read", "runtime_audit_events_written", "runtime_commands_executed",
        "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified",
        "runtime_arbitrary_files_deleted", "runtime_execution_features",
    ]

    TRIGGER_PATTERNS = [
        ("remember_that", re.compile(r"^\s*remember\s+that\s+", re.IGNORECASE)),
        ("remember", re.compile(r"^\s*remember\s+", re.IGNORECASE)),
        ("ingat_bahwa", re.compile(r"^\s*ingat\s+bahwa\s+", re.IGNORECASE)),
        ("ingat", re.compile(r"^\s*ingat\s+", re.IGNORECASE)),
        ("catat_bahwa", re.compile(r"^\s*catat\s+bahwa\s+", re.IGNORECASE)),
        ("catat", re.compile(r"^\s*catat\s+", re.IGNORECASE)),
        ("pin_this", re.compile(r"^\s*pin\s+(?:this|that)\s+", re.IGNORECASE)),
    ]

    SENSITIVE_PATTERNS = {
        "email_pattern_detected": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
        "phone_pattern_detected": re.compile(r"(?<!\w)(?:\+?\d[\d .()\-]{7,}\d)(?!\w)"),
        "credential_keyword_detected": re.compile(r"\b(?:password|passwd|credential|secret|api[_ -]?key|access[_ -]?token|private[_ -]?key)\b", re.IGNORECASE),
        "private_key_marker_detected": re.compile(r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY", re.IGNORECASE),
    }

    DURABLE_MARKERS = (
        "from now on", "mulai sekarang", "always", "selalu", "long-term", "jangka panjang",
        "local-first", "permission-gated", "workflow", "aturan", "policy", "kebijakan",
    )
    TEMPORARY_MARKERS = (
        "today", "hari ini", "tomorrow", "besok", "this week", "minggu ini",
        "temporary", "sementara", "one time", "sekali ini", "current session", "sesi ini",
    )
    PIN_MARKERS = ("pin this", "pin that", "sematkan", "jadikan penting", "important", "penting")

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
            "memory_importance_pinning_policy_only": True,
            "thin_runtime_alpha": True,
            "memory_importance_pinning_policy_enabled": True,
            "memory_extraction_dry_run_dependency_ready": True,
            "memory_write_permission_gate_dependency_ready": True,
            "deterministic_importance_scoring_enabled": True,
            "explainable_score_factors_enabled": True,
            "durability_signal_detection_enabled": True,
            "temporary_signal_detection_enabled": True,
            "retention_recommendation_preview_enabled": True,
            "pin_recommendation_preview_enabled": True,
            "automatic_pin_disabled": True,
            "pin_mutation_disabled": True,
            "unpin_mutation_disabled": True,
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
            "manual_review_required": True,
            "privacy_review_required": True,
            "release_gate_closed": True,
            "next_sprint_175_memory_review_queue_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "memory_importance_pinning_policy_ready": True,
            "memory_importance_pinning_policy_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_memory_importance_pinning_policy_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        return {
            **self.status(),
            "source_contract": "single_user_supplied_candidate_only",
            "scoring_method": "deterministic_explainable_no_model",
            "importance_bands": ["ephemeral", "normal", "important", "critical_review"],
            "pin_mode": "recommendation_preview_only",
            "write_permission_scope": "memory.write.single_candidate",
            "future_pin_permission_scope": "memory.pin.single_candidate",
            "next_sprint": "Sprint 175 Memory Review Queue",
        }

    @staticmethod
    def _normalize_whitespace(value: str) -> str:
        return " ".join(str(value or "").strip().split())

    def _extract_candidate_text(self, source_text: str) -> tuple[str, str, bool]:
        normalized = self._normalize_whitespace(source_text)
        for trigger_name, pattern in self.TRIGGER_PATTERNS:
            match = pattern.match(normalized)
            if match:
                return self._normalize_whitespace(normalized[match.end():])[:1000], trigger_name, True
        return normalized[:1000], "no_explicit_trigger", False

    @staticmethod
    def _classify_candidate(candidate_text: str) -> tuple[str, int]:
        lowered = candidate_text.casefold()
        if any(marker in lowered for marker in ("i prefer", "saya suka", "saya lebih suka", "preferensi", "my preference")):
            return "user_preference", 50
        if any(marker in lowered for marker in ("from now on", "mulai sekarang", "selalu", "jangan", "workflow", "aturan", "policy", "kebijakan")):
            return "workflow_rule", 70
        if any(marker in lowered for marker in ("my name", "nama saya", "i am", "saya adalah")):
            return "identity_fact", 65
        if any(marker in lowered for marker in ("aura", "project", "proyek", "sprint", "atlas", "orion")):
            return "project_fact", 60
        return "general_user_asserted_fact", 35

    def _screen_sensitive_patterns(self, candidate_text: str) -> tuple[str, list[str]]:
        matches = [name for name, pattern in self.SENSITIVE_PATTERNS.items() if pattern.search(candidate_text)]
        if matches:
            return "sensitive_pattern_detected_review_hold", matches
        return "no_common_sensitive_pattern_detected", []

    @staticmethod
    def _safe_preview(candidate_text: str, sensitive_matches: list[str]) -> str:
        if sensitive_matches:
            return "[redacted: sensitive pattern requires privacy review]"
        return candidate_text[:160]

    @staticmethod
    def _fingerprint(candidate_text: str, candidate_kind: str) -> str:
        return sha256(f"user_supplied_message|{candidate_kind}|{candidate_text.casefold()}".encode("utf-8")).hexdigest()[:16]

    @staticmethod
    def _importance_band(score: int) -> str:
        if score >= 90:
            return "critical_review"
        if score >= 70:
            return "important"
        if score >= 40:
            return "normal"
        return "ephemeral"

    def run_policy_preview(self, source_text: str) -> dict[str, Any]:
        candidate_text, trigger, explicit_request = self._extract_candidate_text(source_text)
        candidate_valid = bool(candidate_text)
        candidate_kind, base_score = self._classify_candidate(candidate_text) if candidate_valid else ("invalid_empty_candidate", 0)
        lowered = candidate_text.casefold()
        durable_matches = [marker for marker in self.DURABLE_MARKERS if marker in lowered]
        temporary_matches = [marker for marker in self.TEMPORARY_MARKERS if marker in lowered]
        pin_matches = [marker for marker in self.PIN_MARKERS if marker in str(source_text or "").casefold()]
        sensitive_state, sensitive_matches = self._screen_sensitive_patterns(candidate_text) if candidate_valid else ("not_screened_empty_candidate", [])

        score_factors: list[str] = [f"candidate_kind_base:{base_score}"]
        score = base_score
        if explicit_request:
            score += 15
            score_factors.append("explicit_memory_request:+15")
        if durable_matches:
            score += 10
            score_factors.append("durability_signal:+10")
        if pin_matches:
            score += 5
            score_factors.append("explicit_pin_signal:+5")
        if temporary_matches:
            score -= 35
            score_factors.append("temporary_signal:-35")
        score = max(0, min(100, score))
        importance_band = self._importance_band(score)

        if temporary_matches:
            durability_state = "temporary_candidate"
            retention_recommendation = "ephemeral_review"
        elif durable_matches or candidate_kind in {"workflow_rule", "identity_fact", "project_fact"}:
            durability_state = "durable_candidate"
            retention_recommendation = "long_term_review" if score >= 70 else "normal_retention_review"
        else:
            durability_state = "durability_uncertain"
            retention_recommendation = "normal_retention_review" if score >= 40 else "ephemeral_review"

        pin_eligible = bool(candidate_valid and score >= 75 and not temporary_matches and not sensitive_matches)
        if sensitive_matches:
            retention_recommendation = "sensitive_candidate_hold"
            pin_recommendation = "not_eligible_sensitive_review"
        elif pin_eligible:
            pin_recommendation = "review_pin_candidate"
        else:
            pin_recommendation = "do_not_pin_yet"

        candidate_id = f"memory-candidate-{uuid4().hex[:12]}"
        fingerprint = self._fingerprint(candidate_text, candidate_kind) if candidate_valid else "not_generated"
        packet = MemoryImportancePinningPolicyPacket(
            packet_id=f"memory-importance-{uuid4().hex[:12]}",
            candidate_id=candidate_id,
            candidate_fingerprint=fingerprint,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "version": self.version,
            "session_mode": packet.session_mode,
            "policy_packet_id": packet.packet_id,
            "candidate_id": packet.candidate_id,
            "candidate_fingerprint": packet.candidate_fingerprint,
            "source_kind": "user_supplied_message",
            "policy_evaluations": 1,
            "candidate_previews": 1 if candidate_valid else 0,
            "scoring_method": "deterministic_explainable_no_model",
            "trigger_detected": trigger,
            "explicit_memory_request": explicit_request,
            "candidate_kind": candidate_kind,
            "candidate_text_preview": self._safe_preview(candidate_text, sensitive_matches) if candidate_valid else "[empty candidate rejected]",
            "importance_score": score,
            "importance_band": importance_band,
            "score_factors": ", ".join(score_factors),
            "durability_state": durability_state,
            "durability_signal_count": len(durable_matches),
            "temporary_signal_count": len(temporary_matches),
            "sensitive_state": sensitive_state,
            "sensitive_match_count": len(sensitive_matches),
            "retention_recommendation": retention_recommendation,
            "pin_eligible": pin_eligible,
            "pin_recommendation": pin_recommendation,
            "pin_state": "not_pinned",
            "automatic_pin_applied": False,
            "write_permission_scope": "memory.write.single_candidate",
            "write_permission_state": "required_not_granted",
            "future_pin_permission_scope": "memory.pin.single_candidate",
            "pin_permission_state": "not_requested_runtime_disabled",
            "gate_decision": "blocked_no_explicit_write_grant",
            "write_authorized": False,
            "candidate_persisted": False,
            "memory_state": "policy_preview_only_not_saved",
            "manual_review_required": True,
            "privacy_review_required": True,
            "next_sprint": "Sprint 175 Memory Review Queue",
            "policy_evaluations_persisted": 0,
            "permission_requests_persisted": 0,
            "permission_grants": 0,
            "memory_writes": 0,
            "memory_store_mutations": 0,
            "memory_pins": 0,
            "memory_unpins": 0,
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
            "memory_pin_runtime": "disabled",
            "memory_unpin_runtime": "disabled",
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "credential_runtime": "disabled",
            "audit_write_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_read": "disabled",
            "arbitrary_file_write": "disabled",
            "full_memory_runtime": "disabled",
            "aura_reply": (
                "Memory Importance and Pinning Policy selesai sebagai preview deterministik tanpa model. "
                "Skor, durability, retention, dan rekomendasi pin hanya metadata untuk review. "
                "Kandidat tidak dipersist, pin tidak diterapkan, dan memory write tetap diblokir tanpa izin eksplisit."
            ),
        }

    def render_policy_preview(self, source_text: str) -> str:
        data = self.run_policy_preview(source_text)
        labels = [
            ("Version", "version"), ("Session Mode", "session_mode"), ("Policy Packet ID", "policy_packet_id"),
            ("Candidate ID", "candidate_id"), ("Candidate Fingerprint", "candidate_fingerprint"), ("Source Kind", "source_kind"),
            ("Policy Evaluations", "policy_evaluations"), ("Candidate Previews", "candidate_previews"), ("Scoring Method", "scoring_method"),
            ("Trigger Detected", "trigger_detected"), ("Explicit Memory Request", "explicit_memory_request"), ("Candidate Kind", "candidate_kind"),
            ("Candidate Text Preview", "candidate_text_preview"), ("Importance Score", "importance_score"), ("Importance Band", "importance_band"),
            ("Score Factors", "score_factors"), ("Durability State", "durability_state"), ("Durability Signal Count", "durability_signal_count"),
            ("Temporary Signal Count", "temporary_signal_count"), ("Sensitive State", "sensitive_state"), ("Sensitive Match Count", "sensitive_match_count"),
            ("Retention Recommendation", "retention_recommendation"), ("Pin Eligible", "pin_eligible"), ("Pin Recommendation", "pin_recommendation"),
            ("Pin State", "pin_state"), ("Automatic Pin Applied", "automatic_pin_applied"), ("Write Permission Scope", "write_permission_scope"),
            ("Write Permission State", "write_permission_state"), ("Future Pin Permission Scope", "future_pin_permission_scope"), ("Pin Permission State", "pin_permission_state"),
            ("Gate Decision", "gate_decision"), ("Write Authorized", "write_authorized"), ("Candidate Persisted", "candidate_persisted"),
            ("Memory State", "memory_state"), ("Manual Review Required", "manual_review_required"), ("Privacy Review Required", "privacy_review_required"),
            ("Next Sprint", "next_sprint"), ("Policy Evaluations Persisted", "policy_evaluations_persisted"), ("Permission Requests Persisted", "permission_requests_persisted"),
            ("Permission Grants", "permission_grants"), ("Memory Writes", "memory_writes"), ("Memory Store Mutations", "memory_store_mutations"),
            ("Memory Pins", "memory_pins"), ("Memory Unpins", "memory_unpins"), ("Memory Deletes", "memory_deletes"),
            ("Memory Exports", "memory_exports"), ("Model Requests", "model_requests"), ("Model Responses", "model_responses"),
            ("Network Requests", "network_requests"), ("Credentials Read", "credentials_read"), ("Audit Events Written", "audit_events_written"),
            ("Commands Executed", "commands_executed"), ("Arbitrary Files Read", "arbitrary_files_read"), ("Arbitrary Files Wrote", "arbitrary_files_wrote"),
            ("Runtime Execution", "runtime_execution"), ("Candidate Persist Runtime", "candidate_persist_runtime"), ("Permission Grant Runtime", "permission_grant_runtime"),
            ("Memory Write Runtime", "memory_write_runtime"), ("Memory Store Mutation", "memory_store_mutation"), ("Memory Pin Runtime", "memory_pin_runtime"),
            ("Memory Unpin Runtime", "memory_unpin_runtime"), ("Model Runtime", "model_runtime"), ("Network Runtime", "network_runtime"),
            ("Credential Runtime", "credential_runtime"), ("Audit Write Runtime", "audit_write_runtime"), ("Command Execution", "command_execution"),
            ("Arbitrary File Read", "arbitrary_file_read"), ("Arbitrary File Write", "arbitrary_file_write"), ("Full Memory Runtime", "full_memory_runtime"),
        ]
        lines = ["[memory-importance] AURA Memory Importance and Pinning Policy Alpha"]
        for label, key in labels:
            lines.append(f"[memory-importance] {label:<30}: {data[key]}")
        lines.append(f"[memory-importance] AURA: {data['aura_reply']}")
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": self._normalize_whitespace(target) or "AURA memory importance and pinning policy",
            "items": [{"id": item, "preview_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def memory_importance_scoring_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_importance_scoring_plan", target, "importance_scoring_items")

    def memory_durability_signal_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_durability_signal_plan", target, "durability_signal_items")

    def memory_temporary_signal_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_temporary_signal_plan", target, "temporary_signal_items")

    def memory_retention_recommendation_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_retention_recommendation_plan", target, "retention_recommendation_items")

    def memory_pin_eligibility_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_pin_eligibility_plan", target, "pin_eligibility_items")

    def memory_pin_permission_boundary_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_pin_permission_boundary_plan", target, "permission_boundary_items")

    def memory_importance_manual_review_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_importance_manual_review_handoff_plan", target, "retention_recommendation_items")

    def memory_importance_sensitive_boundary_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_importance_sensitive_boundary_plan", target, "sensitive_boundary_items")

    def memory_control_center_importance_preview_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_control_center_importance_preview_plan", target, "control_center_handoff_items")

    def no_memory_importance_pinning_unsafe_runtime_plan(self, target: str) -> dict[str, Any]:
        return self._plan("no_memory_importance_pinning_unsafe_runtime_plan", target, "no_unsafe_runtime_items")

    def memory_importance_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        packet = self._plan("memory_importance_next_sprint_readiness_plan", target, "policy_contract_items")
        packet.update({
            "sprint_174_complete_candidate": True,
            "next_sprint": "Sprint 175 Memory Review Queue",
            "review_queue_must_remain_preview_only": True,
            "pin_and_memory_write_must_remain_blocked": True,
        })
        return packet
