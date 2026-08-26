from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)


def call_chat_completion(messages: list, tools: list = None):
    """
    Standard wrapper around OpenAI chat completions API.
    Supports tool definitions if provided.
    """
    kwargs = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 1
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    return client.chat.completions.create(**kwargs)