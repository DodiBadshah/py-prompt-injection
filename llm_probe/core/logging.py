# llm_probe/core/logging.py
"""
Logging configuration for py-prompt-injection.

Sets up loguru as the single logging system. Every module imports the
pre-configured logger from here. Never import Python's built-in logging
module anywhere in this codebase.

Usage:
    from llm_probe.core.logging import logger

    logger.info("Starting test run")
    logger.warning("Rate limit approaching")
    logger.error("Adapter failed", exc_info=True)
"""

import sys
from pathlib import Path

from loguru import logger

from llm_probe.core.config import settings

# ── Constants ────────────────────────────────────────────────────────────────

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "llm_probe.log"

# Console format: colored, concise, human-readable during a live run.
CONSOLE_FORMAT = (
    "<green>{time:HH:mm:ss}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
    "<level>{message}</level>"
)

# File format: plain text, full timestamp, for post-run review.
FILE_FORMAT = (
    "{time:YYYY-MM-DD HH:mm:ss} | "
    "{level: <8} | "
    "{name}:{line} | "
    "{message}"
)


def setup_logging(log_level: str = "INFO") -> None:
    """
    Configure loguru sinks for console and file output.

    Call this once at application startup (from cli/main.py).
    Calling it more than once is safe -- existing handlers are
    removed before new ones are added.

    Args:
        log_level: Minimum log level to emit. Defaults to INFO.
                   Accepts DEBUG, INFO, WARNING, ERROR, CRITICAL.
    """
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    # Remove default loguru handler before adding our own.
    logger.remove()

    # Console sink -- colored output to stdout.
    logger.add(
        sys.stdout,
        format=CONSOLE_FORMAT,
        level=log_level.upper(),
        colorize=True,
        backtrace=False,
        diagnose=False,
    )

    # File sink -- plain text, rotating at 10 MB, keeping 7 days.
    logger.add(
        LOG_FILE,
        format=FILE_FORMAT,
        level="DEBUG",
        rotation="10 MB",
        retention="7 days",
        encoding="utf-8",
        backtrace=True,
        diagnose=True,
    )

    logger.debug(
        f"Logging initialised | level={log_level.upper()} | file={LOG_FILE}"
    )


# Re-export logger so every module only needs one import.
__all__ = ["logger", "setup_logging"]