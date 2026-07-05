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

    return registry
