import logging
import re
from collections import defaultdict

from nltk import PorterStemmer


class LuhnSummarizer:
    def __init__(self, threshold: float, min_sentences_count: int):
        self.threshold = threshold
        self.min_count = min_sentences_count

    @staticmethod
    def sentence_tokenize(text):
        russian = "([А-Яа-яЁё])"
        english = "([A-Za-z])"
        alp = f"({russian}|{english})"
        small = "([a-zа-яё])"
        multiply_dots = "\.+"

        shorts = f"(?<={alp})\.(?={alp}| {small})"
        digits = f"(?<=\d)\.(?=\d)"

        text = re.sub(shorts, "$$$", text)
        text = re.sub(digits, "$$$", text)
        text = re.sub("\?|\!", ".", text)
        text = re.sub(multiply_dots, ".", text)

        return [sentence.replace("$$$", ".").strip() for sentence in text.split(".") if len(sentence) != 0]

    @staticmethod
    def word_tokenize(sentence):
        sentence = re.sub('[,:;\(\)\-—"«»]', ' ', sentence)
        return sentence.split(" ")

    @staticmethod
    def complex_tokenize(text):
        sentences = LuhnSummarizer.sentence_tokenize(text)
        words = [LuhnSummarizer.word_tokenize(sentence) for sentence in sentences]
        return words

    @staticmethod
    def calculate_sentence_significance(stemmed_sentence, word_freq):
        significant_word_indexes = [
            i for i, word in enumerate(stemmed_sentence) if
            (word in word_freq) and (word_freq[word] > 1) and (len(word) > 2)
        ]
        values = [[0 for i in range(len(stemmed_sentence))] for j in range(len(stemmed_sentence))]
        for i in range(len(stemmed_sentence)):
            for j in range(i, len(stemmed_sentence)):
                count = sum([(index >= i) and (index <= j) for index in significant_word_indexes])
                metric = count ** 2 / (j - i + 1)
                values[i][j] = metric

        return max([max(arr) for arr in values])

    def luhn_summarize(self, text):
        sentences = self.sentence_tokenize(text)

        words = [self.word_tokenize(sentence.lower()) for sentence in sentences]
        logging.debug(words)

        # Perform stemming on the words
        stemmer = PorterStemmer()
        stemmed_words = [[stemmer.stem(word) for word in sentence] for sentence in words]

        # Calculate the term frequency of each word
        word_freq = defaultdict(int)
        for sentence in stemmed_words:
            for word in sentence:
                word_freq[word] += 1

        logging.debug(word_freq)

        # Calculate the score of each sentence
        sentence_scores = []
        for i, sentence in enumerate(stemmed_words):
            sentence_scores.append(self.calculate_sentence_significance(sentence, word_freq))

        result = [sentences[i] for i in range(len(sentences)) if sentence_scores[i] >= self.threshold]

        summary = '. '.join(result)

        return summary

    def summarize_file(self, path_to_file: str, save_to: str):
        with open(path_to_file, "r") as f:
            text = f.read()

        with open(save_to, "w") as f:
            f.write(self.luhn_summarize(text))
