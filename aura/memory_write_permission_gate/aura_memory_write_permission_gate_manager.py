"""Sprint 172 Memory Write Permission Gate.

This module adds a default-deny, preview-only permission gate for a single
memory candidate. It creates in-memory candidate fingerprints and permission
request metadata, but it does not apply a permission grant, persist a candidate,
write the memory store, or activate the full memory runtime.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class MemoryWritePermissionGatePacket:
    packet_id: str
    candidate_id: str
    candidate_fingerprint: str
    permission_request_id: str
    created_at: str
    session_mode: str = "local_cli_memory_write_permission_gate_alpha"


class AuraMemoryWritePermissionGateManager:
    """Preview a one-candidate memory-write permission decision safely."""

    name = "memory_write_permission_gate"
    status_name = "online"
    version = "0.172.0-genesis"

    PLAN_TYPES = [
        "memory_write_permission_gate_status",
        "memory_permission_request_envelope_plan",
        "memory_permission_scope_validation_plan",
        "memory_candidate_fingerprint_plan",
        "memory_default_deny_policy_plan",
        "memory_one_shot_grant_plan",
        "memory_permission_expiry_plan",
        "memory_permission_audit_handoff_plan",
        "memory_control_center_permission_handoff_plan",
        "memory_permission_failure_boundary_plan",
        "no_memory_write_permission_gate_unsafe_runtime_plan",
        "memory_permission_gate_next_sprint_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "gate_contract_items": [
            "memory_write_permission_gate_enabled", "single_candidate_gate_contract", "default_deny_gate_state", "explicit_user_decision_required", "candidate_fingerprint_required",
            "permission_request_envelope_required", "permission_scope_validation_required", "one_shot_grant_only_future", "permission_expiry_required", "memory_write_still_disabled",
        ],
        "permission_request_envelope_items": [
            "permission_request_id", "candidate_id", "candidate_fingerprint", "requested_scope", "requested_action",
            "risk_level", "human_readable_reason", "source_kind", "requested_at", "decision_state",
        ],
        "scope_validation_items": [
            "scope_memory_write_single_candidate", "scope_exact_candidate_match", "scope_no_bulk_write", "scope_no_store_rewrite", "scope_no_delete",
            "scope_no_export", "scope_no_import", "scope_no_model_generated_candidate", "scope_no_arbitrary_file_source", "scope_unknown_rejected",
        ],
        "candidate_fingerprint_items": [
            "normalized_text_hash", "source_kind_bound", "candidate_kind_bound", "candidate_id_bound", "permission_request_bound",
            "fingerprint_preview_only", "no_plaintext_secret_hash_log", "no_store_path_hash", "no_cross_candidate_reuse", "fingerprint_mismatch_blocks",
        ],
        "default_deny_items": [
            "missing_grant_blocks", "missing_user_decision_blocks", "expired_grant_blocks", "scope_mismatch_blocks", "fingerprint_mismatch_blocks",
            "candidate_changed_blocks", "privacy_review_missing_blocks", "manual_review_missing_blocks", "audit_handoff_missing_blocks_future", "silent_approval_forbidden",
        ],
        "one_shot_grant_items": [
            "approve_once_future_only", "single_candidate_lifetime", "single_write_attempt_lifetime", "no_always_allow", "no_background_allow",
            "no_wildcard_scope", "no_session_wide_memory_write", "no_cross_source_grant", "grant_apply_runtime_disabled", "grant_reuse_forbidden",
        ],
        "expiry_and_revocation_items": [
            "short_expiry_future_required", "unused_grant_expiry", "used_grant_consumed", "candidate_change_invalidates", "user_cancel_invalidates",
            "privacy_change_invalidates", "manual_review_change_invalidates", "runtime_restart_requires_revalidation", "revocation_runtime_deferred", "expiry_runtime_deferred",
        ],
        "audit_handoff_items": [
            "permission_request_audit_preview", "gate_decision_audit_preview", "scope_validation_audit_preview", "fingerprint_match_audit_preview", "denial_reason_audit_preview",
            "approval_reason_audit_future", "grant_consumption_audit_future", "memory_write_audit_future", "audit_writer_runtime_disabled", "no_audit_file_append",
        ],
        "control_center_handoff_items": [
            "memory_permission_card_ready", "candidate_preview_card_ready", "scope_badge_ready", "risk_badge_ready", "default_deny_badge_ready",
            "approve_once_button_future", "deny_button_future", "edit_candidate_button_future", "expiry_badge_future", "write_action_button_disabled",
        ],
        "no_unsafe_runtime_items": [
            "no_permission_grant_apply", "no_memory_write", "no_memory_store_mutation", "no_memory_delete", "no_memory_export",
            "no_model_request", "no_network_request", "no_credential_read", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_permission_request_persist", "runtime_permission_grant_apply", "runtime_permission_deny_apply", "runtime_permission_scope_activation", "runtime_permission_scope_revocation",
        "runtime_permission_expiry_timer", "runtime_permission_grant_consume", "runtime_memory_candidate_persist", "runtime_memory_write", "runtime_memory_store_mutation",
        "runtime_memory_delete", "runtime_memory_export", "runtime_memory_import", "runtime_background_memory_loop", "runtime_model_request_dispatch",
        "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request", "runtime_credential_read",
        "runtime_audit_event_write", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_full_memory_runtime_open",
        "runtime_full_chat_runtime_open",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_gate_checks_completed", "runtime_permission_requests_persisted", "runtime_permission_grants_applied", "runtime_permission_denials_applied", "runtime_permission_scopes_activated",
        "runtime_permission_scopes_revoked", "runtime_permission_expiry_timers_started", "runtime_permission_grants_consumed", "runtime_memory_candidates_persisted", "runtime_memory_writes",
        "runtime_memory_store_mutations", "runtime_memory_deletes", "runtime_memory_exports", "runtime_memory_imports", "runtime_model_requests_dispatched",
        "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read", "runtime_audit_events_written", "runtime_commands_executed",
        "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read", "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified",
        "runtime_arbitrary_files_deleted", "runtime_execution_features",
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
            "memory_write_permission_gate_only": True,
            "thin_runtime_alpha": True,
            "memory_write_permission_gate_enabled": True,
            "memory_runtime_foundation_dependency_ready": True,
            "permission_request_envelope_preview_enabled": True,
            "permission_scope_validation_enabled": True,
            "candidate_fingerprint_runtime_enabled": True,
            "explicit_user_decision_required": True,
            "default_deny_without_grant": True,
            "one_shot_grant_required": True,
            "permission_expiry_required": True,
            "manual_review_required": True,
            "privacy_review_required": True,
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
            "next_sprint_173_memory_extraction_dry_run_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "memory_write_permission_gate_ready": True,
            "memory_write_permission_gate_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_memory_write_permission_gate_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "plan_types": self.PLAN_TYPES,
            "blueprints": self.BLUEPRINTS,
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    @staticmethod
    def _normalize(source_text: str) -> str:
        return " ".join((source_text or "").strip().split())

    def _candidate_preview(self, source_text: str) -> dict[str, Any]:
        normalized = self._normalize(source_text)
        candidate_id = f"memory-candidate-{uuid4().hex[:12]}"
        digest_input = f"user_note_candidate|user_supplied_message|{normalized}".encode("utf-8")
        fingerprint = sha256(digest_input).hexdigest()[:16]
        return {
            "candidate_id": candidate_id,
            "candidate_kind": "user_note_candidate",
            "source_kind": "user_supplied_message",
            "source_ref": "local_cli_argument",
            "text_preview": normalized[:160] if normalized else "empty_preview",
            "candidate_fingerprint": fingerprint,
            "privacy_state": "review_required",
            "manual_review_state": "required",
            "write_state": "preview_only_not_saved",
        }

    def run_permission_gate_alpha(self, source_text: str) -> dict[str, Any]:
        candidate = self._candidate_preview(source_text)
        permission_request_id = f"memory-permission-{uuid4().hex[:12]}"
        packet = MemoryWritePermissionGatePacket(
            packet_id=f"memory-write-gate-{uuid4().hex[:12]}",
            candidate_id=candidate["candidate_id"],
            candidate_fingerprint=candidate["candidate_fingerprint"],
            permission_request_id=permission_request_id,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "title": "AURA Memory Write Permission Gate Alpha",
            "version": self.version,
            "session_mode": packet.session_mode,
            "gate_packet_id": packet.packet_id,
            "candidate_id": packet.candidate_id,
            "candidate_fingerprint": packet.candidate_fingerprint,
            "permission_request_id": packet.permission_request_id,
            "source_kind": candidate["source_kind"],
            "candidate_previews": 1,
            "permission_requests": 1,
            "permission_scope": "memory.write.single_candidate",
            "risk_level": "medium",
            "approval_mode": "approve_once_future",
            "grant_lifetime": "one_shot_future",
            "explicit_decision_required": True,
            "decision_state": "required_not_granted",
            "gate_decision": "blocked_no_explicit_grant",
            "write_authorized": False,
            "memory_state": "preview_only_not_saved",
            "candidate_preview": candidate,
            "next_sprint": "Sprint 173 Memory Extraction Dry Run",
            "permission_requests_persisted": 0,
            "permission_grants": 0,
            "permission_denials_applied": 0,
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
                "Memory Write Permission Gate aktif dalam mode default-deny. Kandidat dan permission request hanya dibuat di memori proses sebagai preview. "
                "Tanpa grant eksplisit yang cocok dengan satu fingerprint kandidat, write tetap diblokir. Sprint ini tidak menerapkan grant dan tidak menulis memory store."
            ),
        }

    def render_permission_gate_alpha(self, source_text: str) -> str:
        data = self.run_permission_gate_alpha(source_text)
        lines = [
            "[memory-gate] AURA Memory Write Permission Gate Alpha",
            f"[memory-gate] Version                 : {data['version']}",
            f"[memory-gate] Session Mode            : {data['session_mode']}",
            f"[memory-gate] Gate Packet ID          : {data['gate_packet_id']}",
            f"[memory-gate] Candidate ID            : {data['candidate_id']}",
            f"[memory-gate] Candidate Fingerprint   : {data['candidate_fingerprint']}",
            f"[memory-gate] Permission Request ID   : {data['permission_request_id']}",
            f"[memory-gate] Source Kind             : {data['source_kind']}",
            f"[memory-gate] Candidate Previews      : {data['candidate_previews']}",
            f"[memory-gate] Permission Requests     : {data['permission_requests']}",
            f"[memory-gate] Permission Scope        : {data['permission_scope']}",
            f"[memory-gate] Risk Level              : {data['risk_level']}",
            f"[memory-gate] Approval Mode           : {data['approval_mode']}",
            f"[memory-gate] Grant Lifetime          : {data['grant_lifetime']}",
            f"[memory-gate] Explicit Decision Required: {data['explicit_decision_required']}",
            f"[memory-gate] Decision State          : {data['decision_state']}",
            f"[memory-gate] Gate Decision           : {data['gate_decision']}",
            f"[memory-gate] Write Authorized        : {data['write_authorized']}",
            f"[memory-gate] Memory State            : {data['memory_state']}",
            f"[memory-gate] Next Sprint             : {data['next_sprint']}",
            f"[memory-gate] Permission Requests Persisted: {data['permission_requests_persisted']}",
            f"[memory-gate] Permission Grants       : {data['permission_grants']}",
            f"[memory-gate] Permission Denials Applied: {data['permission_denials_applied']}",
            f"[memory-gate] Memory Writes           : {data['memory_writes']}",
            f"[memory-gate] Memory Store Mutations  : {data['memory_store_mutations']}",
            f"[memory-gate] Memory Deletes          : {data['memory_deletes']}",
            f"[memory-gate] Memory Exports          : {data['memory_exports']}",
            f"[memory-gate] Model Requests          : {data['model_requests']}",
            f"[memory-gate] Model Responses         : {data['model_responses']}",
            f"[memory-gate] Network Requests        : {data['network_requests']}",
            f"[memory-gate] Credentials Read        : {data['credentials_read']}",
            f"[memory-gate] Audit Events Written    : {data['audit_events_written']}",
            f"[memory-gate] Commands Executed       : {data['commands_executed']}",
            f"[memory-gate] Arbitrary Files Read    : {data['arbitrary_files_read']}",
            f"[memory-gate] Arbitrary Files Wrote   : {data['arbitrary_files_wrote']}",
            f"[memory-gate] Runtime Execution       : {data['runtime_execution']}",
            f"[memory-gate] Permission Grant Runtime: {data['permission_grant_runtime']}",
            f"[memory-gate] Memory Write Runtime    : {data['memory_write_runtime']}",
            f"[memory-gate] Memory Store Mutation   : {data['memory_store_mutation']}",
            f"[memory-gate] Model Runtime           : {data['model_runtime']}",
            f"[memory-gate] Network Runtime         : {data['network_runtime']}",
            f"[memory-gate] Credential Runtime      : {data['credential_runtime']}",
            f"[memory-gate] Audit Write Runtime     : {data['audit_write_runtime']}",
            f"[memory-gate] Command Execution       : {data['command_execution']}",
            f"[memory-gate] Arbitrary File Read     : {data['arbitrary_file_read']}",
            f"[memory-gate] Arbitrary File Write    : {data['arbitrary_file_write']}",
            f"[memory-gate] Full Memory Runtime     : {data['full_memory_runtime']}",
            f"[memory-gate] AURA: {data['aura_reply']}",
        ]
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": self._normalize(target) or "AURA memory write permission gate",
            "items": [{"id": item, "preview_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def memory_permission_request_envelope_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_request_envelope_plan", target, "permission_request_envelope_items")

    def memory_permission_scope_validation_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_scope_validation_plan", target, "scope_validation_items")

    def memory_candidate_fingerprint_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_candidate_fingerprint_plan", target, "candidate_fingerprint_items")

    def memory_default_deny_policy_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_default_deny_policy_plan", target, "default_deny_items")

    def memory_one_shot_grant_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_one_shot_grant_plan", target, "one_shot_grant_items")

    def memory_permission_expiry_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_expiry_plan", target, "expiry_and_revocation_items")

    def memory_permission_audit_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_audit_handoff_plan", target, "audit_handoff_items")

    def memory_control_center_permission_handoff_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_control_center_permission_handoff_plan", target, "control_center_handoff_items")

    def memory_permission_failure_boundary_plan(self, target: str) -> dict[str, Any]:
        return self._plan("memory_permission_failure_boundary_plan", target, "default_deny_items")

    def no_memory_write_permission_gate_unsafe_runtime_plan(self, target: str) -> dict[str, Any]:
        return self._plan("no_memory_write_permission_gate_unsafe_runtime_plan", target, "no_unsafe_runtime_items")

    def memory_permission_gate_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        packet = self._plan("memory_permission_gate_next_sprint_readiness_plan", target, "gate_contract_items")
        packet.update({
            "sprint_172_complete_candidate": True,
            "next_sprint": "Sprint 173 Memory Extraction Dry Run",
            "memory_extraction_must_remain_dry_run": True,
            "memory_write_must_remain_blocked": True,
        })
        return packet
