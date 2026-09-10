# Roll Number: cert-aai-2026-06-0002
import json
from mcp_client import MCPClient
from memory import get_memory_summary

class FlightOpsAgent:
    def __init__(self, mcp_client: MCPClient, llm_client):
        self.client = mcp_client
        self.llm = llm_client
        self.tools_schema = self.client.list_tools()
        # FIX: Initialize call_history list to prevent unpacking errors in main.py
        self.call_history = []
        
    def generate_system_prompt(self):
        memory_context = get_memory_summary()
        return f"You are SkyVault, an aviation agent. {memory_context}"

    def execute_tool(self, tool_name: str, arguments: dict):
        print(f"Routing {tool_name} through MCP...")
        self.call_history.append(tool_name)
        return self.client.call_tool(tool_name, arguments)
        
    def run(self, user_query: str):
        self.call_history = []
        messages = [
            {"role": "system", "content": self.generate_system_prompt()},
            {"role": "user", "content": user_query}
        ]
        
        openai_tools = [{"type": "function", "function": {"name": t["name"], "description": t["description"], "parameters": t["parameters"]}} for t in self.tools_schema]

        while True:
            response = self.llm.call_chat_completion(messages, tools=openai_tools)
            message = response.choices[0].message
            messages.append(message)

            if not message.tool_calls:
                # FIX: Return both the content and the tracked call_history array
                return message.content, self.call_history

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                result = self.execute_tool(tool_name, args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })