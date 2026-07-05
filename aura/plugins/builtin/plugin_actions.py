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

    return registry
