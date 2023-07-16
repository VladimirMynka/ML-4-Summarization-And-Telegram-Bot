import json
import logging
import os
import time
import subprocess

import telebot
import openai
import requests

from src.config.classes import Plugin
from src.config.config import config
from src.prompts.prompts import start_prompt, dialog_prompt, new_plugin_prompt
from src.app.openai_requests import send_chatgpt_message, send_single_message
from src.app.utils import get_intents_description, get_available_intents, update_config

update_config(config)

bot = telebot.TeleBot(config.telegram.token)
openai.api_key = config.openai.token

message_history = {}


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.from_user.id, "Привет. Чем тебе помочь?")


def read_file(filepath: str):
    with open(filepath, "r", encoding="utf-8") as f:
        file = f.read()
    return file


def send_too_often_requests(message):
    bot.send_message(message.from_user.id, "Ты отправляешь сообщения слишком часто. Давай жди теперь")
    msg = message_history[message.from_user.id]["messages"][-1]
    message_history[message.from_user.id]["messages"] = message_history[message.from_user.id]["messages"][:-1]
    time.sleep(60)
    return send_chatgpt_message(message_history[message.from_user.id], msg["content"])


def send_answer_with_good_response(response):
    if response["RESPONSE"] == "":
        response["RESPONSE"] = "..."


def send_answer_with_bad_response(message):
    bot.send_message(message.from_user.id, "Твоё сообщение всё сломало. Пиши новое")
    message_history[message.from_user.id]["messages"] = message_history[message.from_user.id]["messages"][:-1]


def process_response(response, message):
    intents: dict[str, Plugin] = {intent.name: intent for intent in config.plugins}
    if response == "await":
        response = send_too_often_requests(message)
    if response is not None:
        send_answer_with_good_response(response)
    else:
        send_answer_with_bad_response(message)
        return

    intent = response["INTENT"]
    if intent not in intents:
        bot.send_message(message.from_user.id, "Пожелание не распознано")
    elif intent == "usual_communication":
        bot.send_message(message.from_user.id, response["RESPONSE"])
    elif intent == "restart_dialog":
        del (message_history[message.from_user.id])
        update_config(config)
        bot.send_message(message.from_user.id, "Контекст забыт. Следующее сообщение будет стартом нового диалога")
    elif intent == "create_plugin":
        bot.send_message(message.from_user.id, f"Создаём плагин...")
        result = create_plugin(message.text)
        bot.send_message(message.from_user.id, result)
    elif intents[intent].url is not None:
        bot.send_message(message.from_user.id, f"Сейчас работает плагин {intent}")
        try:
            intent_response = requests.post(intents[intent].url,
                                            json={"message": message.text, "gpt_response": response})
            intent_response = intent_response.json()
            logging.debug(intent_response)
            if "text" in intent_response:
                if intent_response["text"] != "":
                    bot.send_message(message.from_user.id, intent_response["text"])
                else:
                    bot.send_message(message.from_user.id, "Плагин отправил пустой ответ")
            if "image" in intent_response:
                if os.path.isfile(intent_response["image"]):
                    with open(intent_response["image"], "rb") as f:
                        bot.send_photo(message.from_user.id, f)
                else:
                    bot.send_photo(message.from_user.id, intent_response["image"])
            if "audio" in intent_response:
                if os.path.isfile(intent_response["audio"]):
                    with open(intent_response["audio"], "rb") as f:
                        bot.send_voice(message.from_user.id, f)
                else:
                    bot.send_voice(message.from_user.id, intent_response["audio"])
            if "file" in intent_response:
                if os.path.isfile(intent_response["file"]):
                    with open(intent_response["file"], "rb") as f:
                        bot.send_document(message.from_user.id, f)
                else:
                    bot.send_document(message.from_user.id, intent_response["file"])
        except:
            bot.send_message(message.from_user.id, "Не работает твой этот плагин")


def start_dialog(message):
    message_history[message.from_user.id] = {
        "CONTEXT": "",
        "LAST INTENT": "",
        "messages": []
    }

    response = send_chatgpt_message(
        message_history[message.from_user.id],
        start_prompt.replace(
            "%MESSAGE%", message.text
        ).replace(
            "%AVAILABLE INTENTS%", get_available_intents(config)
        ).replace(
            "%INTENTS_DESCRIPTIONS%", get_intents_description(config)
        )
    )
    process_response(response, message)
    return response


def continue_dialog(message):
    message_object = message_history[message.from_user.id]
    response = send_chatgpt_message(
        message_object,
        dialog_prompt.replace(
            "%MESSAGE%", message.text
        ).replace(
            "%LAST INTENT%", message_object["LAST INTENT"],
        ).replace(
            "%CONTEXT%", message_object["CONTEXT"]
        ).replace(
            "%AVAILABLE INTENTS%", get_available_intents(config)
        )
    )
    process_response(response, message)
    return response


def create_plugin(description: str):
    response: str | dict = "await"
    while response == "await":
        response = send_single_message(
            new_plugin_prompt.replace(
                "%DESCRIPTION%", description
            ).replace(
                "%EXISTING_INTENTS%", get_available_intents(config)
            )
        )
    if response is None:
        return "Не получилось сгенерировать плагин. ChatGPT-генератор вернул невалидный ответ"
    if response["responsibility"] == 0:
        logging.info(response["name"])
        logging.info(description)
        logging.info(response["comment for developer"])
        return response["comment for developer"]

    name = response["name"]
    while name in os.listdir(config.plugins_source_directory):
        name = f"{name}_"
    os.mkdir(os.path.join(config.plugins_source_directory, name))

    src_folder = os.path.join(config.plugins_source_directory, name)
    with open(os.path.join(src_folder, "__init__.py"), "w") as f:
        f.write("")

    with open("last_port", "r") as f:
        port = int(f.read())
    with open("last_port", "w") as f:
        f.write(f"{port + 1}")

    filepath = os.path.join(src_folder, "flask_app.py")
    with open(filepath, "w", encoding="utf-8") as f:
        code = response["code"].replace("%PORT%", str(port))
        if code[-1] == "}":
            code = code[:-1]
        f.write(code, )

    subprocess.Popen(['python', filepath])

    with open(os.path.join(config.plugins_directory, f"{name}.json"), "w") as f:
        json.dump(
            {
                "url": f"http://127.0.0.1:{port}/",
                "description": response["description"]
            },
            f
        )
    update_config(config)

    return "OK"


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id not in message_history:
        start_dialog(message)
    else:
        continue_dialog(message)


print("STARTED")
