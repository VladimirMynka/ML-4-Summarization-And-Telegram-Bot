import logging

import os
import shutil
import time

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=["POST"])
def predict():
    args = request.json
    message = args["message"]
    gpt = args["gpt_response"]

    name = message.split("delete ")[1]
    timestamp = time.strftime("%Y%m%d-%H%M%S")

    old_file_path = f"../../../../data/plugins_configs/{name}.json"
    new_file_path = f"../../../../data/archived_plugins/{name}_{timestamp}.json"

    os.renames(old_file_path, new_file_path)

    return jsonify({
        "text": f"The intent {name} was successfully deleted."
    })


if __name__ == "__main__":
    app.run("0.0.0.0", port=10028)
