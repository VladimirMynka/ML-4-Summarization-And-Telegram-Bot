import openai
import logging
from src.config.config import config
import json


def send_chatgpt_message(message_object, text):
    logging.debug(text)
    message_object["messages"].append(
        {"role": "user", "content": text}
    )
    message_object["messages"] = message_object["messages"][0:1] + message_object["messages"][-6:]
    try:
        completion = openai.ChatCompletion.create(
            model=config.openai.model,
            messages=message_object["messages"]
        )
    except openai.error.RateLimitError as e:
        return "await"
    answer = completion.choices[0].message.content
    logging.debug(answer)
    message_object["messages"].append(
        {"role": "assistant", "content": answer}
    )

    try:
        answer = json.loads(answer)
    except Exception:
        return None

    message_object["CONTEXT"] = answer["CONTEXT"]
    message_object["LAST INTENT"] = answer["INTENT"]

    return answer


def send_single_message(message: str):
    logging.debug(message)
    request_object = [{"role": "user", "content": message}]
    try:
        completion = openai.ChatCompletion.create(
            model=config.openai.model,
            messages=request_object
        )
    except openai.error.RateLimitError:
        return "await"

    answer = completion.choices[0].message.content
    logging.debug(answer)

    try:
        answer = json.loads(answer)
    except Exception:
        return None

    return answer

