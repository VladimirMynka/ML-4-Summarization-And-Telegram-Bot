import logging

import requests
from flask import Flask, request, jsonify


app = Flask(__name__)

with open("secret.txt", "r") as f:
    key = f.read()


def send_stable_diffusion(prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = {
        "key": key,
        "prompt": prompt,
        "negative_prompt": None,
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "20",
        "seed": None,
        "guidance_scale": 7.5,
        "safety_checker": "yes",
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "no",
        "embeddings_model": "embeddings_model_id",
        "webhook": None,
        "track_id": None
    }

    response = requests.post(url, json=payload)
    logging.info(response)
    logging.info(response.text)
    response = response.json()

    return response["output"][0]


@app.route('/', methods=["POST"])
def predict():
    args = request.json
    message = args["message"]
    gpt = args["gpt_response"]

    if ("STABLE DIFFUSION" not in gpt) or (gpt["STABLE DIFFUSION"] == ""):
        return jsonify({
            "text": "GPT не отправила запрос"
        })

    image = send_stable_diffusion(gpt["STABLE DIFFUSION"])
    return jsonify({
        "image": image
    })


if __name__ == "__main__":
    app.run("0.0.0.0", port=6017)
