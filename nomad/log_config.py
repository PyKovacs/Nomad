import os
from logging import Formatter, Logger, handlers
from pathlib import Path

APP_DIR = Path.home() / "nomad"
LOG_PATH = APP_DIR / "log" / "nomad.log"


def get_logger(name: str, log_level: str = "INFO") -> Logger:
    """
    Get a logger with the specified name.
    """
    # create nomad folder in /var/log
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

    formatter = Formatter(f"{name}: %(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")
    logger = Logger(name)

    ### create a handler
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    handler = handlers.TimedRotatingFileHandler(LOG_PATH, when="midnight", backupCount=30)
    handler.setLevel(log_level)

    ### create a formatter
    handler.setFormatter(formatter)

    ### add the handler to the logger
    logger.addHandler(handler)

    return logger
