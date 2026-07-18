"""A small multi-turn terminal chatbot powered by a local Ollama model."""

from ollama import chat


MODEL = "gemma4:e2b"
EXIT_COMMANDS = {"/exit", "exit", "quit"}


def main() -> None:
    """Start an interactive Ollama chat session."""
    messages: list[dict[str, str]] = []

    print("Ollama chatbot is ready. Type /exit to stop.\n")

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

        messages.append({"role": "user", "content": user_message})

        try:
            response = chat(model=MODEL, messages=messages)
        except Exception as error:
            messages.pop()  # Remove the unanswered user turn.
            print(
                "Could not reach Ollama. Confirm that Ollama is running "
                f"and {MODEL} is installed. Details: {error}\n"
            )
            continue

        assistant_message = response.message.content
        if assistant_message is None:
            messages.pop()  # Remove the unanswered user turn.
            print("Ollama returned an empty response. Please try again.\n")
            continue

        messages.append({"role": "assistant", "content": assistant_message})
        print(f"Ollama: {assistant_message}\n")


if __name__ == "__main__":
    main()