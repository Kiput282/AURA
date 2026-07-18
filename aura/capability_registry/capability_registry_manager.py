
"""Capability Registry Consolidation for AURA.

Central planner-only registry describing what AURA can do, what is only a
foundation, what is planner-only, what requires permission, what is only a
review/checkpoint layer, and what is still planned for the future.

This registry prepares data for CLI, shell, service monitor, launcher, and
AURA Control Center views. Sprint 181 activates a localhost-only read-only
HTTP listener, Sprint 182 adds deterministic lifecycle control, and Sprint
183 adds transparent read-only health and status payloads. Chat, models,
permission mutation, commands, tools, files, desktop control, background
service, and external actions remain disabled.
"""
from __future__ import annotations

from typing import Any


class CapabilityRegistryManager:
    """Central planner-only capability registry for AURA."""

    name = "capability_registry"
    version = "0.1.0"
    status_name = "online"

    def registry_plan_types(self) -> list[str]:
        return [
            "capability_registry_status",
            "capability_catalog_plan",
            "capability_state_review_plan",
            "permission_requirement_review_plan",
            "risk_level_review_plan",
            "control_center_capability_view_plan",
            "capability_gap_review_plan",
            "capability_registry_migration_plan",
            "capability_registry_context",
        ]

    def capability_states(self) -> list[str]:
        return [
            "online",
            "foundation_only",
            "planner_only",
            "permission_gated",
            "review_only",
            "planned_future",
            "disabled_runtime",
        ]

    def risk_levels(self) -> list[str]:
        return [
            "low",
            "medium",
            "high",
            "critical",
        ]

    def permission_categories(self) -> list[str]:
        return [
            "none",
            "read_project",
            "user_confirmation",
            "microphone_permission",
            "camera_permission",
            "screen_permission",
            "file_write_permission",
            "command_execution_permission",
            "dependency_download_permission",
            "internet_search_permission",
            "model_request_permission",
            "desktop_control_permission",
            "git_operation_permission",
        ]

    def safe_current_capabilities(self) -> list[str]:
        return [
            "List AURA capabilities as metadata.",
            "Classify capabilities by current state.",
            "Classify capabilities by runtime level.",
            "Classify capabilities by risk level.",
            "List required permission categories.",
            "Identify planned future capabilities without enabling them.",
            "Prepare capability data for AURA Control Center views.",
            "Report the scoped Sprint 181 runtime without starting it, ""while registry inspection remains metadata-only and ""side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
                   'automatic_capability_enablement',
                   'dynamic_runtime_discovery',
                   'runtime_action_activation',
                   'permission_grant_runtime',
                   'public_web_server_runtime',
                   'lan_web_server_runtime',
                   'wildcard_web_server_runtime',
                   'ipv6_wildcard_web_server_runtime',
                   'background_service_runtime',
                   'automatic_service_start_runtime',
                   'mutating_dashboard_runtime',
                   'chat_runtime',
                   'launcher_runtime',
                   'file_read',
                   'file_write',
                   'file_modify',
                   'file_delete',
                   'command_execution',
                   'test_execution',
                   'code_execution',
                   'dependency_install',
                   'package_download',
                   'internet_search',
                   'network_action',
                   'tool_execution',
                   'real_tool_execution',
                   'external_action_execution',
                   'memory_write',
                   'desktop_control',
                   'git_init',
                   'git_add',
                   'git_commit',
                   'git_push',
               ]

    def safety_boundary(self) -> dict[str, bool]:
        return {
                   'registry_only': True,
                   'planner_only': True,
                   'proposal_only': True,
                   'metadata_only': True,
                   'control_center_data_ready': True,
                   'local_web_runtime_alpha': True,
                   'service_lifecycle_runtime': True,
                   'health_status_api_runtime': True,
                   'control_center_backend_runtime': True,
                   'read_only_control_center_backend': True,
                   'control_center_backend_route_count': 9,
                   'control_center_backend_panel_count': 8,
                   'control_center_backend_foundation_contract_count': 8,
                   'control_center_web_shell_runtime': True,
                   'control_center_frontend_asset_runtime': True,
                   'control_center_web_shell_asset_route_count': 3,
                   'control_center_web_shell_panel_count': 8,
                   'control_center_total_route_count': 21,
                   'control_center_responsive_layout': True,
                   'control_center_accessibility_contract': True,
                   'control_center_degraded_state_ui': True,
                   'control_center_safe_idle_indicator': True,
                   'browser_chat_session_runtime': True,
                   'browser_chat_http_routes': True,
                   'browser_chat_session_creation': True,
                   'browser_chat_validated_submission': True,
                   'browser_chat_response_delivery': True,
                   'browser_chat_history_persistence': True,
                   'browser_chat_session_reload': True,
                   'browser_chat_clear_confirmation': True,
                   'browser_chat_revision_control': True,
                   'browser_chat_idempotent_submission': True,
                   'browser_chat_integrity_hash': True,
                   'browser_chat_bounded_mutation': True,
                   'browser_chat_asset_route_count': 3,
                   'browser_chat_route_contract_count': 7,
                   'local_interaction_total_route_contract_count': 37,
                   'local_session_file_write_runtime': True,
                   'local_model_bridge_runtime': True,
                   'local_model_inference_runtime': True,
                   'local_model_provider_profile_runtime': True,
                   'local_model_ollama_contract': True,
                   'local_model_openai_compatible_contract': True,
                   'local_model_loopback_endpoint_enforcement': True,
                   'local_model_resolved_loopback_enforcement': True,
                   'local_model_redirect_following_runtime': False,
                   'local_model_probe_runtime': True,
                   'local_model_text_response_runtime': True,
                   'local_model_explicit_probe_confirmation': True,
                   'local_model_explicit_request_confirmation': True,
                   'local_model_response_persistence': True,
                   'browser_chat_model_bridge_runtime': True,
                   'interactive_control_center_chat_runtime': True,
                   'interactive_chat_web_surface_runtime': True,
                   'interactive_chat_orchestration_runtime': True,
                   'interactive_chat_save_only_default': True,
                   'interactive_chat_local_model_mode': True,
                   'interactive_chat_provider_status_visibility': True,
                   'interactive_chat_model_status_visibility': True,
                   'interactive_chat_probe_confirmation_ui': True,
                   'interactive_chat_model_request_confirmation_ui': True,
                   'interactive_chat_idempotent_retry_ui': True,
                   'interactive_chat_response_kind_visibility': True,
                   'interactive_chat_restart_persistence': True,
                   'interactive_chat_clear_confirmation': True,
                   'permission_audit_recovery_visibility_runtime': True,
                   'permission_visibility_runtime': True,
                   'audit_contract_visibility_runtime': True,
                   'recovery_guidance_visibility_runtime': True,
                   'permission_audit_recovery_http_routes': True,
                   'permission_audit_recovery_browser_panel': True,
                   'permission_audit_recovery_api_route_count': 4,
                   'permission_audit_recovery_asset_route_count': 3,
                   'permission_audit_recovery_total_route_count': 7,
                   'permission_audit_recovery_read_only': True,
                   'sensitive_values_exposed': False,
                   'permission_mutation_runtime': False,
                   'permission_persistence_runtime': False,
                   'audit_writer_runtime': False,
                   'audit_persistence_runtime': False,
                   'automatic_recovery_runtime': False,
                   'automatic_retry_runtime': False,
                   'rollback_execution_runtime': False,
                   'interactive_chat_local_browser_storage_runtime': False,
                   'interactive_chat_websocket_runtime': False,
                   'interactive_chat_eventsource_runtime': False,
                   'interactive_chat_tool_action_command_ui': False,
                   'local_model_download_runtime': False,
                   'local_model_streaming_runtime': False,
                   'local_model_tool_calling_runtime': False,
                   'network_fallback_runtime': False,
                   'aura_long_term_memory_write_runtime': False,
                   'control_center_external_dependency_runtime': False,
                   'control_center_browser_launch_runtime': False,
                   'control_center_backend_mutation_runtime': False,
                   'control_center_service_control_runtime': False,
                   'control_center_plugin_control_runtime': False,
                   'control_center_permission_decision_runtime': False,
                   'control_center_audit_writer_runtime': False,
                   'control_center_memory_write_runtime': False,
                   'read_only_status_routes': True,
                   'status_route_count': 9,
                   'degraded_status_reporting': True,
                   'identity_status_runtime': True,
                   'plugin_status_runtime': True,
                   'capability_status_runtime': True,
                   'service_status_runtime': True,
                   'memory_status_runtime': True,
                   'safety_status_runtime': True,
                   'error_status_runtime': True,
                   'status_api_mutation_runtime': False,
                   'status_api_plugin_start_runtime': False,
                   'status_api_memory_mutation_runtime': False,
                   'status_api_listener_start_probe_runtime': False,
                   'deterministic_lifecycle_state_machine': True,
                   'single_listener_enforced': True,
                   'port_conflict_fail_closed': True,
                   'startup_rollback_runtime': True,
                   'clean_programmatic_stop_runtime': True,
                   'clean_signal_shutdown_runtime': True,
                   'persistent_pid_file_runtime': False,
                   'persistent_lifecycle_state_runtime': False,
                   'remote_lifecycle_control_runtime': False,
                   'http_lifecycle_mutation_runtime': False,
                   'localhost_only_runtime': True,
                   'foreground_only_runtime': True,
                   'read_only_http_runtime': False,
                   'explicit_start_confirmation_required': True,
                   'public_web_server_runtime': False,
                   'lan_web_server_runtime': False,
                   'wildcard_web_server_runtime': False,
                   'ipv6_wildcard_web_server_runtime': False,
                   'background_service_runtime': False,
                   'automatic_service_start_runtime': False,
                   'mutating_dashboard_runtime': False,
                   'runtime_ready': False,
                   'execution_ready': False,
                   'executed': False,
                   'runtime_behavior_change': True,
                   'automatic_capability_enablement': False,
                   'dynamic_runtime_discovery': False,
                   'runtime_action_activation': False,
                   'permission_grant_runtime': False,
                   'ui_runtime': True,
                   'web_server_runtime': True,
                   'chat_runtime': True,
                   'service_runtime': True,
                   'launcher_runtime': False,
                   'file_read': False,
                   'file_write': False,
                   'file_modify': False,
                   'file_delete': False,
                   'command_execution': False,
                   'test_execution': False,
                   'code_execution': False,
                   'dependency_install': False,
                   'package_download': False,
                   'internet_search': False,
                   'network_action': False,
                   'tool_execution': False,
                   'real_tool_execution': False,
                   'external_action_execution': False,
                   'memory_write': False,
                   'desktop_control': False,
                   'git_init': False,
                   'git_add': False,
                   'git_commit': False,
                   'git_push': False,
               }

    def capability_catalog(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "thought_loop_planner",
                "name": "Thought Loop Planner",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "category": "thinking",
                "introduced_in": "0.71.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "reasoning_context_manager",
                "name": "Reasoning Context Manager",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "category": "reasoning",
                "introduced_in": "0.72.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "knowledge_uncertainty_internet_search_gate",
                "name": "Knowledge Uncertainty & Internet Search Gate",
                "state": "online",
                "runtime_level": "permission_gated_planner",
                "risk_level": "medium",
                "permission_required": "internet_search_permission",
                "category": "knowledge_safety",
                "introduced_in": "0.73.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "voice_input_runtime_foundation",
                "name": "Voice Input Runtime Foundation",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "high",
                "permission_required": "microphone_permission",
                "category": "hearing_foundation",
                "introduced_in": "0.74.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "voice_intent_understanding_layer",
                "name": "Voice Intent Understanding Layer",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "hearing_understanding",
                "introduced_in": "0.75.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "vision_input_runtime_foundation",
                "name": "Vision Input Runtime Foundation",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "high",
                "permission_required": "camera_permission",
                "category": "seeing_foundation",
                "introduced_in": "0.76.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "visual_context_understanding_layer",
                "name": "Visual Context Understanding Layer",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "high",
                "permission_required": "screen_permission",
                "category": "seeing_understanding",
                "introduced_in": "0.77.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "coder_project_generation_planner",
                "name": "Coder Project Generation Planner",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "medium",
                "permission_required": "file_write_permission",
                "category": "coding_planner",
                "introduced_in": "0.78.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "dependency_download_permission_gate",
                "name": "Dependency & Download Permission Gate",
                "state": "online",
                "runtime_level": "permission_gated_planner",
                "risk_level": "high",
                "permission_required": "dependency_download_permission",
                "category": "dependency_safety",
                "introduced_in": "0.79.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "review_stabilization_71_80",
                "name": "Review & Stabilization 71-80",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "category": "checkpoint",
                "introduced_in": "0.80.0-genesis",
                "control_center_visible": True,
            },
            {'id': 'roadmap_reconfirmation_after_v1_2_0',
             'name': 'Roadmap Reconfirmation after v1.2.0',
             'state': 'online',
             'runtime_level': 'review_only',
             'risk_level': 'low',
             'permission_required': None,
             'category': 'product_roadmap',
             'introduced_in': '1.2.1',
             'control_center_visible': True,
             'description': 'Canonical v1.2.1 to v1.3.0 daily product roadmap, gap '
                            'ownership, and end-of-block live acceptance policy.'},
            {
                "id": "shared_output_formatter",
                "name": "Shared Output Formatter",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "category": "output_foundation",
                "introduced_in": "0.81.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "capability_registry",
                "name": "Capability Registry Consolidation",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "category": "capability_awareness",
                "introduced_in": "0.82.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "unified_permission_workflow",
                "name": "Unified Permission Workflow Manager",
                "state": "online",
                "runtime_level": "planner_only",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "permission_workflow",
                "introduced_in": "0.83.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "aura_runtime_service",
                "name": "AURA Runtime Service Foundation",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "service_foundation",
                "introduced_in": "0.84.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "aura_launcher_health_monitor",
                "name": "AURA Launcher & Health Monitor",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "operations_monitoring",
                "introduced_in": "0.85.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "aura_control_center",
                "name": "AURA Control Center",
                "state": "online",
                "runtime_level": "foundation_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_console_ui",
                "introduced_in": "0.86.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "controlled_file_write_runtime",
                "name": "Controlled File Write Runtime",
                "state": "disabled_runtime",
                "runtime_level": "deferred_runtime",
                "risk_level": "critical",
                "permission_required": "file_write_permission",
                "category": "runtime_action_deferred",
                "introduced_in": "deferred-91-100",
                "control_center_visible": True,
            },
            {
                "id": "controlled_command_execution_runtime",
                "name": "Controlled Command Execution Runtime",
                "state": "disabled_runtime",
                "runtime_level": "deferred_runtime",
                "risk_level": "critical",
                "permission_required": "command_execution_permission",
                "category": "runtime_action_deferred",
                "introduced_in": "deferred-91-100",
                "control_center_visible": True,
            },
                        {
                    "id": "aura_local_console_web_foundation",
                    "name": "AURA Local Console Web Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "category": "control_center_web",
                    "introduced_in": "0.87.0-genesis",
                    "control_center_visible": True,
                },
                {
                    "id": "aura_chat_bridge_session_state_foundation",
                    "name": "AURA Chat Bridge & Session State Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "category": "chat_bridge",
                    "introduced_in": "0.88.0-genesis",
                    "control_center_visible": True,
                },
                {
                    "id": "aura_plugin_permission_dashboard_foundation",
                    "name": "AURA Plugin / Permission Dashboard Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "category": "plugin_permission_dashboard",
                    "introduced_in": "0.89.0-genesis",
                    "control_center_visible": True,
                },
                {
                    "id": "aura_local_console_static_prototype_foundation",
                    "name": "AURA Local Console Static Prototype Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "category": "local_console_static_prototype",
                    "introduced_in": "0.91.0-genesis",
                    "control_center_visible": True,
                },
                {
                    "id": "aura_local_console_api_schema_foundation",
                    "name": "AURA Local Console API Schema Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "category": "local_console_api_schema",
                    "introduced_in": "0.92.0-genesis",
                    "control_center_visible": True,
                },
                {
                    "id": "aura_control_center_data_aggregator_foundation",
                    "name": "AURA Control Center Data Aggregator Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.93.0-genesis",
                    "category": "control_center",
                    "control_center_visible": True,
                    "description": "Planner-only Control Center data aggregator foundation for ATLAS core packets, ORION client packets, client bridge packets, dashboard view packets, permission scope packets, health snapshot packets, audit event visibility fields, and metadata-only aggregator safety policy.",
                },
                {
                    "id": "aura_permission_request_review_queue_foundation",
                    "name": "AURA Permission Request Review Queue Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.94.0-genesis",
                    "category": "permission",
                    "control_center_visible": True,
                    "description": "Planner-only permission request review queue foundation for permission request blueprints, queue state blueprints, review packet fields, scope boundaries, decision proposal contracts, reviewer checklist items, audit visibility fields, and permission request safety policy.",
                },
                {
                    "id": "aura_chat_session_persistence_planner_foundation",
                    "name": "AURA Chat Session Persistence Planner Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.95.0-genesis",
                    "category": "chat",
                    "control_center_visible": True,
                    "description": "Planner-only chat session persistence planner foundation for session record blueprints, storage boundaries, retention policy blueprints, privacy redaction rules, session lifecycle states, recovery index blueprints, export/migration notes, audit visibility fields, and persistence safety policy.",
                },
                {
                    "id": "aura_safe_local_web_runtime_gate_foundation",
                    "name": "AURA Safe Local Web Runtime Gate Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.96.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only and pre-runtime safe local web runtime gate foundation for localhost binding policies, port policies, permission requirements, runtime preflight checks, start/stop proposal contracts, route boundaries, static asset boundaries, kill switch policies, and web runtime audit visibility.",
                },
                {
                    "id": "aura_controlled_file_write_approval_draft_foundation",
                    "name": "AURA Controlled File Write Approval Draft Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.97.0-genesis",
                    "category": "file_ops",
                    "control_center_visible": True,
                    "description": "Planner-only and draft-only controlled file write approval foundation for file write proposal drafts, target path policies, diff preview contracts, overwrite rules, backup requirements, approval checklist items, rollback notes, file write audit visibility, and safety policy.",
                },
                {
                    "id": "aura_runtime_action_queue_review_layer_foundation",
                    "name": "AURA Runtime Action Queue Review Layer Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.98.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only, review-only, and proposal-only runtime action queue review layer foundation for action queue item blueprints, queue state blueprints, review priority rules, dependency/blocker contracts, permission link requirements, execution preflight check blueprints, approval/denial transition rules, timeout/expiry policies, runtime action audit visibility, and safety policy.",
                },
                {
                    "id": "aura_pre_runtime_security_audit_foundation",
                    "name": "AURA Pre-Runtime Security Audit Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.99.0-genesis",
                    "category": "security",
                    "control_center_visible": True,
                    "description": "Planner-only, review-only, and audit-blueprint-only pre-runtime security audit foundation for audit domains, runtime gate checks, permission boundary checks, file system safety checks, network surface checks, action execution safety checks, ORION boundary checks, audit visibility checks, and Sprint 100 stabilization readiness checks.",
                },
                {
                    "id": "aura_sprint_100_review_stabilization_foundation",
                    "name": "AURA Sprint 100 Review & Stabilization Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.100.0-genesis",
                    "category": "stabilization",
                    "control_center_visible": True,
                    "description": "Planner-only, review-only, and checkpoint-blueprint-only Sprint 100 Review & Stabilization Foundation for Sprint 91-100 block review, completed feature inventory, active vs foundation-only boundaries, runtime-zero safety checks, capability registry stabilization, documentation stabilization, unresolved future features, roadmap 101-110 seed planning, and release readiness.",
                },
                {
                    "id": "aura_genesis_runtime_readiness_baseline_foundation",
                    "name": "AURA Genesis Runtime Readiness Baseline Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.101.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and readiness-blueprint-only Genesis Runtime Readiness Baseline Foundation for readiness domains, runtime candidate classification, dry-run prerequisites, permission requirement matrix, safety gate alignment, rollback and kill-switch readiness, audit and observability readiness, rollout phase recommendations, and Sprint 101-110 block alignment.",
                },
                {
                    "id": "aura_safe_runtime_configuration_profile_foundation",
                    "name": "AURA Safe Runtime Configuration Profile Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.102.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and configuration-blueprint-only Safe Runtime Configuration Profile Foundation for profile types, runtime mode policies, service boundaries, permission boundaries, file system boundaries, network boundaries, dry-run requirements, rollout guards, and configuration audit visibility.",
                },
                {
                    "id": "aura_local_service_start_proposal_review_foundation",
                    "name": "AURA Local Service Start Proposal Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.103.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and proposal-review-only Local Service Start Proposal Review Foundation for future local service start proposals, service candidates, preflight requirements, port binding review, process launch boundaries, permission requirements, risk classification, rollback/kill-switch planning, audit events, and user approval decisions without starting services or activating runtime.",
                },
                {
                    "id": "aura_dashboard_api_contract_consolidation_foundation",
                    "name": "AURA Dashboard API Contract Consolidation Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.104.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and contract-blueprint-only Dashboard API Contract Consolidation Foundation for API contracts, endpoint schemas, request/response contracts, permission mappings, dashboard payloads, error responses, mock API boundaries, frontend/backend boundaries, and contract validation without starting API runtime.",
                },
                {
                    "id": "aura_permission_decision_runtime_dry_run_foundation",
                    "name": "AURA Permission Decision Runtime Dry-Run Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.105.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and dry-run-blueprint-only Permission Decision Runtime Dry-Run Foundation for permission decision candidates, input contracts, dry-run evaluations, permission scope mappings, approval/denial outcomes, risk review rules, audit record blueprints, dashboard review payloads, and dry-run safety boundaries without changing real permissions.",
                },
                {
                    "id": "aura_runtime_action_execution_preview_packet_foundation",
                    "name": "AURA Runtime Action Execution Preview Packet Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.106.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and preview-packet-only Runtime Action Execution Preview Packet Foundation for action candidates, execution preflight checklists, action input snapshots, permission decision references, execution step previews, side effect boundaries, rollback previews, audit preview records, and user confirmation packets without dispatching or executing runtime actions.",
                },
                {
                    "id": "aura_local_runtime_execution_gate_dry_run_foundation",
                    "name": "AURA Local Runtime Execution Gate Dry-Run Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.107.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and dry-run-gate-blueprint-only Local Runtime Execution Gate Dry-Run Foundation for execution gate candidates, runtime gate input contracts, gate preflight evaluations, safe runtime profile references, permission gate references, execution gate decisions, block reasons, audit gate records, and dashboard gate payloads without opening gates or executing runtime actions.",
                },
                {
                    "id": "aura_runtime_audit_event_packet_preview_foundation",
                    "name": "AURA Runtime Audit Event Packet Preview Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.108.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and audit-packet-preview-only Runtime Audit Event Packet Preview Foundation for audit event candidates, input snapshots, runtime references, permission references, action preview references, audit payload shapes, visibility rules, retention/redaction boundaries, and dashboard audit packets without writing, emitting, streaming, sending, or persisting audit events.",
                },
                {
                    "id": "aura_runtime_safety_freeze_manual_approval_barrier_foundation",
                    "name": "AURA Runtime Safety Freeze Manual Approval Barrier Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "read_project",
                    "introduced_in": "0.109.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and barrier-blueprint-only Runtime Safety Freeze Manual Approval Barrier Foundation for safety freeze candidates, manual approval barrier inputs, freeze condition checks, approval rules, blocked runtime catalog, user confirmation barriers, emergency stop requirements, audit freeze packet previews, and dashboard barrier payloads without activating freeze, granting approvals, passing barriers, or executing runtime actions.",
                },
                {
                    "id": "aura_review_stabilization_101_110_foundation",
                    "name": "AURA Review Stabilization 101-110 Foundation",
                    "state": "online",
                    "runtime_level": "review_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.110.0-genesis",
                    "category": "stabilization",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and checkpoint-review-only Review Stabilization 101-110 Foundation for sprint completion inventory, runtime readiness foundation audit, safety invariant verification, capability registry delta review, integration surface review, documentation consistency review, checkpoint risk review, deferred runtime boundary review, and next block readiness without enabling runtime execution.",
                },
                {
                    "id": "aura_genesis_runtime_readiness_next_block_planning_foundation",
                    "name": "AURA Genesis Runtime Readiness Next Block Planning Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.111.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and next-block-planning-only Genesis Runtime Readiness Next Block Planning Foundation for Sprint 111-120 candidates, runtime readiness continuity, manual approval evolution, audit event evolution, dashboard contract evolution, ORION boundary planning, safe local action boundary, integration stabilization, and v1 readiness mapping without enabling runtime execution.",
                },
                {
                    "id": "aura_runtime_permission_flow_consolidation_foundation",
                    "name": "AURA Runtime Permission Flow Consolidation Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.112.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and permission-flow-consolidation-only Runtime Permission Flow Consolidation Foundation for permission request schema, permission decision states, manual approval checkpoints, denial and cancellation flow, permission scope boundaries, high-risk escalation rules, approval audit references, dashboard permission flow payloads, and future runtime grant boundaries without changing permissions or enabling runtime execution.",
                },
                {
                    "id": "aura_audit_event_review_queue_foundation",
                    "name": "AURA Audit Event Review Queue Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.113.0-genesis",
                    "category": "audit",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-queue-blueprint-only Audit Event Review Queue Foundation for audit event intake schema, review queue state model, triage rules, permission linkage review, runtime boundary review, redaction visibility review, dashboard review queue payloads, review outcome catalog, and future audit writer boundary without writing, emitting, streaming, sending, or persisting audit events.",
                },
                {
                    "id": "aura_dashboard_runtime_readiness_view_model_foundation",
                    "name": "AURA Dashboard Runtime Readiness View Model Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.114.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and view-model-only Dashboard Runtime Readiness View Model Foundation for runtime readiness summary, permission state, audit review queue, safety boundary, ORION boundary, action preview, manual approval, v1 cutline, and Control Center payload views without starting dashboard runtime, API server, web server, frontend/backend runtime, or enabling runtime execution.",
                },
                {
                    "id": "aura_safe_local_action_contract_review_foundation",
                    "name": "AURA Safe Local Action Contract Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.115.0-genesis",
                    "category": "local_action",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and contract-review-only Safe Local Action Contract Review Foundation for local open contracts, controlled create contracts, controlled write preview contracts, action preview packets, permission scope contracts, side effect boundaries, rollback/cancel contracts, dashboard contract payloads, and future action runtime boundaries without executing local actions or enabling runtime execution.",
                },
                {
                    "id": "aura_orion_client_boundary_contract_foundation",
                    "name": "AURA ORION Client Boundary Contract Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.116.0-genesis",
                    "category": "orion",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and boundary-contract-only ORION Client Boundary Contract Foundation for ORION client identity, ATLAS/ORION authority, ORION sense permission, ORION local action, emergency stop, dashboard status payload, runtime handshake, data-flow redaction, and future ORION runtime boundaries without starting ORION client runtime or enabling runtime execution.",
                },
                {
                    "id": "aura_runtime_error_rollback_preview_foundation",
                    "name": "AURA Runtime Error and Rollback Preview Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.117.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and preview-only Runtime Error and Rollback Preview Foundation for runtime error taxonomy, rollback preview packets, failure recovery state models, cancellation boundaries, partial execution guards, permission error reviews, audit error references, dashboard error rollback payloads, and future runtime recovery boundaries without executing rollback, recovery, cancellation, or runtime mutation.",
                },
                {
                    "id": "aura_manual_approval_decision_flow_review_foundation",
                    "name": "AURA Manual Approval Decision Flow Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.118.0-genesis",
                    "category": "permission",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Manual Approval Decision Flow Review Foundation for approval request schema, decision state, outcome catalog, denial/cancellation, escalation boundary, audit reference, dashboard payload, runtime gate, and future approval runtime boundaries without creating approval requests, persisting approval state, applying approval decisions, changing permission, or enabling runtime execution.",
                },
                {
                    "id": "aura_v1_runtime_readiness_cutline_review_foundation",
                    "name": "AURA v1 Runtime Readiness Cutline Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.119.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only v1 Runtime Readiness Cutline Review Foundation for allowed capabilities, deferred capabilities, runtime gates, permission/audit requirements, ORION boundaries, dashboard visibility, release blockers, safe idle acceptance, and future v1 runtime activation boundaries without approving v1 runtime, opening release gates, enabling features, or enabling runtime execution.",
                },
                {
                    "id": "aura_review_stabilization_111_120_foundation",
                    "name": "AURA Review Stabilization 111-120 Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.120.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and checkpoint-review-only Review Stabilization 111-120 Foundation for Sprint 111-120 completion review, capability registry stabilization, runtime safety zero-state review, integration surface stabilization, documentation roadmap stabilization, v1 blocker review, release cutline consistency, next block 121-130 boundary planning, and checkpoint 120 acceptance review without approving runtime, opening release gates, enabling v1 runtime, mutating capability states, or enabling runtime execution.",
                },
            {
                "id": "aura_memory_runtime_stabilization",
                "name": "AURA Memory Runtime Stabilization",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.180.0-genesis",
                "control_center_visible": True,
                "description": "Read-only stabilization checkpoint closing the Sprint 171-180 Memory Runtime block by verifying nine component versions/readiness states, zero dependency gaps and runtime violations, stable privacy/review/permission ordering, closed correction/deletion and release gates, and readiness for the Voice Foundation Runtime block while all mutation and execution runtimes remain disabled.",
            },
            {
                "id": "aura_memory_runtime_integration_review",
                "name": "AURA Memory Runtime Integration Review",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.179.0-genesis",
                "control_center_visible": True,
                "description": "Read-only integration review of the Sprint 171-178 memory chain, including component/version readiness, deterministic pipeline order, privacy-before-permission, manual-review-before-write, correction/deletion governance, closed release gates, and zero cross-component mutation counters while all unsafe runtimes remain disabled.",
            },
            {
                "id": "aura_memory_privacy_redaction_layer",
                "name": "AURA Memory Privacy and Redaction Layer",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.178.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic, local, preview-only memory privacy screening with stable redaction placeholders, secret-block boundaries, original-value hiding, privacy-review routing, and default-deny permission handoff while keeping original/redacted persistence, queue decisions, grants, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, full runtimes, and runtime execution disabled.",
            },
            {
                "id": "aura_chat_to_memory_handoff_contract",
                "name": "AURA Chat-to-Memory Handoff Contract",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.177.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic, direct-user-turn, preview-only chat-to-memory handoff with explicit memory intent, exact source binding, privacy precheck, review-queue routing, and default-deny permission state while keeping chat-store/history reads, queue persistence, grants, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, full runtimes, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_correction_deletion_boundary",
                "name": "AURA Memory Correction and Deletion Boundary",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "high",
                "permission_required": "explicit_user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.176.0-genesis",
                "control_center_visible": True,
                "description": "Exact-target, preview-only correction and deletion boundary using future versioned replacement, tombstone-first deletion, and separate purge permission while keeping memory-store reads, record lookups, correction/delete/tombstone/purge application, grants, memory writes/store mutation, model/network/credential activity, audit writes, commands, arbitrary file access, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_review_queue",
                "name": "AURA Memory Review Queue",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.175.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic, ephemeral, preview-only manual review queue for one memory candidate with priority, privacy hold, permission state, and future decision options while keeping queue persistence, decision apply, permission grants, candidate persistence, memory writes/store mutation, pin/unpin operations, model/network/credential activity, audit writes, commands, arbitrary file access, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_importance_pinning_policy",
                "name": "AURA Memory Importance and Pinning Policy",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.174.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic, explainable, preview-only importance scoring, durability detection, retention recommendation, and future pin-eligibility policy for one user-supplied memory candidate while keeping candidate persistence, permission grants, memory writes/store mutation, pin/unpin operations, model, network, credentials, audit writes, commands, arbitrary file access, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_extraction_dry_run",
                "name": "AURA Memory Extraction Dry Run",
                "state": "online",
                "runtime_level": "foundation_alpha",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.173.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic, rule-based, preview-only Memory Extraction Dry Run for a single user-supplied message; detects explicit memory triggers, normalizes and classifies a candidate, screens common sensitive patterns, and prepares fingerprint/permission handoff while keeping candidate persistence, grants, memory writes/store mutation, model, network, credentials, audit writes, commands, arbitrary file access, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_write_permission_gate",
                "name": "AURA Memory Write Permission Gate",
                "state": "online",
                "runtime_level": "foundation_alpha",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "memory_runtime",
                "introduced_in": "0.172.0-genesis",
                "control_center_visible": True,
                "description": "Default-deny and preview-only Memory Write Permission Gate for a single candidate fingerprint and exact memory.write.single_candidate scope; keeps permission grant apply, candidate persistence, memory write/store mutation, model, network, credentials, audit writes, commands, arbitrary file access, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_memory_runtime_foundation",
                "name": "AURA Memory Runtime Foundation",
                "state": "online",
                "runtime_level": "foundation_alpha",
                "risk_level": "medium",
                "permission_required": "read_project",
                "category": "memory_runtime",
                "introduced_in": "0.171.0-genesis",
                "control_center_visible": True,
                "description": "Preview-only and metadata-only Memory Runtime Foundation for the Sprint 171-180 Memory Runtime block; creates memory candidate previews and write-gate plans while keeping memory writes, memory store mutation, model requests, network, credentials, permission grants, audit writes, command execution, arbitrary file access, desktop, voice, vision, service, web, full memory runtime, and runtime execution disabled.",
            },
            {
                "id": "aura_local_chat_runtime_stabilization",
                "name": "AURA Local Chat Runtime Stabilization",
                "state": "online",
                "runtime_level": "stabilization_alpha",
                "risk_level": "medium",
                "permission_required": "read_project",
                "category": "local_chat_runtime",
                "introduced_in": "0.170.0-genesis",
                "control_center_visible": True,
                "description": "Read-only stabilization checkpoint for the Sprint 161-170 local chat alpha block; verifies safe alpha surfaces, controlled store/history contracts, model permission gates, safety/uncertainty boundaries, and memory runtime handoff without opening model, network, memory write, command, file, desktop, voice, vision, service, web, or full chat runtime.",
            },
            {
                "id": "aura_local_chat_integration_review",
                "name": "AURA Local Chat Integration Review",
                "state": "online",
                "runtime_level": "integration_review_alpha",
                "risk_level": "medium",
                "permission_required": "read_project",
                "category": "local_chat_runtime",
                "introduced_in": "0.169.0-genesis",
                "control_center_visible": True,
                "description": "Read-only and metadata-only integration review for the local chat alpha chain across CLI session, message store, persona, model boundary, permission gate, safety/uncertainty, and history viewer without opening model, network, memory, command, file, desktop, voice, vision, or full chat runtime.",
            },
            {
                "id": "aura_local_chat_history_viewer_contract",
                "name": "AURA Local Chat History Viewer Contract",
                "state": "online",
                "runtime_level": "read_only_history_viewer_alpha",
                "risk_level": "medium",
                "permission_required": "local_chat_history_read",
                "category": "local_chat_runtime",
                "introduced_in": "0.168.0-genesis",
                "control_center_visible": True,
                "description": "Read-only viewer contract for controlled AURA local chat message store history; reads only the fixed AURA store path and does not dispatch models, use network, read credentials, write memory/audit, execute commands, or mutate arbitrary files.",
            },
            {
                "id": "aura_local_chat_safety_uncertainty_layer",
                "name": "AURA Local Chat Safety + Uncertainty Layer",
                "state": "online",
                "runtime_level": "safety_uncertainty_alpha",
                "risk_level": "medium",
                "permission_required": "model_request_permission",
                "category": "local_chat_runtime",
                "introduced_in": "0.167.0-genesis",
                "control_center_visible": True,
                "description": "Deterministic local chat safety and uncertainty review layer that runs before future model requests without dispatching models, using network, reading credentials, writing memory, executing commands, or mutating arbitrary files.",
            },
            {
                "id": "aura_local_chat_permission_gated_model_request",
                "name": "AURA Local Chat Permission-Gated Model Request",
                "state": "online",
                "runtime_level": "permission_gate_dry_run_alpha",
                "risk_level": "medium",
                "permission_required": "model_request_permission",
                "category": "local_chat_runtime",
                "introduced_in": "0.166.0-genesis",
                "control_center_visible": True,
                "description": "Permission-gated local chat model request dry-run that creates a permission preview packet, request envelope, and blocked gate decision without dispatching model requests, receiving model responses, reading credentials, using network, writing memory, executing commands, or mutating arbitrary files.",
            },
            {
                "id": "aura_local_chat_model_adapter_boundary",
                "name": "AURA Local Chat Model Adapter Boundary",
                "state": "online",
                "runtime_level": "dry_run_boundary_alpha",
                "risk_level": "medium",
                "permission_required": "future_model_permission_gate",
                "category": "local_chat_runtime",
                "introduced_in": "0.165.0-genesis",
                "control_center_visible": True,
            },
            {
                "id": "aura_local_chat_persona_response_layer",
                "name": "AURA Local Chat Persona Response Layer",
                "state": "online",
                "runtime_level": "thin_runtime_alpha",
                "risk_level": "low",
                "permission_required": "user_confirmation",
                "category": "local_chat_runtime",
                "introduced_in": "0.164.0-genesis",
                "control_center_visible": True,
            },
                {
                    "id": "aura_local_chat_message_store",
                    "name": "AURA Local Chat Message Store",
                    "state": "online",
                    "runtime_level": "controlled_alpha_runtime",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "introduced_in": "0.163.0-genesis",
                    "category": "local_chat_runtime",
                    "control_center_visible": True,
                    "description": "Controlled local chat message store alpha that accepts one manual CLI message, returns a safe persona response, and appends a JSONL turn record to an AURA-owned local store without model runtime, memory runtime, command execution, arbitrary file mutation, desktop control, network access, or autonomous actions.",
                },
                {
                    "id": "aura_local_chat_cli_session_alpha",
                    "name": "AURA Local Chat CLI Session Alpha",
                    "state": "online",
                    "runtime_level": "permission_gated_alpha_runtime",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "introduced_in": "0.162.0-genesis",
                    "category": "local_chat_runtime",
                    "control_center_visible": True,
                    "description": "Safe thin local chat CLI alpha that accepts one manual CLI message, creates a transient in-memory session packet, and returns a deterministic AURA persona response without persisting history, dispatching model requests, writing memory/audit, executing commands, mutating files, launching apps, starting servers, binding ports, or performing autonomous actions.",
                },
                {
                    "id": "aura_local_chat_runtime_foundation",
                    "name": "AURA Local Chat Runtime Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "medium",
                    "permission_required": "user_confirmation",
                    "introduced_in": "0.161.0-genesis",
                    "category": "local_chat_runtime",
                    "control_center_visible": True,
                    "description": "Foundation-only local chat runtime contracts for chat sessions, message schema, chat loop boundaries, persona response boundaries, history boundaries, permission/audit links, model adapter boundaries, and Sprint 162 CLI alpha readiness without accepting runtime messages, persisting chat history, dispatching model requests, executing commands, mutating files, or enabling autonomous actions.",
                },
                {
                    "id": "aura_control_center_runtime_review_stabilization_151_160",
                    "name": "AURA Control Center Runtime Review Stabilization 151-160",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.160.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center Runtime stabilization checkpoint reviewing Sprint 151-159 panel readiness, runtime-disabled boundaries, route/navigation metadata, read-only data contracts, permission/audit links, service monitor/action log surfaces, security/accessibility notes, and next Local Chat Runtime block readiness without starting servers, mounting routes, serving requests, reading live stores, binding ports, dispatching actions, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_read_only_route_map_foundation",
                    "name": "AURA Control Center Read-Only Route Map Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.159.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center route map foundation for dashboard navigation metadata, route definitions, panel crosslinks, route guard boundaries, filtering/grouping, empty/error states, accessibility/security review, and no route map runtime activation without mounting routes, serving requests, starting servers, binding ports, dispatching actions, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_action_log_panel_foundation",
                    "name": "AURA Control Center Action Log Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.158.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center action log panel foundation for action history summaries, action boundary visibility, plugin/action linkage, permission/audit linkage, filters/grouping, privacy and redaction boundaries, accessibility/security review, and no action log panel runtime activation without reading live stores, appending logs, dispatching actions, executing tools or commands, serving dashboard requests, binding ports, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_service_monitor_panel_foundation",
                    "name": "AURA Control Center Service Monitor Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.157.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center service monitor panel foundation for service runtime state summaries, process boundary visibility, health signal cards, restart/recovery status, localhost/security visibility, filters/grouping, error boundaries, accessibility and security review, and no service monitor panel runtime activation without probing live processes, starting services, executing commands, serving dashboard requests, binding ports, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_audit_panel_foundation",
                    "name": "AURA Control Center Audit Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.156.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center audit panel foundation for audit link summaries, event reference visibility, log boundaries, trace-chain summary, retention/redaction boundaries, filtering/grouping, error boundaries, accessibility and security review, and no audit panel runtime activation without reading live audit logs, writing audit events, appending logs, redacting records, serving dashboard requests, binding ports, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_permission_panel_foundation",
                    "name": "AURA Control Center Permission Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.155.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center permission panel foundation for permission request summaries, grant boundary visibility, risk badges, permission filtering/grouping, error boundaries, accessibility, security review, next audit-viewer readiness, and no permission panel runtime activation without creating permission requests, applying grants, mutating permissions, reading live permission stores, writing audits, serving dashboard requests, binding ports, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_plugin_panel_foundation",
                    "name": "AURA Control Center Plugin Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.154.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center plugin panel foundation for plugin layout, plugin registry summary, action status semantics, permission boundary visibility, plugin filtering/grouping, error boundaries, accessibility, security review, next service-monitor readiness, and no plugin panel runtime activation without starting servers, reading live plugin runtime data, rendering live panels, mounting routes, serving dashboard requests, binding ports, dispatching plugin actions, mutating permissions, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_capability_viewer_foundation",
                    "name": "AURA Control Center Capability Viewer Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.153.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center capability viewer foundation for capability layout, registry summary, state indicators, filtering and grouping, runtime boundary visibility, permission and audit visibility, error boundaries, accessibility, next service-monitor readiness, and no capability viewer runtime activation without starting servers, reading live runtime data, rendering live panels, mounting routes, serving dashboard requests, binding ports, dispatching actions, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_read_only_status_panel_foundation",
                    "name": "AURA Control Center Read-Only Status Panel Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.152.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center status panel foundation for status layout, summary data contract, indicator semantics, safe-idle state, error boundaries, refresh policy review, accessibility, security boundary, next capability-viewer readiness, and no status panel runtime activation without starting servers, polling status, rendering live panels, mounting routes, serving dashboard requests, binding ports, dispatching actions, or enabling runtime execution features.",
                },
                {
                    "id": "aura_control_center_runtime_foundation",
                    "name": "AURA Control Center Runtime Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.151.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and read-only Control Center Runtime Foundation for future localhost-only dashboard shell, panel manifest, route blueprints, data-source contracts, permission/audit links, safe-idle and security boundaries, and no Control Center runtime activation without starting servers, binding ports, mounting routes, serving dashboard requests, dispatching actions, writing runtime state, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_review_stabilization_141_150",
                    "name": "AURA Service Review Stabilization 141-150",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.150.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only stabilization checkpoint for Sprint 141-150 Local Service Runtime Foundation completion, runtime zero counters, release gate continuity, capability registry state, documentation consistency, and Sprint 151 Control Center Runtime readiness without starting services, binding ports, writing runtime state, opening release gates, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_security_localhost_binding_review",
                    "name": "AURA Service Security and Localhost Binding Review",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.149.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Service Security and Localhost Binding Review for future localhost-only binding policy, public network exposure blocking, origin/host allowlist policy, loopback interface boundaries, deferred TLS/CORS/external access, Control Center security surfaces, permission/audit links, port binding preflight security, security error boundaries, and no security/binding runtime activation without opening sockets, binding ports, starting HTTP listeners, probing networks, writing security config, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_recovery_restart_policy_foundation",
                    "name": "AURA Service Recovery and Restart Policy Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.148.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Service Recovery and Restart Policy Foundation for future service failure classification, safe-idle recovery, restart approval, retry cooldown, rollback visibility, Control Center recovery surfaces, permission links, audit links, error boundaries, and no recovery/restart runtime activation review without writing recovery state, starting retry timers, restarting services, modifying files/config, reverting git, executing systemd or shell commands, binding ports, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_control_command_review_foundation",
                    "name": "AURA Service Control Command Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.147.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Service Control Command Review Foundation for future service start/stop/restart/status command review scopes, command proposal contracts, permission boundaries, audit links, Control Center command surfaces, failure safe-idle behavior, and no service control command runtime activation review without executing service commands, probing process state, calling systemd or shell commands, starting services, binding ports, writing audit events, mutating permissions, executing tools/commands, using file/memory/model/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_audit_link_foundation",
                    "name": "AURA Service Audit Link Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.146.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Service Audit Link Foundation for future service audit event references, audit link contracts, traceability chains, permission/audit pairing, Control Center audit visibility, redaction boundaries, failure safe-idle behavior, retention boundaries, error boundary, and no audit link runtime activation review without creating audit link records, writing audit events, appending audit logs, executing redaction runtime, writing trace chains, starting services, binding ports, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_service_permission_gate_runtime_boundary",
                    "name": "AURA Service Permission Gate Runtime Boundary",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "critical",
                    "permission_required": "read_project",
                    "introduced_in": "0.145.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Service Permission Gate Runtime Boundary for future service permission scopes, request contracts, grant preflight, denial safe-idle behavior, Control Center permission visibility, audit linkage, grant expiry review, error boundary, manual approval boundary, and no permission runtime activation review without creating permission requests, applying grants, mutating permissions, writing audit events, starting services, binding ports, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_local_service_configuration_port_registry_foundation",
                    "name": "AURA Service Configuration and Port Registry Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.144.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Service Configuration and Port Registry Foundation for future service configuration scope, config schema, port registry schema, localhost port policy, reserved port policy, port conflict preflight, environment override boundary, Control Center config card, permission/audit config linkage, and no config/port runtime activation review without reading or writing runtime configuration, reserving ports, binding ports, opening sockets, starting servers, mutating environment state, writing files, mutating permissions, writing audit events, dispatching actions, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_local_service_health_endpoint_foundation",
                    "name": "AURA Local Service Health Endpoint Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.143.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Local Service Health Endpoint Foundation for future localhost-only health endpoint scope, read-only /health contract, health response schema, localhost binding boundary, safe-idle health state, dependency visibility, permission/audit health linkage, Control Center health card, error fallback, and no-health-endpoint-activation review without starting servers, opening sockets, binding ports, serving HTTP, polling networks, writing files, mutating permissions, writing audit events, dispatching actions, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_local_service_safe_idle_boot_boundary",
                    "name": "AURA Local Service Safe Idle Boot Boundary",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.142.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Local Service Safe Idle Boot Boundary for ATLAS safe-idle boot scope, boot entry state contracts, guard conditions, boot failure fallback, no-autostart boundary, read-only readiness probes, Control Center idle visibility, permission denial idle behavior, audit failure idle behavior, and no-boot-activation review without starting services, autostarting, opening sockets, binding ports, creating or starting systemd units, dispatching actions, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_local_service_runtime_foundation",
                    "name": "AURA Local Service Runtime Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "high",
                    "permission_required": "read_project",
                    "introduced_in": "0.141.0-genesis",
                    "category": "service",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and foundation-only Local Service Runtime Foundation for ATLAS safe-idle service identity, localhost-only boundary, lifecycle state, configuration contract, health surface, permission gate link, audit link, control command boundary, and no-start activation review without starting services, opening sockets, binding ports, creating systemd units, dispatching actions, executing tools/commands, using file/memory/model/permission/audit/ORION/git runtime, or enabling runtime execution features.",
                },
                {
                    "id": "aura_review_stabilization_131_140_foundation",
                    "name": "AURA Review Stabilization 131-140 Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.140.0-genesis",
                    "category": "stabilization",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Review & Stabilization 131-140 Foundation covering Sprint 131-140 scope, runtime boundary integrity, capability registry consistency, system status surfaces, skill/plugin/CLI/shell integration, documentation roadmap state, safety counter zero state, git/boot verification, next block readiness, and no-runtime-activation review without service/API/dashboard/chat/memory/permission/audit/model/action/tool/command/file/port/network/ORION/git runtime or runtime execution features.",
                },
                {
                    "id": "aura_audit_runtime_writer_activation_review_foundation",
                    "name": "AURA Audit Runtime Writer Activation Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.139.0-genesis",
                    "category": "audit",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Audit Runtime Writer Activation Review Foundation covering audit writer activation scope, event schema, append-only storage, redaction boundary, actor context, permission links, dashboard visibility, failure safe idle, retention/export, and no-write activation review without starting/stopping audit writers, receiving/writing audit events, appending logs, writing storage, redaction runtime, dashboard event emit, permission mutation, action dispatch, tool/command execution, file/service/port/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_permission_runtime_grant_gate_review_foundation",
                    "name": "AURA Permission Runtime Grant Gate Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.138.0-genesis",
                    "category": "permission",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Permission Runtime Grant Gate Review Foundation covering permission grant scope, manual approval, expiry, denial, audit link, dashboard visibility, revocation, risk classification, safe idle failure, and no-mutation review without receiving runtime permission requests, creating/applying/updating/revoking grants, applying expiry, creating denials, risk classification runtime, audit writer/event runtime, dashboard event emit, action dispatch, tool/command execution, file/service/port/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_memory_runtime_write_gate_review_foundation",
                    "name": "AURA Memory Runtime Write Gate Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.137.0-genesis",
                    "category": "memory",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Memory Runtime Write Gate Review Foundation covering memory write intent classification, manual approval, scope boundary, redaction, conflict resolution, audit event, rollback, safe idle failure, session link, and no-persistence review without reading memory, writing memory, creating/updating/deleting memory records, receiving runtime memory write requests, creating permission grants, starting audit writers, writing audit events, rollback/recovery execution, dashboard event emit, action dispatch, tool/command execution, file/service/port/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_chat_runtime_minimal_loop_review_foundation",
                    "name": "AURA Chat Runtime Minimal Loop Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.136.0-genesis",
                    "category": "chat",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Chat Runtime Minimal Loop Review Foundation covering chat input boundary, response boundary, session state, permission prompts, memory read/write gates, audit events, safe idle fallback, error recovery, manual approval runtime entry, and no-model-execution review without starting chat runtime, receiving or processing runtime messages, generating or sending responses, mutating sessions, reading/writing memory, creating permission prompts, starting audit writers, model request/inference execution, action dispatch, tool/command execution, file/service/port/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_control_center_runtime_entry_review_foundation",
                    "name": "AURA Control Center Runtime Entry Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.135.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Control Center Runtime Entry Review Foundation covering entry route, localhost boundary, read-only default, status panel runtime entry, permission panel runtime entry, audit panel runtime entry, action proposal panel runtime entry, safe idle/error panel runtime entry, manual approval entry, and no-server-start review without creating routes, binding routes, starting Control Center, starting dashboard/API/web/frontend/backend servers, binding ports, starting panels, emitting dashboard events, creating permission grants, starting audit writers, action dispatch, tool/command execution, file/service/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_local_service_boot_plan_review_foundation",
                    "name": "AURA Local Service Boot Plan Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.134.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Local Service Boot Plan Review Foundation for ATLAS covering manual start, manual stop, health monitor, safe shutdown, config contract, log visibility, localhost-only behavior, autostart guard, failure safe idle, and no-port-binding review without creating service units, modifying startup configuration, enabling autostart, starting services, binding ports, starting API/web/dashboard/chat/memory/permission/audit runtime, action dispatch, tool/command execution, file/service/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_runtime_activation_path_proposal_review_foundation",
                    "name": "AURA Runtime Activation Path Proposal Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.133.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Runtime Activation Path Proposal Review Foundation for runtime activation stage model, manual approval chain, activation blocker register links, permission contract activation, audit contract activation, dashboard visibility activation, safe idle rollback activation, emergency stop activation, release candidate transition, and activation denial/deferment review without applying activation paths, enabling stages, opening runtime gates, starting runtime activation, release candidates, local services, dashboard/chat/memory/permission/audit runtime, blocker mutations, action dispatch, tool/command execution, file/service/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_final_genesis_acceptance_criteria_foundation",
                    "name": "AURA Final Genesis Acceptance Criteria Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.132.0-genesis",
                    "category": "planning",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Final Genesis Acceptance Criteria Foundation for boot stability, local service, Control Center, local chat, memory, permission/audit, safe idle/recovery, optional ORION/voice/vision/avatar boundaries, Final Genesis go/no-go, and future runtime release candidate criteria without Final Genesis release, release candidate runtime, service boot, dashboard/chat/memory runtime, permission grants, audit writer runtime, action dispatch, tool/command execution, file/service/network/ORION/voice/vision/avatar/streaming/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_post_checkpoint_130_next_block_foundation",
                    "name": "AURA Post-Checkpoint 130 Next Block Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.131.0-genesis",
                    "category": "planning",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Post-Checkpoint 130 Next Block Foundation for the Sprint 131-140 block toward Final Genesis, including sprint sequence, Final Genesis acceptance criteria direction, runtime activation path proposal, local service boot plan, Control Center runtime entry, chat runtime minimal loop, memory runtime write gate, permission runtime grant gate, audit runtime writer activation, and Sprint 140 stabilization checkpoint without runtime activation, service boot, dashboard/chat/memory runtime, permission grant runtime, audit writer runtime, action dispatch, tool/command execution, file/service/network/ORION/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_review_stabilization_121_130_foundation",
                    "name": "AURA Review Stabilization 121-130 Foundation",
                    "state": "online",
                    "runtime_level": "review_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.130.0-genesis",
                    "category": "stabilization",
                    "control_center_visible": True,
                    "description": "Review-only Sprint 121-130 stabilization checkpoint for Sprint 121-129 completion, capability registry consistency, permission boundaries, runtime zero counters, dashboard/ORION boundaries, action/permission/recovery/blocker boundaries, documentation and roadmap consistency, boot/CLI surfaces, known deferred runtime, and future Sprint 131-140 readiness without runtime activation, checkpoint mutation, registry mutation, permission change, audit write, dashboard emit, action dispatch, tool/command execution, file/service/network/ORION/memory/git runtime, or runtime execution features.",
                },
                {
                    "id": "aura_runtime_activation_blocker_register_boundary_review_foundation",
                    "name": "AURA Runtime Activation Blocker Register Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.129.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Runtime Activation Blocker Register Boundary Review Foundation for blocker register schema, blocker source classification, blocker severity policy, blocker activation gate link, blocker resolution evidence, blocker dashboard visibility, blocker audit link, blocker failure safe idle, and future runtime activation unblock boundaries without creating, updating, deleting, resolving, or unblocking runtime activation blockers; opening runtime gates; activating runtime; writing audit events; emitting dashboard events; dispatching actions; or enabling runtime execution.",
                },
                {
                    "id": "aura_dashboard_runtime_readiness_boundary_review_foundation",
                    "name": "AURA Dashboard Runtime Readiness Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.128.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Dashboard Runtime Readiness Boundary Review Foundation for dashboard runtime entrypoint, route contract, API contract, websocket event, permission panel runtime, audit panel runtime, action panel runtime, failure safe idle, and future dashboard runtime activation boundaries without starting dashboard/web/API/frontend/backend servers, binding ports, opening browsers, registering runtime routes, opening websockets, emitting dashboard events, changing permissions, writing audit events, dispatching actions, or enabling runtime execution.",
                },
                {
                    "id": "aura_runtime_recovery_drill_boundary_review_foundation",
                    "name": "AURA Runtime Recovery Drill Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.127.0-genesis",
                    "category": "runtime",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Runtime Recovery Drill Boundary Review Foundation for recovery drill scenario catalog, recovery trigger, recovery safe idle, rollback preview, recovery audit/dashboard, recovery permission, ORION recovery disconnect, recovery failure escalation, and future runtime recovery drill boundaries without starting recovery drills, executing recovery actions, applying rollback, restarting services, mutating permissions, writing audit events, emitting dashboard events, dispatching actions, or enabling runtime execution.",
                },
                {
                    "id": "aura_runtime_grant_expiry_boundary_review_foundation",
                    "name": "AURA Runtime Grant Expiry Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.126.0-genesis",
                    "category": "permission",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Runtime Grant Expiry Boundary Review Foundation for grant expiry schema, grant lifetime policy, grant renewal request, grant revocation, expired grant denial, dashboard grant visibility, audit grant expiry, grant expiry failure safe idle, and future runtime grant expiry boundaries without creating grants, renewing grants, revoking grants, applying expiry state, mutating permissions, writing audit events, emitting dashboard events, dispatching actions, or enabling runtime execution.",
                },
                {
                    "id": "aura_safe_local_action_allowlist_boundary_review_foundation",
                    "name": "AURA Safe Local Action Allowlist Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.125.0-genesis",
                    "category": "actions",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Safe Local Action Allowlist Boundary Review Foundation for safe action catalog, action scope, permission requirements, risk levels, rollback references, audit/dashboard visibility, denied action policy, runtime gates, and future safe local action runtime boundaries without applying allowlists, creating permission requests, dispatching actions, executing actions, writing audit events, emitting dashboard events, using file runtime, starting services, probing network, performing ORION handshakes, or enabling runtime execution.",
                },
                {
                    "id": "aura_orion_dry_handshake_boundary_review_foundation",
                    "name": "AURA ORION Dry Handshake Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.124.0-genesis",
                    "category": "orion",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only ORION Dry Handshake Boundary Review Foundation for client identity packets, capability packets, permission scope packets, status heartbeat, redaction, emergency stop, ATLAS/ORION authority, ORION failure safe idle, and future ORION handshake runtime boundaries without starting ORION client runtime, performing handshakes, sending packets, probing network, emitting dashboard events, changing permissions, or enabling runtime execution.",
                },
                {
                    "id": "aura_dashboard_control_center_boundary_review_foundation",
                    "name": "AURA Dashboard Control Center Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.123.0-genesis",
                    "category": "dashboard",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Dashboard Control Center Boundary Review Foundation for shell layout, status payload, permission panel, audit panel, action proposal panel, ORION client panel, runtime gate panel, dashboard failure safe idle policy, and future dashboard control center runtime boundaries without starting dashboard runtime, starting web/API/frontend/backend services, binding routes or ports, emitting dashboard events, changing permissions, performing ORION handshakes, or enabling runtime execution.",
                },
                {
                    "id": "aura_runtime_permission_audit_writer_boundary_review_foundation",
                    "name": "AURA Runtime Permission Audit Writer Boundary Review Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.122.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Runtime Permission Audit Writer Boundary Review Foundation for schema, storage, redaction, visibility, permission decision links, dashboard audit payloads, failure boundaries, runtime gates, and future permission audit writer runtime boundaries without starting audit writer runtime, writing audit events, persisting audit records, writing audit files, changing permissions, emitting dashboard events, performing ORION handshakes, or enabling runtime execution.",
                },
                {
                    "id": "aura_post_checkpoint_120_next_block_planning_foundation",
                    "name": "AURA Post-Checkpoint 120 Next Block Planning Foundation",
                    "state": "online",
                    "runtime_level": "foundation_only",
                    "risk_level": "low",
                    "permission_required": "read_project",
                    "introduced_in": "0.121.0-genesis",
                    "category": "runtime_readiness",
                    "control_center_visible": True,
                    "description": "Planner-only, metadata-only, and review-only Post-Checkpoint 120 Next Block Planning Foundation for checkpoint 120 output review, Sprint 121-130 scope definition, runtime readiness continuation, permission audit writer boundaries, dashboard control center boundaries, ORION dry handshake boundaries, safe local action allowlist boundaries, runtime activation blocker tracking, and future checkpoint 130 boundaries without approving runtime, opening release gates, starting dashboard runtime, enabling audit writer runtime, performing ORION handshakes, or enabling runtime execution.",
                },
            {
                "id": "aura_local_web_runtime_alpha",
                "name": "AURA Local Web Runtime Alpha",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.181.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Explicitly confirmed, foreground-only, "
                    "localhost-only, read-only HTTP runtime alpha "
                    "exposing only /, /health, and /api/status on "
                    "127.0.0.1 while chat, model calls, memory "
                    "writes, permission mutation, audit writes, "
                    "commands, tools, arbitrary file access, "
                    "desktop control, voice, vision, public/LAN "
                    "binding, background service, and autonomous "
                    "actions remain disabled."
                ),
            },
            {
                "id": "aura_service_lifecycle_runtime",
                "name": "AURA Service Lifecycle Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "high",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.182.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Deterministic in-memory lifecycle wrapper for the "
                    "Sprint 181 localhost listener with stopped, starting, "
                    "running, stopping, and failed states; single-listener "
                    "ownership, port-conflict fail-closed handling, startup "
                    "rollback, clean programmatic stop, and clean SIGINT or "
                    "SIGTERM foreground shutdown. Background service, systemd, "
                    "automatic startup, persistent PID/state files, remote "
                    "lifecycle mutation, chat, models, commands, tools, files, "
                    "desktop, voice, vision, and autonomy remain disabled."
                ),
            },
            {
                "id": "aura_health_status_api_runtime",
                "name": "AURA Health and Status API Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.183.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Read-only health and status aggregation plus nine "
                    "localhost HTTP payload routes for identity, boot "
                    "prerequisites, plugins, capabilities, service lifecycle, "
                    "memory availability, safety boundaries, and transparent "
                    "error or degraded reporting. GET and HEAD are allowed; "
                    "mutation methods, plugin start, memory writes, remote "
                    "control, background service, systemd, auto-start, chat, "
                    "models, commands, tools, files, desktop, voice, vision, "
                    "and autonomy remain disabled."
                ),
            },
            {
                "id": "aura_control_center_backend_runtime",
                "name": "AURA Control Center Backend Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.184.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Read-only Control Center backend view models with nine "
                    "localhost JSON routes and eight panels for overview, "
                    "service, capabilities, plugins, permissions, audit, "
                    "memory, and readiness. It reuses the existing listener "
                    "and lifecycle; frontend assets, browser launch, service "
                    "or plugin controls, permission decisions, audit writes, "
                    "memory writes, chat, models, commands, tools, actions, "
                    "background service, public/LAN binding, and autonomy "
                    "remain disabled."
                ),
            },
            {
                "id": "aura_control_center_web_shell_runtime",
                "name": "AURA Control Center Web Shell Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.185.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Usable localhost-only read-only Control Center web "
                    "shell with three local static assets and eight panels "
                    "for overview, service, capabilities, plugins, "
                    "permissions, audit, memory, and readiness. It uses "
                    "the existing listener and backend, has no external "
                    "dependencies, and exposes no service controls, plugin "
                    "controls, permission decisions, audit writes, memory "
                    "writes, chat, models, commands, tools, actions, "
                    "background service, public/LAN binding, or autonomy."
                ),
            },
            {
                "id": "aura_browser_chat_session_runtime",
                "name": "AURA Browser Chat Session Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_chat_runtime",
                "introduced_in": "0.186.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Localhost-only browser chat session runtime with "
                    "bounded session creation, validated message "
                    "submission, deterministic honest placeholder "
                    "response delivery, atomic local history persistence, "
                    "session reload, optimistic revision control, "
                    "idempotent client message replay, integrity hashes, "
                    "and explicit clear confirmation. Local model "
                    "inference, network fallback, AURA long-term memory "
                    "writes, tools, commands, actions, arbitrary files, "
                    "desktop control, background service, public/LAN "
                    "binding, browser auto-launch, and autonomy remain "
                    "disabled."
                ),
            },
            {
                "id": "aura_local_model_bridge_runtime",
                "name": "AURA Local Model Bridge Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "high",
                "permission_required": "model_request_permission",
                "category": "local_model_runtime",
                "introduced_in": "0.187.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Loopback-only local model bridge supporting Ollama "
                    "and OpenAI-compatible provider contracts, strict "
                    "environment-only profiles, explicit probe and model "
                    "request confirmation, bounded text-only inference, "
                    "browser chat model-response persistence, optimistic "
                    "revision conflicts, idempotent replay without duplicate "
                    "model invocation, provider-failure rollback, resolved "
                    "loopback enforcement, and redirect blocking. Model "
                    "downloads, remote providers, internet fallback, "
                    "streaming, tool or function calling, commands, actions, "
                    "desktop control, arbitrary files, AURA long-term memory "
                    "writes, background service, public/LAN binding, and "
                    "autonomy remain disabled."
                ),
            },
            {
                "id": "aura_interactive_control_center_chat_runtime",
                "name": "AURA Interactive Control Center Chat Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "high",
                "permission_required": "model_request_permission",
                "category": "local_interaction_runtime",
                "introduced_in": "0.188.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Interactive localhost Control Center chat with "
                    "persistent bounded sessions, save-only safe default, "
                    "provider and model visibility, explicit provider probe "
                    "confirmation, explicit per-message model confirmation, "
                    "text-only local model responses, stable in-memory retry "
                    "identifiers, optimistic revision conflicts, idempotent "
                    "replay without duplicate model invocation, response-kind "
                    "visibility, restart persistence, and confirmed session "
                    "clearing. Model downloads, remote providers, internet "
                    "fallback, streaming, tools, commands, actions, arbitrary "
                    "files, desktop control, AURA long-term memory writes, "
                    "browser storage, WebSocket/EventSource, background "
                    "service, public/LAN binding, browser auto-launch, and "
                    "autonomy remain disabled."
                ),
            },
            {
                "id": "aura_permission_audit_recovery_visibility_runtime",
                "name": "AURA Permission, Audit, and Recovery Visibility Runtime",
                "state": "online",
                "runtime_level": "permission_gated_alpha_runtime",
                "risk_level": "medium",
                "permission_required": "user_confirmation",
                "category": "local_interaction_runtime",
                "introduced_in": "0.189.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Read-only localhost permission, audit-contract, and "
                    "recovery-guidance visibility through five operator CLI "
                    "commands, one responsive Control Center page, three "
                    "browser assets, and four GET/HEAD API routes. Provider "
                    "state values are redacted; message and model-response "
                    "content are not recorded. Mutation HTTP methods are "
                    "blocked. Permission grant/revoke/persistence, audit "
                    "writer/persistence, automatic retry/restart/recovery, "
                    "rollback execution, model downloads, internet fallback, "
                    "tools, commands, actions, arbitrary files, desktop "
                    "control, AURA long-term memory writes, background "
                    "service, public/LAN binding, browser auto-launch, and "
                    "autonomy remain disabled."
                ),
            },
            {
                "id": "aura_local_interaction_runtime_stabilization",
                "name": "AURA Local Interaction Runtime Stabilization",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "low",
                "permission_required": "none",
                "category": "local_interaction_runtime",
                "introduced_in": "0.190.0-genesis",
                "control_center_visible": True,
                "description": (
                    "Review-only stabilization checkpoint for the Sprint "
                    "181-190 Local Interaction Runtime Activation chain. "
                    "It validates nine runtime components through ten "
                    "existing self-test commands, confirms 1,175 total "
                    "assertions, zero stabilization gaps, zero runtime "
                    "violations, localhost-only listener policy, clean "
                    "shutdown, fail-closed port conflicts, visible errors, "
                    "no permission bypass, and no arbitrary execution. "
                    "Sprint 190 adds no listener, provider, persistence "
                    "store, permission mutation, audit writer, recovery "
                    "executor, command, tool, action, desktop, voice, "
                    "vision, background service, public/LAN binding, or "
                    "autonomous runtime."
                ),
            },

            {
                "id": "aura_genesis_stabilization_runtime_hardening",
                "name": "AURA Genesis Stabilization Runtime Hardening",
                "state": "online",
                "runtime_level": "review_only",
                "risk_level": "low",
                "permission_required": "read_project",
                "introduced_in": "1.0.1-genesis",
                "category": "stabilization",
                "control_center_visible": True,
                "description": (
                    "Deterministic, read-only Sprint 241 runtime "
                    "hardening for exact CLI command ownership, "
                    "pre-construction rejection of unrelated "
                    "commands, immutable finalized-release status "
                    "projection, explicit deep contract continuity, "
                    "latency regression checks, and memory/journal "
                    "integrity verification without activating "
                    "services, listeners, systemd, release gates, "
                    "ORION control, broad voice or vision runtime, "
                    "or autonomous execution."
                ),
            },
    {
        "id": "aura_service_lifecycle_determinism",
        "name": "AURA Service Lifecycle Determinism",
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.2-genesis",
        "category": "stabilization",
        "control_center_visible": True,
        "description": (
            "Deterministic Sprint 242 lifecycle hardening "
            "for startup-stop race rejection, repeated-stop "
            "idempotency, pure-JSON lifecycle validation "
            "output, and preserved normal access logging "
            "without enabling PID persistence, lifecycle "
            "state persistence, systemd, background daemons, "
            "remote lifecycle control, HTTP mutation, or "
            "automatic startup."
        ),
    },
    {
        "id": "aura_configuration_integrity",
        "name": "AURA Configuration Integrity",
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.3-genesis",
        "category": "stabilization",
        "control_center_visible": True,
        "description": (
            "Read-only Sprint 243 canonical settings "
            "integrity validation for path safety, YAML "
            "mapping and exact schema, local-only "
            "reasoning and web endpoints, safe-idle and "
            "explicit-confirmation boundaries, traversal "
            "rejection, secret-like key rejection, and "
            "deterministic negative fixtures without "
            "configuration writes, environment mutation, "
            "runtime activation, socket binding, memory "
            "writes, journal writes, or systemd mutation."
        ),
    },
    {
        "id": "aura_session_memory_persistence_checks",
        "name": "AURA Session and Memory Persistence Checks",
        "description": (
            "Read-only validation of canonical browser "
            "sessions, chat history, memory, and journal "
            "stores, including schema, integrity, path, "
            "timestamp, duplicate-id, and safety-boundary "
            "visibility without repair, migration, writes, "
            "runtime activation, socket binding, or systemd "
            "mutation."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.4-genesis",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {
        "id": "aura_log_rotation_storage_cleanup",
        "name": "AURA Log Rotation and Storage Cleanup",
        "category": "stabilization",
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "description": "Read-only inspection of the canonical AURA log rotation policy, seven-day retention policy, filesystem capacity, active-log protection, rotated-log allowlist, and cleanup-preview candidates without deleting, moving, truncating, compressing, archiving, or mutating canonical logs, session data, conversation history, memory, journal, audit data, services, sockets, systemd, network state, or runtime execution features.",
        "introduced_in": "1.0.5-genesis",
        "visible": True,
    },
    {
        "id": "aura_resource_baseline_metrics",
        "name": "AURA Resource Baseline Metrics",
        "description": (
            "Read-only Sprint 246 single-snapshot "
            "baseline visibility for CPU usage and load, "
            "memory, swap, uptime, process count, filesystem "
            "capacity, and inode capacity across root, home, "
            "AURA data storage, and the project root without "
            "psutil, background sampling, history persistence, "
            "dashboard activation, socket binding, systemd "
            "mutation, network access, process control, or "
            "threshold mutation."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.6-genesis",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {
        "id": "aura_atlas_resource_monitoring",
        "name": "AURA ATLAS Resource Monitoring",
        "description": (
            "Read-only Sprint 247 ATLAS health classification "
            "for CPU, load average, memory, swap, storage, inode "
            "capacity, uptime, and process count using the Sprint "
            "246 resource baseline snapshot with immutable warning "
            "and critical thresholds, absolute free-space checks, "
            "and healthy, warning, critical, or unavailable states "
            "without background sampling, rolling history, metrics "
            "persistence, dashboard activation, alert delivery, "
            "socket binding, systemd mutation, network access, "
            "process control, command execution, or threshold mutation."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.7-genesis",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {
        "id": "aura_localhost_ssh_tunnel_security_review",
        "name": "AURA Localhost and SSH Tunnel Security Review",
        "description": (
            "Read-only Sprint 248 security posture review for AURA "
            "localhost binding, port 8765 exposure, SSH listener "
            "scope, visible sshd configuration, tunnel policy, SSH "
            "file permission metadata, firewall visibility, and "
            "runtime activation. The review reports secure, review, "
            "warning, or unavailable states without executing sshd, "
            "opening connections or tunnels, reading credentials or "
            "private-key content, changing SSH or firewall settings, "
            "restarting services, binding sockets, controlling "
            "processes, mutating systemd, or generating keys."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.8-genesis",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {
        "id": "aura_permission_expiry_recovery_review",
        "name": "AURA Permission Expiry and Recovery Review",
        "description": (
            "Read-only Sprint 249 review of permission grant lifecycle, "
            "expiry enforcement, stale-grant rejection, denial lifecycle, "
            "revocation visibility, recovery visibility, rollback and "
            "emergency-stop linkage, and audit linkage. The review "
            "inspects source contracts and filesystem metadata without "
            "importing or executing permission runtime, reading permission "
            "or audit store contents, creating or applying grants or "
            "denials, applying expiry or revocation, executing recovery, "
            "rollback, emergency stop, writing audit events, mutating "
            "files, controlling processes, activating services, opening "
            "network access, binding sockets, or mutating systemd."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.0.9-genesis",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {
        "id": "aura_backup_restore_rehearsal",
        "name": "AURA Backup and Restore Rehearsal",
        "description": (
            "Read-only Sprint 250 backup and restore rehearsal "
            "covering backup scope inventory, manifest and digest "
            "integrity, restore-plan reversibility, permission and "
            "approval boundaries, audit and provenance linkage, "
            "safe-idle failure verification, contract deduplication, "
            "and Sprint 241-250 block release acceptance. The "
            "rehearsal inspects Python source contracts and path "
            "metadata without creating backups or archives, reading "
            "canonical data or backup-store contents, executing "
            "restore or rollback, replacing or deleting files, "
            "mutating permissions or audit state, controlling "
            "processes, activating services, opening network access, "
            "binding sockets, or mutating systemd."
        ),
        "state": "online",
        "runtime_level": "review_only",
        "risk_level": "low",
        "permission_required": "read_project",
        "introduced_in": "1.1.0",
        "category": "stabilization",
        "control_center_visible": True,
    },
    {'id': 'aura_launcher_service_controls',
     'name': 'AURA Launcher and Service Controls',
     'description': 'Read-only integration facade for launcher and service-control '
                    'visibility, lifecycle ownership, approval, audit, recovery, and '
                    'safe-idle handoff.',
     'state': 'online',
     'runtime_level': 'review_only',
     'risk_level': 'low',
     'permission_required': 'read_project',
     'introduced_in': '1.1.1',
     'category': 'runtime_integration',
     'control_center_visible': True},
    {'id': 'manual_start_stop_status_runtime',
     'name': 'Manual Start, Stop, and Status Runtime',
     'description': 'Permission-gated supervised local runtime for explicit manual service '
                    'start, verified owned-process stop, idempotent control, and live '
                    'lifecycle, listener, ownership, and loopback health status. Restart, '
                    'autostart, systemd mutation, non-loopback binding, permission-store '
                    'mutation, and persistent audit writing remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.2',
     'category': 'runtime_control',
     'control_center_visible': True},

    {'id': 'restart_logs_failure_visibility',
     'name': 'Restart, Logs, and Failure Visibility',
     'description': 'Permission-gated supervised local restart through the canonical '
                    'manual runtime owner, bounded allowlisted and redacted log tail '
                    'visibility, and structured failure packets. Unowned runtime '
                    'evidence, arbitrary PID signaling, arbitrary log paths, systemd '
                    'mutation, autostart mutation, non-loopback binding, permission-store '
                    'mutation, persistent audit writing, and canonical-log mutation '
                    'remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.3',
     'category': 'runtime_control',
     'control_center_visible': True},
    {'id': 'process_ownership_service_state_persistence',
     'name': 'Process Ownership and Service State Persistence',
     'description': 'Persistent project-local ownership state with atomic descriptor-safe '
                    'writes and strict PID, process start, boot, UID, command, cwd, and '
                    'loopback endpoint identity. Stale records recover only through '
                    'approved start, stop, or restart. Systemd, autostart, arbitrary PID '
                    'signaling, non-loopback binding, automatic cleanup, permission-store '
                    'mutation, and persistent audit writing remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.4',
     'category': 'runtime_control',
     'control_center_visible': True},
    {'id': 'reviewed_optional_autostart',
     'name': 'Reviewed Optional Autostart',
     'description': 'Review-only systemd user-service contract, host posture, exact unit '
                    'preview, explicit activation plan, and rollback plan. The target '
                    'unit is aura-local.service under the current user manager with '
                    'bounded on-failure restart. Unit writing, daemon reload, enable, '
                    'start, linger change, system-unit mutation, non-loopback binding, '
                    'and automatic activation remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.5',
     'category': 'runtime_control',
     'control_center_visible': True},
    {'id': 'persistent_local_chat_session_activation',
     'name': 'Persistent Local Chat Session Activation',
     'description': 'Hardened project-local browser chat session persistence using '
                    'descriptor-safe reads, O_NOFOLLOW, fstat, cross-process directory '
                    'locking, private 0700 storage, private 0600 session files, atomic '
                    'replace and fsync, integrity hashes, revision control, bounded '
                    'metadata history, exact session loading, and explicit existing '
                    'memory gates. Model-service activation, network fallback, '
                    'non-loopback binding, automatic memory handoff, content logging, '
                    'systemd mutation, and autostart activation remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.6',
     'category': 'local_chat',
     'control_center_visible': True},
    {'id': 'local_model_service_discovery_health',
     'name': 'Local Model Service Discovery and Health',
     'description': 'Read-only local model service discovery over the existing '
                    'Sprint 187 bridge, including Ollama binary metadata, systemd '
                    'unit state, process ownership, loopback listener posture, '
                    'environment profile posture, provider contracts, and a '
                    'default-off explicit-confirmation localhost health probe. '
                    'Model names are not exposed by the new health surface. '
                    'Service start/stop/install, model download/pull/load/unload, '
                    'chat routing, non-loopback networking, credentials, systemd '
                    'mutation, and autostart mutation remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'user_confirmation',
     'introduced_in': '1.1.7',
     'category': 'local_model_runtime',
     'control_center_visible': True},
    {'id': 'local_model_router_activation',
     'name': 'Local Model Router Activation',
     'description': 'Permission-gated exact-route selection over the existing '
                    'ModelRouter with validated local provider profile, explicit '
                    'health verification, explicit model-request confirmation, '
                    'and bounded handoff to AuraLocalModelBridgeRuntimeManager. '
                    'Unknown fallback execution, foundation/planned routes, '
                    'route persistence, real runtime switching, service control, '
                    'model download/load, queue activation, resource-budget '
                    'mutation, non-loopback networking, credentials, systemd, '
                    'and autostart mutation remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'model_request_permission',
     'introduced_in': '1.1.8',
     'category': 'local_model_runtime',
     'control_center_visible': True},
    {'id': 'model_loading_unloading_queue_resource_budgets',
     'name': 'Model Loading, Unloading, Queue, and Resource Budgets',
     'description': 'Permission-gated provider lifecycle, bounded in-memory '
                    'queueing, and read-only resource-budget gates. Automatic '
                    'load/release, model download/pull, persistent queueing, '
                    'background workers, threshold mutation, service control, '
                    'non-loopback networking, credentials, systemd, and '
                    'autostart mutation remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'model_lifecycle_permission',
     'introduced_in': '1.1.9',
     'category': 'local_model_runtime',
     'control_center_visible': True},
    {'id': 'active_local_runtime_integration_stabilization',
     'name': 'Active Local Runtime Integration and Stabilization',
     'description': 'Explicit manual coordinator for safe-idle service, '
                    'private persistent chat, loopback health, exact companion '
                    'routing, provider lifecycle, bounded queue, read-only '
                    'resource budgets, successful response persistence, and '
                    'mandatory stop-and-restore. Automatic activation, model '
                    'requests, session writes, model download/pull, persistent '
                    'queues, non-loopback networking, credentials, threshold '
                    'mutation, systemd, and autostart remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'high',
     'permission_required': 'active_local_runtime_integration_permission',
     'introduced_in': '1.2.0',
     'category': 'local_runtime_integration',
     'control_center_visible': True},
    {'id': 'operational_browser_chat_model_handoff',
     'name': 'Operational Browser Chat Model Handoff',
     'description': 'Operational persistent browser chat handoff to the '
                    'explicitly confirmed localhost companion route with native '
                    'process-role classification.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'local_model_request',
     'introduced_in': '1.2.2',
     'category': 'local_model_runtime',
     'control_center_visible': True},

    {'id': 'session_list_resume_rename_archive_restore',
     'name': 'Session List, Resume, Rename, Archive, and Restore',
     'description': 'Permission-gated local browser session lifecycle runtime for active and archived '
                    'lists, same-session resume, title-only rename, non-destructive archive, and '
                    'non-destructive restore. Permanent delete, cross-session history merge, lifecycle '
                    'model invocation, and lifecycle network access remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'local_model_request',
     'introduced_in': '1.2.3',
     'category': 'local_model_runtime',
     'control_center_visible': True},

    {'id': 'chat_history_recovery_ux',
     'name': 'Chat History Recovery UX',
     'description': 'Permission-gated local browser history recovery UX with a read-only diagnostic '
                    'endpoint, integrity failure visibility, stale-revision reload guidance, in-memory '
                    'draft preservation, missing-session neutral state, and archived-session restore '
                    'guidance. Automatic repair, quarantine, replacement, deletion, model calls, and '
                    'network fallback remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'local_model_request',
     'introduced_in': '1.2.4',
     'category': 'local_model_runtime',
     'control_center_visible': True},

    {'id': 'review_first_memory_integration',
     'name': 'Review-First Memory Integration',
     'description': 'Permission-gated local browser review runtime for explicitly selected '
                    'user-message memory candidates. Candidates live only in an in-process queue and '
                    'support edit, privacy hold, importance and pinning preview, transient rejection, '
                    'and approval of a future permission envelope preview. Candidate persistence, '
                    'review queue persistence, permission grant application, durable memory writes, '
                    'MemoryStore construction or mutation, automatic write, merge, delete, model '
                    'invocation, and network access remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'memory_write',
     'introduced_in': '1.2.5',
     'category': 'memory_runtime',
     'control_center_visible': True},
    {'id': 'control_center_runtime_ux_consolidation',
     'name': 'Control Center Runtime UX Consolidation',
     'description': 'Permission-gated local browser review runtime for explicitly selected '
                    'user-message memory candidates. Candidates live only in an in-process queue and '
                    'support edit, privacy hold, importance and pinning preview, transient rejection, '
                    'and approval of a future permission envelope preview. Candidate persistence, '
                    'review queue persistence, permission grant application, durable memory writes, '
                    'MemoryStore construction or mutation, automatic write, merge, delete, model '
                    'invocation, and network access remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'memory_write',
     'introduced_in': '1.2.6',
     'category': 'memory_runtime',
     'control_center_visible': True},
    {'id': 'atlas_resource_monitoring_dashboard',
     'name': 'ATLAS Resource Monitoring Dashboard',
     'description': 'Permission-gated local browser review runtime for explicitly selected '
                    'user-message memory candidates. Candidates live only in an in-process queue and '
                    'support edit, privacy hold, importance and pinning preview, transient rejection, '
                    'and approval of a future permission envelope preview. Candidate persistence, '
                    'review queue persistence, permission grant application, durable memory writes, '
                    'MemoryStore construction or mutation, automatic write, merge, delete, model '
                    'invocation, and network access remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'memory_write',
     'introduced_in': '1.2.7',
     'category': 'memory_runtime',
     'control_center_visible': True},
    {'id': 'permission_audit_action_visibility_ux',
     'name': 'Permission Audit Action Visibility UX',
     'description': 'Permission-gated local browser review runtime for explicitly selected '
                    'user-message memory candidates. Candidates live only in an in-process queue and '
                    'support edit, privacy hold, importance and pinning preview, transient rejection, '
                    'and approval of a future permission envelope preview. Candidate persistence, '
                    'review queue persistence, permission grant application, durable memory writes, '
                    'MemoryStore construction or mutation, automatic write, merge, delete, model '
                    'invocation, and network access remain disabled.',
     'state': 'online',
     'runtime_level': 'permission_gated_alpha_runtime',
     'risk_level': 'medium',
     'permission_required': 'memory_write',
     'introduced_in': '1.2.8',
     'category': 'memory_runtime',
     'control_center_visible': True},
]


    def capability_summary(self) -> dict[str, Any]:
        catalog = self.capability_catalog()
        state_counts: dict[str, int] = {}
        risk_counts: dict[str, int] = {}
        permission_counts: dict[str, int] = {}

        for item in catalog:
            state_counts[item["state"]] = state_counts.get(item["state"], 0) + 1
            risk_counts[item["risk_level"]] = risk_counts.get(item["risk_level"], 0) + 1
            permission = item["permission_required"]
            permission_counts[permission] = permission_counts.get(permission, 0) + 1

        return {
            "total_capabilities": len(catalog),
            "online_capabilities": state_counts.get("online", 0),
            "foundation_only_count": sum(1 for item in catalog if item["runtime_level"] == "foundation_only"),
            "planner_only_count": sum(1 for item in catalog if item["runtime_level"] == "planner_only"),
            "permission_gated_count": sum(1 for item in catalog if "permission_gated" in item["runtime_level"]),
            "review_only_count": sum(1 for item in catalog if item["runtime_level"] == "review_only"),
            "planned_future_count": state_counts.get("planned_future", 0),
            "disabled_runtime_count": state_counts.get("disabled_runtime", 0),
            "runtime_execution_features": ((1 + int(any((capability.get('id') == 'aura_local_model_bridge_runtime' and capability.get('state') == 'online' and (capability.get('runtime_level') == 'permission_gated_alpha_runtime') for capability in self.capability_catalog()))) + int(any((capability.get('id') == 'aura_interactive_control_center_chat_runtime' and capability.get('state') == 'online' and (capability.get('runtime_level') == 'permission_gated_alpha_runtime') for capability in self.capability_catalog()))) + int(any((capability.get('id') == 'aura_permission_audit_recovery_visibility_runtime' and capability.get('state') == 'online' and (capability.get('runtime_level') == 'permission_gated_alpha_runtime') for capability in self.capability_catalog()))) + int(any(capability.get('id') == 'manual_start_stop_status_runtime' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'restart_logs_failure_visibility' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'process_ownership_service_state_persistence' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'reviewed_optional_autostart' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'persistent_local_chat_session_activation' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'local_model_service_discovery_health' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'local_model_router_activation' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'model_loading_unloading_queue_resource_budgets' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get('id') == 'active_local_runtime_integration_stabilization' and capability.get('state') == 'online' and capability.get('runtime_level') == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get("id") == 'operational_browser_chat_model_handoff' and capability.get("state") == "online" and capability.get("runtime_level") == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get("id") == 'session_list_resume_rename_archive_restore' and capability.get("state") == "online" and capability.get("runtime_level") == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get("id") == 'chat_history_recovery_ux' and capability.get("state") == "online" and capability.get("runtime_level") == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())) + int(any(capability.get("id") == 'review_first_memory_integration' and capability.get("state") == "online" and capability.get("runtime_level") == 'permission_gated_alpha_runtime' for capability in self.capability_catalog())))),
            "state_counts": state_counts,
            "risk_counts": risk_counts,
            "permission_counts": permission_counts,
        }

    def capabilities_by_state(self, state: str) -> list[dict[str, Any]]:
        return [item for item in self.capability_catalog() if item["state"] == state]

    def capabilities_requiring_permission(self) -> list[dict[str, Any]]:
        return [
            item for item in self.capability_catalog()
            if item["permission_required"] not in {"none", "read_project"}
        ]

    def control_center_catalog(self) -> list[dict[str, Any]]:
        return [
            {
                "id": item["id"],
                "name": item["name"],
                "state": item["state"],
                "runtime_level": item["runtime_level"],
                "risk_level": item["risk_level"],
                "permission_required": item["permission_required"],
                "category": item["category"],
                "visible": item["control_center_visible"],
            }
            for item in self.capability_catalog()
            if item["control_center_visible"]
        ]

    def normalize_text(self, text: Any) -> str:
        return " ".join(str(text or "").strip().split())

    def base_plan(self, plan_type: str, target: str) -> dict[str, Any]:
        normalized_target = self.normalize_text(target) or "AURA capability registry"
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": "planned",
            "plan_type": plan_type,
            "target": normalized_target,
            "principle": "know_capabilities_before_runtime_actions",
            "registry_plan_types": self.registry_plan_types(),
            "capability_summary": self.capability_summary(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def capability_catalog_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("capability_catalog_plan", target)
        plan["catalog_steps"] = [
            "List currently online, foundation-only, planner-only, permission-gated, review-only, planned, and disabled runtime capabilities.",
            "Assign risk level to each capability.",
            "Assign required permission category to each capability.",
            "Expose display-safe capability data for the future Control Center.",
        ]
        return plan

    def capability_state_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("capability_state_review_plan", target)
        plan["state_review_steps"] = [
            "Confirm online capabilities do not imply runtime execution.",
            "Keep foundation-only systems separate from runtime-ready systems.",
            "Keep planner-only systems separate from action execution.",
            "Keep disabled runtime capabilities visible as deferred and locked.",
        ]
        return plan

    def permission_requirement_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("permission_requirement_review_plan", target)
        plan["permission_review_steps"] = [
            "Map every risky capability to a permission category.",
            "Use user confirmation for future service, launcher, UI, and permission workflow actions.",
            "Keep microphone, camera, screen, file, command, download, internet, desktop, and git permissions explicit.",
            "Do not grant permission from the registry itself.",
        ]
        return plan

    def risk_level_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("risk_level_review_plan", target)
        plan["risk_review_steps"] = [
            "Mark display-only and planning features as low risk.",
            "Mark intent, UI, launcher, and monitoring foundations as medium risk.",
            "Mark microphone, camera, visual context, dependency/download, service, and permission workflow as high risk.",
            "Mark file write and command execution runtime as critical and deferred.",
        ]
        return plan

    def control_center_capability_view_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("control_center_capability_view_plan", target)
        plan["control_center_cards"] = [
            "Capability name",
            "Current state",
            "Runtime level",
            "Risk level",
            "Permission required",
            "Introduced version",
            "Category",
        ]
        plan["control_center_rule"] = "Control Center may display capability status, but must not enable capabilities without explicit permission workflow."
        return plan

    def capability_gap_review_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("capability_gap_review_plan", target)
        plan["gap_review_steps"] = [
            "Identify planned 83-90 operational control foundations.",
            "Keep controlled file write and command execution runtime deferred to 91-100.",
            "Keep voice and vision runtime adapters deferred until service, permission, launcher, and console foundations are stable.",
            "Use registry visibility to prevent confusing planned features with active runtime features.",
        ]
        return plan

    def capability_registry_migration_plan(self, target: str) -> dict[str, Any]:
        plan = self.base_plan("capability_registry_migration_plan", target)
        plan["migration_steps"] = [
            "Introduce capability registry as read-only metadata first.",
            "Expose registry through skill, plugin, CLI, shell, and system status.",
            "Use registry data in future launcher and Control Center views.",
            "Do not migrate permission decisions into this registry; keep permission workflow separate.",
        ]
        return plan

    def context(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "registry_plan_types": self.registry_plan_types(),
            "capability_states": self.capability_states(),
            "risk_levels": self.risk_levels(),
            "permission_categories": self.permission_categories(),
            "capability_summary": self.capability_summary(),
            "capability_catalog": self.capability_catalog(),
            "control_center_catalog": self.control_center_catalog(),
            "safe_current_capabilities": self.safe_current_capabilities(),
            "disabled_capabilities": self.disabled_capabilities(),
            **boundary,
        }

    def status(self) -> dict[str, Any]:
        boundary = self.safety_boundary()
        summary = self.capability_summary()
        return {
            "name": self.name,
            "version": self.version,
            "status": self.status_name,
            "registry_ready": True,
            "planner_ready": True,
            "control_center_data_ready": True,
            "capability_catalog_plan_ready": True,
            "capability_state_review_plan_ready": True,
            "permission_requirement_review_plan_ready": True,
            "risk_level_review_plan_ready": True,
            "control_center_capability_view_plan_ready": True,
            "capability_gap_review_plan_ready": True,
            "capability_registry_migration_plan_ready": True,
            "context_ready": True,
            "registry_plan_types": self.registry_plan_types(),
            "plan_type_count": len(self.registry_plan_types()),
            **summary,
            **boundary,
        }
