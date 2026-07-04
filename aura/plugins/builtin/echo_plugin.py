from loguru import logger

from aura.plugins.plugin import Plugin


class EchoPlugin(Plugin):
    name = "echo"
    version = "0.1.0"
    description = "Simple built-in test plugin for AURA."

    def start(self) -> None:
        logger.info("EchoPlugin started")

    def stop(self) -> None:
        logger.info("EchoPlugin stopped")

    def status(self) -> str:
        return "OK"
