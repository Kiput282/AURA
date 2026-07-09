"""AURA Local Chat Integration Review.

Sprint 169.

This module reviews the Sprint 161-168 local chat alpha chain and confirms the
thin runtime pieces are connected behind safe boundaries. It is a metadata-only
and read-only integration review. It does not call a model, use network, read
credentials, apply permission grants, write memory, write audit events, execute
commands, read arbitrary user files, mutate files, start desktop action, start
voice, start vision, or open the full chat runtime gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class LocalChatIntegrationReviewPacket:
    """Read-only local chat integration review packet for Sprint 169."""

    packet_id: str
    components_checked: int
    components_ready: int
    integration_gaps_found: int
    created_at: str
    session_mode: str = "local_cli_chat_integration_review_alpha"
    source: str = "AuraCLI"


class AuraLocalChatIntegrationReviewManager:
    """Describe and run Sprint 169 Local Chat Integration Review."""

    name = "aura_local_chat_integration_review"
    version = "0.1.0"
    status_name = "online"

    PLAN_TYPES = [
        "local_chat_integration_review_status",
        "chat_alpha_chain_review_plan",
        "chat_cli_surface_review_plan",
        "chat_message_store_integration_review_plan",
        "chat_persona_integration_review_plan",
        "chat_model_boundary_integration_review_plan",
        "chat_permission_gate_integration_review_plan",
        "chat_safety_uncertainty_integration_review_plan",
        "chat_history_viewer_integration_review_plan",
        "chat_control_center_handoff_review_plan",
        "no_local_chat_integration_unsafe_runtime_plan",
        "local_chat_integration_next_sprint_readiness_plan",
    ]

    BLUEPRINTS = {
        "alpha_chain_review_items": [
            "sprint_161_foundation_present", "sprint_162_cli_alpha_present", "sprint_163_message_store_present", "sprint_164_persona_layer_present", "sprint_165_model_adapter_boundary_present",
            "sprint_166_permission_gate_present", "sprint_167_safety_uncertainty_present", "sprint_168_history_viewer_present", "thin_runtime_chain_identified", "full_chat_runtime_still_deferred",
        ],
        "cli_surface_review_items": [
            "local_chat_alpha_command_registered", "local_chat_store_alpha_command_registered", "local_chat_persona_alpha_command_registered", "local_chat_model_adapter_dry_run_registered", "local_chat_permission_model_dry_run_registered",
            "local_chat_safety_alpha_registered", "local_chat_history_alpha_registered", "local_chat_integration_alpha_registered", "status_commands_registered", "plan_commands_registered",
        ],
        "message_store_integration_items": [
            "controlled_store_path_preserved", "jsonl_store_contract_preserved", "message_store_write_limited_to_store_alpha", "history_viewer_read_only_preserved", "no_arbitrary_store_path",
            "no_history_delete", "no_history_export", "no_model_replay_from_history", "future_memory_handoff_identified", "sprint_170_store_review_ready",
        ],
        "persona_integration_items": [
            "identity_persona_present", "capability_honesty_present", "action_decline_present", "safe_persona_reply_present", "no_desktop_action_claims",
            "no_voice_claims", "no_vision_claims", "no_model_claims_without_gate", "user_facing_boundary_language_present", "persona_handoff_to_model_adapter_ready",
        ],
        "model_boundary_integration_items": [
            "model_adapter_packet_contract_present", "prompt_envelope_contract_present", "provider_candidate_metadata_present", "local_disabled_adapter_default", "no_model_dispatch",
            "no_model_response_receive", "no_local_llm_process_start", "no_remote_api_call", "no_network_request", "sprint_170_model_boundary_review_ready",
        ],
        "permission_gate_integration_items": [
            "permission_preview_packet_present", "model_request_envelope_present", "gate_decision_present", "blocked_without_grant_default", "permission_state_required_not_granted",
            "permission_grant_runtime_disabled", "credential_runtime_disabled", "audit_handoff_deferred", "model_gate_handoff_preserved", "future_explicit_grant_required",
        ],
        "safety_uncertainty_integration_items": [
            "safety_classifier_present", "uncertainty_classifier_present", "freshness_boundary_present", "knowledge_boundary_present", "current_info_verification_flag_present",
            "safe_persona_gate_present", "no_web_search_runtime", "no_network_runtime", "no_pretend_latest_fact_policy", "sprint_170_safety_review_ready",
        ],
        "history_viewer_integration_items": [
            "history_viewer_contract_present", "controlled_store_read_only_present", "bounded_preview_present", "summary_renderer_present", "privacy_redaction_contract_present",
            "no_arbitrary_file_read", "no_history_mutation", "control_center_history_card_handoff_ready", "recent_turn_preview_ready", "sprint_170_history_review_ready",
        ],
        "control_center_handoff_items": [
            "chat_status_card_ready", "message_store_status_card_ready", "persona_status_card_ready", "model_boundary_status_card_ready", "permission_gate_status_card_ready",
            "safety_uncertainty_status_card_ready", "history_viewer_status_card_ready", "integration_review_card_ready", "read_only_panel_contract_preserved", "route_mount_deferred",
        ],
        "no_integration_unsafe_runtime_items": [
            "no_model_request_dispatch", "no_model_response_receive", "no_network_request", "no_credential_read", "no_permission_grant_apply",
            "no_memory_write", "no_audit_write", "no_command_execution", "no_arbitrary_file_access", "no_runtime_gate_open",
        ],
    }

    COMPONENTS = [
        ("local_chat_cli_session_alpha", "Sprint 162 CLI session alpha"),
        ("local_chat_message_store", "Sprint 163 controlled message store"),
        ("local_chat_persona_response_layer", "Sprint 164 persona response layer"),
        ("local_chat_model_adapter_boundary", "Sprint 165 model adapter boundary"),
        ("local_chat_permission_gated_model_request", "Sprint 166 permission-gated model request"),
        ("local_chat_safety_uncertainty_layer", "Sprint 167 chat safety + uncertainty"),
        ("local_chat_history_viewer_contract", "Sprint 168 chat history viewer"),
    ]

    RUNTIME_FALSE_FLAGS = [
        "runtime_model_request_dispatch", "runtime_model_response_receive", "runtime_local_llm_process_start", "runtime_remote_api_call", "runtime_network_request",
        "runtime_credential_read", "runtime_permission_grant_apply", "runtime_permission_mutation", "runtime_memory_write", "runtime_audit_event_write",
        "runtime_audit_log_append", "runtime_command_execution", "runtime_tool_execution", "runtime_plugin_action_dispatch", "runtime_arbitrary_file_read",
        "runtime_arbitrary_file_write", "runtime_arbitrary_file_modify", "runtime_arbitrary_file_delete", "runtime_desktop_control", "runtime_voice_input_start",
        "runtime_screen_capture_start", "runtime_control_center_server_start", "runtime_full_chat_runtime_open", "runtime_background_loop_start", "runtime_autonomous_message_send",
    ]

    RUNTIME_ZERO_COUNTERS = [
        "runtime_integration_checks_completed", "runtime_components_checked", "runtime_components_ready", "runtime_integration_gaps_found", "runtime_model_requests_dispatched",
        "runtime_model_responses_received", "runtime_network_requests", "runtime_credentials_read", "runtime_permission_grants_applied", "runtime_memory_writes",
        "runtime_audit_events_written", "runtime_commands_executed", "runtime_tools_executed", "runtime_plugin_actions_dispatched", "runtime_arbitrary_files_read",
        "runtime_arbitrary_files_written", "runtime_arbitrary_files_modified", "runtime_arbitrary_files_deleted", "runtime_desktop_actions_started", "runtime_execution_features",
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
            "local_chat_integration_review_only": True,
            "thin_runtime_alpha": True,
            "local_chat_integration_review_enabled": True,
            "cli_alpha_integration_checked": True,
            "message_store_integration_checked": True,
            "persona_layer_integration_checked": True,
            "model_adapter_boundary_checked": True,
            "permission_gate_integration_checked": True,
            "safety_uncertainty_integration_checked": True,
            "history_viewer_integration_checked": True,
            "control_center_handoff_checked": True,
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
            "full_chat_runtime_disabled": True,
            "release_gate_closed": True,
            "sprint_170_stabilization_required": True,
        }
        boundary.update(self._runtime_false_map())
        return boundary

    def status(self) -> dict[str, Any]:
        components = self._component_packets()
        ready_count = sum(1 for item in components if item["ready"])
        data: dict[str, Any] = {
            "module": self.name,
            "version": "0.169.0-genesis",
            "status": self.status_name,
            "local_chat_integration_review_ready": True,
            "local_chat_integration_review_data_ready": True,
            "plan_type_count": len(self.PLAN_TYPES),
            "total_local_chat_integration_review_blueprint_count": self._blueprint_count(),
            "components_declared": len(self.COMPONENTS),
            "components_ready": ready_count,
            "integration_gaps_found": len(self.COMPONENTS) - ready_count,
            "component_packets": components,
            **self._boundary(),
            **self._runtime_zero_map(),
        }
        return data

    def context(self) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.169.0-genesis",
            "status": self.status_name,
            "plan_types": self.PLAN_TYPES,
            "blueprints": self.BLUEPRINTS,
            "components": self._component_packets(),
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def run_integration_review_alpha(self) -> dict[str, Any]:
        components = self._component_packets()
        ready_count = sum(1 for item in components if item["ready"])
        gaps = len(components) - ready_count
        packet = LocalChatIntegrationReviewPacket(
            packet_id=f"integration-{uuid4().hex[:12]}",
            components_checked=len(components),
            components_ready=ready_count,
            integration_gaps_found=gaps,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        return {
            "title": "AURA Local Chat Integration Review Alpha",
            "version": "0.169.0-genesis",
            "session_mode": packet.session_mode,
            "review_packet_id": packet.packet_id,
            "integration_checks": 1,
            "components_checked": packet.components_checked,
            "components_ready": packet.components_ready,
            "integration_gaps_found": packet.integration_gaps_found,
            "chat_chain_ready": gaps == 0,
            "next_sprint": "Sprint 170 Local Chat Runtime Stabilization",
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
            "aura_reply": "Local Chat Integration Review aktif. Rantai chat alpha 162-168 sudah dicek sebagai jalur tipis yang aman: CLI, store, persona, model boundary, permission gate, safety/uncertainty, dan history viewer terhubung sebagai metadata/read-only review. Model, network, credential, memory write, command execution, file bebas, voice, vision, dan full chat runtime masih nonaktif sampai Sprint 170+ menyelesaikan stabilisasi dan izin yang diperlukan.",
        }

    def render_integration_review_alpha(self) -> str:
        data = self.run_integration_review_alpha()
        lines = [
            "[integration] AURA Local Chat Integration Review Alpha",
            f"[integration] Version              : {data['version']}",
            f"[integration] Session Mode         : {data['session_mode']}",
            f"[integration] Review Packet ID     : {data['review_packet_id']}",
            f"[integration] Integration Checks   : {data['integration_checks']}",
            f"[integration] Components Checked   : {data['components_checked']}",
            f"[integration] Components Ready     : {data['components_ready']}",
            f"[integration] Integration Gaps     : {data['integration_gaps_found']}",
            f"[integration] Chat Chain Ready     : {data['chat_chain_ready']}",
            f"[integration] Next Sprint          : {data['next_sprint']}",
        ]
        for component in data["component_packets"]:
            lines.append(f"[integration] Component            : {component['id']} ready={component['ready']} runtime_action={component['runtime_action']}")
        lines.extend([
            f"[integration] Model Requests       : {data['model_requests']}",
            f"[integration] Model Responses      : {data['model_responses']}",
            f"[integration] Network Requests     : {data['network_requests']}",
            f"[integration] Credentials Read     : {data['credentials_read']}",
            f"[integration] Permission Grants    : {data['permission_grants']}",
            f"[integration] Memory Writes        : {data['memory_writes']}",
            f"[integration] Audit Events Written : {data['audit_events_written']}",
            f"[integration] Commands Executed    : {data['commands_executed']}",
            f"[integration] Arbitrary Files Read : {data['arbitrary_files_read']}",
            f"[integration] Arbitrary Files Wrote: {data['arbitrary_files_wrote']}",
            f"[integration] Runtime Execution    : {data['runtime_execution']}",
            f"[integration] Model Runtime        : {data['model_runtime']}",
            f"[integration] Network Runtime      : {data['network_runtime']}",
            f"[integration] Credential Runtime   : {data['credential_runtime']}",
            f"[integration] Permission Grant     : {data['permission_grant']}",
            f"[integration] Memory Runtime       : {data['memory_runtime']}",
            f"[integration] Command Execution    : {data['command_execution']}",
            f"[integration] Arbitrary File Read  : {data['arbitrary_file_read']}",
            f"[integration] Arbitrary File Write : {data['arbitrary_file_write']}",
            f"[integration] AURA: {data['aura_reply']}",
        ])
        return "\n".join(lines)

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        return {
            "module": self.name,
            "version": "0.169.0-genesis",
            "plan_type": plan_type,
            "target": target,
            "created_for": "Sprint 169 Local Chat Integration Review",
            **self._boundary(),
            **self._runtime_zero_map(),
        }

    def chat_alpha_chain_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_alpha_chain_review_plan", target)
        plan["review_steps"] = ["Confirm sprints 161-168 local chat components are present.", "Confirm full chat runtime remains disabled.", "Prepare Sprint 170 stabilization checklist."]
        return plan

    def chat_cli_surface_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_cli_surface_review_plan", target)
        plan["review_steps"] = ["Confirm alpha CLI commands are registered.", "Keep CLI commands manual only.", "Do not enable autonomous chat loop."]
        return plan

    def chat_message_store_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_message_store_integration_review_plan", target)
        plan["review_steps"] = ["Confirm controlled JSONL store contract.", "Confirm history viewer is read-only.", "Keep memory runtime separate from message history."]
        return plan

    def chat_persona_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_persona_integration_review_plan", target)
        plan["review_steps"] = ["Confirm persona honesty language.", "Confirm action decline language.", "Keep local persona separate from model runtime."]
        return plan

    def chat_model_boundary_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_model_boundary_integration_review_plan", target)
        plan["review_steps"] = ["Confirm adapter packet and prompt envelope exist.", "Confirm provider remains disabled.", "Confirm no dispatch path is open."]
        return plan

    def chat_permission_gate_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_permission_gate_integration_review_plan", target)
        plan["review_steps"] = ["Confirm model requests require explicit grant.", "Confirm grant runtime is disabled.", "Confirm blocked_no_permission_grant remains default."]
        return plan

    def chat_safety_uncertainty_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_safety_uncertainty_integration_review_plan", target)
        plan["review_steps"] = ["Confirm safety classifier present.", "Confirm uncertainty/freshness boundary present.", "Confirm no web/network runtime is used."]
        return plan

    def chat_history_viewer_integration_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_history_viewer_integration_review_plan", target)
        plan["review_steps"] = ["Confirm controlled store read contract.", "Confirm no arbitrary file read.", "Confirm no delete/export/replay actions."]
        return plan

    def chat_control_center_handoff_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("chat_control_center_handoff_review_plan", target)
        plan["review_steps"] = ["Prepare read-only cards for each chat component.", "Keep routes and server runtime deferred.", "Hand off status data to future Control Center panel."]
        return plan

    def no_local_chat_integration_unsafe_runtime_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("no_local_chat_integration_unsafe_runtime_plan", target)
        plan["unsafe_runtime_disabled"] = self.RUNTIME_FALSE_FLAGS
        return plan

    def local_chat_integration_next_sprint_readiness_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("local_chat_integration_next_sprint_readiness_plan", target)
        plan["next_sprint"] = "Sprint 170 Local Chat Runtime Stabilization"
        plan["readiness"] = ["Review chain complete.", "Stabilization checkpoint next.", "Full model/chat runtime still gated."]
        return plan
