"""
Core Multi-Tool Agent execution loop using standard Python flow.
"""
import json
from llm import call_chat_completion
from schemas import TOOL_SCHEMAS
from tools import TOOL_REGISTRY


SYSTEM_PROMPT = (
    "You are FlightOps, an advanced AI Operations Officer at AeroWing Airlines.\n"
    "Your objective is to provide safe, accurate, and fully verified operational answers.\n"
    "Guidelines:\n"
    "1. When answering operational questions (e.g. on-time likelihood, aircraft dispatch, gating),\n"
    "   synthesize all relevant factors: flight status, weather at origin/destination, and maintenance issues.\n"
    "2. If a tool returns an error, explain the issue clearly to the user instead of failing.\n"
    "3. Base all your conclusions strictly on the tool execution outputs."
)


def run_flightops_agent(user_query: str) -> tuple[str, list]:
    """
    Executes the multi-tool lifecycle loop:
    1. Sends query + tools to the LLM.
    2. Runs requested tools locally.
    3. Feeds back tool results until model produces the final answer.
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    call_history = []
    max_turns = 10
    turn_count = 0

    while turn_count < max_turns:
        turn_count += 1
        
        # 1. Ask LLM with available tools
        response = call_chat_completion(messages=messages, tools=TOOL_SCHEMAS)
        message = response.choices[0].message

        # Check if the model requested any tool calls
        tool_calls = message.tool_calls

        if not tool_calls:
            # Model produced a final textual response
            return message.content, call_history

        # Append assistant's intent/tool-calls into the message chain
        messages.append(message)

        # 2. Execute each requested tool
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            raw_args = tool_call.function.arguments
            
            try:
                args = json.loads(raw_args)
            except Exception:
                args = {}

            print(f"  [Agent Action] Calling `{function_name}` with arguments {args}")
            call_history.append({"tool": function_name, "args": args})

            # Look up matching function in registry
            if function_name in TOOL_REGISTRY:
                tool_func = TOOL_REGISTRY[function_name]
                try:
                    tool_result = tool_func(**args)
                except Exception as exc:
                    tool_result = {"status": "error", "message": f"Execution error: {str(exc)}"}
            else:
                tool_result = {"status": "error", "message": f"Tool '{function_name}' is not recognized."}

            # 3. Append the execution output to conversation history
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(tool_result)
            })

    return "Agent loop reached maximum turns without completing.", call_history