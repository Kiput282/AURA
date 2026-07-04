from loguru import logger

from aura.plugins.plugin import Plugin


class PluginManager:
    """
    Manages AURA plugins.

    Responsibilities:
    - register plugins
    - start plugins
    - stop plugins
    - list plugin statuses
    """

    def __init__(self):
        self.plugins: dict[str, Plugin] = {}

    def register(self, plugin: Plugin) -> None:
        if plugin.name in self.plugins:
            raise ValueError(f"Plugin already registered: {plugin.name}")

        self.plugins[plugin.name] = plugin
        logger.info(f"Plugin registered: {plugin.name} v{plugin.version}")

    def start_all(self) -> None:
        for plugin in self.plugins.values():
            logger.info(f"Starting plugin: {plugin.name}")
            plugin.start()

    def stop_all(self) -> None:
        for plugin in self.plugins.values():
            logger.info(f"Stopping plugin: {plugin.name}")
            plugin.stop()

    def list_plugins(self) -> list[dict[str, str]]:
        return [
            {
                "name": plugin.name,
                "version": plugin.version,
                "description": plugin.description,
                "status": plugin.status(),
            }
            for plugin in self.plugins.values()
        ]
