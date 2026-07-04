from loguru import logger

from aura.core.boot import AuraBoot
from aura.events.event import Event
from aura.events.event_bus import EventBus


class AuraApp:
    """
    Main application container for AURA.

    Responsibilities:
    - own the shared EventBus
    - initialize core systems
    - start the boot sequence
    - become the future home for plugins, memory, voice, vision, and services
    """

    def __init__(self):
        self.event_bus = EventBus()
        self.boot = AuraBoot(event_bus=self.event_bus)

    def register_app_events(self):
        self.event_bus.subscribe("aura.app.starting", self.on_app_starting)
        self.event_bus.subscribe("aura.app.started", self.on_app_started)

    def on_app_starting(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def on_app_started(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def start(self):
        self.register_app_events()

        self.event_bus.emit(
            Event(
                name="aura.app.starting",
                source="aura.core.app",
                payload={"status": "starting"},
            )
        )

        self.boot.run()

        self.event_bus.emit(
            Event(
                name="aura.app.started",
                source="aura.core.app",
                payload={"status": "started"},
            )
        )
