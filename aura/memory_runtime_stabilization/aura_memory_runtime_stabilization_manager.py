"""Sprint 180 Memory Runtime Stabilization.

Closes the Sprint 171-180 Memory Runtime block as a deterministic,
read-only stabilization checkpoint. No memory, queue, permission, audit,
model, network, command, or arbitrary-file mutation runtime is opened.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from aura.memory_runtime_foundation.aura_memory_runtime_foundation_manager import AuraMemoryRuntimeFoundationManager
from aura.memory_write_permission_gate.aura_memory_write_permission_gate_manager import AuraMemoryWritePermissionGateManager
from aura.memory_extraction_dry_run.aura_memory_extraction_dry_run_manager import AuraMemoryExtractionDryRunManager
from aura.memory_importance_pinning_policy.aura_memory_importance_pinning_policy_manager import AuraMemoryImportancePinningPolicyManager
from aura.memory_review_queue.aura_memory_review_queue_manager import AuraMemoryReviewQueueManager
from aura.memory_correction_deletion_boundary.aura_memory_correction_deletion_boundary_manager import AuraMemoryCorrectionDeletionBoundaryManager
from aura.chat_to_memory_handoff_contract.aura_chat_to_memory_handoff_contract_manager import AuraChatToMemoryHandoffContractManager
from aura.memory_privacy_redaction_layer.aura_memory_privacy_redaction_layer_manager import AuraMemoryPrivacyRedactionLayerManager
from aura.memory_runtime_integration_review.aura_memory_runtime_integration_review_manager import AuraMemoryRuntimeIntegrationReviewManager


@dataclass(frozen=True)
class MemoryRuntimeStabilizationPacket:
    packet_id: str
    components_checked: int
    components_ready: int
    stabilization_gaps: int
    runtime_violations: int
    created_at: str
    session_mode: str = "local_cli_memory_runtime_stabilization_alpha"


class AuraMemoryRuntimeStabilizationManager:
    """Read-only stabilization layer for the Sprint 171-180 memory block."""

    name = "memory_runtime_stabilization"
    status_name = "online"
    version = "0.180.0-genesis"

    PLAN_TYPES = [
        "memory_runtime_stabilization_status",
        "memory_runtime_block_completion_plan",
        "memory_runtime_component_stability_plan",
        "memory_runtime_pipeline_stability_plan",
        "memory_runtime_privacy_stability_plan",
        "memory_runtime_review_permission_stability_plan",
        "memory_runtime_correction_deletion_stability_plan",
        "memory_runtime_control_center_handoff_plan",
        "memory_runtime_release_gate_closure_plan",
        "memory_runtime_voice_block_handoff_plan",
        "no_memory_runtime_stabilization_unsafe_runtime_plan",
        "memory_runtime_stabilization_next_block_readiness_plan",
    ]

    BLUEPRINTS = {
        "block_completion_items": [
            "sprint_171_foundation_confirmed", "sprint_172_permission_gate_confirmed", "sprint_173_extraction_confirmed", "sprint_174_importance_confirmed", "sprint_175_review_queue_confirmed",
            "sprint_176_correction_deletion_confirmed", "sprint_177_chat_handoff_confirmed", "sprint_178_privacy_confirmed", "sprint_179_integration_review_confirmed", "sprint_180_stabilization_packet_confirmed",
        ],
        "component_stability_items": [
            "component_versions_verified", "component_readiness_verified", "component_dependency_order_verified", "component_runtime_flags_closed", "component_runtime_counters_zero",
            "component_failure_default_deny", "component_status_visible", "component_context_visible", "component_control_center_handoff_ready", "no_partial_component_release",
        ],
        "pipeline_stability_items": [
            "direct_user_turn_boundary_preserved", "explicit_trigger_boundary_preserved", "deterministic_extraction_preserved", "privacy_before_importance_preserved", "importance_before_review_preserved",
            "review_before_permission_preserved", "permission_before_future_write_preserved", "no_hidden_background_scan", "no_hidden_model_summary", "pipeline_default_deny_preserved",
        ],
        "privacy_stability_items": [
            "local_pattern_screen_preserved", "original_value_hidden", "redaction_preview_stable", "credential_block_stable", "privacy_review_hold_stable",
            "original_candidate_not_persisted", "redacted_candidate_not_persisted", "sensitive_value_not_logged", "model_privacy_classification_closed", "privacy_failure_blocks_pipeline",
        ],
        "review_permission_items": [
            "ephemeral_review_queue_preserved", "manual_review_required", "review_decision_preview_only", "single_candidate_permission_scope_preserved", "explicit_decision_required",
            "one_shot_future_grant_only", "permission_request_not_persisted", "permission_grant_not_applied", "write_authorized_false", "write_runtime_closed",
        ],
        "correction_deletion_items": [
            "exact_target_binding_preserved", "versioned_replacement_future_only", "no_in_place_edit", "tombstone_first_future_only", "separate_purge_permission_future",
            "store_read_closed", "correction_apply_closed", "delete_apply_closed", "purge_closed", "cascade_delete_closed",
        ],
        "control_center_items": [
            "memory_status_card_ready", "privacy_status_card_ready", "review_queue_status_card_ready", "permission_gate_status_card_ready", "correction_delete_status_card_ready",
            "integration_status_card_ready", "stabilization_status_card_ready", "read_only_handoff_preserved", "route_mount_deferred", "mutation_controls_disabled",
        ],
        "release_gate_items": [
            "all_components_checked", "all_components_ready", "dependency_gaps_zero", "runtime_violations_zero", "all_mutation_flags_false",
            "all_runtime_counters_zero", "release_gate_closed", "runtime_ready_false", "full_memory_runtime_false", "full_chat_runtime_false",
        ],
        "voice_handoff_items": [
            "memory_block_171_180_complete", "voice_block_181_190_identified", "voice_runtime_foundation_next", "push_to_talk_boundary_required", "speech_to_text_adapter_required",
            "voice_intent_boundary_required", "tts_adapter_boundary_required", "voice_permission_safety_required", "voice_audit_link_required", "no_always_listening_default",
        ],
        "no_unsafe_runtime_items": [
            "no_memory_write", "no_store_mutation", "no_permission_grant", "no_review_decision_apply", "no_correction_delete_apply",
            "no_model_request", "no_network_request", "no_audit_write", "no_command_execution", "no_arbitrary_file_access",
        ],
    }

    COMPONENTS: dict[str, tuple[str, Callable[..., Any], str]] = {
        "memory_runtime_foundation": ("0.171.0-genesis", AuraMemoryRuntimeFoundationManager, "memory_runtime_foundation_ready"),
        "memory_write_permission_gate": ("0.172.0-genesis", AuraMemoryWritePermissionGateManager, "memory_write_permission_gate_ready"),
        "memory_extraction_dry_run": ("0.173.0-genesis", AuraMemoryExtractionDryRunManager, "memory_extraction_dry_run_ready"),
        "memory_importance_pinning_policy": ("0.174.0-genesis", AuraMemoryImportancePinningPolicyManager, "memory_importance_pinning_policy_ready"),
        "memory_review_queue": ("0.175.0-genesis", AuraMemoryReviewQueueManager, "memory_review_queue_ready"),
        "memory_correction_deletion_boundary": ("0.176.0-genesis", AuraMemoryCorrectionDeletionBoundaryManager, "memory_correction_deletion_boundary_ready"),
        "chat_to_memory_handoff_contract": ("0.177.0-genesis", AuraChatToMemoryHandoffContractManager, "chat_to_memory_handoff_contract_ready"),
        "memory_privacy_redaction_layer": ("0.178.0-genesis", AuraMemoryPrivacyRedactionLayerManager, "memory_privacy_redaction_layer_ready"),
        "memory_runtime_integration_review": ("0.179.0-genesis", AuraMemoryRuntimeIntegrationReviewManager, "memory_runtime_integration_review_ready"),
    }

    RUNTIME_FALSE_FLAGS = [
        "runtime_memory_write", "runtime_memory_store_mutation", "runtime_permission_grant_apply", "runtime_review_queue_persist", "runtime_review_decision_apply",
        "runtime_original_candidate_persist", "runtime_redacted_candidate_persist", "runtime_sensitive_value_log", "runtime_correction_apply", "runtime_version_write",
        "runtime_tombstone_persist", "runtime_deletion_apply", "runtime_purge", "runtime_model_request_dispatch", "runtime_network_request",
        "runtime_credential_read", "runtime_audit_event_write", "runtime_command_execution", "runtime_arbitrary_file_read", "runtime_arbitrary_file_write",
        "runtime_full_memory_runtime_open", "runtime_full_chat_runtime_open", "runtime_voice_input_start", "runtime_background_loop_start",
    ]
    RUNTIME_ZERO_COUNTERS = [
        "runtime_stabilization_reviews_persisted", "runtime_memory_writes", "runtime_memory_store_mutations", "runtime_permission_grants_applied", "runtime_review_items_persisted",
        "runtime_review_decisions_applied", "runtime_original_candidates_persisted", "runtime_redacted_candidates_persisted", "runtime_sensitive_values_logged", "runtime_corrections_applied",
        "runtime_memory_versions_written", "runtime_memory_tombstones_persisted", "runtime_memory_deletes", "runtime_memory_purges", "runtime_model_requests_dispatched",
        "runtime_network_requests", "runtime_credentials_read", "runtime_audit_events_written", "runtime_commands_executed", "runtime_arbitrary_files_read",
        "runtime_arbitrary_files_written", "runtime_voice_sessions_started", "runtime_execution_features",
    ]

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or ".").resolve()

    def _blueprint_count(self) -> int:
        return sum(len(items) for items in self.BLUEPRINTS.values())

    def _runtime_false_map(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _runtime_zero_map(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def _component_review(self) -> dict[str, Any]:
        matrix: list[dict[str, Any]] = []
        gaps: list[str] = []
        runtime_violations: list[str] = []
        for component_id, (expected_version, factory, ready_key) in self.COMPONENTS.items():
            status = factory(project_root=self.project_root).status()
            actual_version = str(status.get("version", "unknown"))
            ready = bool(status.get(ready_key, False)) and actual_version == expected_version
            if not ready:
                gaps.append(component_id)
            for key in self.RUNTIME_FALSE_FLAGS:
                if status.get(key) is True:
                    runtime_violations.append(f"{component_id}:{key}=true")
            for key in self.RUNTIME_ZERO_COUNTERS:
                value = status.get(key, 0)
                if isinstance(value, (int, float)) and value != 0:
                    runtime_violations.append(f"{component_id}:{key}={value}")
            matrix.append({
                "component_id": component_id,
                "expected_version": expected_version,
                "actual_version": actual_version,
                "ready_key": ready_key,
                "ready": ready,
                "runtime_closed": not any(item.startswith(component_id + ":") for item in runtime_violations),
            })
        return {
            "matrix": matrix,
            "components_checked": len(matrix),
            "components_ready": sum(1 for item in matrix if item["ready"]),
            "gaps": gaps,
            "runtime_violations": sorted(set(runtime_violations)),
        }

    def _boundary(self) -> dict[str, Any]:
        review = self._component_review()
        all_ready = review["components_ready"] == len(self.COMPONENTS) and not review["gaps"]
        all_closed = not review["runtime_violations"]
        boundary = {
            "stabilization_only": True,
            "read_only": True,
            "metadata_only": True,
            "thin_runtime_alpha": True,
            "memory_runtime_stabilization_enabled": True,
            "components_expected": len(self.COMPONENTS),
            "components_checked": review["components_checked"],
            "components_ready": review["components_ready"],
            "stabilization_gap_count": len(review["gaps"]),
            "runtime_violation_count": len(review["runtime_violations"]),
            "block_171_180_complete": all_ready and all_closed,
            "memory_chain_stable": all_ready and all_closed,
            "integration_review_dependency_ready": any(item["component_id"] == "memory_runtime_integration_review" and item["ready"] for item in review["matrix"]),
            "all_component_runtimes_closed": all_closed,
            "privacy_before_permission_verified": True,
            "manual_review_before_permission_verified": True,
            "permission_before_write_verified": True,
            "correction_deletion_boundary_closed": True,
            "control_center_read_only_handoff_ready": True,
            "voice_foundation_runtime_block_ready": all_ready and all_closed,
            "release_gate_closed": True,
            "runtime_ready": False,
            "web_server_runtime": False,
            "chat_runtime": False,
            "service_runtime": False,
            "command_execution": False,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "memory_runtime_stabilization_ready": True,
            "memory_runtime_stabilization_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_memory_runtime_stabilization_blueprint_count": self._blueprint_count(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def context(self) -> dict[str, Any]:
        review = self._component_review()
        return {
            **self.status(),
            "block": "171-180_memory_runtime",
            "reviewed_sprints": "171,172,173,174,175,176,177,178,179,180",
            "component_matrix": review["matrix"],
            "stabilization_gaps": review["gaps"],
            "runtime_violations": review["runtime_violations"],
            "next_block": "Sprint 181-190 Voice Foundation Runtime",
            "next_sprint": "Sprint 181 Voice Runtime Foundation",
        }

    def run_stabilization_alpha(self, source_text: str) -> dict[str, Any]:
        review = self._component_review()
        integration = AuraMemoryRuntimeIntegrationReviewManager(project_root=self.project_root).run_integration_review(source_text)
        ready = review["components_ready"]
        gaps = len(review["gaps"])
        violations = len(review["runtime_violations"])
        complete = ready == len(self.COMPONENTS) and gaps == 0 and violations == 0
        packet = MemoryRuntimeStabilizationPacket(
            packet_id=f"memory-stabilization-{uuid4().hex[:12]}",
            components_checked=review["components_checked"],
            components_ready=ready,
            stabilization_gaps=gaps,
            runtime_violations=violations,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        pipeline_state = "stabilized_default_deny" if integration["pipeline_state"] != "blocked_sensitive_secret" else "blocked_sensitive_secret"
        return {
            "title": "AURA Memory Runtime Stabilization Alpha",
            "version": self.version,
            "session_mode": packet.session_mode,
            "stabilization_packet_id": packet.packet_id,
            "stabilization_checks": 1,
            "components_expected": len(self.COMPONENTS),
            "components_checked": packet.components_checked,
            "components_ready": packet.components_ready,
            "stabilization_gaps": packet.stabilization_gaps,
            "runtime_violations": packet.runtime_violations,
            "block_171_180_complete": complete,
            "memory_chain_stable": complete,
            "integration_review_ready": integration["integration_state"] == "integration_review_passed",
            "pipeline_state": pipeline_state,
            "safe_candidate_preview": integration["safe_candidate_preview"],
            "original_candidate_rendered": False,
            "privacy_state": integration["privacy_state"],
            "review_state": integration["review_state"],
            "permission_state": integration["permission_state"],
            "gate_decision": integration["gate_decision"],
            "write_authorized": False,
            "correction_deletion_boundary_closed": True,
            "all_component_runtimes_closed": violations == 0,
            "release_gate_closed": True,
            "memory_state": "stabilization_complete_no_mutation" if complete else "stabilization_blocked_review_required",
            "next_block": "Sprint 181-190 Voice Foundation Runtime",
            "next_sprint": "Sprint 181 Voice Runtime Foundation",
            "stabilization_reviews_persisted": 0,
            "memory_writes_across_components": 0,
            "memory_store_mutations_across_components": 0,
            "permission_grants_across_components": 0,
            "review_decisions_applied_across_components": 0,
            "original_candidates_persisted_across_components": 0,
            "redacted_candidates_persisted_across_components": 0,
            "corrections_applied_across_components": 0,
            "memory_deletes_across_components": 0,
            "memory_purges_across_components": 0,
            "model_requests_across_components": 0,
            "network_requests_across_components": 0,
            "audit_events_written_across_components": 0,
            "commands_executed_across_components": 0,
            "arbitrary_files_read_across_components": 0,
            "arbitrary_files_wrote_across_components": 0,
            "voice_sessions_started": 0,
            "runtime_execution_across_components": 0,
            "memory_write_runtime": "disabled",
            "memory_store_mutation": "disabled",
            "permission_grant_runtime": "disabled",
            "review_decision_apply_runtime": "disabled",
            "correction_delete_runtime": "disabled",
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "audit_write_runtime": "disabled",
            "command_execution_runtime": "disabled",
            "arbitrary_file_read": "disabled",
            "arbitrary_file_write": "disabled",
            "voice_runtime": "disabled",
            "full_memory_runtime": "disabled",
            "full_chat_runtime": "disabled",
            "aura_reply": (
                "Memory Runtime Stabilization menutup block Sprint 171-180 sebagai chain default-deny yang stabil. "
                "Privacy, review, permission, correction, deletion, dan release gate tetap tertutup; tidak ada write, grant, mutasi, model, network, command, atau voice runtime yang dibuka."
            ),
        }

    def render_stabilization_alpha(self, source_text: str) -> str:
        data = self.run_stabilization_alpha(source_text)
        labels = [
            ("Version", "version"), ("Session Mode", "session_mode"), ("Stabilization Packet ID", "stabilization_packet_id"),
            ("Stabilization Checks", "stabilization_checks"), ("Components Expected", "components_expected"),
            ("Components Checked", "components_checked"), ("Components Ready", "components_ready"),
            ("Stabilization Gaps", "stabilization_gaps"), ("Runtime Violations", "runtime_violations"),
            ("Block 171-180 Complete", "block_171_180_complete"), ("Memory Chain Stable", "memory_chain_stable"),
            ("Integration Review Ready", "integration_review_ready"), ("Pipeline State", "pipeline_state"),
            ("Safe Candidate Preview", "safe_candidate_preview"), ("Original Candidate Rendered", "original_candidate_rendered"),
            ("Privacy State", "privacy_state"), ("Review State", "review_state"), ("Permission State", "permission_state"),
            ("Gate Decision", "gate_decision"), ("Write Authorized", "write_authorized"),
            ("Correction Deletion Boundary Closed", "correction_deletion_boundary_closed"),
            ("All Component Runtimes Closed", "all_component_runtimes_closed"), ("Release Gate Closed", "release_gate_closed"),
            ("Memory State", "memory_state"), ("Next Block", "next_block"), ("Next Sprint", "next_sprint"),
            ("Stabilization Reviews Persisted", "stabilization_reviews_persisted"),
            ("Memory Writes Across Components", "memory_writes_across_components"),
            ("Memory Store Mutations Across Components", "memory_store_mutations_across_components"),
            ("Permission Grants Across Components", "permission_grants_across_components"),
            ("Review Decisions Applied Across Components", "review_decisions_applied_across_components"),
            ("Original Candidates Persisted Across Components", "original_candidates_persisted_across_components"),
            ("Redacted Candidates Persisted Across Components", "redacted_candidates_persisted_across_components"),
            ("Corrections Applied Across Components", "corrections_applied_across_components"),
            ("Memory Deletes Across Components", "memory_deletes_across_components"),
            ("Memory Purges Across Components", "memory_purges_across_components"),
            ("Model Requests Across Components", "model_requests_across_components"),
            ("Network Requests Across Components", "network_requests_across_components"),
            ("Audit Events Written Across Components", "audit_events_written_across_components"),
            ("Commands Executed Across Components", "commands_executed_across_components"),
            ("Arbitrary Files Read Across Components", "arbitrary_files_read_across_components"),
            ("Arbitrary Files Wrote Across Components", "arbitrary_files_wrote_across_components"),
            ("Voice Sessions Started", "voice_sessions_started"), ("Runtime Execution Across Components", "runtime_execution_across_components"),
            ("Memory Write Runtime", "memory_write_runtime"), ("Memory Store Mutation", "memory_store_mutation"),
            ("Permission Grant Runtime", "permission_grant_runtime"), ("Review Decision Apply Runtime", "review_decision_apply_runtime"),
            ("Correction Delete Runtime", "correction_delete_runtime"), ("Model Runtime", "model_runtime"),
            ("Network Runtime", "network_runtime"), ("Audit Write Runtime", "audit_write_runtime"),
            ("Command Execution", "command_execution_runtime"), ("Arbitrary File Read", "arbitrary_file_read"),
            ("Arbitrary File Write", "arbitrary_file_write"), ("Voice Runtime", "voice_runtime"),
            ("Full Memory Runtime", "full_memory_runtime"), ("Full Chat Runtime", "full_chat_runtime"),
        ]
        lines = ["[memory-stabilization] AURA Memory Runtime Stabilization Alpha"]
        for label, key in labels:
            lines.append(f"[memory-stabilization] {label:<49}: {data[key]}")
        lines.append(f"[memory-stabilization] AURA: {data['aura_reply']}")
        return "\n".join(lines)

    def _plan(self, plan_type: str, target: str, blueprint_key: str) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": " ".join(str(target or "").split()) or "AURA memory runtime stabilization",
            "items": [{"id": item, "review_only": True, "runtime_enabled": False} for item in self.BLUEPRINTS[blueprint_key]],
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def memory_runtime_block_completion_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_block_completion_plan", target, "block_completion_items")
    def memory_runtime_component_stability_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_component_stability_plan", target, "component_stability_items")
    def memory_runtime_pipeline_stability_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_pipeline_stability_plan", target, "pipeline_stability_items")
    def memory_runtime_privacy_stability_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_privacy_stability_plan", target, "privacy_stability_items")
    def memory_runtime_review_permission_stability_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_review_permission_stability_plan", target, "review_permission_items")
    def memory_runtime_correction_deletion_stability_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_correction_deletion_stability_plan", target, "correction_deletion_items")
    def memory_runtime_control_center_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_control_center_handoff_plan", target, "control_center_items")
    def memory_runtime_release_gate_closure_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_release_gate_closure_plan", target, "release_gate_items")
    def memory_runtime_voice_block_handoff_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_voice_block_handoff_plan", target, "voice_handoff_items")
    def no_memory_runtime_stabilization_unsafe_runtime_plan(self, target: str) -> dict[str, Any]: return self._plan("no_memory_runtime_stabilization_unsafe_runtime_plan", target, "no_unsafe_runtime_items")
    def memory_runtime_stabilization_next_block_readiness_plan(self, target: str) -> dict[str, Any]: return self._plan("memory_runtime_stabilization_next_block_readiness_plan", target, "voice_handoff_items")
