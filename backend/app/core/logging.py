"""Centralized logging configuration."""

import logging
import sys
from pathlib import Path

from app.core.config import settings

# Create logs directory if it doesn't exist
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Configure logging format
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create formatter
formatter = logging.Formatter(LOG_FORMAT, datefmt=DATE_FORMAT)

# Create logger
logger = logging.getLogger("smartskale")
logger.setLevel(getattr(logging, settings.log_level))

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, settings.log_level))
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler
file_handler = logging.FileHandler(LOGS_DIR / "app.log")
file_handler.setLevel(getattr(logging, settings.log_level))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(f"smartskale.{name}")
