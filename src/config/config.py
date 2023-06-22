from src.config.classes import Config, TelegramConfig, OpenAIConfig, LoggerConfig, LuhnConfig, Plugin

config = Config(
    telegram=TelegramConfig(
        token="6181114033:AAG6ImZ_hjW1rDE-tSzk6O4SjzTiH3krpTc"
    ),
    openai=OpenAIConfig(
        token="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",
        model="gpt-3.5-turbo",
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
                        "His message looks like `i want you summarize my message` or "
                        "`summarize it:` or `Выдели из моего сообщения главную мысль`. "
                        "Write for him that mode activated in RESPONSE field or keep it empty. "
                        "Also add a new field LUHN_THRESHOLD into your answer and set it 2 by default "
                        "but change if user will ask`"
        ),
        Plugin(
            name="stable_diffusion",
            url="http://127.0.0.1:6017/",
            description="User want to generate image. "
                        "Add new field `STABLE DIFFUSION` into your json and paste request for stable"
                        "diffusion model into it. If you want know more information for generating, you can"
                        "ask it in RESPONSE but you must generate request for Stable Diffusion doesn't matter"
        )
    ]
)
