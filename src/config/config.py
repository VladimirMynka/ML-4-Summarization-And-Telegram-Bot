from src.config.classes import Config, TelegramConfig, OpenAIConfig, LoggerConfig, LuhnConfig

config = Config(
    telegram=TelegramConfig(
        token="your token"
    ),
    openai=OpenAIConfig(
        token="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",
        model="gpt-3.5-turbo",
    ),
    logger=LoggerConfig(
        log_file='data/log_file.log',
        encoding='utf-8',
        level='INFO',
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        date_format="%d/%b/%Y %H:%M:%S"
    ),
    luhn=LuhnConfig(
        threshold=2,
        min_sentences_count=1,
        path_to_file="data/document.txt",
        path_to_output="data/document_abstract.txt"
    )
)
