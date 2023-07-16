from src.config.classes import Config, TelegramConfig, OpenAIConfig, LoggerConfig, LuhnConfig, Plugin
import os

config = Config(
    telegram=TelegramConfig(
        token=os.getenv("TELEGRAM_TOKEN", default="")
    ),
    openai=OpenAIConfig(
        token=os.getenv("OPENAI_TOKEN", default=""),
        model="gpt-3.5-turbo-16k",
    ),
    logger=LoggerConfig(
        log_file='data/log_file.log',
        encoding='utf-8',
        level='DEBUG',
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        date_format="%d/%b/%Y %H:%M:%S"
    ),
    luhn=LuhnConfig(
        threshold=6,
        min_sentences_count=1,
        path_to_file="data/document.txt",
        path_to_output="data/document_abstract.txt"
    ),
    plugins_directory="data/plugins_configs",
    plugins_source_directory="src/app/plugins",
    plugins=[]
)
