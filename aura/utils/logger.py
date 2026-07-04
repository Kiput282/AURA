from pathlib import Path

from loguru import logger


def setup_logger(project_root: Path) -> None:
    """
    Configure AURA logger.

    This should be initialized as early as possible by AuraApp,
    so all app, boot, event, and service logs are captured.
    """

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "aura.log"

    logger.add(
        log_file,
        rotation="1 MB",
        retention="7 days",
        level="INFO",
    )

    logger.info("Logger initialized")
