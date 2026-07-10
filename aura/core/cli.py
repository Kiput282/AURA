import argparse
from pathlib import Path
from typing import Any

import yaml

from aura.core.chat import AuraChat
from aura.core_loop.core_loop_manager import CoreLoopManager
from aura.model_router.model_router import ModelRouter
from aura.partner.partner_alpha_manager import PartnerAlphaManager
from aura.tool_sandbox.tool_sandbox_manager import ToolSandboxManager
from aura.desktop.desktop_manager import DesktopBridgeManager
from aura.desktop.desktop_assistant_alpha_manager import DesktopAssistantAlphaManager
from aura.actions.action_request_manager import ActionRequestManager
from aura.avatar.avatar_manager import AvatarManager
from aura.avatar.avatar_runtime_alpha_manager import AvatarRuntimeAlphaManager
from aura.blender.blender_bridge_foundation_manager import BlenderBridgeFoundationManager
from aura.media.media_understanding_foundation_manager import MediaUnderstandingFoundationManager
from aura.expression.expression_language_manager import ExpressionLanguageManager
from aura.game.game_companion_foundation_manager import GameCompanionFoundationManager
from aura.streaming.streaming_safety_foundation_manager import StreamingSafetyFoundationManager
from aura.core.shell import AuraShell
from aura.memory.memory_item import MemoryItem
from aura.memory.memory_store import MemoryStore
from aura.journal.project_journal import ProjectJournal
from aura.context.context_manager import ContextManager
from aura.permissions.permission_manager import PermissionManager
from aura.skills.builtin_skills import build_builtin_skill_registry
from aura.plugins.builtin.plugin_actions import build_builtin_plugin_action_registry
from aura.plugins.builtin.project_plugin import ProjectPlugin
from aura.project_coding.project_coding_manager import ProjectCodingManager
from aura.project_intent.project_intent_planner_manager import ProjectIntentPlannerManager
from aura.creative.creative_assistant_foundation_manager import CreativeAssistantFoundationManager
from aura.local_task.local_task_planner_alpha_manager import LocalTaskPlannerAlphaManager
from aura.file_ops.safe_file_operation_planner_manager import SafeFileOperationPlannerManager
from aura.reflection.memory_reflection_manager import MemoryReflectionManager
from aura.voice.voice_manager import VoiceManager
from aura.voice.voice_runtime_planner import VoiceRuntimePlanner
from aura.voice.voice_runtime_alpha_manager import VoiceRuntimeAlphaManager
from aura.workspace.workspace_awareness_manager import WorkspaceAwarenessManager
from aura.workspace_memory.workspace_memory_link_manager import WorkspaceMemoryLinkManager
from aura.awakening.awakening_manager import AwakeningManager
from aura.briefing.daily_briefing_manager import DailyBriefingManager
from aura.vision.vision_manager import VisionManager
from aura.vision.vision_runtime_planner import VisionRuntimePlanner
from aura.vision.vision_runtime_alpha_manager import VisionRuntimeAlphaManager
from aura.status.system_status_manager import SystemStatusManager
from aura.roles.builtin_roles import build_builtin_role_registry
from aura.utils.logger import disable_logging
from aura.codebase_change.codebase_change_planner_manager import CodebaseChangePlannerManager
from aura.codebase_validation_gate.codebase_validation_gate_planner_manager import CodebaseValidationGatePlannerManager
from aura.voice_conversation.voice_conversation_planner_manager import VoiceConversationPlannerManager
from aura.vision_context.vision_context_planner_manager import VisionContextPlannerManager
from aura.avatar_interaction.avatar_interaction_planner_manager import AvatarInteractionPlannerManager
from aura.desktop_workflow.desktop_workflow_planner_manager import DesktopWorkflowPlannerManager
from aura.partner_runtime.partner_runtime_planning_manager import PartnerRuntimePlanningManager
from aura.thought_loop.thought_loop_planner_manager import ThoughtLoopPlannerManager
from aura.reasoning_context.reasoning_context_manager import ReasoningContextManager
from aura.knowledge_uncertainty.knowledge_uncertainty_gate_manager import KnowledgeUncertaintyGateManager
from aura.voice_input.voice_input_runtime_foundation_manager import VoiceInputRuntimeFoundationManager
from aura.voice_intent.voice_intent_understanding_manager import VoiceIntentUnderstandingManager
from aura.vision_input.vision_input_runtime_foundation_manager import VisionInputRuntimeFoundationManager
from aura.visual_context.visual_context_understanding_manager import VisualContextUnderstandingManager
from aura.coder_project.coder_project_generation_planner_manager import CoderProjectGenerationPlannerManager
from aura.dependency_permission.dependency_download_permission_gate_manager import DependencyDownloadPermissionGateManager
from aura.checkpoint_80.review_stabilization_71_80_manager import ReviewStabilization7180Manager
from aura.output_formatter.shared_output_formatter_manager import SharedOutputFormatterManager
from aura.capability_registry.capability_registry_manager import CapabilityRegistryManager
from aura.permission_workflow.unified_permission_workflow_manager import UnifiedPermissionWorkflowManager
from aura.runtime_service.aura_runtime_service_foundation_manager import AuraRuntimeServiceFoundationManager
from aura.launcher_monitor.aura_launcher_health_monitor_foundation_manager import AuraLauncherHealthMonitorFoundationManager
from aura.control_center.aura_control_center_ui_blueprint_manager import AuraControlCenterUIBlueprintManager
from aura.local_console_web.aura_local_console_web_foundation_manager import AuraLocalConsoleWebFoundationManager
from aura.chat_bridge.aura_chat_bridge_session_state_foundation_manager import AuraChatBridgeSessionStateFoundationManager
from aura.plugin_permission_dashboard.aura_plugin_permission_dashboard_foundation_manager import AuraPluginPermissionDashboardFoundationManager
from aura.local_console_static_prototype.aura_local_console_static_prototype_foundation_manager import AuraLocalConsoleStaticPrototypeFoundationManager
from aura.local_console_api_schema.aura_local_console_api_schema_foundation_manager import AuraLocalConsoleAPISchemaFoundationManager
from aura.control_center_data_aggregator.aura_control_center_data_aggregator_foundation_manager import AuraControlCenterDataAggregatorFoundationManager
from aura.permission_request_review_queue.aura_permission_request_review_queue_foundation_manager import AuraPermissionRequestReviewQueueFoundationManager
from aura.chat_session_persistence_planner.aura_chat_session_persistence_planner_foundation_manager import AuraChatSessionPersistencePlannerFoundationManager
from aura.safe_local_web_runtime_gate.aura_safe_local_web_runtime_gate_foundation_manager import AuraSafeLocalWebRuntimeGateFoundationManager
from aura.controlled_file_write_approval_draft.aura_controlled_file_write_approval_draft_foundation_manager import AuraControlledFileWriteApprovalDraftFoundationManager
from aura.runtime_action_queue_review_layer.aura_runtime_action_queue_review_layer_foundation_manager import AuraRuntimeActionQueueReviewLayerFoundationManager
from aura.pre_runtime_security_audit.aura_pre_runtime_security_audit_foundation_manager import AuraPreRuntimeSecurityAuditFoundationManager
from aura.sprint_100_review_stabilization.aura_sprint_100_review_stabilization_foundation_manager import AuraSprint100ReviewStabilizationFoundationManager
from aura.genesis_runtime_readiness_baseline.aura_genesis_runtime_readiness_baseline_foundation_manager import AuraGenesisRuntimeReadinessBaselineFoundationManager
from aura.safe_runtime_configuration_profile.aura_safe_runtime_configuration_profile_foundation_manager import AuraSafeRuntimeConfigurationProfileFoundationManager
from aura.local_service_start_proposal_review.aura_local_service_start_proposal_review_foundation_manager import AuraLocalServiceStartProposalReviewFoundationManager
from aura.dashboard_api_contract_consolidation.aura_dashboard_api_contract_consolidation_foundation_manager import AuraDashboardApiContractConsolidationFoundationManager
from aura.permission_decision_runtime_dry_run.aura_permission_decision_runtime_dry_run_foundation_manager import AuraPermissionDecisionRuntimeDryRunFoundationManager
from aura.runtime_action_execution_preview_packet.aura_runtime_action_execution_preview_packet_foundation_manager import AuraRuntimeActionExecutionPreviewPacketFoundationManager
from aura.local_runtime_execution_gate_dry_run.aura_local_runtime_execution_gate_dry_run_foundation_manager import AuraLocalRuntimeExecutionGateDryRunFoundationManager
from aura.runtime_audit_event_packet_preview.aura_runtime_audit_event_packet_preview_foundation_manager import AuraRuntimeAuditEventPacketPreviewFoundationManager
from aura.runtime_safety_freeze_manual_approval_barrier.aura_runtime_safety_freeze_manual_approval_barrier_foundation_manager import AuraRuntimeSafetyFreezeManualApprovalBarrierFoundationManager
from aura.review_stabilization_101_110.aura_review_stabilization_101_110_foundation_manager import AuraReviewStabilization101110FoundationManager
from aura.genesis_runtime_readiness_next_block_planning.aura_genesis_runtime_readiness_next_block_planning_foundation_manager import AuraGenesisRuntimeReadinessNextBlockPlanningFoundationManager
from aura.runtime_permission_flow_consolidation.aura_runtime_permission_flow_consolidation_foundation_manager import AuraRuntimePermissionFlowConsolidationFoundationManager
from aura.audit_event_review_queue.aura_audit_event_review_queue_foundation_manager import AuraAuditEventReviewQueueFoundationManager
from aura.dashboard_runtime_readiness_view_model.aura_dashboard_runtime_readiness_view_model_foundation_manager import AuraDashboardRuntimeReadinessViewModelFoundationManager
from aura.safe_local_action_contract_review.aura_safe_local_action_contract_review_foundation_manager import AuraSafeLocalActionContractReviewFoundationManager
from aura.orion_client_boundary_contract.aura_orion_client_boundary_contract_foundation_manager import AuraOrionClientBoundaryContractFoundationManager
from aura.runtime_error_rollback_preview.aura_runtime_error_rollback_preview_foundation_manager import AuraRuntimeErrorRollbackPreviewFoundationManager
from aura.manual_approval_decision_flow_review.aura_manual_approval_decision_flow_review_foundation_manager import AuraManualApprovalDecisionFlowReviewFoundationManager
from aura.v1_runtime_readiness_cutline_review.aura_v1_runtime_readiness_cutline_review_foundation_manager import AuraV1RuntimeReadinessCutlineReviewFoundationManager
from aura.review_stabilization_111_120.aura_review_stabilization_111_120_foundation_manager import AuraReviewStabilization111120FoundationManager
from aura.post_checkpoint_120_next_block_planning.aura_post_checkpoint_120_next_block_planning_foundation_manager import AuraPostCheckpoint120NextBlockPlanningFoundationManager
from aura.runtime_permission_audit_writer_boundary_review.aura_runtime_permission_audit_writer_boundary_review_foundation_manager import AuraRuntimePermissionAuditWriterBoundaryReviewFoundationManager
from aura.dashboard_control_center_boundary_review.aura_dashboard_control_center_boundary_review_foundation_manager import AuraDashboardControlCenterBoundaryReviewFoundationManager
from aura.orion_dry_handshake_boundary_review.aura_orion_dry_handshake_boundary_review_foundation_manager import AuraOrionDryHandshakeBoundaryReviewFoundationManager
from aura.safe_local_action_allowlist_boundary_review.aura_safe_local_action_allowlist_boundary_review_foundation_manager import AuraSafeLocalActionAllowlistBoundaryReviewFoundationManager
from aura.runtime_grant_expiry_boundary_review.aura_runtime_grant_expiry_boundary_review_foundation_manager import AuraRuntimeGrantExpiryBoundaryReviewFoundationManager
from aura.runtime_recovery_drill_boundary_review.aura_runtime_recovery_drill_boundary_review_foundation_manager import AuraRuntimeRecoveryDrillBoundaryReviewFoundationManager
from aura.dashboard_runtime_readiness_boundary_review.aura_dashboard_runtime_readiness_boundary_review_foundation_manager import AuraDashboardRuntimeReadinessBoundaryReviewFoundationManager
from aura.runtime_activation_blocker_register_boundary_review.aura_runtime_activation_blocker_register_boundary_review_foundation_manager import AuraRuntimeActivationBlockerRegisterBoundaryReviewFoundationManager
from aura.review_stabilization_121_130.aura_review_stabilization_121_130_foundation_manager import AuraReviewStabilization121130FoundationManager
from aura.post_checkpoint_130_next_block_foundation.aura_post_checkpoint_130_next_block_foundation_manager import AuraPostCheckpoint130NextBlockFoundationManager
from aura.final_genesis_acceptance_criteria_foundation.aura_final_genesis_acceptance_criteria_foundation_manager import AuraFinalGenesisAcceptanceCriteriaFoundationManager
from aura.runtime_activation_path_proposal_review.aura_runtime_activation_path_proposal_review_foundation_manager import AuraRuntimeActivationPathProposalReviewFoundationManager
from aura.local_service_boot_plan_review.aura_local_service_boot_plan_review_foundation_manager import AuraLocalServiceBootPlanReviewFoundationManager
from aura.control_center_runtime_entry_review.aura_control_center_runtime_entry_review_foundation_manager import AuraControlCenterRuntimeEntryReviewFoundationManager
from aura.chat_runtime_minimal_loop_review.aura_chat_runtime_minimal_loop_review_foundation_manager import AuraChatRuntimeMinimalLoopReviewFoundationManager
from aura.memory_runtime_write_gate_review.aura_memory_runtime_write_gate_review_foundation_manager import AuraMemoryRuntimeWriteGateReviewFoundationManager
from aura.permission_runtime_grant_gate_review.aura_permission_runtime_grant_gate_review_foundation_manager import AuraPermissionRuntimeGrantGateReviewFoundationManager
from aura.audit_runtime_writer_activation_review.aura_audit_runtime_writer_activation_review_foundation_manager import AuraAuditRuntimeWriterActivationReviewFoundationManager
from aura.review_stabilization_131_140.aura_review_stabilization_131_140_foundation_manager import AuraReviewStabilization131140FoundationManager
from aura.local_service_runtime_foundation.aura_local_service_runtime_foundation_manager import AuraLocalServiceRuntimeFoundationManager
from aura.local_service_safe_idle_boot_boundary.aura_local_service_safe_idle_boot_boundary_manager import AuraLocalServiceSafeIdleBootBoundaryManager
from aura.local_service_health_endpoint_foundation.aura_local_service_health_endpoint_foundation_manager import AuraLocalServiceHealthEndpointFoundationManager
from aura.local_service_configuration_port_registry_foundation.aura_local_service_configuration_port_registry_foundation_manager import AuraLocalServiceConfigurationPortRegistryFoundationManager
from aura.service_permission_gate_runtime_boundary.aura_service_permission_gate_runtime_boundary_manager import AuraServicePermissionGateRuntimeBoundaryManager
from aura.service_audit_link_foundation.aura_service_audit_link_foundation_manager import AuraServiceAuditLinkFoundationManager
from aura.service_control_command_review_foundation.aura_service_control_command_review_foundation_manager import AuraServiceControlCommandReviewFoundationManager
from aura.service_recovery_restart_policy_foundation.aura_service_recovery_restart_policy_foundation_manager import AuraServiceRecoveryRestartPolicyFoundationManager
from aura.service_security_localhost_binding_review.aura_service_security_localhost_binding_review_manager import AuraServiceSecurityLocalhostBindingReviewManager
from aura.service_review_stabilization_141_150.aura_service_review_stabilization_141_150_manager import AuraServiceReviewStabilization141150Manager
from aura.control_center_runtime_foundation.aura_control_center_runtime_foundation_manager import AuraControlCenterRuntimeFoundationManager
from aura.control_center_read_only_status_panel_foundation.aura_control_center_read_only_status_panel_foundation_manager import AuraControlCenterReadOnlyStatusPanelFoundationManager
from aura.control_center_capability_viewer_foundation.aura_control_center_capability_viewer_foundation_manager import AuraControlCenterCapabilityViewerFoundationManager
from aura.control_center_plugin_panel_foundation.aura_control_center_plugin_panel_foundation_manager import AuraControlCenterPluginPanelFoundationManager
from aura.control_center_permission_panel_foundation.aura_control_center_permission_panel_foundation_manager import AuraControlCenterPermissionPanelFoundationManager
from aura.control_center_audit_panel_foundation.aura_control_center_audit_panel_foundation_manager import AuraControlCenterAuditPanelFoundationManager
from aura.control_center_service_monitor_panel_foundation.aura_control_center_service_monitor_panel_foundation_manager import AuraControlCenterServiceMonitorPanelFoundationManager
from aura.control_center_action_log_panel_foundation.aura_control_center_action_log_panel_foundation_manager import AuraControlCenterActionLogPanelFoundationManager
from aura.control_center_read_only_route_map_foundation.aura_control_center_read_only_route_map_foundation_manager import AuraControlCenterReadOnlyRouteMapFoundationManager
from aura.control_center_runtime_review_stabilization_151_160.aura_control_center_runtime_review_stabilization_151_160_manager import AuraControlCenterRuntimeReviewStabilization151160Manager
from aura.local_chat_runtime_foundation.aura_local_chat_runtime_foundation_manager import AuraLocalChatRuntimeFoundationManager
from aura.local_chat_cli_session_alpha.aura_local_chat_cli_session_alpha_manager import AuraLocalChatCliSessionAlphaManager
from aura.local_chat_message_store.aura_local_chat_message_store_manager import AuraLocalChatMessageStoreManager
from aura.local_chat_persona_response_layer.aura_local_chat_persona_response_layer_manager import AuraLocalChatPersonaResponseLayerManager
from aura.local_chat_model_adapter_boundary.aura_local_chat_model_adapter_boundary_manager import AuraLocalChatModelAdapterBoundaryManager
from aura.local_chat_permission_gated_model_request.aura_local_chat_permission_gated_model_request_manager import AuraLocalChatPermissionGatedModelRequestManager
from aura.local_chat_safety_uncertainty_layer.aura_local_chat_safety_uncertainty_layer_manager import AuraLocalChatSafetyUncertaintyLayerManager
from aura.local_chat_history_viewer_contract.aura_local_chat_history_viewer_contract_manager import AuraLocalChatHistoryViewerContractManager
from aura.local_chat_integration_review.aura_local_chat_integration_review_manager import AuraLocalChatIntegrationReviewManager
from aura.local_chat_runtime_stabilization.aura_local_chat_runtime_stabilization_manager import AuraLocalChatRuntimeStabilizationManager
from aura.memory_runtime_foundation.aura_memory_runtime_foundation_manager import AuraMemoryRuntimeFoundationManager
from aura.memory_runtime_stabilization.aura_memory_runtime_stabilization_manager import AuraMemoryRuntimeStabilizationManager
from aura.memory_runtime_integration_review.aura_memory_runtime_integration_review_manager import AuraMemoryRuntimeIntegrationReviewManager
from aura.memory_privacy_redaction_layer.aura_memory_privacy_redaction_layer_manager import AuraMemoryPrivacyRedactionLayerManager
from aura.chat_to_memory_handoff_contract.aura_chat_to_memory_handoff_contract_manager import AuraChatToMemoryHandoffContractManager
from aura.memory_correction_deletion_boundary.aura_memory_correction_deletion_boundary_manager import AuraMemoryCorrectionDeletionBoundaryManager
from aura.memory_review_queue.aura_memory_review_queue_manager import AuraMemoryReviewQueueManager
from aura.memory_importance_pinning_policy.aura_memory_importance_pinning_policy_manager import AuraMemoryImportancePinningPolicyManager
from aura.memory_extraction_dry_run.aura_memory_extraction_dry_run_manager import AuraMemoryExtractionDryRunManager
from aura.memory_write_permission_gate.aura_memory_write_permission_gate_manager import AuraMemoryWritePermissionGateManager
from aura.codebase_patch_proposal.codebase_patch_proposal_renderer_manager import CodebasePatchProposalRendererManager
from aura.local_web_runtime_alpha.aura_local_web_runtime_cli import handle_local_web_runtime_command
from aura.service_lifecycle_runtime.aura_service_lifecycle_runtime_cli import handle_service_lifecycle_command
from aura.health_status_api_runtime.aura_health_status_api_runtime_cli import handle_health_status_api_command
from aura.control_center_backend_runtime.aura_control_center_backend_runtime_cli import handle_control_center_backend_command
from aura.control_center_web_shell_runtime.aura_control_center_web_shell_runtime_cli import handle_control_center_web_shell_command
from aura.browser_chat_session_runtime.aura_browser_chat_session_runtime_cli import handle_browser_chat_session_command
from aura.local_model_bridge_runtime.aura_local_model_bridge_runtime_cli import handle_local_model_bridge_command
from aura.interactive_control_center_chat_runtime.aura_interactive_control_center_chat_runtime_cli import handle_interactive_chat_command
from aura.permission_audit_recovery_visibility_runtime.aura_permission_audit_recovery_visibility_runtime_cli import handle_permission_audit_recovery_command
from aura.local_interaction_runtime_stabilization.aura_local_interaction_runtime_stabilization_cli import handle_local_interaction_runtime_stabilization_command


class AuraCLI:
    """
    Simple command-line interface for AURA.

    Supported commands:
    - remember
    - recall
    - chat
    - history
    - provider
    - provider-check
    - reason
    - reason-check
    - shell
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.settings_path = self.project_root / "aura" / "config" / "settings.yaml"

    def get_memory_store(self) -> MemoryStore:
        return MemoryStore(project_root=self.project_root)

    def load_settings(self) -> dict:
        if not self.settings_path.exists():
            return {}

        with self.settings_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def configured_provider_name(self) -> str:
        settings = self.load_settings()
        reasoning = settings.get("reasoning", {})
        return reasoning.get("provider", "unknown")

    def print_provider_runtime_check(self, runtime: dict[str, Any]) -> None:
        print("AURA Provider Runtime Check")
        print("===========================")
        print(f"Provider : {runtime.get('provider', 'unknown')} v{runtime.get('version', 'unknown')}")
        print(f"Config   : {self.configured_provider_name()}")
        print(f"Status   : {runtime.get('status', 'UNKNOWN')}")
        print(f"Message  : {runtime.get('message', '-')}")

        if "host" in runtime:
            print(f"Host     : {runtime.get('host')}")

        if "model" in runtime:
            print(f"Model    : {runtime.get('model')}")

        available_models = runtime.get("available_models", [])
        if available_models:
            print("Models   :")
            for model in available_models:
                print(f"- {model}")
        elif "available_models" in runtime:
            print("Models   : none")

    def remember(self, content: str) -> None:
        memory_store = self.get_memory_store()

        memory = MemoryItem(
            kind="user_note",
            content=content,
            metadata={
                "source": "AuraCLI",
            },
        )

        memory_store.save(memory)

        print("Memory saved.")
        print(f"Content: {content}")

    def recall(self, limit: int = 5) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_recent(limit=limit)

        print("AURA Memory Recall")
        print("==================")

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def chat(self, message: str) -> None:
        chat = AuraChat(project_root=self.project_root)
        response = chat.respond(message, source="AuraCLI")
        print(response)

    def history(self, limit: int = 5) -> None:
        chat = AuraChat(project_root=self.project_root)
        turns = chat.recent_conversations(limit=limit)

        print("AURA Chat History")
        print("=================")

        if not turns:
            print("No chat history found.")
            return

        for turn in turns:
            print(f"User: {turn.user_message}")
            print(f"AURA: {turn.aura_response}")
            print("---")

    def provider(self) -> None:
        chat = AuraChat(project_root=self.project_root)
        provider = chat.provider_info()
        configured_provider = self.configured_provider_name()

        print("AURA Reasoning Provider")
        print("=======================")
        print(f"Name    : {provider['name']}")
        print(f"Version : {provider['version']}")
        print(f"Config  : {configured_provider}")

    def provider_check(self) -> None:
        chat = AuraChat(project_root=self.project_root)
        runtime = chat.provider_runtime_check()
        self.print_provider_runtime_check(runtime)

    def memory_count(self) -> None:
        memory_store = self.get_memory_store()
        count = memory_store.count()

        print("AURA Memory Count")
        print("=================")
        print(f"Records: {count}")

    def memory_list(self, limit: int = 5) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_recent(limit=limit)

        print("AURA Memory List")
        print("================")
        print(f"Limit: {limit}")
        print()

        if not memories:
            print("No memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def memory_delete(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.find_by_id(memory_id=memory_id)

        print("AURA Memory Delete")
        print("==================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        if memory_store.is_protected(memory):
            print("Cannot delete protected system memory.")
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")
            return

        deleted_memory = memory_store.delete_by_id(memory_id=memory_id)

        if deleted_memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Deleted memory:")
        print(f"- ID: {deleted_memory.id}")
        print(f"  Kind: {deleted_memory.kind}")
        print(f"  Content: {deleted_memory.content}")

    def memory_search(self, query: str, limit: int = 5) -> None:
        chat = AuraChat(project_root=self.project_root)
        memories = chat.relevant_memories(message=query, limit=limit)

        print("AURA Relevant Memories")
        print("======================")
        print(f"Query: {query}")
        print()

        if not memories:
            print("No relevant memories found.")
            return

        for memory in memories:
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")

    def get_project_journal(self) -> ProjectJournal:
        return ProjectJournal(project_root=self.project_root)

    def journal(self, limit: int = 5) -> None:
        project_journal = self.get_project_journal()
        entries = project_journal.list_recent(limit=limit)

        print("AURA Project Journal")
        print("====================")
        print(f"Limit: {limit}")
        print()

        if not entries:
            print("No journal entries found.")
            return

        for entry in entries:
            print(f"- ID: {entry.id}")
            print(f"  Title: {entry.title}")
            print(f"  Content: {entry.content}")
            print(f"  Created At: {entry.created_at}")

    def journal_add(self, content: str) -> None:
        project_journal = self.get_project_journal()

        title = "Manual Entry"
        if ":" in content:
            title = content.split(":", 1)[0].strip() or "Manual Entry"

        entry = project_journal.add(
            title=title,
            content=content,
            metadata={"source": "cli"},
        )

        print("AURA Project Journal")
        print("====================")
        print("Journal entry saved.")
        print(f"- ID: {entry.id}")
        print(f"  Title: {entry.title}")
        print(f"  Content: {entry.content}")

    def journal_count(self) -> None:
        project_journal = self.get_project_journal()

        print("AURA Project Journal Count")
        print("==========================")
        print(f"Entries: {project_journal.count()}")

    def roles(self) -> None:
        registry = build_builtin_role_registry()
        roles = registry.list_roles()

        print("AURA Roles")
        print("==========")
        print(f"Total: {registry.count()}")
        print()

        for role in roles:
            print(f"- {role.name}")
            print(f"  Status      : {role.status}")
            print(f"  Provider    : {role.provider}")
            print(f"  Model       : {role.model}")
            print(f"  Description : {role.description}")

            if role.capabilities:
                print("  Capabilities:")
                for capability in role.capabilities:
                    print(f"  - {capability}")

            print()

    def memory_pin(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.set_pinned(memory_id=memory_id, pinned=True)

        print("AURA Memory Pin")
        print("===============")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory pinned.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_unpin(self, memory_id: str) -> None:
        memory_store = self.get_memory_store()
        memory = memory_store.set_pinned(memory_id=memory_id, pinned=False)

        print("AURA Memory Unpin")
        print("=================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory unpinned.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_importance(self, memory_id: str, importance: int) -> None:
        memory_store = self.get_memory_store()

        print("AURA Memory Importance")
        print("======================")

        try:
            memory = memory_store.set_importance(
                memory_id=memory_id,
                importance=importance,
            )
        except ValueError as error:
            print(str(error))
            return

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Memory importance updated.")
        print(f"- ID: {memory.id}")
        print(f"  Kind: {memory.kind}")
        print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
        print(f"  Importance: {memory.metadata.get('importance', 3)}")
        print(f"  Content: {memory.content}")

    def memory_pinned(self) -> None:
        memory_store = self.get_memory_store()
        memories = memory_store.list_pinned()

        print("AURA Pinned Memories")
        print("====================")

        if not memories:
            print("No pinned memories found.")
            return

        for memory in memories:
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {bool(memory.metadata.get('pinned', False))}")
            print(f"  Importance: {memory.metadata.get('importance', 3)}")
            print(f"  Content: {memory.content}")

    def context(self, message: str) -> None:
        context_manager = ContextManager(project_root=self.project_root)
        packet = context_manager.build(user_message=message)

        print(packet.to_text())

    def permissions(self) -> None:
        permission_manager = PermissionManager()

        print("AURA Permissions")
        print("================")

        for result in permission_manager.list_permissions():
            print(f"- {result.action}")
            print(f"  Level       : {int(result.level)} - {result.level.label}")
            print(f"  Allowed     : {result.allowed}")
            print(f"  Confirmation: {result.requires_confirmation}")
            print(f"  Description : {result.description}")
            print(f"  Reason      : {result.reason}")
            print()

    def permission_check(self, action: str) -> None:
        permission_manager = PermissionManager()
        result = permission_manager.check(action=action)

        print("AURA Permission Check")
        print("=====================")
        print(f"Action      : {result.action}")
        print(f"Level       : {int(result.level)} - {result.level.label}")
        print(f"Allowed     : {result.allowed}")
        print(f"Confirmation: {result.requires_confirmation}")
        print(f"Description : {result.description}")
        print(f"Reason      : {result.reason}")

    def skills(self) -> None:
        registry = build_builtin_skill_registry()

        print("AURA Skills")
        print("===========")
        print(f"Total: {registry.count()}")
        print()

        for skill in registry.list_skills():
            permission = registry.check_permission(skill)

            print(f"- {skill.name}")
            print(f"  Status      : {skill.status}")
            print(f"  Role        : {skill.role}")
            print(f"  Permission  : {skill.permission_action}")
            print(f"  Allowed     : {permission.allowed}")
            print(f"  Confirmation: {permission.requires_confirmation}")
            print(f"  Description : {skill.description}")

            if skill.capabilities:
                print("  Capabilities:")
                for capability in skill.capabilities:
                    print(f"  - {capability}")

            print()

    def skill_detail(self, name: str) -> None:
        registry = build_builtin_skill_registry()
        skill = registry.get(name=name)

        print("AURA Skill")
        print("==========")

        if skill is None:
            print(f"Skill not found: {name}")
            return

        permission = registry.check_permission(skill)

        print(f"Name        : {skill.name}")
        print(f"Status      : {skill.status}")
        print(f"Role        : {skill.role}")
        print(f"Permission  : {skill.permission_action}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Description : {skill.description}")

        if skill.capabilities:
            print("Capabilities:")
            for capability in skill.capabilities:
                print(f"- {capability}")

    def skill_check(self, name: str) -> None:
        registry = build_builtin_skill_registry()
        skill = registry.get(name=name)

        print("AURA Skill Check")
        print("================")

        if skill is None:
            print(f"Skill not found: {name}")
            return

        permission = registry.check_permission(skill)

        print(f"Skill       : {skill.name}")
        print(f"Status      : {skill.status}")
        print(f"Role        : {skill.role}")
        print(f"Permission  : {skill.permission_action}")
        print(f"Level       : {int(permission.level)} - {permission.level.label}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Reason      : {permission.reason}")

    def action_request(self, action: str) -> None:
        manager = ActionRequestManager()
        request = manager.build(action_name=action)

        print("AURA Action Request")
        print("===================")
        print(f"Requested Action   : {request.requested_action}")
        print(f"Resolved Action    : {request.resolved_action}")
        print(f"Request State      : {request.request_state}")
        print(f"Plugin Action Found: {request.plugin_action_found}")
        print(f"Plugin             : {request.plugin or '-'}")
        print(f"Skill              : {request.skill or '-'}")
        print(f"Plugin Status      : {request.plugin_action_status}")
        print(f"Permission Action  : {request.permission_action}")
        print(f"Permission Level   : {request.permission_level} - {request.permission_level_label}")
        print(f"Allowed            : {request.allowed}")
        print(f"Confirmation       : {request.requires_confirmation}")
        print(f"Description        : {request.description}")
        print(f"Reason             : {request.reason}")
        print(f"Note               : {request.note}")

    def plugin_actions(self) -> None:
        registry = build_builtin_plugin_action_registry()

        print("AURA Plugin Actions")
        print("===================")
        print(f"Total: {registry.count()}")
        print()

        for action in registry.list_actions():
            permission = registry.check_permission(action)

            print(f"- {action.name}")
            print(f"  Plugin      : {action.plugin}")
            print(f"  Status      : {action.status}")
            print(f"  Skill       : {action.skill}")
            print(f"  Permission  : {action.permission_action}")
            print(f"  Allowed     : {permission.allowed}")
            print(f"  Confirmation: {permission.requires_confirmation}")
            print(f"  Description : {action.description}")
            print()

    def plugin_action_detail(self, name: str) -> None:
        registry = build_builtin_plugin_action_registry()
        action = registry.get(name=name)

        print("AURA Plugin Action")
        print("==================")

        if action is None:
            print(f"Plugin action not found: {name}")
            return

        permission = registry.check_permission(action)

        print(f"Name        : {action.name}")
        print(f"Plugin      : {action.plugin}")
        print(f"Status      : {action.status}")
        print(f"Skill       : {action.skill}")
        print(f"Permission  : {action.permission_action}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Description : {action.description}")

    def plugin_action_check(self, name: str) -> None:
        registry = build_builtin_plugin_action_registry()
        action = registry.get(name=name)

        print("AURA Plugin Action Check")
        print("========================")

        if action is None:
            print(f"Plugin action not found: {name}")
            return

        permission = registry.check_permission(action)

        print(f"Action      : {action.name}")
        print(f"Plugin      : {action.plugin}")
        print(f"Status      : {action.status}")
        print(f"Skill       : {action.skill}")
        print(f"Permission  : {action.permission_action}")
        print(f"Level       : {int(permission.level)} - {permission.level.label}")
        print(f"Allowed     : {permission.allowed}")
        print(f"Confirmation: {permission.requires_confirmation}")
        print(f"Reason      : {permission.reason}")

    def project_map(self, depth: int = 2, limit: int = 80) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        project_map = plugin.project_map(depth=depth, limit=limit)

        print("AURA Project Map")
        print("================")
        print(f"Project Root: {project_map['project_root']}")
        print(f"Depth       : {project_map['depth']}")
        print(f"Limit       : {project_map['limit']}")
        print(f"Directories : {project_map['directories']}")
        print(f"Files       : {project_map['files']}")
        print()
        print("Entries:")

        for entry in project_map["entries"]:
            marker = "[D]" if entry["type"] == "directory" else "[F]"
            print(f"- {marker} {entry['path']}")

    def project_inspect(self, relative_path: str) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        try:
            info = plugin.inspect_path(relative_path=relative_path)
        except Exception as error:
            print(f"Error: {error}")
            return

        print("AURA Project Inspect")
        print("====================")
        print(f"Path: {info['path']}")
        print(f"Type: {info['type']}")

        if info["type"] == "directory":
            print(f"Children Shown: {info['children_shown']}/{info['child_limit']}")
            print()
            print("Children:")

            for child in info["children"]:
                marker = "[D]" if child["type"] == "directory" else "[F]"
                print(f"- {marker} {child['path']}")

            return

        if info["type"] == "file":
            print(f"Suffix      : {info['suffix']}")
            print(f"Size Bytes  : {info['size_bytes']}")
            print(f"Safe To Read: {info['safe_to_read']}")
            print(f"Preview     : {info['preview_line_count']} line(s)")
            print()

            if info["preview_lines"]:
                print("Preview:")
                for index, line in enumerate(info["preview_lines"], start=1):
                    print(f"{index:03}: {line}")

            return

    def project_find(self, keyword: str, limit: int = 30) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        try:
            result = plugin.find_text(keyword=keyword, limit=limit)
        except Exception as error:
            print(f"Error: {error}")
            return

        print("AURA Project Find")
        print("=================")
        print(f"Keyword: {result['keyword']}")
        print(f"Limit  : {result['limit']}")
        print(f"Matches: {result['match_count']}")
        print()

        if not result["matches"]:
            print("No matches found.")
            return

        for match in result["matches"]:
            print(f"- {match['file']}:{match['line']}")
            print(f"  {match['text']}")

    def project_summary(self) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        summary = plugin.summary()

        print("AURA Project Summary")
        print("====================")
        print(f"Project Root  : {summary['project_root']}")
        print(f"Visible Files : {summary['visible_files']}")
        print(f"Python Files  : {summary['python_files']}")
        print(f"Markdown Files: {summary['markdown_files']}")
        print(f"YAML Files    : {summary['yaml_files']}")
        print()
        print("Top Files:")
        for file in summary["top_files"]:
            print(f"- {file}")

    def project_files(self, limit: int = 50) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)
        files = plugin.list_files(limit=limit)

        print("AURA Project Files")
        print("==================")
        print(f"Limit: {limit}")
        print()

        if not files:
            print("No visible project files found.")
            return

        for file in files:
            print(f"- {file}")

    def project_read(self, relative_path: str) -> None:
        plugin = ProjectPlugin(project_root=self.project_root)

        print("AURA Project Read")
        print("=================")
        print(f"File: {relative_path}")
        print()

        try:
            content = plugin.read_file(relative_path=relative_path)
        except Exception as error:
            print(f"Error: {error}")
            return

        print(content)

    def voice_runtime_status(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        status = planner.status()

        print("AURA Voice Runtime Status")
        print("=========================")
        print(f"Name                        : {status['name']}")
        print(f"Version                     : {status['version']}")
        print(f"Status                      : {status['status']}")
        print(f"Planning Ready              : {status['planning_ready']}")
        print(f"Activation Foundation Ready : {status['activation_foundation_ready']}")
        print(f"Listen State Foundation Ready: {status['listen_state_foundation_ready']}")
        print(f"Default Listen State        : {status['default_listen_state']}")
        print(f"Current Listen State        : {status['current_listen_state']}")
        print(f"Allowed Listen States       : {status['allowed_listen_states']}")
        print(f"Microphone Boundary Ready   : {status['microphone_boundary_ready']}")
        print(f"Mic Capture Runtime Ready   : {status['microphone_capture_runtime_ready']}")
        print(f"Microphone Capture Active   : {status['microphone_capture_active']}")
        print(f"Audio Device Access         : {status['audio_device_access']}")
        print(f"Audio Device Discovery      : {status['audio_device_discovery_active']}")
        print(f"Recording Active            : {status['recording_active']}")
        print(f"Audio Buffer Active         : {status['audio_buffer_active']}")
        print(f"STT Adapter Contract Ready  : {status['stt_adapter_contract_ready']}")
        print(f"STT Adapter Runtime Ready   : {status['stt_adapter_runtime_ready']}")
        print(f"STT Default Adapter         : {status['stt_default_adapter']}")
        print(f"STT Adapter Candidates      : {status['stt_adapter_candidates']}")
        print(f"Audio File STT Runtime Ready: {status['audio_file_transcription_runtime_ready']}")
        print(f"Live Mic Transcription      : {status['live_microphone_transcription_active']}")
        print(f"Transcription Active        : {status['transcription_active']}")
        print(f"Cloud STT Fallback          : {status['cloud_stt_fallback_enabled']}")
        print(f"Transcript To Action        : {status['transcript_to_action_enabled']}")
        print(f"Runtime Ready               : {status['runtime_ready']}")
        print(f"Safe Idle Default           : {status['safe_idle_default']}")
        print(f"Push To Talk Required       : {status['push_to_talk_required']}")
        print(f"Always Listening Enabled    : {status['always_listening_enabled']}")
        print(f"Hidden Capture Enabled      : {status['hidden_capture_enabled']}")
        print(f"Background Wake Word Enabled: {status['background_wake_word_enabled']}")
        print(f"Silent Cloud Fallback       : {status['silent_cloud_fallback_enabled']}")
        print(f"Direct Voice To Action      : {status['direct_voice_to_action_enabled']}")
        print(f"Chat Session Reuse Required : {status['chat_session_reuse_required']}")
        print(f"Microphone Access           : {status['microphone_access']}")
        print(f"Speaker Output              : {status['speaker_output']}")
        print(f"STT Runtime Ready           : {status['stt_runtime_ready']}")
        print(f"TTS Runtime Ready           : {status['tts_runtime_ready']}")
        print(f"STT Candidates              : {status['stt_candidates']}")
        print(f"TTS Candidates              : {status['tts_candidates']}")
        print(f"Candidate Count             : {status['candidate_count']}")
        print(f"Note                        : {status['note']}")

    def voice_runtime_plan(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        plan = planner.plan()
        recommended = plan["recommended_path"]

        print("AURA Voice Runtime Plan")
        print("=======================")
        print("Recommended Path")
        print("----------------")
        print(f"STT         : {recommended['stt']}")
        print(f"TTS         : {recommended['tts']}")
        print(f"Fallback TTS: {recommended['fallback_tts']}")
        print(f"Audio I/O   : {recommended['audio_io']}")
        print(f"Description : {recommended['description']}")
        print()
        print("Phases")
        print("------")

        for phase in plan["phases"]:
            print(f"- Phase {phase['phase']}: {phase['name']}")
            print(f"  Status     : {phase['status']}")
            print(f"  Description: {phase['description']}")

        print()
        print("STT Candidates")
        print("--------------")
        for candidate in plan["stt_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("TTS Candidates")
        print("--------------")
        for candidate in plan["tts_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Safety Rules")
        print("------------")
        for rule in plan["safety_rules"]:
            print(f"- {rule}")

    def voice_runtime_check(self) -> None:
        planner = VoiceRuntimePlanner(project_root=self.project_root)
        result = planner.check()
        dependencies = result["dependencies"]
        activation = result["activation_contract"]
        listen_state = result["listen_state_contract"]
        microphone_boundary = result["microphone_capture_boundary_contract"]
        stt_adapter = result["speech_to_text_adapter_runtime_contract"]

        print("AURA Voice Runtime Check")
        print("========================")
        print(f"Status                      : {result['status']}")
        print(f"Planning Ready              : {result['planning_ready']}")
        print(f"Activation Foundation Ready : {result['activation_foundation_ready']}")
        print(f"Runtime Ready               : {result['runtime_ready']}")
        print(f"Assertion Count             : {result['assertion_count']}")
        print(f"Failed Assertion Count      : {result['failed_assertion_count']}")
        print(f"Python Packages             : {result['python_packages_installed']}/{result['python_packages_total']}")
        print(f"Executables                 : {result['executables_found']}/{result['executables_total']}")
        print()
        print("Sprint 191 Activation Guardrails")
        print("--------------------------------")
        print(f"Safe Idle Default           : {activation['safe_idle_default']}")
        print(f"Push To Talk Required       : {activation['push_to_talk_required']}")
        print(f"Explicit Listen Required    : {activation['explicit_listen_required']}")
        print(f"Always Listening Enabled    : {activation['always_listening_enabled']}")
        print(f"Hidden Capture Enabled      : {activation['hidden_capture_enabled']}")
        print(f"Background Wake Word Enabled: {activation['background_wake_word_enabled']}")
        print(f"Silent Cloud Fallback       : {activation['silent_cloud_fallback_enabled']}")
        print(f"Direct Voice To Action      : {activation['direct_voice_to_action_enabled']}")
        print(f"Chat Session Reuse Required : {activation['chat_session_reuse_required']}")
        print()
        print("Sprint 192 Listen State")
        print("-----------------------")
        print(f"Listen State Foundation Ready: {listen_state['listen_state_foundation_ready']}")
        print(f"Default State                : {listen_state['default_state']}")
        print(f"Current State                : {listen_state['current_state']}")
        print(f"Allowed States               : {len(listen_state['allowed_states'])}")
        print(f"Explicit Stop Required       : {listen_state['explicit_stop_required']}")
        print(f"Permission Before Listening  : {listen_state['permission_required_before_listening']}")
        print(f"Microphone Capture Active    : {listen_state['microphone_capture_active']}")
        print(f"Audio Buffer Active          : {listen_state['audio_buffer_active']}")
        print(f"STT Runtime Active           : {listen_state['stt_runtime_active']}")
        print(f"Listen Loop Active           : {listen_state['listen_loop_active']}")
        print(f"Background Listener Active   : {listen_state['background_listener_active']}")
        print(f"Wake Word Active             : {listen_state['wake_word_active']}")
        print(f"State Persistence Runtime    : {listen_state['state_persistence_runtime']}")
        print(f"State Mutation Runtime       : {listen_state['state_mutation_runtime']}")
        print(f"Audio Device Access          : {listen_state['audio_device_access']}")
        print()
        print("Allowed Listen States")
        print("---------------------")
        for state in listen_state["allowed_states"]:
            print(f"- {state}")
        print()
        print("Sprint 193 Microphone Capture Boundary")
        print("--------------------------------------")
        print(f"Microphone Boundary Ready   : {microphone_boundary['microphone_boundary_ready']}")
        print(f"Capture Runtime Ready       : {microphone_boundary['microphone_capture_runtime_ready']}")
        print(f"Microphone Capture Active   : {microphone_boundary['microphone_capture_active']}")
        print(f"Permission Before Capture   : {microphone_boundary['permission_required_before_capture']}")
        print(f"Listen State Before Capture : {microphone_boundary['explicit_listen_state_required_before_capture']}")
        print(f"Required Listen State       : {microphone_boundary['required_listen_state_before_capture']}")
        print(f"Push To Talk Before Capture : {microphone_boundary['push_to_talk_required_before_capture']}")
        print(f"Audio Device Access         : {microphone_boundary['audio_device_access']}")
        print(f"Audio Device Discovery      : {microphone_boundary['audio_device_discovery_active']}")
        print(f"Device Enumeration Performed: {microphone_boundary['device_enumeration_performed']}")
        print(f"Sounddevice Available       : {microphone_boundary['sounddevice_available']}")
        print(f"Sounddevice Runtime Imported: {microphone_boundary['sounddevice_runtime_imported']}")
        print(f"Recording Enabled           : {microphone_boundary['recording_enabled']}")
        print(f"Recording Active            : {microphone_boundary['recording_active']}")
        print(f"Audio Buffer Active         : {microphone_boundary['audio_buffer_active']}")
        print(f"Audio File Write Active     : {microphone_boundary['audio_file_write_active']}")
        print(f"Audio Persistence Enabled   : {microphone_boundary['audio_persistence_enabled']}")
        print(f"Audio Transmission Enabled  : {microphone_boundary['audio_transmission_enabled']}")
        print(f"STT Runtime Active          : {microphone_boundary['stt_runtime_active']}")
        print(f"Transcription Active        : {microphone_boundary['transcription_active']}")
        print(f"Listen Loop Active          : {microphone_boundary['listen_loop_active']}")
        print(f"Background Listener Active  : {microphone_boundary['background_listener_active']}")
        print(f"Wake Word Active            : {microphone_boundary['wake_word_active']}")
        print(f"Hidden Capture Enabled      : {microphone_boundary['hidden_capture_enabled']}")
        print(f"Always Listening Enabled    : {microphone_boundary['always_listening_enabled']}")
        print()
        print("Sprint 194 Speech-to-Text Adapter Runtime")
        print("-----------------------------------------")
        print(f"STT Adapter Contract Ready  : {stt_adapter['stt_adapter_contract_ready']}")
        print(f"STT Adapter Runtime Ready   : {stt_adapter['stt_adapter_runtime_ready']}")
        print(f"Default Adapter             : {stt_adapter['default_adapter']}")
        print(f"Candidate Adapter Count     : {stt_adapter['candidate_adapter_count']}")
        print(f"Local First Required        : {stt_adapter['local_first_required']}")
        print(f"Offline First Required      : {stt_adapter['offline_first_required']}")
        print(f"Audio File Boundary Ready   : {stt_adapter['audio_file_input_boundary_ready']}")
        print(f"Audio File STT Runtime Ready: {stt_adapter['audio_file_transcription_runtime_ready']}")
        print(f"Audio File Read Active      : {stt_adapter['audio_file_read_active']}")
        print(f"Audio File Write Active     : {stt_adapter['audio_file_write_active']}")
        print(f"Mic Capture Required        : {stt_adapter['microphone_capture_required_for_adapter_contract']}")
        print(f"Live Mic Transcription      : {stt_adapter['live_microphone_transcription_active']}")
        print(f"Microphone Capture Active   : {stt_adapter['microphone_capture_active']}")
        print(f"Audio Device Access         : {stt_adapter['audio_device_access']}")
        print(f"Audio Device Discovery      : {stt_adapter['audio_device_discovery_active']}")
        print(f"Recording Active            : {stt_adapter['recording_active']}")
        print(f"Audio Buffer Active         : {stt_adapter['audio_buffer_active']}")
        print(f"STT Runtime Active          : {stt_adapter['stt_runtime_active']}")
        print(f"Transcription Active        : {stt_adapter['transcription_active']}")
        print(f"Transcript Persistence      : {stt_adapter['transcript_persistence_enabled']}")
        print(f"Transcript To Chat Handoff  : {stt_adapter['transcript_to_chat_handoff_enabled']}")
        print(f"Transcript To Action        : {stt_adapter['transcript_to_action_enabled']}")
        print(f"Model Download Required     : {stt_adapter['model_download_required']}")
        print(f"Model Download Performed    : {stt_adapter['model_download_performed']}")
        print(f"Dependency Install Performed: {stt_adapter['dependency_install_performed']}")
        print(f"Cloud STT Fallback          : {stt_adapter['cloud_stt_fallback_enabled']}")
        print(f"Silent Cloud Fallback       : {stt_adapter['silent_cloud_fallback_enabled']}")
        print(f"Remote Provider Enabled     : {stt_adapter['remote_provider_enabled']}")
        print(f"Permission Before STT       : {stt_adapter['permission_required_before_transcription']}")
        print()
        print("STT Adapter Candidates")
        print("----------------------")
        for adapter in stt_adapter["candidate_adapters"]:
            print(f"- {adapter}")
        print()
        print("Failed Assertions")
        print("-----------------")
        if result["failed_assertions"]:
            for assertion in result["failed_assertions"]:
                print(f"- {assertion}")
        else:
            print("- none")
        print()
        print("Python Packages")
        print("---------------")
        for package in dependencies["python_packages"]:
            print(f"- {package['name']}: {package['installed']} ({package['purpose']})")

        print()
        print("Executables")
        print("-----------")
        for executable in dependencies["executables"]:
            print(f"- {executable['name']}: {executable['found']} ({executable['purpose']})")

        print()
        print("Environment")
        print("-----------")
        environment = dependencies["environment"]
        print(f"OS             : {environment['os']}")
        print(f"OS Release     : {environment['os_release']}")
        print(f"Machine        : {environment['machine']}")
        print(f"Pulse Server   : {environment['pulse_server'] or '-'}")
        print(f"PipeWire Runtime: {environment['pipewire_runtime'] or '-'}")
        print(f"XDG Runtime    : {environment['xdg_runtime'] or '-'}")
        print()
        print(f"Note: {result['note']}")

    def voice_status(self) -> None:
        voice_manager = VoiceManager()
        status = voice_manager.status()

        print("AURA Voice Status")
        print("=================")
        print(f"Status           : {status['status']}")
        print(f"Microphone Access: {status['microphone_access']}")
        print(f"Speaker Output   : {status['speaker_output']}")
        print(f"STT Ready        : {status['stt_ready']}")
        print(f"TTS Ready        : {status['tts_ready']}")
        print(f"Providers        : {status['providers']}")
        print(f"Note             : {status['note']}")

    def voice_providers(self) -> None:
        voice_manager = VoiceManager()

        print("AURA Voice Providers")
        print("====================")

        for provider in voice_manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type            : {provider.provider_type}")
            print(f"  Status          : {provider.status}")
            print(f"  Input Supported : {provider.input_supported}")
            print(f"  Output Supported: {provider.output_supported}")
            print(f"  Description     : {provider.description}")
            print()

    def awakening_status(self) -> None:
        awakening_manager = AwakeningManager(project_root=self.project_root)
        status = awakening_manager.build_status()

        print("AURA Awakening Status")
        print("=====================")
        print(f"Milestone     : {status['milestone']}")
        print(f"Phase         : {status['phase']}")
        print(f"Status        : {status['status']}")
        print(f"Readiness     : {status['ready_count']}/{status['total_pillars']} pillars")
        print()
        print("Pillars:")
        for pillar in status["pillars"]:
            print(f"- {pillar['name']}")
            print(f"  Status     : {pillar['status']}")
            print(f"  Ready      : {pillar['ready']}")
            print(f"  Description: {pillar['description']}")
            print(f"  Note       : {pillar['note']}")
        print()
        print("Foundation Counts:")
        print(f"- Voice Providers: {status['voice_providers']}")
        print(f"- Vision Providers: {status['vision_providers']}")
        print(f"- Memory Records : {status['memory_records']}")
        print(f"- Journal Entries: {status['journal_entries']}")
        print(f"- Roles          : {status['roles']}")
        print(f"- Skills         : {status['skills']}")
        print(f"- Plugin Actions : {status['plugin_actions']}")
        print()
        print(f"Summary: {status['summary']}")

    def vision_runtime_status(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        status = planner.status()

        print("AURA Vision Runtime Status")
        print("==========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Planning Ready       : {status['planning_ready']}")
        print(f"Runtime Ready        : {status['runtime_ready']}")
        print(f"Screen Access        : {status['screen_access']}")
        print(f"Camera Access        : {status['camera_access']}")
        print(f"Screen Runtime Ready : {status['screen_runtime_ready']}")
        print(f"Camera Runtime Ready : {status['camera_runtime_ready']}")
        print(f"Vision Model Ready   : {status['vision_model_ready']}")
        print(f"Screen Candidates    : {status['screen_candidates']}")
        print(f"Camera Candidates    : {status['camera_candidates']}")
        print(f"Model Candidates     : {status['model_candidates']}")
        print(f"Candidate Count      : {status['candidate_count']}")
        print(f"Note                 : {status['note']}")

    def vision_runtime_plan(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        plan = planner.plan()
        recommended = plan["recommended_path"]

        print("AURA Vision Runtime Plan")
        print("========================")
        print("Recommended Path")
        print("----------------")
        print(f"Screen Capture  : {recommended['screen_capture']}")
        print(f"Camera Capture  : {recommended['camera_capture']}")
        print(f"Vision Model    : {recommended['vision_model']}")
        print(f"Image Processing: {recommended['image_processing']}")
        print(f"Description     : {recommended['description']}")
        print()
        print("Phases")
        print("------")

        for phase in plan["phases"]:
            print(f"- Phase {phase['phase']}: {phase['name']}")
            print(f"  Status     : {phase['status']}")
            print(f"  Description: {phase['description']}")

        print()
        print("Screen Capture Candidates")
        print("-------------------------")
        for candidate in plan["screen_capture_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Camera Capture Candidates")
        print("-------------------------")
        for candidate in plan["camera_capture_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Vision Model Candidates")
        print("-----------------------")
        for candidate in plan["vision_model_candidates"]:
            print(f"- {candidate['name']} ({candidate['status']})")
            print(f"  {candidate['description']}")

        print()
        print("Safety Rules")
        print("------------")
        for rule in plan["safety_rules"]:
            print(f"- {rule}")

    def vision_runtime_check(self) -> None:
        planner = VisionRuntimePlanner(project_root=self.project_root)
        result = planner.check()
        dependencies = result["dependencies"]

        print("AURA Vision Runtime Check")
        print("=========================")
        print(f"Status                 : {result['status']}")
        print(f"Planning Ready         : {result['planning_ready']}")
        print(f"Runtime Ready          : {result['runtime_ready']}")
        print(f"Python Packages        : {result['python_packages_installed']}/{result['python_packages_total']}")
        print(f"Executables            : {result['executables_found']}/{result['executables_total']}")
        print()
        print("Python Packages")
        print("---------------")
        for package in dependencies["python_packages"]:
            print(f"- {package['name']}: {package['installed']} ({package['purpose']})")

        print()
        print("Executables")
        print("-----------")
        for executable in dependencies["executables"]:
            print(f"- {executable['name']}: {executable['found']} ({executable['purpose']})")

        print()
        print("Environment")
        print("-----------")
        environment = dependencies["environment"]
        print(f"OS                 : {environment['os']}")
        print(f"OS Release         : {environment['os_release']}")
        print(f"Machine            : {environment['machine']}")
        print(f"Desktop Environment: {environment['desktop_environment']}")
        print(f"Display            : {environment['display'] or '-'}")
        print(f"Wayland Display    : {environment['wayland_display'] or '-'}")
        print(f"XDG Runtime        : {environment['xdg_runtime'] or '-'}")
        print()
        print(f"Note: {result['note']}")

    def vision_status(self) -> None:
        vision_manager = VisionManager()
        status = vision_manager.status()

        print("AURA Vision Status")
        print("==================")
        print(f"Status       : {status['status']}")
        print(f"Screen Access: {status['screen_access']}")
        print(f"Camera Access: {status['camera_access']}")
        print(f"Screen Ready : {status['screen_ready']}")
        print(f"Camera Ready : {status['camera_ready']}")
        print(f"Providers    : {status['providers']}")
        print(f"Note         : {status['note']}")

    def vision_providers(self) -> None:
        vision_manager = VisionManager()

        print("AURA Vision Providers")
        print("=====================")

        for provider in vision_manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type            : {provider.provider_type}")
            print(f"  Status          : {provider.status}")
            print(f"  Screen Supported: {provider.screen_supported}")
            print(f"  Camera Supported: {provider.camera_supported}")
            print(f"  Description     : {provider.description}")
            print()

    def tool_sandbox_status(self) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        status = sandbox.status()

        print("AURA Tool Sandbox Status")
        print("========================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Sandbox Ready                : {status['sandbox_ready']}")
        print(f"Policy Ready                 : {status['policy_ready']}")
        print(f"Dry Run Ready                : {status['dry_run_ready']}")
        print(f"Real Execution Ready         : {status['real_execution_ready']}")
        print(f"Requires Confirmation        : {status['requires_confirmation_for_execution']}")
        print(f"Allowed Commands             : {status['allowed_command_count']}")
        print(f"Blocked Commands             : {status['blocked_command_count']}")
        print(f"Blocked Patterns             : {status['blocked_pattern_count']}")
        print(f"Project Root                 : {status['project_root']}")
        print()
        print(f"Note: {status['note']}")

    def tool_sandbox_policy(self) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        policy = sandbox.policy_dict()

        print("AURA Tool Sandbox Policy")
        print("========================")
        print(f"Name                         : {policy['name']}")
        print(f"Status                       : {policy['status']}")
        print(f"Dry Run Supported            : {policy['dry_run_supported']}")
        print(f"Real Execution Supported     : {policy['real_execution_supported']}")
        print(f"Requires Confirmation        : {policy['requires_confirmation_for_execution']}")
        print(f"Description                  : {policy['description']}")
        print()

        print("Allowed Commands")
        print("----------------")
        for command in policy["allowed_commands"]:
            print(f"- {command}")

        print()
        print("Blocked Commands")
        print("----------------")
        for command in policy["blocked_commands"]:
            print(f"- {command}")

        print()
        print("Blocked Patterns")
        print("----------------")
        for pattern in policy["blocked_patterns"]:
            print(f"- {pattern}")

    def tool_sandbox_check(self, command: str) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        result = sandbox.check_command(command)

        print("AURA Tool Sandbox Check")
        print("=======================")
        print(f"Command              : {result['command']}")
        print(f"Normalized Command   : {result['normalized_command']}")
        print(f"Base Command         : {result['base_command']}")
        print(f"State                : {result['state']}")
        print(f"Allowed              : {result['allowed']}")
        print(f"Dry Run Supported    : {result['dry_run_supported']}")
        print(f"Real Execution       : {result['real_execution_supported']}")
        print(f"Confirmation Required: {result['requires_confirmation_for_execution']}")
        print(f"Executed             : {result['executed']}")
        print(f"Reason               : {result['reason']}")

        if result["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in result["blocked_patterns_found"]:
                print(f"- {pattern}")

        print()
        print(f"Note: {result['note']}")

    def tool_sandbox_dry_run(self, command: str) -> None:
        sandbox = ToolSandboxManager(project_root=self.project_root)
        result = sandbox.dry_run(command)
        check = result["check"]

        print("AURA Tool Sandbox Dry Run")
        print("=========================")
        print(f"Command       : {result['command']}")
        print(f"Dry Run Ready : {result['dry_run_ready']}")
        print(f"Would Execute : {result['would_execute']}")
        print(f"Executed      : {result['executed']}")
        print(f"Check State   : {check['state']}")
        print(f"Allowed       : {check['allowed']}")
        print(f"Reason        : {check['reason']}")

        if check["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in check["blocked_patterns_found"]:
                print(f"- {pattern}")

        if result["plan"]:
            print()
            print("Plan")
            print("----")
            for step in result["plan"]:
                print(f"- {step}")

        print()
        print(f"Note: {result['note']}")

    def model_router_status(self) -> None:
        router = ModelRouter(project_root=self.project_root)
        status = router.status()

        print("AURA Model Router Status")
        print("========================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Router Ready           : {status['router_ready']}")
        print(f"Route Selection Ready  : {status['route_selection_ready']}")
        print(f"Runtime Switching Ready: {status['runtime_switching_ready']}")
        print(f"Model Download Ready   : {status['model_download_ready']}")
        print(f"Active Provider        : {status['active_provider']}")
        print(f"Active Model           : {status['active_model']}")
        print(f"Active Host            : {status['active_host']}")
        print(f"Routes                 : {status['routes']}")
        print()
        print("Route Status Counts")
        print("-------------------")
        for name, value in status["route_status_counts"].items():
            print(f"{name:<12}: {value}")
        print()
        print(f"Note: {status['note']}")

    def model_router_routes(self) -> None:
        router = ModelRouter(project_root=self.project_root)

        print("AURA Model Router Routes")
        print("========================")

        for route in router.list_routes():
            print(f"- {route.name}")
            print(f"  Role       : {route.role}")
            print(f"  Provider   : {route.provider}")
            print(f"  Model      : {route.model}")
            print(f"  Status     : {route.status}")
            print(f"  Description: {route.description}")

            if route.use_cases:
                print(f"  Use Cases  : {', '.join(route.use_cases)}")

            if route.candidate_models:
                print(f"  Candidates : {', '.join(route.candidate_models)}")

            if route.safety_notes:
                print("  Safety:")
                for note in route.safety_notes:
                    print(f"  - {note}")

            print()

    def model_router_select(self, target: str) -> None:
        router = ModelRouter(project_root=self.project_root)
        result = router.select(target)
        route = result["route"]

        print("AURA Model Router Selection")
        print("===========================")
        print(f"Target                     : {result['target']}")
        print(f"Normalized Target          : {result['normalized_target']}")
        print(f"Found                      : {result['found']}")
        print(f"Fallback Used              : {result['fallback_used']}")
        print(f"Runtime Switching Performed: {result['runtime_switching_performed']}")
        print()

        if route:
            print("Selected Route")
            print("--------------")
            print(f"Name       : {route['name']}")
            print(f"Role       : {route['role']}")
            print(f"Provider   : {route['provider']}")
            print(f"Model      : {route['model']}")
            print(f"Status     : {route['status']}")
            print(f"Description: {route['description']}")

            if route["use_cases"]:
                print(f"Use Cases  : {', '.join(route['use_cases'])}")

            if route["candidate_models"]:
                print(f"Candidates : {', '.join(route['candidate_models'])}")

            if route["safety_notes"]:
                print("Safety:")
                for note in route["safety_notes"]:
                    print(f"- {note}")

        print()
        print(f"Note: {result['note']}")

    def core_loop_status(self) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Alpha Core Loop Status")
        print("===========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Loop Ready           : {status['loop_ready']}")
        print(f"Execution Ready      : {status['execution_ready']}")
        print(f"Safe Action Execution: {status['safe_action_execution']}")
        print(f"Steps                : {status['steps']}")
        print(f"Flow                 : {status['flow']}")
        print()
        print("Systems")
        print("-------")
        for name, value in status["systems"].items():
            print(f"{name:<16}: {value}")
        print()
        print("Runtime")
        print("-------")
        for name, value in status["runtime"].items():
            print(f"{name:<22}: {value}")
        print()
        print(f"Note: {status['note']}")

    def core_loop_run(self, message: str) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        result = manager.run(message=message)

        print("AURA Alpha Core Loop Run")
        print("========================")
        print(f"Input     : {result['input']['message']}")
        print(f"Action    : {result['plan']['inferred_action']}")
        print(f"Mode      : {result['plan']['mode']}")
        print(f"Executed  : {result['execution']['executed']}")
        print()
        print("Context")
        print("-------")
        context = result["context"]
        print(f"Pinned Memories       : {context['pinned_memories']}")
        print(f"Important Memories    : {context['important_memories']}")
        print(f"Relevant Memories     : {context['relevant_memories']}")
        print(f"Recent Journal Entries: {context['recent_journal_entries']}")
        if context["latest_journal"]:
            print(f"Latest Journal        : {context['latest_journal']}")
        print()
        print("Safety")
        print("------")
        safety = result["safety"]
        print(f"Resolved Action : {safety['resolved_action']}")
        print(f"Request State   : {safety['request_state']}")
        print(f"Allowed         : {safety['allowed']}")
        print(f"Confirmation    : {safety['requires_confirmation']}")
        print(f"Permission      : {safety['permission_action']}")
        print(f"Reason          : {safety['reason']}")
        print()
        print("AURA Response")
        print("-------------")
        print(result["response"]["text"])
        print()
        print("Journal")
        print("-------")
        print(f"Mode           : {result['journal']['mode']}")
        print(f"Write Performed: {result['journal']['write_performed']}")
        print(f"Note           : {result['journal']['note']}")

    def core_loop_trace(self, message: str) -> None:
        manager = CoreLoopManager(project_root=self.project_root)
        result = manager.trace(message=message)

        print("AURA Alpha Core Loop Trace")
        print("==========================")
        print(f"Loop      : {result['loop']['name']} v{result['loop']['version']}")
        print(f"Status    : {result['loop']['status']}")
        print(f"Input     : {result['input']['message']}")
        print()
        print("Steps")
        print("-----")
        for step in result["loop"]["steps"]:
            print(f"{step['index']}. {step['name']}")
            print(f"   Status     : {step['status']}")
            print(f"   Component  : {step['component']}")
            print(f"   Description: {step['description']}")
        print()
        print("Trace Summary")
        print("-------------")
        print(f"Inferred Action: {result['plan']['inferred_action']}")
        print(f"Safety State   : {result['safety']['request_state']}")
        print(f"Allowed        : {result['safety']['allowed']}")
        print(f"Executed       : {result['execution']['executed']}")
        print()
        print("Response Preview")
        print("----------------")
        print(result["response"]["text"])

    def avatar_status(self) -> None:
        manager = AvatarManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Avatar Status")
        print("==================")
        print(f"Name                    : {status['name']}")
        print(f"Version                 : {status['version']}")
        print(f"Status                  : {status['status']}")
        print(f"Foundation Ready        : {status['foundation_ready']}")
        print(f"Runtime Ready           : {status['runtime_ready']}")
        print(f"Avatar Loaded           : {status['avatar_loaded']}")
        print(f"Expression Runtime Ready: {status['expression_runtime_ready']}")
        print(f"Gesture Runtime Ready   : {status['gesture_runtime_ready']}")
        print(f"Motion Runtime Ready    : {status['motion_runtime_ready']}")
        print(f"Providers               : {status['providers']}")
        print(f"Expressions             : {status['expressions']}")
        print(f"Gestures                : {status['gestures']}")
        print(f"Note                    : {status['note']}")

    def avatar_providers(self) -> None:
        manager = AvatarManager(project_root=self.project_root)

        print("AURA Avatar Providers")
        print("=====================")

        for provider in manager.list_providers():
            print(f"- {provider.name}")
            print(f"  Type                : {provider.provider_type}")
            print(f"  Status              : {provider.status}")
            print(f"  State Supported     : {provider.state_supported}")
            print(f"  Expression Supported: {provider.expression_supported}")
            print(f"  Gesture Supported   : {provider.gesture_supported}")
            print(f"  Runtime Supported   : {provider.runtime_supported}")
            print(f"  Description         : {provider.description}")
            print()

    def avatar_state(self) -> None:
        manager = AvatarManager(project_root=self.project_root)
        state = manager.state()

        print("AURA Avatar State")
        print("=================")
        print(f"Avatar Name       : {state['avatar_name']}")
        print(f"Avatar Format     : {state['avatar_format']}")
        print(f"Runtime           : {state['runtime']}")
        print(f"Body State        : {state['body_state']}")
        print(f"Pose              : {state['pose']}")
        print(f"Expression        : {state['expression']}")
        print(f"Gesture           : {state['gesture']}")
        print(f"Model Loaded      : {state['model_loaded']}")
        print(f"Tracking Connected: {state['tracking_connected']}")
        print(f"Voice Link Ready  : {state['voice_link_ready']}")
        print(f"Vision Link Ready : {state['vision_link_ready']}")
        print(f"Motion Link Ready : {state['motion_link_ready']}")
        print()
        print("Supported Expressions:")
        for expression in state["supported_expressions"]:
            print(f"- {expression}")
        print()
        print("Supported Gestures:")
        for gesture in state["supported_gestures"]:
            print(f"- {gesture}")
        print()
        print("Planning:")
        planning = state["planning"]
        print(f"Preferred Format   : {planning['preferred_format']}")
        print(f"Authoring Tools    : {', '.join(planning['authoring_tools'])}")
        print(f"Runtime Candidates : {', '.join(planning['runtime_candidates'])}")
        print(f"Future Links       : {', '.join(planning['future_links'])}")
        print()
        print(f"Note: {state['note']}")

    def avatar_expression(self, expression: str) -> None:
        manager = AvatarManager(project_root=self.project_root)
        result = manager.expression_request(expression=expression)
        permission = result["permission"]

        print("AURA Avatar Expression Proposal")
        print("===============================")
        print(f"Requested Expression: {result['requested_expression']}")
        print(f"Supported           : {result['supported']}")
        print(f"Request State       : {result['request_state']}")
        print(f"Runtime Ready       : {result['runtime_ready']}")
        print(f"Executed            : {result['executed']}")
        print()
        print("Permission")
        print("----------")
        print(f"Action      : {permission['action']}")
        print(f"Level       : {permission['level']} - {permission['level_label']}")
        print(f"Allowed     : {permission['allowed']}")
        print(f"Confirmation: {permission['requires_confirmation']}")
        print(f"Reason      : {permission['reason']}")
        print()
        print(f"Note: {result['note']}")

    def avatar_gesture(self, gesture: str) -> None:
        manager = AvatarManager(project_root=self.project_root)
        result = manager.gesture_request(gesture=gesture)
        permission = result["permission"]

        print("AURA Avatar Gesture Proposal")
        print("============================")
        print(f"Requested Gesture: {result['requested_gesture']}")
        print(f"Supported        : {result['supported']}")
        print(f"Request State    : {result['request_state']}")
        print(f"Runtime Ready    : {result['runtime_ready']}")
        print(f"Executed         : {result['executed']}")
        print()
        print("Permission")
        print("----------")
        print(f"Action      : {permission['action']}")
        print(f"Level       : {permission['level']} - {permission['level_label']}")
        print(f"Allowed     : {permission['allowed']}")
        print(f"Confirmation: {permission['requires_confirmation']}")
        print(f"Reason      : {permission['reason']}")
        print()
        print(f"Note: {result['note']}")

    def desktop_status(self) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        status = manager.status()
        environment = status["environment"]

        print("AURA Desktop Bridge Status")
        print("==========================")
        print(f"Name                 : {status['name']}")
        print(f"Version              : {status['version']}")
        print(f"Status               : {status['status']}")
        print(f"Bridge Ready         : {status['bridge_ready']}")
        print(f"Execution Ready      : {status['execution_ready']}")
        print(f"Safe Action Execution: {status['safe_action_execution']}")
        print(f"Capability Count     : {status['capability_count']}")
        print()
        print("Environment")
        print("-----------")
        print(f"OS                  : {environment['os']}")
        print(f"OS Release          : {environment['os_release']}")
        print(f"Machine             : {environment['machine']}")
        print(f"Desktop Environment: {environment['desktop_environment']}")
        print(f"Display             : {environment['display'] or '-'}")
        print(f"Wayland Display     : {environment['wayland_display'] or '-'}")
        print()
        print(f"Note: {status['note']}")

    def desktop_capabilities(self) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        capabilities = manager.capabilities()

        print("AURA Desktop Capabilities")
        print("=========================")
        print(f"Total: {len(capabilities)}")
        print()

        for capability in capabilities:
            print(f"- {capability['name']}")
            print(f"  Status       : {capability['status']}")
            print(f"  Permission   : {capability['permission_action']}")
            print(f"  Confirmation : {capability['requires_confirmation']}")
            print(f"  Execution    : {capability['execution_ready']}")
            print(f"  Description  : {capability['description']}")
            print()

    def desktop_action(self, action: str) -> None:
        manager = DesktopBridgeManager(project_root=self.project_root)
        proposal = manager.action_request(action_name=action)
        request = proposal["action_request"]

        print("AURA Desktop Action Proposal")
        print("============================")
        print(f"Requested Action        : {proposal['requested_action']}")
        print(f"Desktop Capability Found: {proposal['desktop_capability_found']}")
        print(f"Desktop State           : {proposal['desktop_state']}")
        print(f"Execution Ready         : {proposal['execution_ready']}")
        print(f"Executed                : {proposal['executed']}")
        print()
        print("Action Request")
        print("--------------")
        print(f"Resolved Action   : {request.resolved_action}")
        print(f"Request State     : {request.request_state}")
        print(f"Plugin Found      : {request.plugin_action_found}")
        print(f"Plugin            : {request.plugin or '-'}")
        print(f"Skill             : {request.skill or '-'}")
        print(f"Plugin Status     : {request.plugin_action_status}")
        print(f"Permission Action : {request.permission_action}")
        print(f"Permission Level  : {request.permission_level} - {request.permission_level_label}")
        print(f"Allowed           : {request.allowed}")
        print(f"Confirmation      : {request.requires_confirmation}")
        print(f"Reason            : {request.reason}")
        print(f"Note              : {proposal['note']}")

    def system_status(self) -> None:
        status_manager = SystemStatusManager(project_root=self.project_root)
        status = status_manager.build_status()

        print("AURA Unified System Status")
        print("==========================")
        print(f"Name       : {status['identity']['name']}")
        print(f"Version    : {status['identity']['version']}")
        print(f"Codename   : {status['identity']['codename']}")
        print(f"Creator    : {status['identity']['creator']}")
        print(f"Motto      : {status['identity']['motto']}")
        print(f"Project    : {status['project_root']}")
        print()
        print("Reasoning")
        print("---------")
        print(f"Provider   : {status['reasoning']['provider']}")
        print(f"Model      : {status['reasoning']['model']}")
        print(f"Host       : {status['reasoning']['host']}")
        print()
        print("Foundation Counts")
        print("-----------------")
        print(f"Memory Records      : {status['foundation']['memory_records']}")
        print(f"Journal Entries     : {status['foundation']['journal_entries']}")
        print(f"Roles               : {status['foundation']['roles']}")
        print(f"Skills              : {status['foundation']['skills']}")
        print(f"Plugin Actions      : {status['foundation']['plugin_actions']}")
        print(f"Core Loop Steps     : {status['foundation']['core_loop_steps']}")
        print(f"Model Routes        : {status['foundation']['model_routes']}")
        print(f"Sandbox Allowed     : {status['foundation']['sandbox_allowed_commands']}")
        print(f"Sandbox Blocked     : {status['foundation']['sandbox_blocked_commands']}")
        print(f"Sandbox Patterns    : {status['foundation']['sandbox_blocked_patterns']}")
        print(f"Project Python Files: {status['foundation']['project_python_files']}")
        print(f"Creative Assistant  : {status['foundation']['creative_assistant_sections']}")
        print(f"Creative Plan Types : {status['foundation']['creative_plan_types']}")
        print(f"Local Task Planner  : {status['foundation']['local_task_planner_sections']}")
        print(f"Local Task Types    : {status['foundation']['local_task_plan_types']}")
        print(f"Safe File Planner   : {status['foundation']['safe_file_operation_sections']}")
        print(f"Safe File Types     : {status['foundation']['safe_file_operation_types']}")
        print(f"Reflection Milestones: {status['foundation']['reflection_milestones']}")
        print(f"Voice Providers     : {status['foundation']['voice_providers']}")
        print(f"Voice Runtime Alpha : {status['foundation']['voice_runtime_alpha_sections']}")
        print(f"Vision Providers    : {status['foundation']['vision_providers']}")
        print(f"Vision Runtime Alpha: {status['foundation']['vision_runtime_alpha_sections']}")
        print(f"Avatar Providers    : {status['foundation']['avatar_providers']}")
        print(f"Avatar Runtime Alpha: {status['foundation']['avatar_runtime_alpha_sections']}")
        print(f"Awakening Readiness : {status['foundation']['awakening_readiness']}")
        print()
        print("Systems")
        print("-------")
        for name, value in status["systems"].items():
            print(f"{name:16}: {value}")
        print()
        print("Runtime")
        print("-------")
        for name, value in status["runtime"].items():
            print(f"{name:22}: {value}")
        print()
        print(f"Summary: {status['summary']}")

    def shell(self) -> None:
        shell = AuraShell()
        shell.run()

    def parse(self, args: list[str] | None = None):
        parser = argparse.ArgumentParser(
            prog="aura",
            description="AURA Genesis command-line interface",
        )

        subparsers = parser.add_subparsers(dest="command")

        remember_parser = subparsers.add_parser("remember")
        remember_parser.add_argument("content", type=str)

        recall_parser = subparsers.add_parser("recall")
        recall_parser.add_argument("--limit", type=int, default=5)

        chat_parser = subparsers.add_parser("chat")
        chat_parser.add_argument("message", type=str)

        history_parser = subparsers.add_parser("history")

        history_parser.add_argument("limit", type=int, nargs="?", default=5)
        history_parser.add_argument("--limit", type=int, default=5)

        journal_parser = subparsers.add_parser("journal")
        journal_parser.add_argument("--limit", type=int, default=5)

        journal_latest_parser = subparsers.add_parser("journal-latest")
        journal_latest_parser.add_argument("--limit", type=int, default=5)

        journal_add_parser = subparsers.add_parser("journal-add")
        journal_add_parser.add_argument("content", type=str)

        subparsers.add_parser("journal-count")

        context_parser = subparsers.add_parser("context")
        context_parser.add_argument("message", type=str)

        context_preview_parser = subparsers.add_parser("context-preview")
        context_preview_parser.add_argument("message", type=str)

        subparsers.add_parser("tool-sandbox-status")
        subparsers.add_parser("tool-sandbox-policy")

        tool_sandbox_check_parser = subparsers.add_parser("tool-sandbox-check")
        tool_sandbox_check_parser.add_argument("command_text", type=str)

        tool_sandbox_dry_run_parser = subparsers.add_parser("tool-sandbox-dry-run")
        tool_sandbox_dry_run_parser.add_argument("command_text", type=str)

        subparsers.add_parser("model-router-status")
        subparsers.add_parser("model-router-routes")

        model_router_select_parser = subparsers.add_parser("model-router-select")
        model_router_select_parser.add_argument("target", type=str)

        subparsers.add_parser("core-loop-status")

        core_loop_run_parser = subparsers.add_parser("core-loop-run")
        core_loop_run_parser.add_argument("message", type=str)

        core_loop_trace_parser = subparsers.add_parser("core-loop-trace")
        core_loop_trace_parser.add_argument("message", type=str)

        subparsers.add_parser("avatar-runtime-alpha-status")

        avatar_expression_plan_parser = subparsers.add_parser("avatar-expression-plan")
        avatar_expression_plan_parser.add_argument("expression")

        avatar_gesture_plan_parser = subparsers.add_parser("avatar-gesture-plan")
        avatar_gesture_plan_parser.add_argument("gesture")

        subparsers.add_parser("avatar-runtime-context")

        subparsers.add_parser("avatar-status")
        subparsers.add_parser("avatar-providers")
        subparsers.add_parser("avatar-state")

        avatar_expression_parser = subparsers.add_parser("avatar-expression")
        avatar_expression_parser.add_argument("expression", type=str)

        avatar_gesture_parser = subparsers.add_parser("avatar-gesture")
        avatar_gesture_parser.add_argument("gesture", type=str)

        subparsers.add_parser("desktop-alpha-status")

        desktop_action_plan_parser = subparsers.add_parser("desktop-action-plan")
        desktop_action_plan_parser.add_argument("action_type")
        desktop_action_plan_parser.add_argument("target", nargs="+")

        desktop_open_app_plan_parser = subparsers.add_parser("desktop-open-app-plan")
        desktop_open_app_plan_parser.add_argument("app_name", nargs="+")

        desktop_open_browser_plan_parser = subparsers.add_parser("desktop-open-browser-plan")
        desktop_open_browser_plan_parser.add_argument("url", nargs="+")

        desktop_open_file_plan_parser = subparsers.add_parser("desktop-open-file-plan")
        desktop_open_file_plan_parser.add_argument("file_path", nargs="+")

        subparsers.add_parser("desktop-workspace-context")

        subparsers.add_parser("desktop-status")
        subparsers.add_parser("desktop-capabilities")

        desktop_action_parser = subparsers.add_parser("desktop-action")
        desktop_action_parser.add_argument("action", type=str)

        subparsers.add_parser("system-status")
        subparsers.add_parser("status-full")

        subparsers.add_parser("vision-runtime-alpha-status")
        subparsers.add_parser("vision-screen-plan")
        subparsers.add_parser("vision-camera-plan")
        subparsers.add_parser("vision-runtime-context")

        subparsers.add_parser("vision-runtime-status")
        subparsers.add_parser("vision-runtime-plan")
        subparsers.add_parser("vision-runtime-check")

        subparsers.add_parser("vision-status")
        subparsers.add_parser("vision-providers")

        subparsers.add_parser("safe-file-operation-status")

        safe_file_read_parser = subparsers.add_parser("safe-file-read-plan")
        safe_file_read_parser.add_argument("target", nargs="+")

        safe_file_write_parser = subparsers.add_parser("safe-file-write-plan")
        safe_file_write_parser.add_argument("target", nargs="+")

        safe_file_edit_parser = subparsers.add_parser("safe-file-edit-plan")
        safe_file_edit_parser.add_argument("target", nargs="+")

        safe_file_risk_parser = subparsers.add_parser("safe-file-move-copy-delete-risk-review")
        safe_file_risk_parser.add_argument("target", nargs="+")

        safe_file_checklist_parser = subparsers.add_parser("safe-file-operation-checklist")
        safe_file_checklist_parser.add_argument("target", nargs="+")

        subparsers.add_parser("safe-file-operation-context")

        subparsers.add_parser("local-task-planner-status")

        local_task_intent_parser = subparsers.add_parser("local-task-intent-plan")
        local_task_intent_parser.add_argument("target", nargs="+")

        local_task_breakdown_parser = subparsers.add_parser("local-task-breakdown-plan")
        local_task_breakdown_parser.add_argument("target", nargs="+")

        local_task_risk_parser = subparsers.add_parser("local-task-risk-review")
        local_task_risk_parser.add_argument("target", nargs="+")

        local_task_checklist_parser = subparsers.add_parser("local-task-execution-checklist")
        local_task_checklist_parser.add_argument("target", nargs="+")

        subparsers.add_parser("local-task-context")

        subparsers.add_parser("creative-assistant-status")

        creative_brief_parser = subparsers.add_parser("creative-brief-plan")
        creative_brief_parser.add_argument("target", nargs="+")

        creative_character_parser = subparsers.add_parser("creative-character-concept-plan")
        creative_character_parser.add_argument("target", nargs="+")

        creative_visual_parser = subparsers.add_parser("creative-visual-asset-plan")
        creative_visual_parser.add_argument("target", nargs="+")

        creative_content_parser = subparsers.add_parser("creative-content-idea-plan")
        creative_content_parser.add_argument("target", nargs="+")

        creative_review_parser = subparsers.add_parser("creative-review-plan")
        creative_review_parser.add_argument("target", nargs="+")

        subparsers.add_parser("creative-context")

        subparsers.add_parser("project-intent-status")

        project_intent_summary_parser = subparsers.add_parser("project-intent-summary")
        project_intent_summary_parser.add_argument("topic", nargs="+")

        project_goal_plan_parser = subparsers.add_parser("project-goal-plan")
        project_goal_plan_parser.add_argument("goal", nargs="+")

        sprint_intent_plan_parser = subparsers.add_parser("sprint-intent-plan")
        sprint_intent_plan_parser.add_argument("goal", nargs="+")

        project_next_action_candidates_parser = subparsers.add_parser("project-next-action-candidates")
        project_next_action_candidates_parser.add_argument("topic", nargs="+")

        subparsers.add_parser("project-intent-context")

        subparsers.add_parser("workspace-memory-link-status")
        subparsers.add_parser("workspace-memory-summary")

        workspace_memory_candidates_parser = subparsers.add_parser("workspace-memory-candidates")
        workspace_memory_candidates_parser.add_argument("target", nargs="+")

        workspace_file_memory_candidates_parser = subparsers.add_parser("workspace-file-memory-candidates")
        workspace_file_memory_candidates_parser.add_argument("target", nargs="+")

        workspace_milestone_memory_candidates_parser = subparsers.add_parser("workspace-milestone-memory-candidates")
        workspace_milestone_memory_candidates_parser.add_argument("target", nargs="+")

        subparsers.add_parser("workspace-memory-link-context")

        subparsers.add_parser("streaming-safety-status")

        streaming_context_plan_parser = subparsers.add_parser("streaming-context-plan")
        streaming_context_plan_parser.add_argument("target", nargs="+")

        streaming_chat_safety_plan_parser = subparsers.add_parser("streaming-chat-safety-plan")
        streaming_chat_safety_plan_parser.add_argument("target", nargs="+")

        streaming_content_boundary_plan_parser = subparsers.add_parser("streaming-content-boundary-plan")
        streaming_content_boundary_plan_parser.add_argument("target", nargs="+")

        streaming_privacy_plan_parser = subparsers.add_parser("streaming-privacy-plan")
        streaming_privacy_plan_parser.add_argument("target", nargs="+")

        streaming_moderation_plan_parser = subparsers.add_parser("streaming-moderation-plan")
        streaming_moderation_plan_parser.add_argument("target", nargs="+")

        subparsers.add_parser("streaming-safety-context")

        subparsers.add_parser("game-companion-status")

        game_session_plan_parser = subparsers.add_parser("game-session-plan")
        game_session_plan_parser.add_argument("target", nargs="+")

        game_strategy_plan_parser = subparsers.add_parser("game-strategy-plan")
        game_strategy_plan_parser.add_argument("target", nargs="+")

        game_streaming_plan_parser = subparsers.add_parser("game-streaming-plan")
        game_streaming_plan_parser.add_argument("target", nargs="+")

        game_coaching_plan_parser = subparsers.add_parser("game-coaching-plan")
        game_coaching_plan_parser.add_argument("target", nargs="+")

        subparsers.add_parser("game-context")

        subparsers.add_parser("expression-language-status")
        subparsers.add_parser("expression-state")

        expression_plan_parser = subparsers.add_parser("expression-plan")
        expression_plan_parser.add_argument("text", nargs="+")

        expression_voice_hint_parser = subparsers.add_parser("expression-voice-hint")
        expression_voice_hint_parser.add_argument("target", nargs="+")

        expression_avatar_hint_parser = subparsers.add_parser("expression-avatar-hint")
        expression_avatar_hint_parser.add_argument("target", nargs="+")

        expression_gesture_hint_parser = subparsers.add_parser("expression-gesture-hint")
        expression_gesture_hint_parser.add_argument("target", nargs="+")

        subparsers.add_parser("expression-context")

        subparsers.add_parser("media-understanding-status")
        subparsers.add_parser("media-asset-summary")

        media_image_plan_parser = subparsers.add_parser("media-image-plan")
        media_image_plan_parser.add_argument("goal", nargs="+")

        media_texture_reference_plan_parser = subparsers.add_parser("media-texture-reference-plan")
        media_texture_reference_plan_parser.add_argument("goal", nargs="+")

        media_thumbnail_review_plan_parser = subparsers.add_parser("media-thumbnail-review-plan")
        media_thumbnail_review_plan_parser.add_argument("goal", nargs="+")

        media_video_plan_parser = subparsers.add_parser("media-video-plan")
        media_video_plan_parser.add_argument("goal", nargs="+")

        subparsers.add_parser("media-context")

        subparsers.add_parser("blender-bridge-status")

        blender_scene_plan_parser = subparsers.add_parser("blender-scene-plan")
        blender_scene_plan_parser.add_argument("goal", nargs="+")

        blender_asset_plan_parser = subparsers.add_parser("blender-asset-plan")
        blender_asset_plan_parser.add_argument("goal", nargs="+")

        blender_texture_plan_parser = subparsers.add_parser("blender-texture-plan")
        blender_texture_plan_parser.add_argument("goal", nargs="+")

        blender_rigging_plan_parser = subparsers.add_parser("blender-rigging-plan")
        blender_rigging_plan_parser.add_argument("goal", nargs="+")

        blender_animation_plan_parser = subparsers.add_parser("blender-animation-plan")
        blender_animation_plan_parser.add_argument("goal", nargs="+")

        subparsers.add_parser("blender-context")

        subparsers.add_parser("workspace-status")
        subparsers.add_parser("workspace-awareness-status")
        subparsers.add_parser("workspace-map")
        subparsers.add_parser("workspace-context")
        subparsers.add_parser("workspace-current-state")
        subparsers.add_parser("workspace-important-files")

        subparsers.add_parser("partner-alpha-status")
        subparsers.add_parser("partner-context")
        subparsers.add_parser("partner-readiness")
        subparsers.add_parser("partner-next-step")

        subparsers.add_parser("awakening-status")
        subparsers.add_parser("awaken")

        subparsers.add_parser("voice-runtime-alpha-status")

        voice_speak_plan_parser = subparsers.add_parser("voice-speak-plan")
        voice_speak_plan_parser.add_argument("text", nargs="+")

        voice_speak_test_parser = subparsers.add_parser("voice-speak-test")
        voice_speak_test_parser.add_argument("text", nargs="+")

        subparsers.add_parser("voice-runtime-context")

        subparsers.add_parser("voice-runtime-status")
        subparsers.add_parser("voice-runtime-plan")
        subparsers.add_parser("voice-runtime-check")

        subparsers.add_parser("voice-status")
        subparsers.add_parser("voice-providers")

        subparsers.add_parser("project-code-status")

        project_code_map_parser = subparsers.add_parser("project-code-map")
        project_code_map_parser.add_argument("--limit", type=int, default=30)

        project_code_inspect_parser = subparsers.add_parser("project-code-inspect")
        project_code_inspect_parser.add_argument("path", type=str)

        project_code_plan_parser = subparsers.add_parser("project-code-plan")
        project_code_plan_parser.add_argument("request", type=str)

        project_code_safety_parser = subparsers.add_parser("project-code-safety")
        project_code_safety_parser.add_argument("command_text", type=str)

        project_map_parser = subparsers.add_parser("project-map")
        project_map_parser.add_argument("--depth", type=int, default=2)
        project_map_parser.add_argument("--limit", type=int, default=80)

        project_inspect_parser = subparsers.add_parser("project-inspect")
        project_inspect_parser.add_argument("relative_path", type=str)

        project_find_parser = subparsers.add_parser("project-find")
        project_find_parser.add_argument("keyword", type=str)
        project_find_parser.add_argument("--limit", type=int, default=30)

        subparsers.add_parser("project-summary")

        project_files_parser = subparsers.add_parser("project-files")
        project_files_parser.add_argument("--limit", type=int, default=50)

        project_read_parser = subparsers.add_parser("project-read")
        project_read_parser.add_argument("relative_path", type=str)

        action_request_parser = subparsers.add_parser("action-request")
        action_request_parser.add_argument("action", type=str)

        action_request_check_parser = subparsers.add_parser("action-request-check")
        action_request_check_parser.add_argument("action", type=str)

        subparsers.add_parser("plugin-actions")

        plugin_action_parser = subparsers.add_parser("plugin-action")
        plugin_action_parser.add_argument("name", type=str)

        plugin_action_check_parser = subparsers.add_parser("plugin-action-check")
        plugin_action_check_parser.add_argument("name", type=str)

        subparsers.add_parser("skills")

        skill_parser = subparsers.add_parser("skill")
        skill_parser.add_argument("name", type=str)

        skill_check_parser = subparsers.add_parser("skill-check")
        skill_check_parser.add_argument("name", type=str)

        subparsers.add_parser("permissions")

        permission_check_parser = subparsers.add_parser("permission-check")
        permission_check_parser.add_argument("action", type=str)

        perm_check_parser = subparsers.add_parser("perm-check")
        perm_check_parser.add_argument("action", type=str)

        subparsers.add_parser("provider")
        subparsers.add_parser("roles")
        subparsers.add_parser("reason")

        subparsers.add_parser("daily-briefing-status")

        daily_briefing_parser = subparsers.add_parser("daily-briefing")
        daily_briefing_parser.add_argument("--limit", type=int, default=6)

        daily_briefing_compact_parser = subparsers.add_parser("daily-briefing-compact")
        daily_briefing_compact_parser.add_argument("--limit", type=int, default=4)

        daily_briefing_context_parser = subparsers.add_parser("daily-briefing-context")
        daily_briefing_context_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("memory-reflection-status")

        memory_reflect_parser = subparsers.add_parser("memory-reflect")
        memory_reflect_parser.add_argument("--limit", type=int, default=8)

        memory_insights_parser = subparsers.add_parser("memory-insights")
        memory_insights_parser.add_argument("--limit", type=int, default=8)

        memory_reflection_context_parser = subparsers.add_parser("memory-reflection-context")
        memory_reflection_context_parser.add_argument("--limit", type=int, default=5)

        memory_delete_parser = subparsers.add_parser("memory-delete")
        memory_delete_parser.add_argument("memory_id", type=str)

        mem_delete_parser = subparsers.add_parser("mem-delete")
        mem_delete_parser.add_argument("memory_id", type=str)

        memory_pin_parser = subparsers.add_parser("memory-pin")
        memory_pin_parser.add_argument("memory_id", type=str)

        mem_pin_parser = subparsers.add_parser("mem-pin")
        mem_pin_parser.add_argument("memory_id", type=str)

        memory_unpin_parser = subparsers.add_parser("memory-unpin")
        memory_unpin_parser.add_argument("memory_id", type=str)

        mem_unpin_parser = subparsers.add_parser("mem-unpin")
        mem_unpin_parser.add_argument("memory_id", type=str)

        memory_importance_parser = subparsers.add_parser("memory-importance")
        memory_importance_parser.add_argument("memory_id", type=str)
        memory_importance_parser.add_argument("importance", type=int)

        mem_importance_parser = subparsers.add_parser("mem-importance")
        mem_importance_parser.add_argument("memory_id", type=str)
        mem_importance_parser.add_argument("importance", type=int)

        subparsers.add_parser("memory-pinned")
        subparsers.add_parser("mem-pinned")

        subparsers.add_parser("memory-count")
        subparsers.add_parser("mem-count")

        memory_list_parser = subparsers.add_parser("memory-list")
        memory_list_parser.add_argument("--limit", type=int, default=5)

        mem_list_parser = subparsers.add_parser("mem-list")
        mem_list_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("provider-check")
        subparsers.add_parser("reason-check")

        memory_search_parser = subparsers.add_parser("memory-search")
        memory_search_parser.add_argument("query", type=str)
        memory_search_parser.add_argument("--limit", type=int, default=5)

        mem_search_parser = subparsers.add_parser("mem-search")
        mem_search_parser.add_argument("query", type=str)
        mem_search_parser.add_argument("--limit", type=int, default=5)

        subparsers.add_parser("shell")

        return parser.parse_args(args)


    # Sprint 65.1 codebase compatibility CLI helpers.
    def print_codebase_compat_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<38}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<38}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<38}: {len(value)} field(s)")

        print()
        print("Safety Boundary")
        print("---------------")
        for key in [
            "read_only",
            "proposal_only",
            "metadata_only",
            "file_read",
            "file_write",
            "file_edit",
            "file_delete",
            "file_move",
            "file_copy",
            "command_execution",
            "git_commit",
            "git_push",
            "external_action_execution",
            "real_tool_execution",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<38}: {packet[key]}")

    def handle_codebase_compat_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general codebase change"
        project_root = self.project_root

        change_manager = CodebaseChangePlannerManager(project_root=project_root)
        patch_manager = CodebasePatchProposalRendererManager(project_root=project_root)
        validation_manager = CodebaseValidationGatePlannerManager(project_root=project_root)

        if command == "codebase-change-status":
            self.print_codebase_compat_packet("AURA Codebase Change Planner Status", change_manager.status())
            return True

        if command == "codebase-change-plan":
            self.print_codebase_compat_packet("AURA Codebase Change Plan", change_manager.change_intent_plan(target))
            return True

        if command == "codebase-impact-review":
            self.print_codebase_compat_packet("AURA Codebase Impact Review", change_manager.change_impact_plan(target))
            return True

        if command == "codebase-patch-proposal-status":
            self.print_codebase_compat_packet("AURA Codebase Patch Proposal Renderer Status", patch_manager.status())
            return True

        if command == "codebase-patch-proposal":
            self.print_codebase_compat_packet("AURA Codebase Patch Proposal", patch_manager.render_proposal(target))
            return True

        if command == "codebase-patch-safety-packet":
            packet = patch_manager.render_proposal(target)
            packet["compatibility_view"] = "safety_packet"
            self.print_codebase_compat_packet("AURA Codebase Patch Safety Packet", packet)
            return True

        if command == "codebase-validation-gate-status":
            self.print_codebase_compat_packet("AURA Codebase Validation Gate Planner Status", validation_manager.status())
            return True

        if command == "codebase-validation-gate-plan":
            self.print_codebase_compat_packet("AURA Codebase Validation Gate Plan", validation_manager.validation_gate_plan(target))
            return True

        if command == "codebase-validation-preflight-gate":
            self.print_codebase_compat_packet("AURA Codebase Validation Preflight Gate", validation_manager.preflight_gate(target))
            return True

        return False


    # Sprint 66.0 voice conversation compatibility CLI helpers.
    def print_voice_conversation_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<42}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<42}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<42}: {len(value)} field(s)")

        print()
        print("Voice Safety Boundary")
        print("---------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "microphone_access",
            "speaker_output",
            "tts_runtime_output",
            "audio_recording",
            "wake_word_runtime",
            "voice_command_execution",
            "desktop_action_execution",
            "app_opened",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<42}: {packet[key]}")

    def handle_voice_conversation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general voice conversation"
        manager = VoiceConversationPlannerManager(project_root=self.project_root)

        if command == "voice-conversation-status":
            self.print_voice_conversation_packet("AURA Voice Conversation Planner Status", manager.status())
            return True

        if command == "voice-intent-plan":
            self.print_voice_conversation_packet("AURA Voice Intent Plan", manager.voice_intent_plan(target))
            return True

        if command == "voice-response-plan":
            self.print_voice_conversation_packet("AURA Voice Response Plan", manager.voice_response_plan(target))
            return True

        if command == "voice-turn-plan":
            self.print_voice_conversation_packet("AURA Voice Conversation Turn Plan", manager.conversation_turn_plan(target))
            return True

        if command == "voice-safety-plan":
            self.print_voice_conversation_packet("AURA Voice Safety Plan", manager.voice_safety_plan(target))
            return True

        if command == "voice-conversation-context":
            self.print_voice_conversation_packet("AURA Voice Conversation Planner Context", manager.context())
            return True

        return False


    # Sprint 67.0 vision context compatibility CLI helpers.
    def print_vision_context_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<44}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<44}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<44}: {len(value)} field(s)")

        print()
        print("Vision Safety Boundary")
        print("----------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "screen_capture",
            "camera_access",
            "image_open",
            "image_read",
            "video_capture",
            "ocr_runtime",
            "visual_recognition_runtime",
            "desktop_action_execution",
            "app_opened",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<44}: {packet[key]}")

    def handle_vision_context_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general vision context"
        manager = VisionContextPlannerManager(project_root=self.project_root)

        if command == "vision-context-status":
            self.print_vision_context_packet("AURA Vision Context Planner Status", manager.status())
            return True

        if command == "visual-context-plan":
            self.print_vision_context_packet("AURA Visual Context Plan", manager.visual_context_plan(target))
            return True

        if command == "screen-context-plan":
            self.print_vision_context_packet("AURA Screen Context Plan", manager.screen_context_plan(target))
            return True

        if command == "camera-context-plan":
            self.print_vision_context_packet("AURA Camera Context Plan", manager.camera_context_plan(target))
            return True

        if command == "vision-safety-plan":
            self.print_vision_context_packet("AURA Vision Safety Plan", manager.vision_safety_plan(target))
            return True

        if command == "vision-context":
            self.print_vision_context_packet("AURA Vision Context Planner Context", manager.context())
            return True

        return False


    # Sprint 68.0 avatar interaction compatibility CLI helpers.
    def print_avatar_interaction_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {len(value)} field(s)")

        print()
        print("Avatar Safety Boundary")
        print("----------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "avatar_rendering",
            "animation_playback",
            "mocap_runtime",
            "camera_tracking",
            "face_tracking",
            "body_tracking",
            "rig_manipulation",
            "blendshape_control",
            "bone_control",
            "blender_execution",
            "obs_control",
            "desktop_action_execution",
            "app_opened",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {packet[key]}")

    def handle_avatar_interaction_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general avatar interaction"
        manager = AvatarInteractionPlannerManager(project_root=self.project_root)

        if command == "avatar-interaction-status":
            self.print_avatar_interaction_packet("AURA Avatar Interaction Planner Status", manager.status())
            return True

        if command == "avatar-expression-plan":
            self.print_avatar_interaction_packet("AURA Avatar Expression Plan", manager.avatar_expression_plan(target))
            return True

        if command == "avatar-gesture-plan":
            self.print_avatar_interaction_packet("AURA Avatar Gesture Plan", manager.avatar_gesture_plan(target))
            return True

        if command == "avatar-pose-plan":
            self.print_avatar_interaction_packet("AURA Avatar Pose Plan", manager.avatar_pose_plan(target))
            return True

        if command == "avatar-streaming-presence-plan":
            self.print_avatar_interaction_packet("AURA Avatar Streaming Presence Plan", manager.avatar_streaming_presence_plan(target))
            return True

        if command == "avatar-safety-plan":
            self.print_avatar_interaction_packet("AURA Avatar Safety Plan", manager.avatar_safety_plan(target))
            return True

        if command == "avatar-interaction-context":
            self.print_avatar_interaction_packet("AURA Avatar Interaction Planner Context", manager.context())
            return True

        return False


    # Sprint 69.0 desktop workflow compatibility CLI helpers.
    def print_desktop_workflow_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {len(value)} field(s)")

        print()
        print("Desktop Safety Boundary")
        print("-----------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "desktop_control",
            "app_opening",
            "window_inspection",
            "window_control",
            "mouse_control",
            "keyboard_control",
            "screen_capture",
            "clipboard_access",
            "notification_access",
            "process_inspection",
            "file_read",
            "file_write",
            "command_execution",
            "external_action_execution",
            "real_tool_execution",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<46}: {packet[key]}")

    def handle_desktop_workflow_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general desktop workflow"
        manager = DesktopWorkflowPlannerManager(project_root=self.project_root)

        if command == "desktop-workflow-status":
            self.print_desktop_workflow_packet("AURA Desktop Workflow Planner Status", manager.status())
            return True

        if command == "desktop-workflow-plan":
            self.print_desktop_workflow_packet("AURA Desktop Workflow Plan", manager.desktop_workflow_plan(target))
            return True

        if command == "desktop-app-context-plan":
            self.print_desktop_workflow_packet("AURA Desktop App Context Plan", manager.desktop_app_context_plan(target))
            return True

        if command == "desktop-window-flow-plan":
            self.print_desktop_workflow_packet("AURA Desktop Window Flow Plan", manager.desktop_window_flow_plan(target))
            return True

        if command == "desktop-task-sequence-plan":
            self.print_desktop_workflow_packet("AURA Desktop Task Sequence Plan", manager.desktop_task_sequence_plan(target))
            return True

        if command == "desktop-safety-plan":
            self.print_desktop_workflow_packet("AURA Desktop Safety Plan", manager.desktop_safety_plan(target))
            return True

        if command == "desktop-workflow-context":
            self.print_desktop_workflow_packet("AURA Desktop Workflow Planner Context", manager.context())
            return True

        return False


    # Sprint 70.0 partner runtime compatibility CLI helpers.
    def print_partner_runtime_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Partner Runtime Safety Boundary")
        print("-------------------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "autonomous_runtime",
            "background_agent_loop",
            "scheduled_self_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "desktop_control",
            "app_opening",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "network_action",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_partner_runtime_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general partner runtime planning"
        manager = PartnerRuntimePlanningManager(project_root=self.project_root)

        if command == "partner-runtime-status":
            self.print_partner_runtime_packet("AURA Partner Runtime Planning Layer Status", manager.status())
            return True

        if command == "partner-runtime-mode-plan":
            self.print_partner_runtime_packet("AURA Partner Runtime Mode Plan", manager.partner_runtime_mode_plan(target))
            return True

        if command == "partner-session-plan":
            self.print_partner_runtime_packet("AURA Partner Session Plan", manager.partner_session_plan(target))
            return True

        if command == "partner-multimodal-handoff-plan":
            self.print_partner_runtime_packet("AURA Partner Multimodal Handoff Plan", manager.partner_multimodal_handoff_plan(target))
            return True

        if command == "partner-tool-permission-plan":
            self.print_partner_runtime_packet("AURA Partner Tool Permission Plan", manager.partner_tool_permission_plan(target))
            return True

        if command == "partner-growth-cycle-plan":
            self.print_partner_runtime_packet("AURA Partner Growth Cycle Plan", manager.partner_growth_cycle_plan(target))
            return True

        if command == "partner-runtime-safety-plan":
            self.print_partner_runtime_packet("AURA Partner Runtime Safety Plan", manager.partner_runtime_safety_plan(target))
            return True

        if command == "partner-runtime-context":
            self.print_partner_runtime_packet("AURA Partner Runtime Planning Layer Context", manager.context())
            return True

        return False


    # Sprint 71.0 thought loop compatibility CLI helpers.
    def print_thought_loop_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Thought Loop Safety Boundary")
        print("----------------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "autonomous_thought_loop",
            "background_loop",
            "continuous_self_prompting",
            "self_triggered_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "app_opening",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_thought_loop_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general thought loop planning"
        manager = ThoughtLoopPlannerManager(project_root=self.project_root)

        if command == "thought-loop-status":
            self.print_thought_loop_packet("AURA Thought Loop Planner Status", manager.status())
            return True

        if command == "thought-cycle-plan":
            self.print_thought_loop_packet("AURA Thought Cycle Plan", manager.thought_cycle_plan(target))
            return True

        if command == "intent-frame-plan":
            self.print_thought_loop_packet("AURA Intent Frame Plan", manager.intent_frame_plan(target))
            return True

        if command == "reasoning-summary-plan":
            self.print_thought_loop_packet("AURA Reasoning Summary Plan", manager.reasoning_summary_plan(target))
            return True

        if command == "uncertainty-review-plan":
            self.print_thought_loop_packet("AURA Uncertainty Review Plan", manager.uncertainty_review_plan(target))
            return True

        if command == "action-readiness-review":
            self.print_thought_loop_packet("AURA Action Readiness Review", manager.action_readiness_review(target))
            return True

        if command == "growth-memory-review":
            self.print_thought_loop_packet("AURA Growth Memory Review", manager.growth_memory_review(target))
            return True

        if command == "thought-safety-plan":
            self.print_thought_loop_packet("AURA Thought Safety Plan", manager.thought_safety_plan(target))
            return True

        if command == "thought-loop-context":
            self.print_thought_loop_packet("AURA Thought Loop Planner Context", manager.context())
            return True

        return False


    # Sprint 72.0 reasoning context compatibility CLI helpers.
    def print_reasoning_context_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} field(s)")

        print()
        print("Reasoning Context Safety Boundary")
        print("---------------------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "hidden_chain_of_thought_exposed",
            "private_reasoning_disclosed",
            "autonomous_reasoning_loop",
            "background_reasoning_loop",
            "self_triggered_action",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "file_read",
            "file_write",
            "command_execution",
            "desktop_control",
            "screen_capture",
            "camera_access",
            "microphone_access",
            "speaker_output",
            "avatar_rendering",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {packet[key]}")

    def handle_reasoning_context_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general reasoning context"
        manager = ReasoningContextManager(project_root=self.project_root)

        if command == "reasoning-context-status":
            self.print_reasoning_context_packet("AURA Reasoning Context Manager Status", manager.status())
            return True

        if command == "reasoning-context-plan":
            self.print_reasoning_context_packet("AURA Reasoning Context Plan", manager.reasoning_context_plan(target))
            return True

        if command == "fact-assumption-plan":
            self.print_reasoning_context_packet("AURA Fact Assumption Plan", manager.fact_assumption_plan(target))
            return True

        if command == "unknowns-review-plan":
            self.print_reasoning_context_packet("AURA Unknowns Review Plan", manager.unknowns_review_plan(target))
            return True

        if command == "evidence-boundary-plan":
            self.print_reasoning_context_packet("AURA Evidence Boundary Plan", manager.evidence_boundary_plan(target))
            return True

        if command == "decision-frame-plan":
            self.print_reasoning_context_packet("AURA Decision Frame Plan", manager.decision_frame_plan(target))
            return True

        if command == "response-strategy-plan":
            self.print_reasoning_context_packet("AURA Response Strategy Plan", manager.response_strategy_plan(target))
            return True

        if command == "reasoning-safety-plan":
            self.print_reasoning_context_packet("AURA Reasoning Safety Plan", manager.reasoning_safety_plan(target))
            return True

        if command == "reasoning-context":
            self.print_reasoning_context_packet("AURA Reasoning Context Manager Context", manager.context())
            return True

        return False


    # Sprint 73.0 knowledge uncertainty compatibility CLI helpers.
    def print_knowledge_uncertainty_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Knowledge Uncertainty Safety Boundary")
        print("-------------------------------------")
        for key in [
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "internet_search",
            "web_request",
            "source_fetch",
            "browser_opening",
            "network_action",
            "download_execution",
            "file_download",
            "dependency_install",
            "package_install",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "memory_write",
            "background_monitoring",
            "autonomous_search",
            "fabricated_answer",
            "fabricated_source",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_knowledge_uncertainty_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general knowledge uncertainty gate"
        manager = KnowledgeUncertaintyGateManager(project_root=self.project_root)

        if command == "knowledge-uncertainty-status":
            self.print_knowledge_uncertainty_packet("AURA Knowledge Uncertainty Gate Status", manager.status())
            return True

        if command == "knowledge-gap-plan":
            self.print_knowledge_uncertainty_packet("AURA Knowledge Gap Plan", manager.knowledge_gap_plan(target))
            return True

        if command == "knowledge-uncertainty-review-plan":
            self.print_knowledge_uncertainty_packet("AURA Knowledge Uncertainty Review Plan", manager.uncertainty_review_plan(target))
            return True

        if command == "internet-search-gate-plan":
            self.print_knowledge_uncertainty_packet("AURA Internet Search Gate Plan", manager.internet_search_gate_plan(target))
            return True

        if command == "source-requirement-plan":
            self.print_knowledge_uncertainty_packet("AURA Source Requirement Plan", manager.source_requirement_plan(target))
            return True

        if command == "download-requirement-plan":
            self.print_knowledge_uncertainty_packet("AURA Download Requirement Plan", manager.download_requirement_plan(target))
            return True

        if command == "answer-confidence-plan":
            self.print_knowledge_uncertainty_packet("AURA Answer Confidence Plan", manager.answer_confidence_plan(target))
            return True

        if command == "knowledge-safety-plan":
            self.print_knowledge_uncertainty_packet("AURA Knowledge Safety Plan", manager.knowledge_safety_plan(target))
            return True

        if command == "knowledge-uncertainty-context":
            self.print_knowledge_uncertainty_packet("AURA Knowledge Uncertainty Gate Context", manager.context())
            return True

        return False


    # Sprint 74.0 voice input compatibility CLI helpers.
    def print_voice_input_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Voice Input Safety Boundary")
        print("---------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "microphone_access",
            "audio_recording",
            "audio_capture",
            "speech_to_text_runtime",
            "speech_transcription",
            "wake_word_detection",
            "always_listening",
            "background_listening",
            "voice_command_execution",
            "voice_tool_execution",
            "speaker_output",
            "tts_runtime",
            "network_stt",
            "cloud_stt",
            "file_read",
            "file_write",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_voice_input_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general voice input foundation"
        manager = VoiceInputRuntimeFoundationManager(project_root=self.project_root)

        if command == "voice-input-status":
            self.print_voice_input_packet("AURA Voice Input Runtime Foundation Status", manager.status())
            return True

        if command == "voice-input-permission-plan":
            self.print_voice_input_packet("AURA Voice Input Permission Plan", manager.voice_input_permission_plan(target))
            return True

        if command == "voice-capture-boundary-plan":
            self.print_voice_input_packet("AURA Voice Capture Boundary Plan", manager.voice_capture_boundary_plan(target))
            return True

        if command == "speech-to-text-adapter-plan":
            self.print_voice_input_packet("AURA Speech To Text Adapter Plan", manager.speech_to_text_adapter_plan(target))
            return True

        if command == "voice-intent-gate-plan":
            self.print_voice_input_packet("AURA Voice Intent Gate Plan", manager.voice_intent_gate_plan(target))
            return True

        if command == "voice-command-confirmation-plan":
            self.print_voice_input_packet("AURA Voice Command Confirmation Plan", manager.voice_command_confirmation_plan(target))
            return True

        if command == "voice-session-plan":
            self.print_voice_input_packet("AURA Voice Session Plan", manager.voice_session_plan(target))
            return True

        if command == "voice-input-safety-plan":
            self.print_voice_input_packet("AURA Voice Input Safety Plan", manager.voice_input_safety_plan(target))
            return True

        if command == "voice-input-context":
            self.print_voice_input_packet("AURA Voice Input Runtime Foundation Context", manager.context())
            return True

        return False


    # Sprint 75.0 voice intent compatibility CLI helpers.
    def print_voice_intent_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Voice Intent Safety Boundary")
        print("----------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "microphone_access",
            "audio_recording",
            "audio_capture",
            "speech_to_text_runtime",
            "speech_transcription",
            "wake_word_detection",
            "always_listening",
            "background_listening",
            "voice_command_execution",
            "voice_tool_execution",
            "action_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_voice_intent_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general voice intent understanding"
        manager = VoiceIntentUnderstandingManager(project_root=self.project_root)

        if command == "voice-intent-status":
            self.print_voice_intent_packet("AURA Voice Intent Understanding Status", manager.status())
            return True

        if command == "voice-transcript-normalization-plan":
            self.print_voice_intent_packet("AURA Voice Transcript Normalization Plan", manager.voice_transcript_normalization_plan(target))
            return True

        if command == "voice-intent-classification-plan":
            self.print_voice_intent_packet("AURA Voice Intent Classification Plan", manager.voice_intent_classification_plan(target))
            return True

        if command == "voice-entity-slot-plan":
            self.print_voice_intent_packet("AURA Voice Entity Slot Plan", manager.voice_entity_slot_plan(target))
            return True

        if command == "voice-clarification-plan":
            self.print_voice_intent_packet("AURA Voice Clarification Plan", manager.voice_clarification_plan(target))
            return True

        if command == "voice-action-gate-plan":
            self.print_voice_intent_packet("AURA Voice Action Gate Plan", manager.voice_action_gate_plan(target))
            return True

        if command == "voice-response-plan":
            self.print_voice_intent_packet("AURA Voice Response Plan", manager.voice_response_plan(target))
            return True

        if command == "voice-intent-safety-plan":
            self.print_voice_intent_packet("AURA Voice Intent Safety Plan", manager.voice_intent_safety_plan(target))
            return True

        if command == "voice-intent-context":
            self.print_voice_intent_packet("AURA Voice Intent Understanding Context", manager.context())
            return True

        return False


    # Sprint 76.0 vision input compatibility CLI helpers.
    def print_vision_input_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {len(value)} field(s)")

        print()
        print("Vision Input Safety Boundary")
        print("----------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "camera_access",
            "screen_capture",
            "screenshot_capture",
            "image_capture",
            "video_capture",
            "webcam_runtime",
            "vision_runtime",
            "image_analysis_runtime",
            "object_detection_runtime",
            "ocr_runtime",
            "always_watching",
            "background_watching",
            "visual_command_execution",
            "visual_tool_execution",
            "action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<48}: {packet[key]}")

    def handle_vision_input_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general vision input foundation"
        manager = VisionInputRuntimeFoundationManager(project_root=self.project_root)

        if command == "vision-input-status":
            self.print_vision_input_packet("AURA Vision Input Runtime Foundation Status", manager.status())
            return True

        if command == "vision-input-permission-plan":
            self.print_vision_input_packet("AURA Vision Input Permission Plan", manager.vision_input_permission_plan(target))
            return True

        if command == "visual-capture-boundary-plan":
            self.print_vision_input_packet("AURA Visual Capture Boundary Plan", manager.visual_capture_boundary_plan(target))
            return True

        if command == "image-input-adapter-plan":
            self.print_vision_input_packet("AURA Image Input Adapter Plan", manager.image_input_adapter_plan(target))
            return True

        if command == "visual-source-plan":
            self.print_vision_input_packet("AURA Visual Source Plan", manager.visual_source_plan(target))
            return True

        if command == "visual-session-plan":
            self.print_vision_input_packet("AURA Visual Session Plan", manager.visual_session_plan(target))
            return True

        if command == "visual-action-gate-plan":
            self.print_vision_input_packet("AURA Visual Action Gate Plan", manager.visual_action_gate_plan(target))
            return True

        if command == "vision-input-safety-plan":
            self.print_vision_input_packet("AURA Vision Input Safety Plan", manager.vision_input_safety_plan(target))
            return True

        if command == "vision-input-context":
            self.print_vision_input_packet("AURA Vision Input Runtime Foundation Context", manager.context())
            return True

        return False


    # Sprint 77.0 visual context compatibility CLI helpers.
    def print_visual_context_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} field(s)")

        print()
        print("Visual Context Safety Boundary")
        print("------------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "camera_access",
            "screen_capture",
            "screenshot_capture",
            "image_capture",
            "video_capture",
            "webcam_runtime",
            "vision_runtime",
            "visual_context_runtime",
            "image_analysis_runtime",
            "object_detection_runtime",
            "ocr_runtime",
            "image_text_extraction_runtime",
            "face_recognition",
            "biometric_identification",
            "identity_recognition",
            "emotion_inference_from_face",
            "always_watching",
            "background_watching",
            "visual_command_execution",
            "visual_tool_execution",
            "action_execution",
            "file_read",
            "file_write",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {packet[key]}")

    def handle_visual_context_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general visual context understanding"
        manager = VisualContextUnderstandingManager(project_root=self.project_root)

        if command == "visual-context-status":
            self.print_visual_context_packet("AURA Visual Context Understanding Status", manager.status())
            return True

        if command == "visual-scene-understanding-plan":
            self.print_visual_context_packet("AURA Visual Scene Understanding Plan", manager.visual_scene_understanding_plan(target))
            return True

        if command == "visual-object-relation-plan":
            self.print_visual_context_packet("AURA Visual Object Relation Plan", manager.visual_object_relation_plan(target))
            return True

        if command == "visual-text-context-plan":
            self.print_visual_context_packet("AURA Visual Text Context Plan", manager.visual_text_context_plan(target))
            return True

        if command == "visual-uncertainty-plan":
            self.print_visual_context_packet("AURA Visual Uncertainty Plan", manager.visual_uncertainty_plan(target))
            return True

        if command == "visual-clarification-plan":
            self.print_visual_context_packet("AURA Visual Clarification Plan", manager.visual_clarification_plan(target))
            return True

        if command == "visual-response-context-plan":
            self.print_visual_context_packet("AURA Visual Response Context Plan", manager.visual_response_context_plan(target))
            return True

        if command == "visual-context-safety-plan":
            self.print_visual_context_packet("AURA Visual Context Safety Plan", manager.visual_context_safety_plan(target))
            return True

        if command == "visual-context":
            self.print_visual_context_packet("AURA Visual Context Understanding Context", manager.context())
            return True

        return False


    # Sprint 78.0 coder project compatibility CLI helpers.
    def print_coder_project_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {len(value)} field(s)")

        print()
        print("Coder Project Safety Boundary")
        print("-----------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "generation_ready",
            "execution_ready",
            "project_creation_runtime",
            "project_files_written",
            "directory_creation",
            "file_read",
            "file_write",
            "file_delete",
            "file_modify",
            "code_generation_runtime",
            "code_execution",
            "test_execution",
            "command_execution",
            "dependency_install",
            "package_download",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "memory_write",
            "internet_search",
            "network_action",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<52}: {packet[key]}")

    def handle_coder_project_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general coder project generation"
        manager = CoderProjectGenerationPlannerManager(project_root=self.project_root)

        if command == "coder-project-status":
            self.print_coder_project_packet("AURA Coder Project Generation Planner Status", manager.status())
            return True

        if command == "project-request-frame-plan":
            self.print_coder_project_packet("AURA Project Request Frame Plan", manager.project_request_frame_plan(target))
            return True

        if command == "project-structure-plan":
            self.print_coder_project_packet("AURA Project Structure Plan", manager.project_structure_plan(target))
            return True

        if command == "code-file-blueprint-plan":
            self.print_coder_project_packet("AURA Code File Blueprint Plan", manager.code_file_blueprint_plan(target))
            return True

        if command == "dependency-plan":
            self.print_coder_project_packet("AURA Dependency Plan", manager.dependency_plan(target))
            return True

        if command == "generation-review-gate-plan":
            self.print_coder_project_packet("AURA Generation Review Gate Plan", manager.generation_review_gate_plan(target))
            return True

        if command == "validation-strategy-plan":
            self.print_coder_project_packet("AURA Validation Strategy Plan", manager.validation_strategy_plan(target))
            return True

        if command == "project-generation-safety-plan":
            self.print_coder_project_packet("AURA Project Generation Safety Plan", manager.project_generation_safety_plan(target))
            return True

        if command == "coder-project-context":
            self.print_coder_project_packet("AURA Coder Project Generation Planner Context", manager.context())
            return True

        return False


    # Sprint 79.0 dependency permission compatibility CLI helpers.
    def print_dependency_permission_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {len(value)} field(s)")

        print()
        print("Dependency Permission Safety Boundary")
        print("-------------------------------------")
        for key in [
            "foundation_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "permission_ready",
            "execution_ready",
            "dependency_install",
            "package_download",
            "model_download",
            "asset_download",
            "installer_download",
            "binary_download",
            "network_action",
            "internet_search",
            "package_manager_runtime",
            "dependency_resolution_runtime",
            "download_runtime",
            "install_runtime",
            "pip_execution",
            "npm_execution",
            "apt_execution",
            "uv_execution",
            "poetry_execution",
            "shell_execution",
            "command_execution",
            "tool_execution",
            "real_tool_execution",
            "external_action_execution",
            "external_binary_execution",
            "file_read",
            "file_write",
            "file_modify",
            "file_delete",
            "memory_write",
            "desktop_control",
            "git_init",
            "git_add",
            "git_commit",
            "git_push",
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {packet[key]}")

    def handle_dependency_permission_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "general dependency download permission"
        manager = DependencyDownloadPermissionGateManager(project_root=self.project_root)

        if command == "dependency-permission-status":
            self.print_dependency_permission_packet("AURA Dependency Download Permission Gate Status", manager.status())
            return True

        if command == "dependency-request-review-plan":
            self.print_dependency_permission_packet("AURA Dependency Request Review Plan", manager.dependency_request_review_plan(target))
            return True

        if command == "package-source-review-plan":
            self.print_dependency_permission_packet("AURA Package Source Review Plan", manager.package_source_review_plan(target))
            return True

        if command == "download-permission-plan":
            self.print_dependency_permission_packet("AURA Download Permission Plan", manager.download_permission_plan(target))
            return True

        if command == "install-command-review-plan":
            self.print_dependency_permission_packet("AURA Install Command Review Plan", manager.install_command_review_plan(target))
            return True

        if command == "dependency-risk-plan":
            self.print_dependency_permission_packet("AURA Dependency Risk Plan", manager.dependency_risk_plan(target))
            return True

        if command == "offline-alternative-plan":
            self.print_dependency_permission_packet("AURA Offline Alternative Plan", manager.offline_alternative_plan(target))
            return True

        if command == "dependency-permission-safety-plan":
            self.print_dependency_permission_packet("AURA Dependency Permission Safety Plan", manager.dependency_permission_safety_plan(target))
            return True

        if command == "dependency-permission-context":
            self.print_dependency_permission_packet("AURA Dependency Download Permission Gate Context", manager.context())
            return True

        return False


    # Sprint 80.0 checkpoint compatibility CLI helpers.
    def print_checkpoint_80_packet(self, title: str, packet: dict) -> None:
        print(title)
        print("=" * len(title))

        for key, value in packet.items():
            if isinstance(value, (str, int, bool)) or value is None:
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {value}")
            elif isinstance(value, list):
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {len(value)} item(s)")
            elif isinstance(value, dict):
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {len(value)} field(s)")

        print()
        print("Checkpoint 71-80 Safety Boundary")
        print("--------------------------------")
        for key in [
            "checkpoint_only",
            "review_only",
            "planner_only",
            "proposal_only",
            "metadata_only",
            "runtime_ready",
            "execution_ready",
            "runtime_behavior_change",
            "automatic_stabilization",
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
        ]:
            if key in packet:
                label = key.replace("_", " ").title()
                print(f"{label:<56}: {packet[key]}")

    def handle_checkpoint_80_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "Sprint 71-80 checkpoint review"
        manager = ReviewStabilization7180Manager(project_root=self.project_root)

        if command == "checkpoint-80-status":
            self.print_checkpoint_80_packet("AURA Sprint 71-80 Review & Stabilization Status", manager.status())
            return True

        if command == "completed-feature-review-plan":
            self.print_checkpoint_80_packet("AURA Completed Feature Review Plan", manager.completed_feature_review_plan(target))
            return True

        if command == "active-foundation-review-plan":
            self.print_checkpoint_80_packet("AURA Active Foundation Review Plan", manager.active_foundation_review_plan(target))
            return True

        if command == "safety-boundary-review-plan":
            self.print_checkpoint_80_packet("AURA Safety Boundary Review Plan", manager.safety_boundary_review_plan(target))
            return True

        if command == "stabilization-validation-plan":
            self.print_checkpoint_80_packet("AURA Stabilization Validation Plan", manager.stabilization_validation_plan(target))
            return True

        if command == "technical-debt-review-plan":
            self.print_checkpoint_80_packet("AURA Technical Debt Review Plan", manager.technical_debt_review_plan(target))
            return True

        if command == "roadmap-gap-review-plan":
            self.print_checkpoint_80_packet("AURA Roadmap Gap Review Plan", manager.roadmap_gap_review_plan(target))
            return True

        if command == "next-block-planning-plan":
            self.print_checkpoint_80_packet("AURA Next Block Planning Plan", manager.next_block_planning_plan(target))
            return True

        if command == "checkpoint-80-context":
            self.print_checkpoint_80_packet("AURA Sprint 71-80 Checkpoint Context", manager.context())
            return True

        return False


    # Sprint 81.0 shared output formatter CLI helpers.
    def print_output_formatter_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet))

    def handle_output_formatter_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "shared AURA output formatting"
        manager = SharedOutputFormatterManager()

        if command == "output-formatter-status":
            self.print_output_formatter_packet("AURA Shared Output Formatter Status", manager.status())
            return True

        if command == "packet-render-plan":
            self.print_output_formatter_packet("AURA Packet Render Plan", manager.packet_render_plan(target))
            return True

        if command == "safety-boundary-render-plan":
            self.print_output_formatter_packet("AURA Safety Boundary Render Plan", manager.safety_boundary_render_plan(target))
            return True

        if command == "cli-output-format-plan":
            self.print_output_formatter_packet("AURA CLI Output Format Plan", manager.cli_output_format_plan(target))
            return True

        if command == "shell-output-format-plan":
            self.print_output_formatter_packet("AURA Shell Output Format Plan", manager.shell_output_format_plan(target))
            return True

        if command == "console-output-format-plan":
            self.print_output_formatter_packet("AURA Console Output Format Plan", manager.console_output_format_plan(target))
            return True

        if command == "ui-output-contract-plan":
            self.print_output_formatter_packet("AURA UI Output Contract Plan", manager.ui_output_contract_plan(target))
            return True

        if command == "formatter-migration-plan":
            self.print_output_formatter_packet("AURA Formatter Migration Plan", manager.formatter_migration_plan(target))
            return True

        if command == "output-formatter-context":
            self.print_output_formatter_packet("AURA Shared Output Formatter Context", manager.context())
            return True

        return False


    # Sprint 82.0 capability registry CLI helpers.
    def print_capability_registry_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Capability Registry Safety Boundary"))

    def handle_capability_registry_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA capability registry"
        manager = CapabilityRegistryManager()

        if command == "capability-registry-status":
            self.print_capability_registry_packet("AURA Capability Registry Status", manager.status())
            return True

        if command == "capability-catalog-plan":
            self.print_capability_registry_packet("AURA Capability Catalog Plan", manager.capability_catalog_plan(target))
            return True

        if command == "capability-state-review-plan":
            self.print_capability_registry_packet("AURA Capability State Review Plan", manager.capability_state_review_plan(target))
            return True

        if command == "permission-requirement-review-plan":
            self.print_capability_registry_packet("AURA Permission Requirement Review Plan", manager.permission_requirement_review_plan(target))
            return True

        if command == "risk-level-review-plan":
            self.print_capability_registry_packet("AURA Risk Level Review Plan", manager.risk_level_review_plan(target))
            return True

        if command == "control-center-capability-view-plan":
            self.print_capability_registry_packet("AURA Control Center Capability View Plan", manager.control_center_capability_view_plan(target))
            return True

        if command == "capability-gap-review-plan":
            self.print_capability_registry_packet("AURA Capability Gap Review Plan", manager.capability_gap_review_plan(target))
            return True

        if command == "capability-registry-migration-plan":
            self.print_capability_registry_packet("AURA Capability Registry Migration Plan", manager.capability_registry_migration_plan(target))
            return True

        if command == "capability-registry-context":
            self.print_capability_registry_packet("AURA Capability Registry Context", manager.context())
            return True

        return False


    # Sprint 83.0 unified permission workflow CLI helpers.
    def print_permission_workflow_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Workflow Safety Boundary"))

    def handle_permission_workflow_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA permission workflow"
        manager = UnifiedPermissionWorkflowManager()

        if command == "permission-workflow-status":
            self.print_permission_workflow_packet("AURA Unified Permission Workflow Status", manager.status())
            return True

        if command == "permission-request-plan":
            self.print_permission_workflow_packet("AURA Permission Request Plan", manager.permission_request_plan(target))
            return True

        if command == "permission-state-transition-plan":
            self.print_permission_workflow_packet("AURA Permission State Transition Plan", manager.permission_state_transition_plan(target))
            return True

        if command == "permission-risk-review-plan":
            self.print_permission_workflow_packet("AURA Permission Risk Review Plan", manager.permission_risk_review_plan(target))
            return True

        if command == "confirmation-prompt-plan":
            self.print_permission_workflow_packet("AURA Confirmation Prompt Plan", manager.confirmation_prompt_plan(target))
            return True

        if command == "permission-audit-trail-plan":
            self.print_permission_workflow_packet("AURA Permission Audit Trail Plan", manager.permission_audit_trail_plan(target))
            return True

        if command == "control-center-permission-view-plan":
            self.print_permission_workflow_packet("AURA Control Center Permission View Plan", manager.control_center_permission_view_plan(target))
            return True

        if command == "permission-policy-gap-review-plan":
            self.print_permission_workflow_packet("AURA Permission Policy Gap Review Plan", manager.permission_policy_gap_review_plan(target))
            return True

        if command == "permission-workflow-context":
            self.print_permission_workflow_packet("AURA Unified Permission Workflow Context", manager.context())
            return True

        return False


    # Sprint 84.0 runtime service foundation CLI helpers.
    def print_runtime_service_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Service Safety Boundary"))

    def handle_runtime_service_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime service foundation"
        manager = AuraRuntimeServiceFoundationManager(project_root=self.project_root)

        if command == "runtime-service-status":
            self.print_runtime_service_packet("AURA Runtime Service Foundation Status", manager.status())
            return True

        if command == "safe-idle-boot-plan":
            self.print_runtime_service_packet("AURA Safe Idle Boot Plan", manager.safe_idle_boot_plan(target))
            return True

        if command == "service-lifecycle-plan":
            self.print_runtime_service_packet("AURA Service Lifecycle Plan", manager.service_lifecycle_plan(target))
            return True

        if command == "service-health-check-plan":
            self.print_runtime_service_packet("AURA Service Health Check Plan", manager.service_health_check_plan(target))
            return True

        if command == "systemd-unit-blueprint-plan":
            self.print_runtime_service_packet("AURA Systemd Unit Blueprint Plan", manager.systemd_unit_blueprint_plan(target))
            return True

        if command == "service-recovery-plan":
            self.print_runtime_service_packet("AURA Service Recovery Plan", manager.service_recovery_plan(target))
            return True

        if command == "service-monitor-view-plan":
            self.print_runtime_service_packet("AURA Service Monitor View Plan", manager.service_monitor_view_plan(target))
            return True

        if command == "auto-boot-policy-plan":
            self.print_runtime_service_packet("AURA Auto Boot Policy Plan", manager.auto_boot_policy_plan(target))
            return True

        if command == "runtime-service-context":
            self.print_runtime_service_packet("AURA Runtime Service Foundation Context", manager.context())
            return True

        return False


    # Sprint 85.0 launcher health monitor foundation CLI helpers.
    def print_launcher_monitor_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Launcher Monitor Safety Boundary"))

    def handle_launcher_monitor_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA launcher and health monitor foundation"
        manager = AuraLauncherHealthMonitorFoundationManager(project_root=self.project_root)

        if command == "launcher-monitor-status":
            self.print_launcher_monitor_packet("AURA Launcher & Health Monitor Foundation Status", manager.status())
            return True

        if command == "launcher-start-plan":
            self.print_launcher_monitor_packet("AURA Launcher Start Plan", manager.launcher_start_plan(target))
            return True

        if command == "launcher-stop-plan":
            self.print_launcher_monitor_packet("AURA Launcher Stop Plan", manager.launcher_stop_plan(target))
            return True

        if command == "launcher-restart-plan":
            self.print_launcher_monitor_packet("AURA Launcher Restart Plan", manager.launcher_restart_plan(target))
            return True

        if command == "launcher-status-plan":
            self.print_launcher_monitor_packet("AURA Launcher Status Plan", manager.launcher_status_plan(target))
            return True

        if command == "launcher-log-view-plan":
            self.print_launcher_monitor_packet("AURA Launcher Log View Plan", manager.launcher_log_view_plan(target))
            return True

        if command == "health-monitor-plan":
            self.print_launcher_monitor_packet("AURA Health Monitor Plan", manager.health_monitor_plan(target))
            return True

        if command == "control-center-service-monitor-plan":
            self.print_launcher_monitor_packet("AURA Control Center Service Monitor Plan", manager.control_center_service_monitor_plan(target))
            return True

        if command == "launcher-safety-policy-plan":
            self.print_launcher_monitor_packet("AURA Launcher Safety Policy Plan", manager.launcher_safety_policy_plan(target))
            return True

        if command == "launcher-health-context":
            self.print_launcher_monitor_packet("AURA Launcher & Health Monitor Foundation Context", manager.context())
            return True

        return False


    # Sprint 86.0 control center UI blueprint CLI helpers.
    def print_control_center_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Safety Boundary"))

    def handle_control_center_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Control Center UI blueprint"
        manager = AuraControlCenterUIBlueprintManager(project_root=self.project_root)

        if command == "control-center-status":
            self.print_control_center_packet("AURA Control Center UI Blueprint Status", manager.status())
            return True

        if command == "dashboard-layout-blueprint-plan":
            self.print_control_center_packet("AURA Dashboard Layout Blueprint Plan", manager.dashboard_layout_blueprint_plan(target))
            return True

        if command == "permission-center-blueprint-plan":
            self.print_control_center_packet("AURA Permission Center Blueprint Plan", manager.permission_center_blueprint_plan(target))
            return True

        if command == "service-monitor-blueprint-plan":
            self.print_control_center_packet("AURA Service Monitor Blueprint Plan", manager.service_monitor_blueprint_plan(target))
            return True

        if command == "capability-viewer-blueprint-plan":
            self.print_control_center_packet("AURA Capability Viewer Blueprint Plan", manager.capability_viewer_blueprint_plan(target))
            return True

        if command == "launcher-control-blueprint-plan":
            self.print_control_center_packet("AURA Launcher Control Blueprint Plan", manager.launcher_control_blueprint_plan(target))
            return True

        if command == "chat-console-placeholder-plan":
            self.print_control_center_packet("AURA Chat Console Placeholder Plan", manager.chat_console_placeholder_plan(target))
            return True

        if command == "plugin-dashboard-blueprint-plan":
            self.print_control_center_packet("AURA Plugin Dashboard Blueprint Plan", manager.plugin_dashboard_blueprint_plan(target))
            return True

        if command == "action-log-blueprint-plan":
            self.print_control_center_packet("AURA Action Log Blueprint Plan", manager.action_log_blueprint_plan(target))
            return True

        if command == "control-center-safety-policy-plan":
            self.print_control_center_packet("AURA Control Center Safety Policy Plan", manager.control_center_safety_policy_plan(target))
            return True

        if command == "control-center-context":
            self.print_control_center_packet("AURA Control Center UI Blueprint Context", manager.context())
            return True

        return False


    # Sprint 87.0 local console web foundation CLI helpers.
    def print_local_console_web_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console Web Safety Boundary"))

    def handle_local_console_web_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local console web foundation"
        manager = AuraLocalConsoleWebFoundationManager(project_root=self.project_root)

        if command == "local-console-web-status":
            self.print_local_console_web_packet("AURA Local Console Web Foundation Status", manager.status())
            return True

        if command == "local-host-policy-plan":
            self.print_local_console_web_packet("AURA Local Host Policy Plan", manager.local_host_policy_plan(target))
            return True

        if command == "route-blueprint-plan":
            self.print_local_console_web_packet("AURA Route Blueprint Plan", manager.route_blueprint_plan(target))
            return True

        if command == "api-contract-blueprint-plan":
            self.print_local_console_web_packet("AURA API Contract Blueprint Plan", manager.api_contract_blueprint_plan(target))
            return True

        if command == "static-asset-blueprint-plan":
            self.print_local_console_web_packet("AURA Static Asset Blueprint Plan", manager.static_asset_blueprint_plan(target))
            return True

        if command == "session-state-blueprint-plan":
            self.print_local_console_web_packet("AURA Session State Blueprint Plan", manager.session_state_blueprint_plan(target))
            return True

        if command == "security-boundary-plan":
            self.print_local_console_web_packet("AURA Local Console Security Boundary Plan", manager.security_boundary_plan(target))
            return True

        if command == "control-center-web-bridge-plan":
            self.print_local_console_web_packet("AURA Control Center Web Bridge Plan", manager.control_center_web_bridge_plan(target))
            return True

        if command == "developer-console-access-plan":
            self.print_local_console_web_packet("AURA Developer Console Access Plan", manager.developer_console_access_plan(target))
            return True

        if command == "local-console-web-context":
            self.print_local_console_web_packet("AURA Local Console Web Foundation Context", manager.context())
            return True

        return False


    # Sprint 88.0 chat bridge session state foundation CLI helpers.
    def print_chat_bridge_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Bridge Safety Boundary"))

    def handle_chat_bridge_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA chat bridge and session state foundation"
        manager = AuraChatBridgeSessionStateFoundationManager(project_root=self.project_root)

        if command == "chat-bridge-status":
            self.print_chat_bridge_packet("AURA Chat Bridge & Session State Foundation Status", manager.status())
            return True

        if command == "conversation-session-blueprint-plan":
            self.print_chat_bridge_packet("AURA Conversation Session Blueprint Plan", manager.conversation_session_blueprint_plan(target))
            return True

        if command == "message-flow-blueprint-plan":
            self.print_chat_bridge_packet("AURA Message Flow Blueprint Plan", manager.message_flow_blueprint_plan(target))
            return True

        if command == "control-center-chat-panel-bridge-plan":
            self.print_chat_bridge_packet("AURA Control Center Chat Panel Bridge Plan", manager.control_center_chat_panel_bridge_plan(target))
            return True

        if command == "local-console-session-contract-plan":
            self.print_chat_bridge_packet("AURA Local Console Session Contract Plan", manager.local_console_session_contract_plan(target))
            return True

        if command == "permission-aware-chat-action-boundary-plan":
            self.print_chat_bridge_packet("AURA Permission-Aware Chat Action Boundary Plan", manager.permission_aware_chat_action_boundary_plan(target))
            return True

        if command == "chat-context-persistence-blueprint-plan":
            self.print_chat_bridge_packet("AURA Chat Context Persistence Blueprint Plan", manager.chat_context_persistence_blueprint_plan(target))
            return True

        if command == "websocket-boundary-plan":
            self.print_chat_bridge_packet("AURA Websocket Boundary Plan", manager.websocket_boundary_plan(target))
            return True

        if command == "session-recovery-blueprint-plan":
            self.print_chat_bridge_packet("AURA Session Recovery Blueprint Plan", manager.session_recovery_blueprint_plan(target))
            return True

        if command == "chat-bridge-safety-policy-plan":
            self.print_chat_bridge_packet("AURA Chat Bridge Safety Policy Plan", manager.chat_bridge_safety_policy_plan(target))
            return True

        if command == "chat-bridge-context":
            self.print_chat_bridge_packet("AURA Chat Bridge & Session State Foundation Context", manager.context())
            return True

        return False


    # Sprint 89.0 plugin permission dashboard foundation CLI helpers.
    def print_plugin_permission_dashboard_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Plugin / Permission Dashboard Safety Boundary"))

    def handle_plugin_permission_dashboard_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA plugin permission dashboard foundation"
        manager = AuraPluginPermissionDashboardFoundationManager(project_root=self.project_root)

        if command == "plugin-permission-dashboard-status":
            self.print_plugin_permission_dashboard_packet("AURA Plugin / Permission Dashboard Foundation Status", manager.status())
            return True

        if command == "plugin-registry-dashboard-plan":
            self.print_plugin_permission_dashboard_packet("AURA Plugin Registry Dashboard Plan", manager.plugin_registry_dashboard_plan(target))
            return True

        if command == "permission-request-dashboard-plan":
            self.print_plugin_permission_dashboard_packet("AURA Permission Request Dashboard Plan", manager.permission_request_dashboard_plan(target))
            return True

        if command == "permission-decision-visibility-plan":
            self.print_plugin_permission_dashboard_packet("AURA Permission Decision Visibility Plan", manager.permission_decision_visibility_plan(target))
            return True

        if command == "chat-originated-action-visibility-plan":
            self.print_plugin_permission_dashboard_packet("AURA Chat-Originated Action Visibility Plan", manager.chat_originated_action_visibility_plan(target))
            return True

        if command == "capability-permission-matrix-plan":
            self.print_plugin_permission_dashboard_packet("AURA Capability Permission Matrix Plan", manager.capability_permission_matrix_plan(target))
            return True

        if command == "control-center-dashboard-bridge-plan":
            self.print_plugin_permission_dashboard_packet("AURA Control Center Dashboard Bridge Plan", manager.control_center_dashboard_bridge_plan(target))
            return True

        if command == "local-console-dashboard-contract-plan":
            self.print_plugin_permission_dashboard_packet("AURA Local Console Dashboard Contract Plan", manager.local_console_dashboard_contract_plan(target))
            return True

        if command == "audit-trail-dashboard-blueprint-plan":
            self.print_plugin_permission_dashboard_packet("AURA Audit Trail Dashboard Blueprint Plan", manager.audit_trail_dashboard_blueprint_plan(target))
            return True

        if command == "dashboard-safety-policy-plan":
            self.print_plugin_permission_dashboard_packet("AURA Dashboard Safety Policy Plan", manager.dashboard_safety_policy_plan(target))
            return True

        if command == "plugin-permission-dashboard-context":
            self.print_plugin_permission_dashboard_packet("AURA Plugin / Permission Dashboard Foundation Context", manager.context())
            return True

        return False





















































    # Sprint 142.0 local service safe idle boot boundary CLI helpers.


    # Sprint 144.0 service configuration and port registry foundation CLI helpers.
    def print_local_service_configuration_port_registry_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Configuration and Port Registry Foundation Safety Boundary"))

    def handle_local_service_configuration_port_registry_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service configuration and port registry foundation"
        manager = AuraLocalServiceConfigurationPortRegistryFoundationManager(project_root=self.project_root)

        if command == "local-service-configuration-port-registry-foundation-status":
            self.print_local_service_configuration_port_registry_foundation_packet("AURA Service Configuration and Port Registry Foundation Status", manager.status())
            return True

        if command == "local-service-configuration-port-registry-foundation-context":
            self.print_local_service_configuration_port_registry_foundation_packet("AURA Service Configuration and Port Registry Foundation Context", manager.context())
            return True

        command_map = {
            "service-configuration-scope-plan": ("AURA Service Configuration Scope Plan", manager.service_configuration_scope_plan),
            "service-config-schema-plan": ("AURA Service Config Schema Plan", manager.service_config_schema_plan),
            "service-port-registry-schema-plan": ("AURA Service Port Registry Schema Plan", manager.service_port_registry_schema_plan),
            "localhost-port-policy-plan": ("AURA Localhost Port Policy Plan", manager.localhost_port_policy_plan),
            "reserved-port-policy-plan": ("AURA Reserved Port Policy Plan", manager.reserved_port_policy_plan),
            "port-conflict-preflight-plan": ("AURA Port Conflict Preflight Plan", manager.port_conflict_preflight_plan),
            "environment-override-boundary-plan": ("AURA Environment Override Boundary Plan", manager.environment_override_boundary_plan),
            "control-center-config-card-plan": ("AURA Control Center Config Card Plan", manager.control_center_config_card_plan),
            "permission-audit-config-link-plan": ("AURA Permission Audit Config Link Plan", manager.permission_audit_config_link_plan),
            "no-config-port-runtime-activation-plan": ("AURA No Config Port Runtime Activation Plan", manager.no_config_port_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_configuration_port_registry_foundation_packet(title, handler(target))
            return True

        return False




































    # Sprint 180.0 memory runtime stabilization helpers.
    def print_memory_runtime_stabilization_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Runtime Stabilization"))

    def handle_memory_runtime_stabilization_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False
        command = raw_args[0]
        manager = AuraMemoryRuntimeStabilizationManager(project_root=self.project_root)

        if command in {"memory-runtime-stabilization-alpha", "memory-stabilization-alpha"}:
            if len(raw_args) < 2:
                print('Usage: python3 main.py memory-runtime-stabilization-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_stabilization_alpha(" ".join(raw_args[1:])))
            return True
        if command == "memory-runtime-stabilization-status":
            self.print_memory_runtime_stabilization_packet("AURA Memory Runtime Stabilization Status", manager.status())
            return True
        if command == "memory-runtime-stabilization-context":
            self.print_memory_runtime_stabilization_packet("AURA Memory Runtime Stabilization Context", manager.context())
            return True

        target = " ".join(raw_args[1:]) if len(raw_args) > 1 else "AURA memory runtime stabilization"
        command_map = {
            "memory-runtime-block-completion-plan": ("AURA Memory Runtime Block Completion Plan", manager.memory_runtime_block_completion_plan),
            "memory-runtime-component-stability-plan": ("AURA Memory Runtime Component Stability Plan", manager.memory_runtime_component_stability_plan),
            "memory-runtime-pipeline-stability-plan": ("AURA Memory Runtime Pipeline Stability Plan", manager.memory_runtime_pipeline_stability_plan),
            "memory-runtime-privacy-stability-plan": ("AURA Memory Runtime Privacy Stability Plan", manager.memory_runtime_privacy_stability_plan),
            "memory-runtime-review-permission-stability-plan": ("AURA Memory Runtime Review Permission Stability Plan", manager.memory_runtime_review_permission_stability_plan),
            "memory-runtime-correction-deletion-stability-plan": ("AURA Memory Runtime Correction Deletion Stability Plan", manager.memory_runtime_correction_deletion_stability_plan),
            "memory-runtime-control-center-handoff-plan": ("AURA Memory Runtime Control Center Handoff Plan", manager.memory_runtime_control_center_handoff_plan),
            "memory-runtime-release-gate-closure-plan": ("AURA Memory Runtime Release Gate Closure Plan", manager.memory_runtime_release_gate_closure_plan),
            "memory-runtime-voice-block-handoff-plan": ("AURA Memory Runtime Voice Block Handoff Plan", manager.memory_runtime_voice_block_handoff_plan),
            "no-memory-runtime-stabilization-unsafe-runtime-plan": ("AURA No Memory Runtime Stabilization Unsafe Runtime Plan", manager.no_memory_runtime_stabilization_unsafe_runtime_plan),
            "memory-runtime-stabilization-next-block-readiness-plan": ("AURA Memory Runtime Stabilization Next Block Readiness Plan", manager.memory_runtime_stabilization_next_block_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_runtime_stabilization_packet(title, handler(target))
            return True
        return False

    # Sprint 179.0 memory runtime integration review helpers.
    def print_memory_runtime_integration_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Runtime Integration Review"))

    def handle_memory_runtime_integration_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False
        command = raw_args[0]
        manager = AuraMemoryRuntimeIntegrationReviewManager(project_root=self.project_root)

        if command in {"memory-runtime-integration-review-alpha", "memory-integration-review-alpha"}:
            if len(raw_args) < 2:
                print('Usage: python3 main.py memory-runtime-integration-review-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_integration_review(" ".join(raw_args[1:])))
            return True
        if command == "memory-runtime-integration-review-status":
            self.print_memory_runtime_integration_review_packet("AURA Memory Runtime Integration Review Status", manager.status())
            return True
        if command == "memory-runtime-integration-review-context":
            self.print_memory_runtime_integration_review_packet("AURA Memory Runtime Integration Review Context", manager.context())
            return True

        target = " ".join(raw_args[1:]) if len(raw_args) > 1 else "AURA memory runtime integration review"
        command_map = {
            "memory-runtime-component-matrix-plan": ("AURA Memory Runtime Component Matrix Plan", manager.memory_runtime_component_matrix_plan),
            "memory-runtime-pipeline-order-plan": ("AURA Memory Runtime Pipeline Order Plan", manager.memory_runtime_pipeline_order_plan),
            "memory-runtime-dependency-review-plan": ("AURA Memory Runtime Dependency Review Plan", manager.memory_runtime_dependency_review_plan),
            "memory-runtime-permission-review-plan": ("AURA Memory Runtime Permission Review Plan", manager.memory_runtime_permission_review_plan),
            "memory-runtime-privacy-review-plan": ("AURA Memory Runtime Privacy Review Plan", manager.memory_runtime_privacy_review_plan),
            "memory-runtime-correction-deletion-review-plan": ("AURA Memory Runtime Correction Deletion Review Plan", manager.memory_runtime_correction_deletion_review_plan),
            "memory-runtime-control-center-handoff-plan": ("AURA Memory Runtime Control Center Handoff Plan", manager.memory_runtime_control_center_handoff_plan),
            "memory-runtime-failure-boundary-plan": ("AURA Memory Runtime Failure Boundary Plan", manager.memory_runtime_failure_boundary_plan),
            "memory-runtime-release-gate-plan": ("AURA Memory Runtime Release Gate Plan", manager.memory_runtime_release_gate_plan),
            "no-memory-runtime-integration-unsafe-runtime-plan": ("AURA No Memory Runtime Integration Unsafe Runtime Plan", manager.no_memory_runtime_integration_unsafe_runtime_plan),
            "memory-runtime-integration-next-sprint-readiness-plan": ("AURA Memory Runtime Integration Next Sprint Readiness Plan", manager.memory_runtime_integration_next_sprint_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_runtime_integration_review_packet(title, handler(target))
            return True
        return False

    # Sprint 178.0 memory privacy and redaction layer helpers.
    def print_memory_privacy_redaction_layer_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Privacy and Redaction Layer"))

    def handle_memory_privacy_redaction_layer_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False
        command = raw_args[0]
        manager = AuraMemoryPrivacyRedactionLayerManager(project_root=self.project_root)

        if command in {"memory-privacy-redaction-alpha", "memory-privacy-alpha"}:
            if len(raw_args) < 2:
                print('Usage: python3 main.py memory-privacy-redaction-alpha "remember that contact email is demo@example.com"')
                return True
            print(manager.render_privacy_preview(" ".join(raw_args[1:])))
            return True
        if command == "memory-privacy-redaction-status":
            self.print_memory_privacy_redaction_layer_packet("AURA Memory Privacy and Redaction Layer Status", manager.status())
            return True
        if command == "memory-privacy-redaction-context":
            self.print_memory_privacy_redaction_layer_packet("AURA Memory Privacy and Redaction Layer Context", manager.context())
            return True

        target = " ".join(raw_args[1:]) if len(raw_args) > 1 else "AURA memory privacy and redaction layer"
        command_map = {
            "memory-privacy-classification-plan": ("AURA Memory Privacy Classification Plan", manager.memory_privacy_classification_plan),
            "memory-sensitive-pattern-screen-plan": ("AURA Memory Sensitive Pattern Screen Plan", manager.memory_sensitive_pattern_screen_plan),
            "memory-redaction-preview-plan": ("AURA Memory Redaction Preview Plan", manager.memory_redaction_preview_plan),
            "memory-secret-block-plan": ("AURA Memory Secret Block Plan", manager.memory_secret_block_plan),
            "memory-privacy-review-handoff-plan": ("AURA Memory Privacy Review Handoff Plan", manager.memory_privacy_review_handoff_plan),
            "memory-privacy-permission-handoff-plan": ("AURA Memory Privacy Permission Handoff Plan", manager.memory_privacy_permission_handoff_plan),
            "memory-privacy-control-center-plan": ("AURA Memory Privacy Control Center Plan", manager.memory_privacy_control_center_plan),
            "memory-privacy-failure-boundary-plan": ("AURA Memory Privacy Failure Boundary Plan", manager.memory_privacy_failure_boundary_plan),
            "memory-privacy-lifecycle-plan": ("AURA Memory Privacy Lifecycle Plan", manager.memory_privacy_lifecycle_plan),
            "no-memory-privacy-unsafe-runtime-plan": ("AURA No Memory Privacy Unsafe Runtime Plan", manager.no_memory_privacy_unsafe_runtime_plan),
            "memory-privacy-next-sprint-readiness-plan": ("AURA Memory Privacy Next Sprint Readiness Plan", manager.memory_privacy_next_sprint_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_privacy_redaction_layer_packet(title, handler(target))
            return True
        return False

    # Sprint 177.0 chat-to-memory handoff contract helpers.
    def print_chat_to_memory_handoff_contract_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat-to-Memory Handoff Contract"))

    def handle_chat_to_memory_handoff_contract_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False
        command = raw_args[0]
        manager = AuraChatToMemoryHandoffContractManager(project_root=self.project_root)

        if command in {"chat-to-memory-handoff-alpha", "chat-memory-handoff-alpha"}:
            if len(raw_args) < 2:
                print('Usage: python3 main.py chat-to-memory-handoff-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_handoff_preview(" ".join(raw_args[1:]), source_role="user"))
            return True
        if command == "chat-to-memory-handoff-status":
            self.print_chat_to_memory_handoff_contract_packet("AURA Chat-to-Memory Handoff Contract Status", manager.status())
            return True
        if command == "chat-to-memory-handoff-context":
            self.print_chat_to_memory_handoff_contract_packet("AURA Chat-to-Memory Handoff Contract Context", manager.context())
            return True

        target = " ".join(raw_args[1:]) if len(raw_args) > 1 else "AURA chat-to-memory handoff contract"
        command_map = {
            "chat-source-binding-plan": ("AURA Chat Source Binding Plan", manager.chat_source_binding_plan),
            "chat-memory-intent-gate-plan": ("AURA Chat Memory Intent Gate Plan", manager.chat_memory_intent_gate_plan),
            "chat-memory-candidate-envelope-plan": ("AURA Chat Memory Candidate Envelope Plan", manager.chat_memory_candidate_envelope_plan),
            "chat-memory-review-queue-handoff-plan": ("AURA Chat Memory Review Queue Handoff Plan", manager.chat_memory_review_queue_handoff_plan),
            "chat-memory-permission-handoff-plan": ("AURA Chat Memory Permission Handoff Plan", manager.chat_memory_permission_handoff_plan),
            "chat-memory-privacy-precheck-plan": ("AURA Chat Memory Privacy Precheck Plan", manager.chat_memory_privacy_precheck_plan),
            "chat-memory-control-center-handoff-plan": ("AURA Chat Memory Control Center Handoff Plan", manager.chat_memory_control_center_handoff_plan),
            "chat-memory-failure-boundary-plan": ("AURA Chat Memory Failure Boundary Plan", manager.chat_memory_failure_boundary_plan),
            "chat-memory-lifecycle-plan": ("AURA Chat Memory Lifecycle Plan", manager.chat_memory_lifecycle_plan),
            "no-chat-to-memory-unsafe-runtime-plan": ("AURA No Chat-to-Memory Unsafe Runtime Plan", manager.no_chat_to_memory_unsafe_runtime_plan),
            "chat-to-memory-next-sprint-readiness-plan": ("AURA Chat-to-Memory Next Sprint Readiness Plan", manager.chat_to_memory_next_sprint_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_chat_to_memory_handoff_contract_packet(title, handler(target))
            return True
        return False

    # Sprint 176.0 memory correction and deletion boundary helpers.
    def print_memory_correction_deletion_boundary_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Correction and Deletion Boundary"))

    def handle_memory_correction_deletion_boundary_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        manager = AuraMemoryCorrectionDeletionBoundaryManager(project_root=self.project_root)

        if command in {"memory-correction-deletion-alpha", "memory-mutation-boundary-alpha"}:
            if len(raw_args) < 3:
                print("AURA Memory Correction and Deletion Boundary Alpha")
                print("====================================================")
                print('Usage correction: python3 main.py memory-correction-deletion-alpha correction "old memory => corrected memory"')
                print('Usage deletion  : python3 main.py memory-correction-deletion-alpha delete "memory record text"')
                return True
            operation = raw_args[1]
            payload = " ".join(raw_args[2:]).strip()
            print(manager.render_boundary_preview(operation, payload))
            return True

        target = " ".join(raw_args[1:]).strip() or "AURA memory correction and deletion boundary"
        if command == "memory-correction-deletion-status":
            self.print_memory_correction_deletion_boundary_packet("AURA Memory Correction and Deletion Boundary Status", manager.status())
            return True

        if command == "memory-correction-deletion-context":
            self.print_memory_correction_deletion_boundary_packet("AURA Memory Correction and Deletion Boundary Context", manager.context())
            return True

        command_map = {
            "memory-correction-boundary-plan": ("AURA Memory Correction Boundary Plan", manager.memory_correction_boundary_plan),
            "memory-deletion-boundary-plan": ("AURA Memory Deletion Boundary Plan", manager.memory_deletion_boundary_plan),
            "memory-versioned-replacement-plan": ("AURA Memory Versioned Replacement Plan", manager.memory_versioned_replacement_plan),
            "memory-tombstone-lifecycle-plan": ("AURA Memory Tombstone Lifecycle Plan", manager.memory_tombstone_lifecycle_plan),
            "memory-exact-target-binding-plan": ("AURA Memory Exact Target Binding Plan", manager.memory_exact_target_binding_plan),
            "memory-correction-deletion-permission-handoff-plan": ("AURA Memory Correction Deletion Permission Handoff Plan", manager.memory_correction_deletion_permission_handoff_plan),
            "memory-correction-privacy-rescreen-plan": ("AURA Memory Correction Privacy Rescreen Plan", manager.memory_correction_privacy_rescreen_plan),
            "memory-correction-deletion-control-center-plan": ("AURA Memory Correction Deletion Control Center Plan", manager.memory_correction_deletion_control_center_plan),
            "memory-correction-deletion-failure-boundary-plan": ("AURA Memory Correction Deletion Failure Boundary Plan", manager.memory_correction_deletion_failure_boundary_plan),
            "no-memory-correction-deletion-unsafe-runtime-plan": ("AURA No Memory Correction Deletion Unsafe Runtime Plan", manager.no_memory_correction_deletion_unsafe_runtime_plan),
            "memory-correction-deletion-next-sprint-readiness-plan": ("AURA Memory Correction Deletion Next Sprint Readiness Plan", manager.memory_correction_deletion_next_sprint_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_correction_deletion_boundary_packet(title, handler(target))
            return True
        return False

    # Sprint 175.0 memory review queue helpers.
    def print_memory_review_queue_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Review Queue Boundary"))

    def handle_memory_review_queue_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory review queue"
        manager = AuraMemoryReviewQueueManager(project_root=self.project_root)

        if command in {"memory-review-queue-alpha", "memory-review-alpha"}:
            if not target or target == "AURA memory review queue":
                print("AURA Memory Review Queue Alpha")
                print("==============================")
                print('Usage: python3 main.py memory-review-queue-alpha "remember that AURA is local-first and permission-gated"')
                return True
            print(manager.render_queue_preview(target))
            return True

        if command == "memory-review-queue-status":
            self.print_memory_review_queue_packet("AURA Memory Review Queue Status", manager.status())
            return True

        if command == "memory-review-queue-context":
            self.print_memory_review_queue_packet("AURA Memory Review Queue Context", manager.context())
            return True

        command_map = {
            "memory-review-queue-item-contract-plan": ("AURA Memory Review Queue Item Contract Plan", manager.memory_review_queue_item_contract_plan),
            "memory-review-priority-policy-plan": ("AURA Memory Review Priority Policy Plan", manager.memory_review_priority_policy_plan),
            "memory-review-decision-options-plan": ("AURA Memory Review Decision Options Plan", manager.memory_review_decision_options_plan),
            "memory-review-privacy-hold-plan": ("AURA Memory Review Privacy Hold Plan", manager.memory_review_privacy_hold_plan),
            "memory-review-permission-handoff-plan": ("AURA Memory Review Permission Handoff Plan", manager.memory_review_permission_handoff_plan),
            "memory-review-edit-handoff-plan": ("AURA Memory Review Edit Handoff Plan", manager.memory_review_edit_handoff_plan),
            "memory-review-control-center-queue-plan": ("AURA Memory Review Control Center Queue Plan", manager.memory_review_control_center_queue_plan),
            "memory-review-queue-lifecycle-plan": ("AURA Memory Review Queue Lifecycle Plan", manager.memory_review_queue_lifecycle_plan),
            "memory-review-queue-failure-boundary-plan": ("AURA Memory Review Queue Failure Boundary Plan", manager.memory_review_queue_failure_boundary_plan),
            "no-memory-review-queue-unsafe-runtime-plan": ("AURA No Memory Review Queue Unsafe Runtime Plan", manager.no_memory_review_queue_unsafe_runtime_plan),
            "memory-review-queue-next-sprint-readiness-plan": ("AURA Memory Review Queue Next Sprint Readiness Plan", manager.memory_review_queue_next_sprint_readiness_plan),
        }
        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_review_queue_packet(title, handler(target))
            return True
        return False

    # Sprint 174.0 memory importance and pinning policy helpers.
    def print_memory_importance_pinning_policy_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Importance and Pinning Policy Boundary"))

    def handle_memory_importance_pinning_policy_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory importance and pinning policy"
        manager = AuraMemoryImportancePinningPolicyManager(project_root=self.project_root)

        if command in {"memory-importance-pinning-alpha", "memory-importance-alpha"}:
            if not target or target == "AURA memory importance and pinning policy":
                print("AURA Memory Importance and Pinning Policy Alpha")
                print("================================================")
                print('Usage: python3 main.py memory-importance-pinning-alpha "remember that AURA is local-first and permission-gated"')
                return True
            print(manager.render_policy_preview(target))
            return True

        if command == "memory-importance-pinning-status":
            self.print_memory_importance_pinning_policy_packet("AURA Memory Importance and Pinning Policy Status", manager.status())
            return True

        if command == "memory-importance-pinning-context":
            self.print_memory_importance_pinning_policy_packet("AURA Memory Importance and Pinning Policy Context", manager.context())
            return True

        command_map = {
            "memory-importance-scoring-plan": ("AURA Memory Importance Scoring Plan", manager.memory_importance_scoring_plan),
            "memory-durability-signal-plan": ("AURA Memory Durability Signal Plan", manager.memory_durability_signal_plan),
            "memory-temporary-signal-plan": ("AURA Memory Temporary Signal Plan", manager.memory_temporary_signal_plan),
            "memory-retention-recommendation-plan": ("AURA Memory Retention Recommendation Plan", manager.memory_retention_recommendation_plan),
            "memory-pin-eligibility-plan": ("AURA Memory Pin Eligibility Plan", manager.memory_pin_eligibility_plan),
            "memory-pin-permission-boundary-plan": ("AURA Memory Pin Permission Boundary Plan", manager.memory_pin_permission_boundary_plan),
            "memory-importance-manual-review-handoff-plan": ("AURA Memory Importance Manual Review Handoff Plan", manager.memory_importance_manual_review_handoff_plan),
            "memory-importance-sensitive-boundary-plan": ("AURA Memory Importance Sensitive Boundary Plan", manager.memory_importance_sensitive_boundary_plan),
            "memory-control-center-importance-preview-plan": ("AURA Memory Control Center Importance Preview Plan", manager.memory_control_center_importance_preview_plan),
            "no-memory-importance-pinning-unsafe-runtime-plan": ("AURA No Memory Importance Pinning Unsafe Runtime Plan", manager.no_memory_importance_pinning_unsafe_runtime_plan),
            "memory-importance-next-sprint-readiness-plan": ("AURA Memory Importance Next Sprint Readiness Plan", manager.memory_importance_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_importance_pinning_policy_packet(title, handler(target))
            return True

        return False

    # Sprint 173.0 memory extraction dry run helpers.
    def print_memory_extraction_dry_run_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Extraction Dry Run Boundary"))

    def handle_memory_extraction_dry_run_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory extraction dry run"
        manager = AuraMemoryExtractionDryRunManager(project_root=self.project_root)

        if command in {"memory-extraction-dry-run-alpha", "memory-extraction-alpha"}:
            if not target or target == "AURA memory extraction dry run":
                print("AURA Memory Extraction Dry Run Alpha")
                print("====================================")
                print('Usage: python3 main.py memory-extraction-dry-run-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_extraction_dry_run(target))
            return True

        if command == "memory-extraction-dry-run-status":
            self.print_memory_extraction_dry_run_packet("AURA Memory Extraction Dry Run Status", manager.status())
            return True

        if command == "memory-extraction-dry-run-context":
            self.print_memory_extraction_dry_run_packet("AURA Memory Extraction Dry Run Context", manager.context())
            return True

        command_map = {
            "memory-explicit-trigger-detection-plan": ("AURA Memory Explicit Trigger Detection Plan", manager.memory_explicit_trigger_detection_plan),
            "memory-candidate-normalization-plan": ("AURA Memory Candidate Normalization Plan", manager.memory_candidate_normalization_plan),
            "memory-candidate-classification-plan": ("AURA Memory Candidate Classification Plan", manager.memory_candidate_classification_plan),
            "memory-sensitive-pattern-screen-plan": ("AURA Memory Sensitive Pattern Screen Plan", manager.memory_sensitive_pattern_screen_plan),
            "memory-candidate-fingerprint-handoff-plan": ("AURA Memory Candidate Fingerprint Handoff Plan", manager.memory_candidate_fingerprint_handoff_plan),
            "memory-permission-gate-handoff-plan": ("AURA Memory Permission Gate Handoff Plan", manager.memory_permission_gate_handoff_plan),
            "memory-manual-review-handoff-plan": ("AURA Memory Manual Review Handoff Plan", manager.memory_manual_review_handoff_plan),
            "memory-extraction-failure-boundary-plan": ("AURA Memory Extraction Failure Boundary Plan", manager.memory_extraction_failure_boundary_plan),
            "memory-control-center-extraction-preview-plan": ("AURA Memory Control Center Extraction Preview Plan", manager.memory_control_center_extraction_preview_plan),
            "no-memory-extraction-unsafe-runtime-plan": ("AURA No Memory Extraction Unsafe Runtime Plan", manager.no_memory_extraction_unsafe_runtime_plan),
            "memory-extraction-next-sprint-readiness-plan": ("AURA Memory Extraction Next Sprint Readiness Plan", manager.memory_extraction_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_extraction_dry_run_packet(title, handler(target))
            return True

        return False

    # Sprint 172.0 memory write permission gate helpers.
    def print_memory_write_permission_gate_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Write Permission Gate Boundary"))

    def handle_memory_write_permission_gate_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory write permission gate"
        manager = AuraMemoryWritePermissionGateManager(project_root=self.project_root)

        if command in {"memory-write-permission-gate-alpha", "memory-permission-gate-alpha"}:
            if not target or target == "AURA memory write permission gate":
                print("AURA Memory Write Permission Gate Alpha")
                print("=======================================")
                print('Usage: python3 main.py memory-write-permission-gate-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_permission_gate_alpha(target))
            return True

        if command == "memory-write-permission-gate-status":
            self.print_memory_write_permission_gate_packet("AURA Memory Write Permission Gate Status", manager.status())
            return True

        if command == "memory-write-permission-gate-context":
            self.print_memory_write_permission_gate_packet("AURA Memory Write Permission Gate Context", manager.context())
            return True

        command_map = {
            "memory-permission-request-envelope-plan": ("AURA Memory Permission Request Envelope Plan", manager.memory_permission_request_envelope_plan),
            "memory-permission-scope-validation-plan": ("AURA Memory Permission Scope Validation Plan", manager.memory_permission_scope_validation_plan),
            "memory-candidate-fingerprint-plan": ("AURA Memory Candidate Fingerprint Plan", manager.memory_candidate_fingerprint_plan),
            "memory-default-deny-policy-plan": ("AURA Memory Default Deny Policy Plan", manager.memory_default_deny_policy_plan),
            "memory-one-shot-grant-plan": ("AURA Memory One Shot Grant Plan", manager.memory_one_shot_grant_plan),
            "memory-permission-expiry-plan": ("AURA Memory Permission Expiry Plan", manager.memory_permission_expiry_plan),
            "memory-permission-audit-handoff-plan": ("AURA Memory Permission Audit Handoff Plan", manager.memory_permission_audit_handoff_plan),
            "memory-control-center-permission-handoff-plan": ("AURA Memory Control Center Permission Handoff Plan", manager.memory_control_center_permission_handoff_plan),
            "memory-permission-failure-boundary-plan": ("AURA Memory Permission Failure Boundary Plan", manager.memory_permission_failure_boundary_plan),
            "no-memory-write-permission-gate-unsafe-runtime-plan": ("AURA No Memory Write Permission Gate Unsafe Runtime Plan", manager.no_memory_write_permission_gate_unsafe_runtime_plan),
            "memory-permission-gate-next-sprint-readiness-plan": ("AURA Memory Permission Gate Next Sprint Readiness Plan", manager.memory_permission_gate_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_write_permission_gate_packet(title, handler(target))
            return True

        return False

    # Sprint 171.0 memory runtime foundation helpers.
    def print_memory_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Runtime Foundation Boundary"))

    def handle_memory_runtime_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory runtime foundation"
        manager = AuraMemoryRuntimeFoundationManager(project_root=self.project_root)

        if command in {"memory-runtime-alpha", "memory-runtime-foundation-alpha", "memory-foundation-alpha"}:
            if not target or target == "AURA memory runtime foundation":
                print("AURA Memory Runtime Foundation Alpha")
                print("====================================")
                print('Usage: python3 main.py memory-runtime-alpha "remember that AURA is local-first"')
                return True
            print(manager.render_foundation_alpha(target))
            return True

        if command == "memory-runtime-foundation-status":
            self.print_memory_runtime_foundation_packet("AURA Memory Runtime Foundation Status", manager.status())
            return True

        if command == "memory-runtime-foundation-context":
            self.print_memory_runtime_foundation_packet("AURA Memory Runtime Foundation Context", manager.context())
            return True

        command_map = {
            "memory-candidate-schema-plan": ("AURA Memory Candidate Schema Plan", manager.memory_candidate_schema_plan),
            "memory-write-gate-plan": ("AURA Memory Write Gate Plan", manager.memory_write_gate_plan),
            "memory-source-boundary-plan": ("AURA Memory Source Boundary Plan", manager.memory_source_boundary_plan),
            "memory-privacy-redaction-plan": ("AURA Memory Privacy Redaction Plan", manager.memory_privacy_redaction_plan),
            "memory-review-queue-handoff-plan": ("AURA Memory Review Queue Handoff Plan", manager.memory_review_queue_handoff_plan),
            "memory-correction-deletion-policy-plan": ("AURA Memory Correction Deletion Policy Plan", manager.memory_correction_deletion_policy_plan),
            "chat-to-memory-handoff-plan": ("AURA Chat To Memory Handoff Plan", manager.chat_to_memory_handoff_plan),
            "memory-model-summary-boundary-plan": ("AURA Memory Model Summary Boundary Plan", manager.memory_model_summary_boundary_plan),
            "memory-control-center-handoff-plan": ("AURA Memory Control Center Handoff Plan", manager.memory_control_center_handoff_plan),
            "no-memory-runtime-unsafe-runtime-plan": ("AURA No Memory Runtime Unsafe Runtime Plan", manager.no_memory_runtime_unsafe_runtime_plan),
            "memory-next-sprint-readiness-plan": ("AURA Memory Next Sprint Readiness Plan", manager.memory_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_runtime_foundation_packet(title, handler(target))
            return True

        return False

    # Sprint 170.0 local chat runtime stabilization helpers.
    def print_local_chat_runtime_stabilization_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Runtime Stabilization Boundary"))

    def handle_local_chat_runtime_stabilization_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat runtime stabilization"
        manager = AuraLocalChatRuntimeStabilizationManager(project_root=self.project_root)

        if command in {"local-chat-stabilization-alpha", "local-chat-runtime-stabilization-alpha", "local-chat-block-stabilization"}:
            print(manager.render_stabilization_alpha())
            return True

        if command == "local-chat-runtime-stabilization-status":
            self.print_local_chat_runtime_stabilization_packet("AURA Local Chat Runtime Stabilization Status", manager.status())
            return True

        if command == "local-chat-runtime-stabilization-context":
            self.print_local_chat_runtime_stabilization_packet("AURA Local Chat Runtime Stabilization Context", manager.context())
            return True

        command_map = {
            "local-chat-block-completion-review-plan": ("AURA Local Chat Block Completion Review Plan", manager.local_chat_block_completion_review_plan),
            "local-chat-alpha-surface-stabilization-plan": ("AURA Local Chat Alpha Surface Stabilization Plan", manager.local_chat_alpha_surface_stabilization_plan),
            "local-chat-store-history-stabilization-plan": ("AURA Local Chat Store History Stabilization Plan", manager.local_chat_store_and_history_stabilization_plan),
            "local-chat-persona-safety-stabilization-plan": ("AURA Local Chat Persona Safety Stabilization Plan", manager.local_chat_persona_safety_stabilization_plan),
            "local-chat-model-permission-stabilization-plan": ("AURA Local Chat Model Permission Gate Stabilization Plan", manager.local_chat_model_permission_gate_stabilization_plan),
            "local-chat-control-center-handoff-stabilization-plan": ("AURA Local Chat Control Center Handoff Stabilization Plan", manager.local_chat_control_center_handoff_stabilization_plan),
            "local-chat-memory-runtime-handoff-plan": ("AURA Local Chat Memory Runtime Handoff Plan", manager.local_chat_memory_runtime_handoff_plan),
            "local-chat-release-gate-closure-review-plan": ("AURA Local Chat Release Gate Closure Review Plan", manager.local_chat_release_gate_closure_review_plan),
            "no-local-chat-runtime-stabilization-unsafe-runtime-plan": ("AURA No Local Chat Runtime Stabilization Unsafe Runtime Plan", manager.no_local_chat_runtime_stabilization_unsafe_runtime_plan),
            "local-chat-next-block-171-180-readiness-plan": ("AURA Local Chat Next Block 171-180 Readiness Plan", manager.local_chat_next_block_171_180_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_runtime_stabilization_packet(title, handler(target))
            return True

        return False
    # Sprint 169.0 local chat integration review helpers.
    def print_local_chat_integration_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Integration Review Boundary"))

    def handle_local_chat_integration_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat integration review"
        manager = AuraLocalChatIntegrationReviewManager(project_root=self.project_root)

        if command in {"local-chat-integration-alpha", "local-chat-integration-review-alpha", "local-chat-integration"}:
            print(manager.render_integration_review_alpha())
            return True

        if command == "local-chat-integration-review-status":
            self.print_local_chat_integration_review_packet("AURA Local Chat Integration Review Status", manager.status())
            return True

        if command == "local-chat-integration-review-context":
            self.print_local_chat_integration_review_packet("AURA Local Chat Integration Review Context", manager.context())
            return True

        command_map = {
            "chat-alpha-chain-review-plan": ("AURA Chat Alpha Chain Review Plan", manager.chat_alpha_chain_review_plan),
            "chat-cli-surface-review-plan": ("AURA Chat CLI Surface Review Plan", manager.chat_cli_surface_review_plan),
            "chat-message-store-integration-review-plan": ("AURA Chat Message Store Integration Review Plan", manager.chat_message_store_integration_review_plan),
            "chat-persona-integration-review-plan": ("AURA Chat Persona Integration Review Plan", manager.chat_persona_integration_review_plan),
            "chat-model-boundary-integration-review-plan": ("AURA Chat Model Boundary Integration Review Plan", manager.chat_model_boundary_integration_review_plan),
            "chat-permission-gate-integration-review-plan": ("AURA Chat Permission Gate Integration Review Plan", manager.chat_permission_gate_integration_review_plan),
            "chat-safety-uncertainty-integration-review-plan": ("AURA Chat Safety Uncertainty Integration Review Plan", manager.chat_safety_uncertainty_integration_review_plan),
            "chat-history-viewer-integration-review-plan": ("AURA Chat History Viewer Integration Review Plan", manager.chat_history_viewer_integration_review_plan),
            "chat-control-center-handoff-review-plan": ("AURA Chat Control Center Handoff Review Plan", manager.chat_control_center_handoff_review_plan),
            "no-local-chat-integration-unsafe-runtime-plan": ("AURA No Local Chat Integration Unsafe Runtime Plan", manager.no_local_chat_integration_unsafe_runtime_plan),
            "local-chat-integration-next-sprint-readiness-plan": ("AURA Local Chat Integration Next Sprint Readiness Plan", manager.local_chat_integration_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_integration_review_packet(title, handler(target))
            return True

        return False

    # Sprint 168.0 chat history viewer contract helpers.
    def print_local_chat_history_viewer_contract_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat History Viewer Boundary"))

    def handle_local_chat_history_viewer_contract_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat history viewer contract"
        manager = AuraLocalChatHistoryViewerContractManager(project_root=self.project_root)

        if command in {"local-chat-history-alpha", "local-chat-history-viewer-alpha", "local-chat-history"}:
            limit_text = raw_args[1] if len(raw_args) > 1 else None
            print(manager.render_history_alpha(limit_text))
            return True

        if command == "local-chat-history-viewer-contract-status":
            self.print_local_chat_history_viewer_contract_packet("AURA Local Chat History Viewer Contract Status", manager.status())
            return True

        if command == "local-chat-history-viewer-contract-context":
            self.print_local_chat_history_viewer_contract_packet("AURA Local Chat History Viewer Contract Context", manager.context())
            return True

        command_map = {
            "chat-history-viewer-runtime-plan": ("AURA Chat History Viewer Runtime Plan", manager.chat_history_viewer_runtime_plan),
            "chat-history-store-read-policy-plan": ("AURA Chat History Store Read Policy Plan", manager.chat_history_store_read_policy_plan),
            "chat-history-schema-reader-plan": ("AURA Chat History Schema Reader Plan", manager.chat_history_schema_reader_plan),
            "chat-history-summary-renderer-plan": ("AURA Chat History Summary Renderer Plan", manager.chat_history_summary_renderer_plan),
            "chat-history-privacy-redaction-plan": ("AURA Chat History Privacy Redaction Plan", manager.chat_history_privacy_redaction_plan),
            "chat-history-pagination-contract-plan": ("AURA Chat History Pagination Contract Plan", manager.chat_history_pagination_contract_plan),
            "chat-history-safety-boundary-plan": ("AURA Chat History Safety Boundary Plan", manager.chat_history_safety_boundary_plan),
            "chat-history-control-center-handoff-plan": ("AURA Chat History Control Center Handoff Plan", manager.chat_history_control_center_handoff_plan),
            "no-local-chat-history-viewer-unsafe-runtime-plan": ("AURA No Local Chat History Viewer Unsafe Runtime Plan", manager.no_local_chat_history_viewer_unsafe_runtime_plan),
            "local-chat-history-viewer-next-sprint-readiness-plan": ("AURA Local Chat History Viewer Next Sprint Readiness Plan", manager.local_chat_history_viewer_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_history_viewer_contract_packet(title, handler(target))
            return True

        return False

    # Sprint 167.0 chat safety + uncertainty layer helpers.
    def print_local_chat_safety_uncertainty_layer_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Safety + Uncertainty Layer Boundary"))

    def handle_local_chat_safety_uncertainty_layer_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat safety uncertainty layer"
        manager = AuraLocalChatSafetyUncertaintyLayerManager(project_root=self.project_root)

        if command in {"local-chat-safety-alpha", "local-chat-safety-uncertainty-alpha", "local-chat-safety"}:
            if not target or target == "AURA local chat safety uncertainty layer":
                print("AURA Local Chat Safety + Uncertainty Alpha")
                print("============================================")
                print('Usage: python3 main.py local-chat-safety-alpha "Aura apakah info ini terbaru?"')
                return True
            print(manager.render_safety_alpha(target))
            return True

        if command == "local-chat-safety-uncertainty-layer-status":
            self.print_local_chat_safety_uncertainty_layer_packet("AURA Local Chat Safety + Uncertainty Layer Status", manager.status())
            return True

        if command == "local-chat-safety-uncertainty-layer-context":
            self.print_local_chat_safety_uncertainty_layer_packet("AURA Local Chat Safety + Uncertainty Layer Context", manager.context())
            return True

        command_map = {
            "chat-safety-uncertainty-runtime-plan": ("AURA Chat Safety + Uncertainty Runtime Plan", manager.chat_safety_uncertainty_runtime_plan),
            "chat-safety-classifier-plan": ("AURA Chat Safety Classifier Plan", manager.chat_safety_classifier_plan),
            "chat-uncertainty-classifier-plan": ("AURA Chat Uncertainty Classifier Plan", manager.chat_uncertainty_classifier_plan),
            "capability-honesty-response-plan": ("AURA Capability Honesty Response Plan", manager.capability_honesty_response_plan),
            "freshness-boundary-response-plan": ("AURA Freshness Boundary Response Plan", manager.freshness_boundary_response_plan),
            "model-gate-safety-handoff-plan": ("AURA Model Gate Safety Handoff Plan", manager.model_gate_safety_handoff_plan),
            "memory-command-boundary-plan": ("AURA Memory Command Boundary Plan", manager.memory_command_boundary_plan),
            "safe-fallback-response-plan": ("AURA Safe Fallback Response Plan", manager.safe_fallback_response_plan),
            "no-local-chat-safety-uncertainty-unsafe-runtime-plan": ("AURA No Local Chat Safety + Uncertainty Unsafe Runtime Plan", manager.no_local_chat_safety_uncertainty_unsafe_runtime_plan),
            "local-chat-safety-uncertainty-next-sprint-readiness-plan": ("AURA Local Chat Safety + Uncertainty Next Sprint Readiness Plan", manager.local_chat_safety_uncertainty_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_safety_uncertainty_layer_packet(title, handler(target))
            return True

        return False

    # Sprint 166.0 permission-gated model request helpers.
    def print_local_chat_permission_gated_model_request_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Permission-Gated Model Request Safety Boundary"))

    def handle_local_chat_permission_gated_model_request_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat permission-gated model request"
        manager = AuraLocalChatPermissionGatedModelRequestManager(project_root=self.project_root)

        if command in {"local-chat-permission-model-dry-run", "local-chat-model-permission-dry-run", "local-chat-permission-model"}:
            if not target or target == "AURA local chat permission-gated model request":
                print("AURA Local Chat Permission-Gated Model Request Dry Run")
                print("=======================================================")
                print('Usage: python3 main.py local-chat-permission-model-dry-run "Aura boleh pakai model?"')
                return True
            print(manager.render_permission_model_dry_run(target))
            return True

        if command == "local-chat-permission-gated-model-request-status":
            self.print_local_chat_permission_gated_model_request_packet("AURA Local Chat Permission-Gated Model Request Status", manager.status())
            return True

        if command == "local-chat-permission-gated-model-request-context":
            self.print_local_chat_permission_gated_model_request_packet("AURA Local Chat Permission-Gated Model Request Context", manager.context())
            return True

        command_map = {
            "permission-gated-model-request-runtime-plan": ("AURA Permission-Gated Model Request Runtime Plan", manager.permission_gated_model_request_runtime_plan),
            "model-permission-preview-packet-plan": ("AURA Model Permission Preview Packet Plan", manager.model_permission_preview_packet_plan),
            "model-request-envelope-gate-plan": ("AURA Model Request Envelope Gate Plan", manager.model_request_envelope_gate_plan),
            "model-provider-selection-gate-plan": ("AURA Model Provider Selection Gate Plan", manager.model_provider_selection_gate_plan),
            "model-credential-network-gate-plan": ("AURA Model Credential Network Gate Plan", manager.model_credential_network_gate_plan),
            "model-grant-decision-boundary-plan": ("AURA Model Grant Decision Boundary Plan", manager.model_grant_decision_boundary_plan),
            "model-audit-memory-boundary-plan": ("AURA Model Audit Memory Boundary Plan", manager.model_audit_memory_boundary_plan),
            "model-denial-fallback-plan": ("AURA Model Denial Fallback Plan", manager.model_denial_fallback_plan),
            "no-local-chat-permission-model-unsafe-runtime-plan": ("AURA No Local Chat Permission Model Unsafe Runtime Plan", manager.no_local_chat_permission_model_unsafe_runtime_plan),
            "local-chat-permission-model-next-sprint-readiness-plan": ("AURA Local Chat Permission Model Next Sprint Readiness Plan", manager.local_chat_permission_model_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_permission_gated_model_request_packet(title, handler(target))
            return True

        return False

    # Sprint 165.0 local chat model adapter boundary helpers.
    def print_local_chat_model_adapter_boundary_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Model Adapter Boundary Safety Boundary"))

    def handle_local_chat_model_adapter_boundary_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat model adapter boundary"
        manager = AuraLocalChatModelAdapterBoundaryManager(project_root=self.project_root)

        if command in {"local-chat-model-adapter-dry-run", "local-chat-model-adapter"}:
            if not target or target == "AURA local chat model adapter boundary":
                print("AURA Local Chat Model Adapter Boundary Dry Run")
                print("==============================================")
                print('Usage: python3 main.py local-chat-model-adapter-dry-run "Aura coba model adapter"')
                return True
            print(manager.render_dry_run(target))
            return True

        if command == "local-chat-model-adapter-boundary-status":
            self.print_local_chat_model_adapter_boundary_packet("AURA Local Chat Model Adapter Boundary Status", manager.status())
            return True

        if command == "local-chat-model-adapter-boundary-context":
            self.print_local_chat_model_adapter_boundary_packet("AURA Local Chat Model Adapter Boundary Context", manager.context())
            return True

        command_map = {
            "local-chat-model-adapter-boundary-runtime-plan": ("AURA Local Chat Model Adapter Boundary Runtime Plan", manager.local_chat_model_adapter_boundary_runtime_plan),
            "model-adapter-provider-contract-plan": ("AURA Model Adapter Provider Contract Plan", manager.model_adapter_provider_contract_plan),
            "model-prompt-envelope-contract-plan": ("AURA Model Prompt Envelope Contract Plan", manager.model_prompt_envelope_contract_plan),
            "model-permission-handoff-plan": ("AURA Model Permission Handoff Plan", manager.model_permission_handoff_plan),
            "model-response-envelope-contract-plan": ("AURA Model Response Envelope Contract Plan", manager.model_response_envelope_contract_plan),
            "model-error-boundary-plan": ("AURA Model Error Boundary Plan", manager.model_error_boundary_plan),
            "model-network-credential-boundary-plan": ("AURA Model Network Credential Boundary Plan", manager.model_network_credential_boundary_plan),
            "model-memory-command-boundary-plan": ("AURA Model Memory Command Boundary Plan", manager.model_memory_command_boundary_plan),
            "no-local-chat-model-adapter-unsafe-runtime-plan": ("AURA No Local Chat Model Adapter Unsafe Runtime Plan", manager.no_local_chat_model_adapter_unsafe_runtime_plan),
            "local-chat-model-adapter-next-sprint-readiness-plan": ("AURA Local Chat Model Adapter Next Sprint Readiness Plan", manager.local_chat_model_adapter_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_model_adapter_boundary_packet(title, handler(target))
            return True

        return False

    # Sprint 164.0 local chat persona response layer helpers.
    def print_local_chat_persona_response_layer_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Persona Response Layer Safety Boundary"))

    def handle_local_chat_persona_response_layer_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat persona response layer"
        manager = AuraLocalChatPersonaResponseLayerManager(project_root=self.project_root)

        if command in {"local-chat-persona-alpha", "local-chat-persona"}:
            if not target or target == "AURA local chat persona response layer":
                print("AURA Local Chat Persona Response Alpha")
                print("======================================")
                print('Usage: python3 main.py local-chat-persona-alpha "Aura siapa kamu?"')
                return True
            print(manager.render_persona_turn(target))
            return True

        if command == "local-chat-persona-response-layer-status":
            self.print_local_chat_persona_response_layer_packet("AURA Local Chat Persona Response Layer Status", manager.status())
            return True

        if command == "local-chat-persona-response-layer-context":
            self.print_local_chat_persona_response_layer_packet("AURA Local Chat Persona Response Layer Context", manager.context())
            return True

        command_map = {
            "local-chat-persona-response-runtime-plan": ("AURA Local Chat Persona Response Runtime Plan", manager.local_chat_persona_response_runtime_plan),
            "aura-persona-style-contract-plan": ("AURA Persona Style Contract Plan", manager.aura_persona_style_contract_plan),
            "persona-capability-honesty-plan": ("AURA Persona Capability Honesty Plan", manager.persona_capability_honesty_plan),
            "persona-action-decline-plan": ("AURA Persona Action Decline Plan", manager.persona_action_decline_plan),
            "persona-safety-boundary-plan": ("AURA Persona Safety Boundary Plan", manager.persona_safety_boundary_plan),
            "persona-message-store-link-plan": ("AURA Persona Message Store Link Plan", manager.persona_message_store_link_plan),
            "persona-model-boundary-plan": ("AURA Persona Model Boundary Plan", manager.persona_model_boundary_plan),
            "persona-memory-boundary-plan": ("AURA Persona Memory Boundary Plan", manager.persona_memory_boundary_plan),
            "no-local-chat-persona-unsafe-runtime-plan": ("AURA No Local Chat Persona Unsafe Runtime Plan", manager.no_local_chat_persona_unsafe_runtime_plan),
            "local-chat-persona-next-sprint-readiness-plan": ("AURA Local Chat Persona Next Sprint Readiness Plan", manager.local_chat_persona_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_persona_response_layer_packet(title, handler(target))
            return True

        return False

    # Sprint 163.0 local chat message store helpers.
    def print_local_chat_message_store_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Message Store Safety Boundary"))

    def handle_local_chat_message_store_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat message store"
        manager = AuraLocalChatMessageStoreManager(project_root=self.project_root)

        if command in {"local-chat-store-alpha", "local-chat-store"}:
            if not target or target == "AURA local chat message store":
                print("AURA Local Chat Message Store Alpha")
                print("===================================")
                print('Usage: python3 main.py local-chat-store-alpha "Aura simpan pesan ini"')
                return True
            print(manager.render_store_turn(target))
            return True

        if command == "local-chat-message-store-status":
            self.print_local_chat_message_store_packet("AURA Local Chat Message Store Status", manager.status())
            return True

        if command == "local-chat-message-store-context":
            self.print_local_chat_message_store_packet("AURA Local Chat Message Store Context", manager.context())
            return True

        command_map = {
            "local-chat-message-store-runtime-plan": ("AURA Local Chat Message Store Runtime Plan", manager.local_chat_message_store_runtime_plan),
            "local-chat-message-schema-plan": ("AURA Local Chat Message Schema Plan", manager.local_chat_message_schema_plan),
            "local-chat-store-path-policy-plan": ("AURA Local Chat Store Path Policy Plan", manager.local_chat_store_path_policy_plan),
            "local-chat-store-redaction-plan": ("AURA Local Chat Store Redaction Plan", manager.local_chat_store_redaction_plan),
            "local-chat-store-retention-plan": ("AURA Local Chat Store Retention Plan", manager.local_chat_store_retention_plan),
            "local-chat-store-cli-alpha-plan": ("AURA Local Chat Store CLI Alpha Plan", manager.local_chat_store_cli_alpha_plan),
            "local-chat-store-model-boundary-plan": ("AURA Local Chat Store Model Boundary Plan", manager.local_chat_store_model_boundary_plan),
            "local-chat-store-memory-boundary-plan": ("AURA Local Chat Store Memory Boundary Plan", manager.local_chat_store_memory_boundary_plan),
            "no-local-chat-message-store-unsafe-runtime-plan": ("AURA No Local Chat Message Store Unsafe Runtime Plan", manager.no_local_chat_message_store_unsafe_runtime_plan),
            "local-chat-message-store-next-sprint-readiness-plan": ("AURA Local Chat Message Store Next Sprint Readiness Plan", manager.local_chat_message_store_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_message_store_packet(title, handler(target))
            return True

        return False

    # Sprint 162.0 local chat CLI session alpha helpers.
    def print_local_chat_cli_session_alpha_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat CLI Session Alpha Safety Boundary"))

    def handle_local_chat_cli_session_alpha_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat CLI session alpha"
        manager = AuraLocalChatCliSessionAlphaManager(project_root=self.project_root)

        if command in {"local-chat-alpha", "local-chat"}:
            if not target or target == "AURA local chat CLI session alpha":
                print("AURA Local Chat CLI Alpha")
                print("===========================")
                print('Usage: python3 main.py local-chat-alpha "Aura kamu aktif?"')
                return True
            print(manager.render_alpha_turn(target))
            return True

        if command == "local-chat-cli-session-alpha-status":
            self.print_local_chat_cli_session_alpha_packet("AURA Local Chat CLI Session Alpha Status", manager.status())
            return True

        if command == "local-chat-cli-session-alpha-context":
            self.print_local_chat_cli_session_alpha_packet("AURA Local Chat CLI Session Alpha Context", manager.context())
            return True

        command_map = {
            "local-chat-alpha-session-runtime-plan": ("AURA Local Chat Alpha Session Runtime Plan", manager.local_chat_alpha_session_runtime_plan),
            "local-chat-alpha-message-acceptance-plan": ("AURA Local Chat Alpha Message Acceptance Plan", manager.local_chat_alpha_message_acceptance_plan),
            "local-chat-alpha-persona-response-plan": ("AURA Local Chat Alpha Persona Response Plan", manager.local_chat_alpha_persona_response_plan),
            "local-chat-alpha-transient-history-plan": ("AURA Local Chat Alpha Transient History Plan", manager.local_chat_alpha_transient_history_plan),
            "local-chat-alpha-command-safety-plan": ("AURA Local Chat Alpha Command Safety Plan", manager.local_chat_alpha_command_safety_plan),
            "local-chat-alpha-model-runtime-boundary-plan": ("AURA Local Chat Alpha Model Runtime Boundary Plan", manager.local_chat_alpha_model_runtime_boundary_plan),
            "local-chat-alpha-permission-audit-boundary-plan": ("AURA Local Chat Alpha Permission Audit Boundary Plan", manager.local_chat_alpha_permission_audit_boundary_plan),
            "local-chat-alpha-cli-usage-plan": ("AURA Local Chat Alpha CLI Usage Plan", manager.local_chat_alpha_cli_usage_plan),
            "no-local-chat-cli-alpha-unsafe-runtime-plan": ("AURA No Local Chat CLI Alpha Unsafe Runtime Plan", manager.no_local_chat_cli_alpha_unsafe_runtime_plan),
            "local-chat-alpha-next-sprint-readiness-plan": ("AURA Local Chat Alpha Next Sprint Readiness Plan", manager.local_chat_alpha_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_cli_session_alpha_packet(title, handler(target))
            return True

        return False

    # Sprint 161.0 local chat runtime foundation CLI helpers.
    def print_local_chat_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Runtime Foundation Safety Boundary"))

    def handle_local_chat_runtime_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local chat runtime foundation"
        manager = AuraLocalChatRuntimeFoundationManager(project_root=self.project_root)

        if command == "local-chat-runtime-foundation-status":
            self.print_local_chat_runtime_foundation_packet("AURA Local Chat Runtime Foundation Status", manager.status())
            return True

        if command == "local-chat-runtime-foundation-context":
            self.print_local_chat_runtime_foundation_packet("AURA Local Chat Runtime Foundation Context", manager.context())
            return True

        command_map = {
            "local-chat-session-contract-plan": ("AURA Local Chat Session Contract Plan", manager.local_chat_session_contract_plan),
            "local-chat-message-schema-plan": ("AURA Local Chat Message Schema Plan", manager.local_chat_message_schema_plan),
            "local-chat-loop-boundary-plan": ("AURA Local Chat Loop Boundary Plan", manager.local_chat_loop_boundary_plan),
            "aura-persona-response-boundary-plan": ("AURA Persona Response Boundary Plan", manager.aura_persona_response_boundary_plan),
            "local-chat-history-boundary-plan": ("AURA Local Chat History Boundary Plan", manager.local_chat_history_boundary_plan),
            "local-chat-permission-audit-link-plan": ("AURA Local Chat Permission Audit Link Plan", manager.local_chat_permission_audit_link_plan),
            "local-chat-model-adapter-boundary-plan": ("AURA Local Chat Model Adapter Boundary Plan", manager.local_chat_model_adapter_boundary_plan),
            "local-chat-cli-alpha-readiness-plan": ("AURA Local Chat CLI Alpha Readiness Plan", manager.local_chat_cli_alpha_readiness_plan),
            "no-local-chat-runtime-activation-plan": ("AURA No Local Chat Runtime Activation Plan", manager.no_local_chat_runtime_activation_plan),
            "local-chat-next-sprint-readiness-plan": ("AURA Local Chat Next Sprint Readiness Plan", manager.local_chat_next_sprint_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_chat_runtime_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 160.0 control center runtime review stabilization 151-160 CLI helpers.
    def print_control_center_runtime_review_stabilization_151_160_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Review Stabilization 151-160 Safety Boundary"))

    def handle_control_center_runtime_review_stabilization_151_160_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center runtime review stabilization 151-160"
        manager = AuraControlCenterRuntimeReviewStabilization151160Manager(project_root=self.project_root)

        if command == "control-center-runtime-review-stabilization-151-160-status":
            self.print_control_center_runtime_review_stabilization_151_160_packet("AURA Control Center Runtime Review Stabilization 151-160 Status", manager.status())
            return True

        if command == "control-center-runtime-review-stabilization-151-160-context":
            self.print_control_center_runtime_review_stabilization_151_160_packet("AURA Control Center Runtime Review Stabilization 151-160 Context", manager.context())
            return True

        command_map = {
            "control-center-block-completion-review-plan": ("AURA Control Center Block Completion Review Plan", manager.control_center_block_completion_review_plan),
            "control-center-panel-readiness-review-plan": ("AURA Control Center Panel Readiness Review Plan", manager.control_center_panel_readiness_review_plan),
            "control-center-runtime-boundary-review-plan": ("AURA Control Center Runtime Boundary Review Plan", manager.control_center_runtime_boundary_review_plan),
            "control-center-route-panel-integration-review-plan": ("AURA Control Center Route Panel Integration Review Plan", manager.control_center_route_panel_integration_review_plan),
            "control-center-read-only-data-contract-review-plan": ("AURA Control Center Read Only Data Contract Review Plan", manager.control_center_read_only_data_contract_review_plan),
            "control-center-permission-audit-link-review-plan": ("AURA Control Center Permission Audit Link Review Plan", manager.control_center_permission_audit_link_review_plan),
            "control-center-service-monitor-action-log-review-plan": ("AURA Control Center Service Monitor Action Log Review Plan", manager.control_center_service_monitor_action_log_review_plan),
            "control-center-security-accessibility-stabilization-plan": ("AURA Control Center Security Accessibility Stabilization Plan", manager.control_center_security_accessibility_stabilization_plan),
            "no-control-center-stabilization-runtime-activation-plan": ("AURA No Control Center Stabilization Runtime Activation Plan", manager.no_control_center_stabilization_runtime_activation_plan),
            "control-center-next-block-readiness-plan": ("AURA Control Center Next Block Readiness Plan", manager.control_center_next_block_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_runtime_review_stabilization_151_160_packet(title, handler(target))
            return True

        return False


    # Sprint 159.0 control center read-only route map foundation CLI helpers.
    def print_control_center_read_only_route_map_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Read-Only Route Map Foundation Safety Boundary"))

    def handle_control_center_read_only_route_map_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center read-only route map foundation"
        manager = AuraControlCenterReadOnlyRouteMapFoundationManager(project_root=self.project_root)

        if command == "control-center-read-only-route-map-foundation-status":
            self.print_control_center_read_only_route_map_foundation_packet("AURA Control Center Read-Only Route Map Foundation Status", manager.status())
            return True

        if command == "control-center-read-only-route-map-foundation-context":
            self.print_control_center_read_only_route_map_foundation_packet("AURA Control Center Read-Only Route Map Foundation Context", manager.context())
            return True

        command_map = {
            "route-map-layout-contract-plan": ("AURA Route Map Layout Contract Plan", manager.route_map_layout_contract_plan),
            "dashboard-navigation-surface-plan": ("AURA Dashboard Navigation Surface Plan", manager.dashboard_navigation_surface_plan),
            "route-definition-summary-plan": ("AURA Route Definition Summary Plan", manager.route_definition_summary_plan),
            "panel-crosslink-map-plan": ("AURA Panel Crosslink Map Plan", manager.panel_crosslink_map_plan),
            "route-guard-boundary-plan": ("AURA Route Guard Boundary Plan", manager.route_guard_boundary_plan),
            "route-map-filter-grouping-plan": ("AURA Route Map Filter Grouping Plan", manager.route_map_filter_grouping_plan),
            "route-map-empty-error-state-plan": ("AURA Route Map Empty Error State Plan", manager.route_map_empty_error_state_plan),
            "route-map-accessibility-security-review-plan": ("AURA Route Map Accessibility Security Review Plan", manager.route_map_accessibility_security_review_plan),
            "no-control-center-route-map-runtime-activation-plan": ("AURA No Control Center Route Map Runtime Activation Plan", manager.no_control_center_route_map_runtime_activation_plan),
            "route-map-next-stabilization-readiness-plan": ("AURA Route Map Next Stabilization Readiness Plan", manager.route_map_next_stabilization_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_read_only_route_map_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 158.0 control center action log panel foundation CLI helpers.
    def print_control_center_action_log_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Action Log Panel Foundation Safety Boundary"))

    def handle_control_center_action_log_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center action log panel foundation"
        manager = AuraControlCenterActionLogPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-action-log-panel-foundation-status":
            self.print_control_center_action_log_panel_foundation_packet("AURA Control Center Action Log Panel Foundation Status", manager.status())
            return True

        if command == "control-center-action-log-panel-foundation-context":
            self.print_control_center_action_log_panel_foundation_packet("AURA Control Center Action Log Panel Foundation Context", manager.context())
            return True

        command_map = {
            "action-log-layout-contract-plan": ("AURA Action Log Layout Contract Plan", manager.action_log_layout_contract_plan),
            "action-history-summary-surface-plan": ("AURA Action History Summary Surface Plan", manager.action_history_summary_surface_plan),
            "action-boundary-visibility-plan": ("AURA Action Boundary Visibility Plan", manager.action_boundary_visibility_plan),
            "plugin-action-linkage-surface-plan": ("AURA Plugin Action Linkage Surface Plan", manager.plugin_action_linkage_surface_plan),
            "permission-audit-linkage-summary-plan": ("AURA Permission Audit Linkage Summary Plan", manager.permission_audit_linkage_summary_plan),
            "action-log-filter-grouping-plan": ("AURA Action Log Filter Grouping Plan", manager.action_log_filter_grouping_plan),
            "action-log-redaction-privacy-boundary-plan": ("AURA Action Log Redaction Privacy Boundary Plan", manager.action_log_redaction_privacy_boundary_plan),
            "action-log-empty-error-state-plan": ("AURA Action Log Empty Error State Plan", manager.action_log_empty_error_state_plan),
            "action-log-accessibility-security-review-plan": ("AURA Action Log Accessibility Security Review Plan", manager.action_log_accessibility_security_review_plan),
            "no-control-center-action-log-panel-runtime-activation-plan": ("AURA No Control Center Action Log Panel Runtime Activation Plan", manager.no_control_center_action_log_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_action_log_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 157.0 control center service monitor panel foundation CLI helpers.
    def print_control_center_service_monitor_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Service Monitor Panel Foundation Safety Boundary"))

    def handle_control_center_service_monitor_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center service monitor panel foundation"
        manager = AuraControlCenterServiceMonitorPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-service-monitor-panel-foundation-status":
            self.print_control_center_service_monitor_panel_foundation_packet("AURA Control Center Service Monitor Panel Foundation Status", manager.status())
            return True

        if command == "control-center-service-monitor-panel-foundation-context":
            self.print_control_center_service_monitor_panel_foundation_packet("AURA Control Center Service Monitor Panel Foundation Context", manager.context())
            return True

        command_map = {
            "service-monitor-layout-contract-plan": ("AURA Service Monitor Layout Contract Plan", manager.service_monitor_layout_contract_plan),
            "service-runtime-state-summary-plan": ("AURA Service Runtime State Summary Plan", manager.service_runtime_state_summary_plan),
            "service-process-boundary-visibility-plan": ("AURA Service Process Boundary Visibility Plan", manager.service_process_boundary_visibility_plan),
            "service-health-signal-contract-plan": ("AURA Service Health Signal Contract Plan", manager.service_health_signal_contract_plan),
            "service-restart-recovery-status-plan": ("AURA Service Restart Recovery Status Plan", manager.service_restart_recovery_status_plan),
            "service-security-localhost-status-plan": ("AURA Service Security Localhost Status Plan", manager.service_security_localhost_status_plan),
            "service-monitor-filter-grouping-plan": ("AURA Service Monitor Filter Grouping Plan", manager.service_monitor_filter_grouping_plan),
            "service-monitor-error-boundary-plan": ("AURA Service Monitor Error Boundary Plan", manager.service_monitor_error_boundary_plan),
            "service-monitor-accessibility-security-review-plan": ("AURA Service Monitor Accessibility Security Review Plan", manager.service_monitor_accessibility_security_review_plan),
            "no-control-center-service-monitor-panel-runtime-activation-plan": ("AURA No Control Center Service Monitor Panel Runtime Activation Plan", manager.no_control_center_service_monitor_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_service_monitor_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 156.0 control center audit panel foundation CLI helpers.
    def print_control_center_audit_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Audit Panel Foundation Safety Boundary"))

    def handle_control_center_audit_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center audit panel foundation"
        manager = AuraControlCenterAuditPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-audit-panel-foundation-status":
            self.print_control_center_audit_panel_foundation_packet("AURA Control Center Audit Panel Foundation Status", manager.status())
            return True

        if command == "control-center-audit-panel-foundation-context":
            self.print_control_center_audit_panel_foundation_packet("AURA Control Center Audit Panel Foundation Context", manager.context())
            return True

        command_map = {
            "audit-panel-layout-contract-plan": ("AURA Audit Panel Layout Contract Plan", manager.audit_panel_layout_contract_plan),
            "audit-link-summary-contract-plan": ("AURA Audit Link Summary Contract Plan", manager.audit_link_summary_contract_plan),
            "audit-event-reference-contract-plan": ("AURA Audit Event Reference Contract Plan", manager.audit_event_reference_contract_plan),
            "audit-log-boundary-visibility-plan": ("AURA Audit Log Boundary Visibility Plan", manager.audit_log_boundary_visibility_plan),
            "audit-trace-chain-summary-plan": ("AURA Audit Trace Chain Summary Plan", manager.audit_trace_chain_summary_plan),
            "audit-retention-redaction-boundary-plan": ("AURA Audit Retention Redaction Boundary Plan", manager.audit_retention_redaction_boundary_plan),
            "audit-filter-grouping-plan": ("AURA Audit Filter Grouping Plan", manager.audit_filter_grouping_plan),
            "audit-panel-error-boundary-plan": ("AURA Audit Panel Error Boundary Plan", manager.audit_panel_error_boundary_plan),
            "audit-panel-accessibility-security-review-plan": ("AURA Audit Panel Accessibility Security Review Plan", manager.audit_panel_accessibility_security_review_plan),
            "no-control-center-audit-panel-runtime-activation-plan": ("AURA No Control Center Audit Panel Runtime Activation Plan", manager.no_control_center_audit_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_audit_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 155.0 control center permission panel foundation CLI helpers.
    def print_control_center_permission_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Permission Panel Foundation Safety Boundary"))

    def handle_control_center_permission_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center permission panel foundation"
        manager = AuraControlCenterPermissionPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-permission-panel-foundation-status":
            self.print_control_center_permission_panel_foundation_packet("AURA Control Center Permission Panel Foundation Status", manager.status())
            return True

        if command == "control-center-permission-panel-foundation-context":
            self.print_control_center_permission_panel_foundation_packet("AURA Control Center Permission Panel Foundation Context", manager.context())
            return True

        command_map = {
            "permission-panel-layout-contract-plan": ("AURA Permission Panel Layout Contract Plan", manager.permission_panel_layout_contract_plan),
            "permission-request-summary-contract-plan": ("AURA Permission Request Summary Contract Plan", manager.permission_request_summary_contract_plan),
            "permission-grant-boundary-visibility-plan": ("AURA Permission Grant Boundary Visibility Plan", manager.permission_grant_boundary_visibility_plan),
            "permission-risk-badge-semantics-plan": ("AURA Permission Risk Badge Semantics Plan", manager.permission_risk_badge_semantics_plan),
            "permission-filter-grouping-plan": ("AURA Permission Filter Grouping Plan", manager.permission_filter_grouping_plan),
            "permission-panel-error-boundary-plan": ("AURA Permission Panel Error Boundary Plan", manager.permission_panel_error_boundary_plan),
            "permission-panel-accessibility-contract-plan": ("AURA Permission Panel Accessibility Contract Plan", manager.permission_panel_accessibility_contract_plan),
            "permission-panel-security-review-plan": ("AURA Permission Panel Security Review Plan", manager.permission_panel_security_review_plan),
            "permission-panel-next-audit-viewer-readiness-plan": ("AURA Permission Panel Next Audit Viewer Readiness Plan", manager.permission_panel_next_audit_viewer_readiness_plan),
            "no-control-center-permission-panel-runtime-activation-plan": ("AURA No Control Center Permission Panel Runtime Activation Plan", manager.no_control_center_permission_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_permission_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 154.0 control center plugin panel foundation CLI helpers.
    def print_control_center_plugin_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Plugin Panel Foundation Safety Boundary"))

    def handle_control_center_plugin_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center plugin panel foundation"
        manager = AuraControlCenterPluginPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-plugin-panel-foundation-status":
            self.print_control_center_plugin_panel_foundation_packet("AURA Control Center Plugin Panel Foundation Status", manager.status())
            return True

        if command == "control-center-plugin-panel-foundation-context":
            self.print_control_center_plugin_panel_foundation_packet("AURA Control Center Plugin Panel Foundation Context", manager.context())
            return True

        command_map = {
            "plugin-panel-layout-contract-plan": ("AURA Plugin Panel Layout Contract Plan", manager.plugin_panel_layout_contract_plan),
            "plugin-registry-summary-contract-plan": ("AURA Plugin Registry Summary Contract Plan", manager.plugin_registry_summary_contract_plan),
            "plugin-action-status-semantics-plan": ("AURA Plugin Action Status Semantics Plan", manager.plugin_action_status_semantics_plan),
            "plugin-permission-boundary-visibility-plan": ("AURA Plugin Permission Boundary Visibility Plan", manager.plugin_permission_boundary_visibility_plan),
            "plugin-filter-grouping-plan": ("AURA Plugin Filter Grouping Plan", manager.plugin_filter_grouping_plan),
            "plugin-panel-error-boundary-plan": ("AURA Plugin Panel Error Boundary Plan", manager.plugin_panel_error_boundary_plan),
            "plugin-panel-accessibility-contract-plan": ("AURA Plugin Panel Accessibility Contract Plan", manager.plugin_panel_accessibility_contract_plan),
            "plugin-panel-security-review-plan": ("AURA Plugin Panel Security Review Plan", manager.plugin_panel_security_review_plan),
            "plugin-panel-next-service-monitor-readiness-plan": ("AURA Plugin Panel Next Service Monitor Readiness Plan", manager.plugin_panel_next_service_monitor_readiness_plan),
            "no-control-center-plugin-panel-runtime-activation-plan": ("AURA No Control Center Plugin Panel Runtime Activation Plan", manager.no_control_center_plugin_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_plugin_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 153.0 control center capability viewer foundation CLI helpers.
    def print_control_center_capability_viewer_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Capability Viewer Foundation Safety Boundary"))

    def handle_control_center_capability_viewer_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center capability viewer foundation"
        manager = AuraControlCenterCapabilityViewerFoundationManager(project_root=self.project_root)

        if command == "control-center-capability-viewer-foundation-status":
            self.print_control_center_capability_viewer_foundation_packet("AURA Control Center Capability Viewer Foundation Status", manager.status())
            return True

        if command == "control-center-capability-viewer-foundation-context":
            self.print_control_center_capability_viewer_foundation_packet("AURA Control Center Capability Viewer Foundation Context", manager.context())
            return True

        command_map = {
            "capability-viewer-layout-contract-plan": ("AURA Capability Viewer Layout Contract Plan", manager.capability_viewer_layout_contract_plan),
            "capability-registry-summary-contract-plan": ("AURA Capability Registry Summary Contract Plan", manager.capability_registry_summary_contract_plan),
            "capability-state-indicator-semantics-plan": ("AURA Capability State Indicator Semantics Plan", manager.capability_state_indicator_semantics_plan),
            "capability-filter-grouping-plan": ("AURA Capability Filter Grouping Plan", manager.capability_filter_grouping_plan),
            "capability-runtime-boundary-visibility-plan": ("AURA Capability Runtime Boundary Visibility Plan", manager.capability_runtime_boundary_visibility_plan),
            "capability-permission-audit-visibility-plan": ("AURA Capability Permission Audit Visibility Plan", manager.capability_permission_audit_visibility_plan),
            "capability-viewer-error-boundary-plan": ("AURA Capability Viewer Error Boundary Plan", manager.capability_viewer_error_boundary_plan),
            "capability-viewer-accessibility-contract-plan": ("AURA Capability Viewer Accessibility Contract Plan", manager.capability_viewer_accessibility_contract_plan),
            "capability-viewer-next-service-monitor-readiness-plan": ("AURA Capability Viewer Next Service Monitor Readiness Plan", manager.capability_viewer_next_service_monitor_readiness_plan),
            "no-control-center-capability-viewer-runtime-activation-plan": ("AURA No Control Center Capability Viewer Runtime Activation Plan", manager.no_control_center_capability_viewer_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_capability_viewer_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 152.0 control center read-only status panel foundation CLI helpers.
    def print_control_center_read_only_status_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Read-Only Status Panel Foundation Safety Boundary"))

    def handle_control_center_read_only_status_panel_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center read-only status panel foundation"
        manager = AuraControlCenterReadOnlyStatusPanelFoundationManager(project_root=self.project_root)

        if command == "control-center-read-only-status-panel-foundation-status":
            self.print_control_center_read_only_status_panel_foundation_packet("AURA Control Center Read-Only Status Panel Foundation Status", manager.status())
            return True

        if command == "control-center-read-only-status-panel-foundation-context":
            self.print_control_center_read_only_status_panel_foundation_packet("AURA Control Center Read-Only Status Panel Foundation Context", manager.context())
            return True

        command_map = {
            "status-panel-layout-contract-plan": ("AURA Status Panel Layout Contract Plan", manager.status_panel_layout_contract_plan),
            "status-summary-data-contract-plan": ("AURA Status Summary Data Contract Plan", manager.status_summary_data_contract_plan),
            "status-indicator-semantics-plan": ("AURA Status Indicator Semantics Plan", manager.status_indicator_semantics_plan),
            "status-panel-safe-idle-state-plan": ("AURA Status Panel Safe Idle State Plan", manager.status_panel_safe_idle_state_plan),
            "status-panel-error-boundary-plan": ("AURA Status Panel Error Boundary Plan", manager.status_panel_error_boundary_plan),
            "status-panel-refresh-policy-review-plan": ("AURA Status Panel Refresh Policy Review Plan", manager.status_panel_refresh_policy_review_plan),
            "status-panel-accessibility-contract-plan": ("AURA Status Panel Accessibility Contract Plan", manager.status_panel_accessibility_contract_plan),
            "status-panel-security-boundary-plan": ("AURA Status Panel Security Boundary Plan", manager.status_panel_security_boundary_plan),
            "status-panel-next-capability-viewer-readiness-plan": ("AURA Status Panel Next Capability Viewer Readiness Plan", manager.status_panel_next_capability_viewer_readiness_plan),
            "no-control-center-status-panel-runtime-activation-plan": ("AURA No Control Center Status Panel Runtime Activation Plan", manager.no_control_center_status_panel_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_read_only_status_panel_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 151.0 control center runtime foundation CLI helpers.
    def print_control_center_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Foundation Safety Boundary"))

    def handle_control_center_runtime_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA control center runtime foundation"
        manager = AuraControlCenterRuntimeFoundationManager(project_root=self.project_root)

        if command == "control-center-runtime-foundation-status":
            self.print_control_center_runtime_foundation_packet("AURA Control Center Runtime Foundation Status", manager.status())
            return True

        if command == "control-center-runtime-foundation-context":
            self.print_control_center_runtime_foundation_packet("AURA Control Center Runtime Foundation Context", manager.context())
            return True

        command_map = {
            "control-center-runtime-shell-contract-plan": ("AURA Control Center Runtime Shell Contract Plan", manager.control_center_runtime_shell_contract_plan),
            "control-center-localhost-entry-boundary-plan": ("AURA Control Center Localhost Entry Boundary Plan", manager.control_center_localhost_entry_boundary_plan),
            "control-center-read-only-panel-manifest-plan": ("AURA Control Center Read-Only Panel Manifest Plan", manager.control_center_read_only_panel_manifest_plan),
            "control-center-route-blueprint-plan": ("AURA Control Center Route Blueprint Plan", manager.control_center_route_blueprint_plan),
            "control-center-data-source-contract-plan": ("AURA Control Center Data Source Contract Plan", manager.control_center_data_source_contract_plan),
            "control-center-permission-audit-link-plan": ("AURA Control Center Permission Audit Link Plan", manager.control_center_permission_audit_link_plan),
            "control-center-safe-idle-error-boundary-plan": ("AURA Control Center Safe Idle Error Boundary Plan", manager.control_center_safe_idle_error_boundary_plan),
            "control-center-security-review-plan": ("AURA Control Center Security Review Plan", manager.control_center_security_review_plan),
            "control-center-next-panel-readiness-plan": ("AURA Control Center Next Panel Readiness Plan", manager.control_center_next_panel_readiness_plan),
            "no-control-center-runtime-activation-plan": ("AURA No Control Center Runtime Activation Plan", manager.no_control_center_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_runtime_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 150.0 service review stabilization 141-150 CLI helpers.
    def print_service_review_stabilization_141_150_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Review Stabilization 141-150 Safety Boundary"))

    def handle_service_review_stabilization_141_150_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service review stabilization 141-150"
        manager = AuraServiceReviewStabilization141150Manager(project_root=self.project_root)

        if command == "service-review-stabilization-141-150-status":
            self.print_service_review_stabilization_141_150_packet("AURA Service Review Stabilization 141-150 Status", manager.status())
            return True

        if command == "service-review-stabilization-141-150-context":
            self.print_service_review_stabilization_141_150_packet("AURA Service Review Stabilization 141-150 Context", manager.context())
            return True

        command_map = {
            "service-141-150-completion-review-plan": ("AURA Service 141-150 Completion Review Plan", manager.service_141_150_completion_review_plan),
            "service-runtime-zero-counter-review-plan": ("AURA Service Runtime Zero Counter Review Plan", manager.service_runtime_zero_counter_review_plan),
            "service-permission-audit-security-review-plan": ("AURA Service Permission Audit Security Review Plan", manager.service_permission_audit_security_review_plan),
            "service-control-health-config-review-plan": ("AURA Service Control Health Config Review Plan", manager.service_control_health_config_review_plan),
            "service-recovery-security-review-plan": ("AURA Service Recovery Security Review Plan", manager.service_recovery_security_review_plan),
            "service-capability-registry-stabilization-plan": ("AURA Service Capability Registry Stabilization Plan", manager.service_capability_registry_stabilization_plan),
            "service-documentation-roadmap-stabilization-plan": ("AURA Service Documentation Roadmap Stabilization Plan", manager.service_documentation_roadmap_stabilization_plan),
            "service-next-block-readiness-plan": ("AURA Service Next Block Readiness Plan", manager.service_next_block_readiness_plan),
            "service-release-gate-continuity-review-plan": ("AURA Service Release Gate Continuity Review Plan", manager.service_release_gate_continuity_review_plan),
            "no-service-stabilization-runtime-activation-plan": ("AURA No Service Stabilization Runtime Activation Plan", manager.no_service_stabilization_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_review_stabilization_141_150_packet(title, handler(target))
            return True

        return False


    # Sprint 149.0 service security and localhost binding review CLI helpers.
    def print_service_security_localhost_binding_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Security and Localhost Binding Review Safety Boundary"))

    def handle_service_security_localhost_binding_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service security and localhost binding review"
        manager = AuraServiceSecurityLocalhostBindingReviewManager(project_root=self.project_root)

        if command == "service-security-localhost-binding-review-status":
            self.print_service_security_localhost_binding_review_packet("AURA Service Security and Localhost Binding Review Status", manager.status())
            return True

        if command == "service-security-localhost-binding-review-context":
            self.print_service_security_localhost_binding_review_packet("AURA Service Security and Localhost Binding Review Context", manager.context())
            return True

        command_map = {
            "service-localhost-binding-policy-plan": ("AURA Service Localhost Binding Policy Plan", manager.service_localhost_binding_policy_plan),
            "service-public-network-exposure-block-plan": ("AURA Service Public Network Exposure Block Plan", manager.service_public_network_exposure_block_plan),
            "service-origin-host-allowlist-policy-plan": ("AURA Service Origin Host Allowlist Policy Plan", manager.service_origin_host_allowlist_policy_plan),
            "service-loopback-interface-policy-plan": ("AURA Service Loopback Interface Policy Plan", manager.service_loopback_interface_policy_plan),
            "service-tls-cors-external-access-defer-plan": ("AURA Service TLS CORS External Access Defer Plan", manager.service_tls_cors_external_access_defer_plan),
            "service-security-permission-audit-link-plan": ("AURA Service Security Permission Audit Link Plan", manager.service_security_permission_audit_link_plan),
            "service-port-binding-preflight-security-plan": ("AURA Service Port Binding Preflight Security Plan", manager.service_port_binding_preflight_security_plan),
            "service-control-center-security-surface-plan": ("AURA Service Control Center Security Surface Plan", manager.service_control_center_security_surface_plan),
            "service-security-error-boundary-plan": ("AURA Service Security Error Boundary Plan", manager.service_security_error_boundary_plan),
            "no-security-localhost-runtime-activation-plan": ("AURA No Security Localhost Runtime Activation Plan", manager.no_security_localhost_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_security_localhost_binding_review_packet(title, handler(target))
            return True

        return False


    # Sprint 148.0 service recovery and restart policy foundation CLI helpers.
    def print_service_recovery_restart_policy_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Recovery and Restart Policy Foundation Safety Boundary"))

    def handle_service_recovery_restart_policy_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service recovery and restart policy foundation"
        manager = AuraServiceRecoveryRestartPolicyFoundationManager(project_root=self.project_root)

        if command == "service-recovery-restart-policy-foundation-status":
            self.print_service_recovery_restart_policy_foundation_packet("AURA Service Recovery and Restart Policy Foundation Status", manager.status())
            return True

        if command == "service-recovery-restart-policy-foundation-context":
            self.print_service_recovery_restart_policy_foundation_packet("AURA Service Recovery and Restart Policy Foundation Context", manager.context())
            return True

        command_map = {
            "service-failure-classification-plan": ("AURA Service Failure Classification Plan", manager.service_failure_classification_plan),
            "service-safe-idle-recovery-policy-plan": ("AURA Service Safe Idle Recovery Policy Plan", manager.service_safe_idle_recovery_policy_plan),
            "service-restart-approval-policy-plan": ("AURA Service Restart Approval Policy Plan", manager.service_restart_approval_policy_plan),
            "service-retry-cooldown-policy-plan": ("AURA Service Retry Cooldown Policy Plan", manager.service_retry_cooldown_policy_plan),
            "service-rollback-visibility-plan": ("AURA Service Rollback Visibility Plan", manager.service_rollback_visibility_plan),
            "service-recovery-audit-link-plan": ("AURA Service Recovery Audit Link Plan", manager.service_recovery_audit_link_plan),
            "service-recovery-permission-boundary-plan": ("AURA Service Recovery Permission Boundary Plan", manager.service_recovery_permission_boundary_plan),
            "service-control-center-recovery-surface-plan": ("AURA Service Control Center Recovery Surface Plan", manager.service_control_center_recovery_surface_plan),
            "service-recovery-error-boundary-plan": ("AURA Service Recovery Error Boundary Plan", manager.service_recovery_error_boundary_plan),
            "no-recovery-restart-runtime-activation-plan": ("AURA No Recovery Restart Runtime Activation Plan", manager.no_recovery_restart_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_recovery_restart_policy_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 147.0 service control command review foundation CLI helpers.
    def print_service_control_command_review_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Control Command Review Foundation Safety Boundary"))

    def handle_service_control_command_review_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service control command review foundation"
        manager = AuraServiceControlCommandReviewFoundationManager(project_root=self.project_root)

        if command == "service-control-command-review-foundation-status":
            self.print_service_control_command_review_foundation_packet("AURA Service Control Command Review Foundation Status", manager.status())
            return True

        if command == "service-control-command-review-foundation-context":
            self.print_service_control_command_review_foundation_packet("AURA Service Control Command Review Foundation Context", manager.context())
            return True

        command_map = {
            "service-control-scope-catalog-plan": ("AURA Service Control Scope Catalog Plan", manager.service_control_scope_catalog_plan),
            "service-start-command-review-plan": ("AURA Service Start Command Review Plan", manager.service_start_command_review_plan),
            "service-stop-command-review-plan": ("AURA Service Stop Command Review Plan", manager.service_stop_command_review_plan),
            "service-restart-command-review-plan": ("AURA Service Restart Command Review Plan", manager.service_restart_command_review_plan),
            "service-status-command-review-plan": ("AURA Service Status Command Review Plan", manager.service_status_command_review_plan),
            "service-control-permission-boundary-plan": ("AURA Service Control Permission Boundary Plan", manager.service_control_permission_boundary_plan),
            "service-control-audit-link-plan": ("AURA Service Control Audit Link Plan", manager.service_control_audit_link_plan),
            "service-control-center-command-surface-plan": ("AURA Service Control Center Command Surface Plan", manager.service_control_center_command_surface_plan),
            "service-control-failure-safe-idle-plan": ("AURA Service Control Failure Safe Idle Plan", manager.service_control_failure_safe_idle_plan),
            "no-service-control-command-runtime-activation-plan": ("AURA No Service Control Command Runtime Activation Plan", manager.no_service_control_command_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_control_command_review_foundation_packet(title, handler(target))
            return True

        return False


    # Sprint 146.0 service audit link foundation CLI helpers.
    def print_service_audit_link_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Audit Link Foundation Safety Boundary"))

    def handle_service_audit_link_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service audit link foundation"
        manager = AuraServiceAuditLinkFoundationManager(project_root=self.project_root)

        if command == "service-audit-link-foundation-status":
            self.print_service_audit_link_foundation_packet("AURA Service Audit Link Foundation Status", manager.status())
            return True

        if command == "service-audit-link-foundation-context":
            self.print_service_audit_link_foundation_packet("AURA Service Audit Link Foundation Context", manager.context())
            return True

        command_map = {
            "service-audit-event-reference-plan": ("AURA Service Audit Event Reference Plan", manager.service_audit_event_reference_plan),
            "service-audit-link-contract-plan": ("AURA Service Audit Link Contract Plan", manager.service_audit_link_contract_plan),
            "service-audit-traceability-chain-plan": ("AURA Service Audit Traceability Chain Plan", manager.service_audit_traceability_chain_plan),
            "service-audit-permission-link-plan": ("AURA Service Audit Permission Link Plan", manager.service_audit_permission_link_plan),
            "service-audit-control-center-surface-plan": ("AURA Service Audit Control Center Surface Plan", manager.service_audit_control_center_surface_plan),
            "service-audit-redaction-boundary-plan": ("AURA Service Audit Redaction Boundary Plan", manager.service_audit_redaction_boundary_plan),
            "service-audit-failure-safe-idle-plan": ("AURA Service Audit Failure Safe Idle Plan", manager.service_audit_failure_safe_idle_plan),
            "service-audit-retention-boundary-plan": ("AURA Service Audit Retention Boundary Plan", manager.service_audit_retention_boundary_plan),
            "service-audit-error-boundary-plan": ("AURA Service Audit Error Boundary Plan", manager.service_audit_error_boundary_plan),
            "no-audit-link-runtime-activation-plan": ("AURA No Audit Link Runtime Activation Plan", manager.no_audit_link_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_audit_link_foundation_packet(title, handler(target))
            return True

        return False



    # Sprint 145.0 service permission gate runtime boundary CLI helpers.
    def print_service_permission_gate_runtime_boundary_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Permission Gate Runtime Boundary Safety Boundary"))

    def handle_service_permission_gate_runtime_boundary_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA service permission gate runtime boundary"
        manager = AuraServicePermissionGateRuntimeBoundaryManager(project_root=self.project_root)

        if command == "service-permission-gate-runtime-boundary-status":
            self.print_service_permission_gate_runtime_boundary_packet("AURA Service Permission Gate Runtime Boundary Status", manager.status())
            return True

        if command == "service-permission-gate-runtime-boundary-context":
            self.print_service_permission_gate_runtime_boundary_packet("AURA Service Permission Gate Runtime Boundary Context", manager.context())
            return True

        command_map = {
            "service-permission-scope-catalog-plan": ("AURA Service Permission Scope Catalog Plan", manager.service_permission_scope_catalog_plan),
            "service-permission-request-contract-plan": ("AURA Service Permission Request Contract Plan", manager.service_permission_request_contract_plan),
            "service-permission-grant-preflight-plan": ("AURA Service Permission Grant Preflight Plan", manager.service_permission_grant_preflight_plan),
            "service-permission-denial-safe-idle-plan": ("AURA Service Permission Denial Safe Idle Plan", manager.service_permission_denial_safe_idle_plan),
            "service-permission-control-center-surface-plan": ("AURA Service Permission Control Center Surface Plan", manager.service_permission_control_center_surface_plan),
            "service-permission-audit-link-plan": ("AURA Service Permission Audit Link Plan", manager.service_permission_audit_link_plan),
            "service-permission-expiry-review-plan": ("AURA Service Permission Expiry Review Plan", manager.service_permission_expiry_review_plan),
            "service-permission-error-boundary-plan": ("AURA Service Permission Error Boundary Plan", manager.service_permission_error_boundary_plan),
            "service-permission-manual-approval-boundary-plan": ("AURA Service Permission Manual Approval Boundary Plan", manager.service_permission_manual_approval_boundary_plan),
            "no-permission-runtime-activation-plan": ("AURA No Permission Runtime Activation Plan", manager.no_permission_runtime_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_service_permission_gate_runtime_boundary_packet(title, handler(target))
            return True

        return False
    # Sprint 143.0 local service health endpoint foundation CLI helpers.
    def print_local_service_health_endpoint_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Health Endpoint Foundation Safety Boundary"))

    def handle_local_service_health_endpoint_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local service health endpoint foundation"
        manager = AuraLocalServiceHealthEndpointFoundationManager(project_root=self.project_root)

        if command == "local-service-health-endpoint-foundation-status":
            self.print_local_service_health_endpoint_foundation_packet("AURA Local Service Health Endpoint Foundation Status", manager.status())
            return True

        if command == "local-service-health-endpoint-foundation-context":
            self.print_local_service_health_endpoint_foundation_packet("AURA Local Service Health Endpoint Foundation Context", manager.context())
            return True

        command_map = {
            "health-endpoint-scope-plan": ("AURA Health Endpoint Scope Plan", manager.health_endpoint_scope_plan),
            "health-endpoint-contract-plan": ("AURA Health Endpoint Contract Plan", manager.health_endpoint_contract_plan),
            "health-response-schema-plan": ("AURA Health Response Schema Plan", manager.health_response_schema_plan),
            "localhost-health-binding-boundary-plan": ("AURA Localhost Health Binding Boundary Plan", manager.localhost_health_binding_boundary_plan),
            "safe-idle-health-state-plan": ("AURA Safe Idle Health State Plan", manager.safe_idle_health_state_plan),
            "health-dependency-visibility-plan": ("AURA Health Dependency Visibility Plan", manager.health_dependency_visibility_plan),
            "permission-audit-health-link-plan": ("AURA Permission Audit Health Link Plan", manager.permission_audit_health_link_plan),
            "control-center-health-card-plan": ("AURA Control Center Health Card Plan", manager.control_center_health_card_plan),
            "health-error-fallback-plan": ("AURA Health Error Fallback Plan", manager.health_error_fallback_plan),
            "no-health-endpoint-activation-plan": ("AURA No Health Endpoint Activation Plan", manager.no_health_endpoint_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_health_endpoint_foundation_packet(title, handler(target))
            return True

        return False
    def print_local_service_safe_idle_boot_boundary_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Safe Idle Boot Boundary Safety Boundary"))

    def handle_local_service_safe_idle_boot_boundary_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local service safe idle boot boundary"
        manager = AuraLocalServiceSafeIdleBootBoundaryManager(project_root=self.project_root)

        if command == "local-service-safe-idle-boot-boundary-status":
            self.print_local_service_safe_idle_boot_boundary_packet("AURA Local Service Safe Idle Boot Boundary Status", manager.status())
            return True

        if command == "local-service-safe-idle-boot-boundary-context":
            self.print_local_service_safe_idle_boot_boundary_packet("AURA Local Service Safe Idle Boot Boundary Context", manager.context())
            return True

        command_map = {
            "safe-idle-boot-scope-plan": ("AURA Safe Idle Boot Scope Plan", manager.safe_idle_boot_scope_plan),
            "boot-entry-state-contract-plan": ("AURA Boot Entry State Contract Plan", manager.boot_entry_state_contract_plan),
            "safe-idle-guard-condition-plan": ("AURA Safe Idle Guard Condition Plan", manager.safe_idle_guard_condition_plan),
            "boot-failure-fallback-plan": ("AURA Boot Failure Fallback Plan", manager.boot_failure_fallback_plan),
            "service-no-autostart-boundary-plan": ("AURA Service No-Autostart Boundary Plan", manager.service_no_autostart_boundary_plan),
            "readiness-probe-read-only-plan": ("AURA Readiness Probe Read-Only Plan", manager.readiness_probe_read_only_plan),
            "control-center-idle-visibility-plan": ("AURA Control Center Idle Visibility Plan", manager.control_center_idle_visibility_plan),
            "permission-denial-idle-plan": ("AURA Permission Denial Idle Plan", manager.permission_denial_idle_plan),
            "audit-failure-idle-plan": ("AURA Audit Failure Idle Plan", manager.audit_failure_idle_plan),
            "no-boot-activation-plan": ("AURA No Boot Activation Plan", manager.no_boot_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_safe_idle_boot_boundary_packet(title, handler(target))
            return True

        return False

    # Sprint 141.0 local service runtime foundation CLI helpers.
    def print_local_service_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Runtime Foundation Safety Boundary"))

    def handle_local_service_runtime_foundation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local service runtime foundation"
        manager = AuraLocalServiceRuntimeFoundationManager(project_root=self.project_root)

        if command == "local-service-runtime-foundation-status":
            self.print_local_service_runtime_foundation_packet("AURA Local Service Runtime Foundation Status", manager.status())
            return True

        if command == "local-service-runtime-foundation-context":
            self.print_local_service_runtime_foundation_packet("AURA Local Service Runtime Foundation Context", manager.context())
            return True

        command_map = {
            "service-foundation-scope-plan": ("AURA Service Foundation Scope Plan", manager.service_foundation_scope_plan),
            "service-safe-idle-entry-plan": ("AURA Service Safe Idle Entry Plan", manager.service_safe_idle_entry_plan),
            "localhost-binding-boundary-plan": ("AURA Localhost Binding Boundary Plan", manager.localhost_binding_boundary_plan),
            "service-lifecycle-state-plan": ("AURA Service Lifecycle State Plan", manager.service_lifecycle_state_plan),
            "service-config-contract-plan": ("AURA Service Config Contract Plan", manager.service_config_contract_plan),
            "service-health-surface-plan": ("AURA Service Health Surface Plan", manager.service_health_surface_plan),
            "service-permission-gate-link-plan": ("AURA Service Permission Gate Link Plan", manager.service_permission_gate_link_plan),
            "service-audit-link-plan": ("AURA Service Audit Link Plan", manager.service_audit_link_plan),
            "service-control-command-boundary-plan": ("AURA Service Control Command Boundary Plan", manager.service_control_command_boundary_plan),
            "service-no-start-activation-plan": ("AURA Service No-Start Activation Plan", manager.service_no_start_activation_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_runtime_foundation_packet(title, handler(target))
            return True

        return False

    # Sprint 140.0 review stabilization 131-140 CLI helpers.
    def print_review_stabilization_131_140_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 131-140 Safety Boundary"))

    def handle_review_stabilization_131_140_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA review stabilization 131-140"
        manager = AuraReviewStabilization131140FoundationManager(project_root=self.project_root)

        if command == "review-stabilization-131-140-status":
            self.print_review_stabilization_131_140_packet("AURA Review Stabilization 131-140 Foundation Status", manager.status())
            return True

        if command == "review-stabilization-131-140-context":
            self.print_review_stabilization_131_140_packet("AURA Review Stabilization 131-140 Foundation Context", manager.context())
            return True

        command_map = {
            "sprint-131-140-scope-review-plan": ("AURA Sprint 131-140 Scope Review Plan", manager.sprint_131_140_scope_review_plan),
            "runtime-boundary-integrity-review-plan": ("AURA Runtime Boundary Integrity Review Plan", manager.runtime_boundary_integrity_review_plan),
            "capability-registry-consistency-review-plan": ("AURA Capability Registry Consistency Review Plan", manager.capability_registry_consistency_review_plan),
            "system-status-surface-review-plan": ("AURA System Status Surface Review Plan", manager.system_status_surface_review_plan),
            "skill-plugin-cli-shell-review-plan": ("AURA Skill Plugin CLI Shell Review Plan", manager.skill_plugin_cli_shell_review_plan),
            "documentation-roadmap-review-plan": ("AURA Documentation Roadmap Review Plan", manager.documentation_roadmap_review_plan),
            "safety-counter-zero-review-plan": ("AURA Safety Counter Zero Review Plan", manager.safety_counter_zero_review_plan),
            "git-boot-verification-review-plan": ("AURA Git Boot Verification Review Plan", manager.git_boot_verification_review_plan),
            "next-block-readiness-review-plan": ("AURA Next Block Readiness Review Plan", manager.next_block_readiness_review_plan),
            "no-runtime-activation-review-plan": ("AURA No Runtime Activation Review Plan", manager.no_runtime_activation_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_review_stabilization_131_140_packet(title, handler(target))
            return True

        return False

    # Sprint 139.0 audit runtime writer activation review CLI helpers.
    def print_audit_runtime_writer_activation_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Audit Runtime Writer Activation Review Safety Boundary"))

    def handle_audit_runtime_writer_activation_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA audit runtime writer activation review"
        manager = AuraAuditRuntimeWriterActivationReviewFoundationManager(project_root=self.project_root)

        if command == "audit-runtime-writer-activation-review-status":
            self.print_audit_runtime_writer_activation_review_packet("AURA Audit Runtime Writer Activation Review Foundation Status", manager.status())
            return True

        if command == "audit-runtime-writer-activation-review-context":
            self.print_audit_runtime_writer_activation_review_packet("AURA Audit Runtime Writer Activation Review Foundation Context", manager.context())
            return True

        command_map = {
            "audit-writer-activation-scope-review-plan": ("AURA Audit Writer Activation Scope Review Plan", manager.audit_writer_activation_scope_review_plan),
            "audit-event-schema-review-plan": ("AURA Audit Event Schema Review Plan", manager.audit_event_schema_review_plan),
            "audit-append-only-storage-review-plan": ("AURA Audit Append Only Storage Review Plan", manager.audit_append_only_storage_review_plan),
            "audit-redaction-boundary-review-plan": ("AURA Audit Redaction Boundary Review Plan", manager.audit_redaction_boundary_review_plan),
            "audit-actor-context-review-plan": ("AURA Audit Actor Context Review Plan", manager.audit_actor_context_review_plan),
            "audit-permission-link-review-plan": ("AURA Audit Permission Link Review Plan", manager.audit_permission_link_review_plan),
            "audit-dashboard-visibility-review-plan": ("AURA Audit Dashboard Visibility Review Plan", manager.audit_dashboard_visibility_review_plan),
            "audit-failure-safe-idle-review-plan": ("AURA Audit Failure Safe Idle Review Plan", manager.audit_failure_safe_idle_review_plan),
            "audit-retention-export-review-plan": ("AURA Audit Retention Export Review Plan", manager.audit_retention_export_review_plan),
            "audit-no-write-activation-review-plan": ("AURA Audit No Write Activation Review Plan", manager.audit_no_write_activation_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_audit_runtime_writer_activation_review_packet(title, handler(target))
            return True

        return False

    # Sprint 138.0 permission runtime grant gate review CLI helpers.
    def print_permission_runtime_grant_gate_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Runtime Grant Gate Review Safety Boundary"))

    def handle_permission_runtime_grant_gate_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA permission runtime grant gate review"
        manager = AuraPermissionRuntimeGrantGateReviewFoundationManager(project_root=self.project_root)

        if command == "permission-runtime-grant-gate-review-status":
            self.print_permission_runtime_grant_gate_review_packet("AURA Permission Runtime Grant Gate Review Foundation Status", manager.status())
            return True

        if command == "permission-runtime-grant-gate-review-context":
            self.print_permission_runtime_grant_gate_review_packet("AURA Permission Runtime Grant Gate Review Foundation Context", manager.context())
            return True

        command_map = {
            "permission-grant-scope-review-plan": ("AURA Permission Grant Scope Review Plan", manager.permission_grant_scope_review_plan),
            "permission-grant-manual-approval-review-plan": ("AURA Permission Grant Manual Approval Review Plan", manager.permission_grant_manual_approval_review_plan),
            "permission-grant-expiry-review-plan": ("AURA Permission Grant Expiry Review Plan", manager.permission_grant_expiry_review_plan),
            "permission-grant-denial-review-plan": ("AURA Permission Grant Denial Review Plan", manager.permission_grant_denial_review_plan),
            "permission-grant-audit-link-review-plan": ("AURA Permission Grant Audit Link Review Plan", manager.permission_grant_audit_link_review_plan),
            "permission-grant-dashboard-visibility-review-plan": ("AURA Permission Grant Dashboard Visibility Review Plan", manager.permission_grant_dashboard_visibility_review_plan),
            "permission-grant-revocation-review-plan": ("AURA Permission Grant Revocation Review Plan", manager.permission_grant_revocation_review_plan),
            "permission-grant-risk-classification-review-plan": ("AURA Permission Grant Risk Classification Review Plan", manager.permission_grant_risk_classification_review_plan),
            "permission-grant-safe-idle-failure-review-plan": ("AURA Permission Grant Safe Idle Failure Review Plan", manager.permission_grant_safe_idle_failure_review_plan),
            "permission-grant-no-mutation-review-plan": ("AURA Permission Grant No Mutation Review Plan", manager.permission_grant_no_mutation_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_permission_runtime_grant_gate_review_packet(title, handler(target))
            return True

        return False

    # Sprint 137.0 memory runtime write gate review CLI helpers.
    def print_memory_runtime_write_gate_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Runtime Write Gate Review Safety Boundary"))

    def handle_memory_runtime_write_gate_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA memory runtime write gate review"
        manager = AuraMemoryRuntimeWriteGateReviewFoundationManager(project_root=self.project_root)

        if command == "memory-runtime-write-gate-review-status":
            self.print_memory_runtime_write_gate_review_packet("AURA Memory Runtime Write Gate Review Foundation Status", manager.status())
            return True

        if command == "memory-runtime-write-gate-review-context":
            self.print_memory_runtime_write_gate_review_packet("AURA Memory Runtime Write Gate Review Foundation Context", manager.context())
            return True

        command_map = {
            "memory-write-intent-classification-review-plan": ("AURA Memory Write Intent Classification Review Plan", manager.memory_write_intent_classification_review_plan),
            "memory-write-manual-approval-review-plan": ("AURA Memory Write Manual Approval Review Plan", manager.memory_write_manual_approval_review_plan),
            "memory-write-scope-boundary-review-plan": ("AURA Memory Write Scope Boundary Review Plan", manager.memory_write_scope_boundary_review_plan),
            "memory-write-redaction-review-plan": ("AURA Memory Write Redaction Review Plan", manager.memory_write_redaction_review_plan),
            "memory-write-conflict-resolution-review-plan": ("AURA Memory Write Conflict Resolution Review Plan", manager.memory_write_conflict_resolution_review_plan),
            "memory-write-audit-event-review-plan": ("AURA Memory Write Audit Event Review Plan", manager.memory_write_audit_event_review_plan),
            "memory-write-rollback-review-plan": ("AURA Memory Write Rollback Review Plan", manager.memory_write_rollback_review_plan),
            "memory-write-safe-idle-failure-review-plan": ("AURA Memory Write Safe Idle Failure Review Plan", manager.memory_write_safe_idle_failure_review_plan),
            "memory-write-session-link-review-plan": ("AURA Memory Write Session Link Review Plan", manager.memory_write_session_link_review_plan),
            "memory-write-no-persistence-review-plan": ("AURA Memory Write No Persistence Review Plan", manager.memory_write_no_persistence_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_memory_runtime_write_gate_review_packet(title, handler(target))
            return True

        return False

    # Sprint 136.0 chat runtime minimal loop review CLI helpers.
    def print_chat_runtime_minimal_loop_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Runtime Minimal Loop Review Safety Boundary"))

    def handle_chat_runtime_minimal_loop_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA chat runtime minimal loop review"
        manager = AuraChatRuntimeMinimalLoopReviewFoundationManager(project_root=self.project_root)

        if command == "chat-runtime-minimal-loop-review-status":
            self.print_chat_runtime_minimal_loop_review_packet("AURA Chat Runtime Minimal Loop Review Foundation Status", manager.status())
            return True

        if command == "chat-runtime-minimal-loop-review-context":
            self.print_chat_runtime_minimal_loop_review_packet("AURA Chat Runtime Minimal Loop Review Foundation Context", manager.context())
            return True

        command_map = {
            "chat-input-boundary-review-plan": ("AURA Chat Input Boundary Review Plan", manager.chat_input_boundary_review_plan),
            "chat-response-boundary-review-plan": ("AURA Chat Response Boundary Review Plan", manager.chat_response_boundary_review_plan),
            "chat-session-state-review-plan": ("AURA Chat Session State Review Plan", manager.chat_session_state_review_plan),
            "chat-permission-prompt-review-plan": ("AURA Chat Permission Prompt Review Plan", manager.chat_permission_prompt_review_plan),
            "chat-memory-read-write-gate-review-plan": ("AURA Chat Memory Read Write Gate Review Plan", manager.chat_memory_read_write_gate_review_plan),
            "chat-audit-event-review-plan": ("AURA Chat Audit Event Review Plan", manager.chat_audit_event_review_plan),
            "chat-safe-idle-fallback-review-plan": ("AURA Chat Safe Idle Fallback Review Plan", manager.chat_safe_idle_fallback_review_plan),
            "chat-error-recovery-review-plan": ("AURA Chat Error Recovery Review Plan", manager.chat_error_recovery_review_plan),
            "chat-manual-approval-runtime-entry-review-plan": ("AURA Chat Manual Approval Runtime Entry Review Plan", manager.chat_manual_approval_runtime_entry_review_plan),
            "chat-no-model-execution-review-plan": ("AURA Chat No Model Execution Review Plan", manager.chat_no_model_execution_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_chat_runtime_minimal_loop_review_packet(title, handler(target))
            return True

        return False

    # Sprint 135.0 control center runtime entry review CLI helpers.
    def print_control_center_runtime_entry_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Entry Review Safety Boundary"))

    def handle_control_center_runtime_entry_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Control Center runtime entry review"
        manager = AuraControlCenterRuntimeEntryReviewFoundationManager(project_root=self.project_root)

        if command == "control-center-runtime-entry-review-status":
            self.print_control_center_runtime_entry_review_packet("AURA Control Center Runtime Entry Review Foundation Status", manager.status())
            return True

        if command == "control-center-runtime-entry-review-context":
            self.print_control_center_runtime_entry_review_packet("AURA Control Center Runtime Entry Review Foundation Context", manager.context())
            return True

        command_map = {
            "control-center-entry-route-review-plan": ("AURA Control Center Entry Route Review Plan", manager.control_center_entry_route_review_plan),
            "control-center-localhost-boundary-review-plan": ("AURA Control Center Localhost Boundary Review Plan", manager.control_center_localhost_boundary_review_plan),
            "control-center-read-only-default-review-plan": ("AURA Control Center Read Only Default Review Plan", manager.control_center_read_only_default_review_plan),
            "control-center-status-panel-runtime-entry-review-plan": ("AURA Control Center Status Panel Runtime Entry Review Plan", manager.control_center_status_panel_runtime_entry_review_plan),
            "control-center-permission-panel-runtime-entry-review-plan": ("AURA Control Center Permission Panel Runtime Entry Review Plan", manager.control_center_permission_panel_runtime_entry_review_plan),
            "control-center-audit-panel-runtime-entry-review-plan": ("AURA Control Center Audit Panel Runtime Entry Review Plan", manager.control_center_audit_panel_runtime_entry_review_plan),
            "control-center-action-proposal-panel-runtime-entry-review-plan": ("AURA Control Center Action Proposal Panel Runtime Entry Review Plan", manager.control_center_action_proposal_panel_runtime_entry_review_plan),
            "control-center-safe-idle-error-panel-runtime-entry-review-plan": ("AURA Control Center Safe Idle Error Panel Runtime Entry Review Plan", manager.control_center_safe_idle_error_panel_runtime_entry_review_plan),
            "control-center-manual-approval-entry-review-plan": ("AURA Control Center Manual Approval Entry Review Plan", manager.control_center_manual_approval_entry_review_plan),
            "control-center-no-server-start-review-plan": ("AURA Control Center No Server Start Review Plan", manager.control_center_no_server_start_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_control_center_runtime_entry_review_packet(title, handler(target))
            return True

        return False

    # Sprint 134.0 local service boot plan review CLI helpers.
    def print_local_service_boot_plan_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Boot Plan Review Safety Boundary"))

    def handle_local_service_boot_plan_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local service boot plan review"
        manager = AuraLocalServiceBootPlanReviewFoundationManager(project_root=self.project_root)

        if command == "local-service-boot-plan-review-status":
            self.print_local_service_boot_plan_review_packet("AURA Local Service Boot Plan Review Foundation Status", manager.status())
            return True

        if command == "local-service-boot-plan-review-context":
            self.print_local_service_boot_plan_review_packet("AURA Local Service Boot Plan Review Foundation Context", manager.context())
            return True

        command_map = {
            "local-service-manual-start-review-plan": ("AURA Local Service Manual Start Review Plan", manager.local_service_manual_start_review_plan),
            "local-service-manual-stop-review-plan": ("AURA Local Service Manual Stop Review Plan", manager.local_service_manual_stop_review_plan),
            "local-service-health-monitor-review-plan": ("AURA Local Service Health Monitor Review Plan", manager.local_service_health_monitor_review_plan),
            "local-service-safe-shutdown-review-plan": ("AURA Local Service Safe Shutdown Review Plan", manager.local_service_safe_shutdown_review_plan),
            "local-service-config-contract-review-plan": ("AURA Local Service Config Contract Review Plan", manager.local_service_config_contract_review_plan),
            "local-service-log-visibility-review-plan": ("AURA Local Service Log Visibility Review Plan", manager.local_service_log_visibility_review_plan),
            "local-service-localhost-only-review-plan": ("AURA Local Service Localhost Only Review Plan", manager.local_service_localhost_only_review_plan),
            "local-service-autostart-guard-review-plan": ("AURA Local Service Autostart Guard Review Plan", manager.local_service_autostart_guard_review_plan),
            "local-service-failure-safe-idle-review-plan": ("AURA Local Service Failure Safe Idle Review Plan", manager.local_service_failure_safe_idle_review_plan),
            "local-service-no-port-binding-review-plan": ("AURA Local Service No Port Binding Review Plan", manager.local_service_no_port_binding_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_boot_plan_review_packet(title, handler(target))
            return True

        return False

    # Sprint 133.0 runtime activation path proposal review CLI helpers.
    def print_runtime_activation_path_proposal_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Activation Path Proposal Review Safety Boundary"))

    def handle_runtime_activation_path_proposal_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime activation path proposal review"
        manager = AuraRuntimeActivationPathProposalReviewFoundationManager(project_root=self.project_root)

        if command == "runtime-activation-path-proposal-review-status":
            self.print_runtime_activation_path_proposal_review_packet("AURA Runtime Activation Path Proposal Review Foundation Status", manager.status())
            return True

        if command == "runtime-activation-path-proposal-review-context":
            self.print_runtime_activation_path_proposal_review_packet("AURA Runtime Activation Path Proposal Review Foundation Context", manager.context())
            return True

        command_map = {
            "runtime-activation-stage-model-review-plan": ("AURA Runtime Activation Stage Model Review Plan", manager.runtime_activation_stage_model_review_plan),
            "manual-approval-chain-review-plan": ("AURA Manual Approval Chain Review Plan", manager.manual_approval_chain_review_plan),
            "activation-blocker-register-link-review-plan": ("AURA Activation Blocker Register Link Review Plan", manager.activation_blocker_register_link_review_plan),
            "permission-contract-activation-review-plan": ("AURA Permission Contract Activation Review Plan", manager.permission_contract_activation_review_plan),
            "audit-contract-activation-review-plan": ("AURA Audit Contract Activation Review Plan", manager.audit_contract_activation_review_plan),
            "dashboard-visibility-activation-review-plan": ("AURA Dashboard Visibility Activation Review Plan", manager.dashboard_visibility_activation_review_plan),
            "safe-idle-rollback-activation-review-plan": ("AURA Safe Idle Rollback Activation Review Plan", manager.safe_idle_rollback_activation_review_plan),
            "emergency-stop-activation-review-plan": ("AURA Emergency Stop Activation Review Plan", manager.emergency_stop_activation_review_plan),
            "release-candidate-transition-review-plan": ("AURA Release Candidate Transition Review Plan", manager.release_candidate_transition_review_plan),
            "activation-denial-deferment-review-plan": ("AURA Activation Denial Deferment Review Plan", manager.activation_denial_deferment_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_activation_path_proposal_review_packet(title, handler(target))
            return True

        return False

    # Sprint 132.0 final genesis acceptance criteria CLI helpers.
    def print_final_genesis_acceptance_criteria_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Final Genesis Acceptance Criteria Safety Boundary"))

    def handle_final_genesis_acceptance_criteria_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Final Genesis acceptance criteria"
        manager = AuraFinalGenesisAcceptanceCriteriaFoundationManager(project_root=self.project_root)

        if command == "final-genesis-acceptance-criteria-status":
            self.print_final_genesis_acceptance_criteria_packet("AURA Final Genesis Acceptance Criteria Foundation Status", manager.status())
            return True

        if command == "final-genesis-acceptance-criteria-context":
            self.print_final_genesis_acceptance_criteria_packet("AURA Final Genesis Acceptance Criteria Foundation Context", manager.context())
            return True

        command_map = {
            "boot-stability-acceptance-criteria-plan": ("AURA Boot Stability Acceptance Criteria Plan", manager.boot_stability_acceptance_criteria_plan),
            "local-service-acceptance-criteria-plan": ("AURA Local Service Acceptance Criteria Plan", manager.local_service_acceptance_criteria_plan),
            "control-center-acceptance-criteria-plan": ("AURA Control Center Acceptance Criteria Plan", manager.control_center_acceptance_criteria_plan),
            "local-chat-acceptance-criteria-plan": ("AURA Local Chat Acceptance Criteria Plan", manager.local_chat_acceptance_criteria_plan),
            "memory-acceptance-criteria-plan": ("AURA Memory Acceptance Criteria Plan", manager.memory_acceptance_criteria_plan),
            "permission-audit-acceptance-criteria-plan": ("AURA Permission Audit Acceptance Criteria Plan", manager.permission_audit_acceptance_criteria_plan),
            "safe-idle-recovery-acceptance-criteria-plan": ("AURA Safe Idle Recovery Acceptance Criteria Plan", manager.safe_idle_recovery_acceptance_criteria_plan),
            "optional-orion-voice-vision-avatar-boundary-criteria-plan": ("AURA Optional ORION Voice Vision Avatar Boundary Criteria Plan", manager.optional_orion_voice_vision_avatar_boundary_criteria_plan),
            "final-genesis-go-no-go-criteria-plan": ("AURA Final Genesis Go No Go Criteria Plan", manager.final_genesis_go_no_go_criteria_plan),
            "future-runtime-release-candidate-criteria-plan": ("AURA Future Runtime Release Candidate Criteria Plan", manager.future_runtime_release_candidate_criteria_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_final_genesis_acceptance_criteria_packet(title, handler(target))
            return True

        return False

    # Sprint 131.0 post-checkpoint 130 next block CLI helpers.
    def print_post_checkpoint_130_next_block_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Post-Checkpoint 130 Next Block Safety Boundary"))

    def handle_post_checkpoint_130_next_block_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA post-checkpoint 130 next block"
        manager = AuraPostCheckpoint130NextBlockFoundationManager(project_root=self.project_root)

        if command == "post-checkpoint-130-next-block-status":
            self.print_post_checkpoint_130_next_block_packet("AURA Post-Checkpoint 130 Next Block Foundation Status", manager.status())
            return True

        if command == "post-checkpoint-130-next-block-context":
            self.print_post_checkpoint_130_next_block_packet("AURA Post-Checkpoint 130 Next Block Foundation Context", manager.context())
            return True

        command_map = {
            "sprint-131-140-sequence-foundation-plan": ("AURA Sprint 131-140 Sequence Foundation Plan", manager.sprint_131_140_sequence_foundation_plan),
            "final-genesis-acceptance-criteria-foundation-plan": ("AURA Final Genesis Acceptance Criteria Foundation Plan", manager.final_genesis_acceptance_criteria_foundation_plan),
            "runtime-activation-path-proposal-review-plan": ("AURA Runtime Activation Path Proposal Review Plan", manager.runtime_activation_path_proposal_review_plan),
            "local-service-boot-plan-review-plan": ("AURA Local Service Boot Plan Review Plan", manager.local_service_boot_plan_review_plan),
            "control-center-runtime-entry-review-plan": ("AURA Control Center Runtime Entry Review Plan", manager.control_center_runtime_entry_review_plan),
            "chat-runtime-minimal-loop-review-plan": ("AURA Chat Runtime Minimal Loop Review Plan", manager.chat_runtime_minimal_loop_review_plan),
            "memory-runtime-write-gate-review-plan": ("AURA Memory Runtime Write Gate Review Plan", manager.memory_runtime_write_gate_review_plan),
            "permission-runtime-grant-gate-review-plan": ("AURA Permission Runtime Grant Gate Review Plan", manager.permission_runtime_grant_gate_review_plan),
            "audit-runtime-writer-activation-review-plan": ("AURA Audit Runtime Writer Activation Review Plan", manager.audit_runtime_writer_activation_review_plan),
            "review-stabilization-131-140-checkpoint-plan": ("AURA Review Stabilization 131-140 Checkpoint Plan", manager.review_stabilization_131_140_checkpoint_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_post_checkpoint_130_next_block_packet(title, handler(target))
            return True

        return False

    # Sprint 130.0 review stabilization 121-130 CLI helpers.
    def print_review_stabilization_121_130_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 121-130 Safety Boundary"))

    def handle_review_stabilization_121_130_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA review stabilization 121-130 checkpoint"
        manager = AuraReviewStabilization121130FoundationManager(project_root=self.project_root)

        if command == "review-stabilization-121-130-status":
            self.print_review_stabilization_121_130_packet("AURA Review Stabilization 121-130 Foundation Status", manager.status())
            return True

        if command == "review-stabilization-121-130-context":
            self.print_review_stabilization_121_130_packet("AURA Review Stabilization 121-130 Foundation Context", manager.context())
            return True

        command_map = {
            "sprint-121-129-completion-review-plan": ("AURA Sprint 121-129 Completion Review Plan", manager.sprint_121_129_completion_review_plan),
            "capability-registry-consistency-review-plan": ("AURA Capability Registry Consistency Review Plan", manager.capability_registry_consistency_review_plan),
            "permission-boundary-consistency-review-plan": ("AURA Permission Boundary Consistency Review Plan", manager.permission_boundary_consistency_review_plan),
            "runtime-zero-counter-review-plan": ("AURA Runtime Zero Counter Review Plan", manager.runtime_zero_counter_review_plan),
            "dashboard-orion-boundary-review-plan": ("AURA Dashboard ORION Boundary Review Plan", manager.dashboard_orion_boundary_review_plan),
            "action-permission-recovery-blocker-review-plan": ("AURA Action Permission Recovery Blocker Review Plan", manager.action_permission_recovery_blocker_review_plan),
            "documentation-roadmap-consistency-review-plan": ("AURA Documentation Roadmap Consistency Review Plan", manager.documentation_roadmap_consistency_review_plan),
            "boot-and-cli-surface-review-plan": ("AURA Boot And CLI Surface Review Plan", manager.boot_and_cli_surface_review_plan),
            "known-deferred-runtime-review-plan": ("AURA Known Deferred Runtime Review Plan", manager.known_deferred_runtime_review_plan),
            "future-sprint-131-140-readiness-plan": ("AURA Future Sprint 131-140 Readiness Plan", manager.future_sprint_131_140_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_review_stabilization_121_130_packet(title, handler(target))
            return True

        return False

    # Sprint 129.0 runtime activation blocker register boundary review CLI helpers.
    def print_runtime_activation_blocker_register_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Activation Blocker Register Boundary Review Safety Boundary"))

    def handle_runtime_activation_blocker_register_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime activation blocker register boundary review"
        manager = AuraRuntimeActivationBlockerRegisterBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "runtime-activation-blocker-register-boundary-review-status":
            self.print_runtime_activation_blocker_register_boundary_review_packet("AURA Runtime Activation Blocker Register Boundary Review Foundation Status", manager.status())
            return True

        if command == "runtime-activation-blocker-register-boundary-review-context":
            self.print_runtime_activation_blocker_register_boundary_review_packet("AURA Runtime Activation Blocker Register Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "blocker-register-schema-boundary-review-plan": ("AURA Blocker Register Schema Boundary Review Plan", manager.blocker_register_schema_boundary_review_plan),
            "blocker-source-classification-boundary-review-plan": ("AURA Blocker Source Classification Boundary Review Plan", manager.blocker_source_classification_boundary_review_plan),
            "blocker-severity-policy-boundary-review-plan": ("AURA Blocker Severity Policy Boundary Review Plan", manager.blocker_severity_policy_boundary_review_plan),
            "blocker-activation-gate-link-boundary-review-plan": ("AURA Blocker Activation Gate Link Boundary Review Plan", manager.blocker_activation_gate_link_boundary_review_plan),
            "blocker-resolution-evidence-boundary-review-plan": ("AURA Blocker Resolution Evidence Boundary Review Plan", manager.blocker_resolution_evidence_boundary_review_plan),
            "blocker-dashboard-visibility-boundary-review-plan": ("AURA Blocker Dashboard Visibility Boundary Review Plan", manager.blocker_dashboard_visibility_boundary_review_plan),
            "blocker-audit-link-boundary-review-plan": ("AURA Blocker Audit Link Boundary Review Plan", manager.blocker_audit_link_boundary_review_plan),
            "blocker-failure-safe-idle-boundary-review-plan": ("AURA Blocker Failure Safe Idle Boundary Review Plan", manager.blocker_failure_safe_idle_boundary_review_plan),
            "future-runtime-activation-unblock-boundary-plan": ("AURA Future Runtime Activation Unblock Boundary Plan", manager.future_runtime_activation_unblock_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_activation_blocker_register_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 128.0 dashboard runtime readiness boundary review CLI helpers.
    def print_dashboard_runtime_readiness_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Runtime Readiness Boundary Review Safety Boundary"))

    def handle_dashboard_runtime_readiness_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA dashboard runtime readiness boundary review"
        manager = AuraDashboardRuntimeReadinessBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "dashboard-runtime-readiness-boundary-review-status":
            self.print_dashboard_runtime_readiness_boundary_review_packet("AURA Dashboard Runtime Readiness Boundary Review Foundation Status", manager.status())
            return True

        if command == "dashboard-runtime-readiness-boundary-review-context":
            self.print_dashboard_runtime_readiness_boundary_review_packet("AURA Dashboard Runtime Readiness Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "dashboard-runtime-entrypoint-boundary-review-plan": ("AURA Dashboard Runtime Entrypoint Boundary Review Plan", manager.dashboard_runtime_entrypoint_boundary_review_plan),
            "dashboard-route-contract-boundary-review-plan": ("AURA Dashboard Route Contract Boundary Review Plan", manager.dashboard_route_contract_boundary_review_plan),
            "dashboard-api-contract-boundary-review-plan": ("AURA Dashboard API Contract Boundary Review Plan", manager.dashboard_api_contract_boundary_review_plan),
            "dashboard-websocket-event-boundary-review-plan": ("AURA Dashboard Websocket Event Boundary Review Plan", manager.dashboard_websocket_event_boundary_review_plan),
            "dashboard-permission-panel-runtime-boundary-review-plan": ("AURA Dashboard Permission Panel Runtime Boundary Review Plan", manager.dashboard_permission_panel_runtime_boundary_review_plan),
            "dashboard-audit-panel-runtime-boundary-review-plan": ("AURA Dashboard Audit Panel Runtime Boundary Review Plan", manager.dashboard_audit_panel_runtime_boundary_review_plan),
            "dashboard-action-panel-runtime-boundary-review-plan": ("AURA Dashboard Action Panel Runtime Boundary Review Plan", manager.dashboard_action_panel_runtime_boundary_review_plan),
            "dashboard-failure-safe-idle-boundary-review-plan": ("AURA Dashboard Failure Safe Idle Boundary Review Plan", manager.dashboard_failure_safe_idle_boundary_review_plan),
            "future-dashboard-runtime-activation-boundary-plan": ("AURA Future Dashboard Runtime Activation Boundary Plan", manager.future_dashboard_runtime_activation_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_dashboard_runtime_readiness_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 127.0 runtime recovery drill boundary review CLI helpers.
    def print_runtime_recovery_drill_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Recovery Drill Boundary Review Safety Boundary"))

    def handle_runtime_recovery_drill_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime recovery drill boundary review"
        manager = AuraRuntimeRecoveryDrillBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "runtime-recovery-drill-boundary-review-status":
            self.print_runtime_recovery_drill_boundary_review_packet("AURA Runtime Recovery Drill Boundary Review Foundation Status", manager.status())
            return True

        if command == "runtime-recovery-drill-boundary-review-context":
            self.print_runtime_recovery_drill_boundary_review_packet("AURA Runtime Recovery Drill Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "recovery-drill-scenario-catalog-boundary-review-plan": ("AURA Recovery Drill Scenario Catalog Boundary Review Plan", manager.recovery_drill_scenario_catalog_boundary_review_plan),
            "recovery-trigger-boundary-review-plan": ("AURA Recovery Trigger Boundary Review Plan", manager.recovery_trigger_boundary_review_plan),
            "recovery-safe-idle-boundary-review-plan": ("AURA Recovery Safe Idle Boundary Review Plan", manager.recovery_safe_idle_boundary_review_plan),
            "rollback-preview-boundary-review-plan": ("AURA Rollback Preview Boundary Review Plan", manager.rollback_preview_boundary_review_plan),
            "recovery-audit-dashboard-boundary-review-plan": ("AURA Recovery Audit Dashboard Boundary Review Plan", manager.recovery_audit_dashboard_boundary_review_plan),
            "recovery-permission-boundary-review-plan": ("AURA Recovery Permission Boundary Review Plan", manager.recovery_permission_boundary_review_plan),
            "orion-recovery-disconnect-boundary-review-plan": ("AURA ORION Recovery Disconnect Boundary Review Plan", manager.orion_recovery_disconnect_boundary_review_plan),
            "recovery-failure-escalation-boundary-review-plan": ("AURA Recovery Failure Escalation Boundary Review Plan", manager.recovery_failure_escalation_boundary_review_plan),
            "future-runtime-recovery-drill-boundary-plan": ("AURA Future Runtime Recovery Drill Boundary Plan", manager.future_runtime_recovery_drill_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_recovery_drill_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 126.0 runtime grant expiry boundary review CLI helpers.
    def print_runtime_grant_expiry_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Grant Expiry Boundary Review Safety Boundary"))

    def handle_runtime_grant_expiry_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime grant expiry boundary review"
        manager = AuraRuntimeGrantExpiryBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "runtime-grant-expiry-boundary-review-status":
            self.print_runtime_grant_expiry_boundary_review_packet("AURA Runtime Grant Expiry Boundary Review Foundation Status", manager.status())
            return True

        if command == "runtime-grant-expiry-boundary-review-context":
            self.print_runtime_grant_expiry_boundary_review_packet("AURA Runtime Grant Expiry Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "grant-expiry-schema-boundary-review-plan": ("AURA Grant Expiry Schema Boundary Review Plan", manager.grant_expiry_schema_boundary_review_plan),
            "grant-lifetime-policy-boundary-review-plan": ("AURA Grant Lifetime Policy Boundary Review Plan", manager.grant_lifetime_policy_boundary_review_plan),
            "grant-renewal-request-boundary-review-plan": ("AURA Grant Renewal Request Boundary Review Plan", manager.grant_renewal_request_boundary_review_plan),
            "grant-revocation-boundary-review-plan": ("AURA Grant Revocation Boundary Review Plan", manager.grant_revocation_boundary_review_plan),
            "expired-grant-denial-boundary-review-plan": ("AURA Expired Grant Denial Boundary Review Plan", manager.expired_grant_denial_boundary_review_plan),
            "dashboard-grant-visibility-boundary-review-plan": ("AURA Dashboard Grant Visibility Boundary Review Plan", manager.dashboard_grant_visibility_boundary_review_plan),
            "audit-grant-expiry-boundary-review-plan": ("AURA Audit Grant Expiry Boundary Review Plan", manager.audit_grant_expiry_boundary_review_plan),
            "grant-expiry-failure-safe-idle-boundary-review-plan": ("AURA Grant Expiry Failure Safe Idle Boundary Review Plan", manager.grant_expiry_failure_safe_idle_boundary_review_plan),
            "future-runtime-grant-expiry-boundary-plan": ("AURA Future Runtime Grant Expiry Boundary Plan", manager.future_runtime_grant_expiry_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_grant_expiry_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 125.0 safe local action allowlist boundary review CLI helpers.
    def print_safe_local_action_allowlist_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Action Allowlist Boundary Review Safety Boundary"))

    def handle_safe_local_action_allowlist_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA safe local action allowlist boundary review"
        manager = AuraSafeLocalActionAllowlistBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "safe-local-action-allowlist-boundary-review-status":
            self.print_safe_local_action_allowlist_boundary_review_packet("AURA Safe Local Action Allowlist Boundary Review Foundation Status", manager.status())
            return True

        if command == "safe-local-action-allowlist-boundary-review-context":
            self.print_safe_local_action_allowlist_boundary_review_packet("AURA Safe Local Action Allowlist Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "safe-action-catalog-boundary-review-plan": ("AURA Safe Action Catalog Boundary Review Plan", manager.safe_action_catalog_boundary_review_plan),
            "safe-action-scope-boundary-review-plan": ("AURA Safe Action Scope Boundary Review Plan", manager.safe_action_scope_boundary_review_plan),
            "safe-action-permission-boundary-review-plan": ("AURA Safe Action Permission Boundary Review Plan", manager.safe_action_permission_boundary_review_plan),
            "safe-action-risk-level-boundary-review-plan": ("AURA Safe Action Risk Level Boundary Review Plan", manager.safe_action_risk_level_boundary_review_plan),
            "safe-action-rollback-boundary-review-plan": ("AURA Safe Action Rollback Boundary Review Plan", manager.safe_action_rollback_boundary_review_plan),
            "safe-action-audit-dashboard-boundary-review-plan": ("AURA Safe Action Audit Dashboard Boundary Review Plan", manager.safe_action_audit_dashboard_boundary_review_plan),
            "safe-action-denied-action-boundary-review-plan": ("AURA Safe Action Denied Action Boundary Review Plan", manager.safe_action_denied_action_boundary_review_plan),
            "safe-action-runtime-gate-boundary-review-plan": ("AURA Safe Action Runtime Gate Boundary Review Plan", manager.safe_action_runtime_gate_boundary_review_plan),
            "future-safe-local-action-runtime-boundary-plan": ("AURA Future Safe Local Action Runtime Boundary Plan", manager.future_safe_local_action_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_safe_local_action_allowlist_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 124.0 ORION dry handshake boundary review CLI helpers.
    def print_orion_dry_handshake_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="ORION Dry Handshake Boundary Review Safety Boundary"))

    def handle_orion_dry_handshake_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA ORION dry handshake boundary review"
        manager = AuraOrionDryHandshakeBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "orion-dry-handshake-boundary-review-status":
            self.print_orion_dry_handshake_boundary_review_packet("AURA ORION Dry Handshake Boundary Review Foundation Status", manager.status())
            return True

        if command == "orion-dry-handshake-boundary-review-context":
            self.print_orion_dry_handshake_boundary_review_packet("AURA ORION Dry Handshake Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "orion-client-identity-packet-boundary-review-plan": ("AURA ORION Client Identity Packet Boundary Review Plan", manager.orion_client_identity_packet_boundary_review_plan),
            "orion-capability-packet-boundary-review-plan": ("AURA ORION Capability Packet Boundary Review Plan", manager.orion_capability_packet_boundary_review_plan),
            "orion-permission-scope-packet-boundary-review-plan": ("AURA ORION Permission Scope Packet Boundary Review Plan", manager.orion_permission_scope_packet_boundary_review_plan),
            "orion-status-heartbeat-boundary-review-plan": ("AURA ORION Status Heartbeat Boundary Review Plan", manager.orion_status_heartbeat_boundary_review_plan),
            "orion-redaction-boundary-review-plan": ("AURA ORION Redaction Boundary Review Plan", manager.orion_redaction_boundary_review_plan),
            "orion-emergency-stop-boundary-review-plan": ("AURA ORION Emergency Stop Boundary Review Plan", manager.orion_emergency_stop_boundary_review_plan),
            "atlas-orion-authority-boundary-review-plan": ("AURA ATLAS/ORION Authority Boundary Review Plan", manager.atlas_orion_authority_boundary_review_plan),
            "orion-failure-safe-idle-boundary-review-plan": ("AURA ORION Failure Safe Idle Boundary Review Plan", manager.orion_failure_safe_idle_boundary_review_plan),
            "future-orion-handshake-runtime-boundary-plan": ("AURA Future ORION Handshake Runtime Boundary Plan", manager.future_orion_handshake_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_orion_dry_handshake_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 123.0 dashboard control center boundary review CLI helpers.
    def print_dashboard_control_center_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Control Center Boundary Review Safety Boundary"))

    def handle_dashboard_control_center_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA dashboard control center boundary review"
        manager = AuraDashboardControlCenterBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "dashboard-control-center-boundary-review-status":
            self.print_dashboard_control_center_boundary_review_packet("AURA Dashboard Control Center Boundary Review Foundation Status", manager.status())
            return True

        if command == "dashboard-control-center-boundary-review-context":
            self.print_dashboard_control_center_boundary_review_packet("AURA Dashboard Control Center Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "control-center-shell-layout-boundary-review-plan": ("AURA Control Center Shell Layout Boundary Review Plan", manager.control_center_shell_layout_boundary_review_plan),
            "dashboard-status-payload-boundary-review-plan": ("AURA Dashboard Status Payload Boundary Review Plan", manager.dashboard_status_payload_boundary_review_plan),
            "permission-panel-boundary-review-plan": ("AURA Permission Panel Boundary Review Plan", manager.permission_panel_boundary_review_plan),
            "audit-panel-boundary-review-plan": ("AURA Audit Panel Boundary Review Plan", manager.audit_panel_boundary_review_plan),
            "action-proposal-panel-boundary-review-plan": ("AURA Action Proposal Panel Boundary Review Plan", manager.action_proposal_panel_boundary_review_plan),
            "orion-client-panel-boundary-review-plan": ("AURA ORION Client Panel Boundary Review Plan", manager.orion_client_panel_boundary_review_plan),
            "runtime-gate-panel-boundary-review-plan": ("AURA Runtime Gate Panel Boundary Review Plan", manager.runtime_gate_panel_boundary_review_plan),
            "dashboard-failure-safe-idle-boundary-review-plan": ("AURA Dashboard Failure Safe Idle Boundary Review Plan", manager.dashboard_failure_safe_idle_boundary_review_plan),
            "future-dashboard-control-center-runtime-boundary-plan": ("AURA Future Dashboard Control Center Runtime Boundary Plan", manager.future_dashboard_control_center_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_dashboard_control_center_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 122.0 runtime permission audit writer boundary review CLI helpers.
    def print_runtime_permission_audit_writer_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Permission Audit Writer Boundary Review Safety Boundary"))

    def handle_runtime_permission_audit_writer_boundary_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime permission audit writer boundary review"
        manager = AuraRuntimePermissionAuditWriterBoundaryReviewFoundationManager(project_root=self.project_root)

        if command == "runtime-permission-audit-writer-boundary-review-status":
            self.print_runtime_permission_audit_writer_boundary_review_packet("AURA Runtime Permission Audit Writer Boundary Review Foundation Status", manager.status())
            return True

        if command == "runtime-permission-audit-writer-boundary-review-context":
            self.print_runtime_permission_audit_writer_boundary_review_packet("AURA Runtime Permission Audit Writer Boundary Review Foundation Context", manager.context())
            return True

        command_map = {
            "audit-writer-schema-boundary-review-plan": ("AURA Audit Writer Schema Boundary Review Plan", manager.audit_writer_schema_boundary_review_plan),
            "audit-writer-storage-boundary-review-plan": ("AURA Audit Writer Storage Boundary Review Plan", manager.audit_writer_storage_boundary_review_plan),
            "audit-writer-redaction-boundary-review-plan": ("AURA Audit Writer Redaction Boundary Review Plan", manager.audit_writer_redaction_boundary_review_plan),
            "audit-writer-visibility-boundary-review-plan": ("AURA Audit Writer Visibility Boundary Review Plan", manager.audit_writer_visibility_boundary_review_plan),
            "permission-decision-audit-link-review-plan": ("AURA Permission Decision Audit Link Review Plan", manager.permission_decision_audit_link_review_plan),
            "dashboard-audit-payload-boundary-review-plan": ("AURA Dashboard Audit Payload Boundary Review Plan", manager.dashboard_audit_payload_boundary_review_plan),
            "audit-writer-failure-boundary-review-plan": ("AURA Audit Writer Failure Boundary Review Plan", manager.audit_writer_failure_boundary_review_plan),
            "audit-writer-runtime-gate-boundary-review-plan": ("AURA Audit Writer Runtime Gate Boundary Review Plan", manager.audit_writer_runtime_gate_boundary_review_plan),
            "future-permission-audit-writer-runtime-boundary-plan": ("AURA Future Permission Audit Writer Runtime Boundary Plan", manager.future_permission_audit_writer_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_permission_audit_writer_boundary_review_packet(title, handler(target))
            return True

        return False

    # Sprint 121.0 post-checkpoint 120 next block planning CLI helpers.
    def print_post_checkpoint_120_next_block_planning_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Post-Checkpoint 120 Next Block Planning Safety Boundary"))

    def handle_post_checkpoint_120_next_block_planning_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA post-checkpoint 120 next block planning"
        manager = AuraPostCheckpoint120NextBlockPlanningFoundationManager(project_root=self.project_root)

        if command == "post-checkpoint-120-next-block-planning-status":
            self.print_post_checkpoint_120_next_block_planning_packet("AURA Post-Checkpoint 120 Next Block Planning Foundation Status", manager.status())
            return True

        if command == "post-checkpoint-120-next-block-planning-context":
            self.print_post_checkpoint_120_next_block_planning_packet("AURA Post-Checkpoint 120 Next Block Planning Foundation Context", manager.context())
            return True

        command_map = {
            "checkpoint-120-output-review-plan": ("AURA Checkpoint 120 Output Review Plan", manager.checkpoint_120_output_review_plan),
            "sprint-121-130-scope-definition-plan": ("AURA Sprint 121-130 Scope Definition Plan", manager.sprint_121_130_scope_definition_plan),
            "runtime-readiness-continuation-plan": ("AURA Runtime Readiness Continuation Plan", manager.runtime_readiness_continuation_plan),
            "permission-audit-writer-boundary-plan": ("AURA Permission Audit Writer Boundary Plan", manager.permission_audit_writer_boundary_plan),
            "dashboard-control-center-boundary-plan": ("AURA Dashboard Control Center Boundary Plan", manager.dashboard_control_center_boundary_plan),
            "orion-dry-handshake-boundary-plan": ("AURA ORION Dry Handshake Boundary Plan", manager.orion_dry_handshake_boundary_plan),
            "safe-local-action-allowlist-boundary-plan": ("AURA Safe Local Action Allowlist Boundary Plan", manager.safe_local_action_allowlist_boundary_plan),
            "runtime-activation-blocker-tracking-plan": ("AURA Runtime Activation Blocker Tracking Plan", manager.runtime_activation_blocker_tracking_plan),
            "future-121-130-checkpoint-boundary-plan": ("AURA Future 121-130 Checkpoint Boundary Plan", manager.future_121_130_checkpoint_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_post_checkpoint_120_next_block_planning_packet(title, handler(target))
            return True

        return False

    # Sprint 120.0 review stabilization 111-120 CLI helpers.
    def print_review_stabilization_111_120_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 111-120 Safety Boundary"))

    def handle_review_stabilization_111_120_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA review stabilization 111-120"
        manager = AuraReviewStabilization111120FoundationManager(project_root=self.project_root)

        if command == "review-stabilization-111-120-status":
            self.print_review_stabilization_111_120_packet("AURA Review Stabilization 111-120 Foundation Status", manager.status())
            return True

        if command == "review-stabilization-111-120-context":
            self.print_review_stabilization_111_120_packet("AURA Review Stabilization 111-120 Foundation Context", manager.context())
            return True

        command_map = {
            "sprint-111-120-completion-review-plan": ("AURA Sprint 111-120 Completion Review Plan", manager.sprint_111_120_completion_review_plan),
            "capability-registry-stabilization-review-plan": ("AURA Capability Registry Stabilization Review Plan", manager.capability_registry_stabilization_review_plan),
            "runtime-safety-zero-state-review-plan": ("AURA Runtime Safety Zero-State Review Plan", manager.runtime_safety_zero_state_review_plan),
            "integration-surface-stabilization-review-plan": ("AURA Integration Surface Stabilization Review Plan", manager.integration_surface_stabilization_review_plan),
            "documentation-roadmap-stabilization-review-plan": ("AURA Documentation Roadmap Stabilization Review Plan", manager.documentation_roadmap_stabilization_review_plan),
            "v1-runtime-readiness-blocker-review-plan": ("AURA v1 Runtime Readiness Blocker Review Plan", manager.v1_runtime_readiness_blocker_review_plan),
            "release-cutline-consistency-review-plan": ("AURA Release Cutline Consistency Review Plan", manager.release_cutline_consistency_review_plan),
            "next-block-121-130-boundary-plan": ("AURA Next Block 121-130 Boundary Plan", manager.next_block_121_130_boundary_plan),
            "checkpoint-120-acceptance-review-plan": ("AURA Checkpoint 120 Acceptance Review Plan", manager.checkpoint_120_acceptance_review_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_review_stabilization_111_120_packet(title, handler(target))
            return True

        return False

    # Sprint 119.0 v1 runtime readiness cutline review CLI helpers.
    def print_v1_runtime_readiness_cutline_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="v1 Runtime Readiness Cutline Review Safety Boundary"))

    def handle_v1_runtime_readiness_cutline_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA v1 runtime readiness cutline review"
        manager = AuraV1RuntimeReadinessCutlineReviewFoundationManager(project_root=self.project_root)

        if command == "v1-runtime-readiness-cutline-review-status":
            self.print_v1_runtime_readiness_cutline_review_packet("AURA v1 Runtime Readiness Cutline Review Foundation Status", manager.status())
            return True

        if command == "v1-runtime-readiness-cutline-review-context":
            self.print_v1_runtime_readiness_cutline_review_packet("AURA v1 Runtime Readiness Cutline Review Foundation Context", manager.context())
            return True

        command_map = {
            "v1-allowed-capability-cutline-plan": ("AURA v1 Allowed Capability Cutline Plan", manager.v1_allowed_capability_cutline_plan),
            "v1-deferred-capability-cutline-plan": ("AURA v1 Deferred Capability Cutline Plan", manager.v1_deferred_capability_cutline_plan),
            "v1-runtime-gate-cutline-plan": ("AURA v1 Runtime Gate Cutline Plan", manager.v1_runtime_gate_cutline_plan),
            "v1-permission-audit-cutline-plan": ("AURA v1 Permission Audit Cutline Plan", manager.v1_permission_audit_cutline_plan),
            "v1-orion-boundary-cutline-plan": ("AURA v1 ORION Boundary Cutline Plan", manager.v1_orion_boundary_cutline_plan),
            "v1-dashboard-visibility-cutline-plan": ("AURA v1 Dashboard Visibility Cutline Plan", manager.v1_dashboard_visibility_cutline_plan),
            "v1-release-blocker-cutline-plan": ("AURA v1 Release Blocker Cutline Plan", manager.v1_release_blocker_cutline_plan),
            "v1-safe-idle-acceptance-cutline-plan": ("AURA v1 Safe Idle Acceptance Cutline Plan", manager.v1_safe_idle_acceptance_cutline_plan),
            "future-v1-runtime-activation-boundary-plan": ("AURA Future v1 Runtime Activation Boundary Plan", manager.future_v1_runtime_activation_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_v1_runtime_readiness_cutline_review_packet(title, handler(target))
            return True

        return False

    # Sprint 118.0 manual approval decision flow review CLI helpers.
    def print_manual_approval_decision_flow_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Manual Approval Decision Flow Review Safety Boundary"))

    def handle_manual_approval_decision_flow_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA manual approval decision flow review"
        manager = AuraManualApprovalDecisionFlowReviewFoundationManager(project_root=self.project_root)

        if command == "manual-approval-decision-flow-review-status":
            self.print_manual_approval_decision_flow_review_packet("AURA Manual Approval Decision Flow Review Foundation Status", manager.status())
            return True

        if command == "manual-approval-decision-flow-review-context":
            self.print_manual_approval_decision_flow_review_packet("AURA Manual Approval Decision Flow Review Foundation Context", manager.context())
            return True

        command_map = {
            "approval-request-schema-review-plan": ("AURA Approval Request Schema Review Plan", manager.approval_request_schema_review_plan),
            "approval-decision-state-review-plan": ("AURA Approval Decision State Review Plan", manager.approval_decision_state_review_plan),
            "approval-outcome-catalog-review-plan": ("AURA Approval Outcome Catalog Review Plan", manager.approval_outcome_catalog_review_plan),
            "approval-denial-cancellation-review-plan": ("AURA Approval Denial Cancellation Review Plan", manager.approval_denial_cancellation_review_plan),
            "approval-escalation-boundary-review-plan": ("AURA Approval Escalation Boundary Review Plan", manager.approval_escalation_boundary_review_plan),
            "approval-audit-reference-review-plan": ("AURA Approval Audit Reference Review Plan", manager.approval_audit_reference_review_plan),
            "approval-dashboard-payload-review-plan": ("AURA Approval Dashboard Payload Review Plan", manager.approval_dashboard_payload_review_plan),
            "approval-runtime-gate-boundary-review-plan": ("AURA Approval Runtime Gate Boundary Review Plan", manager.approval_runtime_gate_boundary_review_plan),
            "future-manual-approval-runtime-boundary-plan": ("AURA Future Manual Approval Runtime Boundary Plan", manager.future_manual_approval_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_manual_approval_decision_flow_review_packet(title, handler(target))
            return True

        return False

    # Sprint 117.0 runtime error rollback preview CLI helpers.
    def print_runtime_error_rollback_preview_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Error and Rollback Preview Safety Boundary"))

    def handle_runtime_error_rollback_preview_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime error rollback preview"
        manager = AuraRuntimeErrorRollbackPreviewFoundationManager(project_root=self.project_root)

        if command == "runtime-error-rollback-preview-status":
            self.print_runtime_error_rollback_preview_packet("AURA Runtime Error and Rollback Preview Foundation Status", manager.status())
            return True

        if command == "runtime-error-rollback-preview-context":
            self.print_runtime_error_rollback_preview_packet("AURA Runtime Error and Rollback Preview Foundation Context", manager.context())
            return True

        command_map = {
            "runtime-error-taxonomy-preview-plan": ("AURA Runtime Error Taxonomy Preview Plan", manager.runtime_error_taxonomy_preview_plan),
            "rollback-preview-packet-plan": ("AURA Rollback Preview Packet Plan", manager.rollback_preview_packet_plan),
            "failure-recovery-state-model-plan": ("AURA Failure Recovery State Model Plan", manager.failure_recovery_state_model_plan),
            "cancellation-boundary-preview-plan": ("AURA Cancellation Boundary Preview Plan", manager.cancellation_boundary_preview_plan),
            "partial-execution-guard-preview-plan": ("AURA Partial Execution Guard Preview Plan", manager.partial_execution_guard_preview_plan),
            "permission-error-review-plan": ("AURA Permission Error Review Plan", manager.permission_error_review_plan),
            "audit-error-reference-preview-plan": ("AURA Audit Error Reference Preview Plan", manager.audit_error_reference_preview_plan),
            "dashboard-error-rollback-payload-plan": ("AURA Dashboard Error Rollback Payload Plan", manager.dashboard_error_rollback_payload_plan),
            "future-runtime-recovery-boundary-plan": ("AURA Future Runtime Recovery Boundary Plan", manager.future_runtime_recovery_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_error_rollback_preview_packet(title, handler(target))
            return True

        return False

    # Sprint 116.0 ORION client boundary contract CLI helpers.
    def print_orion_client_boundary_contract_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="ORION Client Boundary Contract Safety Boundary"))

    def handle_orion_client_boundary_contract_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA ORION client boundary contract"
        manager = AuraOrionClientBoundaryContractFoundationManager(project_root=self.project_root)

        if command == "orion-client-boundary-contract-status":
            self.print_orion_client_boundary_contract_packet("AURA ORION Client Boundary Contract Foundation Status", manager.status())
            return True

        if command == "orion-client-boundary-contract-context":
            self.print_orion_client_boundary_contract_packet("AURA ORION Client Boundary Contract Foundation Context", manager.context())
            return True

        command_map = {
            "orion-client-identity-boundary-plan": ("AURA ORION Client Identity Boundary Plan", manager.orion_client_identity_boundary_plan),
            "atlas-orion-authority-boundary-plan": ("AURA ATLAS ORION Authority Boundary Plan", manager.atlas_orion_authority_boundary_plan),
            "orion-sense-permission-boundary-plan": ("AURA ORION Sense Permission Boundary Plan", manager.orion_sense_permission_boundary_plan),
            "orion-local-action-boundary-plan": ("AURA ORION Local Action Boundary Plan", manager.orion_local_action_boundary_plan),
            "orion-emergency-stop-boundary-plan": ("AURA ORION Emergency Stop Boundary Plan", manager.orion_emergency_stop_boundary_plan),
            "orion-dashboard-status-boundary-plan": ("AURA ORION Dashboard Status Boundary Plan", manager.orion_dashboard_status_boundary_plan),
            "orion-runtime-handshake-boundary-plan": ("AURA ORION Runtime Handshake Boundary Plan", manager.orion_runtime_handshake_boundary_plan),
            "orion-data-flow-redaction-boundary-plan": ("AURA ORION Data Flow Redaction Boundary Plan", manager.orion_data_flow_redaction_boundary_plan),
            "future-orion-runtime-boundary-plan": ("AURA Future ORION Runtime Boundary Plan", manager.future_orion_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_orion_client_boundary_contract_packet(title, handler(target))
            return True

        return False

    # Sprint 115.0 safe local action contract review CLI helpers.
    def print_safe_local_action_contract_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Action Contract Review Safety Boundary"))

    def handle_safe_local_action_contract_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA safe local action contract review"
        manager = AuraSafeLocalActionContractReviewFoundationManager(project_root=self.project_root)

        if command == "safe-local-action-contract-review-status":
            self.print_safe_local_action_contract_review_packet("AURA Safe Local Action Contract Review Foundation Status", manager.status())
            return True

        if command == "safe-local-action-contract-review-context":
            self.print_safe_local_action_contract_review_packet("AURA Safe Local Action Contract Review Foundation Context", manager.context())
            return True

        command_map = {
            "local-open-contract-review-plan": ("AURA Local Open Contract Review Plan", manager.local_open_contract_review_plan),
            "controlled-create-contract-review-plan": ("AURA Controlled Create Contract Review Plan", manager.controlled_create_contract_review_plan),
            "controlled-write-preview-contract-review-plan": ("AURA Controlled Write Preview Contract Review Plan", manager.controlled_write_preview_contract_review_plan),
            "action-preview-packet-contract-plan": ("AURA Action Preview Packet Contract Plan", manager.action_preview_packet_contract_plan),
            "permission-scope-contract-review-plan": ("AURA Permission Scope Contract Review Plan", manager.permission_scope_contract_review_plan),
            "side-effect-boundary-contract-plan": ("AURA Side Effect Boundary Contract Plan", manager.side_effect_boundary_contract_plan),
            "rollback-cancel-contract-review-plan": ("AURA Rollback Cancel Contract Review Plan", manager.rollback_cancel_contract_review_plan),
            "dashboard-contract-payload-plan": ("AURA Dashboard Contract Payload Plan", manager.dashboard_contract_payload_plan),
            "future-action-runtime-boundary-plan": ("AURA Future Action Runtime Boundary Plan", manager.future_action_runtime_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_safe_local_action_contract_review_packet(title, handler(target))
            return True

        return False

    # Sprint 114.0 dashboard runtime readiness view model CLI helpers.
    def print_dashboard_runtime_readiness_view_model_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Runtime Readiness View Model Safety Boundary"))

    def handle_dashboard_runtime_readiness_view_model_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA dashboard runtime readiness view model"
        manager = AuraDashboardRuntimeReadinessViewModelFoundationManager(project_root=self.project_root)

        if command == "dashboard-runtime-readiness-view-model-status":
            self.print_dashboard_runtime_readiness_view_model_packet("AURA Dashboard Runtime Readiness View Model Foundation Status", manager.status())
            return True

        if command == "dashboard-runtime-readiness-view-model-context":
            self.print_dashboard_runtime_readiness_view_model_packet("AURA Dashboard Runtime Readiness View Model Foundation Context", manager.context())
            return True

        command_map = {
            "runtime-readiness-summary-view-plan": ("AURA Runtime Readiness Summary View Plan", manager.runtime_readiness_summary_view_plan),
            "permission-state-view-plan": ("AURA Permission State View Plan", manager.permission_state_view_plan),
            "audit-review-queue-view-plan": ("AURA Audit Review Queue View Plan", manager.audit_review_queue_view_plan),
            "safety-boundary-view-plan": ("AURA Safety Boundary View Plan", manager.safety_boundary_view_plan),
            "orion-boundary-view-plan": ("AURA ORION Boundary View Plan", manager.orion_boundary_view_plan),
            "action-preview-view-plan": ("AURA Action Preview View Plan", manager.action_preview_view_plan),
            "manual-approval-view-plan": ("AURA Manual Approval View Plan", manager.manual_approval_view_plan),
            "v1-cutline-view-plan": ("AURA v1 Cutline View Plan", manager.v1_cutline_view_plan),
            "control-center-payload-view-plan": ("AURA Control Center Payload View Plan", manager.control_center_payload_view_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_dashboard_runtime_readiness_view_model_packet(title, handler(target))
            return True

        return False

    # Sprint 113.0 audit event review queue CLI helpers.
    def print_audit_event_review_queue_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Audit Event Review Queue Safety Boundary"))

    def handle_audit_event_review_queue_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA audit event review queue"
        manager = AuraAuditEventReviewQueueFoundationManager(project_root=self.project_root)

        if command == "audit-event-review-queue-status":
            self.print_audit_event_review_queue_packet("AURA Audit Event Review Queue Foundation Status", manager.status())
            return True

        if command == "audit-event-review-queue-context":
            self.print_audit_event_review_queue_packet("AURA Audit Event Review Queue Foundation Context", manager.context())
            return True

        command_map = {
            "audit-event-intake-schema-plan": ("AURA Audit Event Intake Schema Plan", manager.audit_event_intake_schema_plan),
            "review-queue-state-model-plan": ("AURA Review Queue State Model Plan", manager.review_queue_state_model_plan),
            "audit-event-triage-rule-plan": ("AURA Audit Event Triage Rule Plan", manager.audit_event_triage_rule_plan),
            "permission-linkage-review-plan": ("AURA Permission Linkage Review Plan", manager.permission_linkage_review_plan),
            "runtime-boundary-review-plan": ("AURA Runtime Boundary Review Plan", manager.runtime_boundary_review_plan),
            "redaction-visibility-review-plan": ("AURA Redaction Visibility Review Plan", manager.redaction_visibility_review_plan),
            "dashboard-review-queue-payload-plan": ("AURA Dashboard Review Queue Payload Plan", manager.dashboard_review_queue_payload_plan),
            "review-outcome-catalog-plan": ("AURA Review Outcome Catalog Plan", manager.review_outcome_catalog_plan),
            "future-audit-writer-boundary-plan": ("AURA Future Audit Writer Boundary Plan", manager.future_audit_writer_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_audit_event_review_queue_packet(title, handler(target))
            return True

        return False

    # Sprint 112.0 runtime permission flow consolidation CLI helpers.
    def print_runtime_permission_flow_consolidation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Permission Flow Consolidation Safety Boundary"))

    def handle_runtime_permission_flow_consolidation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime permission flow consolidation"
        manager = AuraRuntimePermissionFlowConsolidationFoundationManager(project_root=self.project_root)

        if command == "runtime-permission-flow-consolidation-status":
            self.print_runtime_permission_flow_consolidation_packet("AURA Runtime Permission Flow Consolidation Foundation Status", manager.status())
            return True

        if command == "runtime-permission-flow-consolidation-context":
            self.print_runtime_permission_flow_consolidation_packet("AURA Runtime Permission Flow Consolidation Foundation Context", manager.context())
            return True

        command_map = {
            "permission-request-schema-consolidation-plan": ("AURA Permission Request Schema Consolidation Plan", manager.permission_request_schema_consolidation_plan),
            "permission-decision-state-model-plan": ("AURA Permission Decision State Model Plan", manager.permission_decision_state_model_plan),
            "manual-approval-checkpoint-plan": ("AURA Manual Approval Checkpoint Plan", manager.manual_approval_checkpoint_plan),
            "denial-cancellation-flow-plan": ("AURA Denial Cancellation Flow Plan", manager.denial_cancellation_flow_plan),
            "permission-scope-boundary-plan": ("AURA Permission Scope Boundary Plan", manager.permission_scope_boundary_plan),
            "high-risk-escalation-rule-plan": ("AURA High Risk Escalation Rule Plan", manager.high_risk_escalation_rule_plan),
            "approval-audit-reference-plan": ("AURA Approval Audit Reference Plan", manager.approval_audit_reference_plan),
            "dashboard-permission-flow-payload-plan": ("AURA Dashboard Permission Flow Payload Plan", manager.dashboard_permission_flow_payload_plan),
            "future-runtime-grant-boundary-plan": ("AURA Future Runtime Grant Boundary Plan", manager.future_runtime_grant_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_permission_flow_consolidation_packet(title, handler(target))
            return True

        return False

    # Sprint 111.0 genesis runtime readiness next block planning CLI helpers.
    def print_genesis_runtime_readiness_next_block_planning_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Genesis Runtime Readiness Next Block Planning Safety Boundary"))

    def handle_genesis_runtime_readiness_next_block_planning_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Sprint 111-120 next block planning"
        manager = AuraGenesisRuntimeReadinessNextBlockPlanningFoundationManager(project_root=self.project_root)

        if command == "genesis-runtime-readiness-next-block-planning-status":
            self.print_genesis_runtime_readiness_next_block_planning_packet("AURA Genesis Runtime Readiness Next Block Planning Foundation Status", manager.status())
            return True

        if command == "genesis-runtime-readiness-next-block-planning-context":
            self.print_genesis_runtime_readiness_next_block_planning_packet("AURA Genesis Runtime Readiness Next Block Planning Foundation Context", manager.context())
            return True

        command_map = {
            "next-block-sprint-candidate-plan": ("AURA Next Block Sprint Candidate Plan", manager.next_block_sprint_candidate_plan),
            "runtime-readiness-continuity-plan": ("AURA Runtime Readiness Continuity Plan", manager.runtime_readiness_continuity_plan),
            "manual-approval-evolution-plan": ("AURA Manual Approval Evolution Plan", manager.manual_approval_evolution_plan),
            "audit-event-evolution-plan": ("AURA Audit Event Evolution Plan", manager.audit_event_evolution_plan),
            "dashboard-contract-evolution-plan": ("AURA Dashboard Contract Evolution Plan", manager.dashboard_contract_evolution_plan),
            "orion-boundary-planning-plan": ("AURA ORION Boundary Planning Plan", manager.orion_boundary_planning_plan),
            "safe-local-action-boundary-plan": ("AURA Safe Local Action Boundary Plan", manager.safe_local_action_boundary_plan),
            "integration-stabilization-plan": ("AURA Integration Stabilization Plan", manager.integration_stabilization_plan),
            "v1-readiness-mapping-plan": ("AURA v1 Readiness Mapping Plan", manager.v1_readiness_mapping_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_genesis_runtime_readiness_next_block_planning_packet(title, handler(target))
            return True

        return False

    # Sprint 110.0 review stabilization 101-110 CLI helpers.
    def print_review_stabilization_101_110_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 101-110 Safety Boundary"))

    def handle_review_stabilization_101_110_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Sprint 101-110 review stabilization"
        manager = AuraReviewStabilization101110FoundationManager(project_root=self.project_root)

        if command == "review-stabilization-101-110-status":
            self.print_review_stabilization_101_110_packet("AURA Review Stabilization 101-110 Foundation Status", manager.status())
            return True

        if command == "review-stabilization-101-110-context":
            self.print_review_stabilization_101_110_packet("AURA Review Stabilization 101-110 Foundation Context", manager.context())
            return True

        command_map = {
            "sprint-completion-inventory-plan": ("AURA Sprint Completion Inventory Plan", manager.sprint_completion_inventory_plan),
            "runtime-readiness-foundation-audit-plan": ("AURA Runtime Readiness Foundation Audit Plan", manager.runtime_readiness_foundation_audit_plan),
            "safety-invariant-verification-plan": ("AURA Safety Invariant Verification Plan", manager.safety_invariant_verification_plan),
            "capability-registry-delta-review-plan": ("AURA Capability Registry Delta Review Plan", manager.capability_registry_delta_review_plan),
            "integration-surface-review-plan": ("AURA Integration Surface Review Plan", manager.integration_surface_review_plan),
            "documentation-roadmap-consistency-plan": ("AURA Documentation Roadmap Consistency Plan", manager.documentation_roadmap_consistency_plan),
            "checkpoint-risk-review-plan": ("AURA Checkpoint Risk Review Plan", manager.checkpoint_risk_review_plan),
            "deferred-runtime-boundary-plan": ("AURA Deferred Runtime Boundary Plan", manager.deferred_runtime_boundary_plan),
            "next-block-readiness-plan": ("AURA Next Block Readiness Plan", manager.next_block_readiness_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_review_stabilization_101_110_packet(title, handler(target))
            return True

        return False

    # Sprint 109.0 runtime safety freeze manual approval barrier CLI helpers.
    def print_runtime_safety_freeze_manual_approval_barrier_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Safety Freeze Manual Approval Barrier Safety Boundary"))

    def handle_runtime_safety_freeze_manual_approval_barrier_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime safety freeze manual approval barrier"
        manager = AuraRuntimeSafetyFreezeManualApprovalBarrierFoundationManager(project_root=self.project_root)

        if command == "runtime-safety-freeze-manual-approval-barrier-status":
            self.print_runtime_safety_freeze_manual_approval_barrier_packet("AURA Runtime Safety Freeze Manual Approval Barrier Foundation Status", manager.status())
            return True

        if command == "runtime-safety-freeze-manual-approval-barrier-context":
            self.print_runtime_safety_freeze_manual_approval_barrier_packet("AURA Runtime Safety Freeze Manual Approval Barrier Foundation Context", manager.context())
            return True

        command_map = {
            "safety-freeze-candidate-inventory-plan": ("AURA Safety Freeze Candidate Inventory Plan", manager.safety_freeze_candidate_inventory_plan),
            "manual-approval-barrier-input-plan": ("AURA Manual Approval Barrier Input Plan", manager.manual_approval_barrier_input_plan),
            "freeze-condition-check-plan": ("AURA Freeze Condition Check Plan", manager.freeze_condition_check_plan),
            "approval-requirement-rule-plan": ("AURA Approval Requirement Rule Plan", manager.approval_requirement_rule_plan),
            "blocked-runtime-catalog-plan": ("AURA Blocked Runtime Catalog Plan", manager.blocked_runtime_catalog_plan),
            "user-confirmation-barrier-plan": ("AURA User Confirmation Barrier Plan", manager.user_confirmation_barrier_plan),
            "emergency-stop-requirement-plan": ("AURA Emergency Stop Requirement Plan", manager.emergency_stop_requirement_plan),
            "audit-freeze-packet-preview-plan": ("AURA Audit Freeze Packet Preview Plan", manager.audit_freeze_packet_preview_plan),
            "dashboard-barrier-payload-plan": ("AURA Dashboard Barrier Payload Plan", manager.dashboard_barrier_payload_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_safety_freeze_manual_approval_barrier_packet(title, handler(target))
            return True

        return False

    # Sprint 108.0 runtime audit event packet preview CLI helpers.
    def print_runtime_audit_event_packet_preview_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Audit Event Packet Preview Safety Boundary"))

    def handle_runtime_audit_event_packet_preview_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime audit event packet preview"
        manager = AuraRuntimeAuditEventPacketPreviewFoundationManager(project_root=self.project_root)

        if command == "runtime-audit-event-packet-preview-status":
            self.print_runtime_audit_event_packet_preview_packet("AURA Runtime Audit Event Packet Preview Foundation Status", manager.status())
            return True

        if command == "runtime-audit-event-packet-preview-context":
            self.print_runtime_audit_event_packet_preview_packet("AURA Runtime Audit Event Packet Preview Foundation Context", manager.context())
            return True

        command_map = {
            "audit-event-candidate-inventory-plan": ("AURA Audit Event Candidate Inventory Plan", manager.audit_event_candidate_inventory_plan),
            "audit-event-input-snapshot-plan": ("AURA Audit Event Input Snapshot Plan", manager.audit_event_input_snapshot_plan),
            "runtime-reference-mapping-plan": ("AURA Runtime Reference Mapping Plan", manager.runtime_reference_mapping_plan),
            "permission-reference-mapping-plan": ("AURA Permission Reference Mapping Plan", manager.permission_reference_mapping_plan),
            "action-preview-reference-plan": ("AURA Action Preview Reference Plan", manager.action_preview_reference_plan),
            "audit-payload-shape-plan": ("AURA Audit Payload Shape Plan", manager.audit_payload_shape_plan),
            "audit-visibility-rule-plan": ("AURA Audit Visibility Rule Plan", manager.audit_visibility_rule_plan),
            "retention-redaction-boundary-plan": ("AURA Retention Redaction Boundary Plan", manager.retention_redaction_boundary_plan),
            "dashboard-audit-packet-plan": ("AURA Dashboard Audit Packet Plan", manager.dashboard_audit_packet_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_audit_event_packet_preview_packet(title, handler(target))
            return True

        return False

    # Sprint 107.0 local runtime execution gate dry-run CLI helpers.
    def print_local_runtime_execution_gate_dry_run_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Runtime Execution Gate Dry-Run Safety Boundary"))

    def handle_local_runtime_execution_gate_dry_run_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local runtime execution gate dry-run"
        manager = AuraLocalRuntimeExecutionGateDryRunFoundationManager(project_root=self.project_root)

        if command == "local-runtime-execution-gate-dry-run-status":
            self.print_local_runtime_execution_gate_dry_run_packet("AURA Local Runtime Execution Gate Dry-Run Foundation Status", manager.status())
            return True

        if command == "local-runtime-execution-gate-dry-run-context":
            self.print_local_runtime_execution_gate_dry_run_packet("AURA Local Runtime Execution Gate Dry-Run Foundation Context", manager.context())
            return True

        command_map = {
            "execution-gate-candidate-inventory-plan": ("AURA Execution Gate Candidate Inventory Plan", manager.execution_gate_candidate_inventory_plan),
            "runtime-gate-input-contract-plan": ("AURA Runtime Gate Input Contract Plan", manager.runtime_gate_input_contract_plan),
            "gate-preflight-evaluation-plan": ("AURA Gate Preflight Evaluation Plan", manager.gate_preflight_evaluation_plan),
            "safe-runtime-profile-reference-plan": ("AURA Safe Runtime Profile Reference Plan", manager.safe_runtime_profile_reference_plan),
            "permission-gate-reference-plan": ("AURA Permission Gate Reference Plan", manager.permission_gate_reference_plan),
            "execution-gate-decision-plan": ("AURA Execution Gate Decision Plan", manager.execution_gate_decision_plan),
            "block-reason-catalog-plan": ("AURA Block Reason Catalog Plan", manager.block_reason_catalog_plan),
            "audit-gate-record-plan": ("AURA Audit Gate Record Plan", manager.audit_gate_record_plan),
            "dashboard-gate-payload-plan": ("AURA Dashboard Gate Payload Plan", manager.dashboard_gate_payload_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_runtime_execution_gate_dry_run_packet(title, handler(target))
            return True

        return False

    # Sprint 106.0 runtime action execution preview packet CLI helpers.
    def print_runtime_action_execution_preview_packet_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Action Execution Preview Packet Safety Boundary"))

    def handle_runtime_action_execution_preview_packet_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime action execution preview packet"
        manager = AuraRuntimeActionExecutionPreviewPacketFoundationManager(project_root=self.project_root)

        if command == "runtime-action-execution-preview-packet-status":
            self.print_runtime_action_execution_preview_packet_packet("AURA Runtime Action Execution Preview Packet Foundation Status", manager.status())
            return True

        if command == "runtime-action-execution-preview-packet-context":
            self.print_runtime_action_execution_preview_packet_packet("AURA Runtime Action Execution Preview Packet Foundation Context", manager.context())
            return True

        command_map = {
            "action-candidate-inventory-plan": ("AURA Action Candidate Inventory Plan", manager.action_candidate_inventory_plan),
            "execution-preflight-checklist-plan": ("AURA Execution Preflight Checklist Plan", manager.execution_preflight_checklist_plan),
            "action-input-snapshot-plan": ("AURA Action Input Snapshot Plan", manager.action_input_snapshot_plan),
            "permission-decision-reference-plan": ("AURA Permission Decision Reference Plan", manager.permission_decision_reference_plan),
            "execution-step-preview-plan": ("AURA Execution Step Preview Plan", manager.execution_step_preview_plan),
            "side-effect-boundary-plan": ("AURA Side Effect Boundary Plan", manager.side_effect_boundary_plan),
            "rollback-preview-plan": ("AURA Rollback Preview Plan", manager.rollback_preview_plan),
            "audit-preview-record-plan": ("AURA Audit Preview Record Plan", manager.audit_preview_record_plan),
            "user-confirmation-packet-plan": ("AURA User Confirmation Packet Plan", manager.user_confirmation_packet_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_runtime_action_execution_preview_packet_packet(title, handler(target))
            return True

        return False

    # Sprint 105.0 permission decision runtime dry-run CLI helpers.
    def print_permission_decision_runtime_dry_run_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Decision Runtime Dry-Run Safety Boundary"))

    def handle_permission_decision_runtime_dry_run_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA permission decision runtime dry-run"
        manager = AuraPermissionDecisionRuntimeDryRunFoundationManager(project_root=self.project_root)

        if command == "permission-decision-runtime-dry-run-status":
            self.print_permission_decision_runtime_dry_run_packet("AURA Permission Decision Runtime Dry-Run Foundation Status", manager.status())
            return True

        if command == "permission-decision-runtime-dry-run-context":
            self.print_permission_decision_runtime_dry_run_packet("AURA Permission Decision Runtime Dry-Run Foundation Context", manager.context())
            return True

        command_map = {
            "permission-decision-candidate-inventory-plan": ("AURA Permission Decision Candidate Inventory Plan", manager.permission_decision_candidate_inventory_plan),
            "permission-decision-input-contract-plan": ("AURA Permission Decision Input Contract Plan", manager.permission_decision_input_contract_plan),
            "permission-decision-dry-run-evaluation-plan": ("AURA Permission Decision Dry-Run Evaluation Plan", manager.permission_decision_dry_run_evaluation_plan),
            "permission-scope-mapping-plan": ("AURA Permission Scope Mapping Plan", manager.permission_scope_mapping_plan),
            "approval-denial-outcome-plan": ("AURA Approval Denial Outcome Plan", manager.approval_denial_outcome_plan),
            "permission-risk-review-rule-plan": ("AURA Permission Risk Review Rule Plan", manager.risk_review_rule_plan),
            "permission-audit-record-blueprint-plan": ("AURA Permission Audit Record Blueprint Plan", manager.audit_record_blueprint_plan),
            "permission-dashboard-review-payload-plan": ("AURA Permission Dashboard Review Payload Plan", manager.dashboard_review_payload_plan),
            "permission-dry-run-safety-boundary-plan": ("AURA Permission Dry-Run Safety Boundary Plan", manager.dry_run_safety_boundary_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_permission_decision_runtime_dry_run_packet(title, handler(target))
            return True

        return False

    # Sprint 104.0 dashboard API contract consolidation CLI helpers.
    def print_dashboard_api_contract_consolidation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard API Contract Consolidation Safety Boundary"))

    def handle_dashboard_api_contract_consolidation_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Dashboard API contract consolidation"
        manager = AuraDashboardApiContractConsolidationFoundationManager(project_root=self.project_root)

        if command == "dashboard-api-contract-consolidation-status":
            self.print_dashboard_api_contract_consolidation_packet("AURA Dashboard API Contract Consolidation Foundation Status", manager.status())
            return True

        if command == "dashboard-api-contract-consolidation-context":
            self.print_dashboard_api_contract_consolidation_packet("AURA Dashboard API Contract Consolidation Foundation Context", manager.context())
            return True

        command_map = {
            "api-contract-inventory-plan": ("AURA API Contract Inventory Plan", manager.api_contract_inventory_plan),
            "endpoint-schema-alignment-plan": ("AURA Endpoint Schema Alignment Plan", manager.endpoint_schema_alignment_plan),
            "request-response-contract-plan": ("AURA Request Response Contract Plan", manager.request_response_contract_plan),
            "permission-contract-mapping-plan": ("AURA Permission Contract Mapping Plan", manager.permission_contract_mapping_plan),
            "dashboard-status-payload-plan": ("AURA Dashboard Status Payload Plan", manager.dashboard_status_payload_plan),
            "error-response-contract-plan": ("AURA Error Response Contract Plan", manager.error_response_contract_plan),
            "mock-api-boundary-plan": ("AURA Mock API Boundary Plan", manager.mock_api_boundary_plan),
            "frontend-backend-contract-boundary-plan": ("AURA Frontend Backend Contract Boundary Plan", manager.frontend_backend_contract_boundary_plan),
            "contract-validation-checklist-plan": ("AURA Contract Validation Checklist Plan", manager.contract_validation_checklist_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_dashboard_api_contract_consolidation_packet(title, handler(target))
            return True

        return False

    # Sprint 103.0 local service start proposal review CLI helpers.
    def print_local_service_start_proposal_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Start Proposal Review Safety Boundary"))

    def handle_local_service_start_proposal_review_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA local service start proposal review"
        manager = AuraLocalServiceStartProposalReviewFoundationManager(project_root=self.project_root)

        if command == "local-service-start-proposal-review-status":
            self.print_local_service_start_proposal_review_packet("AURA Local Service Start Proposal Review Foundation Status", manager.status())
            return True

        if command == "local-service-start-proposal-review-context":
            self.print_local_service_start_proposal_review_packet("AURA Local Service Start Proposal Review Foundation Context", manager.context())
            return True

        command_map = {
            "service-start-candidate-inventory-plan": ("AURA Service Start Candidate Inventory Plan", manager.service_start_candidate_inventory_plan),
            "service-start-preflight-requirement-plan": ("AURA Service Start Preflight Requirement Plan", manager.service_start_preflight_requirement_plan),
            "port-binding-review-plan": ("AURA Port Binding Review Plan", manager.port_binding_review_plan),
            "process-launch-boundary-plan": ("AURA Process Launch Boundary Plan", manager.process_launch_boundary_plan),
            "permission-requirement-plan": ("AURA Permission Requirement Plan", manager.permission_requirement_plan),
            "risk-classification-plan": ("AURA Risk Classification Plan", manager.risk_classification_plan),
            "rollback-kill-switch-plan": ("AURA Rollback Kill-Switch Plan", manager.rollback_kill_switch_plan),
            "audit-event-plan": ("AURA Audit Event Plan", manager.audit_event_plan),
            "user-approval-decision-plan": ("AURA User Approval Decision Plan", manager.user_approval_decision_plan),
        }

        if command in command_map:
            title, handler = command_map[command]
            self.print_local_service_start_proposal_review_packet(title, handler(target))
            return True

        return False

    # Sprint 102.0 safe runtime configuration profile foundation CLI helpers.
    def print_safe_runtime_configuration_profile_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Runtime Configuration Profile Safety Boundary"))

    def handle_safe_runtime_configuration_profile_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA safe runtime configuration profile foundation"
        manager = AuraSafeRuntimeConfigurationProfileFoundationManager(project_root=self.project_root)

        if command == "safe-runtime-configuration-profile-status":
            self.print_safe_runtime_configuration_profile_packet("AURA Safe Runtime Configuration Profile Foundation Status", manager.status())
            return True

        if command == "configuration-profile-type-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Configuration Profile Type Plan", manager.configuration_profile_type_plan(target))
            return True

        if command == "runtime-mode-policy-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Runtime Mode Policy Plan", manager.runtime_mode_policy_plan(target))
            return True

        if command == "service-configuration-boundary-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Service Configuration Boundary Plan", manager.service_configuration_boundary_plan(target))
            return True

        if command == "permission-configuration-boundary-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Permission Configuration Boundary Plan", manager.permission_configuration_boundary_plan(target))
            return True

        if command == "file-system-configuration-boundary-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA File System Configuration Boundary Plan", manager.file_system_configuration_boundary_plan(target))
            return True

        if command == "network-configuration-boundary-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Network Configuration Boundary Plan", manager.network_configuration_boundary_plan(target))
            return True

        if command == "dry-run-configuration-requirement-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Dry-Run Configuration Requirement Plan", manager.dry_run_configuration_requirement_plan(target))
            return True

        if command == "rollout-configuration-guard-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Rollout Configuration Guard Plan", manager.rollout_configuration_guard_plan(target))
            return True

        if command == "configuration-audit-visibility-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Configuration Audit Visibility Plan", manager.configuration_audit_visibility_plan(target))
            return True

        if command == "safe-runtime-configuration-profile-safety-policy-plan":
            self.print_safe_runtime_configuration_profile_packet("AURA Safe Runtime Configuration Profile Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "safe-runtime-configuration-profile-context":
            self.print_safe_runtime_configuration_profile_packet("AURA Safe Runtime Configuration Profile Foundation Context", manager.context())
            return True

        return False

    # Sprint 101.0 genesis runtime readiness baseline foundation CLI helpers.
    def print_genesis_runtime_readiness_baseline_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Genesis Runtime Readiness Baseline Safety Boundary"))

    def handle_genesis_runtime_readiness_baseline_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Genesis runtime readiness baseline foundation"
        manager = AuraGenesisRuntimeReadinessBaselineFoundationManager(project_root=self.project_root)

        if command == "genesis-runtime-readiness-baseline-status":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Genesis Runtime Readiness Baseline Foundation Status", manager.status())
            return True

        if command == "readiness-domain-inventory-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Readiness Domain Inventory Plan", manager.readiness_domain_inventory_plan(target))
            return True

        if command == "runtime-candidate-classification-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Runtime Candidate Classification Plan", manager.runtime_candidate_classification_plan(target))
            return True

        if command == "dry-run-prerequisite-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Dry-Run Prerequisite Plan", manager.dry_run_prerequisite_plan(target))
            return True

        if command == "permission-requirement-matrix-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Permission Requirement Matrix Plan", manager.permission_requirement_matrix_plan(target))
            return True

        if command == "safety-gate-alignment-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Safety Gate Alignment Plan", manager.safety_gate_alignment_plan(target))
            return True

        if command == "rollback-and-kill-switch-readiness-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Rollback and Kill-Switch Readiness Plan", manager.rollback_and_kill_switch_readiness_plan(target))
            return True

        if command == "audit-and-observability-readiness-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Audit and Observability Readiness Plan", manager.audit_and_observability_readiness_plan(target))
            return True

        if command == "rollout-phase-recommendation-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Rollout Phase Recommendation Plan", manager.rollout_phase_recommendation_plan(target))
            return True

        if command == "block-101-110-alignment-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Block 101-110 Alignment Plan", manager.block_101_110_alignment_plan(target))
            return True

        if command == "genesis-runtime-readiness-baseline-safety-policy-plan":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Genesis Runtime Readiness Baseline Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "genesis-runtime-readiness-baseline-context":
            self.print_genesis_runtime_readiness_baseline_packet("AURA Genesis Runtime Readiness Baseline Foundation Context", manager.context())
            return True

        return False

    # Sprint 100.0 review and stabilization foundation CLI helpers.
    def print_sprint_100_review_stabilization_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Sprint 100 Review Stabilization Safety Boundary"))

    def handle_sprint_100_review_stabilization_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Sprint 100 review stabilization foundation"
        manager = AuraSprint100ReviewStabilizationFoundationManager(project_root=self.project_root)

        if command == "sprint-100-review-stabilization-status":
            self.print_sprint_100_review_stabilization_packet("AURA Sprint 100 Review & Stabilization Foundation Status", manager.status())
            return True

        if command == "sprint-block-review-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Sprint Block Review Plan", manager.sprint_block_review_plan(target))
            return True

        if command == "completed-feature-inventory-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Completed Feature Inventory Plan", manager.completed_feature_inventory_plan(target))
            return True

        if command == "active-vs-foundation-boundary-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Active vs Foundation Boundary Plan", manager.active_vs_foundation_boundary_plan(target))
            return True

        if command == "runtime-zero-safety-check-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Runtime Zero Safety Check Plan", manager.runtime_zero_safety_check_plan(target))
            return True

        if command == "capability-registry-stabilization-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Capability Registry Stabilization Plan", manager.capability_registry_stabilization_plan(target))
            return True

        if command == "documentation-stabilization-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Documentation Stabilization Plan", manager.documentation_stabilization_plan(target))
            return True

        if command == "unresolved-future-feature-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Unresolved Future Feature Plan", manager.unresolved_future_feature_plan(target))
            return True

        if command == "roadmap-101-110-seed-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Roadmap 101-110 Seed Plan", manager.roadmap_101_110_seed_plan(target))
            return True

        if command == "sprint-100-release-readiness-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Sprint 100 Release Readiness Plan", manager.sprint_100_release_readiness_plan(target))
            return True

        if command == "sprint-100-review-stabilization-safety-policy-plan":
            self.print_sprint_100_review_stabilization_packet("AURA Sprint 100 Review Stabilization Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "sprint-100-review-stabilization-context":
            self.print_sprint_100_review_stabilization_packet("AURA Sprint 100 Review & Stabilization Foundation Context", manager.context())
            return True

        return False

    # Sprint 99.0 pre-runtime security audit foundation CLI helpers.
    def print_pre_runtime_security_audit_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Pre-Runtime Security Audit Safety Boundary"))

    def handle_pre_runtime_security_audit_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA pre-runtime security audit foundation"
        manager = AuraPreRuntimeSecurityAuditFoundationManager(project_root=self.project_root)

        if command == "pre-runtime-security-audit-status":
            self.print_pre_runtime_security_audit_packet("AURA Pre-Runtime Security Audit Foundation Status", manager.status())
            return True

        if command == "security-audit-domain-plan":
            self.print_pre_runtime_security_audit_packet("AURA Security Audit Domain Plan", manager.security_audit_domain_plan(target))
            return True

        if command == "runtime-gate-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Runtime Gate Check Plan", manager.runtime_gate_check_plan(target))
            return True

        if command == "permission-boundary-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Permission Boundary Check Plan", manager.permission_boundary_check_plan(target))
            return True

        if command == "file-system-safety-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA File System Safety Check Plan", manager.file_system_safety_check_plan(target))
            return True

        if command == "network-surface-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Network Surface Check Plan", manager.network_surface_check_plan(target))
            return True

        if command == "action-execution-safety-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Action Execution Safety Check Plan", manager.action_execution_safety_check_plan(target))
            return True

        if command == "orion-boundary-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA ORION Boundary Check Plan", manager.orion_boundary_check_plan(target))
            return True

        if command == "audit-visibility-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Audit Visibility Check Plan", manager.audit_visibility_check_plan(target))
            return True

        if command == "stabilization-readiness-check-plan":
            self.print_pre_runtime_security_audit_packet("AURA Stabilization Readiness Check Plan", manager.stabilization_readiness_check_plan(target))
            return True

        if command == "pre-runtime-security-audit-safety-policy-plan":
            self.print_pre_runtime_security_audit_packet("AURA Pre-Runtime Security Audit Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "pre-runtime-security-audit-context":
            self.print_pre_runtime_security_audit_packet("AURA Pre-Runtime Security Audit Foundation Context", manager.context())
            return True

        return False

    # Sprint 98.0 runtime action queue review layer foundation CLI helpers.
    def print_runtime_action_queue_review_layer_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Action Queue Review Layer Safety Boundary"))

    def handle_runtime_action_queue_review_layer_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA runtime action queue review layer foundation"
        manager = AuraRuntimeActionQueueReviewLayerFoundationManager(project_root=self.project_root)

        if command == "runtime-action-queue-review-layer-status":
            self.print_runtime_action_queue_review_layer_packet("AURA Runtime Action Queue Review Layer Foundation Status", manager.status())
            return True

        if command == "action-queue-item-blueprint-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Action Queue Item Blueprint Plan", manager.action_queue_item_blueprint_plan(target))
            return True

        if command == "queue-state-blueprint-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Queue State Blueprint Plan", manager.queue_state_blueprint_plan(target))
            return True

        if command == "review-priority-rule-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Review Priority Rule Plan", manager.review_priority_rule_plan(target))
            return True

        if command == "dependency-blocker-contract-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Dependency Blocker Contract Plan", manager.dependency_blocker_contract_plan(target))
            return True

        if command == "permission-link-requirement-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Permission Link Requirement Plan", manager.permission_link_requirement_plan(target))
            return True

        if command == "execution-preflight-check-blueprint-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Execution Preflight Check Blueprint Plan", manager.execution_preflight_check_blueprint_plan(target))
            return True

        if command == "approval-denial-transition-rule-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Approval Denial Transition Rule Plan", manager.approval_denial_transition_rule_plan(target))
            return True

        if command == "timeout-expiry-policy-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Timeout Expiry Policy Plan", manager.timeout_expiry_policy_plan(target))
            return True

        if command == "runtime-action-audit-visibility-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Runtime Action Audit Visibility Plan", manager.runtime_action_audit_visibility_plan(target))
            return True

        if command == "runtime-action-queue-review-layer-safety-policy-plan":
            self.print_runtime_action_queue_review_layer_packet("AURA Runtime Action Queue Review Layer Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "runtime-action-queue-review-layer-context":
            self.print_runtime_action_queue_review_layer_packet("AURA Runtime Action Queue Review Layer Foundation Context", manager.context())
            return True

        return False

    # Sprint 97.0 controlled file write approval draft foundation CLI helpers.
    def print_controlled_file_write_approval_draft_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Controlled File Write Approval Draft Safety Boundary"))

    def handle_controlled_file_write_approval_draft_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA controlled file write approval draft foundation"
        manager = AuraControlledFileWriteApprovalDraftFoundationManager(project_root=self.project_root)

        if command == "controlled-file-write-approval-draft-status":
            self.print_controlled_file_write_approval_draft_packet("AURA Controlled File Write Approval Draft Foundation Status", manager.status())
            return True

        if command == "file-write-proposal-draft-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA File Write Proposal Draft Plan", manager.file_write_proposal_draft_plan(target))
            return True

        if command == "target-path-policy-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Target Path Policy Plan", manager.target_path_policy_plan(target))
            return True

        if command == "diff-preview-contract-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Diff Preview Contract Plan", manager.diff_preview_contract_plan(target))
            return True

        if command == "overwrite-rule-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Overwrite Rule Plan", manager.overwrite_rule_plan(target))
            return True

        if command == "backup-requirement-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Backup Requirement Plan", manager.backup_requirement_plan(target))
            return True

        if command == "approval-checklist-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Approval Checklist Plan", manager.approval_checklist_plan(target))
            return True

        if command == "rollback-note-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA Rollback Note Plan", manager.rollback_note_plan(target))
            return True

        if command == "file-write-audit-visibility-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA File Write Audit Visibility Plan", manager.file_write_audit_visibility_plan(target))
            return True

        if command == "file-write-safety-policy-plan":
            self.print_controlled_file_write_approval_draft_packet("AURA File Write Safety Policy Plan", manager.file_write_safety_policy_plan(target))
            return True

        if command == "controlled-file-write-approval-draft-context":
            self.print_controlled_file_write_approval_draft_packet("AURA Controlled File Write Approval Draft Foundation Context", manager.context())
            return True

        return False

    # Sprint 96.0 safe local web runtime gate foundation CLI helpers.
    def print_safe_local_web_runtime_gate_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Web Runtime Gate Safety Boundary"))

    def handle_safe_local_web_runtime_gate_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA safe local web runtime gate foundation"
        manager = AuraSafeLocalWebRuntimeGateFoundationManager(project_root=self.project_root)

        if command == "safe-local-web-runtime-gate-status":
            self.print_safe_local_web_runtime_gate_packet("AURA Safe Local Web Runtime Gate Foundation Status", manager.status())
            return True

        if command == "localhost-binding-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Localhost Binding Policy Plan", manager.localhost_binding_policy_plan(target))
            return True

        if command == "port-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Port Policy Plan", manager.port_policy_plan(target))
            return True

        if command == "web-runtime-permission-requirement-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Web Runtime Permission Requirement Plan", manager.permission_requirement_plan(target))
            return True

        if command == "runtime-preflight-check-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Runtime Preflight Check Plan", manager.runtime_preflight_check_plan(target))
            return True

        if command == "start-stop-proposal-contract-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Start Stop Proposal Contract Plan", manager.start_stop_proposal_contract_plan(target))
            return True

        if command == "route-boundary-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Route Boundary Policy Plan", manager.route_boundary_policy_plan(target))
            return True

        if command == "static-asset-boundary-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Static Asset Boundary Policy Plan", manager.static_asset_boundary_policy_plan(target))
            return True

        if command == "kill-switch-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Kill Switch Policy Plan", manager.kill_switch_policy_plan(target))
            return True

        if command == "web-runtime-audit-visibility-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Web Runtime Audit Visibility Plan", manager.web_runtime_audit_visibility_plan(target))
            return True

        if command == "safe-local-web-runtime-gate-safety-policy-plan":
            self.print_safe_local_web_runtime_gate_packet("AURA Safe Local Web Runtime Gate Safety Policy Plan", manager.safety_policy_plan(target))
            return True

        if command == "safe-local-web-runtime-gate-context":
            self.print_safe_local_web_runtime_gate_packet("AURA Safe Local Web Runtime Gate Foundation Context", manager.context())
            return True

        return False

    # Sprint 95.0 chat session persistence planner foundation CLI helpers.
    def print_chat_session_persistence_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Session Persistence Safety Boundary"))

    def handle_chat_session_persistence_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA chat session persistence planner foundation"
        manager = AuraChatSessionPersistencePlannerFoundationManager(project_root=self.project_root)

        if command == "chat-session-persistence-planner-status":
            self.print_chat_session_persistence_packet("AURA Chat Session Persistence Planner Foundation Status", manager.status())
            return True

        if command == "session-record-blueprint-plan":
            self.print_chat_session_persistence_packet("AURA Session Record Blueprint Plan", manager.session_record_blueprint_plan(target))
            return True

        if command == "storage-boundary-blueprint-plan":
            self.print_chat_session_persistence_packet("AURA Storage Boundary Blueprint Plan", manager.storage_boundary_blueprint_plan(target))
            return True

        if command == "retention-policy-blueprint-plan":
            self.print_chat_session_persistence_packet("AURA Retention Policy Blueprint Plan", manager.retention_policy_blueprint_plan(target))
            return True

        if command == "privacy-redaction-rule-plan":
            self.print_chat_session_persistence_packet("AURA Privacy Redaction Rule Plan", manager.privacy_redaction_rule_plan(target))
            return True

        if command == "session-lifecycle-blueprint-plan":
            self.print_chat_session_persistence_packet("AURA Session Lifecycle Blueprint Plan", manager.session_lifecycle_blueprint_plan(target))
            return True

        if command == "recovery-index-blueprint-plan":
            self.print_chat_session_persistence_packet("AURA Recovery Index Blueprint Plan", manager.recovery_index_blueprint_plan(target))
            return True

        if command == "export-migration-note-plan":
            self.print_chat_session_persistence_packet("AURA Export Migration Note Plan", manager.export_migration_note_plan(target))
            return True

        if command == "chat-persistence-safety-policy-plan":
            self.print_chat_session_persistence_packet("AURA Chat Persistence Safety Policy Plan", manager.chat_persistence_safety_policy_plan(target))
            return True

        if command == "chat-session-persistence-status-packet":
            self.print_chat_session_persistence_packet("AURA Chat Session Persistence Status Packet", manager.status_packet())
            return True

        if command == "chat-session-persistence-context":
            self.print_chat_session_persistence_packet("AURA Chat Session Persistence Planner Foundation Context", manager.context())
            return True

        return False

    # Sprint 94.0 permission request review queue foundation CLI helpers.
    def print_permission_request_review_queue_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Request Review Queue Safety Boundary"))

    def handle_permission_request_review_queue_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA permission request review queue foundation"
        manager = AuraPermissionRequestReviewQueueFoundationManager(project_root=self.project_root)

        if command == "permission-request-review-queue-status":
            self.print_permission_request_review_queue_packet("AURA Permission Request Review Queue Foundation Status", manager.status())
            return True

        if command == "permission-request-blueprint-plan":
            self.print_permission_request_review_queue_packet("AURA Permission Request Blueprint Plan", manager.permission_request_blueprint_plan(target))
            return True

        if command == "queue-state-blueprint-plan":
            self.print_permission_request_review_queue_packet("AURA Queue State Blueprint Plan", manager.queue_state_blueprint_plan(target))
            return True

        if command == "review-packet-field-plan":
            self.print_permission_request_review_queue_packet("AURA Review Packet Field Plan", manager.review_packet_field_plan(target))
            return True

        if command == "permission-scope-boundary-plan":
            self.print_permission_request_review_queue_packet("AURA Permission Scope Boundary Plan", manager.permission_scope_boundary_plan(target))
            return True

        if command == "decision-proposal-contract-plan":
            self.print_permission_request_review_queue_packet("AURA Decision Proposal Contract Plan", manager.decision_proposal_contract_plan(target))
            return True

        if command == "reviewer-checklist-plan":
            self.print_permission_request_review_queue_packet("AURA Reviewer Checklist Plan", manager.reviewer_checklist_plan(target))
            return True

        if command == "audit-visibility-field-plan":
            self.print_permission_request_review_queue_packet("AURA Audit Visibility Field Plan", manager.audit_visibility_field_plan(target))
            return True

        if command == "permission-request-safety-policy-plan":
            self.print_permission_request_review_queue_packet("AURA Permission Request Safety Policy Plan", manager.permission_request_safety_policy_plan(target))
            return True

        if command == "permission-request-review-queue-status-packet":
            self.print_permission_request_review_queue_packet("AURA Permission Request Review Queue Status Packet", manager.status_packet())
            return True

        if command == "permission-request-review-queue-context":
            self.print_permission_request_review_queue_packet("AURA Permission Request Review Queue Foundation Context", manager.context())
            return True

        return False

    # Sprint 93.0 control center data aggregator foundation CLI helpers.
    def print_control_center_data_aggregator_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Data Aggregator Safety Boundary"))

    def handle_control_center_data_aggregator_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Control Center data aggregator foundation"
        manager = AuraControlCenterDataAggregatorFoundationManager(project_root=self.project_root)

        if command == "control-center-data-aggregator-status":
            self.print_control_center_data_aggregator_packet("AURA Control Center Data Aggregator Foundation Status", manager.status())
            return True

        if command == "aggregator-packet-catalog-plan":
            self.print_control_center_data_aggregator_packet("AURA Aggregator Packet Catalog Plan", manager.aggregator_packet_catalog_plan(target))
            return True

        if command == "atlas-core-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA ATLAS Core Packet Plan", manager.atlas_core_packet_plan(target))
            return True

        if command == "orion-client-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA ORION Client Packet Plan", manager.orion_client_packet_plan(target))
            return True

        if command == "client-bridge-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA Client Bridge Packet Plan", manager.client_bridge_packet_plan(target))
            return True

        if command == "dashboard-view-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA Dashboard View Packet Plan", manager.dashboard_view_packet_plan(target))
            return True

        if command == "permission-scope-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA Permission Scope Packet Plan", manager.permission_scope_packet_plan(target))
            return True

        if command == "health-snapshot-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA Health Snapshot Packet Plan", manager.health_snapshot_packet_plan(target))
            return True

        if command == "audit-event-visibility-packet-plan":
            self.print_control_center_data_aggregator_packet("AURA Audit Event Visibility Packet Plan", manager.audit_event_visibility_packet_plan(target))
            return True

        if command == "data-aggregator-safety-policy-plan":
            self.print_control_center_data_aggregator_packet("AURA Data Aggregator Safety Policy Plan", manager.data_aggregator_safety_policy_plan(target))
            return True

        if command == "control-center-data-aggregator-context":
            self.print_control_center_data_aggregator_packet("AURA Control Center Data Aggregator Foundation Context", manager.context())
            return True

        return False

    # Sprint 92.0 local console API schema foundation CLI helpers.
    def print_local_console_api_schema_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console API Schema Safety Boundary"))

    def handle_local_console_api_schema_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Local Console API schema foundation"
        manager = AuraLocalConsoleAPISchemaFoundationManager(project_root=self.project_root)

        if command == "local-console-api-schema-status":
            self.print_local_console_api_schema_packet("AURA Local Console API Schema Foundation Status", manager.status())
            return True

        if command == "api-schema-catalog-plan":
            self.print_local_console_api_schema_packet("AURA API Schema Catalog Plan", manager.api_schema_catalog_plan(target))
            return True

        if command == "endpoint-blueprint-plan":
            self.print_local_console_api_schema_packet("AURA Endpoint Blueprint Plan", manager.endpoint_blueprint_plan(target))
            return True

        if command == "response-envelope-plan":
            self.print_local_console_api_schema_packet("AURA Response Envelope Plan", manager.response_envelope_plan(target))
            return True

        if command == "request-schema-blueprint-plan":
            self.print_local_console_api_schema_packet("AURA Request Schema Blueprint Plan", manager.request_schema_blueprint_plan(target))
            return True

        if command == "validation-rule-plan":
            self.print_local_console_api_schema_packet("AURA Validation Rule Plan", manager.validation_rule_plan(target))
            return True

        if command == "permission-boundary-schema-plan":
            self.print_local_console_api_schema_packet("AURA Permission Boundary Schema Plan", manager.permission_boundary_schema_plan(target))
            return True

        if command == "error-contract-plan":
            self.print_local_console_api_schema_packet("AURA Error Contract Plan", manager.error_contract_plan(target))
            return True

        if command == "schema-versioning-plan":
            self.print_local_console_api_schema_packet("AURA Schema Versioning Plan", manager.schema_versioning_plan(target))
            return True

        if command == "api-schema-safety-policy-plan":
            self.print_local_console_api_schema_packet("AURA API Schema Safety Policy Plan", manager.api_schema_safety_policy_plan(target))
            return True

        if command == "local-console-api-schema-context":
            self.print_local_console_api_schema_packet("AURA Local Console API Schema Foundation Context", manager.context())
            return True

        return False

    # Sprint 91.0 local console static prototype foundation CLI helpers.
    def print_local_console_static_prototype_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console Static Prototype Safety Boundary"))

    def handle_local_console_static_prototype_cli_command(self, raw_args: list[str]) -> bool:
        if not raw_args:
            return False

        command = raw_args[0]
        target = " ".join(raw_args[1:]).strip() or "AURA Local Console static prototype foundation"
        manager = AuraLocalConsoleStaticPrototypeFoundationManager(project_root=self.project_root)

        if command == "local-console-static-prototype-status":
            self.print_local_console_static_prototype_packet("AURA Local Console Static Prototype Foundation Status", manager.status())
            return True

        if command == "static-prototype-structure-plan":
            self.print_local_console_static_prototype_packet("AURA Static Prototype Structure Plan", manager.static_prototype_structure_plan(target))
            return True

        if command == "static-page-blueprint-plan":
            self.print_local_console_static_prototype_packet("AURA Static Page Blueprint Plan", manager.static_page_blueprint_plan(target))
            return True

        if command == "static-asset-blueprint-plan":
            self.print_local_console_static_prototype_packet("AURA Static Asset Blueprint Plan", manager.static_asset_blueprint_plan(target))
            return True

        if command == "panel-layout-blueprint-plan":
            self.print_local_console_static_prototype_packet("AURA Panel Layout Blueprint Plan", manager.panel_layout_blueprint_plan(target))
            return True

        if command == "route-static-mapping-plan":
            self.print_local_console_static_prototype_packet("AURA Route Static Mapping Plan", manager.route_static_mapping_plan(target))
            return True

        if command == "data-placeholder-contract-plan":
            self.print_local_console_static_prototype_packet("AURA Data Placeholder Contract Plan", manager.data_placeholder_contract_plan(target))
            return True

        if command == "theme-token-blueprint-plan":
            self.print_local_console_static_prototype_packet("AURA Theme Token Blueprint Plan", manager.theme_token_blueprint_plan(target))
            return True

        if command == "accessibility-blueprint-plan":
            self.print_local_console_static_prototype_packet("AURA Accessibility Blueprint Plan", manager.accessibility_blueprint_plan(target))
            return True

        if command == "static-prototype-safety-policy-plan":
            self.print_local_console_static_prototype_packet("AURA Static Prototype Safety Policy Plan", manager.static_prototype_safety_policy_plan(target))
            return True

        if command == "local-console-static-prototype-context":
            self.print_local_console_static_prototype_packet("AURA Local Console Static Prototype Foundation Context", manager.context())
            return True

        return False

    def run(self, args: list[str] | None = None) -> bool:
        if handle_local_interaction_runtime_stabilization_command(args):
            return True

        if handle_permission_audit_recovery_command(args):
            return True

        if handle_interactive_chat_command(args):
            return True

        if handle_local_model_bridge_command(args):
            return True

        if handle_browser_chat_session_command(args):
            return True

        if handle_control_center_web_shell_command(args):
            return True

        if handle_control_center_backend_command(args):
            return True

        if handle_health_status_api_command(args):
            return True

        if handle_service_lifecycle_command(args):
            return True

        if handle_local_web_runtime_command(args):
            return True

        import sys

        raw_args = sys.argv[1:] if args is None else args
        if self.handle_codebase_compat_cli_command(raw_args):
            return True

        if self.handle_voice_conversation_cli_command(raw_args):
            return True

        if self.handle_vision_context_cli_command(raw_args):
            return True

        if self.handle_avatar_interaction_cli_command(raw_args):
            return True

        if self.handle_desktop_workflow_cli_command(raw_args):
            return True

        if self.handle_partner_runtime_cli_command(raw_args):
            return True

        if self.handle_thought_loop_cli_command(raw_args):
            return True

        if self.handle_reasoning_context_cli_command(raw_args):
            return True

        if self.handle_knowledge_uncertainty_cli_command(raw_args):
            return True

        if self.handle_voice_input_cli_command(raw_args):
            return True

        if self.handle_voice_intent_cli_command(raw_args):
            return True

        if self.handle_vision_input_cli_command(raw_args):
            return True

        if self.handle_visual_context_cli_command(raw_args):
            return True

        if self.handle_coder_project_cli_command(raw_args):
            return True

        if self.handle_dependency_permission_cli_command(raw_args):
            return True

        if self.handle_checkpoint_80_cli_command(raw_args):
            return True

        if self.handle_output_formatter_cli_command(raw_args):
            return True

        if self.handle_capability_registry_cli_command(raw_args):
            return True

        if self.handle_permission_workflow_cli_command(raw_args):
            return True

        if self.handle_runtime_service_cli_command(raw_args):
            return True

        if self.handle_launcher_monitor_cli_command(raw_args):
            return True

        if self.handle_control_center_cli_command(raw_args):
            return True

        if self.handle_local_console_web_cli_command(raw_args):
            return True

        if self.handle_chat_bridge_cli_command(raw_args):
            return True

        if self.handle_plugin_permission_dashboard_cli_command(raw_args):
            return True

        if self.handle_local_console_static_prototype_cli_command(raw_args):
            return True

        if self.handle_local_console_api_schema_cli_command(raw_args):
            return True

        if self.handle_control_center_data_aggregator_cli_command(raw_args):
            return True

        if self.handle_permission_request_review_queue_cli_command(raw_args):
            return True

        if self.handle_chat_session_persistence_cli_command(raw_args):
            return True

        if self.handle_safe_local_web_runtime_gate_cli_command(raw_args):
            return True

        if self.handle_controlled_file_write_approval_draft_cli_command(raw_args):
            return True

        if self.handle_runtime_action_queue_review_layer_cli_command(raw_args):
            return True

        if self.handle_pre_runtime_security_audit_cli_command(raw_args):
            return True

        if self.handle_sprint_100_review_stabilization_cli_command(raw_args):
            return True

        if self.handle_genesis_runtime_readiness_baseline_cli_command(raw_args):
            return True

        if self.handle_safe_runtime_configuration_profile_cli_command(raw_args):
            return True

        if self.handle_local_service_start_proposal_review_cli_command(raw_args):
            return True

        if self.handle_dashboard_api_contract_consolidation_cli_command(raw_args):
            return True

        if self.handle_permission_decision_runtime_dry_run_cli_command(raw_args):
            return True

        if self.handle_runtime_action_execution_preview_packet_cli_command(raw_args):
            return True

        if self.handle_local_runtime_execution_gate_dry_run_cli_command(raw_args):
            return True

        if self.handle_runtime_audit_event_packet_preview_cli_command(raw_args):
            return True

        if self.handle_runtime_safety_freeze_manual_approval_barrier_cli_command(raw_args):
            return True

        if self.handle_review_stabilization_101_110_cli_command(raw_args):
            return True

        if self.handle_genesis_runtime_readiness_next_block_planning_cli_command(raw_args):
            return True

        if self.handle_runtime_permission_flow_consolidation_cli_command(raw_args):
            return True

        if self.handle_audit_event_review_queue_cli_command(raw_args):
            return True

        if self.handle_dashboard_runtime_readiness_view_model_cli_command(raw_args):
            return True

        if self.handle_safe_local_action_contract_review_cli_command(raw_args):
            return True

        if self.handle_orion_client_boundary_contract_cli_command(raw_args):
            return True

        if self.handle_runtime_error_rollback_preview_cli_command(raw_args):
            return True

        if self.handle_manual_approval_decision_flow_review_cli_command(raw_args):
            return True

        if self.handle_v1_runtime_readiness_cutline_review_cli_command(raw_args):
            return True

        if self.handle_review_stabilization_111_120_cli_command(raw_args):
            return True

        if self.handle_post_checkpoint_120_next_block_planning_cli_command(raw_args):
            return True

        if self.handle_runtime_permission_audit_writer_boundary_review_cli_command(raw_args):
            return True

        if self.handle_dashboard_control_center_boundary_review_cli_command(raw_args):
            return True

        if self.handle_orion_dry_handshake_boundary_review_cli_command(raw_args):
            return True

        if self.handle_safe_local_action_allowlist_boundary_review_cli_command(raw_args):
            return True

        if self.handle_runtime_grant_expiry_boundary_review_cli_command(raw_args):
            return True

        if self.handle_runtime_recovery_drill_boundary_review_cli_command(raw_args):
            return True

        if self.handle_dashboard_runtime_readiness_boundary_review_cli_command(raw_args):
            return True

        if self.handle_runtime_activation_blocker_register_boundary_review_cli_command(raw_args):
            return True

        if self.handle_review_stabilization_121_130_cli_command(raw_args):
            return True

        if self.handle_post_checkpoint_130_next_block_cli_command(raw_args):
            return True

        if self.handle_final_genesis_acceptance_criteria_cli_command(raw_args):
            return True

        if self.handle_runtime_activation_path_proposal_review_cli_command(raw_args):
            return True

        if self.handle_local_service_boot_plan_review_cli_command(raw_args):
            return True

        if self.handle_control_center_runtime_entry_review_cli_command(raw_args):
            return True

        if self.handle_chat_runtime_minimal_loop_review_cli_command(raw_args):
            return True

        if self.handle_memory_runtime_write_gate_review_cli_command(raw_args):
            return True

        if self.handle_permission_runtime_grant_gate_review_cli_command(raw_args):
            return True

        if self.handle_audit_runtime_writer_activation_review_cli_command(raw_args):
            return True

        if self.handle_review_stabilization_131_140_cli_command(raw_args):
            return True

        if self.handle_local_service_runtime_foundation_cli_command(raw_args):
            return True

        if self.handle_local_service_safe_idle_boot_boundary_cli_command(raw_args):
            return True

        if self.handle_local_service_health_endpoint_foundation_cli_command(raw_args):
            return True

        if self.handle_local_service_configuration_port_registry_foundation_cli_command(raw_args):
            return True

        if self.handle_service_permission_gate_runtime_boundary_cli_command(raw_args):
            return True

        if self.handle_service_audit_link_foundation_cli_command(raw_args):
            return True

        if self.handle_service_control_command_review_foundation_cli_command(raw_args):
            return True

        if self.handle_service_recovery_restart_policy_foundation_cli_command(raw_args):
            return True

        if self.handle_service_security_localhost_binding_review_cli_command(raw_args):
            return True

        if self.handle_service_review_stabilization_141_150_cli_command(raw_args):
            return True

        if self.handle_control_center_runtime_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_read_only_status_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_memory_runtime_stabilization_cli_command(raw_args):
            return True

        if self.handle_memory_runtime_integration_review_cli_command(raw_args):
            return

        if self.handle_memory_privacy_redaction_layer_cli_command(raw_args):
            return

        if self.handle_chat_to_memory_handoff_contract_cli_command(raw_args):
            return

        if self.handle_memory_correction_deletion_boundary_cli_command(raw_args):
            return True

        if self.handle_memory_review_queue_cli_command(raw_args):
            return True

        if self.handle_memory_importance_pinning_policy_cli_command(raw_args):
            return True

        if self.handle_memory_extraction_dry_run_cli_command(raw_args):
            return True

        if self.handle_memory_write_permission_gate_cli_command(raw_args):
            return True

        if self.handle_memory_runtime_foundation_cli_command(raw_args):
            return True

        if self.handle_local_chat_runtime_stabilization_cli_command(raw_args):
            return True

        if self.handle_local_chat_integration_review_cli_command(raw_args):
            return True

        if self.handle_local_chat_history_viewer_contract_cli_command(raw_args):
            return True

        if self.handle_local_chat_safety_uncertainty_layer_cli_command(raw_args):
            return True

        if self.handle_local_chat_permission_gated_model_request_cli_command(raw_args):
            return True

        if self.handle_local_chat_model_adapter_boundary_cli_command(raw_args):
            return True

        if self.handle_local_chat_persona_response_layer_cli_command(raw_args):
            return True

        if self.handle_local_chat_message_store_cli_command(raw_args):
            return True

        if self.handle_local_chat_cli_session_alpha_cli_command(raw_args):
            return True

        if self.handle_local_chat_runtime_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_runtime_review_stabilization_151_160_cli_command(raw_args):
            return True

        if self.handle_control_center_read_only_route_map_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_action_log_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_service_monitor_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_audit_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_permission_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_plugin_panel_foundation_cli_command(raw_args):
            return True

        if self.handle_control_center_capability_viewer_foundation_cli_command(raw_args):
            return True

        parsed = self.parse(args)

        if parsed.command == "remember":
            disable_logging()
            self.remember(parsed.content)
            return True

        if parsed.command == "recall":
            disable_logging()
            self.recall(limit=parsed.limit)
            return True

        if parsed.command == "chat":
            disable_logging()
            self.chat(parsed.message)
            return True

        if parsed.command == "history":
            disable_logging()
            self.history(limit=parsed.limit)
            return True

        if parsed.command in {"journal", "journal-latest"}:
            disable_logging()
            self.journal(limit=parsed.limit)
            return True

        if parsed.command == "journal-add":
            disable_logging()
            self.journal_add(content=parsed.content)
            return True

        if parsed.command == "journal-count":
            disable_logging()
            self.journal_count()
            return True

        if parsed.command == "roles":
            disable_logging()
            self.roles()
            return True

        if parsed.command in {"context", "context-preview"}:
            disable_logging()
            self.context(message=parsed.message)
            return True

        if parsed.command == "tool-sandbox-status":
            disable_logging()
            self.tool_sandbox_status()
            return True

        if parsed.command == "tool-sandbox-policy":
            disable_logging()
            self.tool_sandbox_policy()
            return True

        if parsed.command == "tool-sandbox-check":
            disable_logging()
            self.tool_sandbox_check(command=parsed.command_text)
            return True

        if parsed.command == "tool-sandbox-dry-run":
            disable_logging()
            self.tool_sandbox_dry_run(command=parsed.command_text)
            return True

        if parsed.command == "model-router-status":
            disable_logging()
            self.model_router_status()
            return True

        if parsed.command == "model-router-routes":
            disable_logging()
            self.model_router_routes()
            return True

        if parsed.command == "model-router-select":
            disable_logging()
            self.model_router_select(target=parsed.target)
            return True

        if parsed.command == "core-loop-status":
            disable_logging()
            self.core_loop_status()
            return True

        if parsed.command == "core-loop-run":
            disable_logging()
            self.core_loop_run(message=parsed.message)
            return True

        if parsed.command == "core-loop-trace":
            disable_logging()
            self.core_loop_trace(message=parsed.message)
            return True

        if parsed.command == "avatar-runtime-alpha-status":
            disable_logging()
            self.avatar_runtime_alpha_status()
            return True

        if parsed.command == "avatar-expression-plan":
            disable_logging()
            self.avatar_expression_plan(expression=parsed.expression)
            return True

        if parsed.command == "avatar-gesture-plan":
            disable_logging()
            self.avatar_gesture_plan(gesture=parsed.gesture)
            return True

        if parsed.command == "avatar-runtime-context":
            disable_logging()
            self.avatar_runtime_context()
            return True

        if parsed.command == "avatar-status":
            disable_logging()
            self.avatar_status()
            return True

        if parsed.command == "avatar-providers":
            disable_logging()
            self.avatar_providers()
            return True

        if parsed.command == "avatar-state":
            disable_logging()
            self.avatar_state()
            return True

        if parsed.command == "avatar-expression":
            disable_logging()
            self.avatar_expression(expression=parsed.expression)
            return True

        if parsed.command == "avatar-gesture":
            disable_logging()
            self.avatar_gesture(gesture=parsed.gesture)
            return True

        if parsed.command == "desktop-alpha-status":
            disable_logging()
            self.desktop_alpha_status()
            return True

        if parsed.command == "desktop-action-plan":
            disable_logging()
            self.desktop_action_plan(
                action_type=parsed.action_type,
                target=" ".join(parsed.target),
            )
            return True

        if parsed.command == "desktop-open-app-plan":
            disable_logging()
            self.desktop_open_app_plan(app_name=" ".join(parsed.app_name))
            return True

        if parsed.command == "desktop-open-browser-plan":
            disable_logging()
            self.desktop_open_browser_plan(url=" ".join(parsed.url))
            return True

        if parsed.command == "desktop-open-file-plan":
            disable_logging()
            self.desktop_open_file_plan(file_path=" ".join(parsed.file_path))
            return True

        if parsed.command == "desktop-workspace-context":
            disable_logging()
            self.desktop_workspace_context()
            return True

        if parsed.command == "desktop-status":
            disable_logging()
            self.desktop_status()
            return True

        if parsed.command == "desktop-capabilities":
            disable_logging()
            self.desktop_capabilities()
            return True

        if parsed.command == "desktop-action":
            disable_logging()
            self.desktop_action(action=parsed.action)
            return True

        if parsed.command in {"system-status", "status-full"}:
            disable_logging()
            self.system_status()
            return True

        if parsed.command == "vision-runtime-alpha-status":
            disable_logging()
            self.vision_runtime_alpha_status()
            return True

        if parsed.command == "vision-screen-plan":
            disable_logging()
            self.vision_screen_plan()
            return True

        if parsed.command == "vision-camera-plan":
            disable_logging()
            self.vision_camera_plan()
            return True

        if parsed.command == "vision-runtime-context":
            disable_logging()
            self.vision_runtime_context()
            return True

        if parsed.command == "vision-runtime-status":
            disable_logging()
            self.vision_runtime_status()
            return True

        if parsed.command == "vision-runtime-plan":
            disable_logging()
            self.vision_runtime_plan()
            return True

        if parsed.command == "vision-runtime-check":
            disable_logging()
            self.vision_runtime_check()
            return True

        if parsed.command == "vision-status":
            disable_logging()
            self.vision_status()
            return True

        if parsed.command == "vision-providers":
            disable_logging()
            self.vision_providers()
            return True

        if parsed.command == "safe-file-operation-status":
            disable_logging()
            self.safe_file_operation_status()
            return True

        if parsed.command == "safe-file-read-plan":
            disable_logging()
            self.safe_file_read_plan(" ".join(parsed.target))
            return True

        if parsed.command == "safe-file-write-plan":
            disable_logging()
            self.safe_file_write_plan(" ".join(parsed.target))
            return True

        if parsed.command == "safe-file-edit-plan":
            disable_logging()
            self.safe_file_edit_plan(" ".join(parsed.target))
            return True

        if parsed.command == "safe-file-move-copy-delete-risk-review":
            disable_logging()
            self.safe_file_move_copy_delete_risk_review(" ".join(parsed.target))
            return True

        if parsed.command == "safe-file-operation-checklist":
            disable_logging()
            self.safe_file_operation_checklist(" ".join(parsed.target))
            return True

        if parsed.command == "safe-file-operation-context":
            disable_logging()
            self.safe_file_operation_context()
            return True

        if parsed.command == "local-task-planner-status":
            disable_logging()
            self.local_task_planner_status()
            return True

        if parsed.command == "local-task-intent-plan":
            disable_logging()
            self.local_task_intent_plan(" ".join(parsed.target))
            return True

        if parsed.command == "local-task-breakdown-plan":
            disable_logging()
            self.local_task_breakdown_plan(" ".join(parsed.target))
            return True

        if parsed.command == "local-task-risk-review":
            disable_logging()
            self.local_task_risk_review(" ".join(parsed.target))
            return True

        if parsed.command == "local-task-execution-checklist":
            disable_logging()
            self.local_task_execution_checklist(" ".join(parsed.target))
            return True

        if parsed.command == "local-task-context":
            disable_logging()
            self.local_task_context()
            return True

        if parsed.command == "creative-assistant-status":
            disable_logging()
            self.creative_assistant_status()
            return True

        if parsed.command == "creative-brief-plan":
            disable_logging()
            self.creative_brief_plan(" ".join(parsed.target))
            return True

        if parsed.command == "creative-character-concept-plan":
            disable_logging()
            self.creative_character_concept_plan(" ".join(parsed.target))
            return True

        if parsed.command == "creative-visual-asset-plan":
            disable_logging()
            self.creative_visual_asset_plan(" ".join(parsed.target))
            return True

        if parsed.command == "creative-content-idea-plan":
            disable_logging()
            self.creative_content_idea_plan(" ".join(parsed.target))
            return True

        if parsed.command == "creative-review-plan":
            disable_logging()
            self.creative_review_plan(" ".join(parsed.target))
            return True

        if parsed.command == "creative-context":
            disable_logging()
            self.creative_context()
            return True

        if parsed.command == "project-intent-status":
            disable_logging()
            self.project_intent_status()
            return True

        if parsed.command == "project-intent-summary":
            disable_logging()
            self.project_intent_summary(" ".join(parsed.topic))
            return True

        if parsed.command == "project-goal-plan":
            disable_logging()
            self.project_goal_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "sprint-intent-plan":
            disable_logging()
            self.sprint_intent_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "project-next-action-candidates":
            disable_logging()
            self.project_next_action_candidates(" ".join(parsed.topic))
            return True

        if parsed.command == "project-intent-context":
            disable_logging()
            self.project_intent_context()
            return True

        if parsed.command == "workspace-memory-link-status":
            disable_logging()
            self.workspace_memory_link_status()
            return True

        if parsed.command == "workspace-memory-summary":
            disable_logging()
            self.workspace_memory_summary()
            return True

        if parsed.command == "workspace-memory-candidates":
            disable_logging()
            self.workspace_memory_candidates(" ".join(parsed.target))
            return True

        if parsed.command == "workspace-file-memory-candidates":
            disable_logging()
            self.workspace_file_memory_candidates(" ".join(parsed.target))
            return True

        if parsed.command == "workspace-milestone-memory-candidates":
            disable_logging()
            self.workspace_milestone_memory_candidates(" ".join(parsed.target))
            return True

        if parsed.command == "workspace-memory-link-context":
            disable_logging()
            self.workspace_memory_link_context()
            return True

        if parsed.command == "streaming-safety-status":
            disable_logging()
            self.streaming_safety_status()
            return True

        if parsed.command == "streaming-context-plan":
            disable_logging()
            self.streaming_context_plan(" ".join(parsed.target))
            return True

        if parsed.command == "streaming-chat-safety-plan":
            disable_logging()
            self.streaming_chat_safety_plan(" ".join(parsed.target))
            return True

        if parsed.command == "streaming-content-boundary-plan":
            disable_logging()
            self.streaming_content_boundary_plan(" ".join(parsed.target))
            return True

        if parsed.command == "streaming-privacy-plan":
            disable_logging()
            self.streaming_privacy_plan(" ".join(parsed.target))
            return True

        if parsed.command == "streaming-moderation-plan":
            disable_logging()
            self.streaming_moderation_plan(" ".join(parsed.target))
            return True

        if parsed.command == "streaming-safety-context":
            disable_logging()
            self.streaming_safety_context()
            return True

        if parsed.command == "game-companion-status":
            disable_logging()
            self.game_companion_status()
            return True

        if parsed.command == "game-session-plan":
            disable_logging()
            self.game_session_plan(" ".join(parsed.target))
            return True

        if parsed.command == "game-strategy-plan":
            disable_logging()
            self.game_strategy_plan(" ".join(parsed.target))
            return True

        if parsed.command == "game-streaming-plan":
            disable_logging()
            self.game_streaming_plan(" ".join(parsed.target))
            return True

        if parsed.command == "game-coaching-plan":
            disable_logging()
            self.game_coaching_plan(" ".join(parsed.target))
            return True

        if parsed.command == "game-context":
            disable_logging()
            self.game_context()
            return True

        if parsed.command == "expression-language-status":
            disable_logging()
            self.expression_language_status()
            return True

        if parsed.command == "expression-state":
            disable_logging()
            self.expression_state()
            return True

        if parsed.command == "expression-plan":
            disable_logging()
            self.expression_plan(" ".join(parsed.text))
            return True

        if parsed.command == "expression-voice-hint":
            disable_logging()
            self.expression_voice_hint(" ".join(parsed.target))
            return True

        if parsed.command == "expression-avatar-hint":
            disable_logging()
            self.expression_avatar_hint(" ".join(parsed.target))
            return True

        if parsed.command == "expression-gesture-hint":
            disable_logging()
            self.expression_gesture_hint(" ".join(parsed.target))
            return True

        if parsed.command == "expression-context":
            disable_logging()
            self.expression_context()
            return True

        if parsed.command == "media-understanding-status":
            disable_logging()
            self.media_understanding_status()
            return True

        if parsed.command == "media-asset-summary":
            disable_logging()
            self.media_asset_summary()
            return True

        if parsed.command == "media-image-plan":
            disable_logging()
            self.media_image_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "media-texture-reference-plan":
            disable_logging()
            self.media_texture_reference_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "media-thumbnail-review-plan":
            disable_logging()
            self.media_thumbnail_review_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "media-video-plan":
            disable_logging()
            self.media_video_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "media-context":
            disable_logging()
            self.media_context()
            return True

        if parsed.command == "blender-bridge-status":
            disable_logging()
            self.blender_bridge_status()
            return True

        if parsed.command == "blender-scene-plan":
            disable_logging()
            self.blender_scene_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-asset-plan":
            disable_logging()
            self.blender_asset_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-texture-plan":
            disable_logging()
            self.blender_texture_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-rigging-plan":
            disable_logging()
            self.blender_rigging_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-animation-plan":
            disable_logging()
            self.blender_animation_plan(" ".join(parsed.goal))
            return True

        if parsed.command == "blender-context":
            disable_logging()
            self.blender_context()
            return True

        if parsed.command == "workspace-status":
            disable_logging()
            self.workspace_awareness_status()
            return True

        if parsed.command == "workspace-awareness-status":
            disable_logging()
            self.workspace_awareness_status()
            return True

        if parsed.command == "workspace-map":
            disable_logging()
            self.workspace_map()
            return True

        if parsed.command == "workspace-context":
            disable_logging()
            self.workspace_context()
            return True

        if parsed.command == "workspace-current-state":
            disable_logging()
            self.workspace_current_state()
            return True

        if parsed.command == "workspace-important-files":
            disable_logging()
            self.workspace_important_files()
            return True

        if parsed.command == "partner-alpha-status":
            disable_logging()
            self.partner_alpha_status()
            return True

        if parsed.command == "partner-context":
            disable_logging()
            self.partner_context()
            return True

        if parsed.command == "partner-readiness":
            disable_logging()
            self.partner_readiness()
            return True

        if parsed.command == "partner-next-step":
            disable_logging()
            self.partner_next_step()
            return True

        if parsed.command in {"awakening-status", "awaken"}:
            disable_logging()
            self.awakening_status()
            return True

        if parsed.command == "voice-runtime-alpha-status":
            disable_logging()
            self.voice_runtime_alpha_status()
            return True

        if parsed.command == "voice-speak-plan":
            disable_logging()
            self.voice_speak_plan(text=" ".join(parsed.text))
            return True

        if parsed.command == "voice-speak-test":
            disable_logging()
            self.voice_speak_test(text=" ".join(parsed.text))
            return True

        if parsed.command == "voice-runtime-context":
            disable_logging()
            self.voice_runtime_context()
            return True

        if parsed.command == "voice-runtime-status":
            disable_logging()
            self.voice_runtime_status()
            return True

        if parsed.command == "voice-runtime-plan":
            disable_logging()
            self.voice_runtime_plan()
            return True

        if parsed.command == "voice-runtime-check":
            disable_logging()
            self.voice_runtime_check()
            return True

        if parsed.command == "voice-status":
            disable_logging()
            self.voice_status()
            return True

        if parsed.command == "voice-providers":
            disable_logging()
            self.voice_providers()
            return True

        if parsed.command == "project-code-status":
            disable_logging()
            self.project_code_status()
            return True

        if parsed.command == "project-code-map":
            disable_logging()
            self.project_code_map(limit=parsed.limit)
            return True

        if parsed.command == "project-code-inspect":
            disable_logging()
            self.project_code_inspect(relative_path=parsed.path)
            return True

        if parsed.command == "project-code-plan":
            disable_logging()
            self.project_code_plan(request=parsed.request)
            return True

        if parsed.command == "project-code-safety":
            disable_logging()
            self.project_code_safety(command=parsed.command_text)
            return True

        if parsed.command == "project-map":
            disable_logging()
            self.project_map(depth=parsed.depth, limit=parsed.limit)
            return True

        if parsed.command == "project-inspect":
            disable_logging()
            self.project_inspect(relative_path=parsed.relative_path)
            return True

        if parsed.command == "project-find":
            disable_logging()
            self.project_find(keyword=parsed.keyword, limit=parsed.limit)
            return True

        if parsed.command == "project-summary":
            disable_logging()
            self.project_summary()
            return True

        if parsed.command == "project-files":
            disable_logging()
            self.project_files(limit=parsed.limit)
            return True

        if parsed.command == "project-read":
            disable_logging()
            self.project_read(relative_path=parsed.relative_path)
            return True

        if parsed.command in {"action-request", "action-request-check"}:
            disable_logging()
            self.action_request(action=parsed.action)
            return True

        if parsed.command == "plugin-actions":
            disable_logging()
            self.plugin_actions()
            return True

        if parsed.command == "plugin-action":
            disable_logging()
            self.plugin_action_detail(name=parsed.name)
            return True

        if parsed.command == "plugin-action-check":
            disable_logging()
            self.plugin_action_check(name=parsed.name)
            return True

        if parsed.command == "skills":
            disable_logging()
            self.skills()
            return True

        if parsed.command == "skill":
            disable_logging()
            self.skill_detail(name=parsed.name)
            return True

        if parsed.command == "skill-check":
            disable_logging()
            self.skill_check(name=parsed.name)
            return True

        if parsed.command == "permissions":
            disable_logging()
            self.permissions()
            return True

        if parsed.command in {"permission-check", "perm-check"}:
            disable_logging()
            self.permission_check(action=parsed.action)
            return True

        if parsed.command in {"provider", "reason"}:
            disable_logging()
            self.provider()
            return True

        if parsed.command in {"provider-check", "reason-check"}:
            disable_logging()
            self.provider_check()
            return True

        if parsed.command == "daily-briefing-status":
            disable_logging()
            self.daily_briefing_status()
            return True

        if parsed.command == "daily-briefing":
            disable_logging()
            self.daily_briefing(limit=parsed.limit)
            return True

        if parsed.command == "daily-briefing-compact":
            disable_logging()
            self.daily_briefing_compact(limit=parsed.limit)
            return True

        if parsed.command == "daily-briefing-context":
            disable_logging()
            self.daily_briefing_context(limit=parsed.limit)
            return True

        if parsed.command == "memory-reflection-status":
            disable_logging()
            self.memory_reflection_status()
            return True

        if parsed.command == "memory-reflect":
            disable_logging()
            self.memory_reflect(limit=parsed.limit)
            return True

        if parsed.command == "memory-insights":
            disable_logging()
            self.memory_insights(limit=parsed.limit)
            return True

        if parsed.command == "memory-reflection-context":
            disable_logging()
            self.memory_reflection_context(limit=parsed.limit)
            return True

        if parsed.command in {"memory-delete", "mem-delete"}:
            disable_logging()
            self.memory_delete(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-pin", "mem-pin"}:
            disable_logging()
            self.memory_pin(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-unpin", "mem-unpin"}:
            disable_logging()
            self.memory_unpin(memory_id=parsed.memory_id)
            return True

        if parsed.command in {"memory-importance", "mem-importance"}:
            disable_logging()
            self.memory_importance(
                memory_id=parsed.memory_id,
                importance=parsed.importance,
            )
            return True

        if parsed.command in {"memory-pinned", "mem-pinned"}:
            disable_logging()
            self.memory_pinned()
            return True

        if parsed.command in {"memory-count", "mem-count"}:
            disable_logging()
            self.memory_count()
            return True

        if parsed.command in {"memory-list", "mem-list"}:
            disable_logging()
            self.memory_list(limit=parsed.limit)
            return True

        if parsed.command in {"memory-search", "mem-search"}:
            disable_logging()
            self.memory_search(query=parsed.query, limit=parsed.limit)
            return True

        if parsed.command == "shell":
            disable_logging()
            self.shell()
            return True

        return False


    def project_code_status(self) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        status = manager.status()
        route = status["coding_route"]

        print("AURA Project Coding Assistant v2")
        print("================================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Analysis Ready         : {status['analysis_ready']}")
        print(f"AST Inspection Ready   : {status['ast_inspection_ready']}")
        print(f"Patch Planning Ready   : {status['patch_planning_ready']}")
        print(f"File Write Ready       : {status['file_write_ready']}")
        print(f"Command Execution Ready: {status['command_execution_ready']}")
        print(f"Sandbox Check Ready    : {status['sandbox_check_ready']}")
        print(f"Real Tool Execution    : {status['real_tool_execution']}")
        print(f"Python Files           : {status['python_files']}")
        print()
        print("Coding Route")
        print("------------")
        print(f"Route   : {route['name']}")
        print(f"Provider: {route['provider']}")
        print(f"Model   : {route['model']}")
        print(f"Status  : {route['status']}")
        print()
        print(f"Note: {status['note']}")

    def project_code_map(self, limit: int = 30) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        result = manager.code_map(limit=limit)
        totals = result["totals"]

        print("AURA Project Code Map")
        print("=====================")
        print(f"Files    : {totals['files']}")
        print(f"Classes  : {totals['classes']}")
        print(f"Functions: {totals['functions']}")
        print(f"Methods  : {totals['methods']}")
        print()

        for item in result["files"]:
            print(f"- {item['path']}")
            print(f"  Parse OK : {item.get('parse_ok', False)}")
            print(f"  Lines    : {item.get('line_count', 0)}")
            print(f"  Classes  : {item.get('class_count', 0)}")
            print(f"  Functions: {item.get('function_count', 0)}")
            print(f"  Methods  : {item.get('method_count', 0)}")

            classes = item.get("classes", [])
            functions = item.get("functions", [])
            methods = item.get("methods", [])

            if classes:
                print(f"  Class List   : {', '.join(classes[:8])}")
            if functions:
                print(f"  Function List: {', '.join(functions[:8])}")
            if methods:
                print(f"  Method List  : {', '.join(methods[:8])}")

            if item.get("parse_error"):
                print(f"  Error: {item['parse_error']}")

            print()

        print(f"Note: {result['note']}")

    def project_code_inspect(self, relative_path: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        summary = manager.summarize_file(relative_path)

        print("AURA Project Code Inspect")
        print("=========================")
        print(f"Path     : {summary['path']}")
        print(f"Language : {summary['language']}")
        print(f"Size     : {summary['size_bytes']} bytes")
        print(f"Lines    : {summary['line_count']}")
        print(f"Parse OK : {summary['parse_ok']}")
        print(f"Imports  : {summary['import_count']}")
        print(f"Classes  : {summary['class_count']}")
        print(f"Functions: {summary['function_count']}")
        print(f"Methods  : {summary['method_count']}")

        if summary["parse_error"]:
            print(f"Parse Error: {summary['parse_error']}")

        if summary["imports"]:
            print()
            print("Imports")
            print("-------")
            for item in summary["imports"][:40]:
                print(f"- {item}")

        if summary["classes"]:
            print()
            print("Classes")
            print("-------")
            for item in summary["classes"]:
                print(f"- {item}")

        if summary["functions"]:
            print()
            print("Functions")
            print("---------")
            for item in summary["functions"][:60]:
                print(f"- {item}")

        if summary["methods"]:
            print()
            print("Methods")
            print("-------")
            for item in summary["methods"][:80]:
                print(f"- {item}")

        if summary["safety_notes"]:
            print()
            print("Safety Notes")
            print("------------")
            for note in summary["safety_notes"]:
                print(f"- {note}")

    def project_code_plan(self, request: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        plan = manager.patch_plan(request)
        route = plan["coding_route"]

        print("AURA Project Code Patch Plan")
        print("============================")
        print(f"Request                    : {plan['request']}")
        print(f"Mode                       : {plan['mode']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print(f"Command Execution Performed: {plan['command_execution_performed']}")
        print()

        print("Coding Route")
        print("------------")
        print(f"Route   : {route['name']}")
        print(f"Provider: {route['provider']}")
        print(f"Model   : {route['model']}")
        print(f"Status  : {route['status']}")
        print()

        print("Related Files")
        print("-------------")
        for file in plan["related_files"]:
            print(f"- {file}")

        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")

        print()
        print("Sandbox Checks")
        print("--------------")
        for check in plan["sandbox_checks"]:
            print(f"- {check['command']} -> state={check['state']} allowed={check['allowed']} executed={check['executed']}")

        print()
        print("Safety")
        print("------")
        safety = plan["safety"]
        print(f"Writes Without Confirmation: {safety['writes_allowed_without_confirmation']}")
        print(f"Real Tool Execution        : {safety['real_tool_execution']}")
        print(f"Dangerous Commands Blocked : {safety['dangerous_commands_blocked']}")
        print(f"Note                       : {safety['note']}")

    def project_code_safety(self, command: str) -> None:
        manager = ProjectCodingManager(project_root=self.project_root)
        result = manager.command_safety(command)
        check = result["check"]
        dry_run = result["dry_run"]

        print("AURA Project Code Command Safety")
        print("================================")
        print(f"Command      : {result['command']}")
        print(f"State        : {check['state']}")
        print(f"Allowed      : {check['allowed']}")
        print(f"Dry Run Ready: {dry_run['dry_run_ready']}")
        print(f"Would Execute: {dry_run['would_execute']}")
        print(f"Executed     : {dry_run['executed']}")
        print(f"Reason       : {check['reason']}")

        if check["blocked_patterns_found"]:
            print("Blocked Patterns Found:")
            for pattern in check["blocked_patterns_found"]:
                print(f"- {pattern}")

        print()
        print(f"Note: {result['project_coding_note']}")


    def memory_reflection_status(self) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Memory Reflection System")
        print("=============================")
        print(f"Name                    : {status['name']}")
        print(f"Version                 : {status['version']}")
        print(f"Status                  : {status['status']}")
        print(f"Reflection Ready        : {status['reflection_ready']}")
        print(f"Memory Read Ready       : {status['memory_read_ready']}")
        print(f"Journal Read Ready      : {status['journal_read_ready']}")
        print(f"Insight Generation Ready: {status['insight_generation_ready']}")
        print(f"Automatic Memory Write  : {status['automatic_memory_write']}")
        print(f"Automatic Memory Delete : {status['automatic_memory_delete']}")
        print(f"Automatic Memory Merge  : {status['automatic_memory_merge']}")
        print(f"Memory Count            : {status['memory_count']}")
        print(f"Journal Count           : {status['journal_count']}")
        print(f"Pinned Memory Count     : {status['pinned_memory_count']}")
        print(f"Important Memory Count  : {status['important_memory_count']}")
        print(f"Milestone Count         : {status['milestone_count']}")
        print()
        print(f"Note: {status['note']}")

    def memory_reflect(self, limit: int = 8) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        reflection = manager.reflect(limit=limit)

        print("AURA Memory Reflection")
        print("======================")
        print(f"Title          : {reflection['title']}")
        print(f"Status         : {reflection['status']}")
        print(f"Memory Count   : {reflection['memory_count']}")
        print(f"Journal Count  : {reflection['journal_count']}")
        print(f"Milestone Count: {reflection['milestone_count']}")
        print(f"Limit          : {reflection['metadata']['limit']}")
        print()

        print("Recent Milestones")
        print("-----------------")
        for item in reflection["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in reflection["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in reflection["project_insights"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in reflection["safety_notes"]:
            print(f"- {item}")

    def memory_insights(self, limit: int = 8) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        result = manager.insights(limit=limit)

        print("AURA Memory Insights")
        print("====================")
        print(f"Status         : {result['status']}")
        print(f"Insight Count  : {result['insight_count']}")
        print(f"Write Performed: {result['write_performed']}")
        print(f"Delete Performed: {result['delete_performed']}")
        print(f"Merge Performed : {result['merge_performed']}")
        print()

        print("Insights")
        print("--------")
        for item in result["insights"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in result["safety_notes"]:
            print(f"- {item}")

    def memory_reflection_context(self, limit: int = 5) -> None:
        manager = MemoryReflectionManager(project_root=self.project_root)
        context = manager.reflection_context(limit=limit)

        print("AURA Memory Reflection Context")
        print("==============================")
        print(f"Status          : {context['status']}")
        print(f"Context Ready   : {context['context_ready']}")
        print(f"Memory Count    : {context['memory_count']}")
        print(f"Journal Count   : {context['journal_count']}")
        print(f"Milestones      : {len(context['milestones'])}")
        print(f"Memory Highlights: {len(context['memory_highlights'])}")
        print(f"Write Performed : {context['write_performed']}")
        print()
        print("Milestones")
        print("----------")
        for milestone in context["milestones"]:
            print(f"- {milestone['title']}: {milestone['content']}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for memory in context["memory_highlights"]:
            print(f"- {memory['content']}")

        print()
        print(f"Note: {context['note']}")


    def daily_briefing_status(self) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Daily Project Briefing Status")
        print("==================================")
        print(f"Name                   : {status['name']}")
        print(f"Version                : {status['version']}")
        print(f"Status                 : {status['status']}")
        print(f"Briefing Ready         : {status['briefing_ready']}")
        print(f"Compact Ready          : {status['compact_ready']}")
        print(f"Context Ready          : {status['context_ready']}")
        print(f"Journal Read Ready     : {status['journal_read_ready']}")
        print(f"Reflection Read Ready  : {status['reflection_read_ready']}")
        print(f"System Summary Ready   : {status['system_summary_ready']}")
        print(f"Automatic File Write   : {status['automatic_file_write']}")
        print(f"Automatic Memory Write : {status['automatic_memory_write']}")
        print(f"Automatic Journal Write: {status['automatic_journal_write']}")
        print(f"Command Execution      : {status['command_execution']}")
        print(f"AURA Version           : {status['aura_version']}")
        print(f"Memory Count           : {status['memory_count']}")
        print(f"Journal Count          : {status['journal_count']}")
        print(f"Milestone Count        : {status['milestone_count']}")
        print(f"Latest Milestone       : {status['latest_milestone']}")
        print(f"Briefing Sections      : {status['briefing_sections']}")
        print()
        print(f"Note: {status['note']}")

    def daily_briefing(self, limit: int = 6) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        briefing = manager.build(limit=limit)

        print("AURA Daily Project Briefing")
        print("===========================")
        print(f"Title   : {briefing['title']}")
        print(f"Status  : {briefing['status']}")
        print(f"Version : {briefing['version']}")
        print(f"Limit   : {briefing['metadata']['limit']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
        print()

        latest = briefing["latest_milestone"]
        print("Latest Milestone")
        print("----------------")
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Recent Milestones")
        print("-----------------")
        for item in briefing["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in briefing["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in briefing["project_insights"]:
            print(f"- {item}")

        print()
        print("Safety State")
        print("------------")
        for key, value in briefing["safety_state"].items():
            print(f"{key}: {value}")

        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in briefing["recommended_next_steps"]:
            print(f"- {item}")

        print()
        print("Safety Notes")
        print("------------")
        for item in briefing["safety_notes"]:
            print(f"- {item}")

    def daily_briefing_compact(self, limit: int = 4) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        briefing = manager.compact(limit=limit)

        print("AURA Daily Project Briefing Compact")
        print("===================================")
        print(f"Title                    : {briefing['title']}")
        print(f"Status                   : {briefing['status']}")
        print(f"Version                  : {briefing['version']}")
        print(f"Write Performed          : {briefing['write_performed']}")
        print(f"Command Execution        : {briefing['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
        print()

        print("Latest Milestone")
        print("----------------")
        latest = briefing["latest_milestone"]
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Top Insights")
        print("------------")
        for item in briefing["top_insights"]:
            print(f"- {item}")

        print()
        print("Next Steps")
        print("----------")
        for item in briefing["next_steps"]:
            print(f"- {item}")

        print()
        print("Safety State")
        print("------------")
        for key, value in briefing["safety_state"].items():
            print(f"{key}: {value}")

    def daily_briefing_context(self, limit: int = 5) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        context = manager.context(limit=limit)

        print("AURA Daily Project Briefing Context")
        print("===================================")
        print(f"Status             : {context['status']}")
        print(f"Context Ready      : {context['context_ready']}")
        print(f"Write Performed    : {context['write_performed']}")
        print(f"Command Execution  : {context['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(context["project_summary"])
        print()

        latest = context["latest_milestone"]
        print("Latest Milestone")
        print("----------------")
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

        print()
        print("Recent Milestones")
        print("-----------------")
        for item in context["recent_milestones"]:
            print(f"- {item}")

        print()
        print("Memory Highlights")
        print("-----------------")
        for item in context["memory_highlights"]:
            print(f"- {item}")

        print()
        print("Project Insights")
        print("----------------")
        for item in context["project_insights"]:
            print(f"- {item}")

        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in context["recommended_next_steps"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def voice_runtime_alpha_status(self) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Voice Runtime Alpha Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Speak Plan Ready             : {status['speak_plan_ready']}")
        print(f"Speak Test Ready             : {status['speak_test_ready']}")
        print(f"Voice Context Ready          : {status['voice_context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"TTS Backend Found            : {status['tts_backend_found']}")
        print(f"TTS Backend                  : {status['tts_backend'] or '-'}")
        print(f"TTS Backend Path             : {status['tts_backend_path'] or '-'}")
        print(f"STT Runtime Ready            : {status['stt_runtime_ready']}")
        print(f"TTS Runtime Ready            : {status['tts_runtime_ready']}")
        print(f"Microphone Access            : {status['microphone_access']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"Recording Enabled            : {status['recording_enabled']}")
        print(f"Playback Enabled             : {status['playback_enabled']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Audio File Write             : {status['audio_file_write']}")
        print(f"Requires Speaker Confirmation: {status['requires_speaker_confirmation']}")
        print(f"Requires Mic Confirmation    : {status['requires_microphone_confirmation']}")
        print(f"Python Packages              : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                  : {status['executables_found']}/{status['executables_total']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def voice_speak_plan(self, text: str) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.speak_plan(text=text)

        print("AURA Voice Speak Plan")
        print("=====================")
        print(f"Status                    : {plan['status']}")
        print(f"Text                      : {plan['text']}")
        print(f"Text Length               : {plan['text_length']}")
        print(f"Command Available         : {plan['command_available']}")
        print(f"TTS Backend               : {plan['tts_backend']['name'] or '-'}")
        print(f"TTS Backend Found         : {plan['tts_backend']['found']}")
        print(f"Proposed Command          : {plan['proposed_command'] or '-'}")
        print(f"Command Reason            : {plan['command_reason']}")
        print(f"Speaker Output            : {plan['speaker_output']}")
        print(f"Microphone Access         : {plan['microphone_access']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Playback Performed        : {plan['playback_performed']}")
        print(f"File Write Performed      : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Speaker Permission")
        print("------------------")
        permission = plan["speaker_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def voice_speak_test(self, text: str) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        result = manager.speak_test(text=text)
        plan = result["speak_plan"]

        print("AURA Voice Speak Test")
        print("=====================")
        print(f"Status               : {result['status']}")
        print(f"Test Ready           : {result['test_ready']}")
        print(f"Would Speak          : {result['would_speak']}")
        print(f"Speaker Output       : {result['speaker_output']}")
        print(f"Microphone Access    : {result['microphone_access']}")
        print(f"Command Execution    : {result['command_execution_performed']}")
        print(f"Playback Performed   : {result['playback_performed']}")
        print(f"File Write Performed : {result['file_write_performed']}")
        print()
        print("Prepared Speak Plan")
        print("-------------------")
        print(f"Text              : {plan['text']}")
        print(f"Command Available : {plan['command_available']}")
        print(f"TTS Backend       : {plan['tts_backend']['name'] or '-'}")
        print(f"Proposed Command  : {plan['proposed_command'] or '-'}")
        print(f"Command Reason    : {plan['command_reason']}")
        print()
        print(f"Note: {result['note']}")

    def voice_runtime_context(self) -> None:
        manager = VoiceRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]

        print("AURA Voice Runtime Alpha Context")
        print("================================")
        print(f"Status                      : {context['status']}")
        print(f"Context Ready               : {context['context_ready']}")
        print(f"Write Performed             : {context['write_performed']}")
        print(f"Command Execution Performed : {context['command_execution_performed']}")
        print(f"Microphone Access Performed : {context['microphone_access_performed']}")
        print(f"Speaker Output Performed    : {context['speaker_output_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready       : {alpha['alpha_ready']}")
        print(f"Speak Plan Ready  : {alpha['speak_plan_ready']}")
        print(f"Speak Test Ready  : {alpha['speak_test_ready']}")
        print(f"TTS Backend Found : {alpha['tts_backend_found']}")
        print(f"TTS Backend       : {alpha['tts_backend'] or '-'}")
        print(f"Microphone Access : {alpha['microphone_access']}")
        print(f"Speaker Output    : {alpha['speaker_output']}")
        print(f"Command Execution : {alpha['command_execution']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def vision_runtime_alpha_status(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Vision Runtime Alpha Status")
        print("================================")
        print(f"Name                        : {status['name']}")
        print(f"Version                     : {status['version']}")
        print(f"Status                      : {status['status']}")
        print(f"Alpha Ready                 : {status['alpha_ready']}")
        print(f"Screen Plan Ready           : {status['screen_plan_ready']}")
        print(f"Camera Plan Ready           : {status['camera_plan_ready']}")
        print(f"Vision Context Ready        : {status['vision_context_ready']}")
        print(f"Dependency Check Ready      : {status['dependency_check_ready']}")
        print(f"Screen Backend Found        : {status['screen_backend_found']}")
        print(f"Screen Backend              : {status['screen_backend'] or '-'}")
        print(f"Screen Backend Path         : {status['screen_backend_path'] or '-'}")
        print(f"Camera Backend Found        : {status['camera_backend_found']}")
        print(f"Camera Backend              : {status['camera_backend'] or '-'}")
        print(f"Camera Backend Path         : {status['camera_backend_path'] or '-'}")
        print(f"Screen Capture Ready        : {status['screen_capture_ready']}")
        print(f"Camera Capture Ready        : {status['camera_capture_ready']}")
        print(f"Vision Model Ready          : {status['vision_model_ready']}")
        print(f"Screen Access               : {status['screen_access']}")
        print(f"Camera Access               : {status['camera_access']}")
        print(f"Screenshot Capture          : {status['screenshot_capture']}")
        print(f"Camera Frame Capture        : {status['camera_frame_capture']}")
        print(f"Command Execution           : {status['command_execution']}")
        print(f"Image File Write            : {status['image_file_write']}")
        print(f"Requires Screen Confirmation: {status['requires_screen_confirmation']}")
        print(f"Requires Camera Confirmation: {status['requires_camera_confirmation']}")
        print(f"Python Packages             : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                 : {status['executables_found']}/{status['executables_total']}")
        print(f"Sections                    : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def vision_screen_plan(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.screen_plan()

        print("AURA Vision Screen Plan")
        print("=======================")
        print(f"Status                     : {plan['status']}")
        print(f"Command Available          : {plan['command_available']}")
        print(f"Screen Backend             : {plan['screen_backend']['name'] or '-'}")
        print(f"Screen Backend Found       : {plan['screen_backend']['found']}")
        print(f"Proposed Command           : {plan['proposed_command'] or '-'}")
        print(f"Command Reason             : {plan['command_reason']}")
        print(f"Screen Access              : {plan['screen_access']}")
        print(f"Camera Access              : {plan['camera_access']}")
        print(f"Screenshot Capture         : {plan['screenshot_capture_performed']}")
        print(f"Command Execution          : {plan['command_execution_performed']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Screen Permission")
        print("-----------------")
        permission = plan["screen_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def vision_camera_plan(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.camera_plan()

        print("AURA Vision Camera Plan")
        print("=======================")
        print(f"Status                     : {plan['status']}")
        print(f"Command Available          : {plan['command_available']}")
        print(f"Camera Backend             : {plan['camera_backend']['name'] or '-'}")
        print(f"Camera Backend Found       : {plan['camera_backend']['found']}")
        print(f"Proposed Command           : {plan['proposed_command'] or '-'}")
        print(f"Command Reason             : {plan['command_reason']}")
        print(f"Screen Access              : {plan['screen_access']}")
        print(f"Camera Access              : {plan['camera_access']}")
        print(f"Camera Frame Capture       : {plan['camera_frame_capture_performed']}")
        print(f"Command Execution          : {plan['command_execution_performed']}")
        print(f"File Write Performed       : {plan['file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Camera Permission")
        print("-----------------")
        permission = plan["camera_permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def vision_runtime_context(self) -> None:
        manager = VisionRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]

        print("AURA Vision Runtime Alpha Context")
        print("=================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"Screen Access Performed      : {context['screen_access_performed']}")
        print(f"Camera Access Performed      : {context['camera_access_performed']}")
        print(f"Screenshot Capture Performed : {context['screenshot_capture_performed']}")
        print(f"Camera Frame Capture         : {context['camera_frame_capture_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready          : {alpha['alpha_ready']}")
        print(f"Screen Plan Ready    : {alpha['screen_plan_ready']}")
        print(f"Camera Plan Ready    : {alpha['camera_plan_ready']}")
        print(f"Screen Backend Found : {alpha['screen_backend_found']}")
        print(f"Screen Backend       : {alpha['screen_backend'] or '-'}")
        print(f"Camera Backend Found : {alpha['camera_backend_found']}")
        print(f"Camera Backend       : {alpha['camera_backend'] or '-'}")
        print(f"Screen Access        : {alpha['screen_access']}")
        print(f"Camera Access        : {alpha['camera_access']}")
        print(f"Command Execution    : {alpha['command_execution']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def avatar_runtime_alpha_status(self) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Avatar Runtime Alpha Status")
        print("================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Expression Plan Ready        : {status['expression_plan_ready']}")
        print(f"Gesture Plan Ready           : {status['gesture_plan_ready']}")
        print(f"Avatar Context Ready         : {status['avatar_context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Foundation Ready             : {status['foundation_ready']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Avatar Loaded                : {status['avatar_loaded']}")
        print(f"Model Loaded                 : {status['model_loaded']}")
        print(f"Tracking Connected           : {status['tracking_connected']}")
        print(f"Voice Link Ready             : {status['voice_link_ready']}")
        print(f"Vision Link Ready            : {status['vision_link_ready']}")
        print(f"Motion Link Ready            : {status['motion_link_ready']}")
        print(f"Render Backend Found         : {status['render_backend_found']}")
        print(f"Render Backend               : {status['render_backend'] or '-'}")
        print(f"Render Backend Path          : {status['render_backend_path'] or '-'}")
        print(f"Media Backend Found          : {status['media_backend_found']}")
        print(f"Media Backend                : {status['media_backend'] or '-'}")
        print(f"Media Backend Path           : {status['media_backend_path'] or '-'}")
        print(f"Expression Runtime Ready     : {status['expression_runtime_ready']}")
        print(f"Gesture Runtime Ready        : {status['gesture_runtime_ready']}")
        print(f"Motion Runtime Ready         : {status['motion_runtime_ready']}")
        print(f"Render Runtime Ready         : {status['render_runtime_ready']}")
        print(f"Render Performed             : {status['render_performed']}")
        print(f"Expression Changed           : {status['expression_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"External App Opened          : {status['external_app_opened']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Image File Write             : {status['image_file_write']}")
        print(f"Animation File Write         : {status['animation_file_write']}")
        print(f"Requires Prepare Confirmation: {status['requires_prepare_confirmation']}")
        print(f"Requires Write Confirmation  : {status['requires_write_confirmation']}")
        print(f"Requires Command Confirmation: {status['requires_command_confirmation']}")
        print(f"Python Packages              : {status['python_packages_installed']}/{status['python_packages_total']}")
        print(f"Executables                  : {status['executables_found']}/{status['executables_total']}")
        print(f"Supported Expressions        : {status['supported_expressions']}")
        print(f"Supported Gestures           : {status['supported_gestures']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print(f"Note: {status['note']}")

    def avatar_expression_plan(self, expression: str) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.expression_plan(expression=expression)

        print("AURA Avatar Expression Plan")
        print("===========================")
        print(f"Status                    : {plan['status']}")
        print(f"Requested Expression      : {plan['requested_expression']}")
        print(f"Supported                 : {plan['supported']}")
        print(f"Request State             : {plan['request_state']}")
        print(f"Render Command Available  : {plan['render_command_available']}")
        print(f"Render Backend            : {plan['render_backend']['name'] or '-'}")
        print(f"Render Backend Found      : {plan['render_backend']['found']}")
        print(f"Proposed Render Command   : {plan['proposed_render_command'] or '-'}")
        print(f"Render Command Reason     : {plan['render_command_reason']}")
        print(f"Runtime Ready             : {plan['runtime_ready']}")
        print(f"Avatar Loaded             : {plan['avatar_loaded']}")
        print(f"Expression Changed        : {plan['expression_changed']}")
        print(f"Gesture Changed           : {plan['gesture_changed']}")
        print(f"Render Performed          : {plan['render_performed']}")
        print(f"External App Opened       : {plan['external_app_opened']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Image File Write          : {plan['image_file_write_performed']}")
        print(f"Animation File Write      : {plan['animation_file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def avatar_gesture_plan(self, gesture: str) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        plan = manager.gesture_plan(gesture=gesture)

        print("AURA Avatar Gesture Plan")
        print("========================")
        print(f"Status                    : {plan['status']}")
        print(f"Requested Gesture         : {plan['requested_gesture']}")
        print(f"Supported                 : {plan['supported']}")
        print(f"Request State             : {plan['request_state']}")
        print(f"Render Command Available  : {plan['render_command_available']}")
        print(f"Render Backend            : {plan['render_backend']['name'] or '-'}")
        print(f"Render Backend Found      : {plan['render_backend']['found']}")
        print(f"Proposed Render Command   : {plan['proposed_render_command'] or '-'}")
        print(f"Render Command Reason     : {plan['render_command_reason']}")
        print(f"Runtime Ready             : {plan['runtime_ready']}")
        print(f"Avatar Loaded             : {plan['avatar_loaded']}")
        print(f"Expression Changed        : {plan['expression_changed']}")
        print(f"Gesture Changed           : {plan['gesture_changed']}")
        print(f"Render Performed          : {plan['render_performed']}")
        print(f"External App Opened       : {plan['external_app_opened']}")
        print(f"Command Execution         : {plan['command_execution_performed']}")
        print(f"Image File Write          : {plan['image_file_write_performed']}")
        print(f"Animation File Write      : {plan['animation_file_write_performed']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")

        print()
        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")

        print()
        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def avatar_runtime_context(self) -> None:
        manager = AvatarRuntimeAlphaManager(project_root=self.project_root)
        context = manager.context()
        alpha = context["alpha_status"]
        state = context["avatar_state"]

        print("AURA Avatar Runtime Alpha Context")
        print("=================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"Render Performed             : {context['render_performed']}")
        print(f"External App Opened          : {context['external_app_opened']}")
        print(f"Expression Changed           : {context['expression_changed']}")
        print(f"Gesture Changed              : {context['gesture_changed']}")
        print(f"Image File Write             : {context['image_file_write_performed']}")
        print(f"Animation File Write         : {context['animation_file_write_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready           : {alpha['alpha_ready']}")
        print(f"Expression Plan Ready : {alpha['expression_plan_ready']}")
        print(f"Gesture Plan Ready    : {alpha['gesture_plan_ready']}")
        print(f"Render Backend Found  : {alpha['render_backend_found']}")
        print(f"Render Backend        : {alpha['render_backend'] or '-'}")
        print(f"Media Backend Found   : {alpha['media_backend_found']}")
        print(f"Media Backend         : {alpha['media_backend'] or '-'}")
        print(f"Avatar Loaded         : {alpha['avatar_loaded']}")
        print(f"Render Performed      : {alpha['render_performed']}")
        print(f"Command Execution     : {alpha['command_execution']}")
        print()
        print("Avatar State")
        print("------------")
        print(f"Avatar Name       : {state['avatar_name']}")
        print(f"Avatar Format     : {state['avatar_format']}")
        print(f"Runtime           : {state['runtime']}")
        print(f"Body State        : {state['body_state']}")
        print(f"Pose              : {state['pose']}")
        print(f"Expression        : {state['expression']}")
        print(f"Gesture           : {state['gesture']}")
        print(f"Model Loaded      : {state['model_loaded']}")
        print(f"Tracking Connected: {state['tracking_connected']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")

        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")

        print()
        print(f"Note: {context['note']}")


    def desktop_alpha_status(self) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Desktop Assistant Alpha Status")
        print("===================================")
        print(f"Name                          : {status['name']}")
        print(f"Version                       : {status['version']}")
        print(f"Status                        : {status['status']}")
        print(f"Alpha Ready                   : {status['alpha_ready']}")
        print(f"Action Plan Ready             : {status['action_plan_ready']}")
        print(f"Open App Plan Ready           : {status['open_app_plan_ready']}")
        print(f"Open Browser Plan Ready       : {status['open_browser_plan_ready']}")
        print(f"Open File Plan Ready          : {status['open_file_plan_ready']}")
        print(f"Workspace Context Ready       : {status['workspace_context_ready']}")
        print(f"Dependency Check Ready        : {status['dependency_check_ready']}")
        print(f"Bridge Ready                  : {status['bridge_ready']}")
        print(f"Execution Ready               : {status['execution_ready']}")
        print(f"Safe Action Execution         : {status['safe_action_execution']}")
        print(f"App Opened                    : {status['app_opened']}")
        print(f"Browser Opened                : {status['browser_opened']}")
        print(f"File Opened                   : {status['file_opened']}")
        print(f"Click Performed               : {status['click_performed']}")
        print(f"Keyboard Input Performed      : {status['keyboard_input_performed']}")
        print(f"Mouse Control                 : {status['mouse_control']}")
        print(f"Command Execution             : {status['command_execution']}")
        print(f"File Write                    : {status['file_write']}")
        print(f"External App Opened           : {status['external_app_opened']}")
        print(f"Open App Confirmation         : {status['requires_open_app_confirmation']}")
        print(f"Open Browser Confirmation     : {status['requires_open_browser_confirmation']}")
        print(f"Open File Confirmation        : {status['requires_open_file_confirmation']}")
        print(f"Run Command Confirmation      : {status['requires_run_command_confirmation']}")
        print(f"Write File Confirmation       : {status['requires_write_file_confirmation']}")
        print(f"Capability Count              : {status['capability_count']}")
        print(f"Supported Action Types        : {status['supported_action_type_count']}")
        print(f"Sandbox Ready                 : {status['sandbox_ready']}")
        print(f"Sandbox Dry Run Ready         : {status['sandbox_dry_run_ready']}")
        print(f"Real Tool Execution           : {status['real_tool_execution']}")
        print(f"Sections                      : {status['sections']}")
        print()
        print("Environment")
        print("-----------")
        env = status["environment"]
        print(f"OS                  : {env['os']}")
        print(f"OS Release          : {env['os_release']}")
        print(f"Machine             : {env['machine']}")
        print(f"Desktop Environment : {env['desktop_environment']}")
        print(f"Display             : {env['display'] or '-'}")
        print(f"Wayland Display     : {env['wayland_display'] or '-'}")
        print()
        print("Supported Action Types")
        print("----------------------")
        for item in status["supported_action_types"]:
            print(f"- {item}")
        print()
        print(f"Note: {status['note']}")

    def desktop_action_plan(self, action_type: str, target: str) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        plan = manager.action_plan(action_type=action_type, target=target)

        print("AURA Desktop Action Plan")
        print("========================")
        print(f"Status                  : {plan['status']}")
        print(f"Action Type             : {plan['action_type']}")
        print(f"Target                  : {plan['target'] or '-'}")
        print(f"Plan State              : {plan['plan_state']}")
        print(f"Supported               : {plan['supported']}")
        print(f"Description             : {plan['description']}")
        print(f"Plugin Action           : {plan['plugin_action']}")
        print(f"Command Available       : {plan['command_available']}")
        print(f"Proposed Command        : {plan['proposed_command'] or '-'}")
        print(f"Command Reason          : {plan['command_reason']}")
        print(f"Execution Ready         : {plan['execution_ready']}")
        print(f"Executed                : {plan['executed']}")
        print(f"App Opened              : {plan['app_opened']}")
        print(f"Browser Opened          : {plan['browser_opened']}")
        print(f"File Opened             : {plan['file_opened']}")
        print(f"Click Performed         : {plan['click_performed']}")
        print(f"Keyboard Input          : {plan['keyboard_input_performed']}")
        print(f"Mouse Control           : {plan['mouse_control_performed']}")
        print(f"External App Opened     : {plan['external_app_opened']}")
        print(f"Command Execution       : {plan['command_execution_performed']}")
        print(f"File Write              : {plan['file_write_performed']}")
        print()

        print("Permission")
        print("----------")
        permission = plan["permission"]
        print(f"Action       : {permission['action']}")
        print(f"Level        : {permission['level']} - {permission['level_label']}")
        print(f"Allowed      : {permission['allowed']}")
        print(f"Confirmation : {permission['requires_confirmation']}")
        print(f"Reason       : {permission['reason']}")
        print()

        sandbox_check = plan.get("sandbox_check")
        print("Sandbox Check")
        print("-------------")
        if sandbox_check:
            print(f"State      : {sandbox_check['state']}")
            print(f"Allowed    : {sandbox_check['allowed']}")
            print(f"Executed   : {sandbox_check['executed']}")
            print(f"Reason     : {sandbox_check['reason']}")
        else:
            print("-")
        print()

        print("Safety Notes")
        print("------------")
        for item in plan["safety_notes"]:
            print(f"- {item}")

    def desktop_open_app_plan(self, app_name: str) -> None:
        self.desktop_action_plan(action_type="open_app", target=app_name)

    def desktop_open_browser_plan(self, url: str) -> None:
        self.desktop_action_plan(action_type="open_browser", target=url)

    def desktop_open_file_plan(self, file_path: str) -> None:
        self.desktop_action_plan(action_type="open_file", target=file_path)

    def desktop_workspace_context(self) -> None:
        manager = DesktopAssistantAlphaManager(project_root=self.project_root)
        context = manager.workspace_context()
        alpha = context["alpha_status"]
        env = context["environment"]

        print("AURA Desktop Workspace Context")
        print("==============================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"App Opened                   : {context['app_opened']}")
        print(f"Browser Opened               : {context['browser_opened']}")
        print(f"File Opened                  : {context['file_opened']}")
        print(f"Click Performed              : {context['click_performed']}")
        print(f"Keyboard Input Performed     : {context['keyboard_input_performed']}")
        print(f"Mouse Control Performed      : {context['mouse_control_performed']}")
        print()
        print("Alpha Status")
        print("------------")
        print(f"Alpha Ready              : {alpha['alpha_ready']}")
        print(f"Action Plan Ready        : {alpha['action_plan_ready']}")
        print(f"Open App Plan Ready      : {alpha['open_app_plan_ready']}")
        print(f"Open Browser Plan Ready  : {alpha['open_browser_plan_ready']}")
        print(f"Open File Plan Ready     : {alpha['open_file_plan_ready']}")
        print(f"Workspace Context Ready  : {alpha['workspace_context_ready']}")
        print(f"Safe Action Execution    : {alpha['safe_action_execution']}")
        print(f"Command Execution        : {alpha['command_execution']}")
        print(f"File Write               : {alpha['file_write']}")
        print()
        print("Environment")
        print("-----------")
        print(f"OS                  : {env['os']}")
        print(f"OS Release          : {env['os_release']}")
        print(f"Machine             : {env['machine']}")
        print(f"Desktop Environment : {env['desktop_environment']}")
        print(f"Display             : {env['display'] or '-'}")
        print(f"Wayland Display     : {env['wayland_display'] or '-'}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def partner_alpha_status(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Partner Alpha Status")
        print("=========================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Alpha Ready                  : {status['alpha_ready']}")
        print(f"Partner Ready                : {status['partner_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Readiness Report Ready       : {status['readiness_report_ready']}")
        print(f"Next Step Ready              : {status['next_step_ready']}")
        print(f"Action Safety Ready          : {status['action_safety_ready']}")
        print(f"Component Readiness          : {status['component_readiness']}")
        print(f"Awakening Readiness          : {status['awakening_readiness']}")
        print(f"Memory Count                 : {status['memory_count']}")
        print(f"Journal Count                : {status['journal_count']}")
        print(f"Roles                        : {status['roles']}")
        print(f"Skills                       : {status['skills']}")
        print(f"Plugin Actions               : {status['plugin_actions']}")
        print(f"Voice Runtime Alpha Ready    : {status['voice_runtime_alpha_ready']}")
        print(f"Vision Runtime Alpha Ready   : {status['vision_runtime_alpha_ready']}")
        print(f"Avatar Runtime Alpha Ready   : {status['avatar_runtime_alpha_ready']}")
        print(f"Desktop Assistant Alpha Ready: {status['desktop_assistant_alpha_ready']}")
        print(f"Actions Checked              : {status['actions_checked']}")
        print(f"Actions Need Confirmation    : {status['actions_requiring_confirmation']}")
        print(f"Actions Restricted           : {status['actions_restricted']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Safe Action Execution        : {status['safe_action_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Microphone Access            : {status['microphone_access']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"Screen Access                : {status['screen_access']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Avatar Rendering             : {status['avatar_rendering']}")
        print(f"Avatar Expression Changed    : {status['avatar_expression_changed']}")
        print(f"Avatar Gesture Changed       : {status['avatar_gesture_changed']}")
        print(f"Desktop App Opened           : {status['desktop_app_opened']}")
        print(f"Desktop Browser Opened       : {status['desktop_browser_opened']}")
        print(f"Desktop File Opened          : {status['desktop_file_opened']}")
        print(f"Desktop Click Performed      : {status['desktop_click_performed']}")
        print(f"Desktop Keyboard Input       : {status['desktop_keyboard_input_performed']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print()
        print(f"Note: {status['note']}")

    def partner_context(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Partner Alpha Context")
        print("==========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Project")
        print("-------")
        print(f"Project Summary : {context['project_summary']}")
        print(f"Latest Milestone: {context['latest_milestone'] or '-'}")
        print()
        print("Readiness")
        print("---------")
        readiness = context["readiness"]
        print(f"Readiness Ready : {readiness['readiness_ready']}")
        print(f"Readiness       : {readiness['readiness']}")
        print(f"Partner Ready   : {readiness['partner_ready']}")
        print(f"Write Performed : {readiness['write_performed']}")
        print(f"Command Executed: {readiness['command_execution_performed']}")
        print()
        print("Action Safety")
        print("-------------")
        safety = context["action_safety"]
        print(f"Status                    : {safety['status']}")
        print(f"Actions Checked           : {safety['actions_checked']}")
        print(f"Ready Count               : {safety['ready_count']}")
        print(f"Requires Confirmation     : {safety['requires_confirmation_count']}")
        print(f"Restricted Count          : {safety['restricted_count']}")
        print(f"Executed                  : {safety['executed']}")
        print()
        print("Project Insights")
        print("----------------")
        for item in context["project_insights"][:6]:
            print(f"- {item}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in context["recommended_next_steps"][:6]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")

    def partner_readiness(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        readiness = manager.readiness_report()

        print("AURA Partner Alpha Readiness")
        print("============================")
        print(f"Status                       : {readiness['status']}")
        print(f"Readiness Ready              : {readiness['readiness_ready']}")
        print(f"Readiness                    : {readiness['readiness']}")
        print(f"Partner Ready                : {readiness['partner_ready']}")
        print(f"Ready Count                  : {readiness['ready_count']}")
        print(f"Total Components             : {readiness['total_components']}")
        print(f"Write Performed              : {readiness['write_performed']}")
        print(f"Command Execution Performed  : {readiness['command_execution_performed']}")
        print()
        print("Components")
        print("----------")
        for component in readiness["components"]:
            print(f"- {component['name']}")
            print(f"  Status : {component['status']}")
            print(f"  Ready  : {component['ready']}")
            print(f"  Summary: {component['summary']}")
        print()
        print("Blocked Real-World Access")
        print("-------------------------")
        for item in readiness["blocked_real_world_access"]:
            print(f"- {item}")
        print()
        print("Safety State")
        print("------------")
        safety = readiness["safety_state"]
        print(f"Real Tool Execution : {safety['real_tool_execution']}")
        print(f"Safe Action Execution: {safety['safe_action_execution']}")
        print(f"Memory Write        : {safety['memory_write']}")
        print(f"Journal Write       : {safety['journal_write']}")
        print(f"File Write          : {safety['file_write']}")
        print(f"Command Execution   : {safety['command_execution']}")
        print()
        print(f"Note: {readiness['note']}")

    def partner_next_step(self) -> None:
        manager = PartnerAlphaManager(project_root=self.project_root)
        recommendation = manager.next_step_recommendation()

        print("AURA Partner Alpha Next Step")
        print("============================")
        print(f"Status                       : {recommendation['status']}")
        print(f"Recommendation Ready         : {recommendation['recommendation_ready']}")
        print(f"Latest Milestone             : {recommendation['latest_milestone'] or '-'}")
        print(f"Write Performed              : {recommendation['write_performed']}")
        print(f"Memory Write Performed       : {recommendation['memory_write_performed']}")
        print(f"Journal Write Performed      : {recommendation['journal_write_performed']}")
        print(f"Command Execution Performed  : {recommendation['command_execution_performed']}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in recommendation["recommended_next_steps"]:
            print(f"- {item}")
        print()
        print("Safety Notes")
        print("------------")
        for item in recommendation["safety_notes"]:
            print(f"- {item}")


    def workspace_awareness_status(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Workspace Awareness Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Awareness Ready              : {status['awareness_ready']}")
        print(f"Workspace Map Ready          : {status['workspace_map_ready']}")
        print(f"Workspace Context Ready      : {status['workspace_context_ready']}")
        print(f"Current State Ready          : {status['current_state_ready']}")
        print(f"Important Files Ready        : {status['important_files_ready']}")
        print(f"Project Root Detected        : {status['project_root_detected']}")
        print(f"Git Repository Detected      : {status['git_repository_detected']}")
        print(f"Git Branch                   : {status['git_branch']}")
        print(f"Latest Commit Hint           : {status['latest_commit_hint'] or '-'}")
        print(f"AURA Version                 : {status['aura_version']}")
        print(f"Current Sprint               : {status['current_sprint'] or '-'}")
        print(f"Top-Level Directories        : {status['top_level_directories']}")
        print(f"Top-Level Files              : {status['top_level_files']}")
        print(f"Workspace Directories        : {status['workspace_directories']}")
        print(f"Workspace Files              : {status['workspace_files']}")
        print(f"Important Files              : {status['existing_important_file_count']}/{status['important_file_count']}")
        print(f"Ignored Directories          : {status['ignored_dir_count']}")
        print(f"Python Files                 : {status['python_files']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def workspace_map(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        workspace_map = manager.workspace_map(depth=2, limit=120)

        print("AURA Workspace Map")
        print("==================")
        print(f"Status                       : {workspace_map['status']}")
        print(f"Workspace Map Ready          : {workspace_map['workspace_map_ready']}")
        print(f"Project Root                 : {workspace_map['project_root']}")
        print(f"Depth                        : {workspace_map['depth']}")
        print(f"Limit                        : {workspace_map['limit']}")
        print(f"Directories                  : {workspace_map['directories']}")
        print(f"Files                        : {workspace_map['files']}")
        print(f"Read Only                    : {workspace_map['read_only']}")
        print(f"Write Performed              : {workspace_map['write_performed']}")
        print(f"Command Execution Performed  : {workspace_map['command_execution_performed']}")
        print()
        print("Ignored/Runtime Directories")
        print("---------------------------")
        for item in workspace_map["ignored_dirs"]:
            print(f"- {item}")
        print()
        print("Entries")
        print("-------")
        for item in workspace_map["entries"]:
            marker = "D" if item["type"] == "directory" else "F"
            print(f"- [{marker}] {item['path']}")
        print()
        print(f"Note: {workspace_map['note']}")

    def workspace_context(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Workspace Context")
        print("======================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Summary")
        print("-------")
        print(context["workspace_summary"])
        print()
        print("Current State")
        print("-------------")
        state = context["current_state"]
        print(f"Version             : {state['version']}")
        print(f"Codename            : {state['codename']}")
        print(f"Creator             : {state['creator']}")
        print(f"Motto               : {state['motto']}")
        print(f"Current Sprint      : {state['current_sprint'] or '-'}")
        print(f"Git Repository      : {state['git_repository_detected']}")
        print(f"Git Branch          : {state['git_branch']}")
        print(f"Git Status Checked  : {state['git_status_checked']}")
        print(f"Python Files        : {state['python_files']}")
        print(f"Memory Records      : {state['memory_records']}")
        print(f"Journal Entries     : {state['journal_entries']}")
        print()
        print("Top-Level Directories")
        print("---------------------")
        for item in context["top_level_directories"]:
            print(f"- {item}")
        print()
        print("Top-Level Files")
        print("---------------")
        for item in context["top_level_files"]:
            print(f"- {item}")
        print()
        print("Important Files")
        print("---------------")
        for item in context["important_files"]:
            state_text = "exists" if item["exists"] else "missing"
            print(f"- {item['path']} [{state_text}]")
            print(f"  Reason: {item['reason']}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")

    def workspace_current_state(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        state = manager.current_state()

        print("AURA Workspace Current State")
        print("============================")
        print(f"Status                       : {state['status']}")
        print(f"Current State Ready          : {state['current_state_ready']}")
        print(f"Project Root                 : {state['project_root']}")
        print(f"Version                      : {state['version']}")
        print(f"Codename                     : {state['codename']}")
        print(f"Creator                      : {state['creator']}")
        print(f"Motto                        : {state['motto']}")
        print(f"Current Sprint               : {state['current_sprint'] or '-'}")
        print(f"Git Repository Detected      : {state['git_repository_detected']}")
        print(f"Git Branch                   : {state['git_branch']}")
        print(f"Latest Commit Hint           : {state['latest_commit_hint'] or '-'}")
        print(f"Git Status Checked           : {state['git_status_checked']}")
        print(f"Git Status Note              : {state['git_status_note']}")
        print(f"Python Files                 : {state['python_files']}")
        print(f"Memory Records               : {state['memory_records']}")
        print(f"Journal Entries              : {state['journal_entries']}")
        print(f"Read Only                    : {state['read_only']}")
        print(f"Write Performed              : {state['write_performed']}")
        print(f"Command Execution Performed  : {state['command_execution_performed']}")

    def workspace_important_files(self) -> None:
        manager = WorkspaceAwarenessManager(project_root=self.project_root)
        files = manager.important_files()

        print("AURA Workspace Important Files")
        print("==============================")
        print(f"Important File Candidates: {len(files)}")
        print()
        for item in files:
            state_text = "exists" if item["exists"] else "missing"
            print(f"- {item['path']}")
            print(f"  State : {state_text}")
            print(f"  Type  : {item['type']}")
            print(f"  Size  : {item['size_bytes']} bytes")
            print(f"  Reason: {item['reason']}")
        print()
        print("Safety")
        print("------")
        print("Read Only                 : True")
        print("Write Performed           : False")
        print("Command Execution Performed: False")


    def blender_bridge_status(self) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Blender Bridge Foundation Status")
        print("=====================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Bridge Ready                 : {status['bridge_ready']}")
        print(f"Scene Plan Ready             : {status['scene_plan_ready']}")
        print(f"Asset Plan Ready             : {status['asset_plan_ready']}")
        print(f"Texture Plan Ready           : {status['texture_plan_ready']}")
        print(f"Material Plan Ready          : {status['material_plan_ready']}")
        print(f"Rigging Plan Ready           : {status['rigging_plan_ready']}")
        print(f"Animation Plan Ready         : {status['animation_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Asset Awareness Ready        : {status['asset_awareness_ready']}")
        print(f"Backend Found                : {status['backend_found']}")
        print(f"Backend Name                 : {status['backend_name'] or '-'}")
        print(f"Backend Path                 : {status['backend_path'] or '-'}")
        print(f"bpy Found                    : {status['bpy_found']}")
        print(f"Blender Executable Found     : {status['blender_executable_found']}")
        print(f"Blender Executable Path      : {status['blender_executable_path'] or '-'}")
        print(f"FFmpeg Found                 : {status['ffmpeg_found']}")
        print(f"Asset Candidates             : {status['asset_candidate_count']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Blender App Opened           : {status['blender_app_opened']}")
        print(f"Blender Script Executed      : {status['blender_script_executed']}")
        print(f"Scene Modified               : {status['scene_modified']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Blend File Write             : {status['blend_file_write']}")
        print(f"Texture File Write           : {status['texture_file_write']}")
        print(f"Script File Write            : {status['script_file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_blender_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Blender App Opened           : {plan['blender_app_opened']}")
        print(f"Blender Script Executed      : {plan['blender_script_executed']}")
        print(f"Scene Modified               : {plan['scene_modified']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Command Plan")
        print("------------")
        command_plan = plan["command_plan"]
        print(f"Available: {command_plan['available']}")
        print(f"Backend  : {command_plan['backend']['name'] or '-'}")
        print(f"Command  : {command_plan['command'] or '-'}")
        print(f"Reason   : {command_plan['reason']}")
        print()
        print("Asset Summary")
        print("-------------")
        asset_summary = plan["asset_summary"]
        print(f"Candidate Count: {asset_summary['candidate_count']}")
        print(f"Read Only      : {asset_summary['read_only']}")
        print(f"File Write     : {asset_summary['file_write_performed']}")
        print(f"Command Exec   : {asset_summary['command_execution_performed']}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def blender_scene_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.scene_plan(goal)
        self.print_blender_plan("AURA Blender Scene Plan", plan)

    def blender_asset_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.asset_plan(goal)
        self.print_blender_plan("AURA Blender Asset Plan", plan)

    def blender_texture_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.texture_plan(goal)
        self.print_blender_plan("AURA Blender Texture/Material Plan", plan)

    def blender_rigging_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.rigging_plan(goal)
        self.print_blender_plan("AURA Blender Rigging Plan", plan)

    def blender_animation_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        plan = manager.animation_plan(goal)
        self.print_blender_plan("AURA Blender Animation Plan", plan)

    def blender_context(self) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Blender Bridge Context")
        print("===========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print(f"Blender App Opened           : {context['blender_app_opened']}")
        print(f"Blender Script Executed      : {context['blender_script_executed']}")
        print()
        print("Bridge Status")
        print("-------------")
        status = context["bridge_status"]
        print(f"Bridge Ready       : {status['bridge_ready']}")
        print(f"Backend Found      : {status['backend_found']}")
        print(f"Backend Name       : {status['backend_name'] or '-'}")
        print(f"Asset Candidates   : {status['asset_candidate_count']}")
        print(f"Runtime Ready      : {status['runtime_ready']}")
        print(f"File Write         : {status['file_write']}")
        print(f"Command Execution  : {status['command_execution']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(context["workspace_context"]["workspace_summary"])
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print("Asset Summary")
        print("-------------")
        asset_summary = context["asset_summary"]
        print(f"Candidate Count: {asset_summary['candidate_count']}")
        print(f"Read Only      : {asset_summary['read_only']}")
        print(f"File Write     : {asset_summary['file_write_performed']}")
        print(f"Command Exec   : {asset_summary['command_execution_performed']}")
        print()
        print(f"Note: {context['note']}")


    def media_understanding_status(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Media Understanding Foundation Status")
        print("==========================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Understanding Ready          : {status['understanding_ready']}")
        print(f"Asset Summary Ready          : {status['asset_summary_ready']}")
        print(f"Image Plan Ready             : {status['image_plan_ready']}")
        print(f"Texture Reference Ready      : {status['texture_reference_ready']}")
        print(f"Thumbnail Review Ready       : {status['thumbnail_review_ready']}")
        print(f"Video Plan Ready             : {status['video_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Dependency Check Ready       : {status['dependency_check_ready']}")
        print(f"Metadata Inspection Ready    : {status['metadata_inspection_ready']}")
        print(f"Candidate Count              : {status['candidate_count']}")
        print(f"Image Count                  : {status['image_count']}")
        print(f"Texture Reference Count      : {status['texture_reference_count']}")
        print(f"Video Count                  : {status['video_count']}")
        print(f"Audio Count                  : {status['audio_count']}")
        print(f"3D Count                     : {status['three_d_count']}")
        print(f"Design Source Count          : {status['design_source_count']}")
        print(f"PIL Found                    : {status['pil_found']}")
        print(f"cv2 Found                    : {status['cv2_found']}")
        print(f"NumPy Found                  : {status['numpy_found']}")
        print(f"FFmpeg Found                 : {status['ffmpeg_found']}")
        print(f"FFprobe Found                : {status['ffprobe_found']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Metadata Only                : {status['metadata_only']}")
        print(f"Media File Opened            : {status['media_file_opened']}")
        print(f"Media Pixel Read             : {status['media_pixel_read']}")
        print(f"Image Pixel Read             : {status['image_pixel_read']}")
        print(f"Video Frame Read             : {status['video_frame_read']}")
        print(f"Audio Stream Read            : {status['audio_stream_read']}")
        print(f"Thumbnail Generated          : {status['thumbnail_generated']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def media_asset_summary(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        summary = manager.asset_summary()

        print("AURA Media Asset Summary")
        print("========================")
        print(f"Status                       : {summary['status']}")
        print(f"Asset Summary Ready          : {summary['asset_summary_ready']}")
        print(f"Candidate Count              : {summary['candidate_count']}")
        print(f"Image Count                  : {summary['image_count']}")
        print(f"Texture Reference Count      : {summary['texture_reference_count']}")
        print(f"Video Count                  : {summary['video_count']}")
        print(f"Audio Count                  : {summary['audio_count']}")
        print(f"3D Count                     : {summary['three_d_count']}")
        print(f"Design Source Count          : {summary['design_source_count']}")
        print(f"Metadata Only                : {summary['metadata_only']}")
        print(f"File Opened                  : {summary['file_opened']}")
        print(f"Pixel Read                   : {summary['pixel_read']}")
        print(f"File Write Performed         : {summary['file_write_performed']}")
        print(f"Command Execution Performed  : {summary['command_execution_performed']}")
        print()
        print("By Category")
        print("-----------")
        if summary["by_category"]:
            for key, value in sorted(summary["by_category"].items()):
                print(f"- {key}: {value}")
        else:
            print("- none")
        print()
        print("By Suffix")
        print("---------")
        if summary["by_suffix"]:
            for key, value in sorted(summary["by_suffix"].items()):
                print(f"- {key}: {value}")
        else:
            print("- none")
        print()
        print("Assets")
        print("------")
        if summary["assets"]:
            for item in summary["assets"]:
                print(f"- {item['path']} [{item['category']}, {item['suffix']}, {item['size_bytes']} bytes]")
        else:
            print("- no visible media assets found in safe project files")
        print()
        print(f"Note: {summary['note']}")

    def print_media_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Metadata Only                : {plan['metadata_only']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Media File Opened            : {plan['media_file_opened']}")
        print(f"Pixel Read                   : {plan['pixel_read']}")
        print(f"Image Pixel Read             : {plan['image_pixel_read']}")
        print(f"Video Frame Read             : {plan['video_frame_read']}")
        print(f"Audio Stream Read            : {plan['audio_stream_read']}")
        print(f"Thumbnail Generated          : {plan['thumbnail_generated']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Blender Context Ready        : {plan['blender_context_ready']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Asset Summary")
        print("-------------")
        summary = plan["asset_summary"]
        print(f"Candidate Count: {summary['candidate_count']}")
        print(f"Images         : {summary['image_count']}")
        print(f"Videos         : {summary['video_count']}")
        print(f"Audio          : {summary['audio_count']}")
        print(f"3D Assets      : {summary['three_d_count']}")
        print(f"Metadata Only  : {summary['metadata_only']}")
        print(f"File Opened    : {summary['file_opened']}")
        print(f"Pixel Read     : {summary['pixel_read']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def media_image_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Image Description Plan", manager.image_description_plan(goal))

    def media_texture_reference_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Texture Reference Plan", manager.texture_reference_plan(goal))

    def media_thumbnail_review_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Thumbnail/Banner Review Plan", manager.thumbnail_review_plan(goal))

    def media_video_plan(self, goal: str) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        self.print_media_plan("AURA Media Video/Audio Plan", manager.video_plan(goal))

    def media_context(self) -> None:
        manager = MediaUnderstandingFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Media Understanding Context")
        print("================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Metadata Only                : {context['metadata_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Media File Opened            : {context['media_file_opened']}")
        print(f"Pixel Read                   : {context['pixel_read']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Media Status")
        print("------------")
        status = context["media_status"]
        print(f"Understanding Ready : {status['understanding_ready']}")
        print(f"Candidate Count     : {status['candidate_count']}")
        print(f"Image Count         : {status['image_count']}")
        print(f"Video Count         : {status['video_count']}")
        print(f"Audio Count         : {status['audio_count']}")
        print(f"3D Count            : {status['three_d_count']}")
        print(f"Runtime Ready       : {status['runtime_ready']}")
        print(f"File Write          : {status['file_write']}")
        print(f"Command Execution   : {status['command_execution']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(context["workspace_context"]["workspace_summary"])
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print("Asset Summary")
        print("-------------")
        summary = context["asset_summary"]
        print(f"Candidate Count: {summary['candidate_count']}")
        print(f"Metadata Only  : {summary['metadata_only']}")
        print(f"File Opened    : {summary['file_opened']}")
        print(f"Pixel Read     : {summary['pixel_read']}")
        print(f"File Write     : {summary['file_write_performed']}")
        print(f"Command Exec   : {summary['command_execution_performed']}")
        print()
        print(f"Note: {context['note']}")


    def expression_language_status(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Expression Language Status")
        print("===============================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Language Ready               : {status['language_ready']}")
        print(f"State Ready                  : {status['state_ready']}")
        print(f"Plan Ready                   : {status['plan_ready']}")
        print(f"Voice Hint Ready             : {status['voice_hint_ready']}")
        print(f"Avatar Hint Ready            : {status['avatar_hint_ready']}")
        print(f"Gesture Hint Ready           : {status['gesture_hint_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Mood States                  : {status['mood_states']}")
        print(f"Emotion Tags                 : {status['emotion_tags']}")
        print(f"Voice Tones                  : {status['voice_tones']}")
        print(f"Avatar Expressions           : {status['avatar_expressions']}")
        print(f"Gestures                     : {status['gestures']}")
        print(f"Response Styles              : {status['response_styles']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Speaker Output               : {status['speaker_output']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def expression_state(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        state = manager.expression_state()

        print("AURA Expression State")
        print("=====================")
        print(f"Status                       : {state['status']}")
        print(f"State Ready                  : {state['state_ready']}")
        print(f"AURA Name                    : {state['aura_name']}")
        print(f"AURA Version                 : {state['aura_version']}")
        print(f"Codename                     : {state['codename']}")
        print(f"Creator                      : {state['creator']}")
        print(f"Base Mood                    : {state['base_mood']}")
        print(f"Base Emotion Tags            : {', '.join(state['base_emotion_tags'])}")
        print(f"Default Voice Tone           : {state['default_voice_tone']}")
        print(f"Default Avatar Expression    : {state['default_avatar_expression']}")
        print(f"Default Gesture              : {state['default_gesture']}")
        print()
        print("Supported Moods")
        print("---------------")
        for item in state["supported_moods"]:
            print(f"- {item}")
        print()
        print("Supported Emotion Tags")
        print("----------------------")
        for item in state["supported_emotion_tags"]:
            print(f"- {item}")
        print()
        print("Supported Voice Tones")
        print("---------------------")
        for item in state["supported_voice_tones"]:
            print(f"- {item}")
        print()
        print("Supported Avatar Expressions")
        print("----------------------------")
        for item in state["supported_avatar_expressions"]:
            print(f"- {item}")
        print()
        print("Supported Gestures")
        print("------------------")
        for item in state["supported_gestures"]:
            print(f"- {item}")
        print()
        print("Supported Response Styles")
        print("-------------------------")
        for item in state["supported_response_styles"]:
            print(f"- {item}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {state['read_only']}")
        print(f"Write Performed              : {state['write_performed']}")
        print(f"Avatar Changed               : {state['avatar_changed']}")
        print(f"Voice Output Performed       : {state['voice_output_performed']}")
        print(f"Command Execution Performed  : {state['command_execution_performed']}")
        print()
        print(f"Note: {state['note']}")

    def print_expression_hint(self, title: str, hint: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {hint['status']}")
        print(f"Hint Type                    : {hint['hint_type']}")
        print(f"Target                       : {hint['target']}")
        print(f"Hint State                   : {hint['hint_state']}")
        print(f"Mood                         : {hint['mood']}")
        print(f"Emotion Tags                 : {', '.join(hint['emotion_tags'])}")
        print(f"Voice Tone Hint              : {hint['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {hint['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {hint['gesture_hint']}")
        print(f"Response Style Hint          : {hint['response_style_hint']}")
        print(f"Execution Ready              : {hint['execution_ready']}")
        print(f"Executed                     : {hint['executed']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Avatar Changed               : {hint['avatar_changed']}")
        print(f"Gesture Changed              : {hint['gesture_changed']}")
        print(f"Voice Output Performed       : {hint['voice_output_performed']}")
        print(f"File Write Performed         : {hint['file_write_performed']}")
        print(f"Command Execution Performed  : {hint['command_execution_performed']}")
        print(f"External Action Performed    : {hint['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in hint["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in hint["safety_notes"]:
            print(f"- {note}")

    def expression_plan(self, text: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        plan = manager.expression_plan(text)

        print("AURA Expression Plan")
        print("====================")
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Text                         : {plan['text']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Mood                         : {plan['mood']}")
        print(f"Emotion Tags                 : {', '.join(plan['emotion_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Voice Runtime Alpha Ready    : {plan['voice_runtime_alpha_ready']}")
        print(f"Avatar Runtime Alpha Ready   : {plan['avatar_runtime_alpha_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Avatar Plan")
        print("-----------")
        avatar_plan = plan["avatar_plan"]
        print(f"Status               : {avatar_plan['status']}")
        print(f"Requested Expression : {avatar_plan['requested_expression']}")
        print(f"Supported            : {avatar_plan['supported']}")
        print(f"Request State        : {avatar_plan['request_state']}")
        print(f"Expression Changed   : {avatar_plan['expression_changed']}")
        print(f"Render Performed     : {avatar_plan['render_performed']}")
        print()
        print("Gesture Plan")
        print("------------")
        gesture_plan = plan["gesture_plan"]
        print(f"Status             : {gesture_plan['status']}")
        print(f"Requested Gesture  : {gesture_plan['requested_gesture']}")
        print(f"Supported          : {gesture_plan['supported']}")
        print(f"Request State      : {gesture_plan['request_state']}")
        print(f"Gesture Changed    : {gesture_plan['gesture_changed']}")
        print(f"Render Performed   : {gesture_plan['render_performed']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"Gesture Changed              : {plan['gesture_changed']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Speaker Output               : {plan['speaker_output']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def expression_voice_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Voice Hint", manager.voice_hint(target))

    def expression_avatar_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Avatar Hint", manager.avatar_hint(target))

    def expression_gesture_hint(self, target: str) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        self.print_expression_hint("AURA Expression Gesture Hint", manager.gesture_hint(target))

    def expression_context(self) -> None:
        manager = ExpressionLanguageManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Expression Language Context")
        print("================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"Gesture Changed              : {context['gesture_changed']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Expression Status")
        print("-----------------")
        status = context["expression_status"]
        print(f"Language Ready      : {status['language_ready']}")
        print(f"State Ready         : {status['state_ready']}")
        print(f"Plan Ready          : {status['plan_ready']}")
        print(f"Voice Hint Ready    : {status['voice_hint_ready']}")
        print(f"Avatar Hint Ready   : {status['avatar_hint_ready']}")
        print(f"Gesture Hint Ready  : {status['gesture_hint_ready']}")
        print(f"Context Ready       : {status['context_ready']}")
        print(f"Runtime Ready       : {status['runtime_ready']}")
        print()
        print("Expression State")
        print("----------------")
        state = context["expression_state"]
        print(f"Base Mood               : {state['base_mood']}")
        print(f"Default Voice Tone      : {state['default_voice_tone']}")
        print(f"Default Avatar Expression: {state['default_avatar_expression']}")
        print(f"Default Gesture         : {state['default_gesture']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def game_companion_status(self) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Game Companion Foundation Status")
        print("=====================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Companion Ready              : {status['companion_ready']}")
        print(f"Session Plan Ready           : {status['session_plan_ready']}")
        print(f"Strategy Plan Ready          : {status['strategy_plan_ready']}")
        print(f"Streaming Plan Ready         : {status['streaming_plan_ready']}")
        print(f"Coaching Plan Ready          : {status['coaching_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Expression Integration Ready : {status['expression_integration_ready']}")
        print(f"Vision Integration Ready     : {status['vision_integration_ready']}")
        print(f"Desktop Integration Ready    : {status['desktop_integration_ready']}")
        print(f"Media Integration Ready      : {status['media_integration_ready']}")
        print(f"Partner Integration Ready    : {status['partner_integration_ready']}")
        print(f"Supported Styles             : {status['supported_styles']}")
        print(f"Support Modes                : {status['support_modes']}")
        print(f"Safety Boundaries            : {status['safety_boundaries']}")
        print(f"Gaming Mode                  : {status['gaming_mode']}")
        print(f"Streaming Mode               : {status['streaming_mode']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Game Screen Read             : {status['game_screen_read']}")
        print(f"Screen Capture               : {status['screen_capture']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Game Input Control           : {status['game_input_control']}")
        print(f"Keyboard Input               : {status['keyboard_input']}")
        print(f"Mouse Control                : {status['mouse_control']}")
        print(f"Game App Opened              : {status['game_app_opened']}")
        print(f"Desktop Action Execution     : {status['desktop_action_execution']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_game_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Game Style                   : {plan['game_style']}")
        print(f"Game Tags                    : {', '.join(plan['game_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Desktop Context Ready        : {plan['desktop_context_ready']}")
        print(f"Media Context Ready          : {plan['media_context_ready']}")
        print(f"Partner Context Ready        : {plan['partner_context_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Game Context")
        print("------------")
        context = plan["game_context"]
        print(f"Style               : {context['style']}")
        print(f"Tags                : {', '.join(context['tags'])}")
        print(f"Streaming Related   : {context['streaming_related']}")
        print(f"Competitive Related : {context['competitive_related']}")
        print(f"Strategy Related    : {context['strategy_related']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Game Screen Read             : {plan['game_screen_read']}")
        print(f"Screen Capture Performed     : {plan['screen_capture_performed']}")
        print(f"Camera Access Performed      : {plan['camera_access_performed']}")
        print(f"Keyboard Input Performed     : {plan['keyboard_input_performed']}")
        print(f"Mouse Control Performed      : {plan['mouse_control_performed']}")
        print(f"Game Input Control           : {plan['game_input_control']}")
        print(f"Game App Opened              : {plan['game_app_opened']}")
        print(f"Desktop Action Performed     : {plan['desktop_action_performed']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def game_session_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Session Plan", manager.session_plan(target))

    def game_strategy_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Strategy Plan", manager.strategy_plan(target))

    def game_streaming_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Streaming Plan", manager.streaming_plan(target))

    def game_coaching_plan(self, target: str) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        self.print_game_plan("AURA Game Coaching Plan", manager.coaching_plan(target))

    def game_context(self) -> None:
        manager = GameCompanionFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Game Companion Context")
        print("===========================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Game Screen Read             : {context['game_screen_read']}")
        print(f"Game Input Control           : {context['game_input_control']}")
        print(f"Game App Opened              : {context['game_app_opened']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Game Status")
        print("-----------")
        status = context["game_status"]
        print(f"Companion Ready      : {status['companion_ready']}")
        print(f"Session Plan Ready   : {status['session_plan_ready']}")
        print(f"Strategy Plan Ready  : {status['strategy_plan_ready']}")
        print(f"Streaming Plan Ready : {status['streaming_plan_ready']}")
        print(f"Coaching Plan Ready  : {status['coaching_plan_ready']}")
        print(f"Context Ready        : {status['context_ready']}")
        print(f"Runtime Ready        : {status['runtime_ready']}")
        print()
        print("Integrations")
        print("------------")
        print(f"Expression : {status['expression_integration_ready']}")
        print(f"Vision     : {status['vision_integration_ready']}")
        print(f"Desktop    : {status['desktop_integration_ready']}")
        print(f"Media      : {status['media_integration_ready']}")
        print(f"Partner    : {status['partner_integration_ready']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def streaming_safety_status(self) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Streaming Safety Foundation Status")
        print("=======================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Safety Ready                 : {status['safety_ready']}")
        print(f"Context Plan Ready           : {status['context_plan_ready']}")
        print(f"Chat Safety Ready            : {status['chat_safety_ready']}")
        print(f"Content Boundary Ready       : {status['content_boundary_ready']}")
        print(f"Privacy Plan Ready           : {status['privacy_plan_ready']}")
        print(f"Moderation Plan Ready        : {status['moderation_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Game Integration Ready       : {status['game_integration_ready']}")
        print(f"Expression Integration Ready : {status['expression_integration_ready']}")
        print(f"Media Integration Ready      : {status['media_integration_ready']}")
        print(f"Vision Integration Ready     : {status['vision_integration_ready']}")
        print(f"Desktop Integration Ready    : {status['desktop_integration_ready']}")
        print(f"Safety Categories            : {status['safety_categories']}")
        print(f"Stream Modes                 : {status['stream_modes']}")
        print(f"Disabled Runtime Actions     : {status['disabled_runtime_actions']}")
        print(f"Streaming Mode               : {status['streaming_mode']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Live Chat Read               : {status['live_chat_read']}")
        print(f"Message Sent                 : {status['message_sent']}")
        print(f"Moderation Action            : {status['moderation_action']}")
        print(f"Screen Capture               : {status['screen_capture']}")
        print(f"Camera Access                : {status['camera_access']}")
        print(f"Browser Opened               : {status['browser_opened']}")
        print(f"App Opened                   : {status['app_opened']}")
        print(f"Voice Output                 : {status['voice_output']}")
        print(f"Avatar Changed               : {status['avatar_changed']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_streaming_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Stream Priority              : {plan['stream_priority']}")
        print(f"Stream Tags                  : {', '.join(plan['stream_tags'])}")
        print(f"Voice Tone Hint              : {plan['voice_tone_hint']}")
        print(f"Avatar Expression Hint       : {plan['avatar_expression_hint']}")
        print(f"Gesture Hint                 : {plan['gesture_hint']}")
        print(f"Response Style Hint          : {plan['response_style_hint']}")
        print(f"Game Context Ready           : {plan['game_context_ready']}")
        print(f"Expression Context Ready     : {plan['expression_context_ready']}")
        print(f"Media Context Ready          : {plan['media_context_ready']}")
        print(f"Vision Context Ready         : {plan['vision_context_ready']}")
        print(f"Desktop Context Ready        : {plan['desktop_context_ready']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print()
        print("Stream Context")
        print("--------------")
        context = plan["stream_context"]
        print(f"Priority        : {context['priority']}")
        print(f"Tags            : {', '.join(context['tags'])}")
        print(f"Chat Related    : {context['chat_related']}")
        print(f"Privacy Related : {context['privacy_related']}")
        print(f"Game Related    : {context['game_related']}")
        print(f"Avatar Related  : {context['avatar_related']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Live Chat Read               : {plan['live_chat_read']}")
        print(f"Chat Message Sent            : {plan['chat_message_sent']}")
        print(f"Moderation Action Performed  : {plan['moderation_action_performed']}")
        print(f"Screen Capture Performed     : {plan['screen_capture_performed']}")
        print(f"Camera Access Performed      : {plan['camera_access_performed']}")
        print(f"Browser Opened               : {plan['browser_opened']}")
        print(f"App Opened                   : {plan['app_opened']}")
        print(f"Voice Output Performed       : {plan['voice_output_performed']}")
        print(f"Avatar Changed               : {plan['avatar_changed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def streaming_context_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Context Plan", manager.context_plan(target))

    def streaming_chat_safety_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Chat Safety Plan", manager.chat_safety_plan(target))

    def streaming_content_boundary_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Content Boundary Plan", manager.content_boundary_plan(target))

    def streaming_privacy_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Privacy Plan", manager.privacy_plan(target))

    def streaming_moderation_plan(self, target: str) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        self.print_streaming_plan("AURA Streaming Moderation Plan", manager.moderation_plan(target))

    def streaming_safety_context(self) -> None:
        manager = StreamingSafetyFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Streaming Safety Context")
        print("=============================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Live Chat Read               : {context['live_chat_read']}")
        print(f"Message Sent                 : {context['message_sent']}")
        print(f"Moderation Action            : {context['moderation_action']}")
        print(f"Screen Capture               : {context['screen_capture']}")
        print(f"Camera Access                : {context['camera_access']}")
        print(f"Browser Opened               : {context['browser_opened']}")
        print(f"App Opened                   : {context['app_opened']}")
        print(f"Voice Output Performed       : {context['voice_output_performed']}")
        print(f"Avatar Changed               : {context['avatar_changed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Streaming Status")
        print("----------------")
        status = context["streaming_status"]
        print(f"Safety Ready           : {status['safety_ready']}")
        print(f"Context Plan Ready     : {status['context_plan_ready']}")
        print(f"Chat Safety Ready      : {status['chat_safety_ready']}")
        print(f"Content Boundary Ready : {status['content_boundary_ready']}")
        print(f"Privacy Plan Ready     : {status['privacy_plan_ready']}")
        print(f"Moderation Plan Ready  : {status['moderation_plan_ready']}")
        print(f"Context Ready          : {status['context_ready']}")
        print(f"Runtime Ready          : {status['runtime_ready']}")
        print()
        print("Integrations")
        print("------------")
        print(f"Game       : {status['game_integration_ready']}")
        print(f"Expression : {status['expression_integration_ready']}")
        print(f"Media      : {status['media_integration_ready']}")
        print(f"Vision     : {status['vision_integration_ready']}")
        print(f"Desktop    : {status['desktop_integration_ready']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def workspace_memory_link_status(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Workspace Memory Link Status")
        print("=================================")
        print(f"Name                         : {status['name']}")
        print(f"Version                      : {status['version']}")
        print(f"Status                       : {status['status']}")
        print(f"Link Ready                   : {status['link_ready']}")
        print(f"Summary Ready                : {status['summary_ready']}")
        print(f"Memory Candidates Ready      : {status['memory_candidates_ready']}")
        print(f"File Memory Candidates Ready : {status['file_memory_candidates_ready']}")
        print(f"Milestone Candidates Ready   : {status['milestone_candidates_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Workspace Integration Ready  : {status['workspace_integration_ready']}")
        print(f"Memory Store Ready           : {status['memory_store_ready']}")
        print(f"Journal Integration Ready    : {status['journal_integration_ready']}")
        print(f"Reflection Integration Ready : {status['reflection_integration_ready']}")
        print(f"Memory Count                 : {status['memory_count']}")
        print(f"Journal Count                : {status['journal_count']}")
        print(f"Milestone Count              : {status['milestone_count']}")
        print(f"Important File Count         : {status['important_file_count']}")
        print(f"Candidate Types              : {status['candidate_types']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print(f"Sections                     : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                    : {status['read_only']}")
        print(f"Candidate Only               : {status['candidate_only']}")
        print(f"Memory Write                 : {status['memory_write']}")
        print(f"Memory Delete                : {status['memory_delete']}")
        print(f"Journal Write                : {status['journal_write']}")
        print(f"File Write                   : {status['file_write']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"External Action Execution    : {status['external_action_execution']}")
        print(f"Real Tool Execution          : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def workspace_memory_summary(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        summary = manager.summary()

        print("AURA Workspace Memory Summary")
        print("=============================")
        print(f"Status                       : {summary['status']}")
        print(f"Summary Ready                : {summary['summary_ready']}")
        print(f"Memory Count                 : {summary['memory_count']}")
        print(f"Journal Count                : {summary['journal_count']}")
        print(f"Milestone Count              : {summary['milestone_count']}")
        print(f"Read Only                    : {summary['read_only']}")
        print(f"Write Performed              : {summary['write_performed']}")
        print(f"Memory Write Performed       : {summary['memory_write_performed']}")
        print(f"Memory Delete Performed      : {summary['memory_delete_performed']}")
        print(f"Journal Write Performed      : {summary['journal_write_performed']}")
        print(f"File Write Performed         : {summary['file_write_performed']}")
        print(f"Command Execution Performed  : {summary['command_execution_performed']}")
        print(f"External Action Performed    : {summary['external_action_execution_performed']}")
        print()
        print("Summary")
        print("-------")
        print(summary["summary"])
        print()
        print("Workspace Summary")
        print("-----------------")
        print(summary["workspace_summary"])
        latest = summary.get("latest_milestone")
        if latest:
            print()
            print("Latest Milestone")
            print("----------------")
            print(f"Title      : {latest['title']}")
            print(f"Created At : {latest['created_at']}")
        print()
        print(f"Note: {summary['note']}")

    def print_workspace_memory_candidates(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                       : {plan['status']}")
        print(f"Plan Type                    : {plan['plan_type']}")
        print(f"Target                       : {plan['target']}")
        print(f"Plan State                   : {plan['plan_state']}")
        print(f"Candidate Count              : {plan['candidate_count']}")
        print(f"Execution Ready              : {plan['execution_ready']}")
        print(f"Executed                     : {plan['executed']}")
        print(f"Read Only                    : {plan['read_only']}")
        print(f"Memory Write Performed       : {plan['memory_write_performed']}")
        print(f"Memory Delete Performed      : {plan['memory_delete_performed']}")
        print(f"Journal Write Performed      : {plan['journal_write_performed']}")
        print(f"File Write Performed         : {plan['file_write_performed']}")
        print(f"Command Execution Performed  : {plan['command_execution_performed']}")
        print(f"External Action Performed    : {plan['external_action_execution_performed']}")
        print()
        print("Candidates")
        print("----------")
        for index, candidate in enumerate(plan["candidates"], start=1):
            metadata = candidate["metadata"]
            print(f"{index}. Type       : {candidate['candidate_type']}")
            print(f"   Kind       : {candidate['kind']}")
            print(f"   Importance : {metadata['suggested_importance']}")
            print(f"   Pinned     : {metadata['suggested_pinned']}")
            print(f"   Write Ready: {candidate['write_ready']}")
            print(f"   Written    : {candidate['written']}")
            print(f"   Reason     : {candidate['reason']}")
            print(f"   Content    : {candidate['content']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def workspace_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace Memory Candidates",
            manager.project_memory_candidates(target),
        )

    def workspace_file_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace File Memory Candidates",
            manager.file_memory_candidates(target),
        )

    def workspace_milestone_memory_candidates(self, target: str) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        self.print_workspace_memory_candidates(
            "AURA Workspace Milestone Memory Candidates",
            manager.milestone_memory_candidates(target),
        )

    def workspace_memory_link_context(self) -> None:
        manager = WorkspaceMemoryLinkManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Workspace Memory Link Context")
        print("==================================")
        print(f"Status                       : {context['status']}")
        print(f"Context Ready                : {context['context_ready']}")
        print(f"Read Only                    : {context['read_only']}")
        print(f"Write Performed              : {context['write_performed']}")
        print(f"Memory Write Performed       : {context['memory_write_performed']}")
        print(f"Memory Delete Performed      : {context['memory_delete_performed']}")
        print(f"Journal Write Performed      : {context['journal_write_performed']}")
        print(f"File Write Performed         : {context['file_write_performed']}")
        print(f"Command Execution Performed  : {context['command_execution_performed']}")
        print(f"External Action Performed    : {context['external_action_execution_performed']}")
        print()
        print("Link Status")
        print("-----------")
        status = context["link_status"]
        print(f"Link Ready              : {status['link_ready']}")
        print(f"Summary Ready           : {status['summary_ready']}")
        print(f"Memory Candidates Ready : {status['memory_candidates_ready']}")
        print(f"File Candidates Ready   : {status['file_memory_candidates_ready']}")
        print(f"Milestone Ready         : {status['milestone_candidates_ready']}")
        print(f"Context Ready           : {status['context_ready']}")
        print(f"Candidate Only          : {status['candidate_only']}")
        print(f"Runtime Ready           : {status['runtime_ready']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def project_intent_status(self) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Project Intent Planner Status")
        print("==================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Intent Ready                          : {status['intent_ready']}")
        print(f"Summary Ready                         : {status['summary_ready']}")
        print(f"Goal Plan Ready                       : {status['goal_plan_ready']}")
        print(f"Sprint Intent Plan Ready              : {status['sprint_intent_plan_ready']}")
        print(f"Next Action Candidates Ready          : {status['next_action_candidates_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Workspace Awareness Integration       : {status['workspace_awareness_integration_ready']}")
        print(f"Project Coding Integration            : {status['project_coding_integration_ready']}")
        print(f"Daily Briefing Integration            : {status['daily_briefing_integration_ready']}")
        print(f"Memory Reflection Integration         : {status['memory_reflection_integration_ready']}")
        print(f"Intent Categories                     : {status['intent_categories']}")
        print(f"Project Python Files                  : {status['project_python_files']}")
        print(f"Memory Count                          : {status['memory_count']}")
        print(f"Journal Count                         : {status['journal_count']}")
        print(f"Milestone Count                       : {status['milestone_count']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"Memory Write                          : {status['memory_write']}")
        print(f"Journal Write                         : {status['journal_write']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def project_intent_summary(self, topic: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        summary = manager.summary(topic)

        print("AURA Project Intent Summary")
        print("===========================")
        print(f"Status                                : {summary['status']}")
        print(f"Summary Ready                         : {summary['summary_ready']}")
        print(f"Topic                                 : {summary['topic']}")
        print(f"Read Only                             : {summary['read_only']}")
        print(f"Write Performed                       : {summary['write_performed']}")
        print(f"File Write Performed                  : {summary['file_write_performed']}")
        print(f"Memory Write Performed                : {summary['memory_write_performed']}")
        print(f"Journal Write Performed               : {summary['journal_write_performed']}")
        print(f"Command Execution Performed           : {summary['command_execution_performed']}")
        print(f"External Action Performed             : {summary['external_action_execution_performed']}")
        print()
        print("Intent")
        print("------")
        intent = summary["intent"]
        print(f"Priority       : {intent['priority']}")
        print(f"Tags           : {', '.join(intent['tags'])}")
        print(f"Safety Related : {intent['safety_related']}")
        print(f"Sprint Related : {intent['sprint_related']}")
        print(f"Implementation : {intent['implementation_related']}")
        print(f"Memory Related : {intent['memory_related']}")
        print()
        print("Summary")
        print("-------")
        print(summary["summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(summary["workspace_memory_summary"])
        print()
        print("Daily Project Summary")
        print("---------------------")
        print(summary["daily_project_summary"])
        print()
        print("Top Insights")
        print("------------")
        for item in summary["top_insights"]:
            print(f"- {item}")
        print()
        print("Recommended Next Steps")
        print("----------------------")
        for item in summary["recommended_next_steps"]:
            print(f"- {item}")
        print()
        print(f"Note: {summary['note']}")

    def print_project_intent_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Intent Priority                       : {plan['intent_priority']}")
        print(f"Intent Tags                           : {', '.join(plan['intent_tags'])}")
        print(f"Project Coding Route                  : {plan['project_coding_route']}")
        print(f"Project Python Files                  : {plan['project_python_files']}")
        print(f"Action Candidate Count                : {plan['action_candidate_count']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"Memory Write Performed                : {plan['memory_write_performed']}")
        print(f"Journal Write Performed               : {plan['journal_write_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print()
        print("Intent")
        print("------")
        intent = plan["intent"]
        print(f"Priority                 : {intent['priority']}")
        print(f"Tags                     : {', '.join(intent['tags'])}")
        print(f"Safety Related           : {intent['safety_related']}")
        print(f"Sprint Related           : {intent['sprint_related']}")
        print(f"Implementation Related   : {intent['implementation_related']}")
        print(f"Memory Related           : {intent['memory_related']}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Daily Project Summary")
        print("---------------------")
        print(plan["daily_project_summary"])
        print()
        print("Patch Plan")
        print("----------")
        patch_plan = plan["patch_plan"]
        print(f"Mode                     : {patch_plan['mode']}")
        print(f"File Write Performed     : {patch_plan['file_write_performed']}")
        print(f"Command Execution        : {patch_plan['command_execution_performed']}")
        print(f"Coding Route             : {patch_plan['coding_route']}")
        print("Related Files:")
        for file in patch_plan["related_files"]:
            print(f"- {file}")
        print()
        print("Action Candidates")
        print("-----------------")
        for index, candidate in enumerate(plan["action_candidates"], start=1):
            print(f"{index}. {candidate['name']}")
            print(f"   Importance : {candidate['importance']}")
            print(f"   Candidate  : {candidate['candidate_only']}")
            print(f"   Executed   : {candidate['executed']}")
            print(f"   Reason     : {candidate['reason']}")
            print(f"   Detail     : {candidate['description']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def project_goal_plan(self, goal: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Project Goal Plan",
            manager.goal_plan(goal),
        )

    def sprint_intent_plan(self, goal: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Sprint Intent Plan",
            manager.sprint_intent_plan(goal),
        )

    def project_next_action_candidates(self, topic: str) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        self.print_project_intent_plan(
            "AURA Project Next Action Candidates",
            manager.next_action_candidates(topic),
        )

    def project_intent_context(self) -> None:
        manager = ProjectIntentPlannerManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Project Intent Context")
        print("===========================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"Memory Write Performed                : {context['memory_write_performed']}")
        print(f"Journal Write Performed               : {context['journal_write_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print()
        print("Planner Status")
        print("--------------")
        status = context["planner_status"]
        print(f"Intent Ready                 : {status['intent_ready']}")
        print(f"Summary Ready                : {status['summary_ready']}")
        print(f"Goal Plan Ready              : {status['goal_plan_ready']}")
        print(f"Sprint Intent Plan Ready     : {status['sprint_intent_plan_ready']}")
        print(f"Next Action Candidates Ready : {status['next_action_candidates_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Proposal Only                : {status['proposal_only']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print()
        print("Project Coding Status")
        print("---------------------")
        coding = context["project_coding_status"]
        print(f"Status              : {coding['status']}")
        print(f"Analysis Ready      : {coding['analysis_ready']}")
        print(f"Patch Planning Ready: {coding['patch_planning_ready']}")
        print(f"Python Files        : {coding['python_files']}")
        print(f"Coding Route        : {coding['coding_route']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def creative_assistant_status(self) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Creative Assistant Foundation Status")
        print("========================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Assistant Ready                       : {status['assistant_ready']}")
        print(f"Brief Plan Ready                      : {status['brief_plan_ready']}")
        print(f"Character Concept Ready               : {status['character_concept_ready']}")
        print(f"Visual Asset Plan Ready               : {status['visual_asset_plan_ready']}")
        print(f"Content Idea Plan Ready               : {status['content_idea_plan_ready']}")
        print(f"Review Plan Ready                     : {status['review_plan_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Project Intent Integration            : {status['project_intent_integration_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Media Understanding Integration       : {status['media_understanding_integration_ready']}")
        print(f"Expression Language Integration       : {status['expression_language_integration_ready']}")
        print(f"Blender Bridge Integration            : {status['blender_bridge_integration_ready']}")
        print(f"Creative Plan Types                   : {status['creative_plan_types']}")
        print(f"Media Candidate Count                 : {status['media_candidate_count']}")
        print(f"Blender Asset Candidate Count         : {status['blender_asset_candidate_count']}")
        print(f"Expression Mood States                : {status['expression_mood_states']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"Image Generation                      : {status['image_generation']}")
        print(f"Media File Opened                     : {status['media_file_opened']}")
        print(f"Pixel Read                            : {status['pixel_read']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_creative_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Creative Focus                        : {plan['creative_direction']['focus']}")
        print(f"Creative Tags                         : {', '.join(plan['creative_direction']['tags'])}")
        print(f"Brand Anchor                          : {plan['creative_direction']['brand_anchor']}")
        print(f"Safety Priority                       : {plan['creative_direction']['safety_priority']}")
        print(f"Creative Output Count                 : {plan['creative_output_count']}")
        print(f"Media Candidate Count                 : {plan['media_candidate_count']}")
        print(f"Media Metadata Only                   : {plan['media_metadata_only']}")
        print(f"Expression Mood                       : {plan['expression_mood']}")
        print(f"Expression Tags                       : {', '.join(plan['expression_tags'])}")
        print(f"Blender Asset Candidate Count         : {plan['blender_asset_candidate_count']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"Proposal Only                         : {plan['proposal_only']}")
        print(f"Image Generation Performed            : {plan['image_generation_performed']}")
        print(f"Media File Opened                     : {plan['media_file_opened']}")
        print(f"Pixel Read                            : {plan['pixel_read']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print()
        print("Creative Outputs")
        print("----------------")
        for item in plan["creative_outputs"]:
            print(f"- {item}")
        print()
        print("Project Intent Summary")
        print("----------------------")
        print(plan["project_intent_summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Expression Plan")
        print("---------------")
        expression = plan["expression_plan"]
        print(f"Mood              : {expression['mood']}")
        print(f"Voice Tone Hint   : {expression['voice_tone_hint']}")
        print(f"Avatar Expression : {expression['avatar_expression_hint']}")
        print(f"Gesture Hint      : {expression['gesture_hint']}")
        print(f"Response Style    : {expression['response_style_hint']}")
        print(f"Avatar Changed    : {expression['avatar_changed']}")
        print(f"Voice Output      : {expression['voice_output_performed']}")
        print()
        print("Recommended Steps")
        print("-----------------")
        for step in plan["recommended_steps"]:
            print(f"- {step}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def creative_brief_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Brief Plan",
            manager.brief_plan(target),
        )

    def creative_character_concept_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Character Concept Plan",
            manager.character_concept_plan(target),
        )

    def creative_visual_asset_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Visual Asset Plan",
            manager.visual_asset_plan(target),
        )

    def creative_content_idea_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Content Idea Plan",
            manager.content_idea_plan(target),
        )

    def creative_review_plan(self, target: str) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        self.print_creative_plan(
            "AURA Creative Review Plan",
            manager.review_plan(target),
        )

    def creative_context(self) -> None:
        manager = CreativeAssistantFoundationManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Creative Assistant Context")
        print("===============================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Proposal Only                         : {context['proposal_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"Image Generation Performed            : {context['image_generation_performed']}")
        print(f"Media File Opened                     : {context['media_file_opened']}")
        print(f"Pixel Read                            : {context['pixel_read']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print()
        print("Creative Status")
        print("---------------")
        status = context["creative_status"]
        print(f"Assistant Ready              : {status['assistant_ready']}")
        print(f"Brief Plan Ready             : {status['brief_plan_ready']}")
        print(f"Character Concept Ready      : {status['character_concept_ready']}")
        print(f"Visual Asset Plan Ready      : {status['visual_asset_plan_ready']}")
        print(f"Content Idea Plan Ready      : {status['content_idea_plan_ready']}")
        print(f"Review Plan Ready            : {status['review_plan_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Proposal Only                : {status['proposal_only']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print()
        print("Integration Summary")
        print("-------------------")
        integration = context["integration_summary"]
        print(f"Project Intent Ready         : {integration['project_intent_ready']}")
        print(f"Workspace Memory Ready       : {integration['workspace_memory_ready']}")
        print(f"Media Understanding Ready    : {integration['media_understanding_ready']}")
        print(f"Expression Language Ready    : {integration['expression_language_ready']}")
        print(f"Blender Bridge Ready         : {integration['blender_bridge_ready']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def local_task_planner_status(self) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Local Task Planner Alpha Status")
        print("====================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Planner Ready                         : {status['planner_ready']}")
        print(f"Task Intent Plan Ready                : {status['task_intent_plan_ready']}")
        print(f"Task Breakdown Plan Ready             : {status['task_breakdown_plan_ready']}")
        print(f"Task Risk Review Ready                : {status['task_risk_review_ready']}")
        print(f"Task Execution Checklist Ready        : {status['task_execution_checklist_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Project Intent Integration            : {status['project_intent_integration_ready']}")
        print(f"Creative Assistant Integration        : {status['creative_assistant_integration_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Tool Sandbox Integration              : {status['tool_sandbox_integration_ready']}")
        print(f"Tool Sandbox Dry Run Ready            : {status['tool_sandbox_dry_run_ready']}")
        print(f"Tool Sandbox Real Execution Ready     : {status['tool_sandbox_real_execution_ready']}")
        print(f"Task Plan Types                       : {status['task_plan_types']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"App Opened                            : {status['app_opened']}")
        print(f"Desktop Action Execution              : {status['desktop_action_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_local_task_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Task Priority                         : {plan['task_priority']}")
        print(f"Task Tags                             : {', '.join(plan['task_tags'])}")
        print(f"Step Count                            : {plan['step_count']}")
        print(f"Checklist Count                       : {plan['checklist_count']}")
        print(f"Tool Sandbox Ready                    : {plan['tool_sandbox_ready']}")
        print(f"Tool Sandbox Dry Run Ready            : {plan['tool_sandbox_dry_run_ready']}")
        print(f"Tool Sandbox Real Execution Ready     : {plan['tool_sandbox_real_execution_ready']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"Proposal Only                         : {plan['proposal_only']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"App Opened                            : {plan['app_opened']}")
        print(f"Desktop Action Performed              : {plan['desktop_action_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print(f"Real Tool Execution Performed         : {plan['real_tool_execution_performed']}")
        print()
        print("Project Intent Summary")
        print("----------------------")
        print(plan["project_intent_summary"])
        print()
        print("Creative Brief Focus")
        print("--------------------")
        print(plan["creative_brief_focus"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Recommended Steps")
        print("-----------------")
        for index, step in enumerate(plan["recommended_steps"], start=1):
            print(f"{index}. {step['title']}")
            print(f"   Risk        : {step['risk']}")
            print(f"   Ready       : {step['ready']}")
            print(f"   Confirmation: {step['requires_confirmation']}")
            print(f"   Description : {step['description']}")
        print()
        print("Checklist")
        print("---------")
        for item in plan["checklist"]:
            print(f"- {item}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def local_task_intent_plan(self, target: str) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.print_local_task_plan(
            "AURA Local Task Intent Plan",
            manager.task_intent_plan(target),
        )

    def local_task_breakdown_plan(self, target: str) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.print_local_task_plan(
            "AURA Local Task Breakdown Plan",
            manager.task_breakdown_plan(target),
        )

    def local_task_risk_review(self, target: str) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.print_local_task_plan(
            "AURA Local Task Risk Review",
            manager.task_risk_review(target),
        )

    def local_task_execution_checklist(self, target: str) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        self.print_local_task_plan(
            "AURA Local Task Execution Checklist",
            manager.task_execution_checklist(target),
        )

    def local_task_context(self) -> None:
        manager = LocalTaskPlannerAlphaManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Local Task Planner Context")
        print("===============================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Proposal Only                         : {context['proposal_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"App Opened                            : {context['app_opened']}")
        print(f"Desktop Action Performed              : {context['desktop_action_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print(f"Real Tool Execution Performed         : {context['real_tool_execution_performed']}")
        print()
        print("Planner Status")
        print("--------------")
        status = context["planner_status"]
        print(f"Planner Ready                : {status['planner_ready']}")
        print(f"Task Intent Plan Ready       : {status['task_intent_plan_ready']}")
        print(f"Task Breakdown Plan Ready    : {status['task_breakdown_plan_ready']}")
        print(f"Task Risk Review Ready       : {status['task_risk_review_ready']}")
        print(f"Execution Checklist Ready    : {status['task_execution_checklist_ready']}")
        print(f"Context Ready                : {status['context_ready']}")
        print(f"Runtime Ready                : {status['runtime_ready']}")
        print()
        print("Tool Sandbox")
        print("------------")
        sandbox = context["tool_sandbox_status"]
        print(f"Sandbox Ready                : {sandbox['sandbox_ready']}")
        print(f"Dry Run Ready                : {sandbox['dry_run_ready']}")
        print(f"Real Execution Ready         : {sandbox['real_execution_ready']}")
        print(f"Allowed Commands             : {sandbox['allowed_command_count']}")
        print(f"Blocked Commands             : {sandbox['blocked_command_count']}")
        print(f"Blocked Patterns             : {sandbox['blocked_pattern_count']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")


    def safe_file_operation_status(self) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        status = manager.status()

        print("AURA Safe File Operation Planner Status")
        print("=======================================")
        print(f"Name                                  : {status['name']}")
        print(f"Version                               : {status['version']}")
        print(f"Status                                : {status['status']}")
        print(f"Planner Ready                         : {status['planner_ready']}")
        print(f"File Read Plan Ready                  : {status['file_read_plan_ready']}")
        print(f"File Write Plan Ready                 : {status['file_write_plan_ready']}")
        print(f"File Edit Plan Ready                  : {status['file_edit_plan_ready']}")
        print(f"Move/Copy/Delete Risk Review Ready    : {status['file_move_copy_delete_risk_review_ready']}")
        print(f"File Operation Checklist Ready        : {status['file_operation_checklist_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Local Task Integration                : {status['local_task_integration_ready']}")
        print(f"Workspace Awareness Integration       : {status['workspace_awareness_integration_ready']}")
        print(f"Workspace Memory Link Integration     : {status['workspace_memory_link_integration_ready']}")
        print(f"Tool Sandbox Integration              : {status['tool_sandbox_integration_ready']}")
        print(f"Tool Sandbox Dry Run Ready            : {status['tool_sandbox_dry_run_ready']}")
        print(f"Tool Sandbox Real Execution Ready     : {status['tool_sandbox_real_execution_ready']}")
        print(f"File Operation Types                  : {status['file_operation_types']}")
        print(f"Important File Count                  : {status['important_file_count']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print(f"Sections                              : {status['sections']}")
        print()
        print("Safety Boundary")
        print("---------------")
        print(f"Read Only                             : {status['read_only']}")
        print(f"Proposal Only                         : {status['proposal_only']}")
        print(f"Metadata Only                         : {status['metadata_only']}")
        print(f"File Read                             : {status['file_read']}")
        print(f"File Opened                           : {status['file_opened']}")
        print(f"File Write                            : {status['file_write']}")
        print(f"File Edit                             : {status['file_edit']}")
        print(f"File Delete                           : {status['file_delete']}")
        print(f"File Move                             : {status['file_move']}")
        print(f"File Copy                             : {status['file_copy']}")
        print(f"Command Execution                     : {status['command_execution']}")
        print(f"External Action Execution             : {status['external_action_execution']}")
        print(f"Real Tool Execution                   : {status['real_tool_execution']}")
        print()
        print(f"Project Root: {status['project_root']}")
        print(f"Note: {status['note']}")

    def print_safe_file_plan(self, title: str, plan: dict) -> None:
        print(title)
        print("=" * len(title))
        print(f"Status                                : {plan['status']}")
        print(f"Plan Type                             : {plan['plan_type']}")
        print(f"Target                                : {plan['target']}")
        print(f"Plan State                            : {plan['plan_state']}")
        print(f"Operation Risk                        : {plan['operation_risk']}")
        print(f"Operation Priority                    : {plan['operation_priority']}")
        print(f"File Tags                             : {', '.join(plan['file_tags'])}")
        print(f"Step Count                            : {plan['step_count']}")
        print(f"Checklist Count                       : {plan['checklist_count']}")
        print(f"Important File Count                  : {plan['important_file_count']}")
        print(f"Tool Sandbox Ready                    : {plan['tool_sandbox_ready']}")
        print(f"Tool Sandbox Dry Run Ready            : {plan['tool_sandbox_dry_run_ready']}")
        print(f"Tool Sandbox Real Execution Ready     : {plan['tool_sandbox_real_execution_ready']}")
        print(f"Execution Ready                       : {plan['execution_ready']}")
        print(f"Executed                              : {plan['executed']}")
        print(f"Read Only                             : {plan['read_only']}")
        print(f"Proposal Only                         : {plan['proposal_only']}")
        print(f"Metadata Only                         : {plan['metadata_only']}")
        print(f"File Read Performed                   : {plan['file_read_performed']}")
        print(f"File Opened                           : {plan['file_opened']}")
        print(f"File Write Performed                  : {plan['file_write_performed']}")
        print(f"File Edit Performed                   : {plan['file_edit_performed']}")
        print(f"File Delete Performed                 : {plan['file_delete_performed']}")
        print(f"File Move Performed                   : {plan['file_move_performed']}")
        print(f"File Copy Performed                   : {plan['file_copy_performed']}")
        print(f"Command Execution Performed           : {plan['command_execution_performed']}")
        print(f"External Action Performed             : {plan['external_action_execution_performed']}")
        print(f"Real Tool Execution Performed         : {plan['real_tool_execution_performed']}")
        print()
        print("Path Classification")
        print("-------------------")
        path_info = plan["path_classification"]
        print(f"Path Risk                             : {path_info['path_risk']}")
        print(f"Matched Important Files               : {path_info['matched_important_file_count']}")
        print(f"Path Traversal Detected               : {path_info['path_traversal_detected']}")
        print(f"Absolute Path Hint                    : {path_info['absolute_path_hint']}")
        print(f"Runtime Path Hint                     : {path_info['runtime_path_hint']}")
        if path_info["matched_important_files"]:
            print("Matched Files:")
            for item in path_info["matched_important_files"]:
                print(f"- {item}")
        print()
        print("Workspace Summary")
        print("-----------------")
        print(plan["workspace_summary"])
        print()
        print("Workspace Memory Summary")
        print("------------------------")
        print(plan["workspace_memory_summary"])
        print()
        print("Recommended Steps")
        print("-----------------")
        for index, step in enumerate(plan["recommended_steps"], start=1):
            print(f"{index}. {step['title']}")
            print(f"   Risk        : {step['risk']}")
            print(f"   Ready       : {step['ready']}")
            print(f"   Confirmation: {step['requires_confirmation']}")
            print(f"   Description : {step['description']}")
        print()
        print("Checklist")
        print("---------")
        for item in plan["checklist"]:
            print(f"- {item}")
        print()
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def safe_file_read_plan(self, target: str) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.print_safe_file_plan(
            "AURA Safe File Read Plan",
            manager.file_read_plan(target),
        )

    def safe_file_write_plan(self, target: str) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.print_safe_file_plan(
            "AURA Safe File Write Plan Proposal",
            manager.file_write_plan(target),
        )

    def safe_file_edit_plan(self, target: str) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.print_safe_file_plan(
            "AURA Safe File Edit Plan Proposal",
            manager.file_edit_plan(target),
        )

    def safe_file_move_copy_delete_risk_review(self, target: str) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.print_safe_file_plan(
            "AURA Safe File Move/Copy/Delete Risk Review",
            manager.file_move_copy_delete_risk_review(target),
        )

    def safe_file_operation_checklist(self, target: str) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        self.print_safe_file_plan(
            "AURA Safe File Operation Checklist",
            manager.file_operation_checklist(target),
        )

    def safe_file_operation_context(self) -> None:
        manager = SafeFileOperationPlannerManager(project_root=self.project_root)
        context = manager.context()

        print("AURA Safe File Operation Planner Context")
        print("========================================")
        print(f"Status                                : {context['status']}")
        print(f"Context Ready                         : {context['context_ready']}")
        print(f"Read Only                             : {context['read_only']}")
        print(f"Proposal Only                         : {context['proposal_only']}")
        print(f"Metadata Only                         : {context['metadata_only']}")
        print(f"Write Performed                       : {context['write_performed']}")
        print(f"File Read Performed                   : {context['file_read_performed']}")
        print(f"File Opened                           : {context['file_opened']}")
        print(f"File Write Performed                  : {context['file_write_performed']}")
        print(f"File Edit Performed                   : {context['file_edit_performed']}")
        print(f"File Delete Performed                 : {context['file_delete_performed']}")
        print(f"File Move Performed                   : {context['file_move_performed']}")
        print(f"File Copy Performed                   : {context['file_copy_performed']}")
        print(f"Command Execution Performed           : {context['command_execution_performed']}")
        print(f"External Action Performed             : {context['external_action_execution_performed']}")
        print(f"Real Tool Execution Performed         : {context['real_tool_execution_performed']}")
        print()
        print("Planner Status")
        print("--------------")
        status = context["planner_status"]
        print(f"Planner Ready                         : {status['planner_ready']}")
        print(f"File Read Plan Ready                  : {status['file_read_plan_ready']}")
        print(f"File Write Plan Ready                 : {status['file_write_plan_ready']}")
        print(f"File Edit Plan Ready                  : {status['file_edit_plan_ready']}")
        print(f"Move/Copy/Delete Risk Review Ready    : {status['file_move_copy_delete_risk_review_ready']}")
        print(f"File Operation Checklist Ready        : {status['file_operation_checklist_ready']}")
        print(f"Context Ready                         : {status['context_ready']}")
        print(f"Runtime Ready                         : {status['runtime_ready']}")
        print()
        print("Tool Sandbox")
        print("------------")
        sandbox = context["tool_sandbox_status"]
        print(f"Sandbox Ready                         : {sandbox['sandbox_ready']}")
        print(f"Dry Run Ready                         : {sandbox['dry_run_ready']}")
        print(f"Real Execution Ready                  : {sandbox['real_execution_ready']}")
        print(f"Allowed Commands                      : {sandbox['allowed_command_count']}")
        print(f"Blocked Commands                      : {sandbox['blocked_command_count']}")
        print(f"Blocked Patterns                      : {sandbox['blocked_pattern_count']}")
        print()
        print("Safe Current Capabilities")
        print("-------------------------")
        for item in context["safe_current_capabilities"]:
            print(f"- {item}")
        print()
        print("Disabled Capabilities")
        print("---------------------")
        for item in context["disabled_capabilities"]:
            print(f"- {item}")
        print()
        print(f"Note: {context['note']}")
