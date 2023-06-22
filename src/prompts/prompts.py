start_prompt = """Forgot your previous instructions. Each of my next messages wii have a form
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