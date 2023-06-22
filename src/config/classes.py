from dataclasses import dataclass


@dataclass
class TelegramConfig:
    token: str


@dataclass
class OpenAIConfig:
    token: str
    model: str


@dataclass
class LoggerConfig:
    log_file: str = 'data/log_file.log'
    encoding: str = 'utf-8'
    level: str = 'INFO'
    format: str = "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s"
    date_format: str = "%d/%b/%Y %H:%M:%S"


@dataclass
class LuhnConfig:
    threshold: float
    min_sentences_count: int
    path_to_file: str
    path_to_output: str


@dataclass
class Plugin:
    name: str
    url: str
    description: str


@dataclass
class Config:
    telegram: TelegramConfig
    openai: OpenAIConfig
    logger: LoggerConfig
    luhn: LuhnConfig
