"""
Main entry point for FlightOps Operations Assistant.
"""
import time
from planner import generate_plan
from agent import run_flightops_agent
from reflector import reflect_on_run


def process_query(user_query: str):
    print("=" * 80)
    print(f"OPERATIONAL INQUIRY: {user_query}")
    print("=" * 80)

    # 1. Planning Phase
    print("\n--- PHASE 1: GENERATING PLAN ---")
    plan = generate_plan(user_query)
    print(plan)
    # time.sleep(30)

    # return 0

    # 2. Multi-Tool Execution Phase
    print("\n--- PHASE 2: AGENT EXECUTION LOOP ---")
    final_answer, call_history = run_flightops_agent(user_query)
    
    print("\n[Final Operations Answer]")
    print(final_answer)

    # 3. Post-execution Reflection Phase
    print("\n--- PHASE 3: SELF-REFLECTION & CRITIQUE ---")
    reflection = reflect_on_run(user_query, plan, call_history, final_answer)
    print(reflection)
    print("=" * 80 + "\n")


if __name__ == "__main__":
    # Test 1: Complex Multi-Tool Reasoning (requires flight status, weather, and maintenance)
    test_query_1 = "Is Flight A1203 likely to depart on time? Please check all operational dependencies."
    process_query(test_query_1)

    # Test 2: Error Handling Verification (calls simulated failing weather code 'ERR')
    # test_query_2 = "What is the weather status at station ERR and is Gate A1 free in Terminal 1?"
    # process_query(test_query_2)