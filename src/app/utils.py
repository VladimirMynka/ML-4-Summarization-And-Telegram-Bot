import json
import logging
import os

from src.config.classes import LoggerConfig, Plugin, Config


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


def json_load_file(path: str):
    with open(path, 'r') as f:
        json_content = json.load(f)
    return json_content


def update_config(config: Config):
    paths = os.listdir(config.plugins_directory)
    plugins = []
    for path in paths:
        if path.split(".")[-1] != "json":
            continue
        content = json_load_file(os.path.join(config.plugins_directory, path))
        content["name"] = path.split(".")[0]
        plugins.append(Plugin(**content))

    config.plugins = plugins
    return config


def get_available_intents(config: Config):
    return "[\"" + "\", \"".join([intent.name for intent in config.plugins]) + "\"]"


def get_intents_description(config: Config):
    return "\n".join(["- " + intent.name + ": " + intent.description for intent in config.plugins])
