from pathlib import Path

import yaml
from loguru import logger

from aura.events.event import Event
from aura.events.event_bus import EventBus


class AuraBoot:
    """
    AURA Core Boot System.

    Responsible for:
    - loading configuration
    - loading identity
    - preparing logger
    - registering boot events
    - running the structured boot sequence
    """

    def __init__(self, event_bus: EventBus):
        self.project_root = Path(__file__).resolve().parents[2]
        self.config_path = self.project_root / "aura" / "config" / "settings.yaml"
        self.identity_path = self.project_root / "aura" / "personality" / "identity.yaml"

        self.config = {}
        self.identity = {}
        self.event_bus = event_bus

    def load_yaml(self, path: Path) -> dict:
        if not path.exists():
            raise FileNotFoundError(f"Required file not found: {path}")

        with path.open("r", encoding="utf-8") as file:
            return yaml.safe_load(file) or {}

    def setup_logger(self):
        logs_dir = self.project_root / "logs"
        logs_dir.mkdir(exist_ok=True)

        log_file = logs_dir / "aura.log"

        logger.add(
            log_file,
            rotation="1 MB",
            retention="7 days",
            level="INFO",
        )

        logger.info("Logger initialized")

    def load_config(self):
        self.config = self.load_yaml(self.config_path)
        logger.info("Config loaded")

    def load_identity(self):
        self.identity = self.load_yaml(self.identity_path)
        logger.info("Identity loaded")

    def register_core_events(self):
        self.event_bus.subscribe("aura.boot.started", self.on_boot_started)
        self.event_bus.subscribe("aura.boot.ready", self.on_boot_ready)
        logger.info("Core event handlers registered")

    def on_boot_started(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def on_boot_ready(self, event: Event):
        logger.info(f"Event handled: {event.name}")

    def run(self):
        self.setup_logger()
        self.register_core_events()

        self.event_bus.emit(
            Event(
                name="aura.boot.started",
                source="aura.core.boot",
                payload={"status": "starting"},
            )
        )

        self.load_config()
        self.load_identity()

        name = self.identity.get("name", "AURA")
        version = self.identity.get("version", "unknown")
        codename = self.identity.get("codename", "unknown")
        creator = self.identity.get("creator", "Kiput")
        motto = self.identity.get("motto", "Grow Together")

        print("AURA Core Boot")
        print("================")
        print(f"Name     : {name}")
        print(f"Version  : {version}")
        print(f"Codename : {codename}")
        print(f"Creator  : {creator}")
        print(f"Motto    : {motto}")
        print("Status   : READY")
        print()
        print(f"Hello, {creator}.")
        print("I'm AURA.")
        print("Core systems are online.")

        self.event_bus.emit(
            Event(
                name="aura.boot.ready",
                source="aura.core.boot",
                payload={"status": "ready", "version": version},
            )
        )

        logger.info("AURA boot sequence completed successfully")
