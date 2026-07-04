from pathlib import Path
import sys

from loguru import logger


def disable_logging() -> None:
    """
    Disable all Loguru sinks.

    Used by CLI commands that should produce clean user-facing output.
    """
    logger.remove()


def setup_logger(project_root: Path, *, console: bool = False) -> None:
    """
    Configure AURA logger.

    By default, logs are written to file only.
    Console logging can be enabled explicitly when needed.
    """

    logger.remove()

    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_file = logs_dir / "aura.log"

    logger.add(
        log_file,
        rotation="1 MB",
        retention="7 days",
        level="INFO",
    )

    if console:
        logger.add(sys.stderr, level="INFO")

    logger.info("Logger initialized")
