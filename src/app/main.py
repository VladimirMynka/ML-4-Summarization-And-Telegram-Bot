import logging
import time

import telebot
import openai
import requests
import json

from src.config.config import config
from src.prompts.prompts import start_prompt, dialog_prompt

bot = telebot.TeleBot(config.telegram.token)
openai.api_key = config.openai.token


message_history = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.from_user.id, "Пошёл в жопу")


def read_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        file = f.read()
    return file


def send_chatgpt_message(message_object, text):
    message_object["messages"].append(
        {"role": "user", "content": text}
    )
    message_object["messages"] = message_object["messages"][-5:]
    try:
        completion = openai.ChatCompletion.create(
            model=config.openai.model,
            messages=message_object["messages"]
        )
    except openai.error.RateLimitError as e:
        return "await"
    answer = completion.choices[0].message.content
    print(answer)
    message_object["messages"].append(
        {"role": "assistant", "content": start_prompt.replace("%MESSAGE%", answer)}
    )

    try:
        answer = json.loads(answer)
    except Exception as e:
        return None
    message_object["CONTEXT"] = answer["CONTEXT"]
    message_object["LAST INTENT"] = answer["INTENT"]

    return answer


def send_stable_diffusion(prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = {
        "key": "KGw3TxYlcASGyZ2YFH0TlQuXnCFUt3MVSAX4k3j4folftuk4WydVWsxm3CdA",
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
    print(response)
    print(response.text)
    response = response.json()

    return response["output"][0]


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id not in message_history:
        message_history[message.from_user.id] = {
            "CONTEXT": "",
            "LAST INTENT": "",
            "messages": []
        }

        response = send_chatgpt_message(
            message_history[message.from_user.id],
            start_prompt.replace("%MESSAGE%", message.text)
        )
        if response == "await":
            bot.send_message(message.from_user.id, "Ты отправляешь сообщения слишком часто. Давай жди теперь")
            time.sleep(40)
            response = send_chatgpt_message(
                message_history[message.from_user.id],
                start_prompt.replace("%MESSAGE%", message.text)
            )
        if response is not None:
            if response["RESPONSE"] == "":
                response["RESPONSE"] = "..."
            bot.send_message(message.from_user.id, response["RESPONSE"])
        else:
            bot.send_message(message.from_user.id, "Твоё сообщение всё сломало. Пиши новое")
    else:
        message_object = message_history[message.from_user.id]
        response = send_chatgpt_message(
            message_object,
            dialog_prompt.replace(
                "%MESSAGE%", message.text
            ).replace(
                "%LAST INTENT%", message_object["LAST INTENT"],
            ).replace(
                "%CONTEXT%", message_object["CONTEXT"]
            )
        )
        if response == "await":
            bot.send_message(message.from_user.id, "Ты отправляешь сообщения слишком часто. Давай жди теперь")
            time.sleep(40)
            response = send_chatgpt_message(
                message_object,
                dialog_prompt.replace(
                    "%MESSAGE%", message.text
                ).replace(
                    "%LAST INTENT%", message_object["LAST INTENT"],
                ).replace(
                    "%CONTEXT%", message_object["CONTEXT"]
                )
            )
        if response is not None:
            if response["RESPONSE"] == "":
                response["RESPONSE"] = "..."
            bot.send_message(message.from_user.id, response["RESPONSE"])
        else:
            message_object["messages"] = message_object["messages"][:-1]
            bot.send_message(message.from_user.id, "Твоё сообщение всё сломало. Пиши новое")

    if response["INTENT"] == "image generating":
        try:
            link = send_stable_diffusion(response["DALL-E REQUEST"])
            bot.send_photo(message.from_user.id, link)
        except Exception as e:
            bot.send_message("Не получилось достучаться до Stable Diffusion. Что-то не так")
            logging.error(e)







