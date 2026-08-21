"""
Post-execution evaluation module for the FlightOps agent.
"""
import json
from llm import call_chat_completion


def reflect_on_run(user_query: str, plan: str, call_history: list, final_answer: str) -> str:
    """Critiques the tool calling sequence and output accuracy."""
    reflector_prompt = (
        "You are an AI Quality & Operations Auditor reviewing an AI Agent's execution trace.\n"
        "Evaluate the run using these 4 points:\n"
        "1. Unnecessary Tools: Were any redundant or unneeded tools called?\n"
        "2. Missing Information: Was any vital operational data left unchecked?\n"
        "3. Efficiency: Could the same question have been answered with fewer steps?\n"
        "4. User Confidence: Rate confidence (Low/Medium/High) and justify why."
    )

    context_summary = (
        f"User Query: {user_query}\n\n"
        f"Initial Plan:\n{plan}\n\n"
        f"Tools Executed: {json.dumps(call_history, indent=2)}\n\n"
        f"Final Answer Given:\n{final_answer}"
    )

    messages = [
        {"role": "system", "content": reflector_prompt},
        {"role": "user", "content": context_summary}
    ]

    response = call_chat_completion(messages=messages)
    return response.choices[0].message.content