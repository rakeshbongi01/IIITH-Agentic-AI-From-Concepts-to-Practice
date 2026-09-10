# Roll Number: cert-aai-2026-06-0002
import time
from mcp_server import ToolRegistry, MCPServer
from mcp_client import MCPClient
from agent import FlightOpsAgent
from memory import remember, recall
from tools import get_flight_status, get_weather, maintenance_history, find_available_gate
from schemas import FLIGHT_STATUS_SCHEMA, WEATHER_SCHEMA, MAINTENANCE_SCHEMA, GATE_SCHEMA
from planner import generate_plan
from reflector import reflect_on_run
import llm

def main():
    print("Booting Project SkyVault...")

    registry = ToolRegistry()
    
    # FIX: Updated schema to strictly follow JSON Schema format required by OpenAI[cite: 1, 29]
    registry.register(
        name="remember",
        description="Saves a fact to persistent memory. Overwrites if key exists.",
        schema={
            "type": "object",
            "properties": {
                "key": {"type": "string"},
                "value": {"type": "string"},
                "source": {"type": "string"}
            },
            "required": ["key", "value", "source"]
        },
        func=remember
    )
    
    # FIX: Updated schema to strictly follow JSON Schema format
    registry.register(
        name="recall",
        description="Retrieves a fact from persistent memory by key.",
        schema={
            "type": "object",
            "properties": {
                "query": {"type": "string"}
            },
            "required": ["query"]
        },
        func=recall
    )
    
    registry.register("get_flight_status", "Get status of a flight", FLIGHT_STATUS_SCHEMA, get_flight_status)
    registry.register("get_weather", "Get weather for an airport", WEATHER_SCHEMA, get_weather)
    registry.register("maintenance_history", "Get maintenance history", MAINTENANCE_SCHEMA, maintenance_history)
    registry.register("find_available_gate", "Find an open gate", GATE_SCHEMA, find_available_gate)

    server = MCPServer(registry)
    client = MCPClient(server)
    agent = FlightOpsAgent(mcp_client=client, llm_client=llm)

    print("\n--- System Prompt Loaded ---")
    print(agent.generate_system_prompt())
    print("----------------------------\n")

    while True:
        try:
            user_input = input("\nUser: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Shutting down SkyVault. Memory will persist.")
                break
            
            print("\n--- PHASE 1: GENERATING PLAN ---")
            plan = generate_plan(user_input)
            print(plan)

            print("\n--- PHASE 2: AGENT EXECUTION LOOP ---")
            final_answer, call_history = agent.run(user_input) 
            print("\n[Final Operations Answer]")
            print(final_answer)

            print("\n--- PHASE 3: SELF-REFLECTION & CRITIQUE ---")
            reflection = reflect_on_run(user_input, plan, call_history, final_answer) 
            print(reflection)
            
        except KeyboardInterrupt:
            print("\nShutting down SkyVault. Memory will persist.")
            break

if __name__ == "__main__":
    main()