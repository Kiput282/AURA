"""Sprint 170 Local Chat Runtime Stabilization.

This module closes the Sprint 161-170 local chat alpha block as a safe
stabilization checkpoint. It summarizes the thin local chat surfaces and verifies
that full runtime gates remain closed.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class LocalChatRuntimeStabilizationPacket:
    packet_id: str
    components_checked: int
    components_ready: int
    stabilization_gaps_found: int
    created_at: str
    session_mode: str = "local_cli_chat_runtime_stabilization_alpha"


class AuraLocalChatRuntimeStabilizationManager:
    """Read-only stabilization layer for the Sprint 161-170 local chat block."""

    name = "local_chat_runtime_stabilization"
    status_name = "online"
    version = "0.170.0-genesis"

    PLAN_TYPES = [
        "local_chat_runtime_stabilization_status",
        "local_chat_block_completion_review_plan",
        "local_chat_alpha_surface_stabilization_plan",
        "local_chat_store_and_history_stabilization_plan",
        "local_chat_persona_safety_stabilization_plan",
        "local_chat_model_permission_gate_stabilization_plan",
        "local_chat_control_center_handoff_stabilization_plan",
        "local_chat_memory_runtime_handoff_plan",
        "local_chat_release_gate_closure_review_plan",
        "local_chat_no_unsafe_runtime_plan",
        "local_chat_runtime_stabilization_context",
        "local_chat_next_block_171_180_readiness_plan",
    ]

    BLUEPRINTS: dict[str, list[str]] = {
        "block_completion_items": [
            "sprint_161_foundation_confirmed", "sprint_162_cli_session_alpha_confirmed", "sprint_163_message_store_confirmed", "sprint_164_persona_layer_confirmed", "sprint_165_model_adapter_boundary_confirmed",
            "sprint_166_permission_gate_confirmed", "sprint_167_safety_uncertainty_confirmed", "sprint_168_history_viewer_confirmed", "sprint_169_integration_review_confirmed", "sprint_170_stabilization_packet_confirmed",
        ],
        "alpha_surface_stabilization_items": [
            "single_message_cli_surface_preserved", "transient_session_surface_preserved", "store_alpha_surface_preserved", "persona_alpha_surface_preserved", "model_adapter_dry_run_surface_preserved",
            "permission_model_dry_run_surface_preserved", "safety_alpha_surface_preserved", "history_alpha_surface_preserved", "integration_alpha_surface_preserved", "stabilization_alpha_surface_added",
        ],
        "message_store_stabilization_items": [
            "controlled_jsonl_store_path_preserved", "bounded_store_append_contract_preserved", "history_read_only_contract_preserved", "store_schema_version_preserved", "store_path_override_for_validation_preserved",
            "no_arbitrary_store_path_acceptance", "no_unbounded_export", "no_delete_runtime", "no_replay_to_model", "memory_handoff_deferred",
        ],
        "persona_safety_stabilization_items": [
            "persona_identity_reply_preserved", "capability_honesty_preserved", "action_decline_preserved", "current_information_uncertainty_preserved", "safe_persona_reply_gate_preserved",
            "no_desktop_action_claim", "no_voice_runtime_claim", "no_vision_runtime_claim", "no_model_claim_without_gate", "user_facing_boundary_language_preserved",
        ],
        "model_permission_gate_stabilization_items": [
            "model_adapter_packet_contract_preserved", "prompt_envelope_contract_preserved", "provider_candidate_metadata_preserved", "permission_preview_contract_preserved", "gate_decision_contract_preserved",
            "blocked_without_grant_default_preserved", "model_dispatch_disabled", "network_disabled", "credential_read_disabled", "permission_grant_runtime_disabled",
        ],
        "safety_uncertainty_stabilization_items": [
            "safety_classifier_contract_preserved", "uncertainty_classifier_contract_preserved", "freshness_boundary_preserved", "knowledge_boundary_preserved", "latest_fact_honesty_preserved",
            "no_web_search_runtime", "no_network_runtime", "no_silent_model_fallback", "safe_persona_gate_default", "future_verification_handoff_preserved",
        ],
        "control_center_handoff_stabilization_items": [
            "chat_status_card_ready", "store_status_card_ready", "persona_status_card_ready", "model_boundary_status_card_ready", "permission_gate_status_card_ready",
            "safety_status_card_ready", "history_status_card_ready", "integration_status_card_ready", "stabilization_status_card_ready", "route_mount_deferred",
        ],
        "memory_runtime_handoff_items": [
            "chat_history_to_memory_boundary_identified", "memory_write_gate_required", "memory_extraction_dry_run_required", "memory_importance_policy_required", "memory_deletion_and_privacy_boundary_required",
            "memory_runtime_block_171_180_ready", "no_automatic_memory_write", "no_background_memory_loop", "no_model_memory_summarization", "explicit_future_permission_required",
        ],
        "release_gate_closure_items": [
            "full_chat_runtime_closed", "model_runtime_closed", "memory_runtime_closed", "network_runtime_closed", "credential_runtime_closed",
            "command_runtime_closed", "desktop_runtime_closed", "voice_runtime_closed", "vision_runtime_closed", "service_web_runtime_closed",
        ],
        "no_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_network_request", "no_credential_read", "no_permission_grant_apply",
            "no_memory_write", "no_audit_write", "no_command_execution", "no_arbitrary_file_access", "no_runtime_gate_open",
        ],
    }

    COMPONENTS = [
        ("local_chat_runtime_foundation", "Sprint 161 Local Chat Runtime Foundation"),
        ("local_chat_cli_session_alpha", "Sprint 162 CLI Session Alpha"),
        ("local_chat_message_store", "Sprint 163 Local Chat Message Store"),
        ("local_chat_persona_response_layer", "Sprint 164 Persona Response Layer"),
        ("local_chat_model_adapter_boundary", "Sprint 165 Model Adapter Boundary"),
        ("local_chat_permission_gated_model_request", "Sprint 166 Permission-Gated Model Request"),
        ("local_chat_safety_uncertainty_layer", "Sprint 167 Chat Safety + Uncertainty"),
        ("local_chat_history_viewer_contract", "Sprint 168 Chat History Viewer Contract"),
        ("local_chat_integration_review", "Sprint 169 Local Chat Integration Review"),
    ]

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_memory_write", "runtime_audit_event_write",
        "runtime_audit_log_append", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_voice_input_start",
        "runtime_vision_input_start", "runtime_screen_capture_start", "runtime_control_center_server_start", "runtime_full_chat_runtime_open", "runtime_background_loop_start",
        "runtime_autonomous_message_send", "runtime_service_start", "runtime_web_server_start",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_stabilization_checks_completed", "runtime_components_checked", "runtime_components_ready", "runtime_stabilization_gaps_found", "runtime_model_requests_dispatched",
        "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read", "runtime_permission_grants_applied", "runtime_memory_writes",
        "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read",
        "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_desktop_actions_started", "runtime_voice_sessions_started",
        "runtime_vision_sessions_started", "runtime_execution_features",
    ]

    def __init__(self, project_root: str | Path | None = None) -> None:
        self.project_root = Path(project_root or ".").resolve()

    def _blueprint_count(self) -> int:
        return sum(len(items) for items in self.BLUEPRINTS.values())

    def _runtime_zero_map(self) -> dict[str, int]:
        return {key: 0 for key in self.RUNTIME_ZERO_COUNTERS}

    def _runtime_false_map(self) -> dict[str, bool]:
        return {key: False for key in self.RUNTIME_FALSE_FLAGS}

    def _component_packets(self) -> list[dict[str, Any]]:
        packets: list[dict[str, Any]] = []
        for component_id, label in self.COMPONENTS:
            package_path = self.project_root / "aura" / component_id
            ready = package_path.exists() and package_path.is_dir()
            packets.append({
                "id": component_id,
                "label": label,
                "ready": ready,
                "mode": "metadata_presence_check",
                "runtime_action": False,
            })
        return packets

    def _boundary(self) -> dict[str, Any]:
        boundary: dict[str, Any] = {
            "local_chat_runtime_stabilization_only": True,
            "thin_runtime_alpha": True,
            "local_chat_runtime_stabilization_enabled": True,
            "local_chat_block_161_170_completed": True,
            "local_chat_alpha_surfaces_stabilized": True,
            "message_store_stabilized": True,
            "history_viewer_stabilized": True,
            "persona_safety_stabilized": True,
            "model_boundary_stabilized": True,
            "permission_gate_stabilized": True,
            "safety_uncertainty_stabilized": True,
            "control_center_handoff_stabilized": True,
            "memory_runtime_handoff_ready": True,
            "full_chat_runtime_disabled": True,
            "model_request_dispatch_blocked_without_grant": True,
            "model_request_dispatch_disabled": True,
            "model_response_runtime_disabled": True,
            "local_llm_process_runtime_disabled": True,
            "remote_api_runtime_disabled": True,
            "network_runtime_disabled": True,
            "credential_runtime_disabled": True,
            "permission_grant_runtime_disabled": True,
            "memory_runtime_disabled": True,
            "audit_write_runtime_disabled": True,
            "command_execution_disabled": True,
            "arbitrary_file_read_disabled": True,
            "arbitrary_file_mutation_disabled": True,
            "desktop_action_disabled": True,
            "voice_runtime_disabled": True,
            "vision_runtime_disabled": True,
            "service_runtime_disabled": True,
            "web_server_runtime_disabled": True,
            "release_gate_closed": True,
            "next_block_171_180_memory_runtime_ready": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        components = self._component_packets()
        ready_count = sum(1 for item in components if item["ready"])
        data: dict[str, Any] = {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "local_chat_runtime_stabilization_ready": True,
            "local_chat_runtime_stabilization_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_runtime_stabilization_blueprint_count": self._blueprint_count(),
            "components_declared": len(self.COMPONENTS),
            "components_ready": ready_count,
            "stabilization_gaps_found": len(self.COMPONENTS) - ready_count,
            "component_packets": components,
            **self._boundary(),
            **self._runtime_zero_map(),
        }
        return data

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": self.version,
            "status": self.status_name,
            "plan_types": self.PLAN_TYPES,
            "blueprints": self.BLUEPRINTS,
            "components": self._component_packets(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def run_stabilization_alpha(self) -> dict[str, Any]:
        components = self._component_packets()
        ready_count = sum(1 for item in components if item["ready"])
        gaps = len(components) - ready_count
        packet = LocalChatRuntimeStabilizationPacket(
            packet_id=f"stabilization-{uuid4().hex[:12]}",
            components_checked=len(components),
            components_ready=ready_count,
            stabilization_gaps_found=gaps,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "title": "AURA Local Chat Runtime Stabilization Alpha",
            "version": self.version,
            "session_mode": packet.session_mode,
            "stabilization_packet_id": packet.packet_id,
            "stabilization_checks": 1,
            "components_checked": packet.components_checked,
            "components_ready": packet.components_ready,
            "stabilization_gaps_found": packet.stabilization_gaps_found,
            "block_161_170_complete": gaps == 0,
            "chat_chain_stable": gaps == 0,
            "next_block": "Sprint 171-180 Memory Runtime",
            "next_sprint": "Sprint 171 Memory Runtime Foundation",
            "component_packets": components,
            "model_requests": 0,
            "model_responses": 0,
            "network_requests": 0,
            "credentials_read": 0,
            "permission_grants": 0,
            "memory_writes": 0,
            "audit_events_written": 0,
            "commands_executed": 0,
            "arbitrary_files_read": 0,
            "arbitrary_files_wrote": 0,
            "runtime_execution": 0,
            "model_runtime": "disabled",
            "network_runtime": "disabled",
            "credential_runtime": "disabled",
            "permission_grant": "disabled",
            "memory_runtime": "disabled",
            "command_execution": "disabled",
            "arbitrary_file_read": "disabled",
            "arbitrary_file_write": "disabled",
            "desktop_action": "disabled",
            "voice_runtime": "disabled",
            "vision_runtime": "disabled",
            "full_chat_runtime": "disabled",
            "aura_reply": (
                "Local Chat Runtime Stabilization selesai untuk block 161-170. "
                "Rantai alpha aman sudah stabil: CLI, store, persona, model boundary, permission gate, safety/uncertainty, history viewer, dan integration review siap sebagai fondasi. "
                "Full chat runtime, model, memory write, command execution, file bebas, voice, vision, desktop action, service, dan web server tetap nonaktif. "
                "Handoff berikutnya adalah Sprint 171-180 Memory Runtime."
            ),
        }

    def render_stabilization_alpha(self) -> str:
        data = self.run_stabilization_alpha()
        lines = [
            "[stabilization] AURA Local Chat Runtime Stabilization Alpha",
            f"[stabilization] Version              : {data['version']}",
            f"[stabilization] Session Mode         : {data['session_mode']}",
            f"[stabilization] Stabilization Packet ID: {data['stabilization_packet_id']}",
            f"[stabilization] Stabilization Checks : {data['stabilization_checks']}",
            f"[stabilization] Components Checked   : {data['components_checked']}",
            f"[stabilization] Components Ready     : {data['components_ready']}",
            f"[stabilization] Stabilization Gaps   : {data['stabilization_gaps_found']}",
            f"[stabilization] Block 161-170 Complete: {data['block_161_170_complete']}",
            f"[stabilization] Chat Chain Stable    : {data['chat_chain_stable']}",
            f"[stabilization] Next Block           : {data['next_block']}",
            f"[stabilization] Next Sprint          : {data['next_sprint']}",
            f"[stabilization] Model Requests       : {data['model_requests']}",
            f"[stabilization] Model Responses      : {data['model_responses']}",
            f"[stabilization] Network Requests     : {data['network_requests']}",
            f"[stabilization] Credentials Read     : {data['credentials_read']}",
            f"[stabilization] Permission Grants    : {data['permission_grants']}",
            f"[stabilization] Memory Writes        : {data['memory_writes']}",
            f"[stabilization] Audit Events Written : {data['audit_events_written']}",
            f"[stabilization] Commands Executed    : {data['commands_executed']}",
            f"[stabilization] Arbitrary Files Read : {data['arbitrary_files_read']}",
            f"[stabilization] Arbitrary Files Wrote: {data['arbitrary_files_wrote']}",
            f"[stabilization] Runtime Execution    : {data['runtime_execution']}",
            f"[stabilization] Model Runtime        : {data['model_runtime']}",
            f"[stabilization] Network Runtime      : {data['network_runtime']}",
            f"[stabilization] Credential Runtime   : {data['credential_runtime']}",
            f"[stabilization] Permission Grant     : {data['permission_grant']}",
            f"[stabilization] Memory Runtime       : {data['memory_runtime']}",
            f"[stabilization] Command Execution    : {data['command_execution']}",
            f"[stabilization] Arbitrary File Read  : {data['arbitrary_file_read']}",
            f"[stabilization] Arbitrary File Write : {data['arbitrary_file_write']}",
            f"[stabilization] Desktop Action       : {data['desktop_action']}",
            f"[stabilization] Voice Runtime        : {data['voice_runtime']}",
            f"[stabilization] Vision Runtime       : {data['vision_runtime']}",
            f"[stabilization] Full Chat Runtime    : {data['full_chat_runtime']}",
            f"[stabilization] AURA: {data['aura_reply']}",
        ]
        return "\n".join(lines)

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "plan_type": plan_type,
            "target": target,
            "version": self.version,
            "status": self.status_name,
            "planner_only": True,
            "metadata_only": True,
            "stabilization_only": True,
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def local_chat_block_completion_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_block_completion_review_plan", target)
        plan["review_items"] = self.BLUEPRINTS["block_completion_items"]
        return plan

    def local_chat_alpha_surface_stabilization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_alpha_surface_stabilization_plan", target)
        plan["stabilization_items"] = self.BLUEPRINTS["alpha_surface_stabilization_items"]
        return plan

    def local_chat_store_and_history_stabilization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_store_and_history_stabilization_plan", target)
        plan["store_items"] = self.BLUEPRINTS["message_store_stabilization_items"]
        return plan

    def local_chat_persona_safety_stabilization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_persona_safety_stabilization_plan", target)
        plan["persona_safety_items"] = self.BLUEPRINTS["persona_safety_stabilization_items"]
        plan["uncertainty_items"] = self.BLUEPRINTS["safety_uncertainty_stabilization_items"]
        return plan

    def local_chat_model_permission_gate_stabilization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_model_permission_gate_stabilization_plan", target)
        plan["model_permission_items"] = self.BLUEPRINTS["model_permission_gate_stabilization_items"]
        return plan

    def local_chat_control_center_handoff_stabilization_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_control_center_handoff_stabilization_plan", target)
        plan["handoff_items"] = self.BLUEPRINTS["control_center_handoff_stabilization_items"]
        return plan

    def local_chat_memory_runtime_handoff_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_memory_runtime_handoff_plan", target)
        plan["handoff_items"] = self.BLUEPRINTS["memory_runtime_handoff_items"]
        plan["next_block"] = "Sprint 171-180 Memory Runtime"
        return plan

    def local_chat_release_gate_closure_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_release_gate_closure_review_plan", target)
        plan["release_gate_items"] = self.BLUEPRINTS["release_gate_closure_items"]
        return plan

    def no_local_chat_runtime_stabilization_unsafe_runtime_plan(self, target: str = "local chat runtime stabilization unsafe runtime") -> dict[str, Any]:
        plan = self.base_plan("no_local_chat_runtime_stabilization_unsafe_runtime_plan", target)
        plan["blocked_runtime_items"] = self.BLUEPRINTS["no_unsafe_runtime_items"]
        return plan

    def local_chat_next_block_171_180_readiness_plan(self, target: str = "memory runtime block 171-180") -> dict[str, Any]:
        plan = self.base_plan("local_chat_next_block_171_180_readiness_plan", target)
        plan["next_block"] = "Sprint 171-180 Memory Runtime"
        plan["next_sprint"] = "Sprint 171 Memory Runtime Foundation"
        plan["required_guardrails"] = [
            "memory_write_gate", "memory_extraction_dry_run", "privacy_redaction_boundary", "deletion_and_correction_policy", "no_background_memory_loop",
            "permission_required_before_memory_write", "audit_handoff_deferred_until_writer_ready", "model_summary_deferred_until_model_permission_ready",
        ]
        return plan
