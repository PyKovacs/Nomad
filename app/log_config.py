from logging import Formatter, Logger, handlers


def get_logger(name: str) -> Logger:
    """
    Get a logger with the specified name.
    """
    ### specify the logger message format to be "NAME: TIME - LEVEL - MESSAGE"
    ### specify the logger date format to be "%d-%m-%Y %H:%M:%S"
    formatter = Formatter(f"{name}: %(asctime)s - %(levelname)s - %(message)s", "%d-%m-%Y %H:%M:%S")

    ### create a logger
    logger = Logger(name)

    ### create a handler
    handler = handlers.TimedRotatingFileHandler("nomad.log", when="midnight", backupCount=30)
    handler.setLevel("DEBUG")

    ### create a formatter
    handler.setFormatter(formatter)

    ### add the handler to the logger
    logger.addHandler(handler)

    return logger
