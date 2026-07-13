import os
from difflib import get_close_matches
from pathlib import Path

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
from aura.plugins.builtin.echo_plugin import EchoPlugin
from aura.plugins.builtin.memory_plugin import MemoryPlugin
from aura.plugins.plugin_manager import PluginManager
from aura.codebase_change.codebase_change_planner_manager import CodebaseChangePlannerManager
from aura.codebase_patch_proposal.codebase_patch_proposal_renderer_manager import CodebasePatchProposalRendererManager
from aura.codebase_validation_gate.codebase_validation_gate_planner_manager import CodebaseValidationGatePlannerManager
from aura.voice_conversation.voice_conversation_planner_manager import VoiceConversationPlannerManager
from aura.vision_context.vision_context_planner_manager import VisionContextPlannerManager
from aura.avatar_interaction.avatar_interaction_planner_manager import AvatarInteractionPlannerManager
from aura.desktop_workflow.desktop_workflow_planner_manager import DesktopWorkflowPlannerManager
from aura.partner_runtime.partner_runtime_planning_manager import PartnerRuntimePlanningManager
from aura.partner_runtime.partner_runtime_alpha_manager import PartnerRuntimeAlphaManager
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


class AuraShell:
    """
    Interactive shell for AURA Genesis.
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"
        self.settings_path = self.project_root / "aura" / "config" / "settings.yaml"

        self.memory_store = MemoryStore(project_root=self.project_root)
        self.chat_engine = AuraChat(project_root=self.project_root)
        self.plugin_manager = PluginManager()
        self.plugins_loaded = False
        self.running = True

    def known_commands(self) -> list[str]:
        return [
            "help",
            "remember",
            "recall",
            "mem",
            "memory",
            "daily-briefing-status",
            "daily-briefing",
            "daily-briefing-compact",
            "daily-briefing-context",
            "memory-reflection-status",
            "memory-reflect",
            "memory-insights",
            "memory-reflection-context",
            "memory-count",
            "mem-count",
            "memory-list",
            "mem-list",
            "memory-search",
            "mem-search",
            "chat",
            "ask",
            "history",
            "status",
            "version",
            "provider",
            "tool-sandbox-status",
            "tool-sandbox-policy",
            "tool-sandbox-check",
            "tool-sandbox-dry-run",
            "model-router-status",
            "model-router-routes",
            "model-router-select",
            "core-loop-status",
            "core-loop-run",
            "core-loop-trace",
            "avatar-runtime-alpha-status",
            "avatar-expression-plan",
            "avatar-gesture-plan",
            "avatar-runtime-context",
            "avatar-status",
            "avatar-providers",
            "avatar-state",
            "avatar-expression",
            "avatar-gesture",
            "desktop-alpha-status",
            "desktop-action-plan",
            "desktop-open-app-plan",
            "desktop-open-browser-plan",
            "desktop-open-file-plan",
            "desktop-workspace-context",
            "desktop-status",
            "desktop-capabilities",
            "desktop-action",
            "system-status",
            "status-full",
            "vision-runtime-alpha-status",
            "vision-screen-plan",
            "vision-camera-plan",
            "vision-runtime-context",
            "vision-runtime-status",
            "vision-runtime-plan",
            "vision-runtime-check",
            "active-permission-runtime-alpha-status",
            "active-permission-runtime-status",
            "active-permission-runtime-check",
            "vision-status",
            "vision-providers",
            "safe-file-operation-status",
            "safe-file-read-plan",
            "safe-file-write-plan",
            "safe-file-edit-plan",
            "safe-file-move-copy-delete-risk-review",
            "safe-file-operation-checklist",
            "safe-file-operation-context",
            "local-task-planner-status",
            "local-task-intent-plan",
            "local-task-breakdown-plan",
            "local-task-risk-review",
            "local-task-execution-checklist",
            "local-task-context",
            "creative-assistant-status",
            "creative-brief-plan",
            "creative-character-concept-plan",
            "creative-visual-asset-plan",
            "creative-content-idea-plan",
            "creative-review-plan",
            "creative-context",
            "project-intent-status",
            "project-intent-summary",
            "project-goal-plan",
            "sprint-intent-plan",
            "project-next-action-candidates",
            "project-intent-context",
            "workspace-memory-link-status",
            "workspace-memory-summary",
            "workspace-memory-candidates",
            "workspace-file-memory-candidates",
            "workspace-milestone-memory-candidates",
            "workspace-memory-link-context",
            "streaming-safety-status",
            "streaming-context-plan",
            "streaming-chat-safety-plan",
            "streaming-content-boundary-plan",
            "streaming-privacy-plan",
            "streaming-moderation-plan",
            "streaming-safety-context",
            "game-companion-status",
            "game-session-plan",
            "game-strategy-plan",
            "game-streaming-plan",
            "game-coaching-plan",
            "game-context",
            "expression-language-status",
            "expression-state",
            "expression-plan",
            "expression-voice-hint",
            "expression-avatar-hint",
            "expression-gesture-hint",
            "expression-context",
            "media-understanding-status",
            "media-asset-summary",
            "media-image-plan",
            "media-texture-reference-plan",
            "media-thumbnail-review-plan",
            "media-video-plan",
            "media-context",
            "blender-bridge-status",
            "blender-scene-plan",
            "blender-asset-plan",
            "blender-texture-plan",
            "blender-rigging-plan",
            "blender-animation-plan",
            "blender-context",
            "workspace-status",
            "workspace-awareness-status",
            "workspace-map",
            "workspace-context",
            "workspace-current-state",
            "workspace-important-files",
            "partner-alpha-status",
            "partner-context",
            "partner-readiness",
            "partner-next-step",
            "awakening-status",
            "awaken",
            "voice-runtime-alpha-status",
            "voice-speak-plan",
            "voice-speak-test",
            "voice-runtime-context",
            "voice-runtime-status",
            "voice-runtime-plan",
            "voice-runtime-check",
            "voice-status",
            "voice-providers",
            "project-code-status",
            "project-code-map",
            "project-code-inspect",
            "project-code-plan",
            "project-code-safety",
            "project-map",
            "project-inspect",
            "project-find",
            "project-summary",
            "project-files",
            "project-read",
            "action-request",
            "action-request-check",
            "plugin-actions",
            "plugin-action",
            "plugin-action-check",
            "skills",
            "skill",
            "skill-check",
            "permissions",
            "permission-check",
            "perm-check",
            "context",
            "context-preview",
            "roles",
            "journal",
            "journal-add",
            "journal-count",
            "reason",
            "provider-check",
            "reason-check",
            "plugins",
            "plugin",
            "health",
            "clear",
            "cls",
            "exit",
            "quit",
            "q",
        ]

    def suggest_command(self, command: str) -> str | None:
        base_command = command.strip().split()[0].lower()

        matches = get_close_matches(
            base_command,
            self.known_commands(),
            n=1,
            cutoff=0.7,
        )

        if not matches:
            return None

        return matches[0]

    def print_banner(self) -> None:
        print("AURA Interactive Shell")
        print("======================")
        print("Type 'help' to see available commands.")
        print("Type 'exit' to leave.")
        print()

    def print_help(self) -> None:
        print("Available commands:")
        print("  help                 Show this help message")
        print("  voice-input-status Show Voice Input Runtime Foundation status")
        print("  voice-intent-status Show Voice Intent Understanding status")
        print("  voice-transcript-normalization-plan <target> Prepare transcript normalization plan")
        print("  voice-intent-classification-plan <target> Prepare voice intent classification plan")
        print("  voice-entity-slot-plan <target> Prepare entity/slot plan")
        print("  voice-clarification-plan <target> Prepare clarification plan")
        print("  voice-action-gate-plan <target> Prepare voice action gate plan")
        print("  voice-response-plan <target> Prepare voice response plan")
        print("  voice-intent-safety-plan <target> Prepare voice intent safety plan")
        print("  voice-intent-context Show Voice Intent Understanding context")
        print("  vision-input-status Show Vision Input Runtime Foundation status")
        print("  vision-input-permission-plan <target> Prepare visual permission plan")
        print("  visual-capture-boundary-plan <target> Prepare visual capture boundary plan")
        print("  image-input-adapter-plan <target> Prepare image input adapter plan")
        print("  visual-source-plan <target> Prepare visual source plan")
        print("  visual-session-plan <target> Prepare visual session plan")
        print("  visual-action-gate-plan <target> Prepare visual action gate plan")
        print("  vision-input-safety-plan <target> Prepare vision input safety plan")
        print("  vision-input-context Show Vision Input Runtime Foundation context")
        print("  visual-context-status Show Visual Context Understanding status")
        print("  visual-scene-understanding-plan <target> Prepare scene understanding plan")
        print("  visual-object-relation-plan <target> Prepare object/relation plan")
        print("  visual-text-context-plan <target> Prepare text-in-image context plan")
        print("  visual-uncertainty-plan <target> Prepare visual uncertainty plan")
        print("  visual-clarification-plan <target> Prepare visual clarification plan")
        print("  visual-response-context-plan <target> Prepare visual response context plan")
        print("  visual-context-safety-plan <target> Prepare visual context safety plan")
        print("  visual-context Show Visual Context Understanding context")
        print("  coder-project-status Show Coder Project Generation Planner status")
        print("  project-request-frame-plan <target> Prepare project request frame plan")
        print("  project-structure-plan <target> Prepare project structure plan")
        print("  code-file-blueprint-plan <target> Prepare code file blueprint plan")
        print("  dependency-plan <target> Prepare dependency plan")
        print("  generation-review-gate-plan <target> Prepare generation review gate plan")
        print("  validation-strategy-plan <target> Prepare validation strategy plan")
        print("  project-generation-safety-plan <target> Prepare project generation safety plan")
        print("  coder-project-context Show Coder Project Generation Planner context")
        print("  dependency-permission-status Show Dependency Download Permission Gate status")
        print("  dependency-request-review-plan <target> Prepare dependency request review plan")
        print("  package-source-review-plan <target> Prepare package/source review plan")
        print("  download-permission-plan <target> Prepare download permission plan")
        print("  install-command-review-plan <target> Prepare install command review plan")
        print("  dependency-risk-plan <target> Prepare dependency risk plan")
        print("  offline-alternative-plan <target> Prepare offline alternative plan")
        print("  dependency-permission-safety-plan <target> Prepare dependency permission safety plan")
        print("  dependency-permission-context Show Dependency Download Permission Gate context")
        print("  checkpoint-80-status Show Sprint 71-80 Review & Stabilization status")
        print("  completed-feature-review-plan <target> Prepare completed feature review plan")
        print("  active-foundation-review-plan <target> Prepare active/foundation review plan")
        print("  safety-boundary-review-plan <target> Prepare safety boundary review plan")
        print("  stabilization-validation-plan <target> Prepare stabilization validation plan")
        print("  technical-debt-review-plan <target> Prepare technical debt review plan")
        print("  roadmap-gap-review-plan <target> Prepare roadmap gap review plan")
        print("  next-block-planning-plan <target> Prepare next block planning plan")
        print("  checkpoint-80-context Show Sprint 71-80 checkpoint context")
        print("  output-formatter-status Show Shared Output Formatter status")
        print("  packet-render-plan <target> Prepare shared packet render plan")
        print("  safety-boundary-render-plan <target> Prepare safety boundary render plan")
        print("  cli-output-format-plan <target> Prepare CLI output format plan")
        print("  shell-output-format-plan <target> Prepare shell output format plan")
        print("  console-output-format-plan <target> Prepare future console output format plan")
        print("  ui-output-contract-plan <target> Prepare future UI output contract plan")
        print("  formatter-migration-plan <target> Prepare formatter migration plan")
        print("  output-formatter-context Show Shared Output Formatter context")
        print("  capability-registry-status Show Capability Registry status")
        print("  capability-catalog-plan <target> Prepare capability catalog plan")
        print("  capability-state-review-plan <target> Prepare capability state review plan")
        print("  permission-requirement-review-plan <target> Prepare permission requirement review plan")
        print("  risk-level-review-plan <target> Prepare risk level review plan")
        print("  control-center-capability-view-plan <target> Prepare Control Center capability view plan")
        print("  capability-gap-review-plan <target> Prepare capability gap review plan")
        print("  capability-registry-migration-plan <target> Prepare capability registry migration plan")
        print("  capability-registry-context Show Capability Registry context")
        print("  permission-workflow-status Show Unified Permission Workflow status")
        print("  permission-request-plan <target> Prepare permission request plan")
        print("  permission-state-transition-plan <target> Prepare permission state transition plan")
        print("  permission-risk-review-plan <target> Prepare permission risk review plan")
        print("  confirmation-prompt-plan <target> Prepare confirmation prompt plan")
        print("  permission-audit-trail-plan <target> Prepare permission audit trail plan")
        print("  control-center-permission-view-plan <target> Prepare Control Center permission view plan")
        print("  permission-policy-gap-review-plan <target> Prepare permission policy gap review plan")
        print("  permission-workflow-context Show Unified Permission Workflow context")
        print("  runtime-service-status Show Runtime Service Foundation status")
        print("  safe-idle-boot-plan <target> Prepare safe_idle boot plan")
        print("  service-lifecycle-plan <target> Prepare service lifecycle plan")
        print("  service-health-check-plan <target> Prepare service health check plan")
        print("  systemd-unit-blueprint-plan <target> Prepare systemd unit blueprint plan")
        print("  service-recovery-plan <target> Prepare service recovery plan")
        print("  service-monitor-view-plan <target> Prepare service monitor view plan")
        print("  auto-boot-policy-plan <target> Prepare auto-boot policy plan")
        print("  runtime-service-context Show Runtime Service Foundation context")
        print("  launcher-monitor-status Show Launcher & Health Monitor Foundation status")
        print("  launcher-start-plan <target> Prepare launcher start plan")
        print("  launcher-stop-plan <target> Prepare launcher stop plan")
        print("  launcher-restart-plan <target> Prepare launcher restart plan")
        print("  launcher-status-plan <target> Prepare launcher status plan")
        print("  launcher-log-view-plan <target> Prepare launcher log view plan")
        print("  health-monitor-plan <target> Prepare health monitor plan")
        print("  control-center-service-monitor-plan <target> Prepare Control Center service monitor plan")
        print("  launcher-safety-policy-plan <target> Prepare launcher safety policy plan")
        print("  launcher-health-context Show Launcher & Health Monitor Foundation context")
        print("  control-center-status Show Control Center UI Blueprint status")
        print("  dashboard-layout-blueprint-plan <target> Prepare dashboard layout blueprint plan")
        print("  permission-center-blueprint-plan <target> Prepare Permission Center blueprint plan")
        print("  service-monitor-blueprint-plan <target> Prepare Service Monitor blueprint plan")
        print("  capability-viewer-blueprint-plan <target> Prepare Capability Viewer blueprint plan")
        print("  launcher-control-blueprint-plan <target> Prepare Launcher Control blueprint plan")
        print("  chat-console-placeholder-plan <target> Prepare Chat Console placeholder plan")
        print("  plugin-dashboard-blueprint-plan <target> Prepare Plugin Dashboard blueprint plan")
        print("  action-log-blueprint-plan <target> Prepare Action Log blueprint plan")
        print("  control-center-safety-policy-plan <target> Prepare Control Center safety policy plan")
        print("  control-center-context Show Control Center UI Blueprint context")
        print("  local-console-web-status Show Local Console Web Foundation status")
        print("  local-host-policy-plan <target> Prepare local host policy plan")
        print("  route-blueprint-plan <target> Prepare route blueprint plan")
        print("  api-contract-blueprint-plan <target> Prepare API contract blueprint plan")
        print("  static-asset-blueprint-plan <target> Prepare static asset blueprint plan")
        print("  session-state-blueprint-plan <target> Prepare session state blueprint plan")
        print("  security-boundary-plan <target> Prepare local console security boundary plan")
        print("  control-center-web-bridge-plan <target> Prepare Control Center web bridge plan")
        print("  developer-console-access-plan <target> Prepare developer console access plan")
        print("  local-console-web-context Show Local Console Web Foundation context")
        print("  chat-bridge-status Show Chat Bridge & Session State Foundation status")
        print("  conversation-session-blueprint-plan <target> Prepare conversation session blueprint plan")
        print("  message-flow-blueprint-plan <target> Prepare message flow blueprint plan")
        print("  control-center-chat-panel-bridge-plan <target> Prepare Control Center chat panel bridge plan")
        print("  local-console-session-contract-plan <target> Prepare Local Console session contract plan")
        print("  permission-aware-chat-action-boundary-plan <target> Prepare permission-aware chat action boundary plan")
        print("  chat-context-persistence-blueprint-plan <target> Prepare chat context persistence blueprint plan")
        print("  websocket-boundary-plan <target> Prepare websocket boundary plan")
        print("  session-recovery-blueprint-plan <target> Prepare session recovery blueprint plan")
        print("  chat-bridge-safety-policy-plan <target> Prepare chat bridge safety policy plan")
        print("  chat-bridge-context Show Chat Bridge & Session State Foundation context")
        print("  plugin-permission-dashboard-status Show Plugin / Permission Dashboard Foundation status")
        print("  plugin-registry-dashboard-plan <target> Prepare plugin registry dashboard plan")
        print("  permission-request-dashboard-plan <target> Prepare permission request dashboard plan")
        print("  permission-decision-visibility-plan <target> Prepare permission decision visibility plan")
        print("  chat-originated-action-visibility-plan <target> Prepare chat-originated action visibility plan")
        print("  capability-permission-matrix-plan <target> Prepare capability permission matrix plan")
        print("  control-center-dashboard-bridge-plan <target> Prepare Control Center dashboard bridge plan")
        print("  local-console-dashboard-contract-plan <target> Prepare Local Console dashboard contract plan")
        print("  audit-trail-dashboard-blueprint-plan <target> Prepare audit trail dashboard blueprint plan")
        print("  dashboard-safety-policy-plan <target> Prepare dashboard safety policy plan")
        print("  plugin-permission-dashboard-context Show Plugin / Permission Dashboard Foundation context")
        print("  local-console-static-prototype-status Show Local Console Static Prototype Foundation status")
        print("  static-prototype-structure-plan <target> Prepare static prototype structure plan")
        print("  static-page-blueprint-plan <target> Prepare static page blueprint plan")
        print("  static-asset-blueprint-plan <target> Prepare static asset blueprint plan")
        print("  panel-layout-blueprint-plan <target> Prepare panel layout blueprint plan")
        print("  route-static-mapping-plan <target> Prepare route static mapping plan")
        print("  data-placeholder-contract-plan <target> Prepare data placeholder contract plan")
        print("  theme-token-blueprint-plan <target> Prepare theme token blueprint plan")
        print("  accessibility-blueprint-plan <target> Prepare accessibility blueprint plan")
        print("  static-prototype-safety-policy-plan <target> Prepare static prototype safety policy plan")
        print("  local-console-static-prototype-context Show Local Console Static Prototype Foundation context")
        print("  local-console-api-schema-status Show Local Console API Schema Foundation status")
        print("  api-schema-catalog-plan <target> Prepare Local Console API schema catalog plan")
        print("  endpoint-blueprint-plan <target> Prepare endpoint blueprint plan")
        print("  response-envelope-plan <target> Prepare response envelope plan")
        print("  request-schema-blueprint-plan <target> Prepare request schema blueprint plan")
        print("  validation-rule-plan <target> Prepare validation rule plan")
        print("  permission-boundary-schema-plan <target> Prepare permission boundary schema plan")
        print("  error-contract-plan <target> Prepare error contract plan")
        print("  schema-versioning-plan <target> Prepare schema versioning plan")
        print("  api-schema-safety-policy-plan <target> Prepare API schema safety policy plan")
        print("  local-console-api-schema-context Show Local Console API Schema Foundation context")
        print("  control-center-data-aggregator-status Show Control Center Data Aggregator Foundation status")
        print("  aggregator-packet-catalog-plan <target> Prepare aggregator packet catalog plan")
        print("  atlas-core-packet-plan <target> Prepare ATLAS core packet plan")
        print("  orion-client-packet-plan <target> Prepare ORION client packet plan")
        print("  client-bridge-packet-plan <target> Prepare client bridge packet plan")
        print("  dashboard-view-packet-plan <target> Prepare dashboard view packet plan")
        print("  permission-scope-packet-plan <target> Prepare permission scope packet plan")
        print("  health-snapshot-packet-plan <target> Prepare health snapshot packet plan")
        print("  audit-event-visibility-packet-plan <target> Prepare audit event visibility packet plan")
        print("  data-aggregator-safety-policy-plan <target> Prepare data aggregator safety policy plan")
        print("  control-center-data-aggregator-context Show Control Center Data Aggregator Foundation context")
        print("  permission-request-review-queue-status Show Permission Request Review Queue Foundation status")
        print("  permission-request-blueprint-plan <target> Prepare permission request blueprint plan")
        print("  queue-state-blueprint-plan <target> Prepare queue state blueprint plan")
        print("  review-packet-field-plan <target> Prepare review packet field plan")
        print("  permission-scope-boundary-plan <target> Prepare permission scope boundary plan")
        print("  decision-proposal-contract-plan <target> Prepare decision proposal contract plan")
        print("  reviewer-checklist-plan <target> Prepare reviewer checklist plan")
        print("  audit-visibility-field-plan <target> Prepare audit visibility field plan")
        print("  permission-request-safety-policy-plan <target> Prepare permission request safety policy plan")
        print("  permission-request-review-queue-status-packet Show Permission Request Review Queue status packet")
        print("  permission-request-review-queue-context Show Permission Request Review Queue Foundation context")
        print("  chat-session-persistence-planner-status Show Chat Session Persistence Planner Foundation status")
        print("  session-record-blueprint-plan <target> Prepare session record blueprint plan")
        print("  storage-boundary-blueprint-plan <target> Prepare storage boundary blueprint plan")
        print("  retention-policy-blueprint-plan <target> Prepare retention policy blueprint plan")
        print("  privacy-redaction-rule-plan <target> Prepare privacy redaction rule plan")
        print("  session-lifecycle-blueprint-plan <target> Prepare session lifecycle blueprint plan")
        print("  recovery-index-blueprint-plan <target> Prepare recovery index blueprint plan")
        print("  export-migration-note-plan <target> Prepare export and migration note plan")
        print("  chat-persistence-safety-policy-plan <target> Prepare chat persistence safety policy plan")
        print("  chat-session-persistence-status-packet Show Chat Session Persistence status packet")
        print("  chat-session-persistence-context Show Chat Session Persistence Planner Foundation context")
        print("  safe-local-web-runtime-gate-status Show Safe Local Web Runtime Gate Foundation status")
        print("  localhost-binding-policy-plan <target> Prepare localhost binding policy plan")
        print("  port-policy-plan <target> Prepare port policy plan")
        print("  web-runtime-permission-requirement-plan <target> Prepare web runtime permission requirement plan")
        print("  runtime-preflight-check-plan <target> Prepare runtime preflight check plan")
        print("  start-stop-proposal-contract-plan <target> Prepare start/stop proposal contract plan")
        print("  route-boundary-policy-plan <target> Prepare route boundary policy plan")
        print("  static-asset-boundary-policy-plan <target> Prepare static asset boundary policy plan")
        print("  kill-switch-policy-plan <target> Prepare kill switch policy plan")
        print("  web-runtime-audit-visibility-plan <target> Prepare web runtime audit visibility plan")
        print("  safe-local-web-runtime-gate-safety-policy-plan <target> Prepare safe local web runtime gate safety policy plan")
        print("  safe-local-web-runtime-gate-context Show Safe Local Web Runtime Gate Foundation context")
        print("  controlled-file-write-approval-draft-status Show Controlled File Write Approval Draft Foundation status")
        print("  file-write-proposal-draft-plan <target> Prepare file write proposal draft plan")
        print("  target-path-policy-plan <target> Prepare target path policy plan")
        print("  diff-preview-contract-plan <target> Prepare diff preview contract plan")
        print("  overwrite-rule-plan <target> Prepare overwrite rule plan")
        print("  backup-requirement-plan <target> Prepare backup requirement plan")
        print("  approval-checklist-plan <target> Prepare approval checklist plan")
        print("  rollback-note-plan <target> Prepare rollback note plan")
        print("  file-write-audit-visibility-plan <target> Prepare file write audit visibility plan")
        print("  file-write-safety-policy-plan <target> Prepare file write safety policy plan")
        print("  controlled-file-write-approval-draft-context Show Controlled File Write Approval Draft Foundation context")
        print("  runtime-action-queue-review-layer-status Show Runtime Action Queue Review Layer Foundation status")
        print("  action-queue-item-blueprint-plan <target> Prepare action queue item blueprint plan")
        print("  queue-state-blueprint-plan <target> Prepare queue state blueprint plan")
        print("  review-priority-rule-plan <target> Prepare review priority rule plan")
        print("  dependency-blocker-contract-plan <target> Prepare dependency/blocker contract plan")
        print("  permission-link-requirement-plan <target> Prepare permission link requirement plan")
        print("  execution-preflight-check-blueprint-plan <target> Prepare execution preflight check blueprint plan")
        print("  approval-denial-transition-rule-plan <target> Prepare approval/denial transition rule plan")
        print("  timeout-expiry-policy-plan <target> Prepare timeout/expiry policy plan")
        print("  runtime-action-audit-visibility-plan <target> Prepare runtime action audit visibility plan")
        print("  runtime-action-queue-review-layer-safety-policy-plan <target> Prepare runtime action queue review layer safety policy plan")
        print("  runtime-action-queue-review-layer-context Show Runtime Action Queue Review Layer Foundation context")
        print("  pre-runtime-security-audit-status Show Pre-Runtime Security Audit Foundation status")
        print("  security-audit-domain-plan <target> Prepare security audit domain plan")
        print("  runtime-gate-check-plan <target> Prepare runtime gate check plan")
        print("  permission-boundary-check-plan <target> Prepare permission boundary check plan")
        print("  file-system-safety-check-plan <target> Prepare file system safety check plan")
        print("  network-surface-check-plan <target> Prepare network surface check plan")
        print("  action-execution-safety-check-plan <target> Prepare action execution safety check plan")
        print("  orion-boundary-check-plan <target> Prepare ORION boundary check plan")
        print("  audit-visibility-check-plan <target> Prepare audit visibility check plan")
        print("  stabilization-readiness-check-plan <target> Prepare stabilization readiness check plan")
        print("  pre-runtime-security-audit-safety-policy-plan <target> Prepare pre-runtime security audit safety policy plan")
        print("  pre-runtime-security-audit-context Show Pre-Runtime Security Audit Foundation context")
        print("  sprint-100-review-stabilization-status Show Sprint 100 Review & Stabilization Foundation status")
        print("  sprint-block-review-plan <target> Prepare Sprint 91-100 block review plan")
        print("  completed-feature-inventory-plan <target> Prepare completed feature inventory plan")
        print("  active-vs-foundation-boundary-plan <target> Prepare active vs foundation-only boundary plan")
        print("  runtime-zero-safety-check-plan <target> Prepare runtime-zero safety check plan")
        print("  capability-registry-stabilization-plan <target> Prepare capability registry stabilization plan")
        print("  documentation-stabilization-plan <target> Prepare documentation stabilization plan")
        print("  unresolved-future-feature-plan <target> Prepare unresolved future feature plan")
        print("  roadmap-101-110-seed-plan <target> Prepare roadmap 101-110 seed plan")
        print("  sprint-100-release-readiness-plan <target> Prepare Sprint 100 release readiness plan")
        print("  sprint-100-review-stabilization-safety-policy-plan <target> Prepare Sprint 100 review stabilization safety policy plan")
        print("  sprint-100-review-stabilization-context Show Sprint 100 Review & Stabilization Foundation context")
        print("  genesis-runtime-readiness-baseline-status Show Genesis Runtime Readiness Baseline Foundation status")
        print("  readiness-domain-inventory-plan <target> Prepare readiness domain inventory plan")
        print("  runtime-candidate-classification-plan <target> Prepare runtime candidate classification plan")
        print("  dry-run-prerequisite-plan <target> Prepare dry-run prerequisite plan")
        print("  permission-requirement-matrix-plan <target> Prepare permission requirement matrix plan")
        print("  safety-gate-alignment-plan <target> Prepare safety gate alignment plan")
        print("  rollback-and-kill-switch-readiness-plan <target> Prepare rollback and kill-switch readiness plan")
        print("  audit-and-observability-readiness-plan <target> Prepare audit and observability readiness plan")
        print("  rollout-phase-recommendation-plan <target> Prepare rollout phase recommendation plan")
        print("  block-101-110-alignment-plan <target> Prepare Sprint 101-110 block alignment plan")
        print("  genesis-runtime-readiness-baseline-safety-policy-plan <target> Prepare Genesis runtime readiness baseline safety policy plan")
        print("  genesis-runtime-readiness-baseline-context Show Genesis Runtime Readiness Baseline Foundation context")
        print("  safe-runtime-configuration-profile-status Show Safe Runtime Configuration Profile Foundation status")
        print("  configuration-profile-type-plan <target> Prepare configuration profile type plan")
        print("  runtime-mode-policy-plan <target> Prepare runtime mode policy plan")
        print("  service-configuration-boundary-plan <target> Prepare service configuration boundary plan")
        print("  permission-configuration-boundary-plan <target> Prepare permission configuration boundary plan")
        print("  file-system-configuration-boundary-plan <target> Prepare file system configuration boundary plan")
        print("  network-configuration-boundary-plan <target> Prepare network configuration boundary plan")
        print("  dry-run-configuration-requirement-plan <target> Prepare dry-run configuration requirement plan")
        print("  rollout-configuration-guard-plan <target> Prepare rollout configuration guard plan")
        print("  configuration-audit-visibility-plan <target> Prepare configuration audit visibility plan")
        print("  safe-runtime-configuration-profile-safety-policy-plan <target> Prepare Safe Runtime Configuration Profile safety policy plan")
        print("  safe-runtime-configuration-profile-context Show Safe Runtime Configuration Profile Foundation context")
        print("  local-service-start-proposal-review-status Show Local Service Start Proposal Review Foundation status")
        print("  service-start-candidate-inventory-plan <target> Prepare service start candidate inventory plan")
        print("  service-start-preflight-requirement-plan <target> Prepare service start preflight requirement plan")
        print("  port-binding-review-plan <target> Prepare port binding review plan")
        print("  process-launch-boundary-plan <target> Prepare process launch boundary plan")
        print("  permission-requirement-plan <target> Prepare permission requirement plan")
        print("  risk-classification-plan <target> Prepare risk classification plan")
        print("  rollback-kill-switch-plan <target> Prepare rollback kill-switch plan")
        print("  audit-event-plan <target> Prepare audit event plan")
        print("  user-approval-decision-plan <target> Prepare user approval decision plan")
        print("  local-service-start-pro Prepare audit event plan")
        print("  user-approval-decision-plan <target> Prepare user approval decision plan")
        print("  local-service-start-proposal-review-context Show Local Service Start Proposal Review context")
        print("  dashboard-api-contract-consolidation-status Show Dashboard API Contract Consolidation Foundation status")
        print("  api-contract-inventory-plan <target> Prepare API contract inventory plan")
        print("  endpoint-schema-alignment-plan <target> Prepare endpoint schema alignment plan")
        print("  request-response-contract-plan <target> Prepare request/response contract plan")
        print("  permission-contract-mapping-plan <target> Prepare permission contract mapping plan")
        print("  dashboard-status-payload-plan <target> Prepare dashboard status payload plan")
        print("  error-response-contract-plan <target> Prepare error response contract plan")
        print("  mock-api-boundary-plan <target> Prepare mock API boundary plan")
        print("  frontend-backend-contract-boundary-plan <target> Prepare frontend/backend contract boundary plan")
        print("  contract-validation-checklist-plan <target> Prepare contract validation checklist plan")
        print("  dashboard-api-contract-consolidation-context Show Dashboard API Contract Consolidation context")
        print("  permission-decision-runtime-dry-run-status Show Permission Decision Runtime Dry-Run Foundation status")
        print("  permission-decision-candidate-inventory-plan <target> Prepare permission decision candidate inventory plan")
        print("  permission-decision-input-contract-plan <target> Prepare permission decision input contract plan")
        print("  permission-decision-dry-run-evaluation-plan <target> Prepare permission decision dry-run evaluation plan")
        print("  permission-scope-mapping-plan <target> Prepare permission scope mapping plan")
        print("  approval-denial-outcome-plan <target> Prepare approval/denial outcome plan")
        print("  permission-risk-review-rule-plan <target> Prepare permission risk review rule plan")
        print("  permission-audit-record-blueprint-plan <target> Prepare permission audit record blueprint plan")
        print("  permission-dashboard-review-payload-plan <target> Prepare permission dashboard review payload plan")
        print("  permission-dry-run-safety-boundary-plan <target> Prepare permission dry-run safety boundary plan")
        print("  permission-decision-runtime-dry-run-context Show Permission Decision Runtime Dry-Run context")
        print("  runtime-action-execution-preview-packet-status Show Runtime Action Execution Preview Packet Foundation status")
        print("  action-candidate-inventory-plan <target> Prepare action candidate inventory plan")
        print("  execution-preflight-checklist-plan <target> Prepare execution preflight checklist plan")
        print("  action-input-snapshot-plan <target> Prepare action input snapshot plan")
        print("  permission-decision-reference-plan <target> Prepare permission decision reference plan")
        print("  execution-step-preview-plan <target> Prepare execution step preview plan")
        print("  side-effect-boundary-plan <target> Prepare side effect boundary plan")
        print("  rollback-preview-plan <target> Prepare rollback preview plan")
        print("  audit-preview-record-plan <target> Prepare audit preview record plan")
        print("  user-confirmation-packet-plan <target> Prepare user confirmation packet plan")
        print("  runtime-action-execution-preview-packet-context Show Runtime Action Execution Preview Packet context")
        print("  local-runtime-execution-gate-dry-run-status Show Local Runtime Execution Gate Dry-Run Foundation status")
        print("  execution-gate-candidate-inventory-plan <target> Prepare execution gate candidate inventory plan")
        print("  runtime-gate-input-contract-plan <target> Prepare runtime gate input contract plan")
        print("  gate-preflight-evaluation-plan <target> Prepare gate preflight evaluation plan")
        print("  safe-runtime-profile-reference-plan <target> Prepare safe runtime profile reference plan")
        print("  permission-gate-reference-plan <target> Prepare permission gate reference plan")
        print("  execution-gate-decision-plan <target> Prepare execution gate decision plan")
        print("  block-reason-catalog-plan <target> Prepare block reason catalog plan")
        print("  audit-gate-record-plan <target> Prepare audit gate record plan")
        print("  dashboard-gate-payload-plan <target> Prepare dashboard gate payload plan")
        print("  local-runtime-execution-gate-dry-run-context Show Local Runtime Execution Gate Dry-Run context")
        print("  runtime-audit-event-packet-preview-status Show Runtime Audit Event Packet Preview Foundation status")
        print("  audit-event-candidate-inventory-plan <target> Prepare audit event candidate inventory plan")
        print("  audit-event-input-snapshot-plan <target> Prepare audit event input snapshot plan")
        print("  runtime-reference-mapping-plan <target> Prepare runtime reference mapping plan")
        print("  permission-reference-mapping-plan <target> Prepare permission reference mapping plan")
        print("  action-preview-reference-plan <target> Prepare action preview reference plan")
        print("  audit-payload-shape-plan <target> Prepare audit payload shape plan")
        print("  audit-visibility-rule-plan <target> Prepare audit visibility rule plan")
        print("  retention-redaction-boundary-plan <target> Prepare retention redaction boundary plan")
        print("  dashboard-audit-packet-plan <target> Prepare dashboard audit packet plan")
        print("  runtime-audit-event-packet-preview-context Show Runtime Audit Event Packet Preview context")
        print("  runtime-safety-freeze-manual-approval-barrier-status Show Runtime Safety Freeze Manual Approval Barrier Foundation status")
        print("  safety-freeze-candidate-inventory-plan <target> Prepare safety freeze candidate inventory plan")
        print("  manual-approval-barrier-input-plan <target> Prepare manual approval barrier input plan")
        print("  freeze-condition-check-plan <target> Prepare freeze condition check plan")
        print("  approval-requirement-rule-plan <target> Prepare approval requirement rule plan")
        print("  blocked-runtime-catalog-plan <target> Prepare blocked runtime catalog plan")
        print("  user-confirmation-barrier-plan <target> Prepare user confirmation barrier plan")
        print("  emergency-stop-requirement-plan <target> Prepare emergency stop requirement plan")
        print("  audit-freeze-packet-preview-plan <target> Prepare audit freeze packet preview plan")
        print("  dashboard-barrier-payload-plan <target> Prepare dashboard barrier payload plan")
        print("  runtime-safety-freeze-manual-approval-barrier-context Show Runtime Safety Freeze Manual Approval Barrier context")
        print("  review-stabilization-101-110-status Show Sprint 101-110 Review Stabilization Foundation status")
        print("  sprint-completion-inventory-plan <target> Prepare sprint completion inventory plan")
        print("  runtime-readiness-foundation-audit-plan <target> Prepare runtime readiness foundation audit plan")
        print("  safety-invariant-verification-plan <target> Prepare safety invariant verification plan")
        print("  capability-registry-delta-review-plan <target> Prepare capability registry delta review plan")
        print("  integration-surface-review-plan <target> Prepare integration surface review plan")
        print("  documentation-roadmap-consistency-plan <target> Prepare documentation roadmap consistency plan")
        print("  checkpoint-risk-review-plan <target> Prepare checkpoint risk review plan")
        print("  deferred-runtime-boundary-plan <target> Prepare deferred runtime boundary plan")
        print("  next-block-readiness-plan <target> Prepare next block readiness plan")
        print("  review-stabilization-101-110-context Show Sprint 101-110 Review Stabilization context")
        print("  genesis-runtime-readiness-next-block-planning-status Show Genesis Runtime Readiness Next Block Planning Foundation status")
        print("  next-block-sprint-candidate-plan <target> Prepare next block sprint candidate plan")
        print("  runtime-readiness-continuity-plan <target> Prepare runtime readiness continuity plan")
        print("  manual-approval-evolution-plan <target> Prepare manual approval evolution plan")
        print("  audit-event-evolution-plan <target> Prepare audit event evolution plan")
        print("  dashboard-contract-evolution-plan <target> Prepare dashboard contract evolution plan")
        print("  orion-boundary-planning-plan <target> Prepare ORION boundary planning plan")
        print("  safe-local-action-boundary-plan <target> Prepare safe local action boundary plan")
        print("  integration-stabilization-plan <target> Prepare integration stabilization plan")
        print("  v1-readiness-mapping-plan <target> Prepare v1 readiness mapping plan")
        print("  genesis-runtime-readiness-next-block-planning-context Show Genesis Runtime Readiness Next Block Planning context")
        print("  runtime-permission-flow-consolidation-status Show Runtime Permission Flow Consolidation Foundation status")
        print("  permission-request-schema-consolidation-plan <target> Prepare permission request schema consolidation plan")
        print("  permission-decision-state-model-plan <target> Prepare permission decision state model plan")
        print("  manual-approval-checkpoint-plan <target> Prepare manual approval checkpoint plan")
        print("  denial-cancellation-flow-plan <target> Prepare denial cancellation flow plan")
        print("  permission-scope-boundary-plan <target> Prepare permission scope boundary plan")
        print("  high-risk-escalation-rule-plan <target> Prepare high risk escalation rule plan")
        print("  approval-audit-reference-plan <target> Prepare approval audit reference plan")
        print("  dashboard-permission-flow-payload-plan <target> Prepare dashboard permission flow payload plan")
        print("  future-runtime-grant-boundary-plan <target> Prepare future runtime grant boundary plan")
        print("  runtime-permission-flow-consolidation-context Show Runtime Permission Flow Consolidation context")
        print("  audit-event-review-queue-status Show Audit Event Review Queue Foundation status")
        print("  audit-event-intake-schema-plan <target> Prepare audit event intake schema plan")
        print("  review-queue-state-model-plan <target> Prepare review queue state model plan")
        print("  audit-event-triage-rule-plan <target> Prepare audit event triage rule plan")
        print("  permission-linkage-review-plan <target> Prepare permission linkage review plan")
        print("  runtime-boundary-review-plan <target> Prepare runtime boundary review plan")
        print("  redaction-visibility-review-plan <target> Prepare redaction visibility review plan")
        print("  dashboard-review-queue-payload-plan <target> Prepare dashboard review queue payload plan")
        print("  review-outcome-catalog-plan <target> Prepare review outcome catalog plan")
        print("  future-audit-writer-boundary-plan <target> Prepare future audit writer boundary plan")
        print("  audit-event-review-queue-context Show Audit Event Review Queue context")
        print("  dashboard-runtime-readiness-view-model-status Show Dashboard Runtime Readiness View Model Foundation status")
        print("  runtime-readiness-summary-view-plan <target> Prepare runtime readiness summary view plan")
        print("  permission-state-view-plan <target> Prepare permission state view plan")
        print("  audit-review-queue-view-plan <target> Prepare audit review queue view plan")
        print("  safety-boundary-view-plan <target> Prepare safety boundary view plan")
        print("  orion-boundary-view-plan <target> Prepare ORION boundary view plan")
        print("  action-preview-view-plan <target> Prepare action preview view plan")
        print("  manual-approval-view-plan <target> Prepare manual approval view plan")
        print("  v1-cutline-view-plan <target> Prepare v1 cutline view plan")
        print("  control-center-payload-view-plan <target> Prepare Control Center payload view plan")
        print("  dashboard-runtime-readiness-view-model-context Show Dashboard Runtime Readiness View Model context")
        print("  safe-local-action-contract-review-status Show Safe Local Action Contract Review Foundation status")
        print("  local-open-contract-review-plan <target> Prepare local open contract review plan")
        print("  controlled-create-contract-review-plan <target> Prepare controlled create contract review plan")
        print("  controlled-write-preview-contract-review-plan <target> Prepare controlled write preview contract review plan")
        print("  action-preview-packet-contract-plan <target> Prepare action preview packet contract plan")
        print("  permission-scope-contract-review-plan <target> Prepare permission scope contract review plan")
        print("  side-effect-boundary-contract-plan <target> Prepare side effect boundary contract plan")
        print("  rollback-cancel-contract-review-plan <target> Prepare rollback cancel contract review plan")
        print("  dashboard-contract-payload-plan <target> Prepare dashboard contract payload plan")
        print("  future-action-runtime-boundary-plan <target> Prepare future action runtime boundary plan")
        print("  safe-local-action-contract-review-context Show Safe Local Action Contract Review context")
        print("  orion-client-boundary-contract-status Show ORION Client Boundary Contract Foundation status")
        print("  orion-client-identity-boundary-plan <target> Prepare ORION client identity boundary plan")
        print("  atlas-orion-authority-boundary-plan <target> Prepare ATLAS ORION authority boundary plan")
        print("  orion-sense-permission-boundary-plan <target> Prepare ORION sense permission boundary plan")
        print("  orion-local-action-boundary-plan <target> Prepare ORION local action boundary plan")
        print("  orion-emergency-stop-boundary-plan <target> Prepare ORION emergency stop boundary plan")
        print("  orion-dashboard-status-boundary-plan <target> Prepare ORION dashboard status boundary plan")
        print("  orion-runtime-handshake-boundary-plan <target> Prepare ORION runtime handshake boundary plan")
        print("  orion-data-flow-redaction-boundary-plan <target> Prepare ORION data flow redaction boundary plan")
        print("  future-orion-runtime-boundary-plan <target> Prepare future ORION runtime boundary plan")
        print("  orion-client-boundary-contract-context Show ORION Client Boundary Contract context")
        print("  runtime-error-rollback-preview-status Show Runtime Error and Rollback Preview Foundation status")
        print("  runtime-error-taxonomy-preview-plan <target> Prepare runtime error taxonomy preview plan")
        print("  rollback-preview-packet-plan <target> Prepare rollback preview packet plan")
        print("  failure-recovery-state-model-plan <target> Prepare failure recovery state model plan")
        print("  cancellation-boundary-preview-plan <target> Prepare cancellation boundary preview plan")
        print("  partial-execution-guard-preview-plan <target> Prepare partial execution guard preview plan")
        print("  permission-error-review-plan <target> Prepare permission error review plan")
        print("  audit-error-reference-preview-plan <target> Prepare audit error reference preview plan")
        print("  dashboard-error-rollback-payload-plan <target> Prepare dashboard error rollback payload plan")
        print("  future-runtime-recovery-boundary-plan <target> Prepare future runtime recovery boundary plan")
        print("  runtime-error-rollback-preview-context Show Runtime Error and Rollback Preview context")
        print("  manual-approval-decision-flow-review-status Show Manual Approval Decision Flow Review Foundation status")
        print("  approval-request-schema-review-plan <target> Prepare approval request schema review plan")
        print("  approval-decision-state-review-plan <target> Prepare approval decision state review plan")
        print("  approval-outcome-catalog-review-plan <target> Prepare approval outcome catalog review plan")
        print("  approval-denial-cancellation-review-plan <target> Prepare approval denial cancellation review plan")
        print("  approval-escalation-boundary-review-plan <target> Prepare approval escalation boundary review plan")
        print("  approval-audit-reference-review-plan <target> Prepare approval audit reference review plan")
        print("  approval-dashboard-payload-review-plan <target> Prepare approval dashboard payload review plan")
        print("  approval-runtime-gate-boundary-review-plan <target> Prepare approval runtime gate boundary review plan")
        print("  future-manual-approval-runtime-boundary-plan <target> Prepare future manual approval runtime boundary plan")
        print("  manual-approval-decision-flow-review-context Show Manual Approval Decision Flow Review context")
        print("  v1-runtime-readiness-cutline-review-status Show v1 Runtime Readiness Cutline Review Foundation status")
        print("  v1-allowed-capability-cutline-plan <target> Prepare v1 allowed capability cutline plan")
        print("  v1-deferred-capability-cutline-plan <target> Prepare v1 deferred capability cutline plan")
        print("  v1-runtime-gate-cutline-plan <target> Prepare v1 runtime gate cutline plan")
        print("  v1-permission-audit-cutline-plan <target> Prepare v1 permission audit cutline plan")
        print("  v1-orion-boundary-cutline-plan <target> Prepare v1 ORION boundary cutline plan")
        print("  v1-dashboard-visibility-cutline-plan <target> Prepare v1 dashboard visibility cutline plan")
        print("  v1-release-blocker-cutline-plan <target> Prepare v1 release blocker cutline plan")
        print("  v1-safe-idle-acceptance-cutline-plan <target> Prepare v1 safe idle acceptance cutline plan")
        print("  future-v1-runtime-activation-boundary-plan <target> Prepare future v1 runtime activation boundary plan")
        print("  v1-runtime-readiness-cutline-review-context Show v1 Runtime Readiness Cutline Review context")
        print("  review-stabilization-111-120-status Show Review Stabilization 111-120 Foundation status")
        print("  sprint-111-120-completion-review-plan <target> Prepare Sprint 111-120 completion review plan")
        print("  capability-registry-stabilization-review-plan <target> Prepare capability registry stabilization review plan")
        print("  runtime-safety-zero-state-review-plan <target> Prepare runtime safety zero-state review plan")
        print("  integration-surface-stabilization-review-plan <target> Prepare integration surface stabilization review plan")
        print("  documentation-roadmap-stabilization-review-plan <target> Prepare documentation roadmap stabilization review plan")
        print("  v1-runtime-readiness-blocker-review-plan <target> Prepare v1 runtime readiness blocker review plan")
        print("  release-cutline-consistency-review-plan <target> Prepare release cutline consistency review plan")
        print("  next-block-121-130-boundary-plan <target> Prepare next block 121-130 boundary plan")
        print("  checkpoint-120-acceptance-review-plan <target> Prepare checkpoint 120 acceptance review plan")
        print("  review-stabilization-111-120-context Show Review Stabilization 111-120 context")
        print("  post-checkpoint-120-next-block-planning-status Show Post-Checkpoint 120 Next Block Planning Foundation status")
        print("  checkpoint-120-output-review-plan <target> Prepare checkpoint 120 output review plan")
        print("  sprint-121-130-scope-definition-plan <target> Prepare Sprint 121-130 scope definition plan")
        print("  runtime-readiness-continuation-plan <target> Prepare runtime readiness continuation plan")
        print("  permission-audit-writer-boundary-plan <target> Prepare permission audit writer boundary plan")
        print("  dashboard-control-center-boundary-plan <target> Prepare dashboard control center boundary plan")
        print("  orion-dry-handshake-boundary-plan <target> Prepare ORION dry handshake boundary plan")
        print("  safe-local-action-allowlist-boundary-plan <target> Prepare safe local action allowlist boundary plan")
        print("  runtime-activation-blocker-tracking-plan <target> Prepare runtime activation blocker tracking plan")
        print("  future-121-130-checkpoint-boundary-plan <target> Prepare future 121-130 checkpoint boundary plan")
        print("  post-checkpoint-120-next-block-planning-context Show Post-Checkpoint 120 Next Block Planning context")
        print("  runtime-permission-audit-writer-boundary-review-status Show Runtime Permission Audit Writer Boundary Review Foundation status")
        print("  audit-writer-schema-boundary-review-plan <target> Prepare audit writer schema boundary review plan")
        print("  audit-writer-storage-boundary-review-plan <target> Prepare audit writer storage boundary review plan")
        print("  audit-writer-redaction-boundary-review-plan <target> Prepare audit writer redaction boundary review plan")
        print("  audit-writer-visibility-boundary-review-plan <target> Prepare audit writer visibility boundary review plan")
        print("  permission-decision-audit-link-review-plan <target> Prepare permission decision audit link review plan")
        print("  dashboard-audit-payload-boundary-review-plan <target> Prepare dashboard audit payload boundary review plan")
        print("  audit-writer-failure-boundary-review-plan <target> Prepare audit writer failure boundary review plan")
        print("  audit-writer-runtime-gate-boundary-review-plan <target> Prepare audit writer runtime gate boundary review plan")
        print("  future-permission-audit-writer-runtime-boundary-plan <target> Prepare future permission audit writer runtime boundary plan")
        print("  runtime-permission-audit-writer-boundary-review-context Show Runtime Permission Audit Writer Boundary Review context")
        print("  dashboard-control-center-boundary-review-status Show Dashboard Control Center Boundary Review Foundation status")
        print("  control-center-shell-layout-boundary-review-plan <target> Prepare control center shell layout boundary review plan")
        print("  dashboard-status-payload-boundary-review-plan <target> Prepare dashboard status payload boundary review plan")
        print("  permission-panel-boundary-review-plan <target> Prepare permission panel boundary review plan")
        print("  audit-panel-boundary-review-plan <target> Prepare audit panel boundary review plan")
        print("  action-proposal-panel-boundary-review-plan <target> Prepare action proposal panel boundary review plan")
        print("  orion-client-panel-boundary-review-plan <target> Prepare ORION client panel boundary review plan")
        print("  runtime-gate-panel-boundary-review-plan <target> Prepare runtime gate panel boundary review plan")
        print("  dashboard-failure-safe-idle-boundary-review-plan <target> Prepare dashboard failure safe idle boundary review plan")
        print("  future-dashboard-control-center-runtime-boundary-plan <target> Prepare future dashboard control center runtime boundary plan")
        print("  dashboard-control-center-boundary-review-context Show Dashboard Control Center Boundary Review context")
        print("  orion-dry-handshake-boundary-review-status Show ORION Dry Handshake Boundary Review Foundation status")
        print("  orion-client-identity-packet-boundary-review-plan <target> Prepare ORION client identity packet boundary review plan")
        print("  orion-capability-packet-boundary-review-plan <target> Prepare ORION capability packet boundary review plan")
        print("  orion-permission-scope-packet-boundary-review-plan <target> Prepare ORION permission scope packet boundary review plan")
        print("  orion-status-heartbeat-boundary-review-plan <target> Prepare ORION status heartbeat boundary review plan")
        print("  orion-redaction-boundary-review-plan <target> Prepare ORION redaction boundary review plan")
        print("  orion-emergency-stop-boundary-review-plan <target> Prepare ORION emergency stop boundary review plan")
        print("  atlas-orion-authority-boundary-review-plan <target> Prepare ATLAS/ORION authority boundary review plan")
        print("  orion-failure-safe-idle-boundary-review-plan <target> Prepare ORION failure safe idle boundary review plan")
        print("  future-orion-handshake-runtime-boundary-plan <target> Prepare future ORION handshake runtime boundary plan")
        print("  orion-dry-handshake-boundary-review-context Show ORION Dry Handshake Boundary Review context")
        print("  safe-local-action-allowlist-boundary-review-status Show Safe Local Action Allowlist Boundary Review Foundation status")
        print("  safe-action-catalog-boundary-review-plan <target> Prepare safe action catalog boundary review plan")
        print("  safe-action-scope-boundary-review-plan <target> Prepare safe action scope boundary review plan")
        print("  safe-action-permission-boundary-review-plan <target> Prepare safe action permission boundary review plan")
        print("  safe-action-risk-level-boundary-review-plan <target> Prepare safe action risk level boundary review plan")
        print("  safe-action-rollback-boundary-review-plan <target> Prepare safe action rollback boundary review plan")
        print("  safe-action-audit-dashboard-boundary-review-plan <target> Prepare safe action audit/dashboard boundary review plan")
        print("  safe-action-denied-action-boundary-review-plan <target> Prepare safe action denied action boundary review plan")
        print("  safe-action-runtime-gate-boundary-review-plan <target> Prepare safe action runtime gate boundary review plan")
        print("  future-safe-local-action-runtime-boundary-plan <target> Prepare future safe local action runtime boundary plan")
        print("  safe-local-action-allowlist-boundary-review-context Show Safe Local Action Allowlist Boundary Review context")
        print("  runtime-grant-expiry-boundary-review-status Show Runtime Grant Expiry Boundary Review Foundation status")
        print("  grant-expiry-schema-boundary-review-plan <target> Prepare grant expiry schema boundary review plan")
        print("  grant-lifetime-policy-boundary-review-plan <target> Prepare grant lifetime policy boundary review plan")
        print("  grant-renewal-request-boundary-review-plan <target> Prepare grant renewal request boundary review plan")
        print("  grant-revocation-boundary-review-plan <target> Prepare grant revocation boundary review plan")
        print("  expired-grant-denial-boundary-review-plan <target> Prepare expired grant denial boundary review plan")
        print("  dashboard-grant-visibility-boundary-review-plan <target> Prepare dashboard grant visibility boundary review plan")
        print("  audit-grant-expiry-boundary-review-plan <target> Prepare audit grant expiry boundary review plan")
        print("  grant-expiry-failure-safe-idle-boundary-review-plan <target> Prepare grant expiry failure safe idle boundary review plan")
        print("  future-runtime-grant-expiry-boundary-plan <target> Prepare future runtime grant expiry boundary plan")
        print("  runtime-grant-expiry-boundary-review-context Show Runtime Grant Expiry Boundary Review context")
        print("  runtime-recovery-drill-boundary-review-status Show Runtime Recovery Drill Boundary Review Foundation status")
        print("  recovery-drill-scenario-catalog-boundary-review-plan <target> Prepare recovery drill scenario catalog boundary review plan")
        print("  recovery-trigger-boundary-review-plan <target> Prepare recovery trigger boundary review plan")
        print("  recovery-safe-idle-boundary-review-plan <target> Prepare recovery safe idle boundary review plan")
        print("  rollback-preview-boundary-review-plan <target> Prepare rollback preview boundary review plan")
        print("  recovery-audit-dashboard-boundary-review-plan <target> Prepare recovery audit/dashboard boundary review plan")
        print("  recovery-permission-boundary-review-plan <target> Prepare recovery permission boundary review plan")
        print("  orion-recovery-disconnect-boundary-review-plan <target> Prepare ORION recovery disconnect boundary review plan")
        print("  recovery-failure-escalation-boundary-review-plan <target> Prepare recovery failure escalation boundary review plan")
        print("  future-runtime-recovery-drill-boundary-plan <target> Prepare future runtime recovery drill boundary plan")
        print("  runtime-recovery-drill-boundary-review-context Show Runtime Recovery Drill Boundary Review context")
        print("  dashboard-runtime-readiness-boundary-review-status Show Dashboard Runtime Readiness Boundary Review Foundation status")
        print("  dashboard-runtime-entrypoint-boundary-review-plan <target> Prepare dashboard runtime entrypoint boundary review plan")
        print("  dashboard-route-contract-boundary-review-plan <target> Prepare dashboard route contract boundary review plan")
        print("  dashboard-api-contract-boundary-review-plan <target> Prepare dashboard API contract boundary review plan")
        print("  dashboard-websocket-event-boundary-review-plan <target> Prepare dashboard websocket event boundary review plan")
        print("  dashboard-permission-panel-runtime-boundary-review-plan <target> Prepare dashboard permission panel runtime boundary review plan")
        print("  dashboard-audit-panel-runtime-boundary-review-plan <target> Prepare dashboard audit panel runtime boundary review plan")
        print("  dashboard-action-panel-runtime-boundary-review-plan <target> Prepare dashboard action panel runtime boundary review plan")
        print("  dashboard-failure-safe-idle-boundary-review-plan <target> Prepare dashboard failure safe idle boundary review plan")
        print("  future-dashboard-runtime-activation-boundary-plan <target> Prepare future dashboard runtime activation boundary plan")
        print("  dashboard-runtime-readiness-boundary-review-context Show Dashboard Runtime Readiness Boundary Review context")
        print("  runtime-activation-blocker-register-boundary-review-status Show Runtime Activation Blocker Register Boundary Review Foundation status")
        print("  blocker-register-schema-boundary-review-plan <target> Prepare blocker register schema boundary review plan")
        print("  blocker-source-classification-boundary-review-plan <target> Prepare blocker source classification boundary review plan")
        print("  blocker-severity-policy-boundary-review-plan <target> Prepare blocker severity policy boundary review plan")
        print("  blocker-activation-gate-link-boundary-review-plan <target> Prepare blocker activation gate link boundary review plan")
        print("  blocker-resolution-evidence-boundary-review-plan <target> Prepare blocker resolution evidence boundary review plan")
        print("  blocker-dashboard-visibility-boundary-review-plan <target> Prepare blocker dashboard visibility boundary review plan")
        print("  blocker-audit-link-boundary-review-plan <target> Prepare blocker audit link boundary review plan")
        print("  blocker-failure-safe-idle-boundary-review-plan <target> Prepare blocker failure safe idle boundary review plan")
        print("  future-runtime-activation-unblock-boundary-plan <target> Prepare future runtime activation unblock boundary plan")
        print("  runtime-activation-blocker-register-boundary-review-context Show Runtime Activation Blocker Register Boundary Review context")
        print("  review-stabilization-121-130-status Show Review Stabilization 121-130 Foundation status")
        print("  sprint-121-129-completion-review-plan <target> Prepare Sprint 121-129 completion review plan")
        print("  capability-registry-consistency-review-plan <target> Prepare capability registry consistency review plan")
        print("  permission-boundary-consistency-review-plan <target> Prepare permission boundary consistency review plan")
        print("  runtime-zero-counter-review-plan <target> Prepare runtime zero counter review plan")
        print("  dashboard-orion-boundary-review-plan <target> Prepare dashboard ORION boundary review plan")
        print("  action-permission-recovery-blocker-review-plan <target> Prepare action permission recovery blocker review plan")
        print("  documentation-roadmap-consistency-review-plan <target> Prepare documentation roadmap consistency review plan")
        print("  boot-and-cli-surface-review-plan <target> Prepare boot and CLI surface review plan")
        print("  known-deferred-runtime-review-plan <target> Prepare known deferred runtime review plan")
        print("  future-sprint-131-140-readiness-plan <target> Prepare future Sprint 131-140 readiness plan")
        print("  review-stabilization-121-130-context Show Review Stabilization 121-130 context")
        print("  post-checkpoint-130-next-block-status Show Post-Checkpoint 130 Next Block Foundation status")
        print("  sprint-131-140-sequence-foundation-plan <target> Prepare Sprint 131-140 sequence foundation plan")
        print("  final-genesis-acceptance-criteria-foundation-plan <target> Prepare Final Genesis acceptance criteria foundation plan")
        print("  runtime-activation-path-proposal-review-plan <target> Prepare runtime activation path proposal review plan")
        print("  local-service-boot-plan-review-plan <target> Prepare local service boot plan review plan")
        print("  control-center-runtime-entry-review-plan <target> Prepare Control Center runtime entry review plan")
        print("  chat-runtime-minimal-loop-review-plan <target> Prepare chat runtime minimal loop review plan")
        print("  memory-runtime-write-gate-review-plan <target> Prepare memory runtime write gate review plan")
        print("  permission-runtime-grant-gate-review-plan <target> Prepare permission runtime grant gate review plan")
        print("  audit-runtime-writer-activation-review-plan <target> Prepare audit runtime writer activation review plan")
        print("  review-stabilization-131-140-checkpoint-plan <target> Prepare review stabilization 131-140 checkpoint plan")
        print("  post-checkpoint-130-next-block-context Show Post-Checkpoint 130 Next Block context")
        print("  final-genesis-acceptance-criteria-status Show Final Genesis Acceptance Criteria Foundation status")
        print("  boot-stability-acceptance-criteria-plan <target> Prepare boot stability acceptance criteria plan")
        print("  local-service-acceptance-criteria-plan <target> Prepare local service acceptance criteria plan")
        print("  control-center-acceptance-criteria-plan <target> Prepare Control Center acceptance criteria plan")
        print("  local-chat-acceptance-criteria-plan <target> Prepare local chat acceptance criteria plan")
        print("  memory-acceptance-criteria-plan <target> Prepare memory acceptance criteria plan")
        print("  permission-audit-acceptance-criteria-plan <target> Prepare permission audit acceptance criteria plan")
        print("  safe-idle-recovery-acceptance-criteria-plan <target> Prepare safe idle recovery acceptance criteria plan")
        print("  optional-orion-voice-vision-avatar-boundary-criteria-plan <target> Prepare optional ORION voice vision avatar boundary criteria plan")
        print("  final-genesis-go-no-go-criteria-plan <target> Prepare Final Genesis go/no-go criteria plan")
        print("  future-runtime-release-candidate-criteria-plan <target> Prepare future runtime release candidate criteria plan")
        print("  final-genesis-acceptance-criteria-context Show Final Genesis Acceptance Criteria context")
        print("  runtime-activation-path-proposal-review-status Show Runtime Activation Path Proposal Review Foundation status")
        print("  runtime-activation-stage-model-review-plan <target> Prepare runtime activation stage model review plan")
        print("  manual-approval-chain-review-plan <target> Prepare manual approval chain review plan")
        print("  activation-blocker-register-link-review-plan <target> Prepare activation blocker register link review plan")
        print("  permission-contract-activation-review-plan <target> Prepare permission contract activation review plan")
        print("  audit-contract-activation-review-plan <target> Prepare audit contract activation review plan")
        print("  dashboard-visibility-activation-review-plan <target> Prepare dashboard visibility activation review plan")
        print("  safe-idle-rollback-activation-review-plan <target> Prepare safe idle rollback activation review plan")
        print("  emergency-stop-activation-review-plan <target> Prepare emergency stop activation review plan")
        print("  release-candidate-transition-review-plan <target> Prepare release candidate transition review plan")
        print("  activation-denial-deferment-review-plan <target> Prepare activation denial deferment review plan")
        print("  runtime-activation-path-proposal-review-context Show Runtime Activation Path Proposal Review context")
        print("  local-service-boot-plan-review-status Show Local Service Boot Plan Review Foundation status")
        print("  local-service-manual-start-review-plan <target> Prepare local service manual start review plan")
        print("  local-service-manual-stop-review-plan <target> Prepare local service manual stop review plan")
        print("  local-service-health-monitor-review-plan <target> Prepare local service health monitor review plan")
        print("  local-service-safe-shutdown-review-plan <target> Prepare local service safe shutdown review plan")
        print("  local-service-config-contract-review-plan <target> Prepare local service config contract review plan")
        print("  local-service-log-visibility-review-plan <target> Prepare local service log visibility review plan")
        print("  local-service-localhost-only-review-plan <target> Prepare local service localhost-only review plan")
        print("  local-service-autostart-guard-review-plan <target> Prepare local service autostart guard review plan")
        print("  local-service-failure-safe-idle-review-plan <target> Prepare local service failure safe idle review plan")
        print("  local-service-no-port-binding-review-plan <target> Prepare local service no-port-binding review plan")
        print("  local-service-boot-plan-review-context Show Local Service Boot Plan Review context")
        print("  control-center-runtime-entry-review-status Show Control Center Runtime Entry Review Foundation status")
        print("  control-center-entry-route-review-plan <target> Prepare Control Center entry route review plan")
        print("  control-center-localhost-boundary-review-plan <target> Prepare Control Center localhost boundary review plan")
        print("  control-center-read-only-default-review-plan <target> Prepare Control Center read-only default review plan")
        print("  control-center-status-panel-runtime-entry-review-plan <target> Prepare Control Center status panel runtime entry review plan")
        print("  control-center-permission-panel-runtime-entry-review-plan <target> Prepare Control Center permission panel runtime entry review plan")
        print("  control-center-audit-panel-runtime-entry-review-plan <target> Prepare Control Center audit panel runtime entry review plan")
        print("  control-center-action-proposal-panel-runtime-entry-review-plan <target> Prepare Control Center action proposal panel runtime entry review plan")
        print("  control-center-safe-idle-error-panel-runtime-entry-review-plan <target> Prepare Control Center safe idle error panel runtime entry review plan")
        print("  control-center-manual-approval-entry-review-plan <target> Prepare Control Center manual approval entry review plan")
        print("  control-center-no-server-start-review-plan <target> Prepare Control Center no-server-start review plan")
        print("  control-center-runtime-entry-review-context Show Control Center Runtime Entry Review context")
        print("  chat-runtime-minimal-loop-review-status Show Chat Runtime Minimal Loop Review Foundation status")
        print("  chat-input-boundary-review-plan <target> Prepare chat input boundary review plan")
        print("  chat-response-boundary-review-plan <target> Prepare chat response boundary review plan")
        print("  chat-session-state-review-plan <target> Prepare chat session state review plan")
        print("  chat-permission-prompt-review-plan <target> Prepare chat permission prompt review plan")
        print("  chat-memory-read-write-gate-review-plan <target> Prepare chat memory read/write gate review plan")
        print("  chat-audit-event-review-plan <target> Prepare chat audit event review plan")
        print("  chat-safe-idle-fallback-review-plan <target> Prepare chat safe idle fallback review plan")
        print("  chat-error-recovery-review-plan <target> Prepare chat error recovery review plan")
        print("  chat-manual-approval-runtime-entry-review-plan <target> Prepare chat manual approval runtime entry review plan")
        print("  chat-no-model-execution-review-plan <target> Prepare chat no-model-execution review plan")
        print("  chat-runtime-minimal-loop-review-context Show Chat Runtime Minimal Loop Review context")
        print("  memory-runtime-write-gate-review-status Show Memory Runtime Write Gate Review Foundation status")
        print("  memory-write-intent-classification-review-plan <target> Prepare memory write intent classification review plan")
        print("  memory-write-manual-approval-review-plan <target> Prepare memory write manual approval review plan")
        print("  memory-write-scope-boundary-review-plan <target> Prepare memory write scope boundary review plan")
        print("  memory-write-redaction-review-plan <target> Prepare memory write redaction review plan")
        print("  memory-write-conflict-resolution-review-plan <target> Prepare memory write conflict resolution review plan")
        print("  memory-write-audit-event-review-plan <target> Prepare memory write audit event review plan")
        print("  memory-write-rollback-review-plan <target> Prepare memory write rollback review plan")
        print("  memory-write-safe-idle-failure-review-plan <target> Prepare memory write safe idle failure review plan")
        print("  memory-write-session-link-review-plan <target> Prepare memory write session link review plan")
        print("  memory-write-no-persistence-review-plan <target> Prepare memory write no-persistence review plan")
        print("  memory-runtime-write-gate-review-context Show Memory Runtime Write Gate Review context")
        print("  permission-runtime-grant-gate-review-status Show Permission Runtime Grant Gate Review Foundation status")
        print("  permission-grant-scope-review-plan <target> Prepare permission grant scope review plan")
        print("  permission-grant-manual-approval-review-plan <target> Prepare permission grant manual approval review plan")
        print("  permission-grant-expiry-review-plan <target> Prepare permission grant expiry review plan")
        print("  permission-grant-denial-review-plan <target> Prepare permission grant denial review plan")
        print("  permission-grant-audit-link-review-plan <target> Prepare permission grant audit link review plan")
        print("  permission-grant-dashboard-visibility-review-plan <target> Prepare permission grant dashboard visibility review plan")
        print("  permission-grant-revocation-review-plan <target> Prepare permission grant revocation review plan")
        print("  permission-grant-risk-classification-review-plan <target> Prepare permission grant risk classification review plan")
        print("  permission-grant-safe-idle-failure-review-plan <target> Prepare permission grant safe idle failure review plan")
        print("  permission-grant-no-mutation-review-plan <target> Prepare permission grant no-mutation review plan")
        print("  permission-runtime-grant-gate-review-context Show Permission Runtime Grant Gate Review context")
        print("  audit-runtime-writer-activation-review-status Show Audit Runtime Writer Activation Review Foundation status")
        print("  audit-writer-activation-scope-review-plan <target> Prepare audit writer activation scope review plan")
        print("  audit-event-schema-review-plan <target> Prepare audit event schema review plan")
        print("  audit-append-only-storage-review-plan <target> Prepare audit append-only storage review plan")
        print("  audit-redaction-boundary-review-plan <target> Prepare audit redaction boundary review plan")
        print("  audit-actor-context-review-plan <target> Prepare audit actor context review plan")
        print("  audit-permission-link-review-plan <target> Prepare audit permission link review plan")
        print("  audit-dashboard-visibility-review-plan <target> Prepare audit dashboard visibility review plan")
        print("  audit-failure-safe-idle-review-plan <target> Prepare audit failure safe idle review plan")
        print("  audit-retention-export-review-plan <target> Prepare audit retention/export review plan")
        print("  audit-no-write-activation-review-plan <target> Prepare audit no-write activation review plan")
        print("  audit-runtime-writer-activation-review-context Show Audit Runtime Writer Activation Review context")
        print("  review-stabilization-131-140-status Show Review Stabilization 131-140 Foundation status")
        print("  sprint-131-140-scope-review-plan <target> Prepare Sprint 131-140 scope review plan")
        print("  runtime-boundary-integrity-review-plan <target> Prepare runtime boundary integrity review plan")
        print("  capability-registry-consistency-review-plan <target> Prepare capability registry consistency review plan")
        print("  system-status-surface-review-plan <target> Prepare system status surface review plan")
        print("  skill-plugin-cli-shell-review-plan <target> Prepare skill/plugin/CLI/shell review plan")
        print("  documentation-roadmap-review-plan <target> Prepare documentation roadmap review plan")
        print("  safety-counter-zero-review-plan <target> Prepare safety counter zero review plan")
        print("  git-boot-verification-review-plan <target> Prepare git boot verification review plan")
        print("  next-block-readiness-review-plan <target> Prepare next block readiness review plan")
        print("  no-runtime-activation-review-plan <target> Prepare no runtime activation review plan")
        print("  review-stabilization-131-140-context Show Review Stabilization 131-140 context")
        print("  local-service-runtime-foundation-status Show Local Service Runtime Foundation status")
        print("  service-foundation-scope-plan <target> Prepare service foundation scope plan")
        print("  service-safe-idle-entry-plan <target> Prepare service safe-idle entry plan")
        print("  localhost-binding-boundary-plan <target> Prepare localhost binding boundary plan")
        print("  service-lifecycle-state-plan <target> Prepare service lifecycle state plan")
        print("  service-config-contract-plan <target> Prepare service config contract plan")
        print("  service-health-surface-plan <target> Prepare service health surface plan")
        print("  service-permission-gate-link-plan <target> Prepare service permission gate link plan")
        print("  service-audit-link-plan <target> Prepare service audit link plan")
        print("  service-control-command-boundary-plan <target> Prepare service control command boundary plan")
        print("  service-no-start-activation-plan <target> Prepare service no-start activation plan")
        print("  local-service-runtime-foundation-context Show Local Service Runtime Foundation context")
        print("  local-service-safe-idle-boot-boundary-status Show Local Service Safe Idle Boot Boundary status")
        print("  safe-idle-boot-scope-plan <target> Prepare safe-idle boot scope plan")
        print("  boot-entry-state-contract-plan <target> Prepare boot entry state contract plan")
        print("  safe-idle-guard-condition-plan <target> Prepare safe-idle guard condition plan")
        print("  boot-failure-fallback-plan <target> Prepare boot failure fallback plan")
        print("  service-no-autostart-boundary-plan <target> Prepare service no-autostart boundary plan")
        print("  readiness-probe-read-only-plan <target> Prepare readiness probe read-only plan")
        print("  control-center-idle-visibility-plan <target> Prepare Control Center idle visibility plan")
        print("  permission-denial-idle-plan <target> Prepare permission denial idle plan")
        print("  audit-failure-idle-plan <target> Prepare audit failure idle plan")
        print("  no-boot-activation-plan <target> Prepare no boot activation plan")
        print("  local-service-safe-idle-boot-boundary-context Show Local Service Safe Idle Boot Boundary context")
        print("  local-service-health-endpoint-foundation-status Show Local Service Health Endpoint Foundation status")
        print("  health-endpoint-scope-plan <target> Prepare health endpoint scope plan")
        print("  health-endpoint-contract-plan <target> Prepare health endpoint contract plan")
        print("  health-response-schema-plan <target> Prepare health response schema plan")
        print("  localhost-health-binding-boundary-plan <target> Prepare localhost health binding boundary plan")
        print("  safe-idle-health-state-plan <target> Prepare safe-idle health state plan")
        print("  health-dependency-visibility-plan <target> Prepare health dependency visibility plan")
        print("  permission-audit-health-link-plan <target> Prepare permission/audit health link plan")
        print("  control-center-health-card-plan <target> Prepare Control Center health card plan")
        print("  health-error-fallback-plan <target> Prepare health error fallback plan")
        print("  no-health-endpoint-activation-plan <target> Prepare no health endpoint activation plan")
        print("  local-service-health-endpoint-foundation-context Show Local Service Health Endpoint Foundation context")
        print("  local-service-configuration-port-registry-foundation-status Show Service Configuration and Port Registry Foundation status")
        print("  service-configuration-scope-plan <target> Prepare service configuration scope plan")
        print("  service-config-schema-plan <target> Prepare service config schema plan")
        print("  service-port-registry-schema-plan <target> Prepare service port registry schema plan")
        print("  localhost-port-policy-plan <target> Prepare localhost port policy plan")
        print("  reserved-port-policy-plan <target> Prepare reserved port policy plan")
        print("  port-conflict-preflight-plan <target> Prepare port conflict preflight plan")
        print("  environment-override-boundary-plan <target> Prepare environment override boundary plan")
        print("  control-center-config-card-plan <target> Prepare Control Center config card plan")
        print("  permission-audit-config-link-plan <target> Prepare permission/audit config link plan")
        print("  no-config-port-runtime-activation-plan <target> Prepare no config/port runtime activation plan")
        print("  local-service-configuration-port-registry-foundation-context Show Service Configuration and Port Registry Foundation context")
        print("  service-permission-gate-runtime-boundary-status Show Service Permission Gate Runtime Boundary status")
        print("  service-permission-scope-catalog-plan <target> Prepare service permission scope catalog plan")
        print("  service-permission-request-contract-plan <target> Prepare service permission request contract plan")
        print("  service-permission-grant-preflight-plan <target> Prepare service permission grant preflight plan")
        print("  service-permission-denial-safe-idle-plan <target> Prepare service permission denial safe-idle plan")
        print("  service-permission-control-center-surface-plan <target> Prepare service permission Control Center surface plan")
        print("  service-permission-audit-link-plan <target> Prepare service permission audit link plan")
        print("  service-permission-expiry-review-plan <target> Prepare service permission expiry review plan")
        print("  service-permission-error-boundary-plan <target> Prepare service permission error boundary plan")
        print("  service-permission-manual-approval-boundary-plan <target> Prepare service permission manual approval boundary plan")
        print("  no-permission-runtime-activation-plan <target> Prepare no permission runtime activation plan")
        print("  service-permission-gate-runtime-boundary-context Show Service Permission Gate Runtime Boundary context")
        print("  service-audit-link-foundation-status Show Service Audit Link Foundation status")
        print("  service-audit-event-reference-plan <target> Prepare service audit event reference plan")
        print("  service-audit-link-contract-plan <target> Prepare service audit link contract plan")
        print("  service-audit-traceability-chain-plan <target> Prepare service audit traceability chain plan")
        print("  service-audit-permission-link-plan <target> Prepare service audit permission link plan")
        print("  service-audit-control-center-surface-plan <target> Prepare service audit Control Center surface plan")
        print("  service-audit-redaction-boundary-plan <target> Prepare service audit redaction boundary plan")
        print("  service-audit-failure-safe-idle-plan <target> Prepare service audit failure safe-idle plan")
        print("  service-audit-retention-boundary-plan <target> Prepare service audit retention boundary plan")
        print("  service-audit-error-boundary-plan <target> Prepare service audit error boundary plan")
        print("  no-audit-link-runtime-activation-plan <target> Prepare no audit link runtime activation plan")
        print("  service-audit-link-foundation-context Show Service Audit Link Foundation context")
        print("  voice-input-permission-plan <target> Prepare microphone permission plan")
        print("  voice-capture-boundary-plan <target> Prepare voice capture boundary plan")
        print("  speech-to-text-adapter-plan <target> Prepare STT adapter plan")
        print("  voice-intent-gate-plan <target> Prepare voice intent gate plan")
        print("  voice-command-confirmation-plan <target> Prepare command confirmation plan")
        print("  voice-session-plan <target> Prepare voice session plan")
        print("  voice-input-safety-plan <target> Prepare voice input safety plan")
        print("  voice-input-context Show Voice Input Runtime Foundation context")
        print("  knowledge-uncertainty-status Show Knowledge Uncertainty Gate status")
        print("  knowledge-gap-plan <target> Prepare knowledge gap plan")
        print("  knowledge-uncertainty-review-plan <target> Prepare uncertainty review plan")
        print("  internet-search-gate-plan <target> Prepare internet search permission gate plan")
        print("  source-requirement-plan <target> Prepare source requirement plan")
        print("  download-requirement-plan <target> Prepare download requirement notice plan")
        print("  answer-confidence-plan <target> Prepare answer confidence plan")
        print("  knowledge-safety-plan <target> Prepare knowledge safety plan")
        print("  knowledge-uncertainty-context Show Knowledge Uncertainty Gate context")
        print("  reasoning-context-status Show Reasoning Context Manager status")
        print("  reasoning-context-plan <target> Prepare visible reasoning context plan")
        print("  fact-assumption-plan <target> Prepare fact/assumption separation plan")
        print("  unknowns-review-plan <target> Prepare unknowns review plan")
        print("  evidence-boundary-plan <target> Prepare evidence boundary plan")
        print("  decision-frame-plan <target> Prepare decision frame plan")
        print("  response-strategy-plan <target> Prepare response strategy plan")
        print("  reasoning-safety-plan <target> Prepare reasoning safety plan")
        print("  reasoning-context Show Reasoning Context Manager context")
        print("  thought-loop-status Show Thought Loop Planner status")
        print("  thought-cycle-plan <target> Prepare metadata-only thought cycle plan")
        print("  intent-frame-plan <target> Prepare metadata-only intent frame plan")
        print("  reasoning-summary-plan <target> Prepare visible reasoning summary plan")
        print("  uncertainty-review-plan <target> Prepare uncertainty review plan")
        print("  action-readiness-review <target> Prepare action readiness review")
        print("  growth-memory-review <target> Prepare growth memory review")
        print("  thought-safety-plan <target> Prepare thought safety plan")
        print("  thought-loop-context Show Thought Loop Planner context")
        print("  partner-runtime-status Show Partner Runtime Planning Layer status")
        print("  partner-runtime-unified-session-status Show Sprint 221 unified-session contract status")
        print("  partner-runtime-unified-session-context Show Sprint 221 unified-session contract context")
        print("  partner-runtime-unified-session-check Run Sprint 221 unified-session contract checks")
        print("  partner-runtime-workspace-project-context-status")
        print("  partner-runtime-workspace-project-context-context")
        print("  partner-runtime-workspace-project-context-check")
        print("  partner-runtime-genesis-release-candidate-approval-status Show Sprint 235 Genesis release candidate approval status")
        print("  partner-runtime-genesis-release-candidate-approval-context Show Sprint 235 Genesis release candidate approval context")
        print("  partner-runtime-genesis-release-candidate-approval-check Run Sprint 235 Genesis release candidate approval checks")
        print("  partner-runtime-genesis-release-candidate-readiness-status Show Sprint 234 Genesis release candidate readiness status")
        print("  partner-runtime-genesis-release-candidate-readiness-context Show Sprint 234 Genesis release candidate readiness context")
        print("  partner-runtime-genesis-release-candidate-readiness-check Run Sprint 234 Genesis release candidate readiness checks")
        print("  partner-runtime-genesis-release-candidate-verification-status Show Sprint 233 Genesis release candidate verification status")
        print("  partner-runtime-genesis-release-candidate-verification-context Show Sprint 233 Genesis release candidate verification context")
        print("  partner-runtime-genesis-release-candidate-verification-check Run Sprint 233 Genesis release candidate verification checks")
        print("  partner-runtime-genesis-release-candidate-assembly-status Show Sprint 232 Genesis release candidate assembly status")
        print("  partner-runtime-genesis-release-candidate-assembly-context Show Sprint 232 Genesis release candidate assembly context")
        print("  partner-runtime-genesis-release-candidate-assembly-check Run Sprint 232 Genesis release candidate assembly checks")
        print("  partner-runtime-genesis-final-integration-and-release-status Show Sprint 231 Genesis final integration and release status")
        print("  partner-runtime-genesis-final-integration-and-release-context Show Sprint 231 Genesis final integration and release context")
        print("  partner-runtime-genesis-final-integration-and-release-check Run Sprint 231 Genesis final integration and release checks")
        print("  partner-runtime-unified-partner-runtime-stabilization-status Show Sprint 230 unified partner runtime stabilization status")
        print("  partner-runtime-unified-partner-runtime-stabilization-context Show Sprint 230 unified partner runtime stabilization context")
        print("  partner-runtime-unified-partner-runtime-stabilization-check Run Sprint 230 unified partner runtime stabilization checks")
        print("  partner-runtime-genesis-acceptance-rehearsal-status Show Sprint 228 Genesis acceptance rehearsal contract status")
        print("  partner-runtime-genesis-acceptance-rehearsal-context Show Sprint 228 Genesis acceptance rehearsal contract context")
        print("  partner-runtime-genesis-acceptance-rehearsal-check Run Sprint 228 Genesis acceptance rehearsal contract checks")
        print("  partner-runtime-safe-auto-start-evaluation-status Show Sprint 228 safe auto-start evaluation contract status")
        print("  partner-runtime-safe-auto-start-evaluation-context Show Sprint 228 safe auto-start evaluation contract context")
        print("  partner-runtime-safe-auto-start-evaluation-check Run Sprint 228 safe auto-start evaluation contract checks")
        print("  partner-runtime-service-persistence-launcher-status Show Sprint 227 service persistence and launcher contract status")
        print("  partner-runtime-service-persistence-launcher-context Show Sprint 227 service persistence and launcher contract context")
        print("  partner-runtime-service-persistence-launcher-check Run Sprint 227 service persistence and launcher contract checks")
        print("  partner-runtime-multi-interface-state-synchronization-status Show Sprint 226 multi-interface state synchronization contract status")
        print("  partner-runtime-multi-interface-state-synchronization-context Show Sprint 226 multi-interface state synchronization contract context")
        print("  partner-runtime-multi-interface-state-synchronization-check Run Sprint 226 multi-interface state synchronization contract checks")
        print("  partner-runtime-personality-consistency-status Show Sprint 225 personality consistency contract status")
        print("  partner-runtime-personality-consistency-context Show Sprint 225 personality consistency contract context")
        print("  partner-runtime-personality-consistency-check Run Sprint 225 personality consistency contract checks")
        print("  partner-runtime-voice-vision-chat-context-fusion-status Show Sprint 224 fusion contract status")
        print("  partner-runtime-voice-vision-chat-context-fusion-context Show Sprint 224 fusion contract context")
        print("  partner-runtime-voice-vision-chat-context-fusion-check Run Sprint 224 fusion contract checks")
        print("  partner-runtime-chat-to-memory-handoff-status Show Sprint 223 handoff contract status")
        print("  partner-runtime-chat-to-memory-handoff-context Show Sprint 223 handoff contract context")
        print("  partner-runtime-chat-to-memory-handoff-check Run Sprint 223 handoff contract checks")
        print("  partner-runtime-mode-plan <target> Prepare metadata-only partner runtime mode plan")
        print("  partner-session-plan <target> Prepare metadata-only partner session plan")
        print("  partner-multimodal-handoff-plan <target> Prepare metadata-only multimodal handoff plan")
        print("  partner-tool-permission-plan <target> Prepare tool permission gate plan")
        print("  partner-growth-cycle-plan <target> Prepare growth checkpoint plan")
        print("  partner-runtime-safety-plan <target> Prepare partner runtime safety plan")
        print("  partner-runtime-context Show Partner Runtime Planning Layer context")
        print("  desktop-workflow-status Show Desktop Workflow Planner status")
        print("  desktop-workflow-plan <target> Prepare metadata-only desktop workflow plan")
        print("  desktop-app-context-plan <target> Prepare metadata-only app context plan")
        print("  desktop-window-flow-plan <target> Prepare metadata-only window flow plan")
        print("  desktop-task-sequence-plan <target> Prepare metadata-only task sequence plan")
        print("  desktop-safety-plan <target> Prepare desktop safety plan")
        print("  desktop-workflow-context Show Desktop Workflow Planner context")
        print("  avatar-interaction-status Show Avatar Interaction Planner status")
        print("  avatar-expression-plan <target> Prepare metadata-only avatar expression plan")
        print("  avatar-gesture-plan <target> Prepare metadata-only avatar gesture plan")
        print("  avatar-pose-plan <target> Prepare metadata-only avatar pose plan")
        print("  avatar-streaming-presence-plan <target> Prepare metadata-only avatar streaming presence plan")
        print("  avatar-safety-plan <target> Prepare avatar safety plan")
        print("  avatar-interaction-context Show Avatar Interaction Planner context")
        print("  vision-context-status Show Vision Context Planner status")
        print("  visual-context-plan <target> Prepare metadata-only visual context plan")
        print("  screen-context-plan <target> Prepare metadata-only screen context plan")
        print("  camera-context-plan <target> Prepare metadata-only camera context plan")
        print("  vision-safety-plan <target> Prepare vision safety plan")
        print("  vision-context Show Vision Context Planner context")
        print("  voice-conversation-status Show Voice Conversation Planner status")
        print("  voice-intent-plan <target> Prepare metadata-only voice intent plan")
        print("  voice-response-plan <target> Prepare metadata-only voice response plan")
        print("  voice-turn-plan <target> Prepare metadata-only conversation turn plan")
        print("  voice-safety-plan <target> Prepare voice safety plan")
        print("  voice-conversation-context Show Voice Conversation Planner context")
        print("  codebase-change-status Show Codebase Change Planner status")
        print("  codebase-change-plan <target> Prepare metadata-only codebase change plan")
        print("  codebase-impact-review <target> Prepare metadata-only codebase impact review")
        print("  codebase-patch-proposal-status Show Codebase Patch Proposal Renderer status")
        print("  codebase-patch-proposal <target> Prepare proposal-only patch packet")
        print("  codebase-patch-safety-packet <target> Prepare proposal-only patch safety packet")
        print("  codebase-validation-gate-status Show Codebase Validation Gate Planner status")
        print("  codebase-validation-gate-plan <target> Prepare proposal-only validation gate plan")
        print("  codebase-validation-preflight-gate <target> Prepare proposal-only preflight gate")
        print("  remember <text>      Save a memory")
        print("  recall               Show recent memories")
        print("  recall <limit>       Show recent memories with limit")
        print("  mem                  Alias for recall")
        print("  memory               Alias for recall")
        print("  daily-briefing-status Show Daily Project Briefing status")
        print("  daily-briefing       Show daily project briefing")
        print("  daily-briefing <n>   Show daily project briefing with limit")
        print("  daily-briefing-compact Show compact daily briefing")
        print("  daily-briefing-compact <n> Show compact daily briefing with limit")
        print("  daily-briefing-context Show daily briefing context")
        print("  daily-briefing-context <n> Show daily briefing context with limit")
        print("  memory-reflection-status Show Memory Reflection System status")
        print("  memory-reflect       Reflect on memory and journal")
        print("  memory-reflect <n>   Reflect with milestone limit")
        print("  memory-insights      Show reflection insights")
        print("  memory-insights <n>  Show reflection insights with limit")
        print("  memory-reflection-context Show reflection context")
        print("  memory-reflection-context <n> Show reflection context with limit")
        print("  memory-count         Show memory record count")
        print("  mem-count            Alias for memory-count")
        print("  memory-list          Show recent memories")
        print("  memory-list <limit>  Show recent memories with limit")
        print("  memory-delete <id>   Delete a memory by ID")
        print("  memory-pin <id>      Pin a memory")
        print("  mem-pin <id>         Alias for memory-pin")
        print("  memory-unpin <id>    Unpin a memory")
        print("  mem-unpin <id>       Alias for memory-unpin")
        print("  memory-importance <id> <1-5>  Set memory importance")
        print("  mem-importance <id> <1-5>     Alias for memory-importance")
        print("  memory-pinned        Show pinned memories")
        print("  mem-pinned           Alias for memory-pinned")
        print("  mem-delete <id>      Alias for memory-delete")
        print("  mem-list             Alias for memory-list")
        print("  chat <text>          Send a message to AURA")
        print("  ask <text>           Alias for chat")
        print("  history              Show recent chat history")
        print("  history <limit>      Show recent chat history with limit")
        print("  memory-search <text> Search relevant memories")
        print("  mem-search <text>    Alias for memory-search")
        print("  status               Show shell status")
        print("  version              Show AURA version")
        print("  journal              Show recent project journal entries")
        print("  journal <limit>      Show recent project journal entries with limit")
        print("  journal-add <text>   Add a project journal entry")
        print("  journal-count        Count project journal entries")
        print("  context <text>       Preview AURA context packet")
        print("  context-preview <text> Alias for context")
        print("  tool-sandbox-status  Show tool sandbox foundation status")
        print("  tool-sandbox-policy  Show tool sandbox policy")
        print("  tool-sandbox-check <cmd> Check command safety")
        print("  tool-sandbox-dry-run <cmd> Prepare dry-run plan")
        print("  model-router-status  Show model router foundation status")
        print("  model-router-routes  List model routes")
        print("  model-router-select <target> Select model route metadata")
        print("  core-loop-status     Show AURA alpha core loop status")
        print("  core-loop-run <text> Run alpha core loop safely")
        print("  core-loop-trace <text> Trace alpha core loop safely")
        print("  avatar-runtime-alpha-status Show Avatar Runtime Alpha status")
        print("  avatar-expression-plan <e> Prepare safe avatar expression plan")
        print("  avatar-gesture-plan <g>   Prepare safe avatar gesture plan")
        print("  avatar-runtime-context Show Avatar Runtime Alpha context")
        print("  avatar-status        Show avatar foundation status")
        print("  avatar-providers     Show avatar placeholder providers")
        print("  avatar-state         Show placeholder avatar state")
        print("  avatar-expression <e> Prepare expression proposal")
        print("  avatar-gesture <g>   Prepare gesture proposal")
        print("  desktop-alpha-status Show Desktop Assistant Alpha status")
        print("  desktop-action-plan <type> <target> Prepare safe desktop action plan")
        print("  desktop-open-app-plan <app> Prepare safe open app plan")
        print("  desktop-open-browser-plan <url> Prepare safe open browser plan")
        print("  desktop-open-file-plan <path> Prepare safe open file plan")
        print("  desktop-workspace-context Show desktop workspace context")
        print("  desktop-status       Show desktop bridge status")
        print("  desktop-capabilities Show desktop bridge capabilities")
        print("  desktop-action <a>   Prepare desktop action proposal")
        print("  system-status        Show unified AURA system status")
        print("  status-full          Alias for system-status")
        print("  vision-runtime-alpha-status Show Vision Runtime Alpha status")
        print("  vision-screen-plan   Prepare safe screen analysis plan")
        print("  vision-camera-plan   Prepare safe camera analysis plan")
        print("  vision-runtime-context Show Vision Runtime Alpha context")
        print("  vision-runtime-status Show vision runtime planning status")
        print("  vision-runtime-plan   Show screen/camera/model runtime plan")
        print("  vision-runtime-check  Run passive vision runtime dependency check")
        print("  active-permission-runtime-alpha-status Show Active Permission Runtime alpha status")
        print("  active-permission-runtime-status Show Active Permission Runtime contract status")
        print("  active-permission-runtime-check Run Active Permission Runtime contract check")
        print("  vision-status        Show vision foundation status")
        print("  vision-providers     Show vision provider placeholders")
        print("  safe-file-operation-status Show AURA Safe File Operation Planner status")
        print("  safe-file-read-plan <target> Prepare safe metadata-only file read plan")
        print("  safe-file-write-plan <target> Prepare safe file write proposal")
        print("  safe-file-edit-plan <target> Prepare safe file edit proposal")
        print("  safe-file-move-copy-delete-risk-review <target> Prepare safe move/copy/delete risk review")
        print("  safe-file-operation-checklist <target> Prepare safe file operation checklist")
        print("  safe-file-operation-context Show safe file operation planner context")
        print("  local-task-planner-status Show AURA Local Task Planner Alpha status")
        print("  local-task-intent-plan <target> Prepare safe local task intent plan")
        print("  local-task-breakdown-plan <target> Prepare safe local task breakdown plan")
        print("  local-task-risk-review <target> Prepare safe local task risk review")
        print("  local-task-execution-checklist <target> Prepare safe task execution checklist")
        print("  local-task-context Show local task planner context")
        print("  creative-assistant-status Show AURA Creative Assistant Foundation status")
        print("  creative-brief-plan <target> Prepare safe creative brief plan")
        print("  creative-character-concept-plan <target> Prepare character concept plan")
        print("  creative-visual-asset-plan <target> Prepare visual asset plan")
        print("  creative-content-idea-plan <target> Prepare content idea plan")
        print("  creative-review-plan <target> Prepare creative review plan")
        print("  creative-context Show creative assistant context")
        print("  project-intent-status Show AURA Project Intent Planner status")
        print("  project-intent-summary <topic> Show read-only project intent summary")
        print("  project-goal-plan <goal> Prepare safety-aware project goal plan")
        print("  sprint-intent-plan <goal> Prepare sprint intent plan")
        print("  project-next-action-candidates <topic> Prepare next action candidates")
        print("  project-intent-context Show project intent planner context")
        print("  workspace-memory-link-status Show AURA Workspace Memory Link status")
        print("  workspace-memory-summary Show read-only workspace memory summary")
        print("  workspace-memory-candidates <target> Prepare project memory candidates")
        print("  workspace-file-memory-candidates <target> Prepare important file memory candidates")
        print("  workspace-milestone-memory-candidates <target> Prepare milestone memory candidates")
        print("  workspace-memory-link-context Show workspace memory link context")
        print("  streaming-safety-status Show AURA Streaming Safety Foundation status")
        print("  streaming-context-plan <target> Prepare safe streaming context plan")
        print("  streaming-chat-safety-plan <target> Prepare safe chat safety plan")
        print("  streaming-content-boundary-plan <target> Prepare safe content boundary plan")
        print("  streaming-privacy-plan <target> Prepare safe privacy plan")
        print("  streaming-moderation-plan <target> Prepare safe moderation note plan")
        print("  streaming-safety-context Show streaming safety context")
        print("  game-companion-status Show AURA Game Companion Foundation status")
        print("  game-session-plan <target> Prepare safe game session plan")
        print("  game-strategy-plan <target> Prepare safe game strategy plan")
        print("  game-streaming-plan <target> Prepare streaming-safe game plan")
        print("  game-coaching-plan <target> Prepare safe game coaching plan")
        print("  game-context Show game companion context")
        print("  expression-language-status Show AURA Expression Language status")
        print("  expression-state Show AURA internal expression state")
        print("  expression-plan <text> Prepare safe expression plan")
        print("  expression-voice-hint <target> Prepare safe voice tone hint")
        print("  expression-avatar-hint <target> Prepare safe avatar expression hint")
        print("  expression-gesture-hint <target> Prepare safe gesture hint")
        print("  expression-context Show expression language context")
        print("  media-understanding-status Show AURA Media Understanding status")
        print("  media-asset-summary Show metadata-only media asset summary")
        print("  media-image-plan <goal> Prepare safe image description plan")
        print("  media-texture-reference-plan <goal> Prepare safe texture reference plan")
        print("  media-thumbnail-review-plan <goal> Prepare safe thumbnail/banner review plan")
        print("  media-video-plan <goal> Prepare safe video/audio plan")
        print("  media-context Show media understanding context")
        print("  blender-bridge-status Show AURA Blender Bridge Foundation status")
        print("  blender-scene-plan <goal> Prepare safe Blender scene plan")
        print("  blender-asset-plan <goal> Prepare safe Blender asset plan")
        print("  blender-texture-plan <goal> Prepare safe Blender texture/material plan")
        print("  blender-rigging-plan <goal> Prepare safe Blender rigging plan")
        print("  blender-animation-plan <goal> Prepare safe Blender animation plan")
        print("  blender-context     Show Blender bridge context")
        print("  workspace-status Alias for workspace-awareness-status")
        print("  workspace-awareness-status Show AURA Workspace Awareness status")
        print("  workspace-map        Show read-only AURA workspace map")
        print("  workspace-context    Show read-only AURA workspace context")
        print("  workspace-current-state Show current AURA workspace state")
        print("  workspace-important-files Show important AURA project files")
        print("  partner-alpha-status Show AURA Partner Alpha status")
        print("  partner-context      Show AURA Partner Alpha context")
        print("  partner-readiness    Show AURA Partner Alpha readiness")
        print("  partner-next-step    Show AURA Partner Alpha next step")
        print("  awakening-status     Show AURA Awakening Alpha status")
        print("  awaken               Alias for awakening-status")
        print("  voice-runtime-alpha-status Show Voice Runtime Alpha status")
        print("  voice-speak-plan <text> Prepare safe TTS speak plan")
        print("  voice-speak-test <text> Prepare speak test without playback")
        print("  voice-runtime-context Show Voice Runtime Alpha context")
        print("  voice-runtime-status Show voice runtime planning status")
        print("  voice-runtime-plan   Show STT/TTS runtime plan")
        print("  voice-runtime-check  Run passive voice runtime dependency check")
        print("  voice-status         Show voice foundation status")
        print("  voice-providers      Show voice provider placeholders")
        print("  project-code-status  Show Project Coding Assistant v2 status")
        print("  project-code-map     Show AST-based project code map")
        print("  project-code-inspect <path> Inspect code file")
        print("  project-code-plan <request> Prepare safe patch plan")
        print("  project-code-safety <cmd> Check command safety")
        print("  project-map          Show safe project map")
        print("  project-inspect <p>  Inspect safe project path")
        print("  project-find <text>  Search keyword in safe project files")
        print("  project-summary      Show project summary")
        print("  project-files        Show visible project files")
        print("  project-files <n>    Show visible project files with limit")
        print("  project-read <path>  Read safe project file")
        print("  action-request <name>       Prepare safe action request proposal")
        print("  action-request-check <name> Alias for action-request")
        print("  plugin-actions       Show plugin action registry")
        print("  plugin-action <name> Show plugin action detail")
        print("  plugin-action-check <name> Check plugin action permission")
        print("  skills               Show AURA skill registry")
        print("  skill <name>         Show skill detail")
        print("  skill-check <name>   Check skill permission")
        print("  permissions          Show permission policy table")
        print("  permission-check <action>  Check permission for an action")
        print("  perm-check <action>        Alias for permission-check")
        print("  provider             Show reasoning provider")
        print("  roles                Show AURA internal roles")
        print("  reason               Alias for provider")
        print("  provider-check       Check reasoning provider runtime")
        print("  reason-check         Alias for provider-check")
        print("  plugins              Show loaded plugins")
        print("  plugin               Alias for plugins")
        print("  health               Show shell health summary")
        print("  clear                Clear the terminal screen")
        print("  cls                  Alias for clear")
        print("  exit                 Exit AURA shell")
        print("  quit                 Alias for exit")
        print("  q                    Alias for exit")

    def load_identity(self) -> dict:
        if not self.identity_path.exists():
            return {}

        with self.identity_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def load_settings(self) -> dict:
        if not self.settings_path.exists():
            return {}

        with self.settings_path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def configured_provider_name(self) -> str:
        settings = self.load_settings()
        reasoning = settings.get("reasoning", {})
        return reasoning.get("provider", "unknown")

    def ensure_plugins_loaded(self) -> None:
        if self.plugins_loaded:
            return

        self.plugin_manager.register(EchoPlugin())
        self.plugin_manager.register(MemoryPlugin(project_root=self.project_root))
        self.plugin_manager.start_all()

        self.plugins_loaded = True

    def remember(self, content: str) -> None:
        if not content.strip():
            print("Nothing to remember.")
            return

        memory = MemoryItem(
            kind="user_note",
            content=content.strip(),
            metadata={
                "source": "AuraShell",
            },
        )

        self.memory_store.save(memory)

        print("Memory saved.")

    def recall(self, limit: int = 5) -> None:
        memories = self.memory_store.list_recent(limit=limit)

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
        response = self.chat_engine.respond(message, source="AuraShell")
        print(response)

    def history(self, limit: int = 5) -> None:
        turns = self.chat_engine.recent_conversations(limit=limit)

        print("AURA Chat History")
        print("=================")

        if not turns:
            print("No chat history found.")
            return

        for turn in turns:
            print(f"User: {turn.user_message}")
            print(f"AURA: {turn.aura_response}")
            print("---")

    def memory_count(self) -> None:
        count = self.memory_store.count()

        print("AURA Memory Count")
        print("=================")
        print(f"Records: {count}")

    def memory_list(self, limit: int = 5) -> None:
        memories = self.memory_store.list_recent(limit=limit)

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

    def memory_pin(self, memory_id: str) -> None:
        memory = self.memory_store.set_pinned(memory_id=memory_id, pinned=True)

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
        memory = self.memory_store.set_pinned(memory_id=memory_id, pinned=False)

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
        print("AURA Memory Importance")
        print("======================")

        try:
            memory = self.memory_store.set_importance(
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
        memories = self.memory_store.list_pinned()

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

    def memory_delete(self, memory_id: str) -> None:
        memory = self.memory_store.find_by_id(memory_id=memory_id)

        print("AURA Memory Delete")
        print("==================")

        if memory is None:
            print(f"Memory not found: {memory_id}")
            return

        if self.memory_store.is_protected(memory):
            print("Cannot delete protected system memory.")
            pinned = bool(memory.metadata.get("pinned", False))
            importance = memory.metadata.get("importance", 3)
            print(f"- ID: {memory.id}")
            print(f"  Kind: {memory.kind}")
            print(f"  Pinned: {pinned}")
            print(f"  Importance: {importance}")
            print(f"  Content: {memory.content}")
            return

        deleted_memory = self.memory_store.delete_by_id(memory_id=memory_id)

        if deleted_memory is None:
            print(f"Memory not found: {memory_id}")
            return

        print("Deleted memory:")
        print(f"- ID: {deleted_memory.id}")
        print(f"  Kind: {deleted_memory.kind}")
        print(f"  Content: {deleted_memory.content}")

    def memory_search(self, query: str, limit: int = 5) -> None:
        memories = self.chat_engine.relevant_memories(message=query, limit=limit)

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

    def status(self) -> None:
        memory_count = self.memory_store.count()
        provider = self.chat_engine.provider_info()

        print("AURA Shell Status")
        print("=================")
        print("Shell   : ONLINE")
        print("Memory  : ONLINE")
        print("Chat    : ONLINE")
        print(f"Reason  : {provider['name']} v{provider['version']}")
        print(f"Records : {memory_count}")

    def version(self) -> None:
        identity = self.load_identity()

        name = identity.get("name", "AURA")
        version = identity.get("version", "unknown")
        codename = identity.get("codename", "unknown")
        motto = identity.get("motto", "Grow Together")

        print("AURA Version")
        print("============")
        print(f"Name     : {name}")
        print(f"Version  : {version}")
        print(f"Codename : {codename}")
        print(f"Motto    : {motto}")

    def provider(self) -> None:
        provider = self.chat_engine.provider_info()
        configured_provider = self.configured_provider_name()

        print("AURA Reasoning Provider")
        print("=======================")
        print(f"Name    : {provider['name']}")
        print(f"Version : {provider['version']}")
        print(f"Config  : {configured_provider}")

    def provider_check(self) -> None:
        runtime = self.chat_engine.provider_runtime_check()

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

    def journal(self, limit: int = 5) -> None:
        project_journal = ProjectJournal(project_root=self.project_root)
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
        project_journal = ProjectJournal(project_root=self.project_root)

        title = "Manual Entry"
        if ":" in content:
            title = content.split(":", 1)[0].strip() or "Manual Entry"

        entry = project_journal.add(
            title=title,
            content=content,
            metadata={"source": "shell"},
        )

        print("AURA Project Journal")
        print("====================")
        print("Journal entry saved.")
        print(f"- ID: {entry.id}")
        print(f"  Title: {entry.title}")
        print(f"  Content: {entry.content}")

    def journal_count(self) -> None:
        project_journal = ProjectJournal(project_root=self.project_root)

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

    def context(self, message: str) -> None:
        context_manager = ContextManager(project_root=self.project_root)
        packet = context_manager.build(user_message=message)

        print(packet.to_text())

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


    def active_permission_runtime_alpha_status(self) -> None:
        from aura.permissions.active_permission_runtime_alpha_manager import (
            ActivePermissionRuntimeAlphaManager,
        )

        manager = ActivePermissionRuntimeAlphaManager()
        status = manager.status()

        print("AURA Permission and Action Runtime Stabilization Alpha")
        print("=====================================================")

        def row(label: str, key: str, fallback: object = "n/a") -> None:
            print(f"{label:<46}: {status.get(key, fallback)}")

        rows = [
            ("Name", "name"),
            ("Version", "version"),
            ("Status", "status"),
            ("Planning Ready", "planning_ready"),
            ("Runtime Ready", "runtime_ready"),
            ("S220 Stabilization Ready", "sprint_220_permission_action_runtime_stabilization_contract_ready"),
            ("S220 Stabilization Runtime", "permission_action_runtime_stabilization_runtime_ready"),
            ("S220 Stabilization Status", "permission_action_runtime_stabilization_status"),
            ("Current Sprint", "permission_action_current_sprint"),
            ("Next Sprint", "permission_action_next_sprint"),
            ("Next Boundary", "permission_action_next_boundary"),
            ("Block Complete", "permission_action_block_complete"),
            ("Block Stabilized", "permission_action_block_stabilized"),
            ("Contract Chain Stable", "permission_action_contract_chain_stable"),
            ("Runtime Zero Counters Stable", "permission_action_runtime_zero_counters_stable"),
            ("Safety Blockers Stable", "permission_action_safety_blockers_stable"),
            ("Stabilized Contract Count", "stabilized_permission_action_contract_count"),
            ("Expected Contract Count", "expected_permission_action_contract_count"),
            ("Allowed Stabilization Profiles", "allowed_stabilization_profile_count"),
            ("Blocked Stabilization Targets", "blocked_stabilization_target_count"),
            ("Runtime Gate Open Allowed", "permission_action_runtime_gate_open_allowed"),
            ("Release Gate Open Allowed", "permission_action_release_gate_open_allowed"),
            ("Runtime Activation Allowed", "permission_action_runtime_activation_allowed"),
            ("Permission Mutation Allowed", "permission_state_mutation_allowed"),
            ("Audit Write Allowed", "audit_write_allowed"),
            ("Action Dispatch Allowed", "action_execution_dispatch_allowed"),
            ("Command Execution Allowed", "command_execution_allowed"),
            ("Tool Execution Allowed", "tool_execution_allowed"),
            ("File Mutation Allowed", "file_mutation_allowed"),
            ("Desktop Action Allowed", "desktop_action_allowed"),
            ("Application Launch Allowed", "application_launch_allowed"),
            ("Runtime Gate Opened", "permission_action_runtime_gate_opened"),
            ("Release Gate Opened", "permission_action_release_gate_opened"),
            ("Runtime Activated", "permission_action_runtime_activated"),
            ("Permission State Mutated", "permission_state_mutated"),
            ("Permission Grant Created", "permission_grant_created"),
            ("Audit Event Written", "audit_event_written"),
            ("Action Executed", "action_executed"),
            ("Command Executed", "command_executed"),
            ("Tool Executed", "tool_executed"),
            ("File Mutated", "file_mutated"),
            ("Desktop Action Executed", "desktop_action_executed"),
            ("Application Launched", "application_launched"),
            ("Rollback Executed", "rollback_executed"),
            ("Emergency Stop Applied", "emergency_stop_applied"),
            ("Recovery Action Dispatched", "recovery_action_dispatched"),
            ("No Runtime Gate Open", "no_permission_action_runtime_gate_open"),
            ("No Release Gate Open", "no_permission_action_release_gate_open"),
            ("No Runtime Activation", "no_permission_action_runtime_activation"),
            ("No Permission Mutation", "no_permission_state_mutation"),
            ("No Audit Write", "no_audit_write"),
            ("No Action Dispatch", "no_action_execution_dispatch"),
            ("No Action Execution", "no_action_execution"),
            ("No Command Execution", "no_command_execution"),
            ("No Tool Execution", "no_tool_execution"),
            ("No File Mutation", "no_file_mutation"),
            ("No Desktop Action", "no_desktop_action"),
            ("No Application Launch", "no_application_launch"),
            ("No Rollback Execution", "no_rollback_execution"),
            ("No Emergency Stop Apply", "no_emergency_stop_apply"),
            ("No Recovery Action Dispatch", "no_recovery_action_dispatch"),
            ("No Autonomous Action", "no_autonomous_action"),
            ("Safety Blocker Count", "safety_blocker_count"),
            ("All Safety Blockers Off", "all_safety_blockers_inactive"),
            ("Assertion Count", "assertion_count"),
            ("Failed Assertion Count", "failed_assertion_count"),
            ("Runtime Scope", "runtime_scope"),
        ]

        for label, key in rows:
            row(label, key)

        print()
        print("Failed Assertions")
        print("-----------------")
        failed = status.get("failed_assertions", [])
        if failed:
            for item in failed:
                print(f"- {item}")
        else:
            print("- none")

        print()
        print(status.get("note", ""))

    def active_permission_runtime_status(self) -> None:
        from aura.permissions.active_permission_runtime_planner import (
            ActivePermissionRuntimePlanner,
        )

        planner = ActivePermissionRuntimePlanner()
        status = planner.status()

        print("AURA Permission and Action Runtime Stabilization Status")
        print("======================================================")

        def row(label: str, key: str, fallback: object = "n/a") -> None:
            print(f"{label:<48}: {status.get(key, fallback)}")

        rows = [
            ("Name", "name"),
            ("Version", "version"),
            ("Status", "status"),
            ("Planning Ready", "planning_ready"),
            ("Runtime Ready", "runtime_ready"),
            ("Contract Ready", "permission_action_runtime_stabilization_contract_ready"),
            ("S220 Stabilization Runtime", "permission_action_runtime_stabilization_runtime_ready"),
            ("Runtime Status", "permission_action_runtime_stabilization_status"),
            ("Current Sprint", "permission_action_current_sprint"),
            ("Next Sprint", "permission_action_next_sprint"),
            ("Next Boundary", "permission_action_next_boundary"),
            ("Block Complete", "permission_action_block_complete"),
            ("Block Stabilized", "permission_action_block_stabilized"),
            ("Block Release Ready", "permission_action_block_release_ready"),
            ("Contract Chain Stable", "permission_action_contract_chain_stable"),
            ("Runtime Zero Counters Stable", "permission_action_runtime_zero_counters_stable"),
            ("Safety Blockers Stable", "permission_action_safety_blockers_stable"),
            ("Stabilized Contract Count", "stabilized_permission_action_contract_count"),
            ("Expected Contract Count", "expected_permission_action_contract_count"),
            ("Stabilization Review Required", "stabilization_review_required"),
            ("Contract Chain Review Required", "contract_chain_review_required"),
            ("Zero Counter Review Required", "runtime_zero_counter_review_required"),
            ("Safety Blocker Review Required", "safety_blocker_review_required"),
            ("Release Gate Review Required", "release_gate_review_required"),
            ("Next Block Handoff Required", "next_block_handoff_review_required"),
            ("Summary Schema", "permission_action_stabilization_summary_schema_ready"),
            ("Contract Chain Schema", "permission_action_contract_chain_schema_ready"),
            ("Zero Counter Schema", "permission_action_runtime_zero_counter_schema_ready"),
            ("Safety Blocker Schema", "permission_action_safety_blocker_register_schema_ready"),
            ("Release Gate Schema", "permission_action_release_gate_schema_ready"),
            ("Next Block Handoff Schema", "permission_action_next_block_handoff_schema_ready"),
            ("Allowed Stabilization Profiles", "allowed_stabilization_profile_count"),
            ("Blocked Stabilization Targets", "blocked_stabilization_target_count"),
            ("Runtime Gate Open Allowed", "permission_action_runtime_gate_open_allowed"),
            ("Release Gate Open Allowed", "permission_action_release_gate_open_allowed"),
            ("Runtime Activation Allowed", "permission_action_runtime_activation_allowed"),
            ("Permission Mutation Allowed", "permission_state_mutation_allowed"),
            ("Grant Creation Allowed", "grant_packet_creation_allowed"),
            ("Audit Write Allowed", "audit_write_allowed"),
            ("Action Dispatch Allowed", "action_execution_dispatch_allowed"),
            ("Command Execution Allowed", "command_execution_allowed"),
            ("Tool Execution Allowed", "tool_execution_allowed"),
            ("File Mutation Allowed", "file_mutation_allowed"),
            ("Desktop Action Allowed", "desktop_action_allowed"),
            ("Application Launch Allowed", "application_launch_allowed"),
            ("Rollback Execution Allowed", "rollback_execution_allowed"),
            ("Emergency Stop Apply Allowed", "emergency_stop_apply_allowed"),
            ("Recovery Action Dispatch Allowed", "recovery_action_dispatch_allowed"),
            ("Runtime Gate Opened", "permission_action_runtime_gate_opened"),
            ("Release Gate Opened", "permission_action_release_gate_opened"),
            ("Runtime Activated", "permission_action_runtime_activated"),
            ("Permission State Mutated", "permission_state_mutated"),
            ("Permission Grant Created", "permission_grant_created"),
            ("Audit Event Written", "audit_event_written"),
            ("Action Executed", "action_executed"),
            ("Command Executed", "command_executed"),
            ("Tool Executed", "tool_executed"),
            ("File Mutated", "file_mutated"),
            ("Desktop Action Executed", "desktop_action_executed"),
            ("Application Launched", "application_launched"),
            ("Rollback Executed", "rollback_executed"),
            ("Emergency Stop Applied", "emergency_stop_applied"),
            ("Recovery Action Dispatched", "recovery_action_dispatched"),
            ("No Runtime Gate Open", "no_permission_action_runtime_gate_open"),
            ("No Release Gate Open", "no_permission_action_release_gate_open"),
            ("No Runtime Activation", "no_permission_action_runtime_activation"),
            ("No Permission Mutation", "no_permission_state_mutation"),
            ("No Audit Write", "no_audit_write"),
            ("No Action Dispatch", "no_action_execution_dispatch"),
            ("No Action Execution", "no_action_execution"),
            ("No Command Execution", "no_command_execution"),
            ("No Tool Execution", "no_tool_execution"),
            ("No File Mutation", "no_file_mutation"),
            ("No Desktop Action", "no_desktop_action"),
            ("No Application Launch", "no_application_launch"),
            ("No Rollback Execution", "no_rollback_execution"),
            ("No Emergency Stop Apply", "no_emergency_stop_apply"),
            ("No Recovery Action Dispatch", "no_recovery_action_dispatch"),
            ("No Autonomous Action", "no_autonomous_action"),
            ("Safety Blocker Count", "safety_blocker_count"),
            ("All Safety Blockers Off", "all_safety_blockers_inactive"),
            ("Runtime Scope", "runtime_scope"),
        ]

        for label, key in rows:
            row(label, key)

        print()
        print(status.get("note", ""))

    def active_permission_runtime_check(self) -> None:
        from aura.permissions.active_permission_runtime_planner import (
            ActivePermissionRuntimePlanner,
        )

        planner = ActivePermissionRuntimePlanner()
        check = planner.check()
        contract = check.get("permission_action_runtime_stabilization_contract", {})

        print("AURA Permission and Action Runtime Stabilization Check")
        print("=====================================================")
        print(f"Status                 : {check.get('status')}")
        print(f"Planning Ready         : {check.get('planning_ready')}")
        print(f"Runtime Ready          : {check.get('runtime_ready')}")
        print(f"Assertion Count        : {check.get('assertion_count')}")
        print(f"Failed Assertion Count : {check.get('failed_assertion_count')}")
        print()
        print("Sprint 220 Permission and Action Runtime Stabilization")
        print("------------------------------------------------------")

        def row(label: str, key: str) -> None:
            print(f"{label:<52}: {contract.get(key)}")

        sprint_rows = [
            ("Contract Ready", "permission_action_runtime_stabilization_contract_ready"),
            ("Runtime Ready", "permission_action_runtime_stabilization_runtime_ready"),
            ("Runtime Status", "permission_action_runtime_stabilization_status"),
            ("S220 Stabilization Ready", "permission_action_runtime_stabilization_contract_ready"),
            ("S220 Stabilization Runtime", "permission_action_runtime_stabilization_runtime_ready"),
            ("Current Sprint", "permission_action_current_sprint"),
            ("Next Sprint", "permission_action_next_sprint"),
            ("Next Boundary", "permission_action_next_boundary"),
            ("Block Complete", "permission_action_block_complete"),
            ("Block Stabilized", "permission_action_block_stabilized"),
            ("Block Release Ready", "permission_action_block_release_ready"),
            ("Contract Only", "contract_only"),
            ("Runtime Ready Flag", "runtime_ready"),
            ("Runtime Gate Open", "runtime_gate_open"),
            ("Runtime Activation Allowed", "runtime_activation_allowed"),
            ("Release Gate Open", "release_gate_open"),
            ("Default Deny", "default_deny"),
            ("Default Grant", "default_grant"),
            ("Contract Chain Stable", "permission_action_contract_chain_stable"),
            ("Runtime Zero Counters Stable", "permission_action_runtime_zero_counters_stable"),
            ("Safety Blockers Stable", "permission_action_safety_blockers_stable"),
            ("CLI Visibility Stable", "permission_action_cli_visibility_stable"),
            ("Stabilized Contract Count", "stabilized_permission_action_contract_count"),
            ("Expected Contract Count", "expected_permission_action_contract_count"),
            ("Stabilization Review Required", "stabilization_review_required"),
            ("Block Completion Review Required", "block_completion_review_required"),
            ("Contract Chain Review Required", "contract_chain_review_required"),
            ("Zero Counter Review Required", "runtime_zero_counter_review_required"),
            ("Safety Blocker Review Required", "safety_blocker_review_required"),
            ("Release Gate Review Required", "release_gate_review_required"),
            ("Next Block Handoff Review Required", "next_block_handoff_review_required"),
            ("Summary Schema", "permission_action_stabilization_summary_schema_ready"),
            ("Contract Chain Schema", "permission_action_contract_chain_schema_ready"),
            ("Zero Counter Schema", "permission_action_runtime_zero_counter_schema_ready"),
            ("Safety Blocker Schema", "permission_action_safety_blocker_register_schema_ready"),
            ("Release Gate Schema", "permission_action_release_gate_schema_ready"),
            ("CLI Surface Schema", "permission_action_cli_surface_schema_ready"),
            ("Docs Version Schema", "permission_action_docs_version_schema_ready"),
            ("Next Block Handoff Schema", "permission_action_next_block_handoff_schema_ready"),
            ("Allowed Stabilization Profile Count", "allowed_stabilization_profile_count"),
            ("Blocked Stabilization Target Count", "blocked_stabilization_target_count"),
            ("Runtime Gate Open Allowed", "permission_action_runtime_gate_open_allowed"),
            ("Release Gate Open Allowed", "permission_action_release_gate_open_allowed"),
            ("Runtime Activation Allowed", "permission_action_runtime_activation_allowed"),
            ("Permission Mutation Allowed", "permission_state_mutation_allowed"),
            ("Permission Persistence Allowed", "permission_state_persistence_allowed"),
            ("Grant Creation Allowed", "grant_packet_creation_allowed"),
            ("Grant Persistence Allowed", "grant_persistence_allowed"),
            ("Audit Event Creation Allowed", "audit_event_packet_creation_allowed"),
            ("Audit Write Allowed", "audit_write_allowed"),
            ("Audit Persistence Allowed", "audit_persistence_allowed"),
            ("Action Dispatch Allowed", "action_execution_dispatch_allowed"),
            ("Command Execution Allowed", "command_execution_allowed"),
            ("Tool Execution Allowed", "tool_execution_allowed"),
            ("File Mutation Allowed", "file_mutation_allowed"),
            ("Desktop Action Allowed", "desktop_action_allowed"),
            ("Application Launch Allowed", "application_launch_allowed"),
            ("Safe Local Open Runtime", "local_open_action_runtime_ready"),
            ("Application Launch Runtime", "application_launch_runtime_ready"),
            ("Controlled Creation Runtime", "controlled_creation_runtime_ready"),
            ("Rollback Execution Allowed", "rollback_execution_allowed"),
            ("Emergency Stop Apply Allowed", "emergency_stop_apply_allowed"),
            ("Recovery Action Dispatch Allowed", "recovery_action_dispatch_allowed"),
        ]

        safety_rows = [
            ("Stabilization Summary Created", "permission_action_stabilization_summary_created"),
            ("Contract Chain Review Created", "permission_action_contract_chain_review_created"),
            ("Zero Counter Review Created", "permission_action_runtime_zero_counter_review_created"),
            ("Safety Blocker Review Created", "permission_action_safety_blocker_review_created"),
            ("Release Gate Review Created", "permission_action_release_gate_review_created"),
            ("Next Block Handoff Created", "permission_action_next_block_handoff_created"),
            ("Runtime Gate Opened", "permission_action_runtime_gate_opened"),
            ("Release Gate Opened", "permission_action_release_gate_opened"),
            ("Runtime Activated", "permission_action_runtime_activated"),
            ("Permission State Mutated", "permission_state_mutated"),
            ("Permission Grant Created", "permission_grant_created"),
            ("Audit Event Created", "audit_event_created"),
            ("Audit Event Written", "audit_event_written"),
            ("Audit Log Appended", "audit_log_appended"),
            ("Action Proposal Created", "action_proposal_created"),
            ("Action Preview Created", "action_preview_created"),
            ("Action Enqueued", "action_enqueued"),
            ("Action Executed", "action_executed"),
            ("Command Executed", "command_executed"),
            ("Tool Executed", "tool_executed"),
            ("File Mutated", "file_mutated"),
            ("Desktop Action Executed", "desktop_action_executed"),
            ("Application Launched", "application_launched"),
            ("Folder Created", "folder_created"),
            ("Simple File Created", "simple_file_created"),
            ("File Written", "file_written"),
            ("Rollback Executed", "rollback_executed"),
            ("Emergency Stop Applied", "emergency_stop_applied"),
            ("Recovery Action Dispatched", "recovery_action_dispatched"),
            ("Network Action Executed", "network_action_executed"),
            ("Git Action Executed", "git_action_executed"),
            ("Memory Written", "memory_written"),
            ("External Upload Performed", "external_upload_performed"),
            ("Cloud Fallback Used", "cloud_fallback_used"),
            ("Autonomous Action Performed", "autonomous_action_performed"),
            ("No Runtime Gate Open", "no_permission_action_runtime_gate_open"),
            ("No Release Gate Open", "no_permission_action_release_gate_open"),
            ("No Runtime Activation", "no_permission_action_runtime_activation"),
            ("No Permission Mutation", "no_permission_state_mutation"),
            ("No Audit Write", "no_audit_write"),
            ("No Action Dispatch", "no_action_execution_dispatch"),
            ("No Action Execution", "no_action_execution"),
            ("No Command Execution", "no_command_execution"),
            ("No Tool Execution", "no_tool_execution"),
            ("No File Mutation", "no_file_mutation"),
            ("No Desktop Action", "no_desktop_action"),
            ("No Application Launch", "no_application_launch"),
            ("No Rollback Execution", "no_rollback_execution"),
            ("No Emergency Stop Apply", "no_emergency_stop_apply"),
            ("No Recovery Action Dispatch", "no_recovery_action_dispatch"),
            ("No Autonomous Action", "no_autonomous_action"),
            ("Safety Blocker Count", "safety_blocker_count"),
            ("All Safety Blockers Off", "all_safety_blockers_inactive"),
        ]

        for label, key in sprint_rows:
            row(label, key)

        print()
        print("Permission and Action Runtime Stabilization Safety State")
        print("--------------------------------------------------------")
        for label, key in safety_rows:
            row(label, key)

        print()
        print("Failed Assertions")
        print("-----------------")
        failed = check.get("failed_assertions", [])
        if failed:
            for item in failed:
                print(f"- {item}")
        else:
            print("- none")

        print()
        print(check.get("note", ""))

    def vision_runtime_status(self) -> None:
        planner = VisionRuntimePlanner(project_root=Path.cwd())
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
        print(f"Vision Model Candidates: {status['vision_model_candidates']}")
        print(f"Candidate Count      : {status['candidate_count']}")
        print(f"Vision Activation Contract: {status['vision_runtime_activation_contract_ready']}")
        print(f"Vision Activation Runtime : {status['vision_runtime_activation_runtime_ready']}")
        print(f"Vision Activation Status  : {status['vision_runtime_activation_status']}")
        print(f"Explicit Screenshot Contract: {status['explicit_screenshot_capture_contract_ready']}")
        print(f"Explicit Screenshot Runtime : {status['explicit_screenshot_capture_runtime_ready']}")
        print(f"Explicit Screenshot Status  : {status['explicit_screenshot_capture_status']}")
        print(f"Screen Context Contract     : {status['screen_context_adapter_contract_ready']}")
        print(f"Screen Context Runtime      : {status['screen_context_adapter_runtime_ready']}")
        print(f"Screen Context Status       : {status['screen_context_adapter_status']}")
        print(f"Local Vision Model Contract : {status['local_vision_model_adapter_contract_ready']}")
        print(f"Local Vision Model Runtime  : {status['local_vision_model_adapter_runtime_ready']}")
        print(f"Local Vision Model Status   : {status['local_vision_model_adapter_status']}")
        print(f"Vision Permission Contract  : {status['vision_permission_redaction_contract_ready']}")
        print(f"Vision Permission Runtime   : {status['vision_permission_redaction_runtime_ready']}")
        print(f"Vision Permission Status    : {status['vision_permission_redaction_status']}")
        print(f"Workspace Visual Contract   : {status['workspace_visual_understanding_contract_ready']}")
        print(f"Workspace Visual Runtime    : {status['workspace_visual_understanding_runtime_ready']}")
        print(f"Workspace Visual Status     : {status['workspace_visual_understanding_status']}")
        print(f"Vision Chat Handoff Contract: {status['vision_to_chat_context_handoff_contract_ready']}")
        print(f"Vision Chat Handoff Runtime : {status['vision_to_chat_context_handoff_runtime_ready']}")
        print(f"Vision Chat Handoff Status  : {status['vision_to_chat_context_handoff_status']}")
        print(f"Control Center Vision Panel Contract: {status['control_center_vision_panel_contract_ready']}")
        print(f"Control Center Vision Panel Runtime : {status['control_center_vision_panel_runtime_ready']}")
        print(f"Control Center Vision Panel Status  : {status['control_center_vision_panel_status']}")
        print(f"Vision Runtime Integration Review Contract: {status['vision_runtime_integration_review_contract_ready']}")
        print(f"Vision Runtime Integration Review Runtime : {status['vision_runtime_integration_review_runtime_ready']}")
        print(f"Vision Runtime Integration Review Status  : {status['vision_runtime_integration_review_status']}")
        print(f"Vision Runtime Stabilization Contract: {status['vision_runtime_stabilization_contract_ready']}")
        print(f"Vision Runtime Stabilization Runtime : {status['vision_runtime_stabilization_runtime_ready']}")
        print(f"Vision Runtime Stabilization Status  : {status['vision_runtime_stabilization_status']}")
        print(f"Vision Block 201-210 Complete        : {status['vision_runtime_block_201_210_complete']}")
        print(f"Vision Block 201-210 Stabilized      : {status['vision_runtime_block_201_210_stabilized']}")
        print(f"Vision Block Start        : {status['vision_runtime_block_start']}")
        print(f"Vision Block End          : {status['vision_runtime_block_end']}")
        print(f"Vision Current Sprint     : {status['vision_runtime_current_sprint']}")
        print(f"Vision Next Sprint        : {status['vision_runtime_next_sprint']}")
        print(f"Vision Next Boundary      : {status['vision_runtime_next_boundary']}")
        print(f"Vision Activation Allowed : {status['vision_runtime_activation_allowed']}")
        print(f"Vision Release Gate Open  : {status['vision_release_gate_open']}")
        print(f"Vision Safe Idle Default  : {status['vision_safe_idle_default']}")
        print(f"Explicit Visual Input     : {status['vision_explicit_visual_input_required']}")
        print(f"Explicit Confirmation     : {status['vision_explicit_user_confirmation_required']}")
        print(f"Explicit Screenshot Request: {status['explicit_screenshot_request_required']}")
        print(f"Explicit Screenshot Confirm: {status['explicit_screenshot_confirmation_required']}")
        print(f"Permission Before Screen  : {status['vision_permission_required_before_screen']}")
        print(f"Permission Before Camera  : {status['vision_permission_required_before_camera']}")
        print(f"Permission Before Analysis: {status['vision_permission_required_before_image_analysis']}")
        print(f"Permission Before Action  : {status['vision_permission_required_before_visual_action']}")
        print(f"Permission Before Screenshot: {status['permission_required_before_screenshot']}")
        print(f"Screen Permission Action  : {status['vision_screen_permission_action']}")
        print(f"Camera Permission Action  : {status['vision_camera_permission_action']}")
        print(f"Screenshot Runtime Ready  : {status['screenshot_capture_runtime_ready']}")
        print(f"Screenshot Capture Done   : {status['screenshot_capture_performed']}")
        print(f"Screenshot Output Created : {status['screenshot_output_file_created']}")
        print(f"Screen Context Packet Created: {status['screen_context_packet_created']}")
        print(f"Screen Context Handoff    : {status['screen_context_handoff_active']}")
        print(f"Local Vision Adapter Active: {status['local_vision_model_adapter_active']}")
        print(f"Local Model Request Active : {status['local_model_request_active']}")
        print(f"Local Model Inference Active: {status['local_model_inference_active']}")
        print(f"Model Chat Handoff Active : {status['model_to_chat_handoff_active']}")
        print(f"Permission Prompt Runtime : {status['permission_prompt_runtime_active']}")
        print(f"Permission Grant Mutation : {status['permission_grant_mutation_active']}")
        print(f"Redaction Runtime Active  : {status['redaction_runtime_active']}")
        print(f"Redacted Context Created  : {status['redacted_context_created']}")
        print(f"Redaction Audit Write     : {status['redaction_audit_write_active']}")
        print(f"Provided Redacted Visual Context: {status['provided_redacted_visual_context_required']}")
        print(f"Provided Workspace Metadata: {status['provided_workspace_metadata_required']}")
        print(f"Provided User Question    : {status['provided_user_question_required']}")
        print(f"Provided Permission Packet: {status['provided_permission_packet_required']}")
        print(f"Redaction Proof Required  : {status['redaction_proof_required']}")
        print(f"Workspace Summary Schema  : {status['workspace_visual_summary_schema_ready']}")
        print(f"Workspace Layout Schema   : {status['workspace_layout_schema_ready']}")
        print(f"Visual Element Schema     : {status['visual_element_schema_ready']}")
        print(f"Workspace Risk Schema     : {status['workspace_risk_schema_ready']}")
        print(f"Workspace Understanding Runtime: {status['workspace_visual_understanding_runtime_active']}")
        print(f"Workspace Summary Created : {status['workspace_visual_summary_created']}")
        print(f"Workspace Chat Handoff    : {status['workspace_to_chat_handoff_active']}")
        print(f"Chat Safe Visual Packet Schema: {status['chat_safe_visual_context_packet_schema_ready']}")
        print(f"Chat Safe Visual Summary Schema: {status['chat_safe_visual_summary_schema_ready']}")
        print(f"Chat Safe Workspace Summary Schema: {status['chat_safe_workspace_summary_schema_ready']}")
        print(f"Chat Context Handoff Packet Schema: {status['chat_context_handoff_packet_schema_ready']}")
        print(f"Chat Source Attribution Schema: {status['chat_source_attribution_schema_ready']}")
        print(f"Chat Limitation Schema    : {status['chat_limitation_schema_ready']}")
        print(f"Chat Uncertainty Schema   : {status['chat_uncertainty_schema_ready']}")
        print(f"Chat Risk Notice Schema   : {status['chat_risk_notice_schema_ready']}")
        print(f"Chat Handoff Preview Schema: {status['chat_handoff_preview_schema_ready']}")
        print(f"Chat Visible Disclosure Contract: {status['chat_visible_disclosure_contract_ready']}")
        print(f"Chat Render Boundary Contract: {status['chat_render_boundary_contract_ready']}")
        print(f"Permission Before Chat Context Injection: {status['permission_required_before_chat_context_injection']}")
        print(f"Permission Before Chat Session Write: {status['permission_required_before_chat_session_write']}")
        print(f"Redaction Before Chat Context Packet: {status['redaction_required_before_chat_context_packet']}")
        print(f"Redaction Before Chat Session Write: {status['redaction_required_before_chat_session_write']}")
        print(f"Explicit User Request For Handoff: {status['explicit_user_request_required_for_handoff']}")
        print(f"Explicit Confirmation For Handoff: {status['explicit_confirmation_required_for_handoff']}")
        print(f"Foreground Chat Session Required: {status['foreground_chat_session_required']}")
        print(f"No Hidden Visual Context Injection: {status['no_hidden_visual_context_injection']}")
        print(f"No Automatic Chat Handoff: {status['no_automatic_chat_handoff']}")
        print(f"No Chat Model Request Without User Message: {status['no_chat_model_request_without_user_message']}")
        print(f"No Memory Write From Visual Handoff: {status['no_memory_write_from_visual_handoff']}")
        print(f"Vision Chat Handoff Runtime: {status['vision_to_chat_context_handoff_runtime_active']}")
        print(f"Chat Context Packet Created: {status['chat_context_packet_created']}")
        print(f"Chat Safe Visual Summary Created: {status['chat_safe_visual_summary_created']}")
        print(f"Chat Source Attribution Created: {status['chat_source_attribution_created']}")
        print(f"Chat Handoff Preview Created: {status['chat_handoff_preview_created']}")
        print(f"Chat Message Injection Active: {status['chat_message_injection_active']}")
        print(f"Chat Session Write Active: {status['chat_session_write_active']}")
        print(f"Chat Model Request Active: {status['chat_model_request_active']}")
        print(f"Chat Response Generation Active: {status['chat_response_generation_active']}")
        print(f"Read Only Vision Panel Contract: {status['read_only_panel_contract_ready']}")
        print(f"Display Only Vision Panel Contract: {status['display_only_panel_contract_ready']}")
        print(f"Control Center Visible Panel Schema: {status['control_center_visible_panel_schema_ready']}")
        print(f"Vision Status Panel Schema: {status['vision_status_panel_schema_ready']}")
        print(f"Vision Safety Panel Schema: {status['vision_safety_panel_schema_ready']}")
        print(f"Vision Dependency Panel Schema: {status['vision_dependency_panel_schema_ready']}")
        print(f"Vision Permission Panel Schema: {status['vision_permission_panel_schema_ready']}")
        print(f"Vision Redaction Panel Schema: {status['vision_redaction_panel_schema_ready']}")
        print(f"Vision Handoff Panel Schema: {status['vision_handoff_panel_schema_ready']}")
        print(f"Vision Limitation Panel Schema: {status['vision_limitation_panel_schema_ready']}")
        print(f"Vision Risk Panel Schema: {status['vision_risk_panel_schema_ready']}")
        print(f"Vision Status Badge Schema: {status['vision_status_badge_schema_ready']}")
        print(f"Vision Safety Blocker List Schema: {status['vision_safety_blocker_list_schema_ready']}")
        print(f"Vision Dependency Baseline Schema: {status['vision_dependency_baseline_schema_ready']}")
        print(f"Vision Capability Boundary Schema: {status['vision_capability_boundary_schema_ready']}")
        print(f"Vision Release Gate Display Schema: {status['vision_release_gate_display_schema_ready']}")
        print(f"Vision Next Boundary Display Schema: {status['vision_next_boundary_display_schema_ready']}")
        print(f"Vision Panel Route Contract: {status['vision_panel_route_contract_ready']}")
        print(f"Vision Panel Navigation Item Contract: {status['vision_panel_navigation_item_contract_ready']}")
        print(f"Vision Panel View Model Contract: {status['vision_panel_view_model_contract_ready']}")
        print(f"Vision Panel Data Aggregator Contract: {status['vision_panel_data_aggregator_contract_ready']}")
        print(f"Vision Panel No Mutation Contract: {status['vision_panel_no_mutation_contract_ready']}")
        print(f"Vision Panel No Capture Contract: {status['vision_panel_no_capture_contract_ready']}")
        print(f"Read Only Status Visibility: {status['read_only_status_visibility']}")
        print(f"Read Only Safety Visibility: {status['read_only_safety_visibility']}")
        print(f"Read Only Dependency Visibility: {status['read_only_dependency_visibility']}")
        print(f"Read Only Handoff Visibility: {status['read_only_handoff_visibility']}")
        print(f"Permission Required Before Future Panel Actions: {status['permission_required_before_future_panel_actions']}")
        print(f"No Permission Grant From Panel: {status['no_permission_grant_from_panel']}")
        print(f"No Permission Mutation From Panel: {status['no_permission_mutation_from_panel']}")
        print(f"No Audit Write From Panel: {status['no_audit_write_from_panel']}")
        print(f"No Command Execution From Panel: {status['no_command_execution_from_panel']}")
        print(f"No Visual Action From Panel: {status['no_visual_action_from_panel']}")
        print(f"No Screenshot Trigger From Panel: {status['no_screenshot_trigger_from_panel']}")
        print(f"No Camera Trigger From Panel: {status['no_camera_trigger_from_panel']}")
        print(f"No Model Request Trigger From Panel: {status['no_model_request_trigger_from_panel']}")
        print(f"No Chat Handoff Trigger From Panel: {status['no_chat_handoff_trigger_from_panel']}")
        print(f"No Memory Write From Panel: {status['no_memory_write_from_panel']}")
        print(f"No External Upload From Panel: {status['no_external_upload_from_panel']}")
        print(f"No Raw Screenshot Display: {status['no_raw_screenshot_display']}")
        print(f"No Unredacted Visual Context Display: {status['no_unredacted_visual_context_display']}")
        print(f"No Hidden Visual Context Display: {status['no_hidden_visual_context_display']}")
        print(f"No Live Visual Feed: {status['no_live_visual_feed']}")
        print(f"No Auto Refresh Runtime: {status['no_auto_refresh_runtime']}")
        print(f"No Websocket Runtime: {status['no_websocket_runtime']}")
        print(f"No Public Panel Route: {status['no_public_panel_route']}")
        print(f"Control Center Vision Panel Runtime: {status['control_center_vision_panel_runtime_active']}")
        print(f"Control Center Vision Panel Rendered: {status['control_center_vision_panel_rendered']}")
        print(f"Control Center Vision Panel Route Created: {status['control_center_vision_panel_route_created']}")
        print(f"Control Center Vision Panel API Endpoint Created: {status['control_center_vision_panel_api_endpoint_created']}")
        print(f"Control Center Vision Panel Static Asset Generated: {status['control_center_vision_panel_static_asset_generated']}")
        print(f"Control Center Vision Panel Web UI Mutation: {status['control_center_vision_panel_web_ui_mutation_active']}")
        print(f"Control Center Vision Panel Data Fetch: {status['control_center_vision_panel_data_fetch_active']}")
        print(f"Control Center Vision Panel Auto Refresh: {status['control_center_vision_panel_auto_refresh_active']}")
        print(f"Control Center Vision Panel Websocket: {status['control_center_vision_panel_websocket_active']}")
        print(f"Panel Permission Request Active: {status['panel_permission_request_active']}")
        print(f"Panel Permission Mutation Active: {status['panel_permission_mutation_active']}")
        print(f"Panel Audit Write Active: {status['panel_audit_write_active']}")
        print(f"Panel Screenshot Control Active: {status['panel_screenshot_control_active']}")
        print(f"Panel Camera Control Active: {status['panel_camera_control_active']}")
        print(f"Panel Model Request Control Active: {status['panel_model_request_control_active']}")
        print(f"Panel Chat Handoff Control Active: {status['panel_chat_handoff_control_active']}")
        print(f"Panel Memory Write Control Active: {status['panel_memory_write_control_active']}")
        print(f"Panel External Upload Control Active: {status['panel_external_upload_control_active']}")
        print(f"Integration Review Packet Schema: {status['integration_review_packet_schema_ready']}")
        print(f"Integration Review Summary Schema: {status['integration_review_summary_schema_ready']}")
        print(f"Integration Acceptance Packet Schema: {status['integration_acceptance_packet_schema_ready']}")
        print(f"Integration Gap List Schema: {status['integration_gap_list_schema_ready']}")
        print(f"Integration Blocker List Schema: {status['integration_blocker_list_schema_ready']}")
        print(f"Integration Runtime Scope Schema: {status['integration_runtime_scope_schema_ready']}")
        print(f"Integration Release Gate Schema: {status['integration_release_gate_schema_ready']}")
        print(f"Integration Dependency Baseline Schema: {status['integration_dependency_baseline_schema_ready']}")
        print(f"Integration Safety Matrix Schema: {status['integration_safety_matrix_schema_ready']}")
        print(f"Integration Next Stabilization Schema: {status['integration_next_stabilization_schema_ready']}")
        print(f"Sprint 201 Activation Boundary Review: {status['sprint_201_activation_boundary_review_ready']}")
        print(f"Sprint 202 Screenshot Boundary Review: {status['sprint_202_screenshot_boundary_review_ready']}")
        print(f"Sprint 203 Screen Context Boundary Review: {status['sprint_203_screen_context_boundary_review_ready']}")
        print(f"Sprint 204 Local Model Boundary Review: {status['sprint_204_local_model_boundary_review_ready']}")
        print(f"Sprint 205 Permission Redaction Boundary Review: {status['sprint_205_permission_redaction_boundary_review_ready']}")
        print(f"Sprint 206 Workspace Visual Boundary Review: {status['sprint_206_workspace_visual_boundary_review_ready']}")
        print(f"Sprint 207 Vision Chat Boundary Review: {status['sprint_207_vision_to_chat_boundary_review_ready']}")
        print(f"Sprint 208 Control Center Panel Boundary Review: {status['sprint_208_control_center_panel_boundary_review_ready']}")
        print(f"Integration Dependency Baseline Review: {status['integration_dependency_baseline_review_ready']}")
        print(f"Integration Release Gate Review: {status['integration_release_gate_review_ready']}")
        print(f"Integration Safety Blocker Review: {status['integration_safety_blocker_review_ready']}")
        print(f"Integration Runtime Scope Review: {status['integration_runtime_scope_review_ready']}")
        print(f"Integration No Action Bypass Review: {status['integration_no_action_bypass_review_ready']}")
        print(f"Integration No External Data Review: {status['integration_no_external_data_review_ready']}")
        print(f"No Runtime Activation From Review: {status['no_runtime_activation_from_review']}")
        print(f"No Release Gate Open From Review: {status['no_release_gate_open_from_review']}")
        print(f"No Dependency Install From Review: {status['no_dependency_install_from_review']}")
        print(f"No Model Download From Review: {status['no_model_download_from_review']}")
        print(f"No Screenshot Capture From Review: {status['no_screenshot_capture_from_review']}")
        print(f"No Image File Read From Review: {status['no_image_file_read_from_review']}")
        print(f"No OCR From Review: {status['no_ocr_from_review']}")
        print(f"No Model Request From Review: {status['no_model_request_from_review']}")
        print(f"No Chat Handoff From Review: {status['no_chat_handoff_from_review']}")
        print(f"No Panel Render From Review: {status['no_panel_render_from_review']}")
        print(f"No Route Creation From Review: {status['no_route_creation_from_review']}")
        print(f"No API Endpoint Creation From Review: {status['no_api_endpoint_creation_from_review']}")
        print(f"No Data Fetch From Review: {status['no_data_fetch_from_review']}")
        print(f"No Permission Mutation From Review: {status['no_permission_mutation_from_review']}")
        print(f"No Audit Write From Review: {status['no_audit_write_from_review']}")
        print(f"No Memory Write From Review: {status['no_memory_write_from_review']}")
        print(f"No Command Execution From Review: {status['no_command_execution_from_review']}")
        print(f"No Visual Action From Review: {status['no_visual_action_from_review']}")
        print(f"No Cloud Fallback From Review: {status['no_cloud_fallback_from_review']}")
        print(f"No External Upload From Review: {status['no_external_upload_from_review']}")
        print(f"Vision Runtime Integration Review Runtime: {status['vision_runtime_integration_review_runtime_active']}")
        print(f"Integration Review Packet Created: {status['integration_review_packet_created']}")
        print(f"Integration Review Summary Created: {status['integration_review_summary_created']}")
        print(f"Integration Acceptance Packet Created: {status['integration_acceptance_packet_created']}")
        print(f"Integration Release Gate Opened: {status['integration_release_gate_opened']}")
        print(f"Runtime Activation Path Open: {status['runtime_activation_path_open']}")
        print(f"Stabilization Acceptance Packet Schema: {status['stabilization_acceptance_packet_schema_ready']}")
        print(f"Stabilization Summary Schema: {status['stabilization_summary_schema_ready']}")
        print(f"Stabilization Gap Report Schema: {status['stabilization_gap_report_schema_ready']}")
        print(f"Stabilization Blocker Report Schema: {status['stabilization_blocker_report_schema_ready']}")
        print(f"Stabilization Dependency Baseline Schema: {status['stabilization_dependency_baseline_schema_ready']}")
        print(f"Stabilization Release Gate Schema: {status['stabilization_release_gate_schema_ready']}")
        print(f"Stabilization Runtime Scope Schema: {status['stabilization_runtime_scope_schema_ready']}")
        print(f"Stabilization Safety Matrix Schema: {status['stabilization_safety_matrix_schema_ready']}")
        print(f"Stabilization Handoff Packet Schema: {status['stabilization_handoff_packet_schema_ready']}")
        print(f"Stabilization Next Block Schema: {status['stabilization_next_block_schema_ready']}")
        print(f"Sprint 201 Activation Stabilized: {status['sprint_201_activation_stabilized']}")
        print(f"Sprint 202 Screenshot Stabilized: {status['sprint_202_screenshot_stabilized']}")
        print(f"Sprint 203 Screen Context Stabilized: {status['sprint_203_screen_context_stabilized']}")
        print(f"Sprint 204 Local Model Stabilized: {status['sprint_204_local_model_stabilized']}")
        print(f"Sprint 205 Permission Redaction Stabilized: {status['sprint_205_permission_redaction_stabilized']}")
        print(f"Sprint 206 Workspace Visual Stabilized: {status['sprint_206_workspace_visual_stabilized']}")
        print(f"Sprint 207 Vision Chat Stabilized: {status['sprint_207_vision_to_chat_stabilized']}")
        print(f"Sprint 208 Control Center Panel Stabilized: {status['sprint_208_control_center_panel_stabilized']}")
        print(f"Sprint 209 Integration Review Stabilized: {status['sprint_209_integration_review_stabilized']}")
        print(f"Vision Dependency Baseline Stable: {status['vision_dependency_baseline_stable']}")
        print(f"Vision Release Gate Stable Closed: {status['vision_release_gate_stable_closed']}")
        print(f"Vision Safety Blockers Stable Inactive: {status['vision_safety_blockers_stable_inactive']}")
        print(f"Vision Runtime Scope Stable Contract Only: {status['vision_runtime_scope_stable_contract_only']}")
        print(f"Vision Block Handoff To Permission Runtime Ready: {status['vision_block_handoff_to_permission_runtime_ready']}")
        print(f"No Runtime Activation From Stabilization: {status['no_runtime_activation_from_stabilization']}")
        print(f"No Release Gate Open From Stabilization: {status['no_release_gate_open_from_stabilization']}")
        print(f"No Dependency Install From Stabilization: {status['no_dependency_install_from_stabilization']}")
        print(f"No Model Download From Stabilization: {status['no_model_download_from_stabilization']}")
        print(f"No Screenshot Capture From Stabilization: {status['no_screenshot_capture_from_stabilization']}")
        print(f"No Image File Read From Stabilization: {status['no_image_file_read_from_stabilization']}")
        print(f"No OCR From Stabilization: {status['no_ocr_from_stabilization']}")
        print(f"No Model Request From Stabilization: {status['no_model_request_from_stabilization']}")
        print(f"No Chat Handoff From Stabilization: {status['no_chat_handoff_from_stabilization']}")
        print(f"No Panel Render From Stabilization: {status['no_panel_render_from_stabilization']}")
        print(f"No Route Creation From Stabilization: {status['no_route_creation_from_stabilization']}")
        print(f"No API Endpoint Creation From Stabilization: {status['no_api_endpoint_creation_from_stabilization']}")
        print(f"No Data Fetch From Stabilization: {status['no_data_fetch_from_stabilization']}")
        print(f"No Permission Mutation From Stabilization: {status['no_permission_mutation_from_stabilization']}")
        print(f"No Audit Write From Stabilization: {status['no_audit_write_from_stabilization']}")
        print(f"No Memory Write From Stabilization: {status['no_memory_write_from_stabilization']}")
        print(f"No Command Execution From Stabilization: {status['no_command_execution_from_stabilization']}")
        print(f"No Visual Action From Stabilization: {status['no_visual_action_from_stabilization']}")
        print(f"No Cloud Fallback From Stabilization: {status['no_cloud_fallback_from_stabilization']}")
        print(f"No External Upload From Stabilization: {status['no_external_upload_from_stabilization']}")
        print(f"Vision Runtime Stabilization Runtime: {status['vision_runtime_stabilization_runtime_active']}")
        print(f"Stabilization Acceptance Packet Created: {status['stabilization_acceptance_packet_created']}")
        print(f"Stabilization Summary Created: {status['stabilization_summary_created']}")
        print(f"Stabilization Release Gate Opened: {status['stabilization_release_gate_opened']}")
        print(f"Stabilization Handoff Packet Created: {status['stabilization_handoff_packet_created']}")
        print(f"No Raw Screenshot To Chat : {status['no_raw_screenshot_to_chat']}")
        print(f"No Unredacted Context To Chat: {status['no_unredacted_context_to_chat']}")
        print(f"Vision Model Runtime      : {status['vision_model_runtime_active']}")
        print(f"OCR Runtime Active        : {status['ocr_runtime_active']}")
        print(f"Cloud Vision Fallback     : {status['cloud_vision_fallback_enabled']}")
        print(f"External Upload           : {status['external_upload_enabled']}")
        print(f"Vision Safety Blockers    : {status['vision_safety_blocker_count']}")
        print(f"All Safety Blockers Off   : {status['vision_all_safety_blockers_inactive']}")
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
        planner = VisionRuntimePlanner(project_root=Path.cwd())
        result = planner.check()
        dependencies = result["dependencies"]
        activation = result["vision_runtime_activation_contract"]
        screenshot = result["explicit_screenshot_capture_contract"]
        screen_context = result["screen_context_adapter_contract"]
        local_model = result["local_vision_model_adapter_contract"]
        permission_redaction = result["vision_permission_redaction_contract"]
        workspace_visual = result["workspace_visual_understanding_contract"]
        vision_to_chat = result["vision_to_chat_context_handoff_contract"]
        control_center_vision_panel = result["control_center_vision_panel_contract"]
        integration_review = result["vision_runtime_integration_review_contract"]
        stabilization = result["vision_runtime_stabilization_contract"]

        print("AURA Vision Runtime Check")
        print("=========================")
        print(f"Status                 : {result['status']}")
        print(f"Planning Ready         : {result['planning_ready']}")
        print(f"Runtime Ready          : {result['runtime_ready']}")
        print(f"Assertion Count        : {result['assertion_count']}")
        print(f"Failed Assertion Count : {result['failed_assertion_count']}")
        print(f"Python Packages        : {result['python_packages_installed']}/{result['python_packages_total']}")
        print(f"Executables            : {result['executables_found']}/{result['executables_total']}")
        print()
        print("Sprint 201 Vision Runtime Activation Foundation")
        print("-----------------------------------------------")
        print(f"Activation Contract    : {activation['vision_runtime_activation_contract_ready']}")
        print(f"Activation Runtime     : {activation['vision_runtime_activation_runtime_ready']}")
        print(f"Activation Status      : {activation['vision_runtime_activation_status']}")
        print()
        print("Sprint 202 Explicit Screenshot Capture")
        print("--------------------------------------")
        print(f"Screenshot Contract    : {screenshot['explicit_screenshot_capture_contract_ready']}")
        print(f"Screenshot Runtime     : {screenshot['explicit_screenshot_capture_runtime_ready']}")
        print(f"Screenshot Capture Performed: {screenshot['screenshot_capture_performed']}")
        print()
        print("Sprint 203 Screen Context Adapter")
        print("---------------------------------")
        print(f"Screen Context Contract : {screen_context['screen_context_adapter_contract_ready']}")
        print(f"Screen Context Runtime  : {screen_context['screen_context_adapter_runtime_ready']}")
        print(f"Screen Context Packet Created: {screen_context['screen_context_packet_created']}")
        print()
        print("Sprint 204 Local Vision Model Adapter")
        print("-------------------------------------")
        print(f"Local Model Contract    : {local_model['local_vision_model_adapter_contract_ready']}")
        print(f"Local Model Runtime     : {local_model['local_vision_model_adapter_runtime_ready']}")
        print(f"Local Model Request Active : {local_model['local_model_request_active']}")
        print(f"Local Model Inference Active: {local_model['local_model_inference_active']}")
        print()
        print("Sprint 205 Vision Permission and Redaction")
        print("------------------------------------------")
        print(f"Permission Redaction Contract: {permission_redaction['vision_permission_redaction_contract_ready']}")
        print(f"Permission Redaction Runtime : {permission_redaction['vision_permission_redaction_runtime_ready']}")
        print(f"Permission Redaction Status  : {permission_redaction['vision_permission_redaction_status']}")
        print()
        print("Sprint 206 Workspace Visual Understanding")
        print("-----------------------------------------")
        print(f"Workspace Visual Contract      : {workspace_visual['workspace_visual_understanding_contract_ready']}")
        print(f"Workspace Visual Runtime       : {workspace_visual['workspace_visual_understanding_runtime_ready']}")
        print(f"Workspace Visual Status        : {workspace_visual['workspace_visual_understanding_status']}")
        print()
        print("Sprint 207 Vision-to-Chat Context Handoff")
        print("-----------------------------------------")
        print(f"Vision Chat Handoff Contract   : {vision_to_chat['vision_to_chat_context_handoff_contract_ready']}")
        print(f"Vision Chat Handoff Runtime    : {vision_to_chat['vision_to_chat_context_handoff_runtime_ready']}")
        print(f"Vision Chat Handoff Status     : {vision_to_chat['vision_to_chat_context_handoff_status']}")
        print(f"Vision Block Start             : {vision_to_chat['vision_runtime_block_start']}")
        print(f"Vision Block End               : {vision_to_chat['vision_runtime_block_end']}")
        print(f"Current Sprint                 : {vision_to_chat['vision_runtime_current_sprint']}")
        print(f"Next Sprint                    : {vision_to_chat['vision_runtime_next_sprint']}")
        print(f"Next Boundary                  : {vision_to_chat['vision_runtime_next_boundary']}")
        print(f"Runtime Ready                  : {vision_to_chat['runtime_ready']}")
        print(f"Runtime Activation             : {vision_to_chat['runtime_activation_allowed']}")
        print(f"Release Gate Open              : {vision_to_chat['release_gate_open']}")
        print(f"Contract Only                  : {vision_to_chat['vision_to_chat_context_handoff_contract_only']}")
        print(f"Provided Redacted Visual Context: {vision_to_chat['provided_redacted_visual_context_required']}")
        print(f"Provided Workspace Visual Summary: {vision_to_chat['provided_workspace_visual_summary_required']}")
        print(f"Provided Workspace Metadata    : {vision_to_chat['provided_workspace_metadata_required']}")
        print(f"Provided User Question         : {vision_to_chat['provided_user_question_required']}")
        print(f"Provided Permission Packet     : {vision_to_chat['provided_permission_packet_required']}")
        print(f"Redaction Proof Required       : {vision_to_chat['redaction_proof_required']}")
        print(f"Source Metadata Required       : {vision_to_chat['source_metadata_required']}")
        print(f"Uncertainty Required           : {vision_to_chat['uncertainty_required']}")
        print(f"Chat Safe Visual Packet Schema : {vision_to_chat['chat_safe_visual_context_packet_schema_ready']}")
        print(f"Chat Safe Visual Summary Schema: {vision_to_chat['chat_safe_visual_summary_schema_ready']}")
        print(f"Chat Safe Workspace Summary Schema: {vision_to_chat['chat_safe_workspace_summary_schema_ready']}")
        print(f"Chat Context Handoff Packet Schema: {vision_to_chat['chat_context_handoff_packet_schema_ready']}")
        print(f"Chat Source Attribution Schema : {vision_to_chat['chat_source_attribution_schema_ready']}")
        print(f"Chat Limitation Schema         : {vision_to_chat['chat_limitation_schema_ready']}")
        print(f"Chat Uncertainty Schema        : {vision_to_chat['chat_uncertainty_schema_ready']}")
        print(f"Chat Risk Notice Schema        : {vision_to_chat['chat_risk_notice_schema_ready']}")
        print(f"Chat Handoff Preview Schema    : {vision_to_chat['chat_handoff_preview_schema_ready']}")
        print(f"Chat Visible Disclosure Contract: {vision_to_chat['chat_visible_disclosure_contract_ready']}")
        print(f"Chat Render Boundary Contract  : {vision_to_chat['chat_render_boundary_contract_ready']}")
        print(f"Permission Before Chat Handoff : {vision_to_chat['permission_required_before_chat_handoff']}")
        print(f"Permission Before Chat Context Injection: {vision_to_chat['permission_required_before_chat_context_injection']}")
        print(f"Permission Before Chat Session Write: {vision_to_chat['permission_required_before_chat_session_write']}")
        print(f"Redaction Before Chat Handoff  : {vision_to_chat['redaction_required_before_chat_handoff']}")
        print(f"Redaction Before Chat Context Packet: {vision_to_chat['redaction_required_before_chat_context_packet']}")
        print(f"Redaction Before Chat Session Write: {vision_to_chat['redaction_required_before_chat_session_write']}")
        print(f"Explicit User Request For Handoff: {vision_to_chat['explicit_user_request_required_for_handoff']}")
        print(f"Explicit Confirmation For Handoff: {vision_to_chat['explicit_confirmation_required_for_handoff']}")
        print(f"Foreground Chat Session Required: {vision_to_chat['foreground_chat_session_required']}")
        print(f"No Raw Screenshot To Chat       : {vision_to_chat['no_raw_screenshot_to_chat']}")
        print(f"No Unredacted Context To Chat   : {vision_to_chat['no_unredacted_context_to_chat']}")
        print(f"No Hidden Visual Context Injection: {vision_to_chat['no_hidden_visual_context_injection']}")
        print(f"No Automatic Chat Handoff       : {vision_to_chat['no_automatic_chat_handoff']}")
        print(f"No Chat Model Request Without User Message: {vision_to_chat['no_chat_model_request_without_user_message']}")
        print(f"No Memory Write From Visual Handoff: {vision_to_chat['no_memory_write_from_visual_handoff']}")
        print(f"No Action Recommendation Without Permission: {vision_to_chat['no_action_recommendation_without_permission']}")
        print(f"No OCR Claims Without OCR       : {vision_to_chat['no_ocr_claims_without_ocr']}")
        print(f"No Model Claims Without Model   : {vision_to_chat['no_model_claims_without_model']}")
        print(f"No Identity Claims              : {vision_to_chat['no_identity_claims']}")
        print(f"No Biometric Identification     : {vision_to_chat['no_biometric_identification']}")
        print(f"No Face Recognition             : {vision_to_chat['no_face_recognition']}")
        print(f"No Emotion Inference From Face  : {vision_to_chat['no_emotion_inference_from_face']}")
        print(f"Image File Read Allowed         : {vision_to_chat['image_file_read_allowed']}")
        print(f"Screenshot Required Now         : {vision_to_chat['screenshot_capture_required_now']}")
        print(f"Screenshot File Read Now        : {vision_to_chat['screenshot_file_read_required_now']}")
        print(f"OCR Required Now                : {vision_to_chat['ocr_required_now']}")
        print(f"Cloud Vision Fallback Allowed   : {vision_to_chat['cloud_vision_fallback_allowed']}")
        print(f"External Upload Allowed         : {vision_to_chat['external_upload_allowed']}")
        print(f"Model Download Required Now     : {vision_to_chat['model_download_required_now']}")
        print(f"Dependency Install              : {vision_to_chat['dependency_install_performed']}")
        print(f"Safety Blocker Count            : {vision_to_chat['safety_blocker_count']}")
        print(f"All Safety Blockers Off         : {vision_to_chat['all_safety_blockers_inactive']}")
        print(f"Runtime Scope                   : {vision_to_chat['runtime_scope']}")
        print()
        print("Sprint 208 Control Center Vision Panel")
        print("--------------------------------------")
        print(f"Control Center Vision Panel Contract : {control_center_vision_panel['control_center_vision_panel_contract_ready']}")
        print(f"Control Center Vision Panel Runtime  : {control_center_vision_panel['control_center_vision_panel_runtime_ready']}")
        print(f"Control Center Vision Panel Status   : {control_center_vision_panel['control_center_vision_panel_status']}")
        print(f"Vision Block Start                   : {control_center_vision_panel['vision_runtime_block_start']}")
        print(f"Vision Block End                     : {control_center_vision_panel['vision_runtime_block_end']}")
        print(f"Current Sprint                       : {control_center_vision_panel['vision_runtime_current_sprint']}")
        print(f"Next Sprint                          : {control_center_vision_panel['vision_runtime_next_sprint']}")
        print(f"Next Boundary                        : {control_center_vision_panel['vision_runtime_next_boundary']}")
        print(f"Runtime Ready                        : {control_center_vision_panel['runtime_ready']}")
        print(f"Runtime Activation                   : {control_center_vision_panel['runtime_activation_allowed']}")
        print(f"Release Gate Open                    : {control_center_vision_panel['release_gate_open']}")
        print(f"Contract Only                        : {control_center_vision_panel['control_center_vision_panel_contract_only']}")
        print(f"Read Only Panel Contract             : {control_center_vision_panel['read_only_panel_contract_ready']}")
        print(f"Display Only Panel Contract          : {control_center_vision_panel['display_only_panel_contract_ready']}")
        print(f"Control Center Visible Panel Schema  : {control_center_vision_panel['control_center_visible_panel_schema_ready']}")
        print(f"Vision Status Panel Schema           : {control_center_vision_panel['vision_status_panel_schema_ready']}")
        print(f"Vision Safety Panel Schema           : {control_center_vision_panel['vision_safety_panel_schema_ready']}")
        print(f"Vision Dependency Panel Schema       : {control_center_vision_panel['vision_dependency_panel_schema_ready']}")
        print(f"Vision Permission Panel Schema       : {control_center_vision_panel['vision_permission_panel_schema_ready']}")
        print(f"Vision Redaction Panel Schema        : {control_center_vision_panel['vision_redaction_panel_schema_ready']}")
        print(f"Vision Handoff Panel Schema          : {control_center_vision_panel['vision_handoff_panel_schema_ready']}")
        print(f"Vision Limitation Panel Schema       : {control_center_vision_panel['vision_limitation_panel_schema_ready']}")
        print(f"Vision Risk Panel Schema             : {control_center_vision_panel['vision_risk_panel_schema_ready']}")
        print(f"Vision Status Badge Schema           : {control_center_vision_panel['vision_status_badge_schema_ready']}")
        print(f"Vision Safety Blocker List Schema    : {control_center_vision_panel['vision_safety_blocker_list_schema_ready']}")
        print(f"Vision Dependency Baseline Schema    : {control_center_vision_panel['vision_dependency_baseline_schema_ready']}")
        print(f"Vision Capability Boundary Schema    : {control_center_vision_panel['vision_capability_boundary_schema_ready']}")
        print(f"Vision Release Gate Display Schema   : {control_center_vision_panel['vision_release_gate_display_schema_ready']}")
        print(f"Vision Next Boundary Display Schema  : {control_center_vision_panel['vision_next_boundary_display_schema_ready']}")
        print(f"Vision Panel Route Contract          : {control_center_vision_panel['vision_panel_route_contract_ready']}")
        print(f"Vision Panel Navigation Item Contract: {control_center_vision_panel['vision_panel_navigation_item_contract_ready']}")
        print(f"Vision Panel View Model Contract     : {control_center_vision_panel['vision_panel_view_model_contract_ready']}")
        print(f"Vision Panel Data Aggregator Contract: {control_center_vision_panel['vision_panel_data_aggregator_contract_ready']}")
        print(f"Vision Panel No Mutation Contract    : {control_center_vision_panel['vision_panel_no_mutation_contract_ready']}")
        print(f"Vision Panel No Capture Contract     : {control_center_vision_panel['vision_panel_no_capture_contract_ready']}")
        print(f"Read Only Status Visibility          : {control_center_vision_panel['read_only_status_visibility']}")
        print(f"Read Only Safety Visibility          : {control_center_vision_panel['read_only_safety_visibility']}")
        print(f"Read Only Dependency Visibility      : {control_center_vision_panel['read_only_dependency_visibility']}")
        print(f"Read Only Handoff Visibility         : {control_center_vision_panel['read_only_handoff_visibility']}")
        print(f"Permission Required Before Future Panel Actions: {control_center_vision_panel['permission_required_before_future_panel_actions']}")
        print(f"No Permission Grant From Panel       : {control_center_vision_panel['no_permission_grant_from_panel']}")
        print(f"No Permission Mutation From Panel    : {control_center_vision_panel['no_permission_mutation_from_panel']}")
        print(f"No Audit Write From Panel            : {control_center_vision_panel['no_audit_write_from_panel']}")
        print(f"No Command Execution From Panel      : {control_center_vision_panel['no_command_execution_from_panel']}")
        print(f"No Visual Action From Panel          : {control_center_vision_panel['no_visual_action_from_panel']}")
        print(f"No Screenshot Trigger From Panel     : {control_center_vision_panel['no_screenshot_trigger_from_panel']}")
        print(f"No Camera Trigger From Panel         : {control_center_vision_panel['no_camera_trigger_from_panel']}")
        print(f"No Model Request Trigger From Panel  : {control_center_vision_panel['no_model_request_trigger_from_panel']}")
        print(f"No Chat Handoff Trigger From Panel   : {control_center_vision_panel['no_chat_handoff_trigger_from_panel']}")
        print(f"No Memory Write From Panel           : {control_center_vision_panel['no_memory_write_from_panel']}")
        print(f"No External Upload From Panel        : {control_center_vision_panel['no_external_upload_from_panel']}")
        print(f"No Raw Screenshot Display            : {control_center_vision_panel['no_raw_screenshot_display']}")
        print(f"No Unredacted Visual Context Display : {control_center_vision_panel['no_unredacted_visual_context_display']}")
        print(f"No Hidden Visual Context Display     : {control_center_vision_panel['no_hidden_visual_context_display']}")
        print(f"No Live Visual Feed                  : {control_center_vision_panel['no_live_visual_feed']}")
        print(f"No Auto Refresh Runtime              : {control_center_vision_panel['no_auto_refresh_runtime']}")
        print(f"No Websocket Runtime                 : {control_center_vision_panel['no_websocket_runtime']}")
        print(f"No Public Panel Route                : {control_center_vision_panel['no_public_panel_route']}")
        print(f"Safety Blocker Count                 : {control_center_vision_panel['safety_blocker_count']}")
        print(f"All Safety Blockers Off              : {control_center_vision_panel['all_safety_blockers_inactive']}")
        print(f"Runtime Scope                        : {control_center_vision_panel['runtime_scope']}")
        print()
        print("Control Center Vision Panel Runtime Safety State")
        print("------------------------------------------------")
        print(f"Control Center Vision Panel Runtime  : {control_center_vision_panel['control_center_vision_panel_runtime_active']}")
        print(f"Control Center Vision Panel Rendered : {control_center_vision_panel['control_center_vision_panel_rendered']}")
        print(f"Control Center Vision Panel Route Created: {control_center_vision_panel['control_center_vision_panel_route_created']}")
        print(f"Control Center Vision Panel API Endpoint Created: {control_center_vision_panel['control_center_vision_panel_api_endpoint_created']}")
        print(f"Control Center Vision Panel Static Asset Generated: {control_center_vision_panel['control_center_vision_panel_static_asset_generated']}")
        print(f"Control Center Vision Panel Web UI Mutation: {control_center_vision_panel['control_center_vision_panel_web_ui_mutation_active']}")
        print(f"Control Center Vision Panel Data Fetch: {control_center_vision_panel['control_center_vision_panel_data_fetch_active']}")
        print(f"Control Center Vision Panel Auto Refresh: {control_center_vision_panel['control_center_vision_panel_auto_refresh_active']}")
        print(f"Control Center Vision Panel Websocket: {control_center_vision_panel['control_center_vision_panel_websocket_active']}")
        print(f"Panel Permission Request Active      : {control_center_vision_panel['panel_permission_request_active']}")
        print(f"Panel Permission Mutation Active     : {control_center_vision_panel['panel_permission_mutation_active']}")
        print(f"Panel Audit Write Active             : {control_center_vision_panel['panel_audit_write_active']}")
        print(f"Panel Screenshot Control Active      : {control_center_vision_panel['panel_screenshot_control_active']}")
        print(f"Panel Camera Control Active          : {control_center_vision_panel['panel_camera_control_active']}")
        print(f"Panel Model Request Control Active   : {control_center_vision_panel['panel_model_request_control_active']}")
        print(f"Panel Chat Handoff Control Active    : {control_center_vision_panel['panel_chat_handoff_control_active']}")
        print(f"Panel Memory Write Control Active    : {control_center_vision_panel['panel_memory_write_control_active']}")
        print(f"Panel External Upload Control Active : {control_center_vision_panel['panel_external_upload_control_active']}")
        print(f"Chat Context Packet Created          : {control_center_vision_panel['chat_context_packet_created']}")
        print(f"Chat Session Write Active            : {control_center_vision_panel['chat_session_write_active']}")
        print(f"Chat Model Request Active            : {control_center_vision_panel['chat_model_request_active']}")
        print(f"Chat Response Generation Active      : {control_center_vision_panel['chat_response_generation_active']}")
        print(f"Screenshot Capture Performed         : {control_center_vision_panel['screenshot_capture_performed']}")
        print(f"Screenshot File Read                 : {control_center_vision_panel['screenshot_file_read_active']}")
        print(f"Local Model Request Active           : {control_center_vision_panel['local_model_request_active']}")
        print(f"Local Model Inference Active         : {control_center_vision_panel['local_model_inference_active']}")
        print(f"Model To Chat Handoff                : {control_center_vision_panel['model_to_chat_handoff_active']}")
        print(f"Vision Model Runtime                 : {control_center_vision_panel['vision_model_runtime_active']}")
        print(f"OCR Runtime Active                   : {control_center_vision_panel['ocr_runtime_active']}")
        print(f"Image Analysis Runtime               : {control_center_vision_panel['image_analysis_runtime_active']}")
        print(f"Object Detection Runtime             : {control_center_vision_panel['object_detection_runtime_active']}")
        print(f"Visual Action Execution              : {control_center_vision_panel['visual_action_execution_active']}")
        print(f"Visual Tool Execution                : {control_center_vision_panel['visual_tool_execution_active']}")
        print(f"Command Execution                    : {control_center_vision_panel['command_execution_active']}")
        print(f"Memory Write                         : {control_center_vision_panel['memory_write_active']}")
        print(f"Cloud Vision Fallback                : {control_center_vision_panel['cloud_vision_fallback_enabled']}")
        print(f"External Upload                      : {control_center_vision_panel['external_upload_enabled']}")
        print(f"Visual Context Action Bypass         : {control_center_vision_panel['visual_context_to_action_bypass_enabled']}")
        print(f"No Tool Use From Visual Context      : {control_center_vision_panel['no_tool_use_from_visual_context']}")
        print(f"No Autonomous Action                 : {control_center_vision_panel['no_autonomous_action']}")
        print()
        print("Sprint 209 Vision Runtime Integration Review")
        print("--------------------------------------------")
        print(f"Vision Runtime Integration Review Contract : {integration_review['vision_runtime_integration_review_contract_ready']}")
        print(f"Vision Runtime Integration Review Runtime  : {integration_review['vision_runtime_integration_review_runtime_ready']}")
        print(f"Vision Runtime Integration Review Status   : {integration_review['vision_runtime_integration_review_status']}")
        print(f"Vision Block Start                         : {integration_review['vision_runtime_block_start']}")
        print(f"Vision Block End                           : {integration_review['vision_runtime_block_end']}")
        print(f"Current Sprint                             : {integration_review['vision_runtime_current_sprint']}")
        print(f"Next Sprint                                : {integration_review['vision_runtime_next_sprint']}")
        print(f"Next Boundary                              : {integration_review['vision_runtime_next_boundary']}")
        print(f"Previous Contract Chain Complete           : {integration_review['previous_contract_chain_complete']}")
        print(f"Runtime Ready                              : {integration_review['runtime_ready']}")
        print(f"Runtime Activation                         : {integration_review['runtime_activation_allowed']}")
        print(f"Release Gate Open                          : {integration_review['release_gate_open']}")
        print(f"Contract Only                              : {integration_review['vision_runtime_integration_review_contract_only']}")
        print(f"Integration Review Packet Schema           : {integration_review['integration_review_packet_schema_ready']}")
        print(f"Integration Review Summary Schema          : {integration_review['integration_review_summary_schema_ready']}")
        print(f"Integration Acceptance Packet Schema       : {integration_review['integration_acceptance_packet_schema_ready']}")
        print(f"Integration Gap List Schema                : {integration_review['integration_gap_list_schema_ready']}")
        print(f"Integration Blocker List Schema            : {integration_review['integration_blocker_list_schema_ready']}")
        print(f"Integration Runtime Scope Schema           : {integration_review['integration_runtime_scope_schema_ready']}")
        print(f"Integration Release Gate Schema            : {integration_review['integration_release_gate_schema_ready']}")
        print(f"Integration Dependency Baseline Schema     : {integration_review['integration_dependency_baseline_schema_ready']}")
        print(f"Integration Safety Matrix Schema           : {integration_review['integration_safety_matrix_schema_ready']}")
        print(f"Integration Next Stabilization Schema      : {integration_review['integration_next_stabilization_schema_ready']}")
        print(f"Sprint 201 Activation Boundary Review      : {integration_review['sprint_201_activation_boundary_review_ready']}")
        print(f"Sprint 202 Screenshot Boundary Review      : {integration_review['sprint_202_screenshot_boundary_review_ready']}")
        print(f"Sprint 203 Screen Context Boundary Review  : {integration_review['sprint_203_screen_context_boundary_review_ready']}")
        print(f"Sprint 204 Local Model Boundary Review     : {integration_review['sprint_204_local_model_boundary_review_ready']}")
        print(f"Sprint 205 Permission Redaction Boundary Review: {integration_review['sprint_205_permission_redaction_boundary_review_ready']}")
        print(f"Sprint 206 Workspace Visual Boundary Review: {integration_review['sprint_206_workspace_visual_boundary_review_ready']}")
        print(f"Sprint 207 Vision Chat Boundary Review     : {integration_review['sprint_207_vision_to_chat_boundary_review_ready']}")
        print(f"Sprint 208 Control Center Panel Boundary Review: {integration_review['sprint_208_control_center_panel_boundary_review_ready']}")
        print(f"Integration Dependency Baseline Review     : {integration_review['integration_dependency_baseline_review_ready']}")
        print(f"Integration Release Gate Review            : {integration_review['integration_release_gate_review_ready']}")
        print(f"Integration Safety Blocker Review          : {integration_review['integration_safety_blocker_review_ready']}")
        print(f"Integration Runtime Scope Review           : {integration_review['integration_runtime_scope_review_ready']}")
        print(f"Integration No Action Bypass Review        : {integration_review['integration_no_action_bypass_review_ready']}")
        print(f"Integration No External Data Review        : {integration_review['integration_no_external_data_review_ready']}")
        print(f"No Runtime Activation From Review          : {integration_review['no_runtime_activation_from_review']}")
        print(f"No Release Gate Open From Review           : {integration_review['no_release_gate_open_from_review']}")
        print(f"No Dependency Install From Review          : {integration_review['no_dependency_install_from_review']}")
        print(f"No Model Download From Review              : {integration_review['no_model_download_from_review']}")
        print(f"No Screenshot Capture From Review          : {integration_review['no_screenshot_capture_from_review']}")
        print(f"No Image File Read From Review             : {integration_review['no_image_file_read_from_review']}")
        print(f"No OCR From Review                         : {integration_review['no_ocr_from_review']}")
        print(f"No Model Request From Review               : {integration_review['no_model_request_from_review']}")
        print(f"No Chat Handoff From Review                : {integration_review['no_chat_handoff_from_review']}")
        print(f"No Panel Render From Review                : {integration_review['no_panel_render_from_review']}")
        print(f"No Route Creation From Review              : {integration_review['no_route_creation_from_review']}")
        print(f"No API Endpoint Creation From Review       : {integration_review['no_api_endpoint_creation_from_review']}")
        print(f"No Data Fetch From Review                  : {integration_review['no_data_fetch_from_review']}")
        print(f"No Permission Mutation From Review         : {integration_review['no_permission_mutation_from_review']}")
        print(f"No Audit Write From Review                 : {integration_review['no_audit_write_from_review']}")
        print(f"No Memory Write From Review                : {integration_review['no_memory_write_from_review']}")
        print(f"No Command Execution From Review           : {integration_review['no_command_execution_from_review']}")
        print(f"No Visual Action From Review               : {integration_review['no_visual_action_from_review']}")
        print(f"No Cloud Fallback From Review              : {integration_review['no_cloud_fallback_from_review']}")
        print(f"No External Upload From Review             : {integration_review['no_external_upload_from_review']}")
        print(f"Safety Blocker Count                       : {integration_review['safety_blocker_count']}")
        print(f"All Safety Blockers Off                    : {integration_review['all_safety_blockers_inactive']}")
        print(f"Runtime Scope                              : {integration_review['runtime_scope']}")
        print()
        print("Vision Runtime Integration Review Safety State")
        print("----------------------------------------------")
        print(f"Vision Runtime Integration Review Runtime    : {integration_review['vision_runtime_integration_review_runtime_active']}")
        print(f"Integration Review Packet Created            : {integration_review['integration_review_packet_created']}")
        print(f"Integration Review Summary Created           : {integration_review['integration_review_summary_created']}")
        print(f"Integration Acceptance Packet Created        : {integration_review['integration_acceptance_packet_created']}")
        print(f"Integration Gap List Created                 : {integration_review['integration_gap_list_created']}")
        print(f"Integration Blocker List Created             : {integration_review['integration_blocker_list_created']}")
        print(f"Integration Release Gate Opened              : {integration_review['integration_release_gate_opened']}")
        print(f"Runtime Activation Path Open                 : {integration_review['runtime_activation_path_open']}")
        print(f"Dependency Install Active                    : {integration_review['dependency_install_active']}")
        print(f"Model Download Active                        : {integration_review['model_download_active']}")
        print(f"Screenshot Capture Performed                 : {integration_review['screenshot_capture_performed']}")
        print(f"Screenshot File Read                         : {integration_review['screenshot_file_read_active']}")
        print(f"Screen Context Packet Created                : {integration_review['screen_context_packet_created']}")
        print(f"Screen Context Handoff                       : {integration_review['screen_context_handoff_active']}")
        print(f"Local Model Request Active                   : {integration_review['local_model_request_active']}")
        print(f"Local Model Inference Active                 : {integration_review['local_model_inference_active']}")
        print(f"Model To Chat Handoff                        : {integration_review['model_to_chat_handoff_active']}")
        print(f"Permission Prompt Runtime                    : {integration_review['permission_prompt_runtime_active']}")
        print(f"Permission Grant Mutation                    : {integration_review['permission_grant_mutation_active']}")
        print(f"Redaction Runtime                            : {integration_review['redaction_runtime_active']}")
        print(f"Redacted Context Created                     : {integration_review['redacted_context_created']}")
        print(f"Redaction Audit Write                        : {integration_review['redaction_audit_write_active']}")
        print(f"Workspace Visual Runtime                     : {integration_review['workspace_visual_understanding_runtime_active']}")
        print(f"Workspace Visual Summary Created             : {integration_review['workspace_visual_summary_created']}")
        print(f"Workspace To Chat Handoff                    : {integration_review['workspace_to_chat_handoff_active']}")
        print(f"Vision To Chat Handoff Runtime               : {integration_review['vision_to_chat_context_handoff_runtime_active']}")
        print(f"Chat Context Packet Created                  : {integration_review['chat_context_packet_created']}")
        print(f"Chat Safe Visual Summary Created             : {integration_review['chat_safe_visual_summary_created']}")
        print(f"Chat Message Injection Active                : {integration_review['chat_message_injection_active']}")
        print(f"Chat Session Write Active                    : {integration_review['chat_session_write_active']}")
        print(f"Chat Model Request Active                    : {integration_review['chat_model_request_active']}")
        print(f"Chat Response Generation Active              : {integration_review['chat_response_generation_active']}")
        print(f"Control Center Vision Panel Runtime          : {integration_review['control_center_vision_panel_runtime_active']}")
        print(f"Control Center Vision Panel Rendered         : {integration_review['control_center_vision_panel_rendered']}")
        print(f"Control Center Vision Panel Route Created    : {integration_review['control_center_vision_panel_route_created']}")
        print(f"Control Center Vision Panel API Endpoint Created: {integration_review['control_center_vision_panel_api_endpoint_created']}")
        print(f"Control Center Vision Panel Data Fetch       : {integration_review['control_center_vision_panel_data_fetch_active']}")
        print(f"Panel Permission Mutation                    : {integration_review['panel_permission_mutation_active']}")
        print(f"Panel Audit Write                            : {integration_review['panel_audit_write_active']}")
        print(f"Panel Screenshot Control                     : {integration_review['panel_screenshot_control_active']}")
        print(f"Panel Camera Control                         : {integration_review['panel_camera_control_active']}")
        print(f"Panel Model Request Control                  : {integration_review['panel_model_request_control_active']}")
        print(f"Panel Chat Handoff Control                   : {integration_review['panel_chat_handoff_control_active']}")
        print(f"Vision Model Runtime                         : {integration_review['vision_model_runtime_active']}")
        print(f"OCR Runtime Active                           : {integration_review['ocr_runtime_active']}")
        print(f"Image Analysis Runtime                       : {integration_review['image_analysis_runtime_active']}")
        print(f"Object Detection Runtime                     : {integration_review['object_detection_runtime_active']}")
        print(f"Visual Action Execution                      : {integration_review['visual_action_execution_active']}")
        print(f"Visual Tool Execution                        : {integration_review['visual_tool_execution_active']}")
        print(f"Command Execution                            : {integration_review['command_execution_active']}")
        print(f"File Mutation                                : {integration_review['file_mutation_active']}")
        print(f"Desktop Action                               : {integration_review['desktop_action_active']}")
        print(f"Network Action                               : {integration_review['network_action_active']}")
        print(f"Git Action                                   : {integration_review['git_action_active']}")
        print(f"Memory Write                                 : {integration_review['memory_write_active']}")
        print(f"Cloud Vision Fallback                        : {integration_review['cloud_vision_fallback_enabled']}")
        print(f"External Upload                              : {integration_review['external_upload_enabled']}")
        print(f"Visual Context Action Bypass                 : {integration_review['visual_context_to_action_bypass_enabled']}")
        print(f"No Tool Use From Visual Context              : {integration_review['no_tool_use_from_visual_context']}")
        print(f"No Autonomous Action                         : {integration_review['no_autonomous_action']}")
        print()
        print("Sprint 210 Vision Runtime Stabilization")
        print("---------------------------------------")
        print(f"Vision Runtime Stabilization Contract : {stabilization['vision_runtime_stabilization_contract_ready']}")
        print(f"Vision Runtime Stabilization Runtime  : {stabilization['vision_runtime_stabilization_runtime_ready']}")
        print(f"Vision Runtime Stabilization Status   : {stabilization['vision_runtime_stabilization_status']}")
        print(f"Vision Block Start                    : {stabilization['vision_runtime_block_start']}")
        print(f"Vision Block End                      : {stabilization['vision_runtime_block_end']}")
        print(f"Current Sprint                        : {stabilization['vision_runtime_current_sprint']}")
        print(f"Next Sprint                           : {stabilization['vision_runtime_next_sprint']}")
        print(f"Next Boundary                         : {stabilization['vision_runtime_next_boundary']}")
        print(f"Vision Block Complete                 : {stabilization['vision_runtime_block_201_210_complete']}")
        print(f"Vision Block Stabilized               : {stabilization['vision_runtime_block_201_210_stabilized']}")
        print(f"Previous Contract Chain Complete      : {stabilization['previous_contract_chain_complete']}")
        print(f"Runtime Ready                         : {stabilization['runtime_ready']}")
        print(f"Runtime Activation                    : {stabilization['runtime_activation_allowed']}")
        print(f"Release Gate Open                     : {stabilization['release_gate_open']}")
        print(f"Contract Only                         : {stabilization['vision_runtime_stabilization_contract_only']}")
        print(f"Stabilization Acceptance Packet Schema: {stabilization['stabilization_acceptance_packet_schema_ready']}")
        print(f"Stabilization Summary Schema          : {stabilization['stabilization_summary_schema_ready']}")
        print(f"Stabilization Gap Report Schema       : {stabilization['stabilization_gap_report_schema_ready']}")
        print(f"Stabilization Blocker Report Schema   : {stabilization['stabilization_blocker_report_schema_ready']}")
        print(f"Stabilization Dependency Baseline Schema: {stabilization['stabilization_dependency_baseline_schema_ready']}")
        print(f"Stabilization Release Gate Schema     : {stabilization['stabilization_release_gate_schema_ready']}")
        print(f"Stabilization Runtime Scope Schema    : {stabilization['stabilization_runtime_scope_schema_ready']}")
        print(f"Stabilization Safety Matrix Schema    : {stabilization['stabilization_safety_matrix_schema_ready']}")
        print(f"Stabilization Handoff Packet Schema   : {stabilization['stabilization_handoff_packet_schema_ready']}")
        print(f"Stabilization Next Block Schema       : {stabilization['stabilization_next_block_schema_ready']}")
        print(f"Sprint 201 Activation Stabilized      : {stabilization['sprint_201_activation_stabilized']}")
        print(f"Sprint 202 Screenshot Stabilized      : {stabilization['sprint_202_screenshot_stabilized']}")
        print(f"Sprint 203 Screen Context Stabilized  : {stabilization['sprint_203_screen_context_stabilized']}")
        print(f"Sprint 204 Local Model Stabilized     : {stabilization['sprint_204_local_model_stabilized']}")
        print(f"Sprint 205 Permission Redaction Stabilized: {stabilization['sprint_205_permission_redaction_stabilized']}")
        print(f"Sprint 206 Workspace Visual Stabilized: {stabilization['sprint_206_workspace_visual_stabilized']}")
        print(f"Sprint 207 Vision Chat Stabilized     : {stabilization['sprint_207_vision_to_chat_stabilized']}")
        print(f"Sprint 208 Control Center Panel Stabilized: {stabilization['sprint_208_control_center_panel_stabilized']}")
        print(f"Sprint 209 Integration Review Stabilized: {stabilization['sprint_209_integration_review_stabilized']}")
        print(f"Vision Dependency Baseline Stable     : {stabilization['vision_dependency_baseline_stable']}")
        print(f"Vision Release Gate Stable Closed     : {stabilization['vision_release_gate_stable_closed']}")
        print(f"Vision Safety Blockers Stable Inactive: {stabilization['vision_safety_blockers_stable_inactive']}")
        print(f"Vision Runtime Scope Stable Contract Only: {stabilization['vision_runtime_scope_stable_contract_only']}")
        print(f"Vision Permission First Boundary Stable: {stabilization['vision_permission_first_boundary_stable']}")
        print(f"Vision Redaction First Boundary Stable: {stabilization['vision_redaction_first_boundary_stable']}")
        print(f"Vision Local First Boundary Stable    : {stabilization['vision_local_first_boundary_stable']}")
        print(f"Vision Offline First Boundary Stable  : {stabilization['vision_offline_first_boundary_stable']}")
        print(f"Vision No Action Bypass Boundary Stable: {stabilization['vision_no_action_bypass_boundary_stable']}")
        print(f"Vision No External Data Boundary Stable: {stabilization['vision_no_external_data_boundary_stable']}")
        print(f"Vision Block Handoff To Permission Runtime Ready: {stabilization['vision_block_handoff_to_permission_runtime_ready']}")
        print(f"No Runtime Activation From Stabilization: {stabilization['no_runtime_activation_from_stabilization']}")
        print(f"No Release Gate Open From Stabilization: {stabilization['no_release_gate_open_from_stabilization']}")
        print(f"No Dependency Install From Stabilization: {stabilization['no_dependency_install_from_stabilization']}")
        print(f"No Model Download From Stabilization   : {stabilization['no_model_download_from_stabilization']}")
        print(f"No Screenshot Capture From Stabilization: {stabilization['no_screenshot_capture_from_stabilization']}")
        print(f"No Image File Read From Stabilization  : {stabilization['no_image_file_read_from_stabilization']}")
        print(f"No OCR From Stabilization              : {stabilization['no_ocr_from_stabilization']}")
        print(f"No Model Request From Stabilization    : {stabilization['no_model_request_from_stabilization']}")
        print(f"No Inference From Stabilization        : {stabilization['no_inference_from_stabilization']}")
        print(f"No Chat Handoff From Stabilization     : {stabilization['no_chat_handoff_from_stabilization']}")
        print(f"No Chat Session Write From Stabilization: {stabilization['no_chat_session_write_from_stabilization']}")
        print(f"No Panel Render From Stabilization     : {stabilization['no_panel_render_from_stabilization']}")
        print(f"No Route Creation From Stabilization   : {stabilization['no_route_creation_from_stabilization']}")
        print(f"No API Endpoint Creation From Stabilization: {stabilization['no_api_endpoint_creation_from_stabilization']}")
        print(f"No Data Fetch From Stabilization       : {stabilization['no_data_fetch_from_stabilization']}")
        print(f"No Permission Mutation From Stabilization: {stabilization['no_permission_mutation_from_stabilization']}")
        print(f"No Audit Write From Stabilization      : {stabilization['no_audit_write_from_stabilization']}")
        print(f"No Memory Write From Stabilization     : {stabilization['no_memory_write_from_stabilization']}")
        print(f"No Command Execution From Stabilization: {stabilization['no_command_execution_from_stabilization']}")
        print(f"No Tool Execution From Stabilization   : {stabilization['no_tool_execution_from_stabilization']}")
        print(f"No Visual Action From Stabilization    : {stabilization['no_visual_action_from_stabilization']}")
        print(f"No File Mutation From Stabilization    : {stabilization['no_file_mutation_from_stabilization']}")
        print(f"No Desktop Action From Stabilization   : {stabilization['no_desktop_action_from_stabilization']}")
        print(f"No Network Action From Stabilization   : {stabilization['no_network_action_from_stabilization']}")
        print(f"No Git Action From Stabilization       : {stabilization['no_git_action_from_stabilization']}")
        print(f"No Cloud Fallback From Stabilization   : {stabilization['no_cloud_fallback_from_stabilization']}")
        print(f"No External Upload From Stabilization  : {stabilization['no_external_upload_from_stabilization']}")
        print(f"Safety Blocker Count                   : {stabilization['safety_blocker_count']}")
        print(f"All Safety Blockers Off                : {stabilization['all_safety_blockers_inactive']}")
        print(f"Python Packages                        : {stabilization['python_packages_installed']}/{stabilization['python_packages_total']}")
        print(f"Executables                            : {stabilization['executables_found']}/{stabilization['executables_total']}")
        print(f"Runtime Scope                          : {stabilization['runtime_scope']}")
        print()
        print("Vision Runtime Stabilization Safety State")
        print("-----------------------------------------")
        print(f"Vision Runtime Stabilization Runtime    : {stabilization['vision_runtime_stabilization_runtime_active']}")
        print(f"Stabilization Acceptance Packet Created : {stabilization['stabilization_acceptance_packet_created']}")
        print(f"Stabilization Summary Created           : {stabilization['stabilization_summary_created']}")
        print(f"Stabilization Gap Report Created        : {stabilization['stabilization_gap_report_created']}")
        print(f"Stabilization Blocker Report Created    : {stabilization['stabilization_blocker_report_created']}")
        print(f"Stabilization Release Gate Opened       : {stabilization['stabilization_release_gate_opened']}")
        print(f"Stabilization Handoff Packet Created    : {stabilization['stabilization_handoff_packet_created']}")
        print(f"Runtime Activation Path Open            : {stabilization['runtime_activation_path_open']}")
        print(f"Dependency Install Active               : {stabilization['dependency_install_active']}")
        print(f"Model Download Active                   : {stabilization['model_download_active']}")
        print(f"Screenshot Capture Performed            : {stabilization['screenshot_capture_performed']}")
        print(f"Screenshot File Read                    : {stabilization['screenshot_file_read_active']}")
        print(f"Screen Context Packet Created           : {stabilization['screen_context_packet_created']}")
        print(f"Screen Context Handoff                  : {stabilization['screen_context_handoff_active']}")
        print(f"Local Model Request Active              : {stabilization['local_model_request_active']}")
        print(f"Local Model Inference Active            : {stabilization['local_model_inference_active']}")
        print(f"Model To Chat Handoff                   : {stabilization['model_to_chat_handoff_active']}")
        print(f"Permission Prompt Runtime               : {stabilization['permission_prompt_runtime_active']}")
        print(f"Permission Grant Mutation               : {stabilization['permission_grant_mutation_active']}")
        print(f"Redaction Runtime                       : {stabilization['redaction_runtime_active']}")
        print(f"Redacted Context Created                : {stabilization['redacted_context_created']}")
        print(f"Redaction Audit Write                   : {stabilization['redaction_audit_write_active']}")
        print(f"Workspace Visual Runtime                : {stabilization['workspace_visual_understanding_runtime_active']}")
        print(f"Workspace Visual Summary Created        : {stabilization['workspace_visual_summary_created']}")
        print(f"Workspace To Chat Handoff               : {stabilization['workspace_to_chat_handoff_active']}")
        print(f"Vision To Chat Handoff Runtime          : {stabilization['vision_to_chat_context_handoff_runtime_active']}")
        print(f"Chat Context Packet Created             : {stabilization['chat_context_packet_created']}")
        print(f"Chat Safe Visual Summary Created        : {stabilization['chat_safe_visual_summary_created']}")
        print(f"Chat Message Injection Active           : {stabilization['chat_message_injection_active']}")
        print(f"Chat Session Write Active               : {stabilization['chat_session_write_active']}")
        print(f"Chat Model Request Active               : {stabilization['chat_model_request_active']}")
        print(f"Chat Response Generation Active         : {stabilization['chat_response_generation_active']}")
        print(f"Control Center Vision Panel Runtime     : {stabilization['control_center_vision_panel_runtime_active']}")
        print(f"Control Center Vision Panel Rendered    : {stabilization['control_center_vision_panel_rendered']}")
        print(f"Control Center Vision Panel Route Created: {stabilization['control_center_vision_panel_route_created']}")
        print(f"Control Center Vision Panel API Endpoint Created: {stabilization['control_center_vision_panel_api_endpoint_created']}")
        print(f"Control Center Vision Panel Data Fetch  : {stabilization['control_center_vision_panel_data_fetch_active']}")
        print(f"Panel Permission Mutation               : {stabilization['panel_permission_mutation_active']}")
        print(f"Panel Audit Write                       : {stabilization['panel_audit_write_active']}")
        print(f"Panel Screenshot Control                : {stabilization['panel_screenshot_control_active']}")
        print(f"Panel Camera Control                    : {stabilization['panel_camera_control_active']}")
        print(f"Panel Model Request Control             : {stabilization['panel_model_request_control_active']}")
        print(f"Panel Chat Handoff Control              : {stabilization['panel_chat_handoff_control_active']}")
        print(f"Vision Model Runtime                    : {stabilization['vision_model_runtime_active']}")
        print(f"OCR Runtime Active                      : {stabilization['ocr_runtime_active']}")
        print(f"Image Analysis Runtime                  : {stabilization['image_analysis_runtime_active']}")
        print(f"Object Detection Runtime                : {stabilization['object_detection_runtime_active']}")
        print(f"Visual Action Execution                 : {stabilization['visual_action_execution_active']}")
        print(f"Visual Tool Execution                   : {stabilization['visual_tool_execution_active']}")
        print(f"Command Execution                       : {stabilization['command_execution_active']}")
        print(f"File Mutation                           : {stabilization['file_mutation_active']}")
        print(f"Desktop Action                          : {stabilization['desktop_action_active']}")
        print(f"Network Action                          : {stabilization['network_action_active']}")
        print(f"Git Action                              : {stabilization['git_action_active']}")
        print(f"Memory Write                            : {stabilization['memory_write_active']}")
        print(f"Cloud Vision Fallback                   : {stabilization['cloud_vision_fallback_enabled']}")
        print(f"External Upload                         : {stabilization['external_upload_enabled']}")
        print(f"Visual Context Action Bypass            : {stabilization['visual_context_to_action_bypass_enabled']}")
        print(f"No Tool Use From Visual Context         : {stabilization['no_tool_use_from_visual_context']}")
        print(f"No Autonomous Action                    : {stabilization['no_autonomous_action']}")
        print()
        print("Vision-to-Chat Context Handoff Runtime Safety State")
        print("---------------------------------------------------")
        print(f"Vision Chat Handoff Runtime    : {vision_to_chat['vision_to_chat_context_handoff_runtime_active']}")
        print(f"Chat Context Packet Created    : {vision_to_chat['chat_context_packet_created']}")
        print(f"Chat Safe Visual Summary Created: {vision_to_chat['chat_safe_visual_summary_created']}")
        print(f"Chat Source Attribution Created: {vision_to_chat['chat_source_attribution_created']}")
        print(f"Chat Handoff Preview Created   : {vision_to_chat['chat_handoff_preview_created']}")
        print(f"Chat Message Injection Active  : {vision_to_chat['chat_message_injection_active']}")
        print(f"Chat Session Write Active      : {vision_to_chat['chat_session_write_active']}")
        print(f"Chat Model Request Active      : {vision_to_chat['chat_model_request_active']}")
        print(f"Chat Response Generation Active: {vision_to_chat['chat_response_generation_active']}")
        print(f"Workspace To Chat Handoff      : {vision_to_chat['workspace_to_chat_handoff_active']}")
        print(f"Workspace Visual Summary Created: {vision_to_chat['workspace_visual_summary_created']}")
        print(f"Redaction Runtime              : {vision_to_chat['redaction_runtime_active']}")
        print(f"Redacted Context Created       : {vision_to_chat['redacted_context_created']}")
        print(f"Redaction Audit Write          : {vision_to_chat['redaction_audit_write_active']}")
        print(f"Screenshot Capture Performed   : {vision_to_chat['screenshot_capture_performed']}")
        print(f"Screenshot Output Created      : {vision_to_chat['screenshot_output_file_created']}")
        print(f"Screenshot File Read           : {vision_to_chat['screenshot_file_read_active']}")
        print(f"Screen Context Packet Created  : {vision_to_chat['screen_context_packet_created']}")
        print(f"Screen Context Handoff         : {vision_to_chat['screen_context_handoff_active']}")
        print(f"Local Vision Adapter Active    : {vision_to_chat['local_vision_model_adapter_active']}")
        print(f"Local Model Request Active     : {vision_to_chat['local_model_request_active']}")
        print(f"Local Model Inference Active   : {vision_to_chat['local_model_inference_active']}")
        print(f"Model To Chat Handoff          : {vision_to_chat['model_to_chat_handoff_active']}")
        print(f"Vision Model Runtime           : {vision_to_chat['vision_model_runtime_active']}")
        print(f"OCR Runtime Active             : {vision_to_chat['ocr_runtime_active']}")
        print(f"Image Analysis Runtime         : {vision_to_chat['image_analysis_runtime_active']}")
        print(f"Object Detection Runtime       : {vision_to_chat['object_detection_runtime_active']}")
        print(f"Visual Action Execution        : {vision_to_chat['visual_action_execution_active']}")
        print(f"Visual Tool Execution          : {vision_to_chat['visual_tool_execution_active']}")
        print(f"Command Execution              : {vision_to_chat['command_execution_active']}")
        print(f"Memory Write                   : {vision_to_chat['memory_write_active']}")
        print(f"Cloud Vision Fallback          : {vision_to_chat['cloud_vision_fallback_enabled']}")
        print(f"External Upload                : {vision_to_chat['external_upload_enabled']}")
        print(f"Visual Context Action Bypass   : {vision_to_chat['visual_context_to_action_bypass_enabled']}")
        print(f"No Tool Use From Visual Context: {vision_to_chat['no_tool_use_from_visual_context']}")
        print(f"No Autonomous Action           : {vision_to_chat['no_autonomous_action']}")
        print()
        print("Vision Safety Blockers")
        print("----------------------")
        for blocker in vision_to_chat["safety_blockers"]:
            print(f"- {blocker}")
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
        env = dependencies["environment"]
        print(f"OS                 : {env['os']}")
        print(f"OS Release         : {env['os_release']}")
        print(f"Machine            : {env['machine']}")
        print(f"Desktop Environment: {env['desktop_environment'] or 'unknown'}")
        print(f"Display            : {env['display'] or '-'}")
        print(f"Wayland Display    : {env['wayland_display'] or '-'}")
        print(f"XDG Runtime        : {env['xdg_runtime'] or '-'}")
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
        print(f"Voice Intent Chat Contract  : {status['voice_intent_chat_contract_ready']}")
        print(f"Voice Intent Runtime Ready  : {status['voice_intent_runtime_ready']}")
        print(f"Transcript Source           : {status['transcript_source']}")
        print(f"Transcript Chat Handoff Ready: {status['transcript_to_chat_handoff_ready']}")
        print(f"Transcript Chat Handoff Active: {status['transcript_to_chat_handoff_active']}")
        print(f"Intent Classification Active: {status['intent_classification_runtime_active']}")
        print(f"Chat Session Write Active   : {status['chat_session_write_active']}")
        print(f"Voice Direct Action Enabled : {status['voice_intent_direct_voice_to_action_enabled']}")
        print(f"Voice Command Execution     : {status['voice_intent_command_execution_active']}")
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
        print(f"TTS Adapter Contract Ready  : {status['tts_adapter_contract_ready']}")
        print(f"TTS Adapter Runtime Ready   : {status['tts_adapter_runtime_ready']}")
        print(f"TTS Default Adapter         : {status['tts_default_adapter']}")
        print(f"TTS Adapter Candidates      : {status['tts_adapter_candidates']}")
        print(f"Voice Response Input Boundary: {status['voice_response_input_boundary_ready']}")
        print(f"TTS Synthesis Active        : {status['tts_synthesis_runtime_active']}")
        print(f"Speaker Playback Active     : {status['speaker_playback_active']}")
        print(f"Audio Output File Write     : {status['audio_output_file_write_active']}")
        print(f"Auto Speak After Chat       : {status['automatic_speak_after_chat_enabled']}")
        print(f"Cloud TTS Fallback          : {status['cloud_tts_fallback_enabled']}")
        print(f"Voice Permission Audit Contract: {status['voice_permission_audit_contract_ready']}")
        print(f"Voice Permission Audit Runtime : {status['voice_permission_audit_runtime_ready']}")
        print(f"Voice Permission Boundary      : {status['voice_permission_boundary_ready']}")
        print(f"Voice Mic Permission Action    : {status['voice_microphone_permission_action']}")
        print(f"Voice Speaker Permission Action: {status['voice_speaker_permission_action']}")
        print(f"Voice Mic Confirm Required     : {status['voice_microphone_permission_requires_confirmation']}")
        print(f"Voice Speaker Confirm Required : {status['voice_speaker_permission_requires_confirmation']}")
        print(f"Voice Audit Event Contract     : {status['voice_audit_event_contract_ready']}")
        print(f"Voice Audit Write Active       : {status['voice_audit_write_runtime_active']}")
        print(f"Voice Permission Decision Active: {status['voice_permission_decision_runtime_active']}")
        print(f"Voice Permission Grant Active  : {status['voice_permission_grant_runtime_active']}")
        print(f"Voice Permission Mutation Active: {status['voice_permission_mutation_active']}")
        print(f"Control Center Voice Contract   : {status['control_center_voice_controls_contract_ready']}")
        print(f"Control Center Voice Runtime    : {status['control_center_voice_controls_runtime_ready']}")
        print(f"Control Center Voice Visible    : {status['control_center_voice_controls_visible']}")
        print(f"Control Center Voice Read Only  : {status['control_center_voice_controls_read_only']}")
        print(f"Control Center Voice Disabled   : {status['control_center_voice_controls_disabled_by_default']}")
        print(f"Control Center Voice Route Ready: {status['control_center_voice_controls_route_contract_ready']}")
        print(f"Control Center Voice Panel Ready: {status['control_center_voice_controls_panel_contract_ready']}")
        print(f"Control Center Voice Listen UI  : {status['control_center_voice_listen_state_display_ready']}")
        print(f"Control Center Voice Mic UI     : {status['control_center_voice_microphone_permission_display_ready']}")
        print(f"Control Center Voice Speaker UI : {status['control_center_voice_speaker_permission_display_ready']}")
        print(f"Control Center Voice Mutation   : {status['control_center_voice_ui_mutation_enabled']}")
        print(f"Control Center Voice Action UI  : {status['control_center_voice_ui_voice_action_trigger_active']}")
        print(f"Voice Integration Review        : {status['voice_runtime_integration_review_contract_ready']}")
        print(f"Voice Integration Runtime       : {status['voice_runtime_integration_review_runtime_ready']}")
        print(f"Voice Integration Status        : {status['voice_runtime_integration_review_status']}")
        print(f"Voice Reviewed Contracts        : {status['voice_runtime_reviewed_contract_count']}")
        print(f"Voice Integration Matrix        : {status['voice_runtime_integration_matrix_ready']}")
        print(f"Voice Prior Contracts Ready     : {status['voice_runtime_all_prior_contracts_ready']}")
        print(f"Voice Prior Runtimes Blocked    : {status['voice_runtime_all_prior_runtimes_not_ready']}")
        print(f"Voice Safety Blocker Matrix     : {status['voice_runtime_safety_blocker_matrix_ready']}")
        print(f"Voice Safety Blocker Count      : {status['voice_runtime_safety_blocker_count']}")
        print(f"Voice Runtime Activation Allowed: {status['voice_runtime_activation_allowed']}")
        print(f"Voice Stabilization Contract    : {status['voice_runtime_stabilization_contract_ready']}")
        print(f"Voice Stabilization Runtime     : {status['voice_runtime_stabilization_runtime_ready']}")
        print(f"Voice Stabilization Status      : {status['voice_runtime_stabilization_status']}")
        print(f"Voice Stabilization Passed      : {status['voice_runtime_stabilization_passed']}")
        print(f"Voice Block 191-200 Complete    : {status['voice_runtime_block_191_200_complete']}")
        print(f"Voice Stabilized Contracts      : {status['voice_runtime_stabilized_contract_count']}")
        print(f"Voice Stabilization Components  : {status['voice_runtime_stabilization_component_count']}")
        print(f"Voice Stabilization Gaps        : {status['voice_runtime_stabilization_gap_count']}")
        print(f"Voice Stabilization Blockers    : {status['voice_runtime_stabilization_safety_blocker_count']}")
        print(f"Voice Release Gate Open         : {status['voice_runtime_release_gate_open']}")
        print(f"Voice Next Sprint               : {status['voice_runtime_next_sprint']}")
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
        print("Sprint 195 Voice Intent and Chat Integration")
        print("--------------------------------------------")
        print(f"Voice Intent Chat Contract : {voice_intent_chat['voice_intent_chat_contract_ready']}")
        print(f"Voice Intent Runtime Ready : {voice_intent_chat['voice_intent_runtime_ready']}")
        print(f"Voice Intent Layer Contract: {voice_intent_chat['voice_intent_layer_contract_ready']}")
        print(f"Transcript Source          : {voice_intent_chat['transcript_source']}")
        print(f"Transcript Input Boundary  : {voice_intent_chat['transcript_input_boundary_ready']}")
        print(f"Provided Transcript Required: {voice_intent_chat['provided_transcript_required_for_future_dry_run']}")
        print(f"Dummy Transcript Allowed   : {voice_intent_chat['dummy_transcript_allowed_for_contract']}")
        print(f"Live Transcript Input      : {voice_intent_chat['live_transcript_input_active']}")
        print(f"Normalization Contract     : {voice_intent_chat['transcript_normalization_contract_ready']}")
        print(f"Normalization Runtime      : {voice_intent_chat['transcript_normalization_runtime_active']}")
        print(f"Intent Contract            : {voice_intent_chat['intent_classification_contract_ready']}")
        print(f"Intent Runtime             : {voice_intent_chat['intent_classification_runtime_active']}")
        print(f"Intent Confidence Runtime  : {voice_intent_chat['intent_confidence_runtime_active']}")
        print(f"Clarification Gate Contract: {voice_intent_chat['clarification_gate_contract_ready']}")
        print(f"Action Gate Contract       : {voice_intent_chat['action_intent_gate_contract_ready']}")
        print(f"Voice Response Contract    : {voice_intent_chat['voice_response_plan_contract_ready']}")
        print(f"Chat Handoff Contract      : {voice_intent_chat['transcript_to_chat_handoff_contract_ready']}")
        print(f"Chat Handoff Active        : {voice_intent_chat['transcript_to_chat_handoff_active']}")
        print(f"Chat Session Reuse Required: {voice_intent_chat['chat_session_reuse_required']}")
        print(f"Chat Session Write Active  : {voice_intent_chat['chat_session_write_active']}")
        print(f"Chat Model Request Active  : {voice_intent_chat['chat_model_request_active']}")
        print(f"Chat Response Generation   : {voice_intent_chat['chat_response_generation_active']}")
        print(f"Permission Before Handoff  : {voice_intent_chat['permission_required_before_chat_handoff']}")
        print(f"Human Confirm Action Intent: {voice_intent_chat['human_confirmation_required_for_action_intent']}")
        print(f"Transcript Persistence     : {voice_intent_chat['transcript_persistence_enabled']}")
        print(f"Memory Write Active        : {voice_intent_chat['memory_write_active']}")
        print(f"Direct Voice To Action     : {voice_intent_chat['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active      : {voice_intent_chat['tool_execution_active']}")
        print(f"Command Execution Active   : {voice_intent_chat['command_execution_active']}")
        print(f"File Mutation Active       : {voice_intent_chat['file_mutation_active']}")
        print(f"Desktop Action Active      : {voice_intent_chat['desktop_action_active']}")
        print(f"Network Action Active      : {voice_intent_chat['network_action_active']}")
        print(f"Git Action Active          : {voice_intent_chat['git_action_active']}")
        print(f"STT Runtime Active         : {voice_intent_chat['stt_runtime_active']}")
        print(f"Transcription Active       : {voice_intent_chat['transcription_active']}")
        print(f"Live Mic Transcription     : {voice_intent_chat['live_microphone_transcription_active']}")
        print(f"TTS Runtime Active         : {voice_intent_chat['tts_runtime_active']}")
        print(f"Speaker Playback Active    : {voice_intent_chat['speaker_playback_active']}")
        print(f"Cloud STT Fallback         : {voice_intent_chat['cloud_stt_fallback_enabled']}")
        print(f"Silent Cloud Fallback      : {voice_intent_chat['silent_cloud_fallback_enabled']}")
        print()
        print("Sprint 196 Text-to-Speech Adapter Runtime")
        print("-----------------------------------------")
        print(f"TTS Adapter Contract Ready : {tts_adapter['tts_adapter_contract_ready']}")
        print(f"TTS Adapter Runtime Ready  : {tts_adapter['tts_adapter_runtime_ready']}")
        print(f"Default Adapter            : {tts_adapter['default_adapter']}")
        print(f"Candidate Adapter Count    : {tts_adapter['candidate_adapter_count']}")
        print(f"Local First Required       : {tts_adapter['local_first_required']}")
        print(f"Offline First Required     : {tts_adapter['offline_first_required']}")
        print(f"Voice Response Input Boundary: {tts_adapter['voice_response_input_boundary_ready']}")
        print(f"Provided Text Required     : {tts_adapter['provided_text_required_for_future_dry_run']}")
        print(f"Dummy Text Allowed         : {tts_adapter['dummy_text_allowed_for_contract']}")
        print(f"Text Normalization Contract: {tts_adapter['tts_text_normalization_contract_ready']}")
        print(f"TTS Synthesis Runtime Ready: {tts_adapter['tts_synthesis_runtime_ready']}")
        print(f"TTS Synthesis Active       : {tts_adapter['tts_synthesis_runtime_active']}")
        print(f"Audio Output Boundary Ready: {tts_adapter['audio_output_file_boundary_ready']}")
        print(f"Audio Output File Write    : {tts_adapter['audio_output_file_write_active']}")
        print(f"Audio Output File Read     : {tts_adapter['audio_output_file_read_active']}")
        print(f"Audio File Persistence     : {tts_adapter['audio_file_persistence_enabled']}")
        print(f"Speaker Permission Required: {tts_adapter['speaker_playback_permission_required']}")
        print(f"Speaker Permission Action  : {tts_adapter['speaker_permission_action']}")
        print(f"Speaker Runtime Ready      : {tts_adapter['speaker_playback_runtime_ready']}")
        print(f"Speaker Playback Active    : {tts_adapter['speaker_playback_active']}")
        print(f"Playback Device Access     : {tts_adapter['audio_playback_device_access']}")
        print(f"Playback Device Discovery  : {tts_adapter['audio_playback_device_discovery_active']}")
        print(f"Playback Enabled           : {tts_adapter['playback_enabled']}")
        print(f"Auto Speak After Chat      : {tts_adapter['automatic_speak_after_chat_enabled']}")
        print(f"Voice Response Playback    : {tts_adapter['voice_response_playback_active']}")
        print(f"Chat Response TTS Contract : {tts_adapter['chat_response_to_tts_handoff_contract_ready']}")
        print(f"Chat Response TTS Active   : {tts_adapter['chat_response_to_tts_handoff_active']}")
        print(f"Model Download Required    : {tts_adapter['model_download_required']}")
        print(f"Model Download Performed   : {tts_adapter['model_download_performed']}")
        print(f"Dependency Install Performed: {tts_adapter['dependency_install_performed']}")
        print(f"Cloud TTS Fallback         : {tts_adapter['cloud_tts_fallback_enabled']}")
        print(f"Silent Cloud Fallback      : {tts_adapter['silent_cloud_fallback_enabled']}")
        print(f"Remote TTS Provider Enabled: {tts_adapter['remote_tts_provider_enabled']}")
        print(f"STT Runtime Active         : {tts_adapter['stt_runtime_active']}")
        print(f"Transcription Active       : {tts_adapter['transcription_active']}")
        print(f"Microphone Capture Active  : {tts_adapter['microphone_capture_active']}")
        print(f"Audio Device Access        : {tts_adapter['audio_device_access']}")
        print(f"Audio Buffer Active        : {tts_adapter['audio_buffer_active']}")
        print(f"Memory Write Active        : {tts_adapter['memory_write_active']}")
        print(f"Direct Voice To Action     : {tts_adapter['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active      : {tts_adapter['tool_execution_active']}")
        print(f"Command Execution Active   : {tts_adapter['command_execution_active']}")
        print(f"File Mutation Active       : {tts_adapter['file_mutation_active']}")
        print(f"Desktop Action Active      : {tts_adapter['desktop_action_active']}")
        print(f"Network Action Active      : {tts_adapter['network_action_active']}")
        print(f"Git Action Active          : {tts_adapter['git_action_active']}")
        print()
        print("TTS Adapter Candidates")
        print("----------------------")
        for adapter in tts_adapter["candidate_adapters"]:
            print(f"- {adapter}")
        print()
        print("Sprint 197 Voice Permission and Audit Runtime")
        print("---------------------------------------------")
        print(f"Voice Permission Audit Contract: {voice_permission_audit['voice_permission_audit_contract_ready']}")
        print(f"Voice Permission Audit Runtime : {voice_permission_audit['voice_permission_audit_runtime_ready']}")
        print(f"Permission Boundary Ready      : {voice_permission_audit['permission_boundary_ready']}")
        print(f"Microphone Permission Action   : {voice_permission_audit['microphone_permission_action']}")
        print(f"Speaker Permission Action      : {voice_permission_audit['speaker_permission_action']}")
        print(f"Microphone Permission Required : {voice_permission_audit['microphone_permission_required']}")
        print(f"Speaker Permission Required    : {voice_permission_audit['speaker_permission_required']}")
        print(f"Microphone Permission Allowed  : {voice_permission_audit['microphone_permission_allowed']}")
        print(f"Speaker Permission Allowed     : {voice_permission_audit['speaker_permission_allowed']}")
        print(f"Microphone Confirm Required    : {voice_permission_audit['microphone_permission_requires_confirmation']}")
        print(f"Speaker Confirm Required       : {voice_permission_audit['speaker_permission_requires_confirmation']}")
        print(f"Transcript Handoff Permission  : {voice_permission_audit['transcript_chat_handoff_permission_required']}")
        print(f"Chat Response TTS Permission   : {voice_permission_audit['chat_response_tts_permission_required']}")
        print(f"Voice Action Permission        : {voice_permission_audit['voice_action_permission_required']}")
        print(f"Permission Before Mic Capture  : {voice_permission_audit['permission_before_microphone_capture']}")
        print(f"Permission Before STT          : {voice_permission_audit['permission_before_stt']}")
        print(f"Permission Before TTS          : {voice_permission_audit['permission_before_tts']}")
        print(f"Permission Before Speaker      : {voice_permission_audit['permission_before_speaker_playback']}")
        print(f"Permission Before Chat Handoff : {voice_permission_audit['permission_before_chat_handoff']}")
        print(f"Human Confirm Voice Action     : {voice_permission_audit['human_confirmation_required_for_voice_action_intent']}")
        print(f"Audit Event Contract Ready     : {voice_permission_audit['audit_event_contract_ready']}")
        print(f"Audit Event Schema Ready       : {voice_permission_audit['audit_event_schema_ready']}")
        print(f"Audit Event Type Count         : {voice_permission_audit['audit_event_type_count']}")
        print(f"Audit Redaction Boundary       : {voice_permission_audit['audit_event_redaction_boundary_ready']}")
        print(f"Audit Local Only Required      : {voice_permission_audit['audit_event_local_only_required']}")
        print(f"Audit Append Only Boundary     : {voice_permission_audit['audit_event_append_only_boundary_ready']}")
        print(f"Audit Write Runtime Ready      : {voice_permission_audit['audit_write_runtime_ready']}")
        print(f"Audit Write Runtime Active     : {voice_permission_audit['audit_write_runtime_active']}")
        print(f"Audit Event Persistence        : {voice_permission_audit['audit_event_persistence_enabled']}")
        print(f"Audit Log Append Active        : {voice_permission_audit['audit_log_append_active']}")
        print(f"Audit Storage Write Active     : {voice_permission_audit['audit_storage_write_active']}")
        print(f"Audit Dashboard Emit Active    : {voice_permission_audit['audit_dashboard_event_emit_active']}")
        print(f"Audit Redaction Runtime        : {voice_permission_audit['audit_redaction_runtime_active']}")
        print(f"Audit Permission Link Runtime  : {voice_permission_audit['audit_permission_link_runtime_active']}")
        print(f"Review Queue Contract Ready    : {voice_permission_audit['review_queue_contract_ready']}")
        print(f"Review Queue Runtime Active    : {voice_permission_audit['review_queue_runtime_active']}")
        print(f"Recovery Visibility Contract   : {voice_permission_audit['recovery_visibility_contract_ready']}")
        print(f"Recovery Action Runtime        : {voice_permission_audit['recovery_action_runtime_active']}")
        print(f"Permission Decision Runtime    : {voice_permission_audit['permission_decision_runtime_active']}")
        print(f"Permission Grant Runtime       : {voice_permission_audit['permission_grant_runtime_active']}")
        print(f"Permission Revoke Runtime      : {voice_permission_audit['permission_revoke_runtime_active']}")
        print(f"Permission Persistence         : {voice_permission_audit['permission_persistence_active']}")
        print(f"Permission Mutation Active     : {voice_permission_audit['permission_mutation_active']}")
        print(f"Microphone Capture Active      : {voice_permission_audit['microphone_capture_active']}")
        print(f"STT Runtime Active             : {voice_permission_audit['stt_runtime_active']}")
        print(f"Transcription Active           : {voice_permission_audit['transcription_active']}")
        print(f"Live Mic Transcription         : {voice_permission_audit['live_microphone_transcription_active']}")
        print(f"TTS Runtime Active             : {voice_permission_audit['tts_runtime_active']}")
        print(f"TTS Synthesis Active           : {voice_permission_audit['tts_synthesis_runtime_active']}")
        print(f"Speaker Playback Active        : {voice_permission_audit['speaker_playback_active']}")
        print(f"Audio Device Access            : {voice_permission_audit['audio_device_access']}")
        print(f"Playback Device Access         : {voice_permission_audit['playback_device_access']}")
        print(f"Audio Buffer Active            : {voice_permission_audit['audio_buffer_active']}")
        print(f"Transcript Chat Handoff Active : {voice_permission_audit['transcript_to_chat_handoff_active']}")
        print(f"Chat Response TTS Handoff Active: {voice_permission_audit['chat_response_to_tts_handoff_active']}")
        print(f"Memory Write Active            : {voice_permission_audit['memory_write_active']}")
        print(f"Direct Voice To Action         : {voice_permission_audit['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active          : {voice_permission_audit['tool_execution_active']}")
        print(f"Command Execution Active       : {voice_permission_audit['command_execution_active']}")
        print(f"File Mutation Active           : {voice_permission_audit['file_mutation_active']}")
        print(f"Desktop Action Active          : {voice_permission_audit['desktop_action_active']}")
        print(f"Network Action Active          : {voice_permission_audit['network_action_active']}")
        print(f"Git Action Active              : {voice_permission_audit['git_action_active']}")
        print(f"Cloud STT Fallback             : {voice_permission_audit['cloud_stt_fallback_enabled']}")
        print(f"Cloud TTS Fallback             : {voice_permission_audit['cloud_tts_fallback_enabled']}")
        print(f"Silent Cloud Fallback          : {voice_permission_audit['silent_cloud_fallback_enabled']}")
        print()
        print("Voice Audit Event Types")
        print("-----------------------")
        for event_type in voice_permission_audit["audit_event_types"]:
            print(f"- {event_type}")
        print()
        print("Sprint 198 Control Center Voice Controls")
        print("----------------------------------------")
        print(f"Control Center Voice Contract : {control_center_voice['control_center_voice_controls_contract_ready']}")
        print(f"Control Center Voice Runtime  : {control_center_voice['control_center_voice_controls_runtime_ready']}")
        print(f"Visible In Control Center     : {control_center_voice['control_center_voice_controls_visible']}")
        print(f"Read Only                     : {control_center_voice['control_center_voice_controls_read_only']}")
        print(f"Disabled By Default           : {control_center_voice['control_center_voice_controls_disabled_by_default']}")
        print(f"Route Contract Ready          : {control_center_voice['control_center_voice_controls_route_contract_ready']}")
        print(f"Panel Contract Ready          : {control_center_voice['control_center_voice_controls_panel_contract_ready']}")
        print(f"Panel ID                      : {control_center_voice['control_center_voice_controls_panel_id']}")
        print(f"Route                         : {control_center_voice['control_center_voice_controls_route']}")
        print(f"Web Panel Anchor              : {control_center_voice['control_center_voice_controls_web_panel_anchor']}")
        print(f"Listen State Display Ready    : {control_center_voice['listen_state_display_boundary_ready']}")
        print(f"Default Listen State          : {control_center_voice['default_listen_state']}")
        print(f"Current Listen State          : {control_center_voice['current_listen_state']}")
        print(f"Allowed Listen State Count    : {control_center_voice['allowed_listen_state_count']}")
        print(f"Push To Talk Display Ready    : {control_center_voice['push_to_talk_display_ready']}")
        print(f"Push To Talk Required         : {control_center_voice['push_to_talk_required']}")
        print(f"Microphone Permission UI      : {control_center_voice['microphone_permission_display_boundary_ready']}")
        print(f"Speaker Permission UI         : {control_center_voice['speaker_permission_display_boundary_ready']}")
        print(f"Microphone Permission Action  : {control_center_voice['microphone_permission_action']}")
        print(f"Speaker Permission Action     : {control_center_voice['speaker_permission_action']}")
        print(f"Microphone Confirm Required   : {control_center_voice['microphone_permission_requires_confirmation']}")
        print(f"Speaker Confirm Required      : {control_center_voice['speaker_permission_requires_confirmation']}")
        print(f"STT Status Display Ready      : {control_center_voice['stt_adapter_status_display_boundary_ready']}")
        print(f"TTS Status Display Ready      : {control_center_voice['tts_adapter_status_display_boundary_ready']}")
        print(f"STT Contract Ready            : {control_center_voice['stt_adapter_contract_ready']}")
        print(f"TTS Contract Ready            : {control_center_voice['tts_adapter_contract_ready']}")
        print(f"STT Runtime Ready             : {control_center_voice['stt_adapter_runtime_ready']}")
        print(f"TTS Runtime Ready             : {control_center_voice['tts_adapter_runtime_ready']}")
        print(f"Voice Intent Display Ready    : {control_center_voice['voice_intent_chat_status_display_boundary_ready']}")
        print(f"Permission Audit Display Ready: {control_center_voice['voice_permission_audit_status_display_boundary_ready']}")
        print(f"Audit Event Display Ready     : {control_center_voice['audit_event_status_display_boundary_ready']}")
        print(f"Runtime Safety Badges Ready   : {control_center_voice['runtime_safety_badges_ready']}")
        print(f"Disabled Control Count        : {control_center_voice['disabled_control_count']}")
        print(f"UI Mutation Enabled           : {control_center_voice['ui_controls_mutation_enabled']}")
        print(f"UI Start Listening Active     : {control_center_voice['ui_start_listening_action_active']}")
        print(f"UI Stop Listening Active      : {control_center_voice['ui_stop_listening_action_active']}")
        print(f"UI Push To Talk Active        : {control_center_voice['ui_push_to_talk_action_active']}")
        print(f"UI Mic Capture Trigger        : {control_center_voice['ui_microphone_capture_trigger_active']}")
        print(f"UI STT Trigger                : {control_center_voice['ui_stt_trigger_active']}")
        print(f"UI TTS Trigger                : {control_center_voice['ui_tts_trigger_active']}")
        print(f"UI Speaker Trigger            : {control_center_voice['ui_speaker_playback_trigger_active']}")
        print(f"UI Permission Grant Trigger   : {control_center_voice['ui_permission_grant_trigger_active']}")
        print(f"UI Permission Revoke Trigger  : {control_center_voice['ui_permission_revoke_trigger_active']}")
        print(f"UI Permission Mutation Trigger: {control_center_voice['ui_permission_mutation_trigger_active']}")
        print(f"UI Audit Write Trigger        : {control_center_voice['ui_audit_write_trigger_active']}")
        print(f"UI Voice Action Trigger       : {control_center_voice['ui_voice_action_trigger_active']}")
        print(f"UI Command Trigger            : {control_center_voice['ui_command_execution_trigger_active']}")
        print(f"UI Tool Trigger               : {control_center_voice['ui_tool_execution_trigger_active']}")
        print(f"UI File Mutation Trigger      : {control_center_voice['ui_file_mutation_trigger_active']}")
        print(f"API GET Contract Ready        : {control_center_voice['api_get_route_contract_ready']}")
        print(f"API POST Mutation Enabled     : {control_center_voice['api_post_mutation_route_enabled']}")
        print(f"API Localhost Only Required   : {control_center_voice['api_requires_localhost_only']}")
        print(f"API Read Only Payload Ready   : {control_center_voice['api_read_only_payload_ready']}")
        print(f"API No Credentials Exposed    : {control_center_voice['api_no_credentials_exposed']}")
        print(f"API No Sensitive Values       : {control_center_voice['api_no_sensitive_values_exposed']}")
        print(f"Frontend Read Only Binding    : {control_center_voice['frontend_read_only_binding_ready']}")
        print(f"Frontend Mutation Controls    : {control_center_voice['frontend_mutation_controls_present']}")
        print(f"Frontend Button Actions       : {control_center_voice['frontend_button_actions_enabled']}")
        print(f"Frontend Permission Buttons   : {control_center_voice['frontend_permission_grant_buttons_enabled']}")
        print(f"Frontend Audio Device Buttons : {control_center_voice['frontend_audio_device_buttons_enabled']}")
        print(f"Frontend Audit Write Buttons  : {control_center_voice['frontend_audit_write_buttons_enabled']}")
        print(f"Visibility Link Allowed       : {control_center_voice['control_center_link_to_visibility_allowed']}")
        print(f"Panel Uses Status Only        : {control_center_voice['control_center_voice_panel_uses_status_only']}")
        print(f"Panel Uses Permission/Audit   : {control_center_voice['control_center_voice_panel_uses_permission_audit_visibility']}")
        print(f"Microphone Capture Active     : {control_center_voice['microphone_capture_active']}")
        print(f"STT Runtime Active            : {control_center_voice['stt_runtime_active']}")
        print(f"Transcription Active          : {control_center_voice['transcription_active']}")
        print(f"Live Mic Transcription        : {control_center_voice['live_microphone_transcription_active']}")
        print(f"TTS Runtime Active            : {control_center_voice['tts_runtime_active']}")
        print(f"TTS Synthesis Active          : {control_center_voice['tts_synthesis_runtime_active']}")
        print(f"Speaker Playback Active       : {control_center_voice['speaker_playback_active']}")
        print(f"Audio Device Access           : {control_center_voice['audio_device_access']}")
        print(f"Playback Device Access        : {control_center_voice['playback_device_access']}")
        print(f"Audio Buffer Active           : {control_center_voice['audio_buffer_active']}")
        print(f"Transcript Chat Handoff Active: {control_center_voice['transcript_to_chat_handoff_active']}")
        print(f"Chat Response TTS Handoff     : {control_center_voice['chat_response_to_tts_handoff_active']}")
        print(f"Permission Decision Runtime   : {control_center_voice['permission_decision_runtime_active']}")
        print(f"Permission Grant Runtime      : {control_center_voice['permission_grant_runtime_active']}")
        print(f"Permission Mutation Active    : {control_center_voice['permission_mutation_active']}")
        print(f"Audit Write Runtime Active    : {control_center_voice['audit_write_runtime_active']}")
        print(f"Audit Event Persistence       : {control_center_voice['audit_event_persistence_enabled']}")
        print(f"Memory Write Active           : {control_center_voice['memory_write_active']}")
        print(f"Direct Voice To Action        : {control_center_voice['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active         : {control_center_voice['tool_execution_active']}")
        print(f"Command Execution Active      : {control_center_voice['command_execution_active']}")
        print(f"File Mutation Active          : {control_center_voice['file_mutation_active']}")
        print(f"Desktop Action Active         : {control_center_voice['desktop_action_active']}")
        print(f"Network Action Active         : {control_center_voice['network_action_active']}")
        print(f"Git Action Active             : {control_center_voice['git_action_active']}")
        print(f"Cloud STT Fallback            : {control_center_voice['cloud_stt_fallback_enabled']}")
        print(f"Cloud TTS Fallback            : {control_center_voice['cloud_tts_fallback_enabled']}")
        print(f"Silent Cloud Fallback         : {control_center_voice['silent_cloud_fallback_enabled']}")
        print()
        print("Disabled Voice Controls")
        print("-----------------------")
        for control in control_center_voice["disabled_controls"]:
            print(f"- {control}")
        print()
        print("Sprint 199 Voice Runtime Integration Review")
        print("-------------------------------------------")
        print(f"Integration Review Contract : {integration_review['voice_runtime_integration_review_contract_ready']}")
        print(f"Integration Review Runtime  : {integration_review['voice_runtime_integration_review_runtime_ready']}")
        print(f"Integration Review Status   : {integration_review['voice_runtime_integration_review_status']}")
        print(f"Reviewed Sprint Start       : {integration_review['reviewed_sprint_start']}")
        print(f"Reviewed Sprint End         : {integration_review['reviewed_sprint_end']}")
        print(f"Reviewed Sprint Count       : {integration_review['reviewed_sprint_count']}")
        print(f"Reviewed Contract Count     : {integration_review['reviewed_contract_count']}")
        print(f"Integration Matrix Ready    : {integration_review['integration_matrix_ready']}")
        print(f"Integration Matrix Items    : {integration_review['integration_matrix_item_count']}")
        print(f"Integration Chain Order     : {integration_review['integration_chain_order_ready']}")
        print(f"All Prior Contracts Ready   : {integration_review['all_prior_contracts_ready']}")
        print(f"All Prior Runtimes Blocked  : {integration_review['all_prior_runtimes_not_ready']}")
        print(f"Activation Contract Ready   : {integration_review['activation_contract_ready']}")
        print(f"Listen State Contract Ready : {integration_review['listen_state_contract_ready']}")
        print(f"Microphone Boundary Ready   : {integration_review['microphone_boundary_contract_ready']}")
        print(f"STT Adapter Contract Ready  : {integration_review['stt_adapter_contract_ready']}")
        print(f"Voice Intent Contract Ready : {integration_review['voice_intent_chat_contract_ready']}")
        print(f"TTS Adapter Contract Ready  : {integration_review['tts_adapter_contract_ready']}")
        print(f"Permission Audit Ready      : {integration_review['voice_permission_audit_contract_ready']}")
        print(f"Control Center Voice Ready  : {integration_review['control_center_voice_controls_contract_ready']}")
        print(f"Safe Idle Reviewed          : {integration_review['safe_idle_default_reviewed']}")
        print(f"Push To Talk Reviewed       : {integration_review['push_to_talk_required_reviewed']}")
        print(f"Explicit Listen Reviewed    : {integration_review['explicit_listen_required_reviewed']}")
        print(f"Default Listen State        : {integration_review['default_listen_state_reviewed']}")
        print(f"Current Listen State        : {integration_review['current_listen_state_reviewed']}")
        print(f"Allowed Listen State Count  : {integration_review['allowed_listen_state_count_reviewed']}")
        print(f"Mic Permission Action       : {integration_review['microphone_permission_action_reviewed']}")
        print(f"Speaker Permission Action   : {integration_review['speaker_permission_action_reviewed']}")
        print(f"Permission Boundary Reviewed: {integration_review['voice_permission_boundary_reviewed']}")
        print(f"Audit Event Contract        : {integration_review['voice_audit_event_contract_reviewed']}")
        print(f"Audit Event Type Count      : {integration_review['voice_audit_event_type_count_reviewed']}")
        print(f"Control Center Route        : {integration_review['control_center_voice_route_reviewed']}")
        print(f"Control Center Panel ID     : {integration_review['control_center_voice_panel_id_reviewed']}")
        print(f"Control Center Read Only    : {integration_review['control_center_voice_read_only_reviewed']}")
        print(f"Control Center Disabled     : {integration_review['control_center_voice_disabled_by_default_reviewed']}")
        print(f"Disabled Control Count      : {integration_review['control_center_disabled_control_count_reviewed']}")
        print(f"Dependency Baseline Reviewed: {integration_review['dependency_baseline_reviewed']}")
        print(f"Python Baseline Expected    : {integration_review['python_package_baseline_expected_installed']}/{integration_review['python_package_baseline_expected_total']}")
        print(f"Executable Baseline Expected: {integration_review['executable_baseline_expected_found']}/{integration_review['executable_baseline_expected_total']}")
        print(f"Permission/Audit Reviewed   : {integration_review['permission_audit_boundary_reviewed']}")
        print(f"Control Center Reviewed     : {integration_review['control_center_boundary_reviewed']}")
        print(f"Handoff Boundary Reviewed   : {integration_review['handoff_boundary_reviewed']}")
        print(f"Safety Blocker Matrix Ready : {integration_review['safety_blocker_matrix_ready']}")
        print(f"Safety Blocker Count        : {integration_review['safety_blocker_count']}")
        print(f"Runtime Activation Allowed  : {integration_review['runtime_activation_allowed']}")
        print(f"Runtime Ready               : {integration_review['runtime_ready']}")
        print(f"Microphone Capture Active   : {integration_review['microphone_capture_active']}")
        print(f"Audio Device Access         : {integration_review['audio_device_access']}")
        print(f"Recording Active            : {integration_review['recording_active']}")
        print(f"Audio Buffer Active         : {integration_review['audio_buffer_active']}")
        print(f"STT Runtime Active          : {integration_review['stt_runtime_active']}")
        print(f"Transcription Active        : {integration_review['transcription_active']}")
        print(f"Live Mic Transcription      : {integration_review['live_microphone_transcription_active']}")
        print(f"Transcript Chat Handoff     : {integration_review['transcript_to_chat_handoff_active']}")
        print(f"Chat Session Write          : {integration_review['chat_session_write_active']}")
        print(f"Chat Model Request          : {integration_review['chat_model_request_active']}")
        print(f"Chat Response Generation    : {integration_review['chat_response_generation_active']}")
        print(f"TTS Runtime Active          : {integration_review['tts_runtime_active']}")
        print(f"TTS Synthesis Active        : {integration_review['tts_synthesis_runtime_active']}")
        print(f"Speaker Playback Active     : {integration_review['speaker_playback_active']}")
        print(f"Playback Device Access      : {integration_review['playback_device_access']}")
        print(f"Permission Decision Runtime : {integration_review['permission_decision_runtime_active']}")
        print(f"Permission Grant Runtime    : {integration_review['permission_grant_runtime_active']}")
        print(f"Permission Revoke Runtime   : {integration_review['permission_revoke_runtime_active']}")
        print(f"Permission Mutation Active  : {integration_review['permission_mutation_active']}")
        print(f"Permission Persistence      : {integration_review['permission_persistence_active']}")
        print(f"Audit Write Runtime         : {integration_review['audit_write_runtime_active']}")
        print(f"Audit Event Persistence     : {integration_review['audit_event_persistence_enabled']}")
        print(f"Audit Log Append            : {integration_review['audit_log_append_active']}")
        print(f"Audit Storage Write         : {integration_review['audit_storage_write_active']}")
        print(f"Audit Dashboard Emit        : {integration_review['audit_dashboard_event_emit_active']}")
        print(f"UI Mutation Enabled         : {integration_review['ui_controls_mutation_enabled']}")
        print(f"UI Mic Capture Trigger      : {integration_review['ui_microphone_capture_trigger_active']}")
        print(f"UI STT Trigger              : {integration_review['ui_stt_trigger_active']}")
        print(f"UI TTS Trigger              : {integration_review['ui_tts_trigger_active']}")
        print(f"UI Speaker Trigger          : {integration_review['ui_speaker_playback_trigger_active']}")
        print(f"UI Permission Grant Trigger : {integration_review['ui_permission_grant_trigger_active']}")
        print(f"UI Audit Write Trigger      : {integration_review['ui_audit_write_trigger_active']}")
        print(f"UI Voice Action Trigger     : {integration_review['ui_voice_action_trigger_active']}")
        print(f"Memory Write Active         : {integration_review['memory_write_active']}")
        print(f"Direct Voice To Action      : {integration_review['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active       : {integration_review['tool_execution_active']}")
        print(f"Command Execution Active    : {integration_review['command_execution_active']}")
        print(f"File Mutation Active        : {integration_review['file_mutation_active']}")
        print(f"Desktop Action Active       : {integration_review['desktop_action_active']}")
        print(f"Network Action Active       : {integration_review['network_action_active']}")
        print(f"Git Action Active           : {integration_review['git_action_active']}")
        print(f"Cloud STT Fallback          : {integration_review['cloud_stt_fallback_enabled']}")
        print(f"Cloud TTS Fallback          : {integration_review['cloud_tts_fallback_enabled']}")
        print(f"Silent Cloud Fallback       : {integration_review['silent_cloud_fallback_enabled']}")
        print()
        print("Voice Integration Matrix")
        print("------------------------")
        for item in integration_review["integration_matrix"]:
            print(f"- Sprint {item['sprint']}: {item['contract']} | ready={item['ready']} | runtime_ready={item['runtime_ready']} | boundary={item['critical_boundary']}")
        print()
        print("Voice Safety Blockers")
        print("---------------------")
        for blocker in integration_review["safety_blockers"]:
            print(f"- {blocker}")
        print()
        print("Sprint 200 Voice Runtime Stabilization")
        print("--------------------------------------")
        print(f"Stabilization Contract    : {stabilization['voice_runtime_stabilization_contract_ready']}")
        print(f"Stabilization Runtime     : {stabilization['voice_runtime_stabilization_runtime_ready']}")
        print(f"Stabilization Status      : {stabilization['voice_runtime_stabilization_status']}")
        print(f"Voice Block Start         : {stabilization['voice_runtime_block_start']}")
        print(f"Voice Block End           : {stabilization['voice_runtime_block_end']}")
        print(f"Voice Block Sprint Count  : {stabilization['voice_runtime_block_sprint_count']}")
        print(f"Stabilized Contract Count : {stabilization['stabilized_contract_count']}")
        print(f"Stabilization Components  : {stabilization['stabilization_component_count']}")
        print(f"Previous Review Ready     : {stabilization['previous_integration_review_ready']}")
        print(f"Previous Review Status    : {stabilization['previous_review_status']}")
        print(f"Previous Contract Count   : {stabilization['previous_reviewed_contract_count']}")
        print(f"Previous Matrix Ready     : {stabilization['previous_integration_matrix_ready']}")
        print(f"Previous Matrix Items     : {stabilization['previous_integration_matrix_item_count']}")
        print(f"Prior Contracts Ready     : {stabilization['previous_all_prior_contracts_ready']}")
        print(f"Prior Runtimes Blocked    : {stabilization['previous_all_prior_runtimes_not_ready']}")
        print(f"Previous Safety Blockers  : {stabilization['previous_safety_blocker_count']}")
        print(f"Dependency Baseline Stable: {stabilization['dependency_baseline_stable']}")
        print(f"Python Baseline Expected  : {stabilization['python_package_baseline_expected_installed']}/{stabilization['python_package_baseline_expected_total']}")
        print(f"Executable Baseline       : {stabilization['executable_baseline_expected_found']}/{stabilization['executable_baseline_expected_total']}")
        print(f"Safe Idle Stable          : {stabilization['safe_idle_default_stable']}")
        print(f"Push To Talk Stable       : {stabilization['push_to_talk_required_stable']}")
        print(f"Explicit Listen Stable    : {stabilization['explicit_listen_required_stable']}")
        print(f"Default Listen State      : {stabilization['default_listen_state_stable']}")
        print(f"Current Listen State      : {stabilization['current_listen_state_stable']}")
        print(f"Allowed Listen States     : {stabilization['allowed_listen_state_count_stable']}")
        print(f"Mic Permission Action     : {stabilization['microphone_permission_action_stable']}")
        print(f"Speaker Permission Action : {stabilization['speaker_permission_action_stable']}")
        print(f"Control Center Route      : {stabilization['control_center_voice_route_stable']}")
        print(f"Control Center Panel ID   : {stabilization['control_center_voice_panel_id_stable']}")
        print(f"Control Center Read Only  : {stabilization['control_center_voice_read_only_stable']}")
        print(f"Control Center Disabled   : {stabilization['control_center_voice_disabled_by_default_stable']}")
        print(f"Disabled Control Count    : {stabilization['disabled_voice_control_count_stable']}")
        print(f"Safety Blocker Count      : {stabilization['safety_blocker_count']}")
        print(f"All Safety Blockers Off   : {stabilization['all_safety_blockers_inactive']}")
        print(f"Stabilization Gap Count   : {stabilization['stabilization_gap_count']}")
        print(f"Stabilization Passed      : {stabilization['stabilization_passed']}")
        print(f"Voice Block Complete      : {stabilization['voice_runtime_block_191_200_complete']}")
        print(f"Runtime Activation Allowed: {stabilization['runtime_activation_allowed']}")
        print(f"Runtime Ready             : {stabilization['runtime_ready']}")
        print(f"Release Gate Open         : {stabilization['release_gate_open']}")
        print(f"V1 Activation Allowed     : {stabilization['v1_runtime_activation_allowed']}")
        print(f"Background Service Allowed: {stabilization['background_service_activation_allowed']}")
        print(f"Systemd Activation Allowed: {stabilization['systemd_activation_allowed']}")
        print(f"Public LAN Binding Allowed: {stabilization['public_lan_binding_allowed']}")
        print(f"Browser Auto Launch       : {stabilization['browser_auto_launch_allowed']}")
        print(f"Autonomy Allowed          : {stabilization['autonomy_allowed']}")
        print(f"Microphone Capture Active : {stabilization['microphone_capture_active']}")
        print(f"STT Runtime Active        : {stabilization['stt_runtime_active']}")
        print(f"TTS Runtime Active        : {stabilization['tts_runtime_active']}")
        print(f"Speaker Playback Active   : {stabilization['speaker_playback_active']}")
        print(f"Permission Grant Runtime  : {stabilization['permission_grant_runtime_active']}")
        print(f"Permission Mutation Active: {stabilization['permission_mutation_active']}")
        print(f"Audit Write Runtime       : {stabilization['audit_write_runtime_active']}")
        print(f"UI Mic Capture Trigger    : {stabilization['ui_microphone_capture_trigger_active']}")
        print(f"UI STT Trigger            : {stabilization['ui_stt_trigger_active']}")
        print(f"UI TTS Trigger            : {stabilization['ui_tts_trigger_active']}")
        print(f"UI Speaker Trigger        : {stabilization['ui_speaker_playback_trigger_active']}")
        print(f"UI Permission Grant       : {stabilization['ui_permission_grant_trigger_active']}")
        print(f"UI Audit Write            : {stabilization['ui_audit_write_trigger_active']}")
        print(f"UI Voice Action           : {stabilization['ui_voice_action_trigger_active']}")
        print(f"Memory Write Active       : {stabilization['memory_write_active']}")
        print(f"Direct Voice To Action    : {stabilization['direct_voice_to_action_enabled']}")
        print(f"Tool Execution Active     : {stabilization['tool_execution_active']}")
        print(f"Command Execution Active  : {stabilization['command_execution_active']}")
        print(f"File Mutation Active      : {stabilization['file_mutation_active']}")
        print(f"Desktop Action Active     : {stabilization['desktop_action_active']}")
        print(f"Network Action Active     : {stabilization['network_action_active']}")
        print(f"Git Action Active         : {stabilization['git_action_active']}")
        print(f"Cloud STT Fallback        : {stabilization['cloud_stt_fallback_enabled']}")
        print(f"Cloud TTS Fallback        : {stabilization['cloud_tts_fallback_enabled']}")
        print(f"Silent Cloud Fallback     : {stabilization['silent_cloud_fallback_enabled']}")
        print(f"Runtime Scope             : {stabilization['runtime_scope']}")
        print(f"Next Sprint               : {stabilization['next_sprint']}")
        print(f"Next Boundary             : {stabilization['next_boundary']}")
        print()
        print("Voice Stabilized Contracts")
        print("--------------------------")
        for contract in stabilization["stabilized_contracts"]:
            print(f"- {contract}")
        print()
        print("Voice Stabilization Components")
        print("------------------------------")
        for component in stabilization["stabilization_components"]:
            print(f"- {component}")
        print()
        print("Voice Stabilization Gaps")
        print("------------------------")
        if stabilization["stabilization_gaps"]:
            for gap in stabilization["stabilization_gaps"]:
                print(f"- {gap}")
        else:
            print("- none")
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

    def plugins(self) -> None:
        self.ensure_plugins_loaded()

        plugins = self.plugin_manager.list_plugins()

        print("AURA Plugins")
        print("============")

        if not plugins:
            print("No plugins loaded.")
            return

        for plugin in plugins:
            print(
                f"{plugin['name']:<10}: {plugin['status']} "
                f"v{plugin['version']} - {plugin['description']}"
            )

    def health(self) -> None:
        self.ensure_plugins_loaded()

        plugins = self.plugin_manager.list_plugins()
        plugin_count = len(plugins)
        memory_count = self.memory_store.count()
        provider = self.chat_engine.provider_info()

        config_status = "OK" if self.settings_path.exists() else "ERROR"
        identity_status = "OK" if self.identity_path.exists() else "ERROR"

        print("AURA Shell Health")
        print("=================")
        print("Shell     : OK - Interactive shell online")
        print(f"Config    : {config_status} - settings.yaml")
        print(f"Identity  : {identity_status} - identity.yaml")
        print("Memory    : OK - File-based memory store online")
        print(f"Reasoning : OK - {provider['name']} v{provider['version']}")
        print("Chat      : OK - Chat interface online")
        print(f"Records   : OK - {memory_count} memory record(s)")
        print(f"Plugins   : OK - {plugin_count} plugin(s) loaded")

    def clear(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")

    def exit_shell(self) -> None:
        print("Goodbye, Kiput.")
        self.running = False


    # Sprint 65.1 codebase compatibility shell helpers.
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

    def handle_codebase_compat_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general codebase change"
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


    # Sprint 66.0 voice conversation compatibility shell helpers.
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

    def handle_voice_conversation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general voice conversation"
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


    # Sprint 67.0 vision context compatibility shell helpers.
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

    def handle_vision_context_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general vision context"
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


    # Sprint 68.0 avatar interaction compatibility shell helpers.
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

    def handle_avatar_interaction_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general avatar interaction"
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


    # Sprint 69.0 desktop workflow compatibility shell helpers.
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

    def handle_desktop_workflow_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general desktop workflow"
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


    # Sprint 70.0 partner runtime compatibility shell helpers.
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

    def handle_partner_runtime_shell_command(self, normalized: str) -> bool:
        # Sprint 235 Genesis Release Candidate Approval shell commands.
        sprint_235_commands = {
            "partner-runtime-genesis-release-candidate-approval-status",
            "partner-runtime-genesis-release-candidate-approval-context",
            "partner-runtime-genesis-release-candidate-approval-check",
        }

        if normalized in sprint_235_commands:
            from aura.partner_runtime import (
                GenesisReleaseCandidateApprovalAlphaManager,
            )

            manager = GenesisReleaseCandidateApprovalAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Genesis Release Candidate Approval Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Genesis Release Candidate Approval Context"
                packet = manager.context()
            else:
                title = "Genesis Release Candidate Approval Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 234 Genesis Release Candidate Readiness shell commands.
        sprint_234_commands = {
            "partner-runtime-genesis-release-candidate-readiness-status",
            "partner-runtime-genesis-release-candidate-readiness-context",
            "partner-runtime-genesis-release-candidate-readiness-check",
        }

        if normalized in sprint_234_commands:
            from aura.partner_runtime import (
                GenesisReleaseCandidateReadinessAlphaManager,
            )

            manager = GenesisReleaseCandidateReadinessAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Genesis Release Candidate Readiness Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Genesis Release Candidate Readiness Context"
                packet = manager.context()
            else:
                title = "Genesis Release Candidate Readiness Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 233 Genesis Release Candidate Verification shell commands.
        sprint_233_commands = {
            "partner-runtime-genesis-release-candidate-verification-status",
            "partner-runtime-genesis-release-candidate-verification-context",
            "partner-runtime-genesis-release-candidate-verification-check",
        }

        if normalized in sprint_233_commands:
            from aura.partner_runtime import (
                GenesisReleaseCandidateVerificationAlphaManager,
            )

            manager = GenesisReleaseCandidateVerificationAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Genesis Release Candidate Verification Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Genesis Release Candidate Verification Context"
                packet = manager.context()
            else:
                title = "Genesis Release Candidate Verification Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 232 Genesis Release Candidate Assembly shell commands.
        sprint_232_commands = {
            "partner-runtime-genesis-release-candidate-assembly-status",
            "partner-runtime-genesis-release-candidate-assembly-context",
            "partner-runtime-genesis-release-candidate-assembly-check",
        }

        if normalized in sprint_232_commands:
            from aura.partner_runtime import (
                GenesisReleaseCandidateAssemblyAlphaManager,
            )

            manager = GenesisReleaseCandidateAssemblyAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Genesis Release Candidate Assembly Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Genesis Release Candidate Assembly Context"
                packet = manager.context()
            else:
                title = "Genesis Release Candidate Assembly Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 231 Genesis Final Integration and Release shell commands.
        sprint_231_commands = {
            "partner-runtime-genesis-final-integration-and-release-status",
            "partner-runtime-genesis-final-integration-and-release-context",
            "partner-runtime-genesis-final-integration-and-release-check",
        }

        if normalized in sprint_231_commands:
            from aura.partner_runtime import (
                GenesisFinalIntegrationAndReleaseAlphaManager,
            )

            manager = GenesisFinalIntegrationAndReleaseAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Genesis Final Integration and Release Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Genesis Final Integration and Release Context"
                packet = manager.context()
            else:
                title = "Genesis Final Integration and Release Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 230 Unified Partner Runtime Stabilization shell commands.
        sprint_230_commands = {
            "partner-runtime-unified-partner-runtime-stabilization-status",
            "partner-runtime-unified-partner-runtime-stabilization-context",
            "partner-runtime-unified-partner-runtime-stabilization-check",
        }

        if normalized in sprint_230_commands:
            from aura.partner_runtime import (
                UnifiedPartnerRuntimeStabilizationAlphaManager,
            )

            manager = UnifiedPartnerRuntimeStabilizationAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = "Unified Partner Runtime Stabilization Status"
                packet = manager.status()
            elif normalized.endswith("-context"):
                title = "Unified Partner Runtime Stabilization Context"
                packet = manager.context()
            else:
                title = "Unified Partner Runtime Stabilization Check"
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )
            return True

        # Sprint 229 Genesis Acceptance Rehearsal shell commands.
        commands = {
            "partner-runtime-genesis-acceptance-rehearsal-status",
            "partner-runtime-genesis-acceptance-rehearsal-context",
            "partner-runtime-genesis-acceptance-rehearsal-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                GenesisAcceptanceRehearsalAlphaManager,
            )

            manager = GenesisAcceptanceRehearsalAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Genesis Acceptance Rehearsal "
                    "Contract Status"
                )
                packet = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Genesis Acceptance Rehearsal "
                    "Contract Context"
                )
                packet = manager.context()

            else:
                title = (
                    "AURA Genesis Acceptance Rehearsal "
                    "Contract Check"
                )
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )

            return True

        # Sprint 228 Safe Auto-Start Evaluation shell commands.
        commands = {
            "partner-runtime-safe-auto-start-evaluation-status",
            "partner-runtime-safe-auto-start-evaluation-context",
            "partner-runtime-safe-auto-start-evaluation-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                SafeAutoStartEvaluationAlphaManager,
            )

            manager = SafeAutoStartEvaluationAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Safe Auto-Start Evaluation "
                    "Contract Status"
                )
                packet = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Safe Auto-Start Evaluation "
                    "Contract Context"
                )
                packet = manager.context()

            else:
                title = (
                    "AURA Safe Auto-Start Evaluation "
                    "Contract Check"
                )
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )

            return True

        # Sprint 227 Service Persistence and Launcher shell commands.
        commands = {
            "partner-runtime-service-persistence-launcher-status",
            "partner-runtime-service-persistence-launcher-context",
            "partner-runtime-service-persistence-launcher-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                ServicePersistenceAndLauncherAlphaManager,
            )

            manager = ServicePersistenceAndLauncherAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Service Persistence and "
                    "Launcher Contract Status"
                )
                packet = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Service Persistence and "
                    "Launcher Contract Context"
                )
                packet = manager.context()

            else:
                title = (
                    "AURA Service Persistence and "
                    "Launcher Contract Check"
                )
                packet = manager.check()

            self.print_partner_runtime_packet(
                title,
                packet,
            )

            return True

        # Sprint 226 Multi-Interface State Synchronization shell commands.
        commands = {
            "partner-runtime-multi-interface-state-synchronization-status",
            "partner-runtime-multi-interface-state-synchronization-context",
            "partner-runtime-multi-interface-state-synchronization-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                MultiInterfaceStateSynchronizationAlphaManager,
            )

            manager = MultiInterfaceStateSynchronizationAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Multi-Interface State "
                    "Synchronization Contract Status"
                )
                payload = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Multi-Interface State "
                    "Synchronization Contract Context"
                )
                payload = manager.context()

            else:
                title = (
                    "AURA Multi-Interface State "
                    "Synchronization Contract Check"
                )
                payload = manager.check()

            self.print_partner_runtime_packet(
                title,
                payload,
            )

            return True

        # Sprint 225 Personality Consistency Runtime shell commands.
        commands = {
            "partner-runtime-personality-consistency-status",
            "partner-runtime-personality-consistency-context",
            "partner-runtime-personality-consistency-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                PersonalityConsistencyRuntimeAlphaManager,
            )

            manager = PersonalityConsistencyRuntimeAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Personality Consistency "
                    "Runtime Contract Status"
                )
                payload = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Personality Consistency "
                    "Runtime Contract Context"
                )
                payload = manager.context()

            else:
                title = (
                    "AURA Personality Consistency "
                    "Runtime Contract Check"
                )
                payload = manager.check()

            self.print_partner_runtime_packet(
                title,
                payload,
            )

            return True

        # Sprint 224 Voice, Vision, and Chat Context Fusion shell commands.
        commands = {
            "partner-runtime-voice-vision-chat-context-fusion-status",
            "partner-runtime-voice-vision-chat-context-fusion-context",
            "partner-runtime-voice-vision-chat-context-fusion-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                VoiceVisionChatContextFusionAlphaManager,
            )

            manager = VoiceVisionChatContextFusionAlphaManager(
                project_root=self.project_root,
            )

            if normalized.endswith("-status"):
                title = (
                    "AURA Voice, Vision, and Chat "
                    "Context Fusion Contract Status"
                )
                payload = manager.status()

            elif normalized.endswith("-context"):
                title = (
                    "AURA Voice, Vision, and Chat "
                    "Context Fusion Contract Context"
                )
                payload = manager.context()

            else:
                title = (
                    "AURA Voice, Vision, and Chat "
                    "Context Fusion Contract Check"
                )
                payload = manager.check()

            self.print_partner_runtime_packet(
                title,
                payload,
            )

            return True

        # Sprint 222 Workspace and Project Context Runtime shell commands.
        # Sprint 223 Chat-to-Memory Runtime Handoff shell commands.
        commands = {
            "partner-runtime-chat-to-memory-handoff-status",
            "partner-runtime-chat-to-memory-handoff-context",
            "partner-runtime-chat-to-memory-handoff-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                ChatToMemoryRuntimeHandoffAlphaManager,
            )

            manager = ChatToMemoryRuntimeHandoffAlphaManager(
                project_root=self.project_root,
            )

            selected_command = normalized

            if selected_command.endswith("-status"):
                title = (
                    "AURA Chat-to-Memory Runtime "
                    "Handoff Contract Status"
                )
                payload = manager.status()

            elif selected_command.endswith("-context"):
                title = (
                    "AURA Chat-to-Memory Runtime "
                    "Handoff Contract Context"
                )
                payload = manager.context()

            else:
                title = (
                    "AURA Chat-to-Memory Runtime "
                    "Handoff Contract Check"
                )
                payload = manager.check()

            self.print_partner_runtime_packet(
                title,
                payload,
            )

            return True
        commands = {
            "partner-runtime-workspace-project-context-status",
            "partner-runtime-workspace-project-context-context",
            "partner-runtime-workspace-project-context-check",
        }

        if normalized in commands:
            from aura.partner_runtime import (
                WorkspaceProjectContextAlphaManager,
            )

            manager = WorkspaceProjectContextAlphaManager(
                project_root=self.project_root,
            )

            selected_command = normalized

            print(
                "AURA Workspace and Project Context "
                "Runtime Contract"
            )
            print(
                "=" * 52
            )

            if selected_command.endswith("-status"):
                payload = manager.status()

                print(
                    f"Status            : "
                    f"{payload['status']}"
                )
                print(
                    f"Contract Ready    : "
                    f"{payload['workspace_project_context_contract_ready']}"
                )
                print(
                    f"Planning Ready    : "
                    f"{payload['planning_ready']}"
                )
                print(
                    f"Current Sprint    : "
                    f"{payload['partner_runtime_current_sprint']}"
                )
                print(
                    f"Next Sprint       : "
                    f"{payload['partner_runtime_next_sprint']}"
                )
                print(
                    f"Next Boundary     : "
                    f"{payload['partner_runtime_next_boundary']}"
                )
                print(
                    f"Session Owner     : "
                    f"{payload['canonical_session_owner']}"
                )
                print(
                    f"Runtime Ready     : "
                    f"{payload['runtime_ready']}"
                )
                print(
                    f"Assertion Count   : "
                    f"{payload['assertion_count']}"
                )
                print(
                    f"Failed Assertions : "
                    f"{payload['failed_assertion_count']}"
                )

            elif selected_command.endswith("-context"):
                payload = manager.context()

                identity = payload["identity_snapshot"]
                git = payload["git_snapshot"]
                workspace = payload["workspace_snapshot"]
                sources = payload[
                    "context_source_snapshot"
                ]
                legacy = payload[
                    "legacy_workspace_snapshot"
                ]

                print(
                    f"Current Sprint     : "
                    f"{payload['current_sprint']}"
                )
                print(
                    f"Next Sprint        : "
                    f"{payload['next_sprint']}"
                )
                print(
                    f"Next Boundary      : "
                    f"{payload['next_boundary']}"
                )
                print(
                    f"Identity Version   : "
                    f"{identity['version']}"
                )
                print(
                    f"Git Branch         : "
                    f"{git['branch']}"
                )
                print(
                    f"Workspace Dirs     : "
                    f"{len(workspace['directories'])}"
                )
                print(
                    f"Workspace Files    : "
                    f"{len(workspace['files'])}"
                )
                print(
                    f"Context Sources OK : "
                    f"{sources['all_available']}"
                )
                print(
                    f"Legacy Constructed : "
                    f"{legacy['constructor_called']}"
                )
                print(
                    f"Journal Accessed   : "
                    f"{legacy['journal_accessed']}"
                )
                print(
                    f"Memory Accessed    : "
                    f"{legacy['memory_accessed']}"
                )
                print(
                    f"Contract Only      : "
                    f"{payload['contract_only']}"
                )
                print(
                    f"Runtime Ready      : "
                    f"{payload['runtime_ready']}"
                )

            else:
                payload = manager.check()

                print(
                    f"Status            : "
                    f"{payload['status']}"
                )
                print(
                    f"Planning Ready    : "
                    f"{payload['planning_ready']}"
                )
                print(
                    f"Assertion Count   : "
                    f"{payload['assertion_count']}"
                )
                print(
                    f"Failed Assertions : "
                    f"{payload['failed_assertion_count']}"
                )
                print(
                    f"Runtime Ready     : "
                    f"{payload['runtime_ready']}"
                )

            return True
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general partner runtime planning"

        if command == "partner-runtime-unified-session-status":
            manager = PartnerRuntimeAlphaManager(project_root=self.project_root)
            self.print_partner_runtime_packet(
                "AURA Unified Session Runtime Contract Status",
                manager.status(),
            )
            return True

        if command == "partner-runtime-unified-session-context":
            manager = PartnerRuntimeAlphaManager(project_root=self.project_root)
            self.print_partner_runtime_packet(
                "AURA Unified Session Runtime Contract Context",
                manager.context(),
            )
            return True

        if command == "partner-runtime-unified-session-check":
            manager = PartnerRuntimeAlphaManager(project_root=self.project_root)
            self.print_partner_runtime_packet(
                "AURA Unified Session Runtime Contract Check",
                manager.check(),
            )
            return True

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


    # Sprint 71.0 thought loop compatibility shell helpers.
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

    def handle_thought_loop_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general thought loop planning"
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


    # Sprint 72.0 reasoning context compatibility shell helpers.
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

    def handle_reasoning_context_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general reasoning context"
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


    # Sprint 73.0 knowledge uncertainty compatibility shell helpers.
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

    def handle_knowledge_uncertainty_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general knowledge uncertainty gate"
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


    # Sprint 74.0 voice input compatibility shell helpers.
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

    def handle_voice_input_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general voice input foundation"
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


    # Sprint 75.0 voice intent compatibility shell helpers.
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

    def handle_voice_intent_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general voice intent understanding"
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


    # Sprint 76.0 vision input compatibility shell helpers.
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

    def handle_vision_input_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general vision input foundation"
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


    # Sprint 77.0 visual context compatibility shell helpers.
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

    def handle_visual_context_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general visual context understanding"
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


    # Sprint 78.0 coder project compatibility shell helpers.
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

    def handle_coder_project_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general coder project generation"
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


    # Sprint 79.0 dependency permission compatibility shell helpers.
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

    def handle_dependency_permission_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "general dependency download permission"
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


    # Sprint 80.0 checkpoint compatibility shell helpers.
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

    def handle_checkpoint_80_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "Sprint 71-80 checkpoint review"
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


    # Sprint 81.0 shared output formatter shell helpers.
    def print_output_formatter_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet))

    def handle_output_formatter_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "shared AURA output formatting"
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


    # Sprint 82.0 capability registry shell helpers.
    def print_capability_registry_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Capability Registry Safety Boundary"))

    def handle_capability_registry_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA capability registry"
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


    # Sprint 83.0 unified permission workflow shell helpers.
    def print_permission_workflow_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Workflow Safety Boundary"))

    def handle_permission_workflow_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA permission workflow"
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


    # Sprint 84.0 runtime service foundation shell helpers.
    def print_runtime_service_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Service Safety Boundary"))

    def handle_runtime_service_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime service foundation"
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


    # Sprint 85.0 launcher health monitor foundation shell helpers.
    def print_launcher_monitor_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Launcher Monitor Safety Boundary"))

    def handle_launcher_monitor_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA launcher and health monitor foundation"
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


    # Sprint 86.0 control center UI blueprint shell helpers.
    def print_control_center_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Safety Boundary"))

    def handle_control_center_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Control Center UI blueprint"
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


    # Sprint 87.0 local console web foundation shell helpers.
    def print_local_console_web_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console Web Safety Boundary"))

    def handle_local_console_web_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local console web foundation"
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


    # Sprint 88.0 chat bridge session state foundation shell helpers.
    def print_chat_bridge_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Bridge Safety Boundary"))

    def handle_chat_bridge_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA chat bridge and session state foundation"
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


    # Sprint 89.0 plugin permission dashboard foundation shell helpers.
    def print_plugin_permission_dashboard_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Plugin / Permission Dashboard Safety Boundary"))

    def handle_plugin_permission_dashboard_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA plugin permission dashboard foundation"
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





















































    # Sprint 142.0 local service safe idle boot boundary shell helpers.


    # Sprint 144.0 service configuration and port registry foundation shell helpers.
    def print_local_service_configuration_port_registry_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Configuration and Port Registry Foundation Safety Boundary"))

    def handle_local_service_configuration_port_registry_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service configuration and port registry foundation"
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




















    # Sprint 161.0 local chat runtime foundation shell helpers.
    def print_local_chat_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Chat Runtime Foundation Safety Boundary"))

    def handle_local_chat_runtime_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split()
        command = parts[0]
        target = " ".join(parts[1:]).strip() or "AURA local chat runtime foundation"
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
            "local-chat-permission-gated-model-request-plan": ("AURA Local Chat Permission-Gated Model Request Plan", AuraLocalChatPermissionGatedModelRequestManager(project_root=self.project_root).permission_gated_model_request_runtime_plan),
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


    # Sprint 160.0 control center runtime review stabilization 151-160 shell helpers.
    def print_control_center_runtime_review_stabilization_151_160_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Review Stabilization 151-160 Safety Boundary"))

    def handle_control_center_runtime_review_stabilization_151_160_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split()
        command = parts[0]
        target = " ".join(parts[1:]).strip() or "AURA control center runtime review stabilization 151-160"
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


    # Sprint 159.0 control center read-only route map foundation shell helpers.
    def print_control_center_read_only_route_map_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Read-Only Route Map Foundation Safety Boundary"))

    def handle_control_center_read_only_route_map_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split()
        command = parts[0]
        target = " ".join(parts[1:]).strip() or "AURA control center read-only route map foundation"
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


    # Sprint 158.0 control center action log panel foundation shell helpers.
    def print_control_center_action_log_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Action Log Panel Foundation Safety Boundary"))

    def handle_control_center_action_log_panel_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split()
        command = parts[0]
        target = " ".join(parts[1:]).strip() or "AURA control center action log panel foundation"
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


    # Sprint 157.0 control center service monitor panel foundation shell helpers.
    def print_control_center_service_monitor_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Service Monitor Panel Foundation Safety Boundary"))

    def handle_control_center_service_monitor_panel_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split()
        command = parts[0]
        target = " ".join(parts[1:]).strip() or "AURA control center service monitor panel foundation"
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


    # Sprint 156.0 control center audit panel foundation shell helpers.
    def print_control_center_audit_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Audit Panel Foundation Safety Boundary"))

    def handle_control_center_audit_panel_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterAuditPanelFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center audit panel foundation"

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


    # Sprint 155.0 control center permission panel foundation shell helpers.
    def print_control_center_permission_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Permission Panel Foundation Safety Boundary"))

    def handle_control_center_permission_panel_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterPermissionPanelFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center permission panel foundation"

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


    # Sprint 154.0 control center plugin panel foundation shell helpers.
    def print_control_center_plugin_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Plugin Panel Foundation Safety Boundary"))

    def handle_control_center_plugin_panel_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterPluginPanelFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center plugin panel foundation"

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


    # Sprint 153.0 control center capability viewer foundation shell helpers.
    def print_control_center_capability_viewer_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Capability Viewer Foundation Safety Boundary"))

    def handle_control_center_capability_viewer_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterCapabilityViewerFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center capability viewer foundation"

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


    # Sprint 152.0 control center read-only status panel foundation shell helpers.
    def print_control_center_read_only_status_panel_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Read-Only Status Panel Foundation Safety Boundary"))

    def handle_control_center_read_only_status_panel_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterReadOnlyStatusPanelFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center read-only status panel foundation"

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


    # Sprint 151.0 control center runtime foundation shell helpers.
    def print_control_center_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Foundation Safety Boundary"))

    def handle_control_center_runtime_foundation_shell_command(self, normalized: str) -> bool:
        manager = AuraControlCenterRuntimeFoundationManager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA control center runtime foundation"

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


    # Sprint 150.0 service review stabilization 141-150 shell helpers.
    def print_service_review_stabilization_141_150_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Review Stabilization 141-150 Safety Boundary"))

    def handle_service_review_stabilization_141_150_shell_command(self, normalized: str) -> bool:
        manager = AuraServiceReviewStabilization141150Manager(project_root=self.project_root)
        command = normalized.strip()
        target = "AURA service review stabilization 141-150"

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


    # Sprint 149.0 service security and localhost binding review shell helpers.
    def print_service_security_localhost_binding_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Security and Localhost Binding Review Safety Boundary"))

    def handle_service_security_localhost_binding_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service security and localhost binding review"
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


    # Sprint 148.0 service recovery and restart policy foundation shell helpers.
    def print_service_recovery_restart_policy_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Recovery and Restart Policy Foundation Safety Boundary"))

    def handle_service_recovery_restart_policy_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service recovery and restart policy foundation"
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


    # Sprint 147.0 service control command review foundation shell helpers.
    def print_service_control_command_review_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Control Command Review Foundation Safety Boundary"))

    def handle_service_control_command_review_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service control command review foundation"
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


    # Sprint 146.0 service audit link foundation shell helpers.
    def print_service_audit_link_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Audit Link Foundation Safety Boundary"))

    def handle_service_audit_link_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service audit link foundation"
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



    # Sprint 145.0 service permission gate runtime boundary shell helpers.
    def print_service_permission_gate_runtime_boundary_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Service Permission Gate Runtime Boundary Safety Boundary"))

    def handle_service_permission_gate_runtime_boundary_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA service permission gate runtime boundary"
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
    # Sprint 143.0 local service health endpoint foundation shell helpers.
    def print_local_service_health_endpoint_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Health Endpoint Foundation Safety Boundary"))

    def handle_local_service_health_endpoint_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local service health endpoint foundation"
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

    def handle_local_service_safe_idle_boot_boundary_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local service safe idle boot boundary"
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

    # Sprint 141.0 local service runtime foundation shell helpers.
    def print_local_service_runtime_foundation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Runtime Foundation Safety Boundary"))

    def handle_local_service_runtime_foundation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local service runtime foundation"
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

    # Sprint 140.0 review stabilization 131-140 shell helpers.
    def print_review_stabilization_131_140_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 131-140 Safety Boundary"))

    def handle_review_stabilization_131_140_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA review stabilization 131-140"
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

    # Sprint 139.0 audit runtime writer activation review shell helpers.
    def print_audit_runtime_writer_activation_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Audit Runtime Writer Activation Review Safety Boundary"))

    def handle_audit_runtime_writer_activation_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA audit runtime writer activation review"
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

    # Sprint 138.0 permission runtime grant gate review shell helpers.
    def print_permission_runtime_grant_gate_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Runtime Grant Gate Review Safety Boundary"))

    def handle_permission_runtime_grant_gate_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA permission runtime grant gate review"
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

    # Sprint 137.0 memory runtime write gate review shell helpers.
    def print_memory_runtime_write_gate_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Memory Runtime Write Gate Review Safety Boundary"))

    def handle_memory_runtime_write_gate_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA memory runtime write gate review"
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

    # Sprint 136.0 chat runtime minimal loop review shell helpers.
    def print_chat_runtime_minimal_loop_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Runtime Minimal Loop Review Safety Boundary"))

    def handle_chat_runtime_minimal_loop_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA chat runtime minimal loop review"
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

    # Sprint 135.0 control center runtime entry review shell helpers.
    def print_control_center_runtime_entry_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Runtime Entry Review Safety Boundary"))

    def handle_control_center_runtime_entry_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Control Center runtime entry review"
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

    # Sprint 134.0 local service boot plan review shell helpers.
    def print_local_service_boot_plan_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Boot Plan Review Safety Boundary"))

    def handle_local_service_boot_plan_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local service boot plan review"
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

    # Sprint 133.0 runtime activation path proposal review shell helpers.
    def print_runtime_activation_path_proposal_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Activation Path Proposal Review Safety Boundary"))

    def handle_runtime_activation_path_proposal_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime activation path proposal review"
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

    # Sprint 132.0 final genesis acceptance criteria shell helpers.
    def print_final_genesis_acceptance_criteria_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Final Genesis Acceptance Criteria Safety Boundary"))

    def handle_final_genesis_acceptance_criteria_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Final Genesis acceptance criteria"
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

    # Sprint 131.0 post-checkpoint 130 next block shell helpers.
    def print_post_checkpoint_130_next_block_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Post-Checkpoint 130 Next Block Safety Boundary"))

    def handle_post_checkpoint_130_next_block_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA post-checkpoint 130 next block"
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

    # Sprint 130.0 review stabilization 121-130 shell helpers.
    def print_review_stabilization_121_130_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 121-130 Safety Boundary"))

    def handle_review_stabilization_121_130_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA review stabilization 121-130 checkpoint"
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

    # Sprint 129.0 runtime activation blocker register boundary review shell helpers.
    def print_runtime_activation_blocker_register_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Activation Blocker Register Boundary Review Safety Boundary"))

    def handle_runtime_activation_blocker_register_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime activation blocker register boundary review"
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

    # Sprint 128.0 dashboard runtime readiness boundary review shell helpers.
    def print_dashboard_runtime_readiness_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Runtime Readiness Boundary Review Safety Boundary"))

    def handle_dashboard_runtime_readiness_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA dashboard runtime readiness boundary review"
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

    # Sprint 127.0 runtime recovery drill boundary review shell helpers.
    def print_runtime_recovery_drill_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Recovery Drill Boundary Review Safety Boundary"))

    def handle_runtime_recovery_drill_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime recovery drill boundary review"
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

    # Sprint 126.0 runtime grant expiry boundary review shell helpers.
    def print_runtime_grant_expiry_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Grant Expiry Boundary Review Safety Boundary"))

    def handle_runtime_grant_expiry_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime grant expiry boundary review"
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

    # Sprint 125.0 safe local action allowlist boundary review shell helpers.
    def print_safe_local_action_allowlist_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Action Allowlist Boundary Review Safety Boundary"))

    def handle_safe_local_action_allowlist_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA safe local action allowlist boundary review"
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

    # Sprint 124.0 ORION dry handshake boundary review shell helpers.
    def print_orion_dry_handshake_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="ORION Dry Handshake Boundary Review Safety Boundary"))

    def handle_orion_dry_handshake_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA ORION dry handshake boundary review"
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

    # Sprint 123.0 dashboard control center boundary review shell helpers.
    def print_dashboard_control_center_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Control Center Boundary Review Safety Boundary"))

    def handle_dashboard_control_center_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA dashboard control center boundary review"
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

    # Sprint 122.0 runtime permission audit writer boundary review shell helpers.
    def print_runtime_permission_audit_writer_boundary_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Permission Audit Writer Boundary Review Safety Boundary"))

    def handle_runtime_permission_audit_writer_boundary_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime permission audit writer boundary review"
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

    # Sprint 121.0 post-checkpoint 120 next block planning shell helpers.
    def print_post_checkpoint_120_next_block_planning_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Post-Checkpoint 120 Next Block Planning Safety Boundary"))

    def handle_post_checkpoint_120_next_block_planning_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA post-checkpoint 120 next block planning"
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

    # Sprint 120.0 review stabilization 111-120 shell helpers.
    def print_review_stabilization_111_120_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 111-120 Safety Boundary"))

    def handle_review_stabilization_111_120_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA review stabilization 111-120"
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

    # Sprint 119.0 v1 runtime readiness cutline review shell helpers.
    def print_v1_runtime_readiness_cutline_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="v1 Runtime Readiness Cutline Review Safety Boundary"))

    def handle_v1_runtime_readiness_cutline_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA v1 runtime readiness cutline review"
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

    # Sprint 118.0 manual approval decision flow review shell helpers.
    def print_manual_approval_decision_flow_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Manual Approval Decision Flow Review Safety Boundary"))

    def handle_manual_approval_decision_flow_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA manual approval decision flow review"
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

    # Sprint 117.0 runtime error rollback preview shell helpers.
    def print_runtime_error_rollback_preview_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Error and Rollback Preview Safety Boundary"))

    def handle_runtime_error_rollback_preview_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime error rollback preview"
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

    # Sprint 116.0 ORION client boundary contract shell helpers.
    def print_orion_client_boundary_contract_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="ORION Client Boundary Contract Safety Boundary"))

    def handle_orion_client_boundary_contract_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA ORION client boundary contract"
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

    # Sprint 115.0 safe local action contract review shell helpers.
    def print_safe_local_action_contract_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Action Contract Review Safety Boundary"))

    def handle_safe_local_action_contract_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA safe local action contract review"
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

    # Sprint 114.0 dashboard runtime readiness view model shell helpers.
    def print_dashboard_runtime_readiness_view_model_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard Runtime Readiness View Model Safety Boundary"))

    def handle_dashboard_runtime_readiness_view_model_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA dashboard runtime readiness view model"
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

    # Sprint 113.0 audit event review queue shell helpers.
    def print_audit_event_review_queue_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Audit Event Review Queue Safety Boundary"))

    def handle_audit_event_review_queue_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA audit event review queue"
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

    # Sprint 112.0 runtime permission flow consolidation shell helpers.
    def print_runtime_permission_flow_consolidation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Permission Flow Consolidation Safety Boundary"))

    def handle_runtime_permission_flow_consolidation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime permission flow consolidation"
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

    # Sprint 111.0 genesis runtime readiness next block planning shell helpers.
    def print_genesis_runtime_readiness_next_block_planning_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Genesis Runtime Readiness Next Block Planning Safety Boundary"))

    def handle_genesis_runtime_readiness_next_block_planning_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Sprint 111-120 next block planning"
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

    # Sprint 110.0 review stabilization 101-110 shell helpers.
    def print_review_stabilization_101_110_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Review Stabilization 101-110 Safety Boundary"))

    def handle_review_stabilization_101_110_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Sprint 101-110 review stabilization"
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

    # Sprint 109.0 runtime safety freeze manual approval barrier shell helpers.
    def print_runtime_safety_freeze_manual_approval_barrier_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Safety Freeze Manual Approval Barrier Safety Boundary"))

    def handle_runtime_safety_freeze_manual_approval_barrier_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime safety freeze manual approval barrier"
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

    # Sprint 108.0 runtime audit event packet preview shell helpers.
    def print_runtime_audit_event_packet_preview_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Audit Event Packet Preview Safety Boundary"))

    def handle_runtime_audit_event_packet_preview_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime audit event packet preview"
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

    # Sprint 107.0 local runtime execution gate dry-run shell helpers.
    def print_local_runtime_execution_gate_dry_run_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Runtime Execution Gate Dry-Run Safety Boundary"))

    def handle_local_runtime_execution_gate_dry_run_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local runtime execution gate dry-run"
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

    # Sprint 106.0 runtime action execution preview packet shell helpers.
    def print_runtime_action_execution_preview_packet_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Action Execution Preview Packet Safety Boundary"))

    def handle_runtime_action_execution_preview_packet_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime action execution preview packet"
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

    # Sprint 105.0 permission decision runtime dry-run shell helpers.
    def print_permission_decision_runtime_dry_run_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Decision Runtime Dry-Run Safety Boundary"))

    def handle_permission_decision_runtime_dry_run_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA permission decision runtime dry-run"
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

    # Sprint 104.0 dashboard API contract consolidation shell helpers.
    def print_dashboard_api_contract_consolidation_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Dashboard API Contract Consolidation Safety Boundary"))

    def handle_dashboard_api_contract_consolidation_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Dashboard API contract consolidation"
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

    # Sprint 103.0 local service start proposal review shell helpers.
    def print_local_service_start_proposal_review_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Service Start Proposal Review Safety Boundary"))

    def handle_local_service_start_proposal_review_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA local service start proposal review"
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

    # Sprint 102.0 safe runtime configuration profile foundation shell helpers.
    def print_safe_runtime_configuration_profile_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Runtime Configuration Profile Safety Boundary"))

    def handle_safe_runtime_configuration_profile_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA safe runtime configuration profile foundation"
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

    # Sprint 101.0 genesis runtime readiness baseline foundation shell helpers.
    def print_genesis_runtime_readiness_baseline_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Genesis Runtime Readiness Baseline Safety Boundary"))

    def handle_genesis_runtime_readiness_baseline_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Genesis runtime readiness baseline foundation"
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

    # Sprint 100.0 review and stabilization foundation shell helpers.
    def print_sprint_100_review_stabilization_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Sprint 100 Review Stabilization Safety Boundary"))

    def handle_sprint_100_review_stabilization_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Sprint 100 review stabilization foundation"
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

    # Sprint 99.0 pre-runtime security audit foundation shell helpers.
    def print_pre_runtime_security_audit_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Pre-Runtime Security Audit Safety Boundary"))

    def handle_pre_runtime_security_audit_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA pre-runtime security audit foundation"
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

    # Sprint 98.0 runtime action queue review layer foundation shell helpers.
    def print_runtime_action_queue_review_layer_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Runtime Action Queue Review Layer Safety Boundary"))

    def handle_runtime_action_queue_review_layer_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA runtime action queue review layer foundation"
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

    # Sprint 97.0 controlled file write approval draft foundation shell helpers.
    def print_controlled_file_write_approval_draft_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Controlled File Write Approval Draft Safety Boundary"))

    def handle_controlled_file_write_approval_draft_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA controlled file write approval draft foundation"
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

    # Sprint 96.0 safe local web runtime gate foundation shell helpers.
    def print_safe_local_web_runtime_gate_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Safe Local Web Runtime Gate Safety Boundary"))

    def handle_safe_local_web_runtime_gate_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA safe local web runtime gate foundation"
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

    # Sprint 95.0 chat session persistence planner foundation shell helpers.
    def print_chat_session_persistence_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Chat Session Persistence Safety Boundary"))

    def handle_chat_session_persistence_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA chat session persistence planner foundation"
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

    # Sprint 94.0 permission request review queue foundation shell helpers.
    def print_permission_request_review_queue_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Permission Request Review Queue Safety Boundary"))

    def handle_permission_request_review_queue_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA permission request review queue foundation"
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

    # Sprint 93.0 control center data aggregator foundation shell helpers.
    def print_control_center_data_aggregator_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Control Center Data Aggregator Safety Boundary"))

    def handle_control_center_data_aggregator_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Control Center data aggregator foundation"
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

    # Sprint 92.0 local console API schema foundation shell helpers.
    def print_local_console_api_schema_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console API Schema Safety Boundary"))

    def handle_local_console_api_schema_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Local Console API schema foundation"
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

    # Sprint 91.0 local console static prototype foundation shell helpers.
    def print_local_console_static_prototype_packet(self, title: str, packet: dict) -> None:
        formatter = SharedOutputFormatterManager()
        print(formatter.render_packet_text(title, packet, safety_title="Local Console Static Prototype Safety Boundary"))

    def handle_local_console_static_prototype_shell_command(self, normalized: str) -> bool:
        if not normalized:
            return False

        parts = normalized.split(maxsplit=1)
        command = parts[0]
        target = parts[1].strip() if len(parts) > 1 else "AURA Local Console static prototype foundation"
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

    def handle_command(self, raw_command: str) -> None:
        command = raw_command.strip()
        normalized = command.lower()

        if not command:
            return

        if self.handle_codebase_compat_shell_command(normalized):
            return

        if self.handle_voice_conversation_shell_command(normalized):
            return

        if self.handle_vision_context_shell_command(normalized):
            return

        if self.handle_avatar_interaction_shell_command(normalized):
            return

        if self.handle_desktop_workflow_shell_command(normalized):
            return

        if self.handle_partner_runtime_shell_command(normalized):
            return

        if self.handle_thought_loop_shell_command(normalized):
            return

        if self.handle_reasoning_context_shell_command(normalized):
            return

        if self.handle_knowledge_uncertainty_shell_command(normalized):
            return

        if self.handle_voice_input_shell_command(normalized):
            return

        if self.handle_voice_intent_shell_command(normalized):
            return

        if self.handle_vision_input_shell_command(normalized):
            return

        if self.handle_visual_context_shell_command(normalized):
            return

        if self.handle_coder_project_shell_command(normalized):
            return

        if self.handle_dependency_permission_shell_command(normalized):
            return

        if self.handle_checkpoint_80_shell_command(normalized):
            return

        if self.handle_output_formatter_shell_command(normalized):
            return

        if self.handle_capability_registry_shell_command(normalized):
            return

        if self.handle_permission_workflow_shell_command(normalized):
            return

        if self.handle_runtime_service_shell_command(normalized):
            return

        if self.handle_launcher_monitor_shell_command(normalized):
            return

        if self.handle_control_center_shell_command(normalized):
            return

        if self.handle_local_console_web_shell_command(normalized):
            return

        if self.handle_chat_bridge_shell_command(normalized):
            return

        if self.handle_plugin_permission_dashboard_shell_command(normalized):
            return

        if self.handle_local_console_static_prototype_shell_command(normalized):
            return

        if self.handle_local_console_api_schema_shell_command(normalized):
            return

        if self.handle_control_center_data_aggregator_shell_command(normalized):
            return

        if self.handle_permission_request_review_queue_shell_command(normalized):
            return

        if self.handle_chat_session_persistence_shell_command(normalized):
            return

        if self.handle_safe_local_web_runtime_gate_shell_command(normalized):
            return

        if self.handle_controlled_file_write_approval_draft_shell_command(normalized):
            return

        if self.handle_runtime_action_queue_review_layer_shell_command(normalized):
            return

        if self.handle_pre_runtime_security_audit_shell_command(normalized):
            return

        if self.handle_sprint_100_review_stabilization_shell_command(normalized):
            return

        if self.handle_genesis_runtime_readiness_baseline_shell_command(normalized):
            return

        if self.handle_safe_runtime_configuration_profile_shell_command(normalized):
            return

        if self.handle_local_service_start_proposal_review_shell_command(normalized):
            return

        if self.handle_dashboard_api_contract_consolidation_shell_command(normalized):
            return

        if self.handle_permission_decision_runtime_dry_run_shell_command(normalized):
            return

        if self.handle_runtime_action_execution_preview_packet_shell_command(normalized):
            return

        if self.handle_local_runtime_execution_gate_dry_run_shell_command(normalized):
            return

        if self.handle_runtime_audit_event_packet_preview_shell_command(normalized):
            return

        if self.handle_runtime_safety_freeze_manual_approval_barrier_shell_command(normalized):
            return

        if self.handle_review_stabilization_101_110_shell_command(normalized):
            return

        if self.handle_genesis_runtime_readiness_next_block_planning_shell_command(normalized):
            return

        if self.handle_runtime_permission_flow_consolidation_shell_command(normalized):
            return

        if self.handle_audit_event_review_queue_shell_command(normalized):
            return

        if self.handle_dashboard_runtime_readiness_view_model_shell_command(normalized):
            return

        if self.handle_safe_local_action_contract_review_shell_command(normalized):
            return

        if self.handle_orion_client_boundary_contract_shell_command(normalized):
            return

        if self.handle_runtime_error_rollback_preview_shell_command(normalized):
            return

        if self.handle_manual_approval_decision_flow_review_shell_command(normalized):
            return

        if self.handle_v1_runtime_readiness_cutline_review_shell_command(normalized):
            return

        if self.handle_review_stabilization_111_120_shell_command(normalized):
            return

        if self.handle_post_checkpoint_120_next_block_planning_shell_command(normalized):
            return

        if self.handle_runtime_permission_audit_writer_boundary_review_shell_command(normalized):
            return

        if self.handle_dashboard_control_center_boundary_review_shell_command(normalized):
            return

        if self.handle_orion_dry_handshake_boundary_review_shell_command(normalized):
            return

        if self.handle_safe_local_action_allowlist_boundary_review_shell_command(normalized):
            return

        if self.handle_runtime_grant_expiry_boundary_review_shell_command(normalized):
            return

        if self.handle_runtime_recovery_drill_boundary_review_shell_command(normalized):
            return

        if self.handle_dashboard_runtime_readiness_boundary_review_shell_command(normalized):
            return

        if self.handle_runtime_activation_blocker_register_boundary_review_shell_command(normalized):
            return

        if self.handle_review_stabilization_121_130_shell_command(normalized):
            return

        if self.handle_post_checkpoint_130_next_block_shell_command(normalized):
            return

        if self.handle_final_genesis_acceptance_criteria_shell_command(normalized):
            return

        if self.handle_runtime_activation_path_proposal_review_shell_command(normalized):
            return

        if self.handle_local_service_boot_plan_review_shell_command(normalized):
            return

        if self.handle_control_center_runtime_entry_review_shell_command(normalized):
            return

        if self.handle_chat_runtime_minimal_loop_review_shell_command(normalized):
            return

        if self.handle_memory_runtime_write_gate_review_shell_command(normalized):
            return

        if self.handle_permission_runtime_grant_gate_review_shell_command(normalized):
            return

        if self.handle_audit_runtime_writer_activation_review_shell_command(normalized):
            return

        if self.handle_review_stabilization_131_140_shell_command(normalized):
            return

        if self.handle_local_service_runtime_foundation_shell_command(normalized):
            return

        if self.handle_local_service_safe_idle_boot_boundary_shell_command(normalized):
            return

        if self.handle_local_service_health_endpoint_foundation_shell_command(normalized):
            return

        if self.handle_local_service_configuration_port_registry_foundation_shell_command(normalized):
            return

        if self.handle_service_permission_gate_runtime_boundary_shell_command(normalized):
            return

        if self.handle_service_audit_link_foundation_shell_command(normalized):
            return

        if self.handle_service_control_command_review_foundation_shell_command(normalized):
            return

        if self.handle_service_recovery_restart_policy_foundation_shell_command(normalized):
            return

        if self.handle_service_security_localhost_binding_review_shell_command(normalized):
            return

        if self.handle_service_review_stabilization_141_150_shell_command(normalized):
            return

        if self.handle_control_center_runtime_foundation_shell_command(normalized):
            return

        if self.handle_control_center_read_only_status_panel_foundation_shell_command(normalized):
            return

        if self.handle_local_chat_runtime_foundation_shell_command(normalized):
            return

        if self.handle_control_center_runtime_review_stabilization_151_160_shell_command(normalized):
            return

        if self.handle_control_center_read_only_route_map_foundation_shell_command(normalized):
            return

        if self.handle_control_center_action_log_panel_foundation_shell_command(normalized):
            return

        if self.handle_control_center_service_monitor_panel_foundation_shell_command(normalized):
            return

        if self.handle_control_center_audit_panel_foundation_shell_command(normalized):
            return

        if self.handle_control_center_permission_panel_foundation_shell_command(normalized):
            return

        if self.handle_control_center_plugin_panel_foundation_shell_command(normalized):
            return

        if self.handle_control_center_capability_viewer_foundation_shell_command(normalized):
            return

        if normalized == "help":
            self.print_help()
            return

        if normalized in {"exit", "quit", "q"}:
            self.exit_shell()
            return

        if normalized.startswith("memory-pin "):
            memory_id = command[len("memory-pin "):].strip()
            self.memory_pin(memory_id=memory_id)
            return

        if normalized.startswith("mem-pin "):
            memory_id = command[len("mem-pin "):].strip()
            self.memory_pin(memory_id=memory_id)
            return

        if normalized.startswith("memory-unpin "):
            memory_id = command[len("memory-unpin "):].strip()
            self.memory_unpin(memory_id=memory_id)
            return

        if normalized.startswith("mem-unpin "):
            memory_id = command[len("mem-unpin "):].strip()
            self.memory_unpin(memory_id=memory_id)
            return

        if normalized.startswith("memory-importance "):
            parts = command.split(maxsplit=2)
            if len(parts) != 3:
                print("Usage: memory-importance <id> <1-5>")
                return

            try:
                importance = int(parts[2])
            except ValueError:
                print("Usage: memory-importance <id> <1-5>")
                return

            self.memory_importance(memory_id=parts[1], importance=importance)
            return

        if normalized.startswith("mem-importance "):
            parts = command.split(maxsplit=2)
            if len(parts) != 3:
                print("Usage: mem-importance <id> <1-5>")
                return

            try:
                importance = int(parts[2])
            except ValueError:
                print("Usage: mem-importance <id> <1-5>")
                return

            self.memory_importance(memory_id=parts[1], importance=importance)
            return

        if normalized in {"memory-pinned", "mem-pinned"}:
            self.memory_pinned()
            return

        if normalized.startswith("memory-delete "):
            memory_id = command[len("memory-delete "):].strip()
            self.memory_delete(memory_id=memory_id)
            return

        if normalized.startswith("mem-delete "):
            memory_id = command[len("mem-delete "):].strip()
            self.memory_delete(memory_id=memory_id)
            return

        if normalized == "daily-briefing-status":
            self.daily_briefing_status()
            return

        if normalized == "daily-briefing":
            self.daily_briefing()
            return

        if normalized.startswith("daily-briefing "):
            value = command[len("daily-briefing "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing <limit>")
                return
            self.daily_briefing(limit=limit)
            return

        if normalized == "daily-briefing-compact":
            self.daily_briefing_compact()
            return

        if normalized.startswith("daily-briefing-compact "):
            value = command[len("daily-briefing-compact "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing-compact <limit>")
                return
            self.daily_briefing_compact(limit=limit)
            return

        if normalized == "daily-briefing-context":
            self.daily_briefing_context()
            return

        if normalized.startswith("daily-briefing-context "):
            value = command[len("daily-briefing-context "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: daily-briefing-context <limit>")
                return
            self.daily_briefing_context(limit=limit)
            return

        if normalized == "memory-reflection-status":
            self.memory_reflection_status()
            return

        if normalized == "memory-reflect":
            self.memory_reflect()
            return

        if normalized.startswith("memory-reflect "):
            value = command[len("memory-reflect "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-reflect <limit>")
                return
            self.memory_reflect(limit=limit)
            return

        if normalized == "memory-insights":
            self.memory_insights()
            return

        if normalized.startswith("memory-insights "):
            value = command[len("memory-insights "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-insights <limit>")
                return
            self.memory_insights(limit=limit)
            return

        if normalized == "memory-reflection-context":
            self.memory_reflection_context()
            return

        if normalized.startswith("memory-reflection-context "):
            value = command[len("memory-reflection-context "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: memory-reflection-context <limit>")
                return
            self.memory_reflection_context(limit=limit)
            return

        if normalized in {"memory-count", "mem-count"}:
            self.memory_count()
            return

        if normalized in {"memory-list", "mem-list"}:
            self.memory_list()
            return

        if normalized.startswith("memory-list "):
            raw_limit = normalized.removeprefix("memory-list ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid memory-list limit. Example: memory-list 10")
                return

            self.memory_list(limit=limit)
            return

        if normalized.startswith("mem-list "):
            raw_limit = normalized.removeprefix("mem-list ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid mem-list limit. Example: mem-list 10")
                return

            self.memory_list(limit=limit)
            return

        if normalized.startswith("memory-search "):
            query = command[len("memory-search "):].strip()
            self.memory_search(query=query)
            return

        if normalized.startswith("mem-search "):
            query = command[len("mem-search "):].strip()
            self.memory_search(query=query)
            return

        if normalized == "status":
            self.status()
            return

        if normalized == "version":
            self.version()
            return

        if normalized == "journal":
            self.journal()
            return

        if normalized.startswith("journal "):
            value = command[len("journal "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: journal <limit>")
                return

            self.journal(limit=limit)
            return

        if normalized.startswith("journal-add "):
            content = command[len("journal-add "):].strip()
            if not content:
                print("Usage: journal-add <text>")
                return

            self.journal_add(content=content)
            return

        if normalized == "journal-count":
            self.journal_count()
            return

        if normalized == "roles":
            self.roles()
            return

        if normalized.startswith("context "):
            message = command[len("context "):].strip()
            if not message:
                print("Usage: context <text>")
                return

            self.context(message=message)
            return

        if normalized.startswith("context-preview "):
            message = command[len("context-preview "):].strip()
            if not message:
                print("Usage: context-preview <text>")
                return

            self.context(message=message)
            return

        if normalized == "tool-sandbox-status":
            self.tool_sandbox_status()
            return

        if normalized == "tool-sandbox-policy":
            self.tool_sandbox_policy()
            return

        if normalized.startswith("tool-sandbox-check "):
            command_text = command[len("tool-sandbox-check "):].strip()

            if not command_text:
                print("Usage: tool-sandbox-check <command>")
                return

            self.tool_sandbox_check(command=command_text)
            return

        if normalized.startswith("tool-sandbox-dry-run "):
            command_text = command[len("tool-sandbox-dry-run "):].strip()

            if not command_text:
                print("Usage: tool-sandbox-dry-run <command>")
                return

            self.tool_sandbox_dry_run(command=command_text)
            return

        if normalized == "model-router-status":
            self.model_router_status()
            return

        if normalized == "model-router-routes":
            self.model_router_routes()
            return

        if normalized.startswith("model-router-select "):
            target = command[len("model-router-select "):].strip()

            if not target:
                print("Usage: model-router-select <target>")
                return

            self.model_router_select(target=target)
            return

        if normalized == "core-loop-status":
            self.core_loop_status()
            return

        if normalized.startswith("core-loop-run "):
            message = command[len("core-loop-run "):].strip()

            if not message:
                print("Usage: core-loop-run <text>")
                return

            self.core_loop_run(message=message)
            return

        if normalized.startswith("core-loop-trace "):
            message = command[len("core-loop-trace "):].strip()

            if not message:
                print("Usage: core-loop-trace <text>")
                return

            self.core_loop_trace(message=message)
            return

        if normalized == "avatar-runtime-alpha-status":
            self.avatar_runtime_alpha_status()
            return

        if normalized.startswith("avatar-expression-plan "):
            expression = command[len("avatar-expression-plan "):].strip()
            if not expression:
                print("Usage: avatar-expression-plan <expression>")
                return
            self.avatar_expression_plan(expression=expression)
            return

        if normalized == "avatar-expression-plan":
            print("Usage: avatar-expression-plan <expression>")
            return

        if normalized.startswith("avatar-gesture-plan "):
            gesture = command[len("avatar-gesture-plan "):].strip()
            if not gesture:
                print("Usage: avatar-gesture-plan <gesture>")
                return
            self.avatar_gesture_plan(gesture=gesture)
            return

        if normalized == "avatar-gesture-plan":
            print("Usage: avatar-gesture-plan <gesture>")
            return

        if normalized == "avatar-runtime-context":
            self.avatar_runtime_context()
            return

        if normalized == "avatar-status":
            self.avatar_status()
            return

        if normalized == "avatar-providers":
            self.avatar_providers()
            return

        if normalized == "avatar-state":
            self.avatar_state()
            return

        if normalized.startswith("avatar-expression "):
            expression = command[len("avatar-expression "):].strip()

            if not expression:
                print("Usage: avatar-expression <expression>")
                return

            self.avatar_expression(expression=expression)
            return

        if normalized.startswith("avatar-gesture "):
            gesture = command[len("avatar-gesture "):].strip()

            if not gesture:
                print("Usage: avatar-gesture <gesture>")
                return

            self.avatar_gesture(gesture=gesture)
            return

        if normalized == "desktop-alpha-status":
            self.desktop_alpha_status()
            return

        if normalized.startswith("desktop-action-plan "):
            rest = command[len("desktop-action-plan "):].strip()
            parts = rest.split(maxsplit=1)
            if len(parts) < 2:
                print("Usage: desktop-action-plan <action_type> <target>")
                return
            self.desktop_action_plan(action_type=parts[0], target=parts[1])
            return

        if normalized == "desktop-action-plan":
            print("Usage: desktop-action-plan <action_type> <target>")
            return

        if normalized.startswith("desktop-open-app-plan "):
            app_name = command[len("desktop-open-app-plan "):].strip()
            if not app_name:
                print("Usage: desktop-open-app-plan <app>")
                return
            self.desktop_open_app_plan(app_name=app_name)
            return

        if normalized == "desktop-open-app-plan":
            print("Usage: desktop-open-app-plan <app>")
            return

        if normalized.startswith("desktop-open-browser-plan "):
            url = command[len("desktop-open-browser-plan "):].strip()
            if not url:
                print("Usage: desktop-open-browser-plan <url>")
                return
            self.desktop_open_browser_plan(url=url)
            return

        if normalized == "desktop-open-browser-plan":
            print("Usage: desktop-open-browser-plan <url>")
            return

        if normalized.startswith("desktop-open-file-plan "):
            file_path = command[len("desktop-open-file-plan "):].strip()
            if not file_path:
                print("Usage: desktop-open-file-plan <path>")
                return
            self.desktop_open_file_plan(file_path=file_path)
            return

        if normalized == "desktop-open-file-plan":
            print("Usage: desktop-open-file-plan <path>")
            return

        if normalized == "desktop-workspace-context":
            self.desktop_workspace_context()
            return

        if normalized == "desktop-status":
            self.desktop_status()
            return

        if normalized == "desktop-capabilities":
            self.desktop_capabilities()
            return

        if normalized.startswith("desktop-action "):
            action = command[len("desktop-action "):].strip()

            if not action:
                print("Usage: desktop-action <action>")
                return

            self.desktop_action(action=action)
            return

        if normalized in {"system-status", "status-full"}:
            self.system_status()
            return

        if normalized == "vision-runtime-alpha-status":
            self.vision_runtime_alpha_status()
            return

        if normalized == "vision-screen-plan":
            self.vision_screen_plan()
            return

        if normalized == "vision-camera-plan":
            self.vision_camera_plan()
            return

        if normalized == "vision-runtime-context":
            self.vision_runtime_context()
            return

        if normalized == "vision-runtime-status":
            self.vision_runtime_status()
            return

        if normalized == "vision-runtime-plan":
            self.vision_runtime_plan()
            return

        if normalized == "vision-runtime-check":
            self.vision_runtime_check()
            return

        if normalized == "active-permission-runtime-alpha-status":
            self.active_permission_runtime_alpha_status()
            return

        if normalized == "active-permission-runtime-status":
            self.active_permission_runtime_status()
            return

        if normalized == "active-permission-runtime-check":
            self.active_permission_runtime_check()
            return

        if normalized == "vision-status":
            self.vision_status()
            return

        if normalized == "vision-providers":
            self.vision_providers()
            return

        if normalized == "safe-file-operation-status":
            self.safe_file_operation_status()
            return

        if normalized.startswith("safe-file-read-plan "):
            target = command[len("safe-file-read-plan "):].strip()
            if not target:
                print("Usage: safe-file-read-plan <target>")
                return
            self.safe_file_read_plan(target)
            return

        if normalized.startswith("safe-file-write-plan "):
            target = command[len("safe-file-write-plan "):].strip()
            if not target:
                print("Usage: safe-file-write-plan <target>")
                return
            self.safe_file_write_plan(target)
            return

        if normalized.startswith("safe-file-edit-plan "):
            target = command[len("safe-file-edit-plan "):].strip()
            if not target:
                print("Usage: safe-file-edit-plan <target>")
                return
            self.safe_file_edit_plan(target)
            return

        if normalized.startswith("safe-file-move-copy-delete-risk-review "):
            target = command[len("safe-file-move-copy-delete-risk-review "):].strip()
            if not target:
                print("Usage: safe-file-move-copy-delete-risk-review <target>")
                return
            self.safe_file_move_copy_delete_risk_review(target)
            return

        if normalized.startswith("safe-file-operation-checklist "):
            target = command[len("safe-file-operation-checklist "):].strip()
            if not target:
                print("Usage: safe-file-operation-checklist <target>")
                return
            self.safe_file_operation_checklist(target)
            return

        if normalized == "safe-file-operation-context":
            self.safe_file_operation_context()
            return

        if normalized == "local-task-planner-status":
            self.local_task_planner_status()
            return

        if normalized.startswith("local-task-intent-plan "):
            target = command[len("local-task-intent-plan "):].strip()
            if not target:
                print("Usage: local-task-intent-plan <target>")
                return
            self.local_task_intent_plan(target)
            return

        if normalized.startswith("local-task-breakdown-plan "):
            target = command[len("local-task-breakdown-plan "):].strip()
            if not target:
                print("Usage: local-task-breakdown-plan <target>")
                return
            self.local_task_breakdown_plan(target)
            return

        if normalized.startswith("local-task-risk-review "):
            target = command[len("local-task-risk-review "):].strip()
            if not target:
                print("Usage: local-task-risk-review <target>")
                return
            self.local_task_risk_review(target)
            return

        if normalized.startswith("local-task-execution-checklist "):
            target = command[len("local-task-execution-checklist "):].strip()
            if not target:
                print("Usage: local-task-execution-checklist <target>")
                return
            self.local_task_execution_checklist(target)
            return

        if normalized == "local-task-context":
            self.local_task_context()
            return

        if normalized == "creative-assistant-status":
            self.creative_assistant_status()
            return

        if normalized.startswith("creative-brief-plan "):
            target = command[len("creative-brief-plan "):].strip()
            if not target:
                print("Usage: creative-brief-plan <target>")
                return
            self.creative_brief_plan(target)
            return

        if normalized.startswith("creative-character-concept-plan "):
            target = command[len("creative-character-concept-plan "):].strip()
            if not target:
                print("Usage: creative-character-concept-plan <target>")
                return
            self.creative_character_concept_plan(target)
            return

        if normalized.startswith("creative-visual-asset-plan "):
            target = command[len("creative-visual-asset-plan "):].strip()
            if not target:
                print("Usage: creative-visual-asset-plan <target>")
                return
            self.creative_visual_asset_plan(target)
            return

        if normalized.startswith("creative-content-idea-plan "):
            target = command[len("creative-content-idea-plan "):].strip()
            if not target:
                print("Usage: creative-content-idea-plan <target>")
                return
            self.creative_content_idea_plan(target)
            return

        if normalized.startswith("creative-review-plan "):
            target = command[len("creative-review-plan "):].strip()
            if not target:
                print("Usage: creative-review-plan <target>")
                return
            self.creative_review_plan(target)
            return

        if normalized == "creative-context":
            self.creative_context()
            return

        if normalized == "project-intent-status":
            self.project_intent_status()
            return

        if normalized.startswith("project-intent-summary "):
            topic = command[len("project-intent-summary "):].strip()
            if not topic:
                print("Usage: project-intent-summary <topic>")
                return
            self.project_intent_summary(topic)
            return

        if normalized.startswith("project-goal-plan "):
            goal = command[len("project-goal-plan "):].strip()
            if not goal:
                print("Usage: project-goal-plan <goal>")
                return
            self.project_goal_plan(goal)
            return

        if normalized.startswith("sprint-intent-plan "):
            goal = command[len("sprint-intent-plan "):].strip()
            if not goal:
                print("Usage: sprint-intent-plan <goal>")
                return
            self.sprint_intent_plan(goal)
            return

        if normalized.startswith("project-next-action-candidates "):
            topic = command[len("project-next-action-candidates "):].strip()
            if not topic:
                print("Usage: project-next-action-candidates <topic>")
                return
            self.project_next_action_candidates(topic)
            return

        if normalized == "project-intent-context":
            self.project_intent_context()
            return

        if normalized == "workspace-memory-link-status":
            self.workspace_memory_link_status()
            return

        if normalized == "workspace-memory-summary":
            self.workspace_memory_summary()
            return

        if normalized.startswith("workspace-memory-candidates "):
            target = command[len("workspace-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-memory-candidates <target>")
                return
            self.workspace_memory_candidates(target)
            return

        if normalized.startswith("workspace-file-memory-candidates "):
            target = command[len("workspace-file-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-file-memory-candidates <target>")
                return
            self.workspace_file_memory_candidates(target)
            return

        if normalized.startswith("workspace-milestone-memory-candidates "):
            target = command[len("workspace-milestone-memory-candidates "):].strip()
            if not target:
                print("Usage: workspace-milestone-memory-candidates <target>")
                return
            self.workspace_milestone_memory_candidates(target)
            return

        if normalized == "workspace-memory-link-context":
            self.workspace_memory_link_context()
            return

        if normalized == "streaming-safety-status":
            self.streaming_safety_status()
            return

        if normalized.startswith("streaming-context-plan "):
            target = command[len("streaming-context-plan "):].strip()
            if not target:
                print("Usage: streaming-context-plan <target>")
                return
            self.streaming_context_plan(target)
            return

        if normalized.startswith("streaming-chat-safety-plan "):
            target = command[len("streaming-chat-safety-plan "):].strip()
            if not target:
                print("Usage: streaming-chat-safety-plan <target>")
                return
            self.streaming_chat_safety_plan(target)
            return

        if normalized.startswith("streaming-content-boundary-plan "):
            target = command[len("streaming-content-boundary-plan "):].strip()
            if not target:
                print("Usage: streaming-content-boundary-plan <target>")
                return
            self.streaming_content_boundary_plan(target)
            return

        if normalized.startswith("streaming-privacy-plan "):
            target = command[len("streaming-privacy-plan "):].strip()
            if not target:
                print("Usage: streaming-privacy-plan <target>")
                return
            self.streaming_privacy_plan(target)
            return

        if normalized.startswith("streaming-moderation-plan "):
            target = command[len("streaming-moderation-plan "):].strip()
            if not target:
                print("Usage: streaming-moderation-plan <target>")
                return
            self.streaming_moderation_plan(target)
            return

        if normalized == "streaming-safety-context":
            self.streaming_safety_context()
            return

        if normalized == "game-companion-status":
            self.game_companion_status()
            return

        if normalized.startswith("game-session-plan "):
            target = command[len("game-session-plan "):].strip()
            if not target:
                print("Usage: game-session-plan <target>")
                return
            self.game_session_plan(target)
            return

        if normalized.startswith("game-strategy-plan "):
            target = command[len("game-strategy-plan "):].strip()
            if not target:
                print("Usage: game-strategy-plan <target>")
                return
            self.game_strategy_plan(target)
            return

        if normalized.startswith("game-streaming-plan "):
            target = command[len("game-streaming-plan "):].strip()
            if not target:
                print("Usage: game-streaming-plan <target>")
                return
            self.game_streaming_plan(target)
            return

        if normalized.startswith("game-coaching-plan "):
            target = command[len("game-coaching-plan "):].strip()
            if not target:
                print("Usage: game-coaching-plan <target>")
                return
            self.game_coaching_plan(target)
            return

        if normalized == "game-context":
            self.game_context()
            return

        if normalized == "expression-language-status":
            self.expression_language_status()
            return

        if normalized == "expression-state":
            self.expression_state()
            return

        if normalized.startswith("expression-plan "):
            target = command[len("expression-plan "):].strip()
            if not target:
                print("Usage: expression-plan <text>")
                return
            self.expression_plan(target)
            return

        if normalized.startswith("expression-voice-hint "):
            target = command[len("expression-voice-hint "):].strip()
            if not target:
                print("Usage: expression-voice-hint <target>")
                return
            self.expression_voice_hint(target)
            return

        if normalized.startswith("expression-avatar-hint "):
            target = command[len("expression-avatar-hint "):].strip()
            if not target:
                print("Usage: expression-avatar-hint <target>")
                return
            self.expression_avatar_hint(target)
            return

        if normalized.startswith("expression-gesture-hint "):
            target = command[len("expression-gesture-hint "):].strip()
            if not target:
                print("Usage: expression-gesture-hint <target>")
                return
            self.expression_gesture_hint(target)
            return

        if normalized == "expression-context":
            self.expression_context()
            return

        if normalized == "media-understanding-status":
            self.media_understanding_status()
            return

        if normalized == "media-asset-summary":
            self.media_asset_summary()
            return

        if normalized.startswith("media-image-plan "):
            goal = command[len("media-image-plan "):].strip()
            if not goal:
                print("Usage: media-image-plan <goal>")
                return
            self.media_image_plan(goal)
            return

        if normalized.startswith("media-texture-reference-plan "):
            goal = command[len("media-texture-reference-plan "):].strip()
            if not goal:
                print("Usage: media-texture-reference-plan <goal>")
                return
            self.media_texture_reference_plan(goal)
            return

        if normalized.startswith("media-thumbnail-review-plan "):
            goal = command[len("media-thumbnail-review-plan "):].strip()
            if not goal:
                print("Usage: media-thumbnail-review-plan <goal>")
                return
            self.media_thumbnail_review_plan(goal)
            return

        if normalized.startswith("media-video-plan "):
            goal = command[len("media-video-plan "):].strip()
            if not goal:
                print("Usage: media-video-plan <goal>")
                return
            self.media_video_plan(goal)
            return

        if normalized == "media-context":
            self.media_context()
            return

        if normalized == "blender-bridge-status":
            self.blender_bridge_status()
            return

        if normalized.startswith("blender-scene-plan "):
            goal = command[len("blender-scene-plan "):].strip()
            if not goal:
                print("Usage: blender-scene-plan <goal>")
                return
            self.blender_scene_plan(goal)
            return

        if normalized.startswith("blender-asset-plan "):
            goal = command[len("blender-asset-plan "):].strip()
            if not goal:
                print("Usage: blender-asset-plan <goal>")
                return
            self.blender_asset_plan(goal)
            return

        if normalized.startswith("blender-texture-plan "):
            goal = command[len("blender-texture-plan "):].strip()
            if not goal:
                print("Usage: blender-texture-plan <goal>")
                return
            self.blender_texture_plan(goal)
            return

        if normalized.startswith("blender-rigging-plan "):
            goal = command[len("blender-rigging-plan "):].strip()
            if not goal:
                print("Usage: blender-rigging-plan <goal>")
                return
            self.blender_rigging_plan(goal)
            return

        if normalized.startswith("blender-animation-plan "):
            goal = command[len("blender-animation-plan "):].strip()
            if not goal:
                print("Usage: blender-animation-plan <goal>")
                return
            self.blender_animation_plan(goal)
            return

        if normalized == "blender-context":
            self.blender_context()
            return

        if normalized == "workspace-status":
            self.workspace_awareness_status()
            return

        if normalized == "workspace-awareness-status":
            self.workspace_awareness_status()
            return

        if normalized == "workspace-map":
            self.workspace_map()
            return

        if normalized == "workspace-context":
            self.workspace_context()
            return

        if normalized == "workspace-current-state":
            self.workspace_current_state()
            return

        if normalized == "workspace-important-files":
            self.workspace_important_files()
            return

        if normalized == "partner-alpha-status":
            self.partner_alpha_status()
            return

        if normalized == "partner-context":
            self.partner_context()
            return

        if normalized == "partner-readiness":
            self.partner_readiness()
            return

        if normalized == "partner-next-step":
            self.partner_next_step()
            return

        if normalized in {"awakening-status", "awaken"}:
            self.awakening_status()
            return

        if normalized == "voice-runtime-alpha-status":
            self.voice_runtime_alpha_status()
            return

        if normalized.startswith("voice-speak-plan "):
            value = command[len("voice-speak-plan "):].strip()
            if not value:
                print("Usage: voice-speak-plan <text>")
                return
            self.voice_speak_plan(text=value)
            return

        if normalized == "voice-speak-plan":
            print("Usage: voice-speak-plan <text>")
            return

        if normalized.startswith("voice-speak-test "):
            value = command[len("voice-speak-test "):].strip()
            if not value:
                print("Usage: voice-speak-test <text>")
                return
            self.voice_speak_test(text=value)
            return

        if normalized == "voice-speak-test":
            print("Usage: voice-speak-test <text>")
            return

        if normalized == "voice-runtime-context":
            self.voice_runtime_context()
            return

        if normalized == "voice-runtime-status":
            self.voice_runtime_status()
            return

        if normalized == "voice-runtime-plan":
            self.voice_runtime_plan()
            return

        if normalized == "voice-runtime-check":
            self.voice_runtime_check()
            return

        if normalized == "voice-status":
            self.voice_status()
            return

        if normalized == "voice-providers":
            self.voice_providers()
            return

        if normalized == "project-code-status":
            self.project_code_status()
            return

        if normalized == "project-code-map":
            self.project_code_map()
            return

        if normalized.startswith("project-code-map "):
            value = command[len("project-code-map "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: project-code-map <limit>")
                return
            self.project_code_map(limit=limit)
            return

        if normalized.startswith("project-code-inspect "):
            relative_path = command[len("project-code-inspect "):].strip()
            if not relative_path:
                print("Usage: project-code-inspect <path>")
                return
            self.project_code_inspect(relative_path=relative_path)
            return

        if normalized.startswith("project-code-plan "):
            request = command[len("project-code-plan "):].strip()
            if not request:
                print("Usage: project-code-plan <request>")
                return
            self.project_code_plan(request=request)
            return

        if normalized.startswith("project-code-safety "):
            command_text = command[len("project-code-safety "):].strip()
            if not command_text:
                print("Usage: project-code-safety <command>")
                return
            self.project_code_safety(command=command_text)
            return

        if normalized == "project-map":
            self.project_map()
            return

        if normalized.startswith("project-map "):
            value = command[len("project-map "):].strip()

            try:
                depth = int(value)
            except ValueError:
                print("Usage: project-map <depth>")
                return

            self.project_map(depth=depth)
            return

        if normalized.startswith("project-inspect "):
            relative_path = command[len("project-inspect "):].strip()

            if not relative_path:
                print("Usage: project-inspect <path>")
                return

            self.project_inspect(relative_path=relative_path)
            return

        if normalized.startswith("project-find "):
            keyword = command[len("project-find "):].strip()

            if not keyword:
                print("Usage: project-find <keyword>")
                return

            self.project_find(keyword=keyword)
            return

        if normalized == "project-summary":
            self.project_summary()
            return

        if normalized == "project-files":
            self.project_files()
            return

        if normalized.startswith("project-files "):
            value = command[len("project-files "):].strip()
            try:
                limit = int(value)
            except ValueError:
                print("Usage: project-files <limit>")
                return

            self.project_files(limit=limit)
            return

        if normalized.startswith("project-read "):
            relative_path = command[len("project-read "):].strip()
            if not relative_path:
                print("Usage: project-read <path>")
                return

            self.project_read(relative_path=relative_path)
            return

        if normalized.startswith("action-request-check "):
            action = command[len("action-request-check "):].strip()

            if not action:
                print("Usage: action-request-check <name>")
                return

            self.action_request(action=action)
            return

        if normalized.startswith("action-request "):
            action = command[len("action-request "):].strip()

            if not action:
                print("Usage: action-request <name>")
                return

            self.action_request(action=action)
            return

        if normalized == "plugin-actions":
            self.plugin_actions()
            return

        if normalized.startswith("plugin-action-check "):
            name = command[len("plugin-action-check "):].strip()
            if not name:
                print("Usage: plugin-action-check <name>")
                return

            self.plugin_action_check(name=name)
            return

        if normalized.startswith("plugin-action "):
            name = command[len("plugin-action "):].strip()
            if not name:
                print("Usage: plugin-action <name>")
                return

            self.plugin_action_detail(name=name)
            return

        if normalized == "skills":
            self.skills()
            return

        if normalized.startswith("skill-check "):
            name = command[len("skill-check "):].strip()
            if not name:
                print("Usage: skill-check <name>")
                return

            self.skill_check(name=name)
            return

        if normalized.startswith("skill "):
            name = command[len("skill "):].strip()
            if not name:
                print("Usage: skill <name>")
                return

            self.skill_detail(name=name)
            return

        if normalized == "permissions":
            self.permissions()
            return

        if normalized.startswith("permission-check "):
            action = command[len("permission-check "):].strip()
            if not action:
                print("Usage: permission-check <action>")
                return

            self.permission_check(action=action)
            return

        if normalized.startswith("perm-check "):
            action = command[len("perm-check "):].strip()
            if not action:
                print("Usage: perm-check <action>")
                return

            self.permission_check(action=action)
            return

        if normalized in {"provider", "reason"}:
            self.provider()
            return

        if normalized in {"provider-check", "reason-check", "provider check", "reason check"}:
            self.provider_check()
            return

        if normalized in {"plugins", "plugin"}:
            self.plugins()
            return

        if normalized == "health":
            self.health()
            return

        if normalized in {"clear", "cls"}:
            self.clear()
            return

        if normalized in {"recall", "mem", "memory"}:
            self.recall()
            return

        if normalized == "history":
            self.history()
            return

        if normalized.startswith("history "):
            raw_limit = normalized.removeprefix("history ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid history limit. Example: history 3")
                return

            self.history(limit=limit)
            return

        if normalized.startswith("recall "):
            raw_limit = normalized.removeprefix("recall ").strip()

            try:
                limit = int(raw_limit)
            except ValueError:
                print("Invalid recall limit. Example: recall 3")
                return

            self.recall(limit=limit)
            return

        if normalized.startswith("remember "):
            content = command[len("remember "):]
            self.remember(content)
            return

        if normalized.startswith("chat "):
            message = command[len("chat "):]
            self.chat(message)
            return

        if normalized.startswith("ask "):
            message = command[len("ask "):]
            self.chat(message)
            return

        suggestion = self.suggest_command(command)

        print(f"Unknown command: {command}")

        if suggestion:
            print(f"Did you mean: {suggestion}?")

        print("Type 'help' to see available commands.")

    def run(self) -> None:
        self.print_banner()

        while self.running:
            try:
                raw_command = input("AURA> ")
                self.handle_command(raw_command)
            except KeyboardInterrupt:
                print()
                print("Goodbye, Kiput.")
                break


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

    def project_code_map(self, limit: int = 20) -> None:
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
            for item in summary["functions"][:40]:
                print(f"- {item}")

        if summary["methods"]:
            print()
            print("Methods")
            print("-------")
            for item in summary["methods"][:50]:
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
        print(f"Status          : {result['status']}")
        print(f"Insight Count   : {result['insight_count']}")
        print(f"Write Performed : {result['write_performed']}")
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
        print(f"Status           : {context['status']}")
        print(f"Context Ready    : {context['context_ready']}")
        print(f"Memory Count     : {context['memory_count']}")
        print(f"Journal Count    : {context['journal_count']}")
        print(f"Milestones       : {len(context['milestones'])}")
        print(f"Memory Highlights: {len(context['memory_highlights'])}")
        print(f"Write Performed  : {context['write_performed']}")
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

        print("Latest Milestone")
        print("----------------")
        latest = briefing["latest_milestone"]
        if latest:
            print(f"{latest['title']}: {latest['content']}")
        else:
            print("-")

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
        print(f"Title             : {briefing['title']}")
        print(f"Status            : {briefing['status']}")
        print(f"Version           : {briefing['version']}")
        print(f"Write Performed   : {briefing['write_performed']}")
        print(f"Command Execution : {briefing['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(briefing["project_summary"])
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

    def daily_briefing_context(self, limit: int = 5) -> None:
        manager = DailyBriefingManager(project_root=self.project_root)
        context = manager.context(limit=limit)

        print("AURA Daily Project Briefing Context")
        print("===================================")
        print(f"Status           : {context['status']}")
        print(f"Context Ready    : {context['context_ready']}")
        print(f"Write Performed  : {context['write_performed']}")
        print(f"Command Execution: {context['command_execution_performed']}")
        print()
        print("Project Summary")
        print("---------------")
        print(context["project_summary"])
        print()
        print("Recent Milestones")
        print("-----------------")
        for item in context["recent_milestones"]:
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
        print(f"Status               : {plan['status']}")
        print(f"Text                 : {plan['text']}")
        print(f"Text Length          : {plan['text_length']}")
        print(f"Command Available    : {plan['command_available']}")
        print(f"TTS Backend          : {plan['tts_backend']['name'] or '-'}")
        print(f"TTS Backend Found    : {plan['tts_backend']['found']}")
        print(f"Proposed Command     : {plan['proposed_command'] or '-'}")
        print(f"Command Reason       : {plan['command_reason']}")
        print(f"Speaker Output       : {plan['speaker_output']}")
        print(f"Microphone Access    : {plan['microphone_access']}")
        print(f"Command Execution    : {plan['command_execution_performed']}")
        print(f"Playback Performed   : {plan['playback_performed']}")
        print(f"File Write Performed : {plan['file_write_performed']}")
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
        print(f"Render Backend Found         : {status['render_backend_found']}")
        print(f"Render Backend               : {status['render_backend'] or '-'}")
        print(f"Media Backend Found          : {status['media_backend_found']}")
        print(f"Media Backend                : {status['media_backend'] or '-'}")
        print(f"Render Performed             : {status['render_performed']}")
        print(f"Expression Changed           : {status['expression_changed']}")
        print(f"Gesture Changed              : {status['gesture_changed']}")
        print(f"External App Opened          : {status['external_app_opened']}")
        print(f"Command Execution            : {status['command_execution']}")
        print(f"Image File Write             : {status['image_file_write']}")
        print(f"Animation File Write         : {status['animation_file_write']}")
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
        print("Safety Notes")
        print("------------")
        for note in plan["safety_notes"]:
            print(f"- {note}")

    def blender_scene_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Scene Plan", manager.scene_plan(goal))

    def blender_asset_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Asset Plan", manager.asset_plan(goal))

    def blender_texture_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Texture/Material Plan", manager.texture_plan(goal))

    def blender_rigging_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Rigging Plan", manager.rigging_plan(goal))

    def blender_animation_plan(self, goal: str) -> None:
        manager = BlenderBridgeFoundationManager(project_root=self.project_root)
        self.print_blender_plan("AURA Blender Animation Plan", manager.animation_plan(goal))

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
