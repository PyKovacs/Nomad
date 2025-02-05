import os
from logging import Formatter, Logger, handlers

LOG_FILE = "logs/nomad.log"


def get_logger(name: str, log_level: str = "INFO") -> Logger:
    """
    Get a logger with the specified name.
    """
    formatter = Formatter(f"{name}: %(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")
    logger = Logger(name)

    ### create a handler
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    handler = handlers.TimedRotatingFileHandler(LOG_FILE, when="midnight", backupCount=30)
    handler.setLevel(log_level)

    ### create a formatter
    handler.setFormatter(formatter)

    ### add the handler to the logger
    logger.addHandler(handler)

    return logger
