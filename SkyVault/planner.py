"""
Generates transparent Goals and Plans prior to tool execution.
"""
from llm import call_chat_completion


def generate_plan(user_query: str) -> str:
    """Prompts the LLM to outline its operational goal and planned inspection steps."""
    system_prompt = (
        "You are the Operations Planner for AeroWing Airlines (FlightOps).\n"
        "Given a user query, output a concise Goal and a numbered Step-by-Step Plan "
        "describing what operational data must be verified before answering.\n"
        "Format strictly as:\n"
        "Goal: <one sentence goal>\n"
        "Plan:\n"
        "1. <step 1>\n"
        "2. <step 2>\n"
        "3. <step 3>\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    response = call_chat_completion(messages=messages)
    return response.choices[0].message.content