"""Shared LLM client — wraps the OpenAI API.

All patterns import from here so the model configuration lives in one place.
"""

import base64
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
    response = _client().responses.create(
        model=model_name,
        input=prompt,
    )
    return response.output_text


def generate_response_with_image(prompt: str, image_bytes: bytes, model_name: str = MODEL) -> str:
    """Generate a response for a prompt that includes an image."""
    image_data = base64.b64encode(image_bytes).decode("ascii")
    response = _client().responses.create(
        model=model_name,
        input=[{
            "role": "user",
            "content": [
                {"type": "input_text", "text": prompt},
                {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_data}"},
            ],
        }],
    )
    return response.output_text
