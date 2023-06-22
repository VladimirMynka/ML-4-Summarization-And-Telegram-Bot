from fire import Fire
from src.app.main import bot
from src.config.config import config
from src.app.utils import init_logging
from src.app.plugins.luhn_summarize.luhn_summarizer import LuhnSummarizer


class CLI:
    def __init__(self):
        init_logging(config.logger)

    def start_bot(self):
        bot.polling(none_stop=True, interval=0)

    def luhn_summarize(self):
        summarizer = LuhnSummarizer(config.luhn.threshold, config.luhn.min_sentences_count)
        summarizer.summarize_file(config.luhn.path_to_file, config.luhn.path_to_output)


if __name__ == "__main__":
    Fire(CLI)
