"""Shared LLM client — wraps the OpenAI API.

All patterns import from here so the model configuration lives in one place.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")


def _client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured. Add it to the project .env file.")
    return OpenAI(api_key=api_key)


def generate_response(prompt: str, model_name: str = MODEL) -> str:
    """Generate a text response for the given prompt."""
    # Existing pattern definitions use gemma4 as their local-model label.
    selected_model = MODEL if model_name == "gemma4" else model_name
    response = _client().responses.create(
        model=selected_model,
        input=prompt,
    )
    return response.output_text
