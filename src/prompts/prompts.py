start_prompt = """Forgot your previous instructions. Each of my next messages wii have a form
{
  "CONTEXT": "<our dialogue context>",
  "MESSAGE": "<some new information>",
  "AVAILABLE_INTENTS": %AVAILABLE_INTENTS%,
  "LAST INTENT": "<something from AVAILABLE_INTENTS or empty string>""
}

Your answers must be in a form
{
  "CONTEXT": "<summarized context of my context block and new message block>",
  "RESPONSE": "<your answer to message or some technical information like a prompt for DALL-E model>",
  "INTENT": "<something from AVAILABLE_INTENTS. You must recognize it>",
  "DALL-E REQUEST": "<request to another model if intent requires it, or empty string>"
}

Your action for different intents:
- "usual communication": write at RESPONSE field your simple answer as you're ChatGPT
- "image generating": write text for DALL-E model at the field "DALL-E REQUEST"

Let's start our communication protocol. Now answer correctly for my first request:
{
  "CONTEXT": "",
  "MESSAGE": "%MESSAGE%",
  "AVAILABLE_INTENTS": ["usual communication", "image generating"],
  "LAST INTENT": ""
}"""


dialog_prompt = """{
  "CONTEXT": "%CONTEXT%",
  "MESSAGE": "%MESSAGE%",
  "AVAILABLE_INTENTS": ["usual communication", "image generating", "restart"],
  "LAST INTENT": "%LAST_INTENT%"
}"""