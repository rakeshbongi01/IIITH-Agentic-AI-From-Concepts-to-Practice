# Roll Number: cert-aai-2026-06-0002
from llm import call_chat_completion

def reflect_on_run(user_query: str, plan: str, call_history: list, final_answer: str) -> str:
    """Audits the run for missing info, unnecessary tools, and confidence score."""
    prompt = (
        f"Audit the following flight operations execution:\n"
        f"Query: {user_query}\n"
        f"Plan: {plan}\n"
        f"Tool Calls: {call_history}\n"
        f"Final Answer: {final_answer}\n\n"
        f"Provide a brief critique detailing:\n"
        f"1. Were any tool calls unnecessary?\n"
        f"2. Is any critical information missing?\n"
        f"3. Confidence Score (1-10)."
    )
    
    messages = [
        {"role": "system", "content": "You are the FlightOps Reflector Agent."},
        {"role": "user", "content": prompt}
    ]
    
    response = call_chat_completion(messages=messages)
    return response.choices[0].message.content