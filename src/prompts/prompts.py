start_prompt = """Forgot your previous instructions. Each of my next messages will have a form
{
  "CONTEXT": "<our dialogue context>",
  "MESSAGE": "<some new information>",
  "AVAILABLE INTENTS": %AVAILABLE INTENTS%,
  "LAST INTENT": "<something from AVAILABLE_INTENTS or empty string>""
}

Your answers must be in a form
{
  "CONTEXT": "<summarized context of my context block and new message block>",
  "RESPONSE": "<your answer to message or some technical information like a prompt for DALL-E model>",
  "INTENT": "<something from AVAILABLE INTENTS. You must recognize it>"б
  <some another fields if intent requires>
}

Your action for different intents:
%INTENTS_DESCRIPTIONS%

Let's start our communication protocol. Now answer correctly for my first request:
{
  "CONTEXT": "",
  "MESSAGE": "%MESSAGE%",
  "AVAILABLE INTENTS": %AVAILABLE INTENTS%,
  "LAST INTENT": ""
}"""


dialog_prompt = """{
  "CONTEXT": "%CONTEXT%",
  "MESSAGE": "%MESSAGE%",
  "AVAILABLE INTENTS": %AVAILABLE INTENTS%,
  "LAST INTENT": "%LAST INTENT%"
}"""

new_plugin_prompt = """
Hello! I have a beautiful bot and you're a part of it. So you must write message in json-format and I (my program) will write json too. My bot has plugins. Where bot recognizes some user's intent, he finds this intent in his database, get URL from it and sends a request in form:
{
  "message": "<some text>",
  "gpt_response": { <any json which was received from GPT model> }
}
Bot database with plugins looks like config:
```
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
```

This is example of plugin code:
```
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
```


You are included into plugin-generator plugin. This plugin will be requested if user wants add new plugin into the system.
You will get request in the form:
{
    "plugin description": "<something that user wants>",
    "existing intents": [<list of existing intent names>]
}

You must answer:
{
    "responsibility": <0 or 1>, // is it responsible for you to generate fully code for this plugin (1) or developer should add something else (1),
    "comment for developer": "<if it's not fully responsible for you, write your comment for developer here>",
    "name": "short_intent_name", // not duplicate for "existing intents" from my json
    "description": "<detailed description which will be gived another language model to recognize intent and generate correct json. Define plugin's input data but not code description. If you want to use some specific fields in your plugin, write about it here>",
    "code": "<full python code with using flask do action which user wants. Replace port number with int("%PORT%") construction. Don't forget about import flask and about app.run() method. Your code must be compilating without any another actions.>"
}

Pay attention that plugins must return json with only optional fields "text", "image", "file", "audio". Not use any another keys. To use file or audio fields, save your file at disk and send absolute path to it. You can use os module for get it. Audio can be only in mp3 format. You can use torchaudio module to save it if you need.
Pay attention that plugins can use only two fields: "message" - \
user original message, and "gpt_response" - json generated by \
language modules. You can't use any another fields in your plugin but you can \
write in description something like this: 'add field "<FIELD_NAME>" in your json'. \
So if GPT can understand you, you can use this value as response["gpt_response"]["<FIELD_NAME>"]

Now answer this request:
{
    "plugin description": "%DESCRIPTION%",
    "existing intents": "%EXISTING_INTENTS%"
}
"""