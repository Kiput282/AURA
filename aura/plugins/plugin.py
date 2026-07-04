from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    Base class for all AURA plugins.

    Every plugin should introduce itself to AURA through this interface.
    """

    name: str = "unknown"
    version: str = "0.0.0"
    description: str = ""

    @abstractmethod
    def start(self) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    def status(self) -> str:
        return "OK"
