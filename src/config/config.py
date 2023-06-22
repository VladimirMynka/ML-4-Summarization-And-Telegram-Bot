from src.config.classes import Config, TelegramConfig, OpenAIConfig, LoggerConfig, LuhnConfig, Plugin

config = Config(
    telegram=TelegramConfig(
        token="your token"
    ),
    openai=OpenAIConfig(
        token="your token",
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
    ),
    plugins=[
        Plugin(
            name="usual_communication",
            url=None,
            description="User hasn't any specific questions. Write your answer as ChatGPT model into RESPONSE field"
        ),
        Plugin(
            name="restart_dialog",
            url=None,
            description="User wants to restart dialog and clear context. "
                        "He writes something like it: `stop`, `restart`, `I want to restart our dialog`. "
                        "Keep RESPONSE field empty"
        ),
        Plugin(
            name="luhn_summarize",
            url="http://127.0.0.1:5017/",
            description="User want to activate summarize mode. "
                        "His message looks like `i want you summarize my next message` or "
                        "`summarize it:` or `Выдели из моего следующего сообщения главную мысль`. "
                        "Write for him that mode activated in RESPONSE field or keep it empty. "
                        "If last intent is luhn_summarize then keep it while user will not write `stop summarize mode`"
        )
    ]
)
