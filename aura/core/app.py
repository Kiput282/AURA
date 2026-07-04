from pathlib import Path

from loguru import logger

from aura.core.boot import AuraBoot
from aura.core.health import HealthCheck
from aura.events.event import Event
from aura.events.event_bus import EventBus
from aura.utils.logger import setup_logger


class AuraApp:
    """
    Main application container for AURA.

    Responsibilities:
    - initialize logging early
    - own the shared EventBus
    - initialize core systems
    - start the boot sequence
    - run health checks
    - become the future home for plugins, memory, voice, vision, and services
    """

    def __init__(self):
        self.project_root = Path(__file__).resolve().parents[2]

        setup_logger(self.project_root)

        self.event_bus = EventBus()
        self.health = HealthCheck()
        self.boot = AuraBoot(event_bus=self.event_bus)

    def register_app_events(self):
        self.event_bus.subscribe("aura.app.starting", self.on_app_starting)
        self.event_bus.subscribe("aura.app.started", self.on_app_started)
        self.event_bus.subscribe("aura.health.checked", self.on_health_checked)

    def on_app_starting(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def on_app_started(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def on_health_checked(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def run_health_check(self):
        self.health.add("Core", "OK", "AuraApp initialized")
        self.health.add("Boot", "OK", "Boot sequence completed")
        self.health.add("Config", "OK", "settings.yaml loaded")
        self.health.add("Identity", "OK", "identity.yaml loaded")
        self.health.add("Events", "OK", "EventBus online")
        self.health.add("Memory", "NOT_READY", "Memory system not implemented yet")
        self.health.add("Plugins", "NOT_READY", "Plugin system not implemented yet")

        self.health.print_summary()

        self.event_bus.emit(
            Event(
                name="aura.health.checked",
                source="aura.core.app",
                payload={
                    "items": [
                        {
                            "name": item.name,
                            "status": item.status,
                            "detail": item.detail,
                        }
                        for item in self.health.summary()
                    ]
                },
            )
        )

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
        self.run_health_check()

        self.event_bus.emit(
            Event(
                name="aura.app.started",
                source="aura.core.app",
                payload={"status": "started"},
            )
        )
