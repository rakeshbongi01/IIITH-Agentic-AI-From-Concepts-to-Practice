"""A small multi-turn terminal chatbot powered by Gemini."""

import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


MODEL = "gemini-3.5-flash"
EXIT_COMMANDS = {"/exit", "exit", "quit"}


def main() -> None:
    """Start an interactive Gemini chat session."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "GEMINI_API_KEY is not set. Add it to your terminal environment first."
        )

    client = genai.Client(api_key=api_key)
    chat = client.chats.create(model=MODEL)

    print("Gemini chatbot is ready. Type /exit to stop.\n")

    while True:
        try:
            user_message = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nChat ended.")
            break

        if user_message.lower() in EXIT_COMMANDS:
            print("Chat ended.")
            break

        if not user_message:
            continue

        try:
            response = chat.send_message(user_message)
            print(f"Gemini: {response.text}\n")
        except Exception as error:
            print(f"Gemini request failed: {error}\n")


if __name__ == "__main__":
    main()