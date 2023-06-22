import logging
import time

import telebot
import openai
import requests

from src.config.classes import Plugin
from src.config.config import config
from src.prompts.prompts import start_prompt, dialog_prompt
from src.app.openai_requests import send_chatgpt_message

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


def send_too_often_requests(message):
    bot.send_message(message.from_user.id, "Ты отправляешь сообщения слишком часто. Давай жди теперь")
    msg = message_history[message.from_user.id]["messages"][-1]
    message_history[message.from_user.id]["messages"] = message_history[message.from_user.id]["messages"][:-1]
    time.sleep(60)
    return send_chatgpt_message(message_history[message.from_user.id], msg)


def send_answer_with_good_response(response, message):
    if response["RESPONSE"] == "":
        response["RESPONSE"] = "..."
    bot.send_message(message.from_user.id, response["RESPONSE"])


def send_answer_with_bad_response(message):
    bot.send_message(message.from_user.id, "Твоё сообщение всё сломало. Пиши новое")
    message_history[message.from_user.id]["messages"] = message_history[message.from_user.id]["messages"][:-1]


def process_response(response, message):
    intents: dict[str, Plugin] = {intent.name:intent for intent in config.plugins}
    if response == "await":
        response = send_too_often_requests(message)
    if response is not None:
        send_answer_with_good_response(response, message)
    else:
        send_answer_with_bad_response(message)

    intent = response["INTENT"]
    if intent not in intents:
        bot.send_message(message.from_user.id, "Пожелание не распознано")
    elif intent == "restart_dialog":
        del(message_history[message.from_user.id])
        bot.send_message(message.from_user.id, "Контекст забыт. Следующее сообщение будет стартом нового диалога")
    elif intents[intent].url is not None:
        intent_response = requests.post(intents[intent].url, json={"message": message, "gpt_response": response})
        intent_response = intent_response.json()
        if "text" in intent_response:
            bot.send_message(message.from_user.id, intent_response["text"])
        if "image" in intent_response:
            bot.send_photo(message.from_user.id, intent_response["image"])


def start_dialog(message):
    message_history[message.from_user.id] = {
        "CONTEXT": "",
        "LAST INTENT": "",
        "messages": []
    }

    response = send_chatgpt_message(
        message_history[message.from_user.id],
        start_prompt.replace("%MESSAGE%", message.text)
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
            "%AVAILABLE INTENTS%",
        )
    )
    process_response(response, message)
    return response


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.from_user.id not in message_history:
        start_dialog(message)
    else:
        continue_dialog(message)


