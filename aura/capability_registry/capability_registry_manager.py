
"""Capability Registry Consolidation for AURA.

Central planner-only registry describing what AURA can do, what is only a
foundation, what is planner-only, what requires permission, what is only a
review/checkpoint layer, and what is still planned for the future.

This registry prepares data for CLI, shell, service monitor, launcher, and
future AURA Control Center views without enabling runtime behavior, file
operations, command execution, tool execution, network action, UI runtime,
service runtime, or external actions.
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
            "Prepare capability data for future AURA Control Center views.",
            "Keep the registry planner-only, metadata-only, and side-effect-free.",
        ]

    def disabled_capabilities(self) -> list[str]:
        return [
            "runtime_behavior_change",
            "automatic_capability_enablement",
            "dynamic_runtime_discovery",
            "runtime_action_activation",
            "permission_grant_runtime",
            "ui_runtime",
            "web_server_runtime",
            "chat_runtime",
            "service_runtime",
            "launcher_runtime",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "command_execution",
            "test_execution",
            "code_execution",
            "dependency_install",
            "package_download",
            "internet_search",
            "network_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]

    def safety_boundary(self) -> dict[str, bool]:
        return {
            "registry_only": True,
            "planner_only": True,
            "proposal_only": True,
            "metadata_only": True,
            "control_center_data_ready": True,
            "runtime_ready": False,
            "execution_ready": False,
            "executed": False,
            "runtime_behavior_change": False,
            "automatic_capability_enablement": False,
            "dynamic_runtime_discovery": False,
            "runtime_action_activation": False,
            "permission_grant_runtime": False,
            "ui_runtime": False,
            "web_server_runtime": False,
            "chat_runtime": False,
            "service_runtime": False,
            "launcher_runtime": False,
            "file_read": False,
            "file_write": False,
            "file_modify": False,
            "file_delete": False,
            "command_execution": False,
            "test_execution": False,
            "code_execution": False,
            "dependency_install": False,
            "package_download": False,
            "internet_search": False,
            "network_action": False,
            "tool_execution": False,
            "real_tool_execution": False,
            "external_action_execution": False,
            "memory_write": False,
            "desktop_control": False,
            "git_init": False,
            "git_add": False,
            "git_commit": False,
            "git_push": False,
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
            "runtime_execution_features": 0,
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
