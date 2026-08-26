"""Compatibility exports for the shared OpenAI client."""

from shared.llm import generate_response, generate_response_with_image

__all__ = ["generate_response", "generate_response_with_image"]
