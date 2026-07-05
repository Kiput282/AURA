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
            description="Open an application when explicitly requested.",
            permission_action="open_app",
            status="planned",
            skill="app_launcher",
        )
    )

    registry.register(
        PluginAction(
            name="browser.open",
            plugin="app_launcher",
            description="Open a browser or URL when explicitly requested.",
            permission_action="open_browser",
            status="planned",
            skill="app_launcher",
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
            description="Analyze the user's screen when screen runtime is enabled.",
            permission_action="screen_analyze",
            status="foundation",
            skill="screen_analyzer",
        )
    )

    registry.register(
        PluginAction(
            name="camera.analyze",
            plugin="vision",
            description="Analyze camera/environment input when camera runtime is enabled.",
            permission_action="camera_analyze",
            status="foundation",
            skill="camera_analyzer",
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
            description="Speak through text-to-speech output when voice mode is enabled.",
            permission_action="speaker_speak",
            status="planned",
            skill="voice_interaction",
        )
    )

    registry.register(
        PluginAction(
            name="voice.listen",
            plugin="voice",
            description="Listen through microphone for voice interaction.",
            permission_action="microphone_listen",
            status="planned",
            skill="voice_interaction",
        )
    )

    registry.register(
        PluginAction(
            name="avatar.control",
            plugin="avatar",
            description="Control AURA avatar state, expression, or gesture.",
            permission_action="prepare_file",
            status="planned",
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
