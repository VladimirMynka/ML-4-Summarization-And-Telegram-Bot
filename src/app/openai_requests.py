import openai
from src.config.config import config
import json


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
        {"role": "assistant", "content": answer}
    )

    try:
        answer = json.loads(answer)
    except Exception as e:
        return None

    message_object["CONTEXT"] = answer["CONTEXT"]
    message_object["LAST INTENT"] = answer["INTENT"]

    return answer
