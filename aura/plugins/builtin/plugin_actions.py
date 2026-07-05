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
