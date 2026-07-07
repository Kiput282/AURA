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

    # Sprint 80.0 review stabilization 71-80 skill.
    registry.register(
        AuraSkill(
            name="review_stabilization_71_80",
            description="Prepare planner-only Sprint 71-80 checkpoint review and stabilization planning for completed feature review, active/foundation/planner-only review, safety boundary review, stabilization validation, technical debt review, roadmap gap review, and next block planning without runtime behavior changes, automatic stabilization, file operations, command execution, test execution, code execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "checkpoint_71_80_status",
                "completed_feature_review_plan",
                "active_foundation_review_plan",
                "safety_boundary_review_plan",
                "stabilization_validation_plan",
                "technical_debt_review_plan",
                "roadmap_gap_review_plan",
                "next_block_planning_plan",
                "checkpoint_71_80_context",
                "planner_only_checkpoint_review",
            ],
        )
    )

    # Sprint 81.0 shared output formatter skill.
    registry.register(
        AuraSkill(
            name="shared_output_formatter",
            description="Provide renderer-only shared output formatting for AURA CLI, shell, service monitor, and future Control Center output without runtime behavior changes, automatic CLI/shell refactor, UI runtime, web server runtime, chat runtime, service runtime, file operations, command execution, test execution, code execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "shared_output_formatter_status",
                "packet_render_plan",
                "safety_boundary_render_plan",
                "cli_output_format_plan",
                "shell_output_format_plan",
                "console_output_format_plan",
                "ui_output_contract_plan",
                "formatter_migration_plan",
                "shared_output_formatter_context",
                "renderer_only_formatting",
            ],
        )
    )

    # Sprint 82.0 capability registry skill.
    registry.register(
        AuraSkill(
            name="capability_registry",
            description="Provide planner-only central AURA capability registry metadata for current capabilities, capability states, runtime levels, risk levels, permission requirements, future Control Center views, capability gaps, and registry migration without runtime behavior changes, automatic capability enablement, dynamic runtime discovery, runtime action activation, permission grant runtime, UI runtime, web server runtime, chat runtime, service runtime, launcher runtime, file operations, command execution, test execution, code execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "capability_registry_status",
                "capability_catalog_plan",
                "capability_state_review_plan",
                "permission_requirement_review_plan",
                "risk_level_review_plan",
                "control_center_capability_view_plan",
                "capability_gap_review_plan",
                "capability_registry_migration_plan",
                "capability_registry_context",
                "control_center_capability_data",
            ],
        )
    )

    # Sprint 83.0 unified permission workflow skill.
    registry.register(
        AuraSkill(
            name="unified_permission_workflow",
            description="Provide planner-only unified permission workflow planning for permission requests, approval/deny states, risk review, confirmation prompts, audit trail planning, future Control Center Permission Center views, and permission policy gap review without granting permission, automatic approval, always-approve mode, background approval, runtime action activation, runtime behavior changes, file operations, command execution, dependency install, download runtime, microphone/camera/screen runtime, internet runtime, desktop control runtime, git runtime, plugin install runtime, service control runtime, UI runtime, web server runtime, chat runtime, launcher runtime, tool execution, memory write, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "permission_workflow_status",
                "permission_request_plan",
                "permission_state_transition_plan",
                "permission_risk_review_plan",
                "confirmation_prompt_plan",
                "permission_audit_trail_plan",
                "control_center_permission_view_plan",
                "permission_policy_gap_review_plan",
                "permission_workflow_context",
                "control_center_permission_data",
            ],
        )
    )

    # Sprint 84.0 runtime service foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_service_foundation",
            description="Prepare planner-only AURA runtime service foundation for ATLAS safe_idle boot mode, service lifecycle planning, health check planning, systemd unit blueprint planning, recovery planning, service monitor view planning, and auto-boot policy planning without creating systemd services, enabling systemd, starting/stopping/restarting services, starting background processes, enabling auto-boot runtime, binding ports, running web/UI/chat/launcher runtime, granting permissions, activating runtime actions, changing runtime behavior, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_service_status",
                "safe_idle_boot_plan",
                "service_lifecycle_plan",
                "service_health_check_plan",
                "systemd_unit_blueprint_plan",
                "service_recovery_plan",
                "service_monitor_view_plan",
                "auto_boot_policy_plan",
                "runtime_service_context",
                "safe_idle_service_planning",
            ],
        )
    )

    # Sprint 85.0 launcher health monitor foundation skill.
    registry.register(
        AuraSkill(
            name="aura_launcher_health_monitor_foundation",
            description="Prepare planner-only AURA Launcher and Health Monitor foundation for safe_idle launch planning, start/stop/restart/status/logs planning, health monitor planning, Control Center service monitor planning, and launcher safety policy planning without starting/stopping/restarting processes, executing systemctl, creating services, reading log files, enabling auto-boot runtime, binding ports, running web/UI/chat/service runtime, granting permissions, activating runtime actions, changing runtime behavior, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "launcher_health_status",
                "launcher_start_plan",
                "launcher_stop_plan",
                "launcher_restart_plan",
                "launcher_status_plan",
                "launcher_log_view_plan",
                "health_monitor_plan",
                "control_center_service_monitor_plan",
                "launcher_safety_policy_plan",
                "launcher_health_context",
                "safe_idle_launcher_monitor_data",
            ],
        )
    )

    # Sprint 86.0 control center UI blueprint skill.
    registry.register(
        AuraSkill(
            name="aura_control_center_ui_blueprint",
            description="Prepare planner-only AURA Control Center / Genesis Console UI blueprint for dashboard layout, Permission Center, Service Monitor, Capability Viewer, Launcher Control, Chat Console placeholder, Plugin Dashboard, Action Log, and safety policy planning without creating frontend apps, backend services, web routes, binding ports, opening browser windows, running UI/web/chat/service/launcher/plugin runtime, granting permissions, activating runtime actions, changing runtime behavior, reading logs, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "control_center_status",
                "dashboard_layout_blueprint_plan",
                "permission_center_blueprint_plan",
                "service_monitor_blueprint_plan",
                "capability_viewer_blueprint_plan",
                "launcher_control_blueprint_plan",
                "chat_console_placeholder_plan",
                "plugin_dashboard_blueprint_plan",
                "action_log_blueprint_plan",
                "control_center_safety_policy_plan",
                "control_center_context",
                "genesis_console_blueprint_data",
            ],
        )
    )

    # Sprint 87.0 local console web foundation skill.
    registry.register(
        AuraSkill(
            name="aura_local_console_web_foundation",
            description="Prepare planner-only AURA Local Console Web Foundation for localhost-only policy planning, route blueprint planning, API contract blueprint planning, static asset blueprint planning, session state blueprint planning, security boundary planning, Control Center web bridge planning, and developer console access planning without starting web servers, binding ports, creating live routes, serving static files, opening browsers, creating frontend/backend runtime, enabling API runtime, enabling session runtime, allowing public/LAN/remote access, running websocket/chat/UI/service/launcher runtime, granting permissions, activating runtime actions, changing runtime behavior, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "local_console_web_status",
                "local_host_policy_plan",
                "route_blueprint_plan",
                "api_contract_blueprint_plan",
                "static_asset_blueprint_plan",
                "session_state_blueprint_plan",
                "security_boundary_plan",
                "control_center_web_bridge_plan",
                "developer_console_access_plan",
                "local_console_web_context",
                "localhost_only_console_metadata",
            ],
        )
    )

    # Sprint 88.0 chat bridge session state foundation skill.
    registry.register(
        AuraSkill(
            name="aura_chat_bridge_session_state_foundation",
            description="Prepare planner-only AURA Chat Bridge and Session State Foundation for conversation session metadata, message flow blueprints, Control Center chat panel bridge planning, Local Console session contract planning, permission-aware chat action boundary planning, chat context persistence blueprint planning, websocket boundary planning, session recovery blueprint planning, and chat bridge safety policy without starting chat runtime, conversation runtime, session runtime, websocket runtime, web/frontend/backend/API runtime, binding ports, sending or receiving messages, persisting sessions, granting permissions, activating runtime actions, changing runtime behavior, running service/launcher/plugin runtime, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "chat_bridge_status",
                "conversation_session_blueprint_plan",
                "message_flow_blueprint_plan",
                "control_center_chat_panel_bridge_plan",
                "local_console_session_contract_plan",
                "permission_aware_chat_action_boundary_plan",
                "chat_context_persistence_blueprint_plan",
                "websocket_boundary_plan",
                "session_recovery_blueprint_plan",
                "chat_bridge_safety_policy_plan",
                "chat_bridge_context",
                "safe_idle_chat_session_metadata",
            ],
        )
    )

    # Sprint 89.0 plugin permission dashboard foundation skill.
    registry.register(
        AuraSkill(
            name="aura_plugin_permission_dashboard_foundation",
            description="Prepare planner-only AURA Plugin / Permission Dashboard Foundation for plugin/action registry dashboard planning, permission request dashboard planning, permission decision visibility planning, chat-originated action request visibility planning, capability-permission matrix planning, Control Center dashboard bridge planning, Local Console dashboard contract planning, audit trail dashboard blueprint planning, and dashboard safety policy without enabling plugin runtime, installing/enabling/disabling plugins, executing plugin actions, granting or denying permissions, resolving permission requests, activating runtime actions, executing chat-originated actions, calling tools, running service/launcher/chat/session/web/frontend/backend/API runtime, creating routes, binding ports, reading or writing logs, file operations, command execution, dependency install, package download, internet/network action, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "plugin_permission_dashboard_status",
                "plugin_registry_dashboard_plan",
                "permission_request_dashboard_plan",
                "permission_decision_visibility_plan",
                "chat_originated_action_visibility_plan",
                "capability_permission_matrix_plan",
                "control_center_dashboard_bridge_plan",
                "local_console_dashboard_contract_plan",
                "audit_trail_dashboard_blueprint_plan",
                "dashboard_safety_policy_plan",
                "plugin_permission_dashboard_context",
                "plugin_permission_visibility_metadata",
            ],
        )
    )

    # Sprint 116.0 ORION client boundary contract foundation skill.
    registry.register(
        AuraSkill(
            name="aura_orion_client_boundary_contract_foundation",
            description="Prepare planner-only, metadata-only, and boundary-contract-only ORION Client Boundary Contract Foundation without starting ORION client runtime, attempting handshakes, capturing screen, starting voice/avatar sessions, executing local actions, controlling desktop, starting services, probing networks, mutating files, writing audit events, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "orion_client_boundary_contract_status",
                "orion_client_identity_boundary_plan",
                "atlas_orion_authority_boundary_plan",
                "orion_sense_permission_boundary_plan",
                "orion_local_action_boundary_plan",
                "orion_emergency_stop_boundary_plan",
                "orion_dashboard_status_boundary_plan",
                "orion_runtime_handshake_boundary_plan",
                "orion_data_flow_redaction_boundary_plan",
                "future_orion_runtime_boundary_plan",
                "orion_client_boundary_contract_context",
            ],
        )
    )

    # Sprint 115.0 safe local action contract review foundation skill.
    registry.register(
        AuraSkill(
            name="aura_safe_local_action_contract_review_foundation",
            description="Prepare planner-only, metadata-only, and contract-review-only Safe Local Action Contract Review Foundation without opening files/folders/software, creating files/folders, writing files, starting services, dispatching actions, executing tools/commands, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "safe_local_action_contract_review_status",
                "local_open_contract_review_plan",
                "controlled_create_contract_review_plan",
                "controlled_write_preview_contract_review_plan",
                "action_preview_packet_contract_plan",
                "permission_scope_contract_review_plan",
                "side_effect_boundary_contract_plan",
                "rollback_cancel_contract_review_plan",
                "dashboard_contract_payload_plan",
                "future_action_runtime_boundary_plan",
                "safe_local_action_contract_review_context",
            ],
        )
    )

    # Sprint 114.0 dashboard runtime readiness view model foundation skill.
    registry.register(
        AuraSkill(
            name="aura_dashboard_runtime_readiness_view_model_foundation",
            description="Prepare planner-only, metadata-only, and view-model-only Dashboard Runtime Readiness View Model Foundation without starting dashboard runtime, API server, web server, frontend/backend runtime, writing dashboard state, emitting dashboard events, dispatching actions, executing tools/commands, mutating files, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "dashboard_runtime_readiness_view_model_status",
                "runtime_readiness_summary_view_plan",
                "permission_state_view_plan",
                "audit_review_queue_view_plan",
                "safety_boundary_view_plan",
                "orion_boundary_view_plan",
                "action_preview_view_plan",
                "manual_approval_view_plan",
                "v1_cutline_view_plan",
                "control_center_payload_view_plan",
                "dashboard_runtime_readiness_view_model_context",
            ],
        )
    )

    # Sprint 113.0 audit event review queue foundation skill.
    registry.register(
        AuraSkill(
            name="aura_audit_event_review_queue_foundation",
            description="Prepare planner-only, metadata-only, and review-queue-blueprint-only Audit Event Review Queue Foundation without writing, emitting, streaming, sending, or persisting audit events; without activating audit writers, persisting review outcomes, dispatching actions, executing tools/commands, mutating files, starting services, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "audit_event_review_queue_status",
                "audit_event_intake_schema_plan",
                "review_queue_state_model_plan",
                "audit_event_triage_rule_plan",
                "permission_linkage_review_plan",
                "runtime_boundary_review_plan",
                "redaction_visibility_review_plan",
                "dashboard_review_queue_payload_plan",
                "review_outcome_catalog_plan",
                "future_audit_writer_boundary_plan",
                "audit_event_review_queue_context",
            ],
        )
    )

    # Sprint 112.0 runtime permission flow consolidation foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_permission_flow_consolidation_foundation",
            description="Prepare planner-only, metadata-only, and permission-flow-consolidation-only Runtime Permission Flow Consolidation Foundation without changing permissions, granting approvals, denying runtime, activating future grants, writing audit events, dispatching actions, executing tools/commands, mutating files, starting services, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_permission_flow_consolidation_status",
                "permission_request_schema_consolidation_plan",
                "permission_decision_state_model_plan",
                "manual_approval_checkpoint_plan",
                "denial_cancellation_flow_plan",
                "permission_scope_boundary_plan",
                "high_risk_escalation_rule_plan",
                "approval_audit_reference_plan",
                "dashboard_permission_flow_payload_plan",
                "future_runtime_grant_boundary_plan",
                "runtime_permission_flow_consolidation_context",
            ],
        )
    )

    # Sprint 111.0 genesis runtime readiness next block planning foundation skill.
    registry.register(
        AuraSkill(
            name="aura_genesis_runtime_readiness_next_block_planning_foundation",
            description="Prepare planner-only, metadata-only, and next-block-planning-only Genesis Runtime Readiness Sprint 111-120 planning foundation without enabling runtime execution, dispatching actions, executing tools/commands, mutating files, starting services, binding ports, probing networks, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "genesis_runtime_readiness_next_block_planning_status",
                "next_block_sprint_candidate_plan",
                "runtime_readiness_continuity_plan",
                "manual_approval_evolution_plan",
                "audit_event_evolution_plan",
                "dashboard_contract_evolution_plan",
                "orion_boundary_planning_plan",
                "safe_local_action_boundary_plan",
                "integration_stabilization_plan",
                "v1_readiness_mapping_plan",
                "genesis_runtime_readiness_next_block_planning_context",
            ],
        )
    )

    # Sprint 110.0 review stabilization 101-110 foundation skill.
    registry.register(
        AuraSkill(
            name="aura_review_stabilization_101_110_foundation",
            description="Prepare planner-only, metadata-only, and checkpoint-review-only Sprint 101-110 review stabilization foundation without executing runtime actions, changing permissions, mutating files, starting services, binding ports, probing networks, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "review_stabilization_101_110_status",
                "sprint_completion_inventory_plan",
                "runtime_readiness_foundation_audit_plan",
                "safety_invariant_verification_plan",
                "capability_registry_delta_review_plan",
                "integration_surface_review_plan",
                "documentation_roadmap_consistency_plan",
                "checkpoint_risk_review_plan",
                "deferred_runtime_boundary_plan",
                "next_block_readiness_plan",
                "review_stabilization_101_110_context",
            ],
        )
    )

    # Sprint 109.0 runtime safety freeze manual approval barrier foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_safety_freeze_manual_approval_barrier_foundation",
            description="Prepare planner-only, metadata-only, and barrier-blueprint-only Runtime Safety Freeze Manual Approval Barrier Foundation without activating runtime freeze, granting approvals, releasing freeze, passing barriers, dispatching actions, executing tools/commands, mutating files, starting services, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_safety_freeze_manual_approval_barrier_status",
                "safety_freeze_candidate_inventory_plan",
                "manual_approval_barrier_input_plan",
                "freeze_condition_check_plan",
                "approval_requirement_rule_plan",
                "blocked_runtime_catalog_plan",
                "user_confirmation_barrier_plan",
                "emergency_stop_requirement_plan",
                "audit_freeze_packet_preview_plan",
                "dashboard_barrier_payload_plan",
                "runtime_safety_freeze_manual_approval_barrier_context",
            ],
        )
    )

    # Sprint 108.0 runtime audit event packet preview foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_audit_event_packet_preview_foundation",
            description="Prepare planner-only, metadata-only, and audit-packet-preview-only Runtime Audit Event Packet Preview Foundation without writing audit logs, emitting events, streaming events, persisting records, writing files, dispatching actions, executing tools/commands, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_audit_event_packet_preview_status",
                "audit_event_candidate_inventory_plan",
                "audit_event_input_snapshot_plan",
                "runtime_reference_mapping_plan",
                "permission_reference_mapping_plan",
                "action_preview_reference_plan",
                "audit_payload_shape_plan",
                "audit_visibility_rule_plan",
                "retention_redaction_boundary_plan",
                "dashboard_audit_packet_plan",
                "runtime_audit_event_packet_preview_context",
            ],
        )
    )

    # Sprint 107.0 local runtime execution gate dry-run foundation skill.
    registry.register(
        AuraSkill(
            name="aura_local_runtime_execution_gate_dry_run_foundation",
            description="Prepare planner-only, metadata-only, and dry-run-gate-blueprint-only Local Runtime Execution Gate Dry-Run Foundation without opening gates, executing actions, starting services, binding ports, probing networks, changing permissions, reading/writing files, executing tools/commands, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "local_runtime_execution_gate_dry_run_status",
                "execution_gate_candidate_inventory_plan",
                "runtime_gate_input_contract_plan",
                "gate_preflight_evaluation_plan",
                "safe_runtime_profile_reference_plan",
                "permission_gate_reference_plan",
                "execution_gate_decision_plan",
                "block_reason_catalog_plan",
                "audit_gate_record_plan",
                "dashboard_gate_payload_plan",
                "local_runtime_execution_gate_dry_run_context",
            ],
        )
    )

    # Sprint 106.0 runtime action execution preview packet foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_action_execution_preview_packet_foundation",
            description="Prepare planner-only, metadata-only, and preview-packet-only Runtime Action Execution Preview Packet Foundation without dispatching actions, executing actions, executing tools/commands, changing permissions, reading/writing files, starting services, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_action_execution_preview_packet_status",
                "action_candidate_inventory_plan",
                "execution_preflight_checklist_plan",
                "action_input_snapshot_plan",
                "permission_decision_reference_plan",
                "execution_step_preview_plan",
                "side_effect_boundary_plan",
                "rollback_preview_plan",
                "audit_preview_record_plan",
                "user_confirmation_packet_plan",
                "runtime_action_execution_preview_packet_context",
            ],
        )
    )

    # Sprint 105.0 permission decision runtime dry-run foundation skill.
    registry.register(
        AuraSkill(
            name="aura_permission_decision_runtime_dry_run_foundation",
            description="Prepare planner-only, metadata-only, and dry-run-blueprint-only Permission Decision Runtime Dry-Run Foundation without changing, granting, denying, activating, or executing real permissions, actions, files, services, tools, commands, ORION handshakes, memory writes, or git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "permission_decision_runtime_dry_run_status",
                "permission_decision_candidate_inventory_plan",
                "permission_decision_input_contract_plan",
                "permission_decision_dry_run_evaluation_plan",
                "permission_scope_mapping_plan",
                "approval_denial_outcome_plan",
                "risk_review_rule_plan",
                "audit_record_blueprint_plan",
                "dashboard_review_payload_plan",
                "dry_run_safety_boundary_plan",
                "permission_decision_runtime_dry_run_context",
            ],
        )
    )

    # Sprint 104.0 dashboard API contract consolidation foundation skill.
    registry.register(
        AuraSkill(
            name="aura_dashboard_api_contract_consolidation_foundation",
            description="Prepare planner-only, metadata-only, and contract-blueprint-only Dashboard API Contract Consolidation Foundation without starting API/web servers, binding ports, handling requests, probing networks, reading/writing runtime files, dispatching actions, executing tools/commands, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "dashboard_api_contract_consolidation_status",
                "api_contract_inventory_plan",
                "endpoint_schema_alignment_plan",
                "request_response_contract_plan",
                "permission_contract_mapping_plan",
                "dashboard_status_payload_plan",
                "error_response_contract_plan",
                "mock_api_boundary_plan",
                "frontend_backend_contract_boundary_plan",
                "contract_validation_checklist_plan",
                "dashboard_api_contract_consolidation_context",
            ],
        )
    )

    # Sprint 103.0 local service start proposal review foundation skill.
    registry.register(
        AuraSkill(
            name="aura_local_service_start_proposal_review_foundation",
            description="Prepare planner-only, metadata-only, and proposal-review-only AURA Local Service Start Proposal Review Foundation for future local service start proposals without starting services, binding ports, probing networks, changing permissions, dispatching actions, executing tools or commands, connecting ORION, writing memory, or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "local_service_start_proposal_review_status",
                "service_start_candidate_inventory_plan",
                "service_start_preflight_requirement_plan",
                "port_binding_review_plan",
                "process_launch_boundary_plan",
                "permission_requirement_plan",
                "risk_classification_plan",
                "rollback_kill_switch_plan",
                "audit_event_plan",
                "user_approval_decision_plan",
                "local_service_start_proposal_review_context",
            ],
        )
    )

    # Sprint 102.0 safe runtime configuration profile foundation skill.
    registry.register(
        AuraSkill(
            name="aura_safe_runtime_configuration_profile_foundation",
            description="Prepare planner-only, metadata-only, and configuration-blueprint-only AURA Safe Runtime Configuration Profile Foundation for profile types, runtime mode policies, service boundaries, permission boundaries, file system boundaries, network boundaries, dry-run requirements, rollout guards, and configuration audit visibility without reading, writing, applying, or activating runtime config; starting services, launchers, web servers, API servers, websockets, or ORION clients; changing permissions; activating dry-run runtime; binding ports; probing networks; dispatching actions; executing tools or commands; writing memory; or performing git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "safe_runtime_configuration_profile_status",
                "configuration_profile_type_plan",
                "runtime_mode_policy_plan",
                "service_configuration_boundary_plan",
                "permission_configuration_boundary_plan",
                "file_system_configuration_boundary_plan",
                "network_configuration_boundary_plan",
                "dry_run_configuration_requirement_plan",
                "rollout_configuration_guard_plan",
                "configuration_audit_visibility_plan",
                "safe_runtime_configuration_profile_context",
                "safe_runtime_configuration_profile_blueprint_metadata",
            ],
        )
    )

    # Sprint 101.0 genesis runtime readiness baseline foundation skill.
    registry.register(
        AuraSkill(
            name="aura_genesis_runtime_readiness_baseline_foundation",
            description="Prepare planner-only, metadata-only, and readiness-blueprint-only AURA Genesis Runtime Readiness Baseline Foundation for readiness domains, runtime candidate classifications, dry-run prerequisites, permission requirement matrix, safety gate alignment, rollback and kill-switch readiness, audit and observability readiness, rollout phase recommendations, and Sprint 101-110 block alignment without activating runtime, dry-run mode, local services, config writes, permission changes, file runtime, network probes, action dispatch, command/tool execution, ORION handshake, memory writes, or git runtime.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "genesis_runtime_readiness_baseline_status",
                "readiness_domain_inventory_plan",
                "runtime_candidate_classification_plan",
                "dry_run_prerequisite_plan",
                "permission_requirement_matrix_plan",
                "safety_gate_alignment_plan",
                "rollback_and_kill_switch_readiness_plan",
                "audit_and_observability_readiness_plan",
                "rollout_phase_recommendation_plan",
                "block_101_110_alignment_plan",
                "genesis_runtime_readiness_baseline_context",
                "genesis_runtime_readiness_baseline_blueprint_metadata",
            ],
        )
    )

    # Sprint 100.0 review and stabilization foundation skill.
    registry.register(
        AuraSkill(
            name="aura_sprint_100_review_stabilization_foundation",
            description="Prepare planner-only, review-only, and checkpoint-blueprint-only AURA Sprint 100 Review & Stabilization Foundation for Sprint 91-100 checkpoint review, completed feature inventory, active vs foundation-only boundaries, runtime-zero safety checks, capability registry stabilization, documentation stabilization, unresolved future features, roadmap 101-110 seed planning, and Sprint 100 release readiness without executing runtime behavior, reading files, probing ports, mutating permissions, dispatching actions, invoking tools, writing memory, or changing system behavior.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "sprint_100_review_stabilization_status",
                "sprint_block_review_plan",
                "completed_feature_inventory_plan",
                "active_vs_foundation_boundary_plan",
                "runtime_zero_safety_check_plan",
                "capability_registry_stabilization_plan",
                "documentation_stabilization_plan",
                "unresolved_future_feature_plan",
                "roadmap_101_110_seed_plan",
                "sprint_100_release_readiness_plan",
                "sprint_100_review_stabilization_context",
                "sprint_100_review_stabilization_blueprint_metadata",
            ],
        )
    )

    # Sprint 99.0 pre-runtime security audit foundation skill.
    registry.register(
        AuraSkill(
            name="aura_pre_runtime_security_audit_foundation",
            description="Prepare planner-only, review-only, and audit-blueprint-only AURA Pre-Runtime Security Audit Foundation for security audit domains, runtime gate checks, permission boundary checks, file system safety checks, network surface checks, action execution safety checks, ORION boundary checks, audit visibility checks, and Sprint 100 stabilization readiness checks without executing security scans, reading files, probing ports, mutating gates, changing permissions, dispatching actions, executing commands, invoking tools, or changing runtime behavior.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "pre_runtime_security_audit_status",
                "security_audit_domain_plan",
                "runtime_gate_check_plan",
                "permission_boundary_check_plan",
                "file_system_safety_check_plan",
                "network_surface_check_plan",
                "action_execution_safety_check_plan",
                "orion_boundary_check_plan",
                "audit_visibility_check_plan",
                "stabilization_readiness_check_plan",
                "pre_runtime_security_audit_context",
                "pre_runtime_security_audit_blueprint_metadata",
            ],
        )
    )

    # Sprint 98.0 runtime action queue review layer foundation skill.
    registry.register(
        AuraSkill(
            name="aura_runtime_action_queue_review_layer_foundation",
            description="Prepare planner-only, review-only, and proposal-only AURA Runtime Action Queue Review Layer Foundation for action queue item blueprints, queue state blueprints, review priority rules, dependency/blocker contracts, permission link requirements, execution preflight check blueprints, approval/denial transition rules, timeout/expiry policies, runtime action audit visibility, and safety policy without creating runtime queue items, dispatching actions, executing actions, running plugins, writing files, executing commands, controlling desktop, invoking tools, or triggering ORION/local actions.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "runtime_action_queue_review_layer_status",
                "action_queue_item_blueprint_plan",
                "queue_state_blueprint_plan",
                "review_priority_rule_plan",
                "dependency_blocker_contract_plan",
                "permission_link_requirement_plan",
                "execution_preflight_check_blueprint_plan",
                "approval_denial_transition_rule_plan",
                "timeout_expiry_policy_plan",
                "runtime_action_audit_visibility_plan",
                "runtime_action_queue_review_layer_context",
                "runtime_action_queue_review_layer_blueprint_metadata",
            ],
        )
    )

    # Sprint 97.0 controlled file write approval draft foundation skill.
    registry.register(
        AuraSkill(
            name="aura_controlled_file_write_approval_draft_foundation",
            description="Prepare planner-only and draft-only AURA Controlled File Write Approval Draft Foundation for file write proposal drafts, target path policy planning, diff preview contract planning, overwrite rule planning, backup requirement planning, approval checklist planning, rollback note planning, file write audit visibility planning, and file write safety policy without reading, writing, modifying, deleting, backing up, overwriting, rolling back files, granting approvals, or executing commands.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "controlled_file_write_approval_draft_status",
                "file_write_proposal_draft_plan",
                "target_path_policy_plan",
                "diff_preview_contract_plan",
                "overwrite_rule_plan",
                "backup_requirement_plan",
                "approval_checklist_plan",
                "rollback_note_plan",
                "file_write_audit_visibility_plan",
                "file_write_safety_policy_plan",
                "controlled_file_write_approval_draft_context",
                "controlled_file_write_approval_draft_blueprint_metadata",
            ],
        )
    )

    # Sprint 96.0 safe local web runtime gate foundation skill.
    registry.register(
        AuraSkill(
            name="aura_safe_local_web_runtime_gate_foundation",
            description="Prepare planner-only and pre-runtime AURA Safe Local Web Runtime Gate Foundation for localhost binding policy planning, port policy planning, permission requirement planning, runtime preflight check planning, start/stop proposal contract planning, route boundary policy planning, static asset boundary policy planning, kill switch policy planning, and web runtime audit visibility planning without starting servers, binding ports, creating routes, serving files, launching browsers, opening websockets, handling API requests, or exposing external networks.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "safe_local_web_runtime_gate_status",
                "localhost_binding_policy_plan",
                "port_policy_plan",
                "permission_requirement_plan",
                "runtime_preflight_check_plan",
                "start_stop_proposal_contract_plan",
                "route_boundary_policy_plan",
                "static_asset_boundary_policy_plan",
                "kill_switch_policy_plan",
                "web_runtime_audit_visibility_plan",
                "safe_local_web_runtime_gate_context",
                "safe_local_web_runtime_gate_blueprint_metadata",
            ],
        )
    )

    # Sprint 95.0 chat session persistence planner foundation skill.
    registry.register(
        AuraSkill(
            name="aura_chat_session_persistence_planner_foundation",
            description="Prepare planner-only AURA Chat Session Persistence Planner Foundation for session record blueprint planning, storage boundary blueprint planning, retention policy blueprint planning, privacy redaction rule planning, session lifecycle blueprint planning, recovery index blueprint planning, export/migration note planning, audit visibility field planning, and chat persistence safety policy without creating chat runtime, session runtime, database runtime, file write runtime, memory write runtime, recovery runtime, exports, archives, deletes, or runtime persistence.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "chat_session_persistence_planner_status",
                "session_record_blueprint_plan",
                "storage_boundary_blueprint_plan",
                "retention_policy_blueprint_plan",
                "privacy_redaction_rule_plan",
                "session_lifecycle_blueprint_plan",
                "recovery_index_blueprint_plan",
                "export_migration_note_plan",
                "chat_persistence_safety_policy_plan",
                "chat_session_persistence_context",
                "chat_session_persistence_status_packet",
                "chat_session_persistence_blueprint_metadata",
            ],
        )
    )

    # Sprint 94.0 permission request review queue foundation skill.
    registry.register(
        AuraSkill(
            name="aura_permission_request_review_queue_foundation",
            description="Prepare planner-only AURA Permission Request Review Queue Foundation for permission request blueprint planning, queue state blueprint planning, review packet field planning, permission scope boundary planning, decision proposal contract planning, reviewer checklist planning, audit visibility field planning, and permission request safety policy without creating, collecting, persisting, mutating, submitting, reviewing, granting, denying, resolving, activating, revoking, or executing runtime permissions/actions.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "permission_request_review_queue_status",
                "permission_request_blueprint_plan",
                "queue_state_blueprint_plan",
                "review_packet_field_plan",
                "permission_scope_boundary_plan",
                "decision_proposal_contract_plan",
                "reviewer_checklist_plan",
                "audit_visibility_field_plan",
                "permission_request_safety_policy_plan",
                "permission_request_review_queue_context",
                "permission_request_review_queue_status_packet",
                "permission_review_queue_blueprint_metadata",
            ],
        )
    )

    # Sprint 93.0 control center data aggregator foundation skill.
    registry.register(
        AuraSkill(
            name="aura_control_center_data_aggregator_foundation",
            description="Prepare planner-only AURA Control Center Data Aggregator Foundation for aggregation packet catalog planning, ATLAS core packet planning, ORION client packet planning, client bridge packet planning, dashboard view packet planning, permission scope packet planning, health snapshot packet planning, audit event visibility packet planning, and data aggregator safety policy without fetching runtime data, connecting to ORION, creating client pairings, sending or receiving heartbeats, fetching or forwarding audit events, rendering dashboard views, starting API/web/client runtime, activating voice/screen/avatar/3D environment/OBS/game/Blender/VS Code/local action bridges, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "control_center_data_aggregator_status",
                "aggregator_packet_catalog_plan",
                "atlas_core_packet_plan",
                "orion_client_packet_plan",
                "client_bridge_packet_plan",
                "dashboard_view_packet_plan",
                "permission_scope_packet_plan",
                "health_snapshot_packet_plan",
                "audit_event_visibility_packet_plan",
                "data_aggregator_safety_policy_plan",
                "control_center_data_aggregator_context",
                "atlas_orion_dashboard_packet_metadata",
            ],
        )
    )

    # Sprint 92.0 local console API schema foundation skill.
    registry.register(
        AuraSkill(
            name="aura_local_console_api_schema_foundation",
            description="Prepare planner-only AURA Local Console API Schema Foundation for API schema catalog planning, endpoint blueprint planning, response envelope planning, request schema blueprint planning, validation rule planning, permission boundary schema planning, error contract planning, schema versioning planning, and API schema safety policy without starting API runtime, creating API routes, handling requests, serving responses, binding ports, starting HTTP/web server runtime, fetching runtime data, running runtime validation, serialization, error emission, frontend/backend runtime, chat/session/plugin/permission/service/launcher/action runtime, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "local_console_api_schema_status",
                "api_schema_catalog_plan",
                "endpoint_blueprint_plan",
                "response_envelope_plan",
                "request_schema_blueprint_plan",
                "validation_rule_plan",
                "permission_boundary_schema_plan",
                "error_contract_plan",
                "schema_versioning_plan",
                "api_schema_safety_policy_plan",
                "local_console_api_schema_context",
                "control_center_api_contract_metadata",
            ],
        )
    )

    # Sprint 91.0 local console static prototype foundation skill.
    registry.register(
        AuraSkill(
            name="aura_local_console_static_prototype_foundation",
            description="Prepare planner-only AURA Local Console Static Prototype Foundation for static prototype structure planning, static page blueprint planning, static asset blueprint planning, panel layout blueprint planning, route-to-static-page mapping planning, data placeholder contract planning, theme token blueprint planning, accessibility blueprint planning, and static prototype safety policy without starting web server runtime, serving static files, binding ports, opening browsers, creating runtime routes, running frontend/backend/API runtime, activating chat/session/plugin/permission/service/launcher/action runtime, creating static assets at runtime, file operations, command execution, dependency install, package download, internet/network action, tool execution, memory write, desktop control, git action, external action execution, or real tool execution.",
            role="partner",
            permission_action="read_project",
            status="online",
            capabilities=[
                "local_console_static_prototype_status",
                "static_prototype_structure_plan",
                "static_page_blueprint_plan",
                "static_asset_blueprint_plan",
                "panel_layout_blueprint_plan",
                "route_static_mapping_plan",
                "data_placeholder_contract_plan",
                "theme_token_blueprint_plan",
                "accessibility_blueprint_plan",
                "static_prototype_safety_policy_plan",
                "local_console_static_prototype_context",
                "control_center_static_visibility_metadata",
            ],
        )
    )

    return registry
