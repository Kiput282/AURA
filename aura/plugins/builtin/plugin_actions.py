from aura.plugins.plugin_action import PluginAction
from aura.plugins.plugin_action_registry import PluginActionRegistry


def build_builtin_plugin_action_registry() -> PluginActionRegistry:
    """
    Builds AURA's built-in plugin action registry.

    Current phase:
    - actions are metadata only
    - permission checks are active
    - execution will be added in a later sprint
    """

    registry = PluginActionRegistry()

    registry.register(
        PluginAction(
            name="tool.sandbox_status",
            plugin="tool_sandbox",
            description="Show tool execution sandbox status.",
            permission_action="sandbox_check",
            status="online",
            skill="tool_sandbox",
        )
    )

    registry.register(
        PluginAction(
            name="tool.sandbox_policy",
            plugin="tool_sandbox",
            description="Show sandbox allowlist and blocked command policy.",
            permission_action="sandbox_check",
            status="online",
            skill="tool_sandbox",
        )
    )

    registry.register(
        PluginAction(
            name="tool.sandbox_check",
            plugin="tool_sandbox",
            description="Check whether a command is allowed by the sandbox policy without executing it.",
            permission_action="sandbox_check",
            status="online",
            skill="tool_sandbox",
        )
    )

    registry.register(
        PluginAction(
            name="tool.sandbox_dry_run",
            plugin="tool_sandbox",
            description="Prepare a dry-run command execution plan without executing the command.",
            permission_action="sandbox_dry_run",
            status="online",
            skill="tool_sandbox",
        )
    )

    registry.register(
        PluginAction(
            name="tool.sandbox_execute",
            plugin="tool_sandbox",
            description="Future real sandbox command execution with confirmation. Disabled for now.",
            permission_action="sandbox_execute",
            status="foundation",
            skill="tool_sandbox",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.alpha_status",
            plugin="desktop",
            description="Show Desktop Assistant Alpha status.",
            permission_action="read_project",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.action_plan",
            plugin="desktop",
            description="Prepare a safe desktop action plan without executing it.",
            permission_action="think",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.open_app_plan",
            plugin="desktop",
            description="Prepare an open app plan without opening the application.",
            permission_action="open_app",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.open_browser_plan",
            plugin="desktop",
            description="Prepare an open browser plan without opening the browser.",
            permission_action="open_browser",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.open_file_plan",
            plugin="desktop",
            description="Prepare an open file plan without opening the file.",
            permission_action="open_file",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.workspace_context",
            plugin="desktop",
            description="Show read-only desktop workspace context.",
            permission_action="read_project",
            status="online",
            skill="desktop_assistant_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.status",
            plugin="desktop",
            description="Show desktop bridge foundation status.",
            permission_action="think",
            status="online",
            skill="desktop_bridge",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.capabilities",
            plugin="desktop",
            description="List desktop bridge capabilities.",
            permission_action="think",
            status="online",
            skill="desktop_bridge",
        )
    )

    registry.register(
        PluginAction(
            name="desktop.action",
            plugin="desktop",
            description="Prepare a desktop action proposal without executing it.",
            permission_action="think",
            status="online",
            skill="desktop_bridge",
        )
    )

    registry.register(
        PluginAction(
            name="model.router_status",
            plugin="model_router",
            description="Show model router foundation status.",
            permission_action="think",
            status="online",
            skill="model_router",
        )
    )

    registry.register(
        PluginAction(
            name="model.router_routes",
            plugin="model_router",
            description="List model routes for AURA roles and tasks.",
            permission_action="think",
            status="online",
            skill="model_router",
        )
    )

    registry.register(
        PluginAction(
            name="model.router_select",
            plugin="model_router",
            description="Select a recommended model route without switching real runtimes.",
            permission_action="think",
            status="online",
            skill="model_router",
        )
    )

    registry.register(
        PluginAction(
            name="core.loop_status",
            plugin="core",
            description="Show AURA alpha core loop status.",
            permission_action="think",
            status="online",
            skill="core_loop",
        )
    )

    registry.register(
        PluginAction(
            name="core.loop_run",
            plugin="core",
            description="Run AURA alpha core loop and return a safe response without executing external actions.",
            permission_action="think",
            status="online",
            skill="core_loop",
        )
    )

    registry.register(
        PluginAction(
            name="core.loop_trace",
            plugin="core",
            description="Trace AURA alpha core loop steps without executing external actions.",
            permission_action="think",
            status="online",
            skill="core_loop",
        )
    )

    registry.register(
        PluginAction(
            name="system.status",
            plugin="system",
            description="Show unified AURA system status.",
            permission_action="read_project",
            status="online",
            skill="system_status",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.status",
            plugin="file_ops",
            description="Show AURA Safe File Operation Planner status.",
            permission_action="read_project",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.read_plan",
            plugin="file_ops",
            description="Prepare a metadata-only safe file read plan without opening or reading files automatically.",
            permission_action="read_project",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.write_plan",
            plugin="file_ops",
            description="Prepare a safe file write proposal without writing files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.edit_plan",
            plugin="file_ops",
            description="Prepare a safe file edit proposal without editing files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.move_copy_delete_risk_review",
            plugin="file_ops",
            description="Prepare a safe move/copy/delete risk review without moving, copying, or deleting files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.checklist",
            plugin="file_ops",
            description="Prepare a safe file operation checklist requiring explicit confirmation before real file actions.",
            permission_action="prepare_file",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="file_ops.context",
            plugin="file_ops",
            description="Show Safe File Operation Planner context without reading, opening, writing, editing, moving, copying, deleting files, or executing commands.",
            permission_action="read_project",
            status="online",
            skill="safe_file_operation_planner",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.status",
            plugin="local_task",
            description="Show AURA Local Task Planner Alpha status.",
            permission_action="read_project",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.intent_plan",
            plugin="local_task",
            description="Prepare a safe local task intent plan without executing commands, writing files, opening apps, or performing desktop actions.",
            permission_action="prepare_file",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.breakdown_plan",
            plugin="local_task",
            description="Prepare a safe local task breakdown plan without executing commands or writing files.",
            permission_action="prepare_file",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.risk_review",
            plugin="local_task",
            description="Prepare a safe local task risk review for file, command, app, desktop, and external action risks.",
            permission_action="prepare_file",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.execution_checklist",
            plugin="local_task",
            description="Prepare a safe local task execution checklist requiring explicit confirmation before real actions.",
            permission_action="prepare_file",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="local_task.context",
            plugin="local_task",
            description="Show Local Task Planner Alpha context without executing commands, writing files, opening apps, or performing desktop actions.",
            permission_action="read_project",
            status="online",
            skill="local_task_planner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="creative.assistant_status",
            plugin="creative",
            description="Show AURA Creative Assistant Foundation status.",
            permission_action="read_project",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.brief_plan",
            plugin="creative",
            description="Prepare a safe creative brief plan without generating images or writing files.",
            permission_action="prepare_file",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.character_concept_plan",
            plugin="creative",
            description="Prepare a safe character concept plan without generating images, changing avatar state, or writing files.",
            permission_action="prepare_file",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.visual_asset_plan",
            plugin="creative",
            description="Prepare a safe visual asset plan without opening media files or writing assets.",
            permission_action="prepare_file",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.content_idea_plan",
            plugin="creative",
            description="Prepare safe creative content ideas without posting, opening apps, or executing commands.",
            permission_action="prepare_file",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.review_plan",
            plugin="creative",
            description="Prepare a safe creative review plan without opening media files or editing assets.",
            permission_action="prepare_file",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="creative.context",
            plugin="creative",
            description="Prepare creative assistant context without generating images, opening media files, writing files, or executing commands.",
            permission_action="read_project",
            status="online",
            skill="creative_assistant_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.status",
            plugin="project_intent",
            description="Show AURA Project Intent Planner status.",
            permission_action="read_project",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.summary",
            plugin="project_intent",
            description="Prepare a read-only project intent summary without writing files, memory, or journal entries.",
            permission_action="read_project",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.goal_plan",
            plugin="project_intent",
            description="Prepare a safety-aware project goal plan without executing actions.",
            permission_action="prepare_file",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.sprint_plan",
            plugin="project_intent",
            description="Prepare a sprint intent plan without writing files, memory, or journal entries.",
            permission_action="prepare_file",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.next_actions",
            plugin="project_intent",
            description="Prepare next action candidates without executing them.",
            permission_action="prepare_file",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="project_intent.context",
            plugin="project_intent",
            description="Prepare project intent context without writing files, memory, journal, or commands.",
            permission_action="read_project",
            status="online",
            skill="project_intent_planner",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.link_status",
            plugin="workspace_memory",
            description="Show AURA Workspace Memory Link status.",
            permission_action="read_memory",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.summary",
            plugin="workspace_memory",
            description="Prepare a read-only workspace memory summary without writing memory.",
            permission_action="read_memory",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.candidates",
            plugin="workspace_memory",
            description="Prepare project memory candidates from workspace context without writing memory.",
            permission_action="prepare_file",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.file_candidates",
            plugin="workspace_memory",
            description="Prepare important file memory candidates without writing memory or files.",
            permission_action="prepare_file",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.milestone_candidates",
            plugin="workspace_memory",
            description="Prepare recent milestone memory candidates without writing memory or journal entries.",
            permission_action="prepare_file",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="workspace_memory.context",
            plugin="workspace_memory",
            description="Prepare workspace memory link context without writing memory, journal, files, or commands.",
            permission_action="read_memory",
            status="online",
            skill="workspace_memory_link",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.safety_status",
            plugin="streaming",
            description="Show AURA Streaming Safety Foundation status.",
            permission_action="read_project",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.context_plan",
            plugin="streaming",
            description="Prepare a safe streaming context plan without reading live chat, capturing screen, or opening apps.",
            permission_action="prepare_file",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.chat_safety_plan",
            plugin="streaming",
            description="Prepare a safe live chat plan without reading chat or sending messages automatically.",
            permission_action="prepare_file",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.content_boundary_plan",
            plugin="streaming",
            description="Prepare safe content boundaries for stream topics, commentary, and avatar behavior.",
            permission_action="prepare_file",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.privacy_plan",
            plugin="streaming",
            description="Prepare a privacy checklist for desktop or stream setup without capturing screen.",
            permission_action="prepare_file",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.moderation_plan",
            plugin="streaming",
            description="Prepare moderation notes and community rules without performing moderation actions.",
            permission_action="prepare_file",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming.safety_context",
            plugin="streaming",
            description="Prepare streaming safety context without live chat access, screen capture, message sending, moderation action, file writing, or command execution.",
            permission_action="read_project",
            status="foundation",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.companion_status",
            plugin="game",
            description="Show AURA Game Companion Foundation status.",
            permission_action="read_project",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.session_plan",
            plugin="game",
            description="Prepare a safe game session companion plan without reading screen or controlling input.",
            permission_action="prepare_file",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.strategy_plan",
            plugin="game",
            description="Prepare a safe game strategy plan without live screen reading or command execution.",
            permission_action="prepare_file",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.streaming_plan",
            plugin="game",
            description="Prepare streaming-safe game companion notes without capture, voice output, or external actions.",
            permission_action="prepare_file",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.coaching_plan",
            plugin="game",
            description="Prepare a safe game coaching/practice plan without input control or screen reading.",
            permission_action="prepare_file",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="game.context",
            plugin="game",
            description="Prepare game companion context without reading screen, controlling input, opening apps, writing files, or executing commands.",
            permission_action="read_project",
            status="foundation",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="expression.language_status",
            plugin="expression",
            description="Show AURA Expression Language status.",
            permission_action="read_project",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.state",
            plugin="expression",
            description="Show AURA internal expression state, moods, emotion tags, voice tones, avatar expressions, gestures, and response styles.",
            permission_action="read_project",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.plan",
            plugin="expression",
            description="Prepare a safe expression plan with mood, emotion tags, voice tone, avatar expression, gesture, and response style hints.",
            permission_action="prepare_file",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.voice_hint",
            plugin="expression",
            description="Prepare a safe voice tone hint without playing audio.",
            permission_action="prepare_file",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.avatar_hint",
            plugin="expression",
            description="Prepare a safe avatar expression hint without changing or rendering a real avatar.",
            permission_action="prepare_file",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.gesture_hint",
            plugin="expression",
            description="Prepare a safe gesture hint without changing or rendering a real avatar.",
            permission_action="prepare_file",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="expression.context",
            plugin="expression",
            description="Prepare expression language context without voice output, avatar changes, file writing, or command execution.",
            permission_action="read_project",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="media.understanding_status",
            plugin="media",
            description="Show AURA Media Understanding Foundation status.",
            permission_action="read_project",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.asset_summary",
            plugin="media",
            description="Show metadata-only summary of safe visible media assets.",
            permission_action="read_project",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.image_plan",
            plugin="media",
            description="Prepare a safe image description plan without opening files or reading pixels.",
            permission_action="prepare_file",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.texture_reference_plan",
            plugin="media",
            description="Prepare a safe texture reference plan without reading or writing texture files.",
            permission_action="prepare_file",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.thumbnail_review_plan",
            plugin="media",
            description="Prepare a safe thumbnail/banner review plan without opening or editing images.",
            permission_action="prepare_file",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.video_plan",
            plugin="media",
            description="Prepare a safe video/audio understanding plan without decoding media or executing ffmpeg.",
            permission_action="prepare_file",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.context",
            plugin="media",
            description="Prepare media understanding context without opening files, reading pixels, writing files, or executing commands.",
            permission_action="read_project",
            status="foundation",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.bridge_status",
            plugin="blender",
            description="Show AURA Blender Bridge Foundation status.",
            permission_action="read_project",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.scene_plan",
            plugin="blender",
            description="Prepare a safe Blender scene plan without opening Blender or writing files.",
            permission_action="prepare_file",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.asset_plan",
            plugin="blender",
            description="Prepare a safe Blender asset plan without creating or modifying assets.",
            permission_action="prepare_file",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.texture_plan",
            plugin="blender",
            description="Prepare a safe Blender texture/material/shader plan without writing texture files.",
            permission_action="prepare_file",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.rigging_plan",
            plugin="blender",
            description="Prepare a safe Blender rigging plan without modifying rigs.",
            permission_action="prepare_file",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.animation_plan",
            plugin="blender",
            description="Prepare a safe Blender animation plan without writing animation data.",
            permission_action="prepare_file",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="blender.context",
            plugin="blender",
            description="Prepare Blender bridge context for future reasoning without executing actions.",
            permission_action="read_project",
            status="foundation",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="workspace.awareness_status",
            plugin="workspace",
            description="Show AURA Workspace Awareness status.",
            permission_action="read_project",
            status="online",
            skill="workspace_awareness",
        )
    )

    registry.register(
        PluginAction(
            name="workspace.map",
            plugin="workspace",
            description="Show a read-only AURA workspace map.",
            permission_action="read_project",
            status="online",
            skill="workspace_awareness",
        )
    )

    registry.register(
        PluginAction(
            name="workspace.context",
            plugin="workspace",
            description="Prepare AURA workspace context without writing or executing actions.",
            permission_action="read_project",
            status="online",
            skill="workspace_awareness",
        )
    )

    registry.register(
        PluginAction(
            name="workspace.current_state",
            plugin="workspace",
            description="Show current AURA workspace state.",
            permission_action="read_project",
            status="online",
            skill="workspace_awareness",
        )
    )

    registry.register(
        PluginAction(
            name="workspace.important_files",
            plugin="workspace",
            description="List important AURA project files and why they matter.",
            permission_action="read_project",
            status="online",
            skill="workspace_awareness",
        )
    )

    registry.register(
        PluginAction(
            name="partner.alpha_status",
            plugin="partner",
            description="Show AURA Partner Alpha status.",
            permission_action="read_project",
            status="online",
            skill="partner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="partner.context",
            plugin="partner",
            description="Prepare unified AURA Partner Alpha context without writing or executing actions.",
            permission_action="read_project",
            status="online",
            skill="partner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="partner.readiness",
            plugin="partner",
            description="Show AURA Partner Alpha readiness report.",
            permission_action="read_project",
            status="online",
            skill="partner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="partner.next_step",
            plugin="partner",
            description="Suggest next safe AURA development steps from Partner Alpha context.",
            permission_action="suggest",
            status="online",
            skill="partner_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="awakening.status",
            plugin="awakening",
            description="Show AURA Awakening Alpha readiness status.",
            permission_action="think",
            status="online",
            skill="awakening_status",
        )
    )

    registry.register(
        PluginAction(
            name="echo.echo",
            plugin="echo",
            description="Echo a test message.",
            permission_action="think",
            status="online",
            skill="chat",
        )
    )

    registry.register(
        PluginAction(
            name="memory.reflection_status",
            plugin="memory_reflection",
            description="Show Memory Reflection System status.",
            permission_action="read_memory",
            status="online",
            skill="memory_reflection",
        )
    )

    registry.register(
        PluginAction(
            name="memory.reflect",
            plugin="memory_reflection",
            description="Create a read-only reflection summary from memory and project journal.",
            permission_action="read_memory",
            status="online",
            skill="memory_reflection",
        )
    )

    registry.register(
        PluginAction(
            name="memory.insights",
            plugin="memory_reflection",
            description="Generate read-only project insights from memory and journal.",
            permission_action="read_memory",
            status="online",
            skill="memory_reflection",
        )
    )

    registry.register(
        PluginAction(
            name="memory.reflection_context",
            plugin="memory_reflection",
            description="Prepare reflection context for future reasoning without writing memory.",
            permission_action="read_memory",
            status="online",
            skill="memory_reflection",
        )
    )

    registry.register(
        PluginAction(
            name="memory.recall",
            plugin="memory",
            description="Recall recent memories.",
            permission_action="read_project",
            status="online",
            skill="memory_recall",
        )
    )

    registry.register(
        PluginAction(
            name="memory.search",
            plugin="memory",
            description="Search relevant memories.",
            permission_action="read_project",
            status="online",
            skill="memory_search",
        )
    )

    registry.register(
        PluginAction(
            name="memory.manage",
            plugin="memory",
            description="Manage memories such as list, count, delete, pin, unpin, and importance.",
            permission_action="write_file",
            status="online",
            skill="memory_manage",
        )
    )

    registry.register(
        PluginAction(
            name="daily.briefing_status",
            plugin="daily_briefing",
            description="Show Daily Project Briefing status.",
            permission_action="read_project",
            status="online",
            skill="daily_project_briefing",
        )
    )

    registry.register(
        PluginAction(
            name="daily.briefing",
            plugin="daily_briefing",
            description="Create a read-only daily project briefing.",
            permission_action="read_project",
            status="online",
            skill="daily_project_briefing",
        )
    )

    registry.register(
        PluginAction(
            name="daily.briefing_compact",
            plugin="daily_briefing",
            description="Create a compact read-only daily project briefing.",
            permission_action="read_project",
            status="online",
            skill="daily_project_briefing",
        )
    )

    registry.register(
        PluginAction(
            name="daily.briefing_context",
            plugin="daily_briefing",
            description="Prepare daily briefing context for future reasoning without writing data.",
            permission_action="read_project",
            status="online",
            skill="daily_project_briefing",
        )
    )

    registry.register(
        PluginAction(
            name="journal.add",
            plugin="journal",
            description="Add a project journal entry.",
            permission_action="write_file",
            status="online",
            skill="project_journal",
        )
    )

    registry.register(
        PluginAction(
            name="journal.list",
            plugin="journal",
            description="List project journal entries.",
            permission_action="read_project",
            status="online",
            skill="project_journal",
        )
    )

    registry.register(
        PluginAction(
            name="context.preview",
            plugin="context",
            description="Build and preview a context packet.",
            permission_action="read_project",
            status="online",
            skill="context_preview",
        )
    )

    registry.register(
        PluginAction(
            name="roles.list",
            plugin="roles",
            description="List AURA internal roles.",
            permission_action="read_project",
            status="online",
            skill="role_list",
        )
    )

    registry.register(
        PluginAction(
            name="skills.list",
            plugin="skills",
            description="List AURA skills.",
            permission_action="read_project",
            status="online",
            skill="skill_registry",
        )
    )

    registry.register(
        PluginAction(
            name="action.request",
            plugin="action",
            description="Prepare a safe action request proposal without executing it.",
            permission_action="think",
            status="online",
            skill="action_request",
        )
    )

    registry.register(
        PluginAction(
            name="permissions.check",
            plugin="permissions",
            description="Check whether an action is allowed, requires confirmation, or is restricted.",
            permission_action="think",
            status="online",
            skill="permission_check",
        )
    )

    registry.register(
        PluginAction(
            name="project.code_status",
            plugin="project_coding",
            description="Show Project Coding Assistant v2 status.",
            permission_action="read_project",
            status="online",
            skill="project_coding_v2",
        )
    )

    registry.register(
        PluginAction(
            name="project.code_map",
            plugin="project_coding",
            description="Build a read-only AST-based code map of safe Python project files.",
            permission_action="read_project",
            status="online",
            skill="project_coding_v2",
        )
    )

    registry.register(
        PluginAction(
            name="project.code_inspect",
            plugin="project_coding",
            description="Inspect a project code file and summarize imports, classes, functions, and methods.",
            permission_action="read_project",
            status="online",
            skill="project_coding_v2",
        )
    )

    registry.register(
        PluginAction(
            name="project.code_plan",
            plugin="project_coding",
            description="Prepare a safe patch plan without modifying files.",
            permission_action="read_project",
            status="online",
            skill="project_coding_v2",
        )
    )

    registry.register(
        PluginAction(
            name="project.code_safety",
            plugin="project_coding",
            description="Check command safety through the tool sandbox for coding workflows.",
            permission_action="sandbox_check",
            status="online",
            skill="project_coding_v2",
        )
    )

    registry.register(
        PluginAction(
            name="project.map",
            plugin="project",
            description="Show a safe high-level project map.",
            permission_action="read_project",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="project.inspect",
            plugin="project",
            description="Inspect a safe file or directory inside the project.",
            permission_action="read_project",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="project.find",
            plugin="project",
            description="Search for a keyword in safe project files.",
            permission_action="read_project",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="project.summary",
            plugin="project",
            description="Show safe project summary and file counts.",
            permission_action="read_project",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="project.files",
            plugin="project",
            description="List safe visible project files.",
            permission_action="read_project",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="project.read_file",
            plugin="project",
            description="Read a safe project file inside the project root.",
            permission_action="read_file",
            status="online",
            skill="file_project_assist",
        )
    )

    registry.register(
        PluginAction(
            name="provider.check",
            plugin="provider",
            description="Check reasoning provider status.",
            permission_action="read_project",
            status="online",
            skill="provider_check",
        )
    )

    registry.register(
        PluginAction(
            name="app.open",
            plugin="app_launcher",
            description="Prepare opening an application through the desktop bridge.",
            permission_action="open_app",
            status="foundation",
            skill="app_launcher",
        )
    )

    registry.register(
        PluginAction(
            name="browser.open",
            plugin="app_launcher",
            description="Prepare opening a browser or URL through the desktop bridge.",
            permission_action="open_browser",
            status="foundation",
            skill="app_launcher",
        )
    )

    registry.register(
        PluginAction(
            name="file.open",
            plugin="app_launcher",
            description="Prepare opening a file through the desktop bridge.",
            permission_action="open_file",
            status="foundation",
            skill="app_launcher",
        )
    )

    registry.register(
        PluginAction(
            name="vision.runtime_alpha_status",
            plugin="vision",
            description="Show Vision Runtime Alpha status.",
            permission_action="read_project",
            status="online",
            skill="vision_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="vision.screen_plan",
            plugin="vision",
            description="Prepare a safe screen analysis plan without capturing the screen.",
            permission_action="suggest",
            status="online",
            skill="vision_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="vision.camera_plan",
            plugin="vision",
            description="Prepare a safe camera analysis plan without accessing the camera.",
            permission_action="suggest",
            status="online",
            skill="vision_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="vision.runtime_alpha_context",
            plugin="vision",
            description="Prepare Vision Runtime Alpha context without accessing screen or camera.",
            permission_action="read_project",
            status="online",
            skill="vision_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="vision.runtime_status",
            plugin="vision",
            description="Show vision runtime planning status.",
            permission_action="think",
            status="online",
            skill="vision_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="vision.runtime_plan",
            plugin="vision",
            description="Show screen/camera/model runtime planning candidates and safety phases.",
            permission_action="think",
            status="online",
            skill="vision_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="vision.runtime_check",
            plugin="vision",
            description="Run passive vision runtime dependency checks without accessing screen or camera.",
            permission_action="think",
            status="online",
            skill="vision_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="vision.status",
            plugin="vision",
            description="Show vision foundation status.",
            permission_action="think",
            status="online",
            skill="vision_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="screen.analyze",
            plugin="vision",
            description="Prepare screen analysis when vision runtime is enabled.",
            permission_action="screen_analyze",
            status="foundation",
            skill="screen_analyzer",
        )
    )

    registry.register(
        PluginAction(
            name="camera.analyze",
            plugin="vision",
            description="Prepare camera/environment analysis when vision runtime is enabled.",
            permission_action="camera_analyze",
            status="foundation",
            skill="camera_analyzer",
        )
    )

    registry.register(
        PluginAction(
            name="voice.runtime_alpha_status",
            plugin="voice",
            description="Show Voice Runtime Alpha status.",
            permission_action="read_project",
            status="online",
            skill="voice_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="voice.speak_plan",
            plugin="voice",
            description="Prepare a safe text-to-speech plan without playing audio.",
            permission_action="suggest",
            status="online",
            skill="voice_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="voice.speak_test",
            plugin="voice",
            description="Prepare a speak test proposal. Speaker output still requires confirmation and is not executed automatically.",
            permission_action="speaker_speak",
            status="online",
            skill="voice_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="voice.runtime_alpha_context",
            plugin="voice",
            description="Prepare Voice Runtime Alpha context without accessing audio devices.",
            permission_action="read_project",
            status="online",
            skill="voice_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="voice.runtime_status",
            plugin="voice",
            description="Show voice runtime planning status.",
            permission_action="think",
            status="online",
            skill="voice_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="voice.runtime_plan",
            plugin="voice",
            description="Show local STT/TTS runtime planning candidates and safety phases.",
            permission_action="think",
            status="online",
            skill="voice_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="voice.runtime_check",
            plugin="voice",
            description="Run passive voice runtime dependency checks without accessing audio devices.",
            permission_action="think",
            status="online",
            skill="voice_runtime_planning",
        )
    )

    registry.register(
        PluginAction(
            name="voice.status",
            plugin="voice",
            description="Show voice foundation status.",
            permission_action="think",
            status="online",
            skill="voice_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="voice.speak",
            plugin="voice",
            description="Prepare text-to-speech output when voice runtime is enabled.",
            permission_action="speaker_speak",
            status="foundation",
            skill="voice_interaction",
        )
    )

    registry.register(
        PluginAction(
            name="voice.listen",
            plugin="voice",
            description="Prepare microphone listening when voice runtime is enabled.",
            permission_action="microphone_listen",
            status="foundation",
            skill="voice_interaction",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.runtime_alpha_status",
            plugin="avatar",
            description="Show Avatar Runtime Alpha status.",
            permission_action="read_project",
            status="online",
            skill="avatar_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.expression_plan",
            plugin="avatar",
            description="Prepare an avatar expression plan without changing or rendering a real avatar.",
            permission_action="prepare_file",
            status="online",
            skill="avatar_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.gesture_plan",
            plugin="avatar",
            description="Prepare an avatar gesture plan without changing or rendering a real avatar.",
            permission_action="prepare_file",
            status="online",
            skill="avatar_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.runtime_alpha_context",
            plugin="avatar",
            description="Prepare Avatar Runtime Alpha context without rendering, writing files, or executing commands.",
            permission_action="read_project",
            status="online",
            skill="avatar_runtime_alpha",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.status",
            plugin="avatar",
            description="Show avatar foundation status.",
            permission_action="think",
            status="online",
            skill="avatar_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.providers",
            plugin="avatar",
            description="List avatar placeholder providers.",
            permission_action="think",
            status="online",
            skill="avatar_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.state",
            plugin="avatar",
            description="Show placeholder avatar state and runtime planning metadata.",
            permission_action="think",
            status="online",
            skill="avatar_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.expression",
            plugin="avatar",
            description="Prepare an avatar expression proposal without controlling a real avatar.",
            permission_action="prepare_file",
            status="foundation",
            skill="avatar_control",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.gesture",
            plugin="avatar",
            description="Prepare an avatar gesture proposal without controlling a real avatar.",
            permission_action="prepare_file",
            status="foundation",
            skill="avatar_control",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.control",
            plugin="avatar",
            description="Prepare avatar state, expression, or gesture control proposal.",
            permission_action="prepare_file",
            status="foundation",
            skill="avatar_control",
        )
    )

    registry.register(
        PluginAction(
            name="motion.capture",
            plugin="motion",
            description="Use motion capture or hand tracking input.",
            permission_action="camera_analyze",
            status="planned",
            skill="motion_capture",
        )
    )

    registry.register(
        PluginAction(
            name="blender.status",
            plugin="blender",
            description="Compatibility alias for AURA Blender Bridge Foundation status.",
            permission_action="read_project",
            status="online",
            skill="blender_bridge_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="media.status",
            plugin="media",
            description="Compatibility alias for AURA Media Understanding Foundation status.",
            permission_action="read_project",
            status="online",
            skill="media_understanding_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="expression.status",
            plugin="expression",
            description="Compatibility alias for AURA Expression Language status.",
            permission_action="read_project",
            status="online",
            skill="expression_language",
        )
    )

    registry.register(
        PluginAction(
            name="game_companion.status",
            plugin="game_companion",
            description="Compatibility alias for AURA Game Companion Foundation status.",
            permission_action="read_project",
            status="online",
            skill="game_companion_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="streaming_safety.status",
            plugin="streaming_safety",
            description="Compatibility alias for AURA Streaming Safety Foundation status.",
            permission_action="read_project",
            status="online",
            skill="streaming_safety_foundation",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.status",
            plugin="codebase_change",
            description="Show AURA Codebase Change Planner status.",
            permission_action="read_project",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.intent_plan",
            plugin="codebase_change",
            description="Prepare a metadata-only codebase change intent plan without reading or writing files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.impact_plan",
            plugin="codebase_change",
            description="Prepare a metadata-only codebase change impact plan without reading or writing files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.patch_plan",
            plugin="codebase_change",
            description="Prepare a proposal-only codebase patch plan without editing files automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.validation_plan",
            plugin="codebase_change",
            description="Prepare a codebase validation plan without executing commands automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.rollback_plan",
            plugin="codebase_change",
            description="Prepare a safe rollback plan without deleting, resetting, committing, or pushing automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_change.context",
            plugin="codebase_change",
            description="Show Codebase Change Planner context without reading, writing, editing, executing commands, committing, or pushing.",
            permission_action="read_project",
            status="online",
            skill="codebase_change_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.status",
            plugin="codebase_patch_proposal",
            description="Show Codebase Patch Proposal Renderer status.",
            permission_action="read_project",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.render",
            plugin="codebase_patch_proposal",
            description="Render a proposal-only codebase patch review packet without reading, writing, editing, applying patches, or executing commands automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.review_packet",
            plugin="codebase_patch_proposal",
            description="Prepare a codebase patch review packet with candidate surfaces and review checklist.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.validation_packet",
            plugin="codebase_patch_proposal",
            description="Prepare proposal-only validation steps for a codebase patch without executing commands automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.rollback_packet",
            plugin="codebase_patch_proposal",
            description="Prepare rollback notes for a codebase patch without resetting, deleting, committing, or pushing automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_patch_proposal.context",
            plugin="codebase_patch_proposal",
            description="Show Codebase Patch Proposal Renderer context and safety boundary.",
            permission_action="read_project",
            status="online",
            skill="codebase_patch_proposal_renderer",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.status",
            plugin="codebase_validation_gate",
            description="Show Codebase Validation Gate Planner status.",
            permission_action="read_project",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.plan",
            plugin="codebase_validation_gate",
            description="Prepare a proposal-only validation gate plan for a codebase change without executing commands automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.preflight",
            plugin="codebase_validation_gate",
            description="Prepare a proposal-only preflight gate for clean tree and branch checks.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.static_validation",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only static validation steps without running py_compile automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.registry_validation",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only registry validation steps for skills and plugin actions.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.runtime_smoke",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only runtime smoke validation steps without executing commands automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.diff_review",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only diff review gates before staging or committing.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.rollback",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only rollback gates for uncommitted or staged changes.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.commit_push",
            plugin="codebase_validation_gate",
            description="Prepare proposal-only commit and push gate steps without committing or pushing automatically.",
            permission_action="prepare_file",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    registry.register(
        PluginAction(
            name="codebase_validation_gate.context",
            plugin="codebase_validation_gate",
            description="Show Codebase Validation Gate Planner context and safety boundary.",
            permission_action="read_project",
            status="online",
            skill="codebase_validation_gate_planner",
        )
    )

    # Sprint 65.1 compatibility aliases for canonical codebase planner action names.
    codebase_compatibility_aliases = [
        (
            'codebase_change.change_plan',
            'codebase_change',
            'codebase_change_planner',
            'prepare_file',
            'Compatibility alias for codebase_change.intent_plan. Prepare a metadata-only codebase change plan without reading, writing, editing, executing commands, committing, or pushing automatically.',
        ),
        (
            'codebase_change.impact_review',
            'codebase_change',
            'codebase_change_planner',
            'prepare_file',
            'Compatibility alias for codebase_change.impact_plan. Prepare a metadata-only codebase impact review without reading, writing, editing, executing commands, committing, or pushing automatically.',
        ),
        (
            'codebase_patch.status',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'read_project',
            'Compatibility alias for codebase_patch_proposal.status. Show Codebase Patch Proposal Renderer status.',
        ),
        (
            'codebase_patch.patch_proposal',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Compatibility alias for codebase_patch_proposal.render. Render a proposal-only codebase patch packet without applying patches automatically.',
        ),
        (
            'codebase_patch.before_after_review',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Prepare a proposal-only before/after codebase patch review without reading, writing, editing, applying patches, or executing commands automatically.',
        ),
        (
            'codebase_patch.diff_summary',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Prepare a proposal-only codebase diff summary without reading, writing, editing, applying patches, or executing commands automatically.',
        ),
        (
            'codebase_patch.review_packet',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Compatibility alias for codebase_patch_proposal.review_packet. Prepare a codebase patch review packet.',
        ),
        (
            'codebase_patch.safety_packet',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Prepare a proposal-only codebase patch safety packet without reading, writing, editing, applying patches, or executing commands automatically.',
        ),
        (
            'codebase_patch.validation_packet',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Compatibility alias for codebase_patch_proposal.validation_packet. Prepare validation notes for a codebase patch.',
        ),
        (
            'codebase_patch.rollback_packet',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Compatibility alias for codebase_patch_proposal.rollback_packet. Prepare rollback notes for a codebase patch.',
        ),
        (
            'codebase_patch.context',
            'codebase_patch',
            'codebase_patch_proposal_renderer',
            'read_project',
            'Compatibility alias for codebase_patch_proposal.context. Show Codebase Patch Proposal Renderer context.',
        ),
        (
            'codebase_patch_proposal.safety_packet',
            'codebase_patch_proposal',
            'codebase_patch_proposal_renderer',
            'prepare_file',
            'Prepare a proposal-only codebase patch safety packet without reading, writing, editing, applying patches, or executing commands automatically.',
        ),
        (
            'codebase_validation.status',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'read_project',
            'Compatibility alias for codebase_validation_gate.status. Show Codebase Validation Gate Planner status.',
        ),
        (
            'codebase_validation.validation_gate',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.plan. Prepare a proposal-only validation gate plan.',
        ),
        (
            'codebase_validation.test_plan',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Prepare a proposal-only codebase validation test plan without executing commands or tests automatically.',
        ),
        (
            'codebase_validation.risk_gate',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Prepare a proposal-only codebase validation risk gate without executing commands automatically.',
        ),
        (
            'codebase_validation.release_checklist',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Prepare a proposal-only release checklist for codebase validation without committing or pushing automatically.',
        ),
        (
            'codebase_validation.context',
            'codebase_validation',
            'codebase_validation_gate_planner',
            'read_project',
            'Compatibility alias for codebase_validation_gate.context. Show Codebase Validation Gate Planner context.',
        ),
        (
            'codebase_validation_gate.validation_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.plan. Prepare a proposal-only validation gate plan.',
        ),
        (
            'codebase_validation_gate.preflight_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.preflight. Prepare a proposal-only preflight gate.',
        ),
        (
            'codebase_validation_gate.static_validation_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.static_validation. Prepare a proposal-only static validation gate.',
        ),
        (
            'codebase_validation_gate.registry_validation_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.registry_validation. Prepare a proposal-only registry validation gate.',
        ),
        (
            'codebase_validation_gate.runtime_smoke_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.runtime_smoke. Prepare a proposal-only runtime smoke gate.',
        ),
        (
            'codebase_validation_gate.diff_review_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.diff_review. Prepare a proposal-only diff review gate.',
        ),
        (
            'codebase_validation_gate.rollback_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.rollback. Prepare a proposal-only rollback gate.',
        ),
        (
            'codebase_validation_gate.commit_push_gate',
            'codebase_validation_gate',
            'codebase_validation_gate_planner',
            'prepare_file',
            'Compatibility alias for codebase_validation_gate.commit_push. Prepare a proposal-only commit/push gate without committing or pushing automatically.',
        ),
    ]

    for alias_name, plugin_name, skill_name, permission_action, description in codebase_compatibility_aliases:
        registry.register(
            PluginAction(
                name=alias_name,
                plugin=plugin_name,
                description=description,
                permission_action=permission_action,
                status="online",
                skill=skill_name,
            )
        )

    # Sprint 66.0 voice conversation planner actions.
    voice_conversation_actions = [
        ('voice_conversation.status', 'read_project', 'Show AURA Voice Conversation Planner status.'),
        ('voice_conversation.intent_plan', 'read_project', 'Prepare a metadata-only voice intent plan without microphone access or command execution.'),
        ('voice_conversation.response_plan', 'read_project', 'Prepare a metadata-only voice response plan without TTS or speaker output.'),
        ('voice_conversation.turn_plan', 'read_project', 'Prepare a metadata-only conversation turn plan without runtime voice action.'),
        ('voice_conversation.safety_plan', 'read_project', 'Prepare a voice safety plan without microphone, speaker, app, file, command, or external action execution.'),
        ('voice_conversation.context', 'read_project', 'Show Voice Conversation Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in voice_conversation_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="voice_conversation",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="voice_conversation_planner",
            )
        )

    # Sprint 67.0 vision context planner actions.
    vision_context_actions = [
        ('vision_context.status', 'read_project', 'Show AURA Vision Context Planner status.'),
        ('vision_context.visual_context_plan', 'read_project', 'Prepare a metadata-only visual context plan without screen capture, camera access, image reading, or runtime recognition.'),
        ('vision_context.screen_context_plan', 'read_project', 'Prepare a metadata-only screen context plan without capturing the screen or executing desktop actions.'),
        ('vision_context.camera_context_plan', 'read_project', 'Prepare a metadata-only camera context plan without camera access or video capture.'),
        ('vision_context.safety_plan', 'read_project', 'Prepare a vision safety plan without screen, camera, file, command, external action, or real tool execution.'),
        ('vision_context.context', 'read_project', 'Show Vision Context Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in vision_context_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="vision_context",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="vision_context_planner",
            )
        )

    # Sprint 68.0 avatar interaction planner actions.
    avatar_interaction_actions = [
        ('avatar_interaction.status', 'read_project', 'Show AURA Avatar Interaction Planner status.'),
        ('avatar_interaction.expression_plan', 'read_project', 'Prepare a metadata-only avatar expression plan without blendshape control, face tracking, rendering, or runtime execution.'),
        ('avatar_interaction.gesture_plan', 'read_project', 'Prepare a metadata-only avatar gesture plan without animation playback, bone control, or runtime execution.'),
        ('avatar_interaction.pose_plan', 'read_project', 'Prepare a metadata-only avatar pose plan without rig manipulation, Blender execution, or file operations.'),
        ('avatar_interaction.streaming_presence_plan', 'read_project', 'Prepare a metadata-only avatar streaming presence plan without OBS control or runtime avatar execution.'),
        ('avatar_interaction.safety_plan', 'read_project', 'Prepare an avatar safety plan without rendering, animation, mocap, Blender, files, commands, external action, or real tool execution.'),
        ('avatar_interaction.context', 'read_project', 'Show Avatar Interaction Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in avatar_interaction_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="avatar_interaction",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="avatar_interaction_planner",
            )
        )

    # Sprint 69.0 desktop workflow planner actions.
    desktop_workflow_actions = [
        ('desktop_workflow.status', 'read_project', 'Show AURA Desktop Workflow Planner status.'),
        ('desktop_workflow.workflow_plan', 'read_project', 'Prepare a metadata-only desktop workflow plan without app opening, window control, screen capture, or runtime execution.'),
        ('desktop_workflow.app_context_plan', 'read_project', 'Prepare a metadata-only app context plan without opening, focusing, inspecting, or controlling apps.'),
        ('desktop_workflow.window_flow_plan', 'read_project', 'Prepare a metadata-only window flow plan without screen capture, window inspection, or window control.'),
        ('desktop_workflow.task_sequence_plan', 'read_project', 'Prepare a metadata-only task sequence plan without file operations, command execution, or external tools.'),
        ('desktop_workflow.safety_plan', 'read_project', 'Prepare a desktop workflow safety plan without desktop, app, window, file, command, external action, or real tool execution.'),
        ('desktop_workflow.context', 'read_project', 'Show Desktop Workflow Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in desktop_workflow_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="desktop_workflow",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="desktop_workflow_planner",
            )
        )

    # Sprint 70.0 partner runtime planning layer actions.
    partner_runtime_actions = [
        ('partner_runtime.status', 'read_project', 'Show AURA Partner Runtime Planning Layer status.'),
        ('partner_runtime.mode_plan', 'read_project', 'Prepare a metadata-only partner runtime mode plan without autonomous runtime or execution.'),
        ('partner_runtime.session_plan', 'read_project', 'Prepare a metadata-only partner session plan without tool, file, desktop, device, command, or git execution.'),
        ('partner_runtime.multimodal_handoff_plan', 'read_project', 'Prepare a metadata-only handoff plan across voice, vision, avatar, desktop, and codebase planners.'),
        ('partner_runtime.tool_permission_plan', 'read_project', 'Prepare a tool permission gate plan without using tools or executing external actions.'),
        ('partner_runtime.growth_cycle_plan', 'read_project', 'Prepare a metadata-only growth cycle and checkpoint review plan.'),
        ('partner_runtime.safety_plan', 'read_project', 'Prepare a partner runtime safety plan without autonomous runtime, tools, files, commands, devices, desktop, network, git, or real tool execution.'),
        ('partner_runtime.context', 'read_project', 'Show Partner Runtime Planning Layer context and safety boundary.'),
    ]

    for action_name, permission_action, description in partner_runtime_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="partner_runtime",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="partner_runtime_planning_layer",
            )
        )

    # Sprint 71.0 thought loop planner actions.
    thought_loop_actions = [
        ('thought_loop.status', 'read_project', 'Show AURA Thought Loop Planner status.'),
        ('thought_loop.thought_cycle_plan', 'read_project', 'Prepare a metadata-only thought cycle plan without autonomous loops or execution.'),
        ('thought_loop.intent_frame_plan', 'read_project', 'Prepare a metadata-only intent framing plan before action.'),
        ('thought_loop.reasoning_summary_plan', 'read_project', 'Prepare a visible reasoning summary plan without exposing hidden chain-of-thought.'),
        ('thought_loop.uncertainty_review_plan', 'read_project', 'Prepare an uncertainty review plan that avoids pretending to know.'),
        ('thought_loop.action_readiness_review', 'read_project', 'Prepare an action readiness and permission gate review without executing actions.'),
        ('thought_loop.growth_memory_review', 'read_project', 'Prepare a growth memory review without writing memory automatically.'),
        ('thought_loop.safety_plan', 'read_project', 'Prepare a thought safety plan without autonomous loops, tools, memory write, internet, files, commands, devices, or real tool execution.'),
        ('thought_loop.context', 'read_project', 'Show Thought Loop Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in thought_loop_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="thought_loop",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="thought_loop_planner",
            )
        )

    # Sprint 72.0 reasoning context manager actions.
    reasoning_context_actions = [
        ('reasoning_context.status', 'read_project', 'Show AURA Reasoning Context Manager status.'),
        ('reasoning_context.context_plan', 'read_project', 'Prepare a metadata-only visible reasoning context plan without hidden chain-of-thought exposure.'),
        ('reasoning_context.fact_assumption_plan', 'read_project', 'Prepare a fact and assumption separation plan.'),
        ('reasoning_context.unknowns_review_plan', 'read_project', 'Prepare an unknowns review plan that avoids pretending to know.'),
        ('reasoning_context.evidence_boundary_plan', 'read_project', 'Prepare an evidence boundary and confidence plan.'),
        ('reasoning_context.decision_frame_plan', 'read_project', 'Prepare a safe decision frame plan.'),
        ('reasoning_context.response_strategy_plan', 'read_project', 'Prepare a response strategy plan for honest answers and next steps.'),
        ('reasoning_context.safety_plan', 'read_project', 'Prepare a reasoning safety plan without hidden chain-of-thought exposure or execution.'),
        ('reasoning_context.context', 'read_project', 'Show Reasoning Context Manager context and safety boundary.'),
    ]

    for action_name, permission_action, description in reasoning_context_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="reasoning_context",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="reasoning_context_manager",
            )
        )

    # Sprint 73.0 knowledge uncertainty gate actions.
    knowledge_uncertainty_actions = [
        ('knowledge_uncertainty.status', 'read_project', 'Show AURA Knowledge Uncertainty Gate status.'),
        ('knowledge_uncertainty.knowledge_gap_plan', 'read_project', 'Prepare a metadata-only knowledge gap plan.'),
        ('knowledge_uncertainty.uncertainty_review_plan', 'read_project', 'Prepare an uncertainty review plan that avoids pretending to know.'),
        ('knowledge_uncertainty.internet_search_gate_plan', 'read_project', 'Prepare an internet search permission gate plan without searching.'),
        ('knowledge_uncertainty.source_requirement_plan', 'read_project', 'Prepare a source requirement plan without fetching sources.'),
        ('knowledge_uncertainty.download_requirement_plan', 'read_project', 'Prepare a download requirement notice plan without downloading.'),
        ('knowledge_uncertainty.answer_confidence_plan', 'read_project', 'Prepare an answer confidence plan.'),
        ('knowledge_uncertainty.safety_plan', 'read_project', 'Prepare a knowledge safety plan without internet, downloads, files, commands, memory, network, or real tool execution.'),
        ('knowledge_uncertainty.context', 'read_project', 'Show Knowledge Uncertainty Gate context and safety boundary.'),
    ]

    for action_name, permission_action, description in knowledge_uncertainty_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="knowledge_uncertainty",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="knowledge_uncertainty_gate",
            )
        )

    # Sprint 74.0 voice input runtime foundation actions.
    voice_input_actions = [
        ('voice_input.status', 'read_project', 'Show AURA Voice Input Runtime Foundation status.'),
        ('voice_input.permission_plan', 'read_project', 'Prepare a microphone permission plan without accessing the microphone.'),
        ('voice_input.capture_boundary_plan', 'read_project', 'Prepare a voice capture boundary plan without recording audio.'),
        ('voice_input.stt_adapter_plan', 'read_project', 'Prepare a speech-to-text adapter plan without running STT.'),
        ('voice_input.intent_gate_plan', 'read_project', 'Prepare a voice intent gate plan before future voice commands.'),
        ('voice_input.command_confirmation_plan', 'read_project', 'Prepare a voice command confirmation plan without executing commands.'),
        ('voice_input.session_plan', 'read_project', 'Prepare a voice session plan without live listening.'),
        ('voice_input.safety_plan', 'read_project', 'Prepare voice input safety boundaries without mic, audio, STT, tools, files, commands, network, or real execution.'),
        ('voice_input.context', 'read_project', 'Show Voice Input Runtime Foundation context and safety boundary.'),
    ]

    for action_name, permission_action, description in voice_input_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="voice_input",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="voice_input_runtime_foundation",
            )
        )

    # Sprint 75.0 voice intent understanding actions.
    voice_intent_actions = [
        ('voice_intent.status', 'read_project', 'Show AURA Voice Intent Understanding status.'),
        ('voice_intent.transcript_normalization_plan', 'read_project', 'Prepare a voice transcript normalization plan without audio capture or STT runtime.'),
        ('voice_intent.classification_plan', 'read_project', 'Prepare a voice intent classification plan without executing actions.'),
        ('voice_intent.entity_slot_plan', 'read_project', 'Prepare a voice entity and slot extraction plan without reading files or external state.'),
        ('voice_intent.clarification_plan', 'read_project', 'Prepare a clarification plan for unclear voice intent.'),
        ('voice_intent.action_gate_plan', 'read_project', 'Prepare a voice action gate plan that requires confirmation before future action.'),
        ('voice_intent.response_plan', 'read_project', 'Prepare a voice-friendly response plan without execution.'),
        ('voice_intent.safety_plan', 'read_project', 'Prepare voice intent safety boundaries without microphone, audio, STT, tools, files, commands, network, desktop, git, or real execution.'),
        ('voice_intent.context', 'read_project', 'Show Voice Intent Understanding context and safety boundary.'),
    ]

    for action_name, permission_action, description in voice_intent_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="voice_intent",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="voice_intent_understanding",
            )
        )

    # Sprint 76.0 vision input runtime foundation actions.
    vision_input_actions = [
        ('vision_input.status', 'read_project', 'Show AURA Vision Input Runtime Foundation status.'),
        ('vision_input.permission_plan', 'read_project', 'Prepare future camera/screen/image permission planning without visual runtime.'),
        ('vision_input.capture_boundary_plan', 'read_project', 'Prepare safe visual capture boundaries without camera, screen, image, or video capture.'),
        ('vision_input.image_adapter_plan', 'read_project', 'Prepare future image input adapter planning without OCR, object detection, or vision runtime.'),
        ('vision_input.visual_source_plan', 'read_project', 'Prepare future visual source selection without reading files or accessing camera/screen.'),
        ('vision_input.visual_session_plan', 'read_project', 'Prepare explicit future visual session planning without always-watching behavior.'),
        ('vision_input.visual_action_gate_plan', 'read_project', 'Prepare visual action gates that require confirmation before future action.'),
        ('vision_input.safety_plan', 'read_project', 'Prepare vision input safety boundaries without camera, screen, image, video, tools, files, commands, network, desktop, git, or real execution.'),
        ('vision_input.context', 'read_project', 'Show Vision Input Runtime Foundation context and safety boundary.'),
    ]

    for action_name, permission_action, description in vision_input_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="vision_input",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="vision_input_runtime_foundation",
            )
        )

    # Sprint 77.0 visual context understanding actions.
    visual_context_actions = [
        ('visual_context.status', 'read_project', 'Show AURA Visual Context Understanding status.'),
        ('visual_context.scene_understanding_plan', 'read_project', 'Prepare visual scene understanding planning without camera, screen, image, or vision runtime.'),
        ('visual_context.object_relation_plan', 'read_project', 'Prepare visual object and relation planning without object detection runtime.'),
        ('visual_context.text_context_plan', 'read_project', 'Prepare text-in-image context planning without OCR or image text extraction runtime.'),
        ('visual_context.uncertainty_plan', 'read_project', 'Prepare visual uncertainty and evidence boundary planning.'),
        ('visual_context.clarification_plan', 'read_project', 'Prepare clarification planning for ambiguous visual context.'),
        ('visual_context.response_context_plan', 'read_project', 'Prepare safe visual response context planning without execution.'),
        ('visual_context.safety_plan', 'read_project', 'Prepare visual context safety boundaries without camera, screen, vision, OCR, face recognition, tools, files, commands, network, desktop, git, or real execution.'),
        ('visual_context.context', 'read_project', 'Show Visual Context Understanding context and safety boundary.'),
    ]

    for action_name, permission_action, description in visual_context_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="visual_context",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="visual_context_understanding",
            )
        )

    # Sprint 78.0 coder project generation planner actions.
    coder_project_actions = [
        ('coder_project.status', 'read_project', 'Show AURA Coder Project Generation Planner status.'),
        ('coder_project.request_frame_plan', 'read_project', 'Prepare project request framing without creating files or running commands.'),
        ('coder_project.structure_plan', 'read_project', 'Prepare project directory/file structure blueprint without writing to disk.'),
        ('coder_project.code_file_blueprint_plan', 'read_project', 'Prepare code file responsibility blueprint without code execution or file write.'),
        ('coder_project.dependency_plan', 'read_project', 'Prepare dependency planning without package download or install.'),
        ('coder_project.generation_review_gate_plan', 'read_project', 'Prepare review gates before future project generation.'),
        ('coder_project.validation_strategy_plan', 'read_project', 'Prepare validation strategy without running tests, builds, commands, or tools.'),
        ('coder_project.safety_plan', 'read_project', 'Prepare project generation safety boundaries without files, commands, dependencies, tools, network, desktop, git, or real execution.'),
        ('coder_project.context', 'read_project', 'Show Coder Project Generation Planner context and safety boundary.'),
    ]

    for action_name, permission_action, description in coder_project_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="coder_project",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="coder_project_generation_planner",
            )
        )

    # Sprint 79.0 dependency download permission gate actions.
    dependency_permission_actions = [
        ('dependency_permission.status', 'read_project', 'Show AURA Dependency Download Permission Gate status.'),
        ('dependency_permission.request_review_plan', 'read_project', 'Prepare dependency request review without installing, downloading, or running commands.'),
        ('dependency_permission.package_source_review_plan', 'read_project', 'Prepare package/source trust review without internet or network action.'),
        ('dependency_permission.download_permission_plan', 'read_project', 'Prepare download permission planning without downloading packages, models, assets, installers, or binaries.'),
        ('dependency_permission.install_command_review_plan', 'read_project', 'Prepare install command review without running pip, npm, apt, uv, poetry, shell, or commands.'),
        ('dependency_permission.risk_plan', 'read_project', 'Prepare dependency risk planning for license, supply chain, malware, and package risk.'),
        ('dependency_permission.offline_alternative_plan', 'read_project', 'Prepare offline or standard-library alternative planning before dependency use.'),
        ('dependency_permission.safety_plan', 'read_project', 'Prepare dependency/download safety boundaries without install, download, network, files, commands, tools, git, or real execution.'),
        ('dependency_permission.context', 'read_project', 'Show Dependency Download Permission Gate context and safety boundary.'),
    ]

    for action_name, permission_action, description in dependency_permission_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="dependency_permission",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="dependency_download_permission_gate",
            )
        )

    # Sprint 80.0 review stabilization 71-80 actions.
    checkpoint_80_actions = [
        ('checkpoint_80.status', 'read_project', 'Show AURA Sprint 71-80 Review & Stabilization checkpoint status.'),
        ('checkpoint_80.completed_feature_review_plan', 'read_project', 'Prepare Sprint 71-80 completed feature review planning.'),
        ('checkpoint_80.active_foundation_review_plan', 'read_project', 'Prepare active, foundation-only, planner-only, and permission-gated review planning.'),
        ('checkpoint_80.safety_boundary_review_plan', 'read_project', 'Prepare Sprint 71-80 safety boundary review planning.'),
        ('checkpoint_80.stabilization_validation_plan', 'read_project', 'Prepare checkpoint stabilization validation planning without executing commands.'),
        ('checkpoint_80.technical_debt_review_plan', 'read_project', 'Prepare technical debt review planning for the next block.'),
        ('checkpoint_80.roadmap_gap_review_plan', 'read_project', 'Prepare roadmap gap review planning for unbuilt runtime capabilities.'),
        ('checkpoint_80.next_block_planning_plan', 'read_project', 'Prepare Sprint 81-90 next block planning direction.'),
        ('checkpoint_80.context', 'read_project', 'Show Sprint 71-80 checkpoint context and safety boundary.'),
    ]

    for action_name, permission_action, description in checkpoint_80_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="checkpoint_80",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="review_stabilization_71_80",
            )
        )

    # Sprint 81.0 shared output formatter actions.
    output_formatter_actions = [
        ('output_formatter.status', 'read_project', 'Show AURA Shared Output Formatter status.'),
        ('output_formatter.packet_render_plan', 'read_project', 'Prepare shared packet rendering plan.'),
        ('output_formatter.safety_boundary_render_plan', 'read_project', 'Prepare shared safety boundary rendering plan.'),
        ('output_formatter.cli_output_format_plan', 'read_project', 'Prepare CLI output formatting migration plan.'),
        ('output_formatter.shell_output_format_plan', 'read_project', 'Prepare shell output formatting migration plan.'),
        ('output_formatter.console_output_format_plan', 'read_project', 'Prepare future Control Center console output formatting plan.'),
        ('output_formatter.ui_output_contract_plan', 'read_project', 'Prepare future UI output contract plan.'),
        ('output_formatter.formatter_migration_plan', 'read_project', 'Prepare shared output formatter migration plan.'),
        ('output_formatter.context', 'read_project', 'Show Shared Output Formatter context and safety boundary.'),
    ]

    for action_name, permission_action, description in output_formatter_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="output_formatter",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="shared_output_formatter",
            )
        )

    # Sprint 82.0 capability registry actions.
    capability_registry_actions = [
        ('capability_registry.status', 'read_project', 'Show AURA Capability Registry status.'),
        ('capability_registry.catalog_plan', 'read_project', 'Prepare capability catalog plan.'),
        ('capability_registry.state_review_plan', 'read_project', 'Prepare capability state review plan.'),
        ('capability_registry.permission_requirement_review_plan', 'read_project', 'Prepare permission requirement review plan.'),
        ('capability_registry.risk_level_review_plan', 'read_project', 'Prepare risk level review plan.'),
        ('capability_registry.control_center_capability_view_plan', 'read_project', 'Prepare future Control Center capability view plan.'),
        ('capability_registry.gap_review_plan', 'read_project', 'Prepare capability gap review plan.'),
        ('capability_registry.migration_plan', 'read_project', 'Prepare capability registry migration plan.'),
        ('capability_registry.context', 'read_project', 'Show Capability Registry context and catalog metadata.'),
    ]

    for action_name, permission_action, description in capability_registry_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="capability_registry",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="capability_registry",
            )
        )

    # Sprint 83.0 unified permission workflow actions.
    permission_workflow_actions = [
        ('permission_workflow.status', 'read_project', 'Show AURA Unified Permission Workflow status.'),
        ('permission_workflow.request_plan', 'read_project', 'Prepare permission request planning.'),
        ('permission_workflow.state_transition_plan', 'read_project', 'Prepare permission state transition planning.'),
        ('permission_workflow.risk_review_plan', 'read_project', 'Prepare permission risk review planning.'),
        ('permission_workflow.confirmation_prompt_plan', 'read_project', 'Prepare confirmation prompt planning.'),
        ('permission_workflow.audit_trail_plan', 'read_project', 'Prepare permission audit trail planning.'),
        ('permission_workflow.control_center_permission_view_plan', 'read_project', 'Prepare future Control Center Permission Center view planning.'),
        ('permission_workflow.policy_gap_review_plan', 'read_project', 'Prepare permission policy gap review planning.'),
        ('permission_workflow.context', 'read_project', 'Show Unified Permission Workflow context and templates.'),
    ]

    for action_name, permission_action, description in permission_workflow_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="permission_workflow",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="unified_permission_workflow",
            )
        )

    # Sprint 84.0 runtime service foundation actions.
    runtime_service_actions = [
        ('runtime_service.status', 'read_project', 'Show AURA Runtime Service Foundation status.'),
        ('runtime_service.safe_idle_boot_plan', 'read_project', 'Prepare safe_idle boot planning.'),
        ('runtime_service.lifecycle_plan', 'read_project', 'Prepare service lifecycle planning.'),
        ('runtime_service.health_check_plan', 'read_project', 'Prepare service health check planning.'),
        ('runtime_service.systemd_unit_blueprint_plan', 'read_project', 'Prepare systemd unit blueprint planning without writing service files.'),
        ('runtime_service.recovery_plan', 'read_project', 'Prepare service recovery planning.'),
        ('runtime_service.monitor_view_plan', 'read_project', 'Prepare service monitor view planning.'),
        ('runtime_service.auto_boot_policy_plan', 'read_project', 'Prepare safe auto-boot policy planning.'),
        ('runtime_service.context', 'read_project', 'Show Runtime Service Foundation context.'),
    ]

    for action_name, permission_action, description in runtime_service_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="runtime_service",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_runtime_service_foundation",
            )
        )

    # Sprint 85.0 launcher health monitor foundation actions.
    launcher_monitor_actions = [
        ('launcher_monitor.status', 'read_project', 'Show AURA Launcher & Health Monitor Foundation status.'),
        ('launcher_monitor.start_plan', 'read_project', 'Prepare launcher start planning without starting a process.'),
        ('launcher_monitor.stop_plan', 'read_project', 'Prepare launcher stop planning without stopping a process.'),
        ('launcher_monitor.restart_plan', 'read_project', 'Prepare launcher restart planning without restarting a process.'),
        ('launcher_monitor.status_plan', 'read_project', 'Prepare launcher status planning.'),
        ('launcher_monitor.log_view_plan', 'read_project', 'Prepare launcher log view planning without reading log files.'),
        ('launcher_monitor.health_monitor_plan', 'read_project', 'Prepare health monitor planning.'),
        ('launcher_monitor.control_center_service_monitor_plan', 'read_project', 'Prepare future Control Center service monitor planning.'),
        ('launcher_monitor.safety_policy_plan', 'read_project', 'Prepare launcher safety policy planning.'),
        ('launcher_monitor.context', 'read_project', 'Show Launcher & Health Monitor Foundation context.'),
    ]

    for action_name, permission_action, description in launcher_monitor_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="launcher_monitor",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_launcher_health_monitor_foundation",
            )
        )

    # Sprint 86.0 control center UI blueprint actions.
    control_center_actions = [
        ('control_center.status', 'read_project', 'Show AURA Control Center UI Blueprint status.'),
        ('control_center.dashboard_layout_blueprint_plan', 'read_project', 'Prepare dashboard layout blueprint planning.'),
        ('control_center.permission_center_blueprint_plan', 'read_project', 'Prepare Permission Center blueprint planning.'),
        ('control_center.service_monitor_blueprint_plan', 'read_project', 'Prepare Service Monitor blueprint planning.'),
        ('control_center.capability_viewer_blueprint_plan', 'read_project', 'Prepare Capability Viewer blueprint planning.'),
        ('control_center.launcher_control_blueprint_plan', 'read_project', 'Prepare Launcher Control blueprint planning.'),
        ('control_center.chat_console_placeholder_plan', 'read_project', 'Prepare Chat Console placeholder planning.'),
        ('control_center.plugin_dashboard_blueprint_plan', 'read_project', 'Prepare Plugin Dashboard blueprint planning.'),
        ('control_center.action_log_blueprint_plan', 'read_project', 'Prepare Action Log blueprint planning.'),
        ('control_center.safety_policy_plan', 'read_project', 'Prepare Control Center safety policy planning.'),
        ('control_center.context', 'read_project', 'Show Control Center UI Blueprint context.'),
    ]

    for action_name, permission_action, description in control_center_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="control_center",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_control_center_ui_blueprint",
            )
        )

    # Sprint 87.0 local console web foundation actions.
    local_console_web_actions = [
        ('local_console_web.status', 'read_project', 'Show AURA Local Console Web Foundation status.'),
        ('local_console_web.local_host_policy_plan', 'read_project', 'Prepare localhost-only policy planning.'),
        ('local_console_web.route_blueprint_plan', 'read_project', 'Prepare route blueprint planning without live routes.'),
        ('local_console_web.api_contract_blueprint_plan', 'read_project', 'Prepare API contract blueprint planning without backend runtime.'),
        ('local_console_web.static_asset_blueprint_plan', 'read_project', 'Prepare static asset blueprint planning without serving files.'),
        ('local_console_web.session_state_blueprint_plan', 'read_project', 'Prepare session state blueprint planning without session runtime.'),
        ('local_console_web.security_boundary_plan', 'read_project', 'Prepare local console web security boundary planning.'),
        ('local_console_web.control_center_web_bridge_plan', 'read_project', 'Prepare Control Center web bridge planning.'),
        ('local_console_web.developer_console_access_plan', 'read_project', 'Prepare local developer console access planning.'),
        ('local_console_web.context', 'read_project', 'Show Local Console Web Foundation context.'),
    ]

    for action_name, permission_action, description in local_console_web_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="local_console_web",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_local_console_web_foundation",
            )
        )

    # Sprint 88.0 chat bridge session state foundation actions.
    chat_bridge_actions = [
        ('chat_bridge.status', 'read_project', 'Show AURA Chat Bridge & Session State Foundation status.'),
        ('chat_bridge.conversation_session_blueprint_plan', 'read_project', 'Prepare conversation session blueprint planning.'),
        ('chat_bridge.message_flow_blueprint_plan', 'read_project', 'Prepare message flow blueprint planning.'),
        ('chat_bridge.control_center_chat_panel_bridge_plan', 'read_project', 'Prepare Control Center chat panel bridge planning.'),
        ('chat_bridge.local_console_session_contract_plan', 'read_project', 'Prepare Local Console session contract planning.'),
        ('chat_bridge.permission_aware_chat_action_boundary_plan', 'read_project', 'Prepare permission-aware chat action boundary planning.'),
        ('chat_bridge.chat_context_persistence_blueprint_plan', 'read_project', 'Prepare chat context persistence blueprint planning.'),
        ('chat_bridge.websocket_boundary_plan', 'read_project', 'Prepare websocket boundary planning without websocket runtime.'),
        ('chat_bridge.session_recovery_blueprint_plan', 'read_project', 'Prepare session recovery blueprint planning.'),
        ('chat_bridge.safety_policy_plan', 'read_project', 'Prepare chat bridge safety policy planning.'),
        ('chat_bridge.context', 'read_project', 'Show Chat Bridge & Session State Foundation context.'),
    ]

    for action_name, permission_action, description in chat_bridge_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="chat_bridge",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_chat_bridge_session_state_foundation",
            )
        )

    # Sprint 89.0 plugin permission dashboard foundation actions.
    plugin_permission_dashboard_actions = [
        ('plugin_permission_dashboard.status', 'read_project', 'Show AURA Plugin / Permission Dashboard Foundation status.'),
        ('plugin_permission_dashboard.plugin_registry_dashboard_plan', 'read_project', 'Prepare plugin registry dashboard planning.'),
        ('plugin_permission_dashboard.permission_request_dashboard_plan', 'read_project', 'Prepare permission request dashboard planning.'),
        ('plugin_permission_dashboard.permission_decision_visibility_plan', 'read_project', 'Prepare permission decision visibility planning.'),
        ('plugin_permission_dashboard.chat_originated_action_visibility_plan', 'read_project', 'Prepare chat-originated action request visibility planning.'),
        ('plugin_permission_dashboard.capability_permission_matrix_plan', 'read_project', 'Prepare capability-permission matrix planning.'),
        ('plugin_permission_dashboard.control_center_dashboard_bridge_plan', 'read_project', 'Prepare Control Center dashboard bridge planning.'),
        ('plugin_permission_dashboard.local_console_dashboard_contract_plan', 'read_project', 'Prepare Local Console dashboard contract planning.'),
        ('plugin_permission_dashboard.audit_trail_dashboard_blueprint_plan', 'read_project', 'Prepare audit trail dashboard blueprint planning.'),
        ('plugin_permission_dashboard.safety_policy_plan', 'read_project', 'Prepare plugin/permission dashboard safety policy planning.'),
        ('plugin_permission_dashboard.context', 'read_project', 'Show Plugin / Permission Dashboard Foundation context.'),
    ]

    for action_name, permission_action, description in plugin_permission_dashboard_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="plugin_permission_dashboard",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_plugin_permission_dashboard_foundation",
            )
        )

    # Sprint 132.0 final genesis acceptance criteria foundation actions.
    final_genesis_acceptance_criteria_actions = [
        ('final_genesis_acceptance_criteria.status', 'read_project', 'Show Final Genesis Acceptance Criteria Foundation status.'),
        ('final_genesis_acceptance_criteria.boot_stability_acceptance_criteria_plan', 'read_project', 'Prepare boot stability acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.local_service_acceptance_criteria_plan', 'read_project', 'Prepare local service acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.control_center_acceptance_criteria_plan', 'read_project', 'Prepare Control Center acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.local_chat_acceptance_criteria_plan', 'read_project', 'Prepare local chat acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.memory_acceptance_criteria_plan', 'read_project', 'Prepare memory acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.permission_audit_acceptance_criteria_plan', 'read_project', 'Prepare permission and audit acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.safe_idle_recovery_acceptance_criteria_plan', 'read_project', 'Prepare safe idle recovery acceptance criteria plan.'),
        ('final_genesis_acceptance_criteria.optional_orion_voice_vision_avatar_boundary_criteria_plan', 'read_project', 'Prepare optional ORION voice vision avatar boundary criteria plan.'),
        ('final_genesis_acceptance_criteria.final_genesis_go_no_go_criteria_plan', 'read_project', 'Prepare Final Genesis go/no-go criteria plan.'),
        ('final_genesis_acceptance_criteria.future_runtime_release_candidate_criteria_plan', 'read_project', 'Prepare future runtime release candidate criteria plan.'),
        ('final_genesis_acceptance_criteria.context', 'read_project', 'Show Final Genesis Acceptance Criteria Foundation context.'),
    ]

    for action_name, permission_action, description in final_genesis_acceptance_criteria_actions:
        registry.register(PluginAction(name=action_name, plugin="final_genesis_acceptance_criteria", description=description, permission_action=permission_action, status="online", skill="aura_final_genesis_acceptance_criteria_foundation"))

    # Sprint 131.0 post-checkpoint 130 next block foundation actions.
    post_checkpoint_130_next_block_actions = [
        ('post_checkpoint_130_next_block.status', 'read_project', 'Show Post-Checkpoint 130 Next Block Foundation status.'),
        ('post_checkpoint_130_next_block.sprint_131_140_sequence_foundation_plan', 'read_project', 'Prepare Sprint 131-140 sequence foundation plan.'),
        ('post_checkpoint_130_next_block.final_genesis_acceptance_criteria_foundation_plan', 'read_project', 'Prepare Final Genesis acceptance criteria foundation plan.'),
        ('post_checkpoint_130_next_block.runtime_activation_path_proposal_review_plan', 'read_project', 'Prepare runtime activation path proposal review plan.'),
        ('post_checkpoint_130_next_block.local_service_boot_plan_review_plan', 'read_project', 'Prepare local service boot plan review plan.'),
        ('post_checkpoint_130_next_block.control_center_runtime_entry_review_plan', 'read_project', 'Prepare Control Center runtime entry review plan.'),
        ('post_checkpoint_130_next_block.chat_runtime_minimal_loop_review_plan', 'read_project', 'Prepare chat runtime minimal loop review plan.'),
        ('post_checkpoint_130_next_block.memory_runtime_write_gate_review_plan', 'read_project', 'Prepare memory runtime write gate review plan.'),
        ('post_checkpoint_130_next_block.permission_runtime_grant_gate_review_plan', 'read_project', 'Prepare permission runtime grant gate review plan.'),
        ('post_checkpoint_130_next_block.audit_runtime_writer_activation_review_plan', 'read_project', 'Prepare audit runtime writer activation review plan.'),
        ('post_checkpoint_130_next_block.review_stabilization_131_140_checkpoint_plan', 'read_project', 'Prepare review stabilization 131-140 checkpoint plan.'),
        ('post_checkpoint_130_next_block.context', 'read_project', 'Show Post-Checkpoint 130 Next Block Foundation context.'),
    ]

    for action_name, permission_action, description in post_checkpoint_130_next_block_actions:
        registry.register(PluginAction(name=action_name, plugin="post_checkpoint_130_next_block", description=description, permission_action=permission_action, status="online", skill="aura_post_checkpoint_130_next_block_foundation"))

    # Sprint 130.0 review stabilization 121-130 foundation actions.
    review_stabilization_121_130_actions = [
        ('review_stabilization_121_130.status', 'read_project', 'Show Review Stabilization 121-130 status.'),
        ('review_stabilization_121_130.sprint_121_129_completion_review_plan', 'read_project', 'Prepare Sprint 121-129 completion review plan.'),
        ('review_stabilization_121_130.capability_registry_consistency_review_plan', 'read_project', 'Prepare capability registry consistency review plan.'),
        ('review_stabilization_121_130.permission_boundary_consistency_review_plan', 'read_project', 'Prepare permission boundary consistency review plan.'),
        ('review_stabilization_121_130.runtime_zero_counter_review_plan', 'read_project', 'Prepare runtime zero counter review plan.'),
        ('review_stabilization_121_130.dashboard_orion_boundary_review_plan', 'read_project', 'Prepare dashboard ORION boundary review plan.'),
        ('review_stabilization_121_130.action_permission_recovery_blocker_review_plan', 'read_project', 'Prepare action permission recovery blocker review plan.'),
        ('review_stabilization_121_130.documentation_roadmap_consistency_review_plan', 'read_project', 'Prepare documentation roadmap consistency review plan.'),
        ('review_stabilization_121_130.boot_and_cli_surface_review_plan', 'read_project', 'Prepare boot and CLI surface review plan.'),
        ('review_stabilization_121_130.known_deferred_runtime_review_plan', 'read_project', 'Prepare known deferred runtime review plan.'),
        ('review_stabilization_121_130.future_sprint_131_140_readiness_plan', 'read_project', 'Prepare future Sprint 131-140 readiness plan.'),
        ('review_stabilization_121_130.context', 'read_project', 'Show Review Stabilization 121-130 context.'),
    ]

    for action_name, permission_action, description in review_stabilization_121_130_actions:
        registry.register(PluginAction(name=action_name, plugin="review_stabilization_121_130", description=description, permission_action=permission_action, status="online", skill="aura_review_stabilization_121_130_foundation"))

    # Sprint 129.0 runtime activation blocker register boundary review foundation actions.
    runtime_activation_blocker_register_boundary_review_actions = [
        ('runtime_activation_blocker_register_boundary_review.status', 'read_project', 'Show Runtime Activation Blocker Register Boundary Review status.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_register_schema_boundary_review_plan', 'read_project', 'Prepare blocker register schema boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_source_classification_boundary_review_plan', 'read_project', 'Prepare blocker source classification boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_severity_policy_boundary_review_plan', 'read_project', 'Prepare blocker severity policy boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_activation_gate_link_boundary_review_plan', 'read_project', 'Prepare blocker activation gate link boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_resolution_evidence_boundary_review_plan', 'read_project', 'Prepare blocker resolution evidence boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_dashboard_visibility_boundary_review_plan', 'read_project', 'Prepare blocker dashboard visibility boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_audit_link_boundary_review_plan', 'read_project', 'Prepare blocker audit link boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.blocker_failure_safe_idle_boundary_review_plan', 'read_project', 'Prepare blocker failure safe idle boundary review plan.'),
        ('runtime_activation_blocker_register_boundary_review.future_runtime_activation_unblock_boundary_plan', 'read_project', 'Prepare future runtime activation unblock boundary plan.'),
        ('runtime_activation_blocker_register_boundary_review.context', 'read_project', 'Show Runtime Activation Blocker Register Boundary Review context.'),
    ]

    for action_name, permission_action, description in runtime_activation_blocker_register_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_activation_blocker_register_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_runtime_activation_blocker_register_boundary_review_foundation"))

    # Sprint 128.0 dashboard runtime readiness boundary review foundation actions.
    dashboard_runtime_readiness_boundary_review_actions = [
        ('dashboard_runtime_readiness_boundary_review.status', 'read_project', 'Show Dashboard Runtime Readiness Boundary Review status.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_runtime_entrypoint_boundary_review_plan', 'read_project', 'Prepare dashboard runtime entrypoint boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_route_contract_boundary_review_plan', 'read_project', 'Prepare dashboard route contract boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_api_contract_boundary_review_plan', 'read_project', 'Prepare dashboard API contract boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_websocket_event_boundary_review_plan', 'read_project', 'Prepare dashboard websocket event boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_permission_panel_runtime_boundary_review_plan', 'read_project', 'Prepare dashboard permission panel runtime boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_audit_panel_runtime_boundary_review_plan', 'read_project', 'Prepare dashboard audit panel runtime boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_action_panel_runtime_boundary_review_plan', 'read_project', 'Prepare dashboard action panel runtime boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.dashboard_failure_safe_idle_boundary_review_plan', 'read_project', 'Prepare dashboard failure safe idle boundary review plan.'),
        ('dashboard_runtime_readiness_boundary_review.future_dashboard_runtime_activation_boundary_plan', 'read_project', 'Prepare future dashboard runtime activation boundary plan.'),
        ('dashboard_runtime_readiness_boundary_review.context', 'read_project', 'Show Dashboard Runtime Readiness Boundary Review context.'),
    ]

    for action_name, permission_action, description in dashboard_runtime_readiness_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="dashboard_runtime_readiness_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_dashboard_runtime_readiness_boundary_review_foundation"))

    # Sprint 127.0 runtime recovery drill boundary review foundation actions.
    runtime_recovery_drill_boundary_review_actions = [
        ('runtime_recovery_drill_boundary_review.status', 'read_project', 'Show Runtime Recovery Drill Boundary Review status.'),
        ('runtime_recovery_drill_boundary_review.recovery_drill_scenario_catalog_boundary_review_plan', 'read_project', 'Prepare recovery drill scenario catalog boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.recovery_trigger_boundary_review_plan', 'read_project', 'Prepare recovery trigger boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.recovery_safe_idle_boundary_review_plan', 'read_project', 'Prepare recovery safe idle boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.rollback_preview_boundary_review_plan', 'read_project', 'Prepare rollback preview boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.recovery_audit_dashboard_boundary_review_plan', 'read_project', 'Prepare recovery audit/dashboard boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.recovery_permission_boundary_review_plan', 'read_project', 'Prepare recovery permission boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.orion_recovery_disconnect_boundary_review_plan', 'read_project', 'Prepare ORION recovery disconnect boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.recovery_failure_escalation_boundary_review_plan', 'read_project', 'Prepare recovery failure escalation boundary review plan.'),
        ('runtime_recovery_drill_boundary_review.future_runtime_recovery_drill_boundary_plan', 'read_project', 'Prepare future runtime recovery drill boundary plan.'),
        ('runtime_recovery_drill_boundary_review.context', 'read_project', 'Show Runtime Recovery Drill Boundary Review context.'),
    ]

    for action_name, permission_action, description in runtime_recovery_drill_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_recovery_drill_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_runtime_recovery_drill_boundary_review_foundation"))

    # Sprint 126.0 runtime grant expiry boundary review foundation actions.
    runtime_grant_expiry_boundary_review_actions = [
        ('runtime_grant_expiry_boundary_review.status', 'read_project', 'Show Runtime Grant Expiry Boundary Review status.'),
        ('runtime_grant_expiry_boundary_review.grant_expiry_schema_boundary_review_plan', 'read_project', 'Prepare grant expiry schema boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.grant_lifetime_policy_boundary_review_plan', 'read_project', 'Prepare grant lifetime policy boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.grant_renewal_request_boundary_review_plan', 'read_project', 'Prepare grant renewal request boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.grant_revocation_boundary_review_plan', 'read_project', 'Prepare grant revocation boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.expired_grant_denial_boundary_review_plan', 'read_project', 'Prepare expired grant denial boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.dashboard_grant_visibility_boundary_review_plan', 'read_project', 'Prepare dashboard grant visibility boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.audit_grant_expiry_boundary_review_plan', 'read_project', 'Prepare audit grant expiry boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.grant_expiry_failure_safe_idle_boundary_review_plan', 'read_project', 'Prepare grant expiry failure safe idle boundary review plan.'),
        ('runtime_grant_expiry_boundary_review.future_runtime_grant_expiry_boundary_plan', 'read_project', 'Prepare future runtime grant expiry boundary plan.'),
        ('runtime_grant_expiry_boundary_review.context', 'read_project', 'Show Runtime Grant Expiry Boundary Review context.'),
    ]

    for action_name, permission_action, description in runtime_grant_expiry_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_grant_expiry_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_runtime_grant_expiry_boundary_review_foundation"))

    # Sprint 125.0 safe local action allowlist boundary review foundation actions.
    safe_local_action_allowlist_boundary_review_actions = [
        ('safe_local_action_allowlist_boundary_review.status', 'read_project', 'Show Safe Local Action Allowlist Boundary Review status.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_catalog_boundary_review_plan', 'read_project', 'Prepare safe action catalog boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_scope_boundary_review_plan', 'read_project', 'Prepare safe action scope boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_permission_boundary_review_plan', 'read_project', 'Prepare safe action permission boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_risk_level_boundary_review_plan', 'read_project', 'Prepare safe action risk level boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_rollback_boundary_review_plan', 'read_project', 'Prepare safe action rollback boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_audit_dashboard_boundary_review_plan', 'read_project', 'Prepare safe action audit/dashboard boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_denied_action_boundary_review_plan', 'read_project', 'Prepare safe action denied action boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.safe_action_runtime_gate_boundary_review_plan', 'read_project', 'Prepare safe action runtime gate boundary review plan.'),
        ('safe_local_action_allowlist_boundary_review.future_safe_local_action_runtime_boundary_plan', 'read_project', 'Prepare future safe local action runtime boundary plan.'),
        ('safe_local_action_allowlist_boundary_review.context', 'read_project', 'Show Safe Local Action Allowlist Boundary Review context.'),
    ]

    for action_name, permission_action, description in safe_local_action_allowlist_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="safe_local_action_allowlist_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_safe_local_action_allowlist_boundary_review_foundation"))

    # Sprint 124.0 ORION dry handshake boundary review foundation actions.
    orion_dry_handshake_boundary_review_actions = [
        ('orion_dry_handshake_boundary_review.status', 'read_project', 'Show ORION Dry Handshake Boundary Review status.'),
        ('orion_dry_handshake_boundary_review.orion_client_identity_packet_boundary_review_plan', 'read_project', 'Prepare ORION client identity packet boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_capability_packet_boundary_review_plan', 'read_project', 'Prepare ORION capability packet boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_permission_scope_packet_boundary_review_plan', 'read_project', 'Prepare ORION permission scope packet boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_status_heartbeat_boundary_review_plan', 'read_project', 'Prepare ORION status heartbeat boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_redaction_boundary_review_plan', 'read_project', 'Prepare ORION redaction boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_emergency_stop_boundary_review_plan', 'read_project', 'Prepare ORION emergency stop boundary review plan.'),
        ('orion_dry_handshake_boundary_review.atlas_orion_authority_boundary_review_plan', 'read_project', 'Prepare ATLAS/ORION authority boundary review plan.'),
        ('orion_dry_handshake_boundary_review.orion_failure_safe_idle_boundary_review_plan', 'read_project', 'Prepare ORION failure safe idle boundary review plan.'),
        ('orion_dry_handshake_boundary_review.future_orion_handshake_runtime_boundary_plan', 'read_project', 'Prepare future ORION handshake runtime boundary plan.'),
        ('orion_dry_handshake_boundary_review.context', 'read_project', 'Show ORION Dry Handshake Boundary Review context.'),
    ]

    for action_name, permission_action, description in orion_dry_handshake_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="orion_dry_handshake_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_orion_dry_handshake_boundary_review_foundation"))

    # Sprint 123.0 dashboard control center boundary review foundation actions.
    dashboard_control_center_boundary_review_actions = [
        ('dashboard_control_center_boundary_review.status', 'read_project', 'Show Dashboard Control Center Boundary Review status.'),
        ('dashboard_control_center_boundary_review.control_center_shell_layout_boundary_review_plan', 'read_project', 'Prepare control center shell layout boundary review plan.'),
        ('dashboard_control_center_boundary_review.dashboard_status_payload_boundary_review_plan', 'read_project', 'Prepare dashboard status payload boundary review plan.'),
        ('dashboard_control_center_boundary_review.permission_panel_boundary_review_plan', 'read_project', 'Prepare permission panel boundary review plan.'),
        ('dashboard_control_center_boundary_review.audit_panel_boundary_review_plan', 'read_project', 'Prepare audit panel boundary review plan.'),
        ('dashboard_control_center_boundary_review.action_proposal_panel_boundary_review_plan', 'read_project', 'Prepare action proposal panel boundary review plan.'),
        ('dashboard_control_center_boundary_review.orion_client_panel_boundary_review_plan', 'read_project', 'Prepare ORION client panel boundary review plan.'),
        ('dashboard_control_center_boundary_review.runtime_gate_panel_boundary_review_plan', 'read_project', 'Prepare runtime gate panel boundary review plan.'),
        ('dashboard_control_center_boundary_review.dashboard_failure_safe_idle_boundary_review_plan', 'read_project', 'Prepare dashboard failure safe idle boundary review plan.'),
        ('dashboard_control_center_boundary_review.future_dashboard_control_center_runtime_boundary_plan', 'read_project', 'Prepare future dashboard control center runtime boundary plan.'),
        ('dashboard_control_center_boundary_review.context', 'read_project', 'Show Dashboard Control Center Boundary Review context.'),
    ]

    for action_name, permission_action, description in dashboard_control_center_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="dashboard_control_center_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_dashboard_control_center_boundary_review_foundation"))

    # Sprint 122.0 runtime permission audit writer boundary review foundation actions.
    runtime_permission_audit_writer_boundary_review_actions = [
        ('runtime_permission_audit_writer_boundary_review.status', 'read_project', 'Show Runtime Permission Audit Writer Boundary Review status.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_schema_boundary_review_plan', 'read_project', 'Prepare audit writer schema boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_storage_boundary_review_plan', 'read_project', 'Prepare audit writer storage boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_redaction_boundary_review_plan', 'read_project', 'Prepare audit writer redaction boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_visibility_boundary_review_plan', 'read_project', 'Prepare audit writer visibility boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.permission_decision_audit_link_review_plan', 'read_project', 'Prepare permission decision audit link review plan.'),
        ('runtime_permission_audit_writer_boundary_review.dashboard_audit_payload_boundary_review_plan', 'read_project', 'Prepare dashboard audit payload boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_failure_boundary_review_plan', 'read_project', 'Prepare audit writer failure boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.audit_writer_runtime_gate_boundary_review_plan', 'read_project', 'Prepare audit writer runtime gate boundary review plan.'),
        ('runtime_permission_audit_writer_boundary_review.future_permission_audit_writer_runtime_boundary_plan', 'read_project', 'Prepare future permission audit writer runtime boundary plan.'),
        ('runtime_permission_audit_writer_boundary_review.context', 'read_project', 'Show Runtime Permission Audit Writer Boundary Review context.'),
    ]

    for action_name, permission_action, description in runtime_permission_audit_writer_boundary_review_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_permission_audit_writer_boundary_review", description=description, permission_action=permission_action, status="online", skill="aura_runtime_permission_audit_writer_boundary_review_foundation"))

    # Sprint 121.0 post-checkpoint 120 next block planning foundation actions.
    post_checkpoint_120_next_block_planning_actions = [
        ('post_checkpoint_120_next_block_planning.status', 'read_project', 'Show Post-Checkpoint 120 Next Block Planning status.'),
        ('post_checkpoint_120_next_block_planning.checkpoint_120_output_review_plan', 'read_project', 'Prepare checkpoint 120 output review plan.'),
        ('post_checkpoint_120_next_block_planning.sprint_121_130_scope_definition_plan', 'read_project', 'Prepare Sprint 121-130 scope definition plan.'),
        ('post_checkpoint_120_next_block_planning.runtime_readiness_continuation_plan', 'read_project', 'Prepare runtime readiness continuation plan.'),
        ('post_checkpoint_120_next_block_planning.permission_audit_writer_boundary_plan', 'read_project', 'Prepare permission audit writer boundary plan.'),
        ('post_checkpoint_120_next_block_planning.dashboard_control_center_boundary_plan', 'read_project', 'Prepare dashboard control center boundary plan.'),
        ('post_checkpoint_120_next_block_planning.orion_dry_handshake_boundary_plan', 'read_project', 'Prepare ORION dry handshake boundary plan.'),
        ('post_checkpoint_120_next_block_planning.safe_local_action_allowlist_boundary_plan', 'read_project', 'Prepare safe local action allowlist boundary plan.'),
        ('post_checkpoint_120_next_block_planning.runtime_activation_blocker_tracking_plan', 'read_project', 'Prepare runtime activation blocker tracking plan.'),
        ('post_checkpoint_120_next_block_planning.future_121_130_checkpoint_boundary_plan', 'read_project', 'Prepare future 121-130 checkpoint boundary plan.'),
        ('post_checkpoint_120_next_block_planning.context', 'read_project', 'Show Post-Checkpoint 120 Next Block Planning context.'),
    ]

    for action_name, permission_action, description in post_checkpoint_120_next_block_planning_actions:
        registry.register(PluginAction(name=action_name, plugin="post_checkpoint_120_next_block_planning", description=description, permission_action=permission_action, status="online", skill="aura_post_checkpoint_120_next_block_planning_foundation"))

    # Sprint 120.0 review stabilization 111-120 foundation actions.
    review_stabilization_111_120_actions = [
        ('review_stabilization_111_120.status', 'read_project', 'Show Review Stabilization 111-120 status.'),
        ('review_stabilization_111_120.sprint_111_120_completion_review_plan', 'read_project', 'Prepare Sprint 111-120 completion review plan.'),
        ('review_stabilization_111_120.capability_registry_stabilization_review_plan', 'read_project', 'Prepare capability registry stabilization review plan.'),
        ('review_stabilization_111_120.runtime_safety_zero_state_review_plan', 'read_project', 'Prepare runtime safety zero-state review plan.'),
        ('review_stabilization_111_120.integration_surface_stabilization_review_plan', 'read_project', 'Prepare integration surface stabilization review plan.'),
        ('review_stabilization_111_120.documentation_roadmap_stabilization_review_plan', 'read_project', 'Prepare documentation roadmap stabilization review plan.'),
        ('review_stabilization_111_120.v1_runtime_readiness_blocker_review_plan', 'read_project', 'Prepare v1 runtime readiness blocker review plan.'),
        ('review_stabilization_111_120.release_cutline_consistency_review_plan', 'read_project', 'Prepare release cutline consistency review plan.'),
        ('review_stabilization_111_120.next_block_121_130_boundary_plan', 'read_project', 'Prepare next block 121-130 boundary plan.'),
        ('review_stabilization_111_120.checkpoint_120_acceptance_review_plan', 'read_project', 'Prepare checkpoint 120 acceptance review plan.'),
        ('review_stabilization_111_120.context', 'read_project', 'Show Review Stabilization 111-120 context.'),
    ]

    for action_name, permission_action, description in review_stabilization_111_120_actions:
        registry.register(PluginAction(name=action_name, plugin="review_stabilization_111_120", description=description, permission_action=permission_action, status="online", skill="aura_review_stabilization_111_120_foundation"))

    # Sprint 119.0 v1 runtime readiness cutline review foundation actions.
    v1_runtime_readiness_cutline_review_actions = [
        ('v1_runtime_readiness_cutline_review.status', 'read_project', 'Show v1 Runtime Readiness Cutline Review status.'),
        ('v1_runtime_readiness_cutline_review.v1_allowed_capability_cutline_plan', 'read_project', 'Prepare v1 allowed capability cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_deferred_capability_cutline_plan', 'read_project', 'Prepare v1 deferred capability cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_runtime_gate_cutline_plan', 'read_project', 'Prepare v1 runtime gate cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_permission_audit_cutline_plan', 'read_project', 'Prepare v1 permission audit cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_orion_boundary_cutline_plan', 'read_project', 'Prepare v1 ORION boundary cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_dashboard_visibility_cutline_plan', 'read_project', 'Prepare v1 dashboard visibility cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_release_blocker_cutline_plan', 'read_project', 'Prepare v1 release blocker cutline plan.'),
        ('v1_runtime_readiness_cutline_review.v1_safe_idle_acceptance_cutline_plan', 'read_project', 'Prepare v1 safe idle acceptance cutline plan.'),
        ('v1_runtime_readiness_cutline_review.future_v1_runtime_activation_boundary_plan', 'read_project', 'Prepare future v1 runtime activation boundary plan.'),
        ('v1_runtime_readiness_cutline_review.context', 'read_project', 'Show v1 Runtime Readiness Cutline Review context.'),
    ]

    for action_name, permission_action, description in v1_runtime_readiness_cutline_review_actions:
        registry.register(PluginAction(name=action_name, plugin="v1_runtime_readiness_cutline_review", description=description, permission_action=permission_action, status="online", skill="aura_v1_runtime_readiness_cutline_review_foundation"))

    # Sprint 118.0 manual approval decision flow review foundation actions.
    manual_approval_decision_flow_review_actions = [
        ('manual_approval_decision_flow_review.status', 'read_project', 'Show Manual Approval Decision Flow Review status.'),
        ('manual_approval_decision_flow_review.approval_request_schema_review_plan', 'read_project', 'Prepare approval request schema review plan.'),
        ('manual_approval_decision_flow_review.approval_decision_state_review_plan', 'read_project', 'Prepare approval decision state review plan.'),
        ('manual_approval_decision_flow_review.approval_outcome_catalog_review_plan', 'read_project', 'Prepare approval outcome catalog review plan.'),
        ('manual_approval_decision_flow_review.approval_denial_cancellation_review_plan', 'read_project', 'Prepare approval denial cancellation review plan.'),
        ('manual_approval_decision_flow_review.approval_escalation_boundary_review_plan', 'read_project', 'Prepare approval escalation boundary review plan.'),
        ('manual_approval_decision_flow_review.approval_audit_reference_review_plan', 'read_project', 'Prepare approval audit reference review plan.'),
        ('manual_approval_decision_flow_review.approval_dashboard_payload_review_plan', 'read_project', 'Prepare approval dashboard payload review plan.'),
        ('manual_approval_decision_flow_review.approval_runtime_gate_boundary_review_plan', 'read_project', 'Prepare approval runtime gate boundary review plan.'),
        ('manual_approval_decision_flow_review.future_manual_approval_runtime_boundary_plan', 'read_project', 'Prepare future manual approval runtime boundary plan.'),
        ('manual_approval_decision_flow_review.context', 'read_project', 'Show Manual Approval Decision Flow Review context.'),
    ]

    for action_name, permission_action, description in manual_approval_decision_flow_review_actions:
        registry.register(PluginAction(name=action_name, plugin="manual_approval_decision_flow_review", description=description, permission_action=permission_action, status="online", skill="aura_manual_approval_decision_flow_review_foundation"))

    # Sprint 117.0 runtime error rollback preview foundation actions.
    runtime_error_rollback_preview_actions = [
        ('runtime_error_rollback_preview.status', 'read_project', 'Show Runtime Error and Rollback Preview status.'),
        ('runtime_error_rollback_preview.runtime_error_taxonomy_preview_plan', 'read_project', 'Prepare runtime error taxonomy preview plan.'),
        ('runtime_error_rollback_preview.rollback_preview_packet_plan', 'read_project', 'Prepare rollback preview packet plan.'),
        ('runtime_error_rollback_preview.failure_recovery_state_model_plan', 'read_project', 'Prepare failure recovery state model plan.'),
        ('runtime_error_rollback_preview.cancellation_boundary_preview_plan', 'read_project', 'Prepare cancellation boundary preview plan.'),
        ('runtime_error_rollback_preview.partial_execution_guard_preview_plan', 'read_project', 'Prepare partial execution guard preview plan.'),
        ('runtime_error_rollback_preview.permission_error_review_plan', 'read_project', 'Prepare permission error review plan.'),
        ('runtime_error_rollback_preview.audit_error_reference_preview_plan', 'read_project', 'Prepare audit error reference preview plan.'),
        ('runtime_error_rollback_preview.dashboard_error_rollback_payload_plan', 'read_project', 'Prepare dashboard error rollback payload plan.'),
        ('runtime_error_rollback_preview.future_runtime_recovery_boundary_plan', 'read_project', 'Prepare future runtime recovery boundary plan.'),
        ('runtime_error_rollback_preview.context', 'read_project', 'Show Runtime Error and Rollback Preview context.'),
    ]

    for action_name, permission_action, description in runtime_error_rollback_preview_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_error_rollback_preview", description=description, permission_action=permission_action, status="online", skill="aura_runtime_error_rollback_preview_foundation"))

    # Sprint 116.0 ORION client boundary contract foundation actions.
    orion_client_boundary_contract_actions = [
        ('orion_client_boundary_contract.status', 'read_project', 'Show ORION Client Boundary Contract status.'),
        ('orion_client_boundary_contract.orion_client_identity_boundary_plan', 'read_project', 'Prepare ORION client identity boundary plan.'),
        ('orion_client_boundary_contract.atlas_orion_authority_boundary_plan', 'read_project', 'Prepare ATLAS ORION authority boundary plan.'),
        ('orion_client_boundary_contract.orion_sense_permission_boundary_plan', 'read_project', 'Prepare ORION sense permission boundary plan.'),
        ('orion_client_boundary_contract.orion_local_action_boundary_plan', 'read_project', 'Prepare ORION local action boundary plan.'),
        ('orion_client_boundary_contract.orion_emergency_stop_boundary_plan', 'read_project', 'Prepare ORION emergency stop boundary plan.'),
        ('orion_client_boundary_contract.orion_dashboard_status_boundary_plan', 'read_project', 'Prepare ORION dashboard status boundary plan.'),
        ('orion_client_boundary_contract.orion_runtime_handshake_boundary_plan', 'read_project', 'Prepare ORION runtime handshake boundary plan.'),
        ('orion_client_boundary_contract.orion_data_flow_redaction_boundary_plan', 'read_project', 'Prepare ORION data flow redaction boundary plan.'),
        ('orion_client_boundary_contract.future_orion_runtime_boundary_plan', 'read_project', 'Prepare future ORION runtime boundary plan.'),
        ('orion_client_boundary_contract.context', 'read_project', 'Show ORION Client Boundary Contract context.'),
    ]

    for action_name, permission_action, description in orion_client_boundary_contract_actions:
        registry.register(PluginAction(name=action_name, plugin="orion_client_boundary_contract", description=description, permission_action=permission_action, status="online", skill="aura_orion_client_boundary_contract_foundation"))

    # Sprint 115.0 safe local action contract review foundation actions.
    safe_local_action_contract_review_actions = [
        ('safe_local_action_contract_review.status', 'read_project', 'Show Safe Local Action Contract Review status.'),
        ('safe_local_action_contract_review.local_open_contract_review_plan', 'read_project', 'Prepare local open contract review plan.'),
        ('safe_local_action_contract_review.controlled_create_contract_review_plan', 'read_project', 'Prepare controlled create contract review plan.'),
        ('safe_local_action_contract_review.controlled_write_preview_contract_review_plan', 'read_project', 'Prepare controlled write preview contract review plan.'),
        ('safe_local_action_contract_review.action_preview_packet_contract_plan', 'read_project', 'Prepare action preview packet contract plan.'),
        ('safe_local_action_contract_review.permission_scope_contract_review_plan', 'read_project', 'Prepare permission scope contract review plan.'),
        ('safe_local_action_contract_review.side_effect_boundary_contract_plan', 'read_project', 'Prepare side effect boundary contract plan.'),
        ('safe_local_action_contract_review.rollback_cancel_contract_review_plan', 'read_project', 'Prepare rollback cancel contract review plan.'),
        ('safe_local_action_contract_review.dashboard_contract_payload_plan', 'read_project', 'Prepare dashboard contract payload plan.'),
        ('safe_local_action_contract_review.future_action_runtime_boundary_plan', 'read_project', 'Prepare future action runtime boundary plan.'),
        ('safe_local_action_contract_review.context', 'read_project', 'Show Safe Local Action Contract Review context.'),
    ]

    for action_name, permission_action, description in safe_local_action_contract_review_actions:
        registry.register(PluginAction(name=action_name, plugin="safe_local_action_contract_review", description=description, permission_action=permission_action, status="online", skill="aura_safe_local_action_contract_review_foundation"))

    # Sprint 114.0 dashboard runtime readiness view model foundation actions.
    dashboard_runtime_readiness_view_model_actions = [
        ('dashboard_runtime_readiness_view_model.status', 'read_project', 'Show Dashboard Runtime Readiness View Model status.'),
        ('dashboard_runtime_readiness_view_model.runtime_readiness_summary_view_plan', 'read_project', 'Prepare runtime readiness summary view plan.'),
        ('dashboard_runtime_readiness_view_model.permission_state_view_plan', 'read_project', 'Prepare permission state view plan.'),
        ('dashboard_runtime_readiness_view_model.audit_review_queue_view_plan', 'read_project', 'Prepare audit review queue view plan.'),
        ('dashboard_runtime_readiness_view_model.safety_boundary_view_plan', 'read_project', 'Prepare safety boundary view plan.'),
        ('dashboard_runtime_readiness_view_model.orion_boundary_view_plan', 'read_project', 'Prepare ORION boundary view plan.'),
        ('dashboard_runtime_readiness_view_model.action_preview_view_plan', 'read_project', 'Prepare action preview view plan.'),
        ('dashboard_runtime_readiness_view_model.manual_approval_view_plan', 'read_project', 'Prepare manual approval view plan.'),
        ('dashboard_runtime_readiness_view_model.v1_cutline_view_plan', 'read_project', 'Prepare v1 cutline view plan.'),
        ('dashboard_runtime_readiness_view_model.control_center_payload_view_plan', 'read_project', 'Prepare Control Center payload view plan.'),
        ('dashboard_runtime_readiness_view_model.context', 'read_project', 'Show Dashboard Runtime Readiness View Model context.'),
    ]

    for action_name, permission_action, description in dashboard_runtime_readiness_view_model_actions:
        registry.register(PluginAction(name=action_name, plugin="dashboard_runtime_readiness_view_model", description=description, permission_action=permission_action, status="online", skill="aura_dashboard_runtime_readiness_view_model_foundation"))

    # Sprint 113.0 audit event review queue foundation actions.
    audit_event_review_queue_actions = [
        ('audit_event_review_queue.status', 'read_project', 'Show Audit Event Review Queue status.'),
        ('audit_event_review_queue.audit_event_intake_schema_plan', 'read_project', 'Prepare audit event intake schema plan.'),
        ('audit_event_review_queue.review_queue_state_model_plan', 'read_project', 'Prepare review queue state model plan.'),
        ('audit_event_review_queue.audit_event_triage_rule_plan', 'read_project', 'Prepare audit event triage rule plan.'),
        ('audit_event_review_queue.permission_linkage_review_plan', 'read_project', 'Prepare permission linkage review plan.'),
        ('audit_event_review_queue.runtime_boundary_review_plan', 'read_project', 'Prepare runtime boundary review plan.'),
        ('audit_event_review_queue.redaction_visibility_review_plan', 'read_project', 'Prepare redaction visibility review plan.'),
        ('audit_event_review_queue.dashboard_review_queue_payload_plan', 'read_project', 'Prepare dashboard review queue payload plan.'),
        ('audit_event_review_queue.review_outcome_catalog_plan', 'read_project', 'Prepare review outcome catalog plan.'),
        ('audit_event_review_queue.future_audit_writer_boundary_plan', 'read_project', 'Prepare future audit writer boundary plan.'),
        ('audit_event_review_queue.context', 'read_project', 'Show Audit Event Review Queue context.'),
    ]

    for action_name, permission_action, description in audit_event_review_queue_actions:
        registry.register(PluginAction(name=action_name, plugin="audit_event_review_queue", description=description, permission_action=permission_action, status="online", skill="aura_audit_event_review_queue_foundation"))

    # Sprint 112.0 runtime permission flow consolidation foundation actions.
    runtime_permission_flow_consolidation_actions = [
        ('runtime_permission_flow_consolidation.status', 'read_project', 'Show Runtime Permission Flow Consolidation status.'),
        ('runtime_permission_flow_consolidation.permission_request_schema_consolidation_plan', 'read_project', 'Prepare permission request schema consolidation plan.'),
        ('runtime_permission_flow_consolidation.permission_decision_state_model_plan', 'read_project', 'Prepare permission decision state model plan.'),
        ('runtime_permission_flow_consolidation.manual_approval_checkpoint_plan', 'read_project', 'Prepare manual approval checkpoint plan.'),
        ('runtime_permission_flow_consolidation.denial_cancellation_flow_plan', 'read_project', 'Prepare denial cancellation flow plan.'),
        ('runtime_permission_flow_consolidation.permission_scope_boundary_plan', 'read_project', 'Prepare permission scope boundary plan.'),
        ('runtime_permission_flow_consolidation.high_risk_escalation_rule_plan', 'read_project', 'Prepare high risk escalation rule plan.'),
        ('runtime_permission_flow_consolidation.approval_audit_reference_plan', 'read_project', 'Prepare approval audit reference plan.'),
        ('runtime_permission_flow_consolidation.dashboard_permission_flow_payload_plan', 'read_project', 'Prepare dashboard permission flow payload plan.'),
        ('runtime_permission_flow_consolidation.future_runtime_grant_boundary_plan', 'read_project', 'Prepare future runtime grant boundary plan.'),
        ('runtime_permission_flow_consolidation.context', 'read_project', 'Show Runtime Permission Flow Consolidation context.'),
    ]

    for action_name, permission_action, description in runtime_permission_flow_consolidation_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_permission_flow_consolidation", description=description, permission_action=permission_action, status="online", skill="aura_runtime_permission_flow_consolidation_foundation"))

    # Sprint 111.0 genesis runtime readiness next block planning foundation actions.
    genesis_runtime_readiness_next_block_planning_actions = [
        ('genesis_runtime_readiness_next_block_planning.status', 'read_project', 'Show Genesis Runtime Readiness Next Block Planning status.'),
        ('genesis_runtime_readiness_next_block_planning.next_block_sprint_candidate_plan', 'read_project', 'Prepare next block sprint candidate plan.'),
        ('genesis_runtime_readiness_next_block_planning.runtime_readiness_continuity_plan', 'read_project', 'Prepare runtime readiness continuity plan.'),
        ('genesis_runtime_readiness_next_block_planning.manual_approval_evolution_plan', 'read_project', 'Prepare manual approval evolution plan.'),
        ('genesis_runtime_readiness_next_block_planning.audit_event_evolution_plan', 'read_project', 'Prepare audit event evolution plan.'),
        ('genesis_runtime_readiness_next_block_planning.dashboard_contract_evolution_plan', 'read_project', 'Prepare dashboard contract evolution plan.'),
        ('genesis_runtime_readiness_next_block_planning.orion_boundary_planning_plan', 'read_project', 'Prepare ORION boundary planning plan.'),
        ('genesis_runtime_readiness_next_block_planning.safe_local_action_boundary_plan', 'read_project', 'Prepare safe local action boundary plan.'),
        ('genesis_runtime_readiness_next_block_planning.integration_stabilization_plan', 'read_project', 'Prepare integration stabilization plan.'),
        ('genesis_runtime_readiness_next_block_planning.v1_readiness_mapping_plan', 'read_project', 'Prepare v1 readiness mapping plan.'),
        ('genesis_runtime_readiness_next_block_planning.context', 'read_project', 'Show Genesis Runtime Readiness Next Block Planning context.'),
    ]

    for action_name, permission_action, description in genesis_runtime_readiness_next_block_planning_actions:
        registry.register(PluginAction(name=action_name, plugin="genesis_runtime_readiness_next_block_planning", description=description, permission_action=permission_action, status="online", skill="aura_genesis_runtime_readiness_next_block_planning_foundation"))

    # Sprint 110.0 review stabilization 101-110 foundation actions.
    review_stabilization_101_110_actions = [
        ('review_stabilization_101_110.status', 'read_project', 'Show Sprint 101-110 Review Stabilization status.'),
        ('review_stabilization_101_110.sprint_completion_inventory_plan', 'read_project', 'Prepare sprint completion inventory plan.'),
        ('review_stabilization_101_110.runtime_readiness_foundation_audit_plan', 'read_project', 'Prepare runtime readiness foundation audit plan.'),
        ('review_stabilization_101_110.safety_invariant_verification_plan', 'read_project', 'Prepare safety invariant verification plan.'),
        ('review_stabilization_101_110.capability_registry_delta_review_plan', 'read_project', 'Prepare capability registry delta review plan.'),
        ('review_stabilization_101_110.integration_surface_review_plan', 'read_project', 'Prepare integration surface review plan.'),
        ('review_stabilization_101_110.documentation_roadmap_consistency_plan', 'read_project', 'Prepare documentation roadmap consistency plan.'),
        ('review_stabilization_101_110.checkpoint_risk_review_plan', 'read_project', 'Prepare checkpoint risk review plan.'),
        ('review_stabilization_101_110.deferred_runtime_boundary_plan', 'read_project', 'Prepare deferred runtime boundary plan.'),
        ('review_stabilization_101_110.next_block_readiness_plan', 'read_project', 'Prepare next block readiness plan.'),
        ('review_stabilization_101_110.context', 'read_project', 'Show Sprint 101-110 Review Stabilization context.'),
    ]

    for action_name, permission_action, description in review_stabilization_101_110_actions:
        registry.register(PluginAction(name=action_name, plugin="review_stabilization_101_110", description=description, permission_action=permission_action, status="online", skill="aura_review_stabilization_101_110_foundation"))

    # Sprint 109.0 runtime safety freeze manual approval barrier foundation actions.
    runtime_safety_freeze_manual_approval_barrier_actions = [
        ('runtime_safety_freeze_manual_approval_barrier.status', 'read_project', 'Show Runtime Safety Freeze Manual Approval Barrier status.'),
        ('runtime_safety_freeze_manual_approval_barrier.safety_freeze_candidate_inventory_plan', 'read_project', 'Prepare safety freeze candidate inventory plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.manual_approval_barrier_input_plan', 'read_project', 'Prepare manual approval barrier input plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.freeze_condition_check_plan', 'read_project', 'Prepare freeze condition check plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.approval_requirement_rule_plan', 'read_project', 'Prepare approval requirement rule plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.blocked_runtime_catalog_plan', 'read_project', 'Prepare blocked runtime catalog plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.user_confirmation_barrier_plan', 'read_project', 'Prepare user confirmation barrier plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.emergency_stop_requirement_plan', 'read_project', 'Prepare emergency stop requirement plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.audit_freeze_packet_preview_plan', 'read_project', 'Prepare audit freeze packet preview plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.dashboard_barrier_payload_plan', 'read_project', 'Prepare dashboard barrier payload plan.'),
        ('runtime_safety_freeze_manual_approval_barrier.context', 'read_project', 'Show Runtime Safety Freeze Manual Approval Barrier context.'),
    ]

    for action_name, permission_action, description in runtime_safety_freeze_manual_approval_barrier_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_safety_freeze_manual_approval_barrier", description=description, permission_action=permission_action, status="online", skill="aura_runtime_safety_freeze_manual_approval_barrier_foundation"))

    # Sprint 108.0 runtime audit event packet preview foundation actions.
    runtime_audit_event_packet_preview_actions = [
        ('runtime_audit_event_packet_preview.status', 'read_project', 'Show Runtime Audit Event Packet Preview status.'),
        ('runtime_audit_event_packet_preview.audit_event_candidate_inventory_plan', 'read_project', 'Prepare audit event candidate inventory plan.'),
        ('runtime_audit_event_packet_preview.audit_event_input_snapshot_plan', 'read_project', 'Prepare audit event input snapshot plan.'),
        ('runtime_audit_event_packet_preview.runtime_reference_mapping_plan', 'read_project', 'Prepare runtime reference mapping plan.'),
        ('runtime_audit_event_packet_preview.permission_reference_mapping_plan', 'read_project', 'Prepare permission reference mapping plan.'),
        ('runtime_audit_event_packet_preview.action_preview_reference_plan', 'read_project', 'Prepare action preview reference plan.'),
        ('runtime_audit_event_packet_preview.audit_payload_shape_plan', 'read_project', 'Prepare audit payload shape plan.'),
        ('runtime_audit_event_packet_preview.audit_visibility_rule_plan', 'read_project', 'Prepare audit visibility rule plan.'),
        ('runtime_audit_event_packet_preview.retention_redaction_boundary_plan', 'read_project', 'Prepare retention redaction boundary plan.'),
        ('runtime_audit_event_packet_preview.dashboard_audit_packet_plan', 'read_project', 'Prepare dashboard audit packet plan.'),
        ('runtime_audit_event_packet_preview.context', 'read_project', 'Show Runtime Audit Event Packet Preview context.'),
    ]

    for action_name, permission_action, description in runtime_audit_event_packet_preview_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_audit_event_packet_preview", description=description, permission_action=permission_action, status="online", skill="aura_runtime_audit_event_packet_preview_foundation"))

    # Sprint 107.0 local runtime execution gate dry-run foundation actions.
    local_runtime_execution_gate_dry_run_actions = [
        ('local_runtime_execution_gate_dry_run.status', 'read_project', 'Show Local Runtime Execution Gate Dry-Run status.'),
        ('local_runtime_execution_gate_dry_run.execution_gate_candidate_inventory_plan', 'read_project', 'Prepare execution gate candidate inventory plan.'),
        ('local_runtime_execution_gate_dry_run.runtime_gate_input_contract_plan', 'read_project', 'Prepare runtime gate input contract plan.'),
        ('local_runtime_execution_gate_dry_run.gate_preflight_evaluation_plan', 'read_project', 'Prepare gate preflight evaluation plan.'),
        ('local_runtime_execution_gate_dry_run.safe_runtime_profile_reference_plan', 'read_project', 'Prepare safe runtime profile reference plan.'),
        ('local_runtime_execution_gate_dry_run.permission_gate_reference_plan', 'read_project', 'Prepare permission gate reference plan.'),
        ('local_runtime_execution_gate_dry_run.execution_gate_decision_plan', 'read_project', 'Prepare execution gate decision plan.'),
        ('local_runtime_execution_gate_dry_run.block_reason_catalog_plan', 'read_project', 'Prepare block reason catalog plan.'),
        ('local_runtime_execution_gate_dry_run.audit_gate_record_plan', 'read_project', 'Prepare audit gate record plan.'),
        ('local_runtime_execution_gate_dry_run.dashboard_gate_payload_plan', 'read_project', 'Prepare dashboard gate payload plan.'),
        ('local_runtime_execution_gate_dry_run.context', 'read_project', 'Show Local Runtime Execution Gate Dry-Run context.'),
    ]

    for action_name, permission_action, description in local_runtime_execution_gate_dry_run_actions:
        registry.register(PluginAction(name=action_name, plugin="local_runtime_execution_gate_dry_run", description=description, permission_action=permission_action, status="online", skill="aura_local_runtime_execution_gate_dry_run_foundation"))

    # Sprint 106.0 runtime action execution preview packet foundation actions.
    runtime_action_execution_preview_packet_actions = [
        ('runtime_action_execution_preview_packet.status', 'read_project', 'Show Runtime Action Execution Preview Packet status.'),
        ('runtime_action_execution_preview_packet.action_candidate_inventory_plan', 'read_project', 'Prepare action candidate inventory plan.'),
        ('runtime_action_execution_preview_packet.execution_preflight_checklist_plan', 'read_project', 'Prepare execution preflight checklist plan.'),
        ('runtime_action_execution_preview_packet.action_input_snapshot_plan', 'read_project', 'Prepare action input snapshot plan.'),
        ('runtime_action_execution_preview_packet.permission_decision_reference_plan', 'read_project', 'Prepare permission decision reference plan.'),
        ('runtime_action_execution_preview_packet.execution_step_preview_plan', 'read_project', 'Prepare execution step preview plan.'),
        ('runtime_action_execution_preview_packet.side_effect_boundary_plan', 'read_project', 'Prepare side effect boundary plan.'),
        ('runtime_action_execution_preview_packet.rollback_preview_plan', 'read_project', 'Prepare rollback preview plan.'),
        ('runtime_action_execution_preview_packet.audit_preview_record_plan', 'read_project', 'Prepare audit preview record plan.'),
        ('runtime_action_execution_preview_packet.user_confirmation_packet_plan', 'read_project', 'Prepare user confirmation packet plan.'),
        ('runtime_action_execution_preview_packet.context', 'read_project', 'Show Runtime Action Execution Preview Packet context.'),
    ]

    for action_name, permission_action, description in runtime_action_execution_preview_packet_actions:
        registry.register(PluginAction(name=action_name, plugin="runtime_action_execution_preview_packet", description=description, permission_action=permission_action, status="online", skill="aura_runtime_action_execution_preview_packet_foundation"))

    # Sprint 105.0 permission decision runtime dry-run foundation actions.
    permission_decision_runtime_dry_run_actions = [
        ('permission_decision_runtime_dry_run.status', 'read_project', 'Show Permission Decision Runtime Dry-Run status.'),
        ('permission_decision_runtime_dry_run.permission_decision_candidate_inventory_plan', 'read_project', 'Prepare permission decision candidate inventory plan.'),
        ('permission_decision_runtime_dry_run.permission_decision_input_contract_plan', 'read_project', 'Prepare permission decision input contract plan.'),
        ('permission_decision_runtime_dry_run.permission_decision_dry_run_evaluation_plan', 'read_project', 'Prepare permission decision dry-run evaluation plan.'),
        ('permission_decision_runtime_dry_run.permission_scope_mapping_plan', 'read_project', 'Prepare permission scope mapping plan.'),
        ('permission_decision_runtime_dry_run.approval_denial_outcome_plan', 'read_project', 'Prepare approval/denial outcome plan.'),
        ('permission_decision_runtime_dry_run.risk_review_rule_plan', 'read_project', 'Prepare risk review rule plan.'),
        ('permission_decision_runtime_dry_run.audit_record_blueprint_plan', 'read_project', 'Prepare audit record blueprint plan.'),
        ('permission_decision_runtime_dry_run.dashboard_review_payload_plan', 'read_project', 'Prepare dashboard review payload plan.'),
        ('permission_decision_runtime_dry_run.dry_run_safety_boundary_plan', 'read_project', 'Prepare dry-run safety boundary plan.'),
        ('permission_decision_runtime_dry_run.context', 'read_project', 'Show Permission Decision Runtime Dry-Run context.'),
    ]

    for action_name, permission_action, description in permission_decision_runtime_dry_run_actions:
        registry.register(PluginAction(name=action_name, plugin="permission_decision_runtime_dry_run", description=description, permission_action=permission_action, status="online", skill="aura_permission_decision_runtime_dry_run_foundation"))

    # Sprint 104.0 dashboard API contract consolidation foundation actions.
    dashboard_api_contract_consolidation_actions = [
        ('dashboard_api_contract_consolidation.status', 'read_project', 'Show Dashboard API Contract Consolidation status.'),
        ('dashboard_api_contract_consolidation.api_contract_inventory_plan', 'read_project', 'Prepare API contract inventory plan.'),
        ('dashboard_api_contract_consolidation.endpoint_schema_alignment_plan', 'read_project', 'Prepare endpoint schema alignment plan.'),
        ('dashboard_api_contract_consolidation.request_response_contract_plan', 'read_project', 'Prepare request/response contract plan.'),
        ('dashboard_api_contract_consolidation.permission_contract_mapping_plan', 'read_project', 'Prepare permission contract mapping plan.'),
        ('dashboard_api_contract_consolidation.dashboard_status_payload_plan', 'read_project', 'Prepare dashboard status payload plan.'),
        ('dashboard_api_contract_consolidation.error_response_contract_plan', 'read_project', 'Prepare error response contract plan.'),
        ('dashboard_api_contract_consolidation.mock_api_boundary_plan', 'read_project', 'Prepare mock API boundary plan.'),
        ('dashboard_api_contract_consolidation.frontend_backend_contract_boundary_plan', 'read_project', 'Prepare frontend/backend contract boundary plan.'),
        ('dashboard_api_contract_consolidation.contract_validation_checklist_plan', 'read_project', 'Prepare contract validation checklist plan.'),
        ('dashboard_api_contract_consolidation.context', 'read_project', 'Show Dashboard API Contract Consolidation context.'),
    ]

    for action_name, permission_action, description in dashboard_api_contract_consolidation_actions:
        registry.register(PluginAction(name=action_name, plugin="dashboard_api_contract_consolidation", description=description, permission_action=permission_action, status="online", skill="aura_dashboard_api_contract_consolidation_foundation"))

    # Sprint 103.0 local service start proposal review foundation actions.
    local_service_start_proposal_review_actions = [
        ('local_service_start_proposal_review.status', 'read_project', 'Show Local Service Start Proposal Review status.'),
        ('local_service_start_proposal_review.service_start_candidate_inventory_plan', 'read_project', 'Prepare service start candidate inventory plan.'),
        ('local_service_start_proposal_review.service_start_preflight_requirement_plan', 'read_project', 'Prepare service start preflight requirement plan.'),
        ('local_service_start_proposal_review.port_binding_review_plan', 'read_project', 'Prepare port binding review plan.'),
        ('local_service_start_proposal_review.process_launch_boundary_plan', 'read_project', 'Prepare process launch boundary plan.'),
        ('local_service_start_proposal_review.permission_requirement_plan', 'read_project', 'Prepare permission requirement plan.'),
        ('local_service_start_proposal_review.risk_classification_plan', 'read_project', 'Prepare risk classification plan.'),
        ('local_service_start_proposal_review.rollback_kill_switch_plan', 'read_project', 'Prepare rollback and kill-switch plan.'),
        ('local_service_start_proposal_review.audit_event_plan', 'read_project', 'Prepare audit event plan.'),
        ('local_service_start_proposal_review.user_approval_decision_plan', 'read_project', 'Prepare user approval decision plan.'),
        ('local_service_start_proposal_review.context', 'read_project', 'Show Local Service Start Proposal Review context.'),
    ]

    for action_name, permission_action, description in local_service_start_proposal_review_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="local_service_start_proposal_review",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_local_service_start_proposal_review_foundation",
            )
        )

    # Sprint 102.0 safe runtime configuration profile foundation actions.
    safe_runtime_configuration_profile_actions = [
        ('safe_runtime_configuration_profile.status', 'read_project', 'Show AURA Safe Runtime Configuration Profile Foundation status.'),
        ('safe_runtime_configuration_profile.configuration_profile_type_plan', 'read_project', 'Prepare configuration profile type planning.'),
        ('safe_runtime_configuration_profile.runtime_mode_policy_plan', 'read_project', 'Prepare runtime mode policy planning.'),
        ('safe_runtime_configuration_profile.service_configuration_boundary_plan', 'read_project', 'Prepare service configuration boundary planning.'),
        ('safe_runtime_configuration_profile.permission_configuration_boundary_plan', 'read_project', 'Prepare permission configuration boundary planning.'),
        ('safe_runtime_configuration_profile.file_system_configuration_boundary_plan', 'read_project', 'Prepare file system configuration boundary planning.'),
        ('safe_runtime_configuration_profile.network_configuration_boundary_plan', 'read_project', 'Prepare network configuration boundary planning.'),
        ('safe_runtime_configuration_profile.dry_run_configuration_requirement_plan', 'read_project', 'Prepare dry-run configuration requirement planning.'),
        ('safe_runtime_configuration_profile.rollout_configuration_guard_plan', 'read_project', 'Prepare rollout configuration guard planning.'),
        ('safe_runtime_configuration_profile.configuration_audit_visibility_plan', 'read_project', 'Prepare configuration audit visibility planning.'),
        ('safe_runtime_configuration_profile.safety_policy_plan', 'read_project', 'Prepare Safe Runtime Configuration Profile safety policy planning.'),
        ('safe_runtime_configuration_profile.context', 'read_project', 'Show Safe Runtime Configuration Profile Foundation context.'),
    ]

    for action_name, permission_action, description in safe_runtime_configuration_profile_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="safe_runtime_configuration_profile",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_safe_runtime_configuration_profile_foundation",
            )
        )

    # Sprint 101.0 genesis runtime readiness baseline foundation actions.
    genesis_runtime_readiness_baseline_actions = [
        ('genesis_runtime_readiness_baseline.status', 'read_project', 'Show AURA Genesis Runtime Readiness Baseline Foundation status.'),
        ('genesis_runtime_readiness_baseline.readiness_domain_inventory_plan', 'read_project', 'Prepare readiness domain inventory planning.'),
        ('genesis_runtime_readiness_baseline.runtime_candidate_classification_plan', 'read_project', 'Prepare runtime candidate classification planning.'),
        ('genesis_runtime_readiness_baseline.dry_run_prerequisite_plan', 'read_project', 'Prepare dry-run prerequisite planning.'),
        ('genesis_runtime_readiness_baseline.permission_requirement_matrix_plan', 'read_project', 'Prepare permission requirement matrix planning.'),
        ('genesis_runtime_readiness_baseline.safety_gate_alignment_plan', 'read_project', 'Prepare safety gate alignment planning.'),
        ('genesis_runtime_readiness_baseline.rollback_and_kill_switch_readiness_plan', 'read_project', 'Prepare rollback and kill-switch readiness planning.'),
        ('genesis_runtime_readiness_baseline.audit_and_observability_readiness_plan', 'read_project', 'Prepare audit and observability readiness planning.'),
        ('genesis_runtime_readiness_baseline.rollout_phase_recommendation_plan', 'read_project', 'Prepare rollout phase recommendation planning.'),
        ('genesis_runtime_readiness_baseline.block_101_110_alignment_plan', 'read_project', 'Prepare Sprint 101-110 block alignment planning.'),
        ('genesis_runtime_readiness_baseline.safety_policy_plan', 'read_project', 'Prepare Genesis Runtime Readiness Baseline safety policy planning.'),
        ('genesis_runtime_readiness_baseline.context', 'read_project', 'Show Genesis Runtime Readiness Baseline Foundation context.'),
    ]

    for action_name, permission_action, description in genesis_runtime_readiness_baseline_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="genesis_runtime_readiness_baseline",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_genesis_runtime_readiness_baseline_foundation",
            )
        )

    # Sprint 100.0 review and stabilization foundation actions.
    sprint_100_review_stabilization_actions = [
        ('sprint_100_review_stabilization.status', 'read_project', 'Show AURA Sprint 100 Review & Stabilization Foundation status.'),
        ('sprint_100_review_stabilization.sprint_block_review_plan', 'read_project', 'Prepare Sprint 91-100 block review planning.'),
        ('sprint_100_review_stabilization.completed_feature_inventory_plan', 'read_project', 'Prepare completed feature inventory planning.'),
        ('sprint_100_review_stabilization.active_vs_foundation_boundary_plan', 'read_project', 'Prepare active vs foundation-only boundary planning.'),
        ('sprint_100_review_stabilization.runtime_zero_safety_check_plan', 'read_project', 'Prepare runtime-zero safety check planning.'),
        ('sprint_100_review_stabilization.capability_registry_stabilization_plan', 'read_project', 'Prepare capability registry stabilization planning.'),
        ('sprint_100_review_stabilization.documentation_stabilization_plan', 'read_project', 'Prepare documentation stabilization planning.'),
        ('sprint_100_review_stabilization.unresolved_future_feature_plan', 'read_project', 'Prepare unresolved future feature planning.'),
        ('sprint_100_review_stabilization.roadmap_101_110_seed_plan', 'read_project', 'Prepare roadmap 101-110 seed planning.'),
        ('sprint_100_review_stabilization.sprint_100_release_readiness_plan', 'read_project', 'Prepare Sprint 100 release readiness planning.'),
        ('sprint_100_review_stabilization.safety_policy_plan', 'read_project', 'Prepare Sprint 100 review stabilization safety policy planning.'),
        ('sprint_100_review_stabilization.context', 'read_project', 'Show Sprint 100 Review & Stabilization Foundation context.'),
    ]

    for action_name, permission_action, description in sprint_100_review_stabilization_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="sprint_100_review_stabilization",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_sprint_100_review_stabilization_foundation",
            )
        )

    # Sprint 99.0 pre-runtime security audit foundation actions.
    pre_runtime_security_audit_actions = [
        ('pre_runtime_security_audit.status', 'read_project', 'Show AURA Pre-Runtime Security Audit Foundation status.'),
        ('pre_runtime_security_audit.security_audit_domain_plan', 'read_project', 'Prepare security audit domain planning.'),
        ('pre_runtime_security_audit.runtime_gate_check_plan', 'read_project', 'Prepare runtime gate check planning.'),
        ('pre_runtime_security_audit.permission_boundary_check_plan', 'read_project', 'Prepare permission boundary check planning.'),
        ('pre_runtime_security_audit.file_system_safety_check_plan', 'read_project', 'Prepare file system safety check planning.'),
        ('pre_runtime_security_audit.network_surface_check_plan', 'read_project', 'Prepare network surface check planning.'),
        ('pre_runtime_security_audit.action_execution_safety_check_plan', 'read_project', 'Prepare action execution safety check planning.'),
        ('pre_runtime_security_audit.orion_boundary_check_plan', 'read_project', 'Prepare ORION boundary check planning.'),
        ('pre_runtime_security_audit.audit_visibility_check_plan', 'read_project', 'Prepare audit visibility check planning.'),
        ('pre_runtime_security_audit.stabilization_readiness_check_plan', 'read_project', 'Prepare Sprint 100 stabilization readiness check planning.'),
        ('pre_runtime_security_audit.safety_policy_plan', 'read_project', 'Prepare pre-runtime security audit safety policy planning.'),
        ('pre_runtime_security_audit.context', 'read_project', 'Show Pre-Runtime Security Audit Foundation context.'),
    ]

    for action_name, permission_action, description in pre_runtime_security_audit_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="pre_runtime_security_audit",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_pre_runtime_security_audit_foundation",
            )
        )

    # Sprint 98.0 runtime action queue review layer foundation actions.
    runtime_action_queue_review_layer_actions = [
        ('runtime_action_queue_review_layer.status', 'read_project', 'Show AURA Runtime Action Queue Review Layer Foundation status.'),
        ('runtime_action_queue_review_layer.action_queue_item_blueprint_plan', 'read_project', 'Prepare action queue item blueprint planning.'),
        ('runtime_action_queue_review_layer.queue_state_blueprint_plan', 'read_project', 'Prepare queue state blueprint planning.'),
        ('runtime_action_queue_review_layer.review_priority_rule_plan', 'read_project', 'Prepare review priority rule planning.'),
        ('runtime_action_queue_review_layer.dependency_blocker_contract_plan', 'read_project', 'Prepare dependency and blocker contract planning.'),
        ('runtime_action_queue_review_layer.permission_link_requirement_plan', 'read_project', 'Prepare permission link requirement planning.'),
        ('runtime_action_queue_review_layer.execution_preflight_check_blueprint_plan', 'read_project', 'Prepare execution preflight check blueprint planning.'),
        ('runtime_action_queue_review_layer.approval_denial_transition_rule_plan', 'read_project', 'Prepare approval and denial transition rule planning.'),
        ('runtime_action_queue_review_layer.timeout_expiry_policy_plan', 'read_project', 'Prepare timeout and expiry policy planning.'),
        ('runtime_action_queue_review_layer.runtime_action_audit_visibility_plan', 'read_project', 'Prepare runtime action audit visibility planning.'),
        ('runtime_action_queue_review_layer.safety_policy_plan', 'read_project', 'Prepare runtime action queue review layer safety policy planning.'),
        ('runtime_action_queue_review_layer.context', 'read_project', 'Show Runtime Action Queue Review Layer Foundation context.'),
    ]

    for action_name, permission_action, description in runtime_action_queue_review_layer_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="runtime_action_queue_review_layer",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_runtime_action_queue_review_layer_foundation",
            )
        )

    # Sprint 97.0 controlled file write approval draft foundation actions.
    controlled_file_write_approval_draft_actions = [
        ('controlled_file_write_approval_draft.status', 'read_project', 'Show AURA Controlled File Write Approval Draft Foundation status.'),
        ('controlled_file_write_approval_draft.file_write_proposal_draft_plan', 'read_project', 'Prepare file write proposal draft planning.'),
        ('controlled_file_write_approval_draft.target_path_policy_plan', 'read_project', 'Prepare target path policy planning.'),
        ('controlled_file_write_approval_draft.diff_preview_contract_plan', 'read_project', 'Prepare diff preview contract planning.'),
        ('controlled_file_write_approval_draft.overwrite_rule_plan', 'read_project', 'Prepare overwrite rule planning.'),
        ('controlled_file_write_approval_draft.backup_requirement_plan', 'read_project', 'Prepare backup requirement planning.'),
        ('controlled_file_write_approval_draft.approval_checklist_plan', 'read_project', 'Prepare approval checklist planning.'),
        ('controlled_file_write_approval_draft.rollback_note_plan', 'read_project', 'Prepare rollback note planning.'),
        ('controlled_file_write_approval_draft.file_write_audit_visibility_plan', 'read_project', 'Prepare file write audit visibility planning.'),
        ('controlled_file_write_approval_draft.safety_policy_plan', 'read_project', 'Prepare file write safety policy planning.'),
        ('controlled_file_write_approval_draft.context', 'read_project', 'Show Controlled File Write Approval Draft Foundation context.'),
    ]

    for action_name, permission_action, description in controlled_file_write_approval_draft_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="controlled_file_write_approval_draft",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_controlled_file_write_approval_draft_foundation",
            )
        )

    # Sprint 96.0 safe local web runtime gate foundation actions.
    safe_local_web_runtime_gate_actions = [
        ('safe_local_web_runtime_gate.status', 'read_project', 'Show AURA Safe Local Web Runtime Gate Foundation status.'),
        ('safe_local_web_runtime_gate.localhost_binding_policy_plan', 'read_project', 'Prepare localhost binding policy planning.'),
        ('safe_local_web_runtime_gate.port_policy_plan', 'read_project', 'Prepare port policy planning.'),
        ('safe_local_web_runtime_gate.permission_requirement_plan', 'read_project', 'Prepare web runtime permission requirement planning.'),
        ('safe_local_web_runtime_gate.runtime_preflight_check_plan', 'read_project', 'Prepare runtime preflight check planning.'),
        ('safe_local_web_runtime_gate.start_stop_proposal_contract_plan', 'read_project', 'Prepare start/stop proposal contract planning.'),
        ('safe_local_web_runtime_gate.route_boundary_policy_plan', 'read_project', 'Prepare route boundary policy planning.'),
        ('safe_local_web_runtime_gate.static_asset_boundary_policy_plan', 'read_project', 'Prepare static asset boundary policy planning.'),
        ('safe_local_web_runtime_gate.kill_switch_policy_plan', 'read_project', 'Prepare kill switch policy planning.'),
        ('safe_local_web_runtime_gate.web_runtime_audit_visibility_plan', 'read_project', 'Prepare web runtime audit visibility planning.'),
        ('safe_local_web_runtime_gate.safety_policy_plan', 'read_project', 'Prepare safe local web runtime gate safety policy planning.'),
        ('safe_local_web_runtime_gate.context', 'read_project', 'Show Safe Local Web Runtime Gate Foundation context.'),
    ]

    for action_name, permission_action, description in safe_local_web_runtime_gate_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="safe_local_web_runtime_gate",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_safe_local_web_runtime_gate_foundation",
            )
        )

    # Sprint 95.0 chat session persistence planner foundation actions.
    chat_session_persistence_planner_actions = [
        ('chat_session_persistence_planner.status', 'read_project', 'Show AURA Chat Session Persistence Planner Foundation status.'),
        ('chat_session_persistence_planner.session_record_blueprint_plan', 'read_project', 'Prepare session record blueprint planning.'),
        ('chat_session_persistence_planner.storage_boundary_blueprint_plan', 'read_project', 'Prepare storage boundary blueprint planning.'),
        ('chat_session_persistence_planner.retention_policy_blueprint_plan', 'read_project', 'Prepare retention policy blueprint planning.'),
        ('chat_session_persistence_planner.privacy_redaction_rule_plan', 'read_project', 'Prepare privacy redaction rule planning.'),
        ('chat_session_persistence_planner.session_lifecycle_blueprint_plan', 'read_project', 'Prepare session lifecycle blueprint planning.'),
        ('chat_session_persistence_planner.recovery_index_blueprint_plan', 'read_project', 'Prepare recovery index blueprint planning.'),
        ('chat_session_persistence_planner.export_migration_note_plan', 'read_project', 'Prepare export and migration note planning.'),
        ('chat_session_persistence_planner.safety_policy_plan', 'read_project', 'Prepare chat persistence safety policy planning.'),
        ('chat_session_persistence_planner.status_packet', 'read_project', 'Prepare chat session persistence status packet.'),
        ('chat_session_persistence_planner.context', 'read_project', 'Show Chat Session Persistence Planner Foundation context.'),
    ]

    for action_name, permission_action, description in chat_session_persistence_planner_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="chat_session_persistence_planner",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_chat_session_persistence_planner_foundation",
            )
        )

    # Sprint 94.0 permission request review queue foundation actions.
    permission_request_review_queue_actions = [
        ('permission_request_review_queue.status', 'read_project', 'Show AURA Permission Request Review Queue Foundation status.'),
        ('permission_request_review_queue.request_blueprint_plan', 'read_project', 'Prepare permission request blueprint planning.'),
        ('permission_request_review_queue.queue_state_blueprint_plan', 'read_project', 'Prepare queue state blueprint planning.'),
        ('permission_request_review_queue.review_packet_field_plan', 'read_project', 'Prepare review packet field planning.'),
        ('permission_request_review_queue.scope_boundary_plan', 'read_project', 'Prepare permission scope boundary planning.'),
        ('permission_request_review_queue.decision_proposal_contract_plan', 'read_project', 'Prepare decision proposal contract planning.'),
        ('permission_request_review_queue.reviewer_checklist_plan', 'read_project', 'Prepare reviewer checklist planning.'),
        ('permission_request_review_queue.audit_visibility_field_plan', 'read_project', 'Prepare audit visibility field planning.'),
        ('permission_request_review_queue.safety_policy_plan', 'read_project', 'Prepare permission request safety policy planning.'),
        ('permission_request_review_queue.status_packet', 'read_project', 'Prepare permission request review queue status packet.'),
        ('permission_request_review_queue.context', 'read_project', 'Show Permission Request Review Queue Foundation context.'),
    ]

    for action_name, permission_action, description in permission_request_review_queue_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="permission_request_review_queue",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_permission_request_review_queue_foundation",
            )
        )

    # Sprint 93.0 control center data aggregator foundation actions.
    control_center_data_aggregator_actions = [
        ('control_center_data_aggregator.status', 'read_project', 'Show AURA Control Center Data Aggregator Foundation status.'),
        ('control_center_data_aggregator.catalog_plan', 'read_project', 'Prepare Control Center aggregation packet catalog planning.'),
        ('control_center_data_aggregator.atlas_core_packet_plan', 'read_project', 'Prepare ATLAS core packet planning.'),
        ('control_center_data_aggregator.orion_client_packet_plan', 'read_project', 'Prepare ORION client packet planning.'),
        ('control_center_data_aggregator.client_bridge_packet_plan', 'read_project', 'Prepare client bridge packet planning.'),
        ('control_center_data_aggregator.dashboard_view_packet_plan', 'read_project', 'Prepare dashboard view packet planning.'),
        ('control_center_data_aggregator.permission_scope_packet_plan', 'read_project', 'Prepare permission scope packet planning.'),
        ('control_center_data_aggregator.health_snapshot_packet_plan', 'read_project', 'Prepare health snapshot packet planning.'),
        ('control_center_data_aggregator.audit_event_visibility_packet_plan', 'read_project', 'Prepare audit event visibility packet planning.'),
        ('control_center_data_aggregator.safety_policy_plan', 'read_project', 'Prepare Control Center data aggregator safety policy planning.'),
        ('control_center_data_aggregator.context', 'read_project', 'Show Control Center Data Aggregator Foundation context.'),
    ]

    for action_name, permission_action, description in control_center_data_aggregator_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="control_center_data_aggregator",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_control_center_data_aggregator_foundation",
            )
        )

    # Sprint 92.0 local console API schema foundation actions.
    local_console_api_schema_actions = [
        ('local_console_api_schema.status', 'read_project', 'Show AURA Local Console API Schema Foundation status.'),
        ('local_console_api_schema.catalog_plan', 'read_project', 'Prepare Local Console API schema catalog planning.'),
        ('local_console_api_schema.endpoint_blueprint_plan', 'read_project', 'Prepare Local Console endpoint blueprint planning.'),
        ('local_console_api_schema.response_envelope_plan', 'read_project', 'Prepare Local Console response envelope planning.'),
        ('local_console_api_schema.request_schema_blueprint_plan', 'read_project', 'Prepare Local Console request schema blueprint planning.'),
        ('local_console_api_schema.validation_rule_plan', 'read_project', 'Prepare Local Console validation rule planning.'),
        ('local_console_api_schema.permission_boundary_schema_plan', 'read_project', 'Prepare Local Console permission boundary schema planning.'),
        ('local_console_api_schema.error_contract_plan', 'read_project', 'Prepare Local Console error contract planning.'),
        ('local_console_api_schema.schema_versioning_plan', 'read_project', 'Prepare Local Console schema versioning planning.'),
        ('local_console_api_schema.safety_policy_plan', 'read_project', 'Prepare Local Console API schema safety policy planning.'),
        ('local_console_api_schema.context', 'read_project', 'Show Local Console API Schema Foundation context.'),
    ]

    for action_name, permission_action, description in local_console_api_schema_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="local_console_api_schema",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_local_console_api_schema_foundation",
            )
        )

    # Sprint 91.0 local console static prototype foundation actions.
    local_console_static_prototype_actions = [
        ('local_console_static_prototype.status', 'read_project', 'Show AURA Local Console Static Prototype Foundation status.'),
        ('local_console_static_prototype.structure_plan', 'read_project', 'Prepare static prototype structure planning.'),
        ('local_console_static_prototype.static_page_blueprint_plan', 'read_project', 'Prepare static page blueprint planning.'),
        ('local_console_static_prototype.static_asset_blueprint_plan', 'read_project', 'Prepare static asset blueprint planning.'),
        ('local_console_static_prototype.panel_layout_blueprint_plan', 'read_project', 'Prepare panel layout blueprint planning.'),
        ('local_console_static_prototype.route_static_mapping_plan', 'read_project', 'Prepare route-to-static-page mapping planning.'),
        ('local_console_static_prototype.data_placeholder_contract_plan', 'read_project', 'Prepare data placeholder contract planning.'),
        ('local_console_static_prototype.theme_token_blueprint_plan', 'read_project', 'Prepare theme token blueprint planning.'),
        ('local_console_static_prototype.accessibility_blueprint_plan', 'read_project', 'Prepare accessibility blueprint planning.'),
        ('local_console_static_prototype.safety_policy_plan', 'read_project', 'Prepare static prototype safety policy planning.'),
        ('local_console_static_prototype.context', 'read_project', 'Show Local Console Static Prototype Foundation context.'),
    ]

    for action_name, permission_action, description in local_console_static_prototype_actions:
        registry.register(
            PluginAction(
                name=action_name,
                plugin="local_console_static_prototype",
                description=description,
                permission_action=permission_action,
                status="online",
                skill="aura_local_console_static_prototype_foundation",
            )
        )

    return registry
