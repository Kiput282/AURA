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
            name="chat",
            description="Talk with the user using AURA's companion personality.",
            role="companion",
            permission_action="think",
            status="online",
            capabilities=["conversation", "identity", "language_control"],
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
            description="Inspect project files, show project summary, and prepare safe file-related assistance.",
            role="coder",
            permission_action="read_project",
            status="online",
            capabilities=["file_review", "project_analysis", "project_summary", "safe_file_read"],
        )
    )

    registry.register(
        AuraSkill(
            name="app_launcher",
            description="Open applications, browser, or files when explicitly requested.",
            role="action",
            permission_action="open_app",
            status="planned",
            capabilities=["open_app", "open_browser", "open_file"],
        )
    )

    registry.register(
        AuraSkill(
            name="vision_foundation",
            description="Show AURA vision foundation status and placeholder vision providers.",
            role="vision",
            permission_action="think",
            status="online",
            capabilities=["vision_status", "screen_placeholder", "camera_placeholder"],
        )
    )

    registry.register(
        AuraSkill(
            name="screen_analyzer",
            description="Future screen analysis once screen runtime is connected.",
            role="vision",
            permission_action="screen_analyze",
            status="foundation",
            capabilities=["screen_analysis", "visual_context", "screen_permission"],
        )
    )

    registry.register(
        AuraSkill(
            name="camera_analyzer",
            description="Future camera and environment analysis once camera runtime is connected.",
            role="vision",
            permission_action="camera_analyze",
            status="foundation",
            capabilities=["camera_context", "environment_analysis", "camera_permission"],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_foundation",
            description="Show AURA voice foundation status and placeholder voice providers.",
            role="voice",
            permission_action="think",
            status="online",
            capabilities=["voice_status", "stt_placeholder", "tts_placeholder"],
        )
    )

    registry.register(
        AuraSkill(
            name="voice_interaction",
            description="Future voice input and output once STT/TTS providers are connected.",
            role="voice",
            permission_action="microphone_listen",
            status="foundation",
            capabilities=["speech_to_text", "text_to_speech", "voice_mode", "microphone_permission"],
        )
    )

    registry.register(
        AuraSkill(
            name="avatar_control",
            description="Control AURA's 3D avatar, expression, gesture, and body state.",
            role="avatar",
            permission_action="prepare_file",
            status="planned",
            capabilities=["vrm", "expression", "gesture", "avatar_state"],
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
