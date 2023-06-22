import logging
from src.config.classes import LoggerConfig
from src.config.config import config


def init_logging(config: LoggerConfig = None):
    """
    Configure logger for this project

    :param config: config for logging
    """
    if config is None:
        config = LoggerConfig()
    logging.basicConfig(
        filename=config.log_file,
        encoding=config.encoding,
        level=config.level,
        format=config.format,
        datefmt=config.date_format
    )


def get_available_intents():
    return "[" + ", ".join([intent.name for intent in config.plugins]) + "]"


def get_intents_description():
    return "\n".join(["- " + intent.name + ": " + intent.description for intent in config.plugins])
