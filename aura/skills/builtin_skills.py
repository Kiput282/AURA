from aura.skills.skill import AuraSkill
from aura.skills.skill_registry import SkillRegistry


def build_builtin_skill_registry() -> SkillRegistry:
    """
    Builds AURA's default skill registry.

    Current phase:
    - online skills are already implemented
    - foundation skills exist but are not fully connected to action execution yet
    - planned skills are future roadmap items
    """

    registry = SkillRegistry()

    registry.register(
        AuraSkill(
            name="system_status",
            description="Show unified AURA system status across core foundation modules.",
            role="companion",
            permission_action="read_project",
            status="online",
            capabilities=["system_status", "foundation_summary", "readiness_overview"],
        )
    )

    registry.register(
        AuraSkill(
            name="safe_file_operation_planner",
            description="Prepare safe metadata-only file read plans, write proposals, edit proposals, move/copy/delete risk reviews, file operation checklists, and file operation context using local task planner, workspace awareness, workspace memory, and tool sandbox without reading, opening, writing, editing, moving, copying, deleting files, or executing commands automatically.",
            role="safety",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "safe_file_operation_status",
                "safe_file_read_plan",
                "safe_file_write_plan",
                "safe_file_edit_plan",
                "safe_file_move_copy_delete_risk_review",
                "safe_file_operation_checklist",
                "safe_file_operation_context",
                "metadata_only_file_operation_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="local_task_planner_alpha",
            description="Prepare safe local task intent plans, task breakdowns, risk reviews, execution checklists, and task context using project intent, creative assistant, workspace memory, and tool sandbox without executing commands, writing files, opening apps, or performing desktop actions.",
            role="planning",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "local_task_planner_status",
                "local_task_intent_plan",
                "local_task_breakdown_plan",
                "local_task_risk_review",
                "local_task_execution_checklist",
                "local_task_context",
                "safe_local_task_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="creative_assistant_foundation",
            description="Prepare safe creative briefs, character concept plans, visual asset plans, content ideas, and creative review plans using project intent, workspace memory, media understanding, expression language, and Blender bridge without generating images, opening media files, writing files, or executing commands.",
            role="creative",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "creative_assistant_status",
                "creative_brief_plan",
                "creative_character_concept_plan",
                "creative_visual_asset_plan",
                "creative_content_idea_plan",
                "creative_review_plan",
                "creative_context",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="project_intent_planner",
            description="Prepare safe project intent summaries, project goal plans, sprint intent plans, and next action candidates using workspace memory, workspace awareness, project coding, daily briefing, and reflection without writing files, memory, journal, or executing commands.",
            role="planning",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "project_intent_status",
                "project_intent_summary",
                "project_goal_plan",
                "sprint_intent_plan",
                "project_next_action_candidates",
                "project_intent_context",
                "safety_aware_project_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="workspace_memory_link",
            description="Prepare safe workspace-memory summaries and memory candidates from workspace awareness, memory, journal, and reflection without writing memory, deleting memory, writing journal entries, writing files, or executing commands.",
            role="memory",
            permission_action="read_memory",
            status="online",
            capabilities=[
                "workspace_memory_link_status",
                "workspace_memory_summary",
                "workspace_memory_candidates",
                "workspace_file_memory_candidates",
                "workspace_milestone_memory_candidates",
                "workspace_memory_link_context",
                "candidate_only_memory_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="streaming_safety_foundation",
            description="Prepare safe streaming context, chat safety, content boundary, privacy, and moderation plans without reading live chat, sending messages, moderating, capturing screen, opening apps/browser, writing files, or executing commands.",
            role="safety",
            permission_action="prepare_file",
            status="foundation",
            capabilities=[
                "streaming_safety_status",
                "streaming_context_plan",
                "streaming_chat_safety_plan",
                "streaming_content_boundary_plan",
                "streaming_privacy_plan",
                "streaming_moderation_plan",
                "streaming_safety_context",
                "non_invasive_stream_safety",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="game_companion_foundation",
            description="Prepare safe game companion session plans, strategy plans, streaming plans, and coaching plans without reading game screen, controlling input, opening games/apps, writing files, or executing commands.",
            role="creative",
            permission_action="prepare_file",
            status="foundation",
            capabilities=[
                "game_companion_status",
                "game_session_plan",
                "game_strategy_plan",
                "game_streaming_plan",
                "game_coaching_plan",
                "game_context",
                "non_invasive_game_support",
                "streaming_safe_game_notes",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="expression_language",
            description="Prepare AURA mood, emotion tags, voice tone hints, avatar expression hints, gesture hints, and response style hints without changing avatar state, playing voice output, writing files, or executing commands.",
            role="creative",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "expression_language_status",
                "expression_state",
                "expression_plan",
                "expression_voice_hint",
                "expression_avatar_hint",
                "expression_gesture_hint",
                "expression_context",
                "safe_expression_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="media_understanding_foundation",
            description="Prepare metadata-only media understanding, image description, texture reference, thumbnail/banner review, and video/audio plans without opening files, reading pixels, writing files, or executing commands.",
            role="creative",
            permission_action="read_project",
            status="foundation",
            capabilities=[
                "media_understanding_status",
                "media_asset_summary",
                "media_image_description_plan",
                "media_texture_reference_plan",
                "media_thumbnail_banner_review_plan",
                "media_video_audio_plan",
                "media_context",
                "metadata_only_media_awareness",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="blender_bridge_foundation",
            description="Prepare safe Blender scene, asset, texture/material, rigging, animation, and context plans without opening Blender, writing files, or executing commands.",
            role="creative",
            permission_action="prepare_file",
            status="foundation",
            capabilities=[
                "blender_bridge_status",
                "blender_scene_plan",
                "blender_asset_plan",
                "blender_texture_material_plan",
                "blender_rigging_plan",
                "blender_animation_plan",
                "blender_context",
                "safe_blender_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="workspace_awareness",
            description="Read AURA workspace structure, current state, important files, workspace map, and workspace context without writing or executing commands.",
            role="project_manager",
            permission_action="read_project",
            status="online",
            capabilities=[
                "workspace_awareness_status",
                "workspace_map",
                "workspace_context",
                "workspace_current_state",
                "workspace_important_files",
                "read_only_workspace_understanding",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="partner_alpha",
            description="Unify AURA memory, reflection, briefing, voice, vision, avatar, desktop, action safety, and readiness into a safe partner alpha layer.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=[
                "partner_alpha_status",
                "partner_context",
                "partner_readiness",
                "partner_next_step",
                "partner_action_safety",
                "safe_partner_layer",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="awakening_status",
            description="Show AURA Awakening Alpha readiness across Speak, See, Think, and Learn.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=["awakening_status", "readiness_check", "system_summary"],
        )
    )

    registry.register(
        AuraSkill(
            name="tool_sandbox",
            description="Check and dry-run tool commands through a safe sandbox policy without real execution.",
            role="action",
            permission_action="sandbox_check",
            status="online",
            capabilities=[
                "tool_sandbox_status",
                "tool_sandbox_policy",
                "tool_sandbox_check",
                "tool_sandbox_dry_run",
                "dangerous_command_blocking",
                "allowlist_policy",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="model_router",
            description="Select recommended model/provider routes for AURA roles and tasks without switching real runtimes yet.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=[
                "model_router_status",
                "model_router_routes",
                "model_router_select",
                "role_model_mapping",
                "runtime_switching_placeholder",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="core_loop",
            description="Run AURA alpha core loop across input, context, reasoning, planning, safety, response, and journal context.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=[
                "core_loop_status",
                "core_loop_run",
                "core_loop_trace",
                "context_reasoning_flow",
                "safe_action_proposal",
                "journal_context",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="chat",
            description="Talk with the user using AURA's companion personality and context manager.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=["conversation", "identity", "language_control", "context_aware_chat"],
        )
    )

    registry.register(
        AuraSkill(
            name="memory_recall",
            description="Recall recent memories.",
            role="memory",
            permission_action="read_project",
            status="online",
            capabilities=["memory", "recall"],
        )
    )

    registry.register(
        AuraSkill(
            name="memory_search",
            description="Search relevant memories.",
            role="memory",
            permission_action="read_project",
            status="online",
            capabilities=["memory", "search", "relevance"],
        )
    )

    registry.register(
        AuraSkill(
            name="memory_reflection",
            description="Reflect on memory and project journal to summarize milestones, highlights, and insights without modifying memory.",
            role="memory",
            permission_action="read_memory",
            status="online",
            capabilities=[
                "memory_reflection_status",
                "memory_reflect",
                "memory_insights",
                "reflection_context",
                "read_only_reflection",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="memory_manage",
            description="List, count, delete, pin, unpin, and set importance for memories.",
            role="memory",
            permission_action="write_file",
            status="online",
            capabilities=["memory_list", "memory_count", "memory_delete", "memory_pin", "memory_importance"],
        )
    )

    registry.register(
        AuraSkill(
            name="daily_project_briefing",
            description="Create read-only daily project briefings from system status, journal, memory reflection, safety state, and next-step recommendations.",
            role="project_manager",
            permission_action="read_project",
            status="online",
            capabilities=[
                "daily_briefing_status",
                "daily_briefing",
                "daily_briefing_compact",
                "daily_briefing_context",
                "project_summary",
                "next_step_recommendations",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="project_journal",
            description="Record and view AURA's project development journal.",
            role="project_manager",
            permission_action="write_file",
            status="online",
            capabilities=["journal_add", "journal_list", "progress_tracking"],
        )
    )

    registry.register(
        AuraSkill(
            name="context_preview",
            description="Build and preview a structured context packet.",
            role="memory",
            permission_action="read_project",
            status="online",
            capabilities=["context_packet", "pinned_memory", "journal_context"],
        )
    )

    registry.register(
        AuraSkill(
            name="role_list",
            description="List AURA internal roles.",
            role="project_manager",
            permission_action="read_project",
            status="online",
            capabilities=["roles", "architecture"],
        )
    )

    registry.register(
        AuraSkill(
            name="action_request",
            description="Prepare safe action request proposals with plugin action and permission metadata.",
            role="action",
            permission_action="think",
            status="online",
            capabilities=["action_request", "permission_check", "confirmation_check", "safe_action_proposal"],
        )
    )

    registry.register(
        AuraSkill(
            name="permission_check",
            description="Check whether an action is allowed, requires confirmation, or is restricted.",
            role="action",
            permission_action="think",
            status="online",
            capabilities=["permission", "action_safety"],
        )
    )

    registry.register(
        AuraSkill(
            name="plugin_action_interface",
            description="List plugin actions and check plugin action permissions.",
            role="action",
            permission_action="think",
            status="online",
            capabilities=["plugin_actions", "action_metadata", "permission_check"],
        )
    )

    registry.register(
        AuraSkill(
            name="provider_check",
            description="Check AURA reasoning provider and runtime status.",
            role="companion",
            permission_action="read_project",
            status="online",
            capabilities=["provider", "runtime_check", "ollama"],
        )
    )

    registry.register(
        AuraSkill(
            name="project_coding_v2",
            description="Analyze project code, summarize Python structure, prepare patch plans, and check command safety without writing files.",
            role="coder",
            permission_action="read_project",
            status="online",
            capabilities=[
                "project_code_status",
                "project_code_map",
                "project_code_inspect",
                "project_code_plan",
                "project_code_safety",
                "python_ast_summary",
                "safe_patch_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="coding_assist",
            description="Help with coding, debugging, software architecture, and code review.",
            role="coder",
            permission_action="think",
            status="foundation",
            capabilities=["coding", "debugging", "architecture", "code_review"],
        )
    )

    registry.register(
        AuraSkill(
            name="file_project_assist",
            description="Inspect project files, map project structure, search code, and prepare safe file-related assistance.",
            role="coder",
            permission_action="read_project",
            status="online",
            capabilities=[
                "file_review",
                "project_analysis",
                "project_summary",
                "project_map",
                "project_inspect",
                "project_find",
                "safe_file_read",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="desktop_assistant_alpha",
            description="Prepare safe desktop assistant alpha status, desktop action plans, open app/browser/file plans, and workspace context without automatic desktop execution.",
            role="action",
            permission_action="think",
            status="online",
            capabilities=[
                "desktop_alpha_status",
                "desktop_action_plan",
                "desktop_open_app_plan",
                "desktop_open_browser_plan",
                "desktop_open_file_plan",
                "desktop_workspace_context",
                "safe_desktop_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="desktop_bridge",
            description="Show desktop bridge status, capabilities, and prepare desktop action proposals.",
            role="action",
            permission_action="think",
            status="online",
            capabilities=[
                "desktop_status",
                "desktop_capabilities",
                "desktop_action_proposal",
                "os_detection",
                "safe_desktop_placeholder",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="app_launcher",
            description="Prepare application, browser, or file opening through the desktop bridge.",
            role="action",
            permission_action="open_app",
            status="foundation",
            capabilities=["open_app", "open_browser", "open_file", "desktop_bridge", "confirmation_required"],
        )
    )

    registry.register(
        AuraSkill(
            name="vision_runtime_alpha",
            description="Prepare safe local vision runtime alpha status, screen plans, camera plans, and context without automatic screen or camera access.",
            role="vision",
            permission_action="screen_analyze",
            status="online",
            capabilities=[
                "vision_runtime_alpha_status",
                "vision_screen_plan",
                "vision_camera_plan",
                "vision_runtime_context",
                "screen_dependency_check",
                "camera_dependency_check",
                "prepare_only_vision_input",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="vision_runtime_planning",
            description="Plan local screen/camera capture, vision model candidates, dependency checks, and safe vision runtime readiness.",
            role="vision",
            permission_action="think",
            status="online",
            capabilities=[
                "vision_runtime_status",
                "vision_runtime_plan",
                "vision_runtime_check",
                "screen_capture_candidates",
                "camera_capture_candidates",
                "vision_model_candidates",
                "dependency_check",
                "vision_permission_mapping",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="vision_foundation",
            description="Show AURA vision foundation status and placeholder vision providers.",
            role="vision",
            permission_action="think",
            status="online",
            capabilities=["vision_status", "screen_placeholder", "camera_placeholder", "vision_runtime_planning"],
        )
    )

    registry.register(
        AuraSkill(
            name="screen_analyzer",
            description="Future screen analysis once screen runtime is connected.",
            role="vision",
            permission_action="screen_analyze",
            status="foundation",
            capabilities=[
                "screen_analysis",
                "visual_context",
                "screen_permission",
                "runtime_planning",
                "confirmation_required",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="camera_analyzer",
            description="Future camera and environment analysis once camera runtime is connected.",
            role="vision",
            permission_action="camera_analyze",
            status="foundation",
            capabilities=[
                "camera_context",
                "environment_analysis",
                "camera_permission",
                "runtime_planning",
                "confirmation_required",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_runtime_alpha",
            description="Prepare safe local voice runtime alpha status, speak plans, speak tests, and context without automatic microphone access or speaker playback.",
            role="voice",
            permission_action="speaker_speak",
            status="online",
            capabilities=[
                "voice_runtime_alpha_status",
                "voice_speak_plan",
                "voice_speak_test",
                "voice_runtime_context",
                "tts_dependency_check",
                "prepare_only_speech_output",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_runtime_planning",
            description="Plan local STT/TTS runtime providers, dependency checks, and safe voice runtime readiness.",
            role="voice",
            permission_action="think",
            status="online",
            capabilities=[
                "voice_runtime_status",
                "voice_runtime_plan",
                "voice_runtime_check",
                "stt_candidates",
                "tts_candidates",
                "dependency_check",
                "voice_permission_mapping",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_foundation",
            description="Show AURA voice foundation status and placeholder voice providers.",
            role="voice",
            permission_action="think",
            status="online",
            capabilities=["voice_status", "stt_placeholder", "tts_placeholder", "voice_runtime_planning"],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_interaction",
            description="Future voice input and output once STT/TTS providers are connected.",
            role="voice",
            permission_action="microphone_listen",
            status="foundation",
            capabilities=[
                "speech_to_text",
                "text_to_speech",
                "voice_mode",
                "microphone_permission",
                "speaker_permission",
                "runtime_planning",
                "confirmation_required",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="avatar_runtime_alpha",
            description="Prepare safe local avatar runtime alpha status, expression plans, gesture plans, and context without automatic rendering or file writing.",
            role="avatar",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "avatar_runtime_alpha_status",
                "avatar_expression_plan",
                "avatar_gesture_plan",
                "avatar_runtime_context",
                "avatar_dependency_check",
                "prepare_only_avatar_control",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="avatar_foundation",
            description="Show AURA avatar foundation status, providers, placeholder state, and avatar runtime planning metadata.",
            role="avatar",
            permission_action="think",
            status="online",
            capabilities=[
                "avatar_status",
                "avatar_providers",
                "avatar_state",
                "expression_options",
                "gesture_options",
                "vrm_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="avatar_control",
            description="Prepare avatar state, expression, gesture, and body control proposals.",
            role="avatar",
            permission_action="prepare_file",
            status="foundation",
            capabilities=[
                "vrm",
                "expression",
                "gesture",
                "avatar_state",
                "expression_proposal",
                "gesture_proposal",
                "runtime_placeholder",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="motion_capture",
            description="Use hand tracking, body tracking, and motion capture for avatar movement.",
            role="motion",
            permission_action="camera_analyze",
            status="planned",
            capabilities=["hand_tracking", "body_tracking", "pose_control", "mocap"],
        )
    )

    registry.register(
        AuraSkill(
            name="streaming_assist",
            description="Assist livestreaming, OBS, chat reaction, and performance mode.",
            role="streaming",
            permission_action="prepare_file",
            status="planned",
            capabilities=["obs", "livestream", "chat_reaction", "singing_mode"],
        )
    )

    registry.register(
        AuraSkill(
            name="gaming_companion",
            description="Act as gaming companion and sandbox game helper.",
            role="gaming",
            permission_action="think",
            status="planned",
            capabilities=["gaming", "sandbox", "game_context"],
        )
    )

    registry.register(
        AuraSkill(
            name="creative_generation",
            description="Help with image, 3D, character, and creative asset generation.",
            role="creative",
            permission_action="prepare_file",
            status="planned",
            capabilities=["image_generation", "3d_generation", "asset_concept"],
        )
    )

    registry.register(
        AuraSkill(
            name="codebase_change_planner",
            description="Prepare safe metadata-only codebase change intent plans, impact plans, patch plans, validation plans, rollback plans, and change context without reading, writing, editing, executing commands, committing, or pushing automatically.",
            role="coder",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "codebase_change_status",
                "codebase_change_intent_plan",
                "codebase_change_impact_plan",
                "codebase_patch_plan",
                "codebase_validation_plan",
                "codebase_rollback_plan",
                "codebase_change_context",
                "metadata_only_codebase_change_planning",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="codebase_patch_proposal_renderer",
            description="Render safe proposal-only codebase patch review packets with candidate surfaces, patch outline, validation packet, rollback packet, and safety boundary without reading, writing, editing, applying patches, executing commands, committing, or pushing automatically.",
            role="coder",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "codebase_patch_proposal_status",
                "codebase_patch_proposal_render",
                "codebase_patch_review_packet",
                "codebase_patch_safety_packet",
                "codebase_patch_validation_packet",
                "codebase_patch_rollback_packet",
                "codebase_patch_proposal_context",
                "proposal_only_patch_rendering",
            ],
        )
    )

    registry.register(
        AuraSkill(
            name="codebase_validation_gate_planner",
            description="Plan safe proposal-only validation gates for codebase changes, including preflight, static validation, registry validation, runtime smoke, diff review, rollback, and commit/push gates without executing commands automatically.",
            role="coder",
            permission_action="prepare_file",
            status="online",
            capabilities=[
                "codebase_validation_gate_status",
                "codebase_validation_gate_plan",
                "codebase_preflight_gate",
                "codebase_static_validation_gate",
                "codebase_registry_validation_gate",
                "codebase_runtime_smoke_gate",
                "codebase_diff_review_gate",
                "codebase_rollback_gate",
                "codebase_commit_push_gate",
                "codebase_validation_gate_context",
                "proposal_only_validation_gating",
            ],
        )
    )

    # Sprint 66.0 voice conversation planner skill.
    registry.register(
        AuraSkill(
            name="voice_conversation_planner",
            description="Plan safe metadata-only voice conversation flows, intent, response style, turn handling, and safety boundaries without microphone access, TTS output, speaker output, command execution, app opening, or runtime voice action.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "voice_conversation_status",
                "voice_intent_plan",
                "voice_response_plan",
                "conversation_turn_plan",
                "voice_safety_plan",
                "voice_conversation_context",
                "metadata_only_voice_conversation_planning",
            ],
        )
    )

    # Sprint 67.0 vision context planner skill.
    registry.register(
        AuraSkill(
            name="vision_context_planner",
            description="Plan safe metadata-only visual context flows for screen, camera, and general vision needs without screen capture, camera access, image reading, OCR runtime, file operations, command execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "vision_context_status",
                "visual_context_plan",
                "screen_context_plan",
                "camera_context_plan",
                "vision_safety_plan",
                "vision_context",
                "metadata_only_vision_context_planning",
            ],
        )
    )

    # Sprint 68.0 avatar interaction planner skill.
    registry.register(
        AuraSkill(
            name="avatar_interaction_planner",
            description="Plan safe metadata-only avatar interaction flows for expressions, gestures, poses, streaming presence, and safety boundaries without rendering, animation playback, mocap, rig manipulation, Blender execution, file operations, command execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "avatar_interaction_status",
                "avatar_expression_plan",
                "avatar_gesture_plan",
                "avatar_pose_plan",
                "avatar_streaming_presence_plan",
                "avatar_safety_plan",
                "avatar_interaction_context",
                "metadata_only_avatar_interaction_planning",
            ],
        )
    )

    # Sprint 69.0 desktop workflow planner skill.
    registry.register(
        AuraSkill(
            name="desktop_workflow_planner",
            description="Plan safe metadata-only desktop workflows, app context, window flow, task sequences, and safety boundaries without app opening, window control, mouse/keyboard control, screen capture, file operations, command execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "desktop_workflow_status",
                "desktop_workflow_plan",
                "desktop_app_context_plan",
                "desktop_window_flow_plan",
                "desktop_task_sequence_plan",
                "desktop_safety_plan",
                "desktop_workflow_context",
                "metadata_only_desktop_workflow_planning",
            ],
        )
    )

    # Sprint 70.0 partner runtime planning layer skill.
    registry.register(
        AuraSkill(
            name="partner_runtime_planning_layer",
            description="Plan safe metadata-only partner runtime coordination, session flow, multimodal handoff, tool permission gates, growth checkpoints, and runtime safety without autonomous runtime, tool execution, file operations, command execution, desktop control, device access, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "partner_runtime_status",
                "partner_runtime_mode_plan",
                "partner_session_plan",
                "partner_multimodal_handoff_plan",
                "partner_tool_permission_plan",
                "partner_growth_cycle_plan",
                "partner_runtime_safety_plan",
                "partner_runtime_context",
                "metadata_only_partner_runtime_planning",
            ],
        )
    )

    # Sprint 71.0 thought loop planner skill.
    registry.register(
        AuraSkill(
            name="thought_loop_planner",
            description="Plan safe metadata-only thought cycles, intent framing, visible reasoning summaries, uncertainty review, action readiness, growth memory review, and thought safety without autonomous loops, tool execution, memory write, internet search, file operations, command execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "thought_loop_status",
                "thought_cycle_plan",
                "intent_frame_plan",
                "reasoning_summary_plan",
                "uncertainty_review_plan",
                "action_readiness_review",
                "growth_memory_review",
                "thought_safety_plan",
                "thought_loop_context",
                "metadata_only_thought_loop_planning",
            ],
        )
    )

    # Sprint 72.0 reasoning context manager skill.
    registry.register(
        AuraSkill(
            name="reasoning_context_manager",
            description="Prepare safe metadata-only visible reasoning context, fact/assumption separation, unknowns review, evidence boundaries, decision frames, response strategy, and reasoning safety without exposing hidden chain-of-thought, autonomous reasoning loops, tool execution, memory write, internet search, file operations, command execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "reasoning_context_status",
                "reasoning_context_plan",
                "fact_assumption_plan",
                "unknowns_review_plan",
                "evidence_boundary_plan",
                "decision_frame_plan",
                "response_strategy_plan",
                "reasoning_safety_plan",
                "reasoning_context",
                "metadata_only_reasoning_context_management",
            ],
        )
    )

    # Sprint 73.0 knowledge uncertainty gate skill.
    registry.register(
        AuraSkill(
            name="knowledge_uncertainty_gate",
            description="Plan safe metadata-only knowledge uncertainty handling, knowledge gaps, internet search permission gates, source requirements, download requirement notices, answer confidence, and knowledge safety without real internet search, downloads, network actions, file operations, command execution, memory write, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "knowledge_uncertainty_status",
                "knowledge_gap_plan",
                "uncertainty_review_plan",
                "internet_search_gate_plan",
                "source_requirement_plan",
                "download_requirement_plan",
                "answer_confidence_plan",
                "knowledge_safety_plan",
                "knowledge_uncertainty_context",
                "metadata_only_knowledge_uncertainty_gate",
            ],
        )
    )

    # Sprint 74.0 voice input runtime foundation skill.
    registry.register(
        AuraSkill(
            name="voice_input_runtime_foundation",
            description="Prepare safe foundation-only voice input runtime plans for microphone permission, voice capture boundaries, speech-to-text adapter planning, voice intent gates, command confirmation, voice sessions, and voice input safety without microphone access, audio recording, STT runtime, voice command execution, file operations, command execution, internet access, network actions, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "voice_input_status",
                "voice_input_permission_plan",
                "voice_capture_boundary_plan",
                "speech_to_text_adapter_plan",
                "voice_intent_gate_plan",
                "voice_command_confirmation_plan",
                "voice_session_plan",
                "voice_input_safety_plan",
                "voice_input_context",
                "foundation_only_voice_input_runtime",
            ],
        )
    )

    # Sprint 75.0 voice intent understanding skill.
    registry.register(
        AuraSkill(
            name="voice_intent_understanding",
            description="Prepare planner-only voice intent understanding for transcript normalization, intent classification, entity/slot extraction, clarification, action gates, response planning, and safety without microphone access, audio recording, speech-to-text runtime, voice command execution, tool execution, file operations, command execution, memory write, internet/network action, desktop control, git execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "voice_intent_status",
                "voice_transcript_normalization_plan",
                "voice_intent_classification_plan",
                "voice_entity_slot_plan",
                "voice_clarification_plan",
                "voice_action_gate_plan",
                "voice_response_plan",
                "voice_intent_safety_plan",
                "voice_intent_context",
                "planner_only_voice_intent_understanding",
            ],
        )
    )

    # Sprint 76.0 vision input runtime foundation skill.
    registry.register(
        AuraSkill(
            name="vision_input_runtime_foundation",
            description="Prepare foundation-only vision input runtime planning for camera permission, screen/image input boundaries, visual source selection, image adapter planning, visual sessions, visual action gates, and vision safety without camera access, screen capture, image capture, video capture, vision runtime, OCR runtime, visual command execution, file operations, command execution, tool execution, memory write, internet/network action, desktop control, git execution, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "vision_input_status",
                "vision_input_permission_plan",
                "visual_capture_boundary_plan",
                "image_input_adapter_plan",
                "visual_source_plan",
                "visual_session_plan",
                "visual_action_gate_plan",
                "vision_input_safety_plan",
                "vision_input_context",
                "planner_only_vision_input_foundation",
            ],
        )
    )

    # Sprint 77.0 visual context understanding skill.
    registry.register(
        AuraSkill(
            name="visual_context_understanding",
            description="Prepare planner-only visual context understanding for scene context, object/relation planning, text-in-image context, uncertainty handling, clarification, visual response planning, and visual safety without camera access, screen capture, image/video capture, vision runtime, OCR runtime, object detection runtime, face recognition, biometric identification, identity recognition, visual command execution, file operations, command execution, tool execution, memory write, internet/network action, desktop control, git execution, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "visual_context_status",
                "visual_scene_understanding_plan",
                "visual_object_relation_plan",
                "visual_text_context_plan",
                "visual_uncertainty_plan",
                "visual_clarification_plan",
                "visual_response_context_plan",
                "visual_context_safety_plan",
                "visual_context",
                "planner_only_visual_context_understanding",
            ],
        )
    )

    # Sprint 78.0 coder project generation planner skill.
    registry.register(
        AuraSkill(
            name="coder_project_generation_planner",
            description="Prepare planner-only code/project generation for project request framing, project structure blueprints, code file blueprints, dependency planning, generation review gates, validation strategy, and project generation safety without creating projects, directories, or files; without reading, writing, modifying, or deleting files; without code execution, test execution, command execution, dependency install, package download, tool execution, memory write, internet/network action, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "coder_project_status",
                "project_request_frame_plan",
                "project_structure_plan",
                "code_file_blueprint_plan",
                "dependency_plan",
                "generation_review_gate_plan",
                "validation_strategy_plan",
                "project_generation_safety_plan",
                "coder_project_context",
                "planner_only_project_generation",
            ],
        )
    )

    # Sprint 79.0 dependency download permission gate skill.
    registry.register(
        AuraSkill(
            name="dependency_download_permission_gate",
            description="Prepare planner-only dependency and download permission gates for dependency request review, package/source review, download permission, install command review, dependency risk review, offline alternatives, and safety without dependency install, package/model/asset/installer/binary download, network action, internet search, package manager runtime, command execution, tool execution, file operations, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "dependency_permission_status",
                "dependency_request_review_plan",
                "package_source_review_plan",
                "download_permission_plan",
                "install_command_review_plan",
                "dependency_risk_plan",
                "offline_alternative_plan",
                "dependency_permission_safety_plan",
                "dependency_permission_context",
                "planner_only_dependency_download_permission",
            ],
        )
    )

    return registry
