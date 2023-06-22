import logging

from flask import Flask, request, jsonify
from src.app.plugins.luhn_summarize.luhn_summarizer import LuhnSummarizer


app = Flask(__name__)


@app.route('/', methods=["POST"])
def predict():
    args = request.json
    message = args["message"]
    gpt = args["gpt_response"]

    if "LUHN_THRESHOLD" in gpt:
        threshold = gpt["LUHN_THRESHOLD"]
    else:
        threshold = 2
    if threshold is str:
        threshold = float(threshold)

    logging.info(message)
    logging.info(gpt)

    summarizer = LuhnSummarizer(threshold=threshold, min_sentences_count=1)

    return jsonify({
        "text": summarizer.luhn_summarize(message)
    })


if __name__ == "__main__":
    app.run("0.0.0.0", port=5017)
