import logging

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=["POST"])
def predict():
    args = request.json
    response = {}
    if 'RESPONSE' in args['gpt_response']:
        response['RESPONSE'] = args['gpt_response']['RESPONSE']
    if 'VASILIY' in args['gpt_response']:
        response['VASILIY'] = args['gpt_response']['VASILIY']
    return jsonify({"text": str(response)})


if __name__ == "__main__":
    app.run("0.0.0.0", port=10020)