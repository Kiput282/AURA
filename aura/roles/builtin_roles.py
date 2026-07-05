from aura.roles.role import AuraRole
from aura.roles.role_registry import RoleRegistry


def build_builtin_role_registry() -> RoleRegistry:
    """
    Builds AURA's default internal role registry.

    Current phase:
    - companion, memory, and project_manager have active foundations
    - other roles are planned for future development
    """

    registry = RoleRegistry()

    registry.register(
        AuraRole(
            name="companion",
            description="Main conversational personality and user-facing partner role.",
            provider="ollama",
            model="llama3.2",
            status="online",
            capabilities=[
                "chat",
                "identity",
                "conversation",
                "language_control",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="memory",
            description="Memory retrieval, recall, relevance, deletion, and protected memory handling.",
            provider="internal",
            model="keyword_memory",
            status="online",
            capabilities=[
                "memory_recall",
                "memory_search",
                "memory_list",
                "memory_count",
                "memory_delete",
                "protected_memory",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="project_manager",
            description="Project progress tracking, roadmap awareness, and development journal support.",
            provider="internal",
            model="project_journal",
            status="foundation",
            capabilities=[
                "project_journal",
                "progress_tracking",
                "roadmap_awareness",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="coder",
            description="Coding, debugging, software architecture, project inspection, and technical reasoning.",
            provider="ollama",
            model="llama3.2",
            status="foundation",
            capabilities=[
                "coding",
                "debugging",
                "architecture",
                "code_review",
                "project_inspection",
                "safe_file_read",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="creative",
            description="Creative generation for images, 3D assets, characters, stories, and concepts.",
            provider="planned",
            model="creative_model",
            status="planned",
            capabilities=[
                "image_generation",
                "3d_concept",
                "asset_concept",
                "creative_writing",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="vision",
            description="Vision foundation, screen analysis, image understanding, camera, and environment awareness.",
            provider="internal",
            model="vision_manager",
            status="foundation",
            capabilities=[
                "vision_status",
                "screen_placeholder",
                "camera_placeholder",
                "screen_analysis",
                "image_understanding",
                "camera_context",
                "environment_analysis",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="voice",
            description="Voice foundation, speech-to-text, text-to-speech, and voice interaction.",
            provider="internal",
            model="voice_manager",
            status="foundation",
            capabilities=[
                "voice_status",
                "stt_placeholder",
                "tts_placeholder",
                "speech_to_text",
                "text_to_speech",
                "voice_interaction",
                "voice_mode",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="action",
            description="Tool usage, plugin calling, safe task execution, permission checks, and automation planning.",
            provider="internal",
            model="permission_manager",
            status="foundation",
            capabilities=[
                "permission_check",
                "action_safety",
                "plugin_action_interface",
                "tool_calling",
                "plugin_control",
                "task_planning",
                "safe_actions",
                "desktop_bridge",
                "desktop_action_proposal",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="avatar",
            description="3D avatar, VRM/VRoid, expressions, gestures, and digital body control.",
            provider="planned",
            model="avatar_model",
            status="planned",
            capabilities=[
                "avatar_control",
                "vrm_control",
                "expression_control",
                "gesture_control",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="gaming",
            description="Gaming companion, game context support, and sandbox game interaction.",
            provider="planned",
            model="gaming_model",
            status="planned",
            capabilities=[
                "gaming_companion",
                "sandbox_interaction",
                "game_context",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="streaming",
            description="Livestream assistant, OBS support, audience interaction, and performance mode.",
            provider="planned",
            model="streaming_model",
            status="planned",
            capabilities=[
                "livestream_assistant",
                "obs_support",
                "chat_reaction",
                "singing_mode",
            ],
        )
    )

    registry.register(
        AuraRole(
            name="motion",
            description="Hand tracking, body tracking, pose commands, and motion capture support.",
            provider="planned",
            model="motion_model",
            status="planned",
            capabilities=[
                "hand_tracking",
                "body_tracking",
                "motion_capture",
                "pose_control",
            ],
        )
    )

    return registry
