# FlightOps: Autonomous Tool-Calling Agent

## 1. Overview & Architecture
FlightOps is a modular, zero-framework Python AI agent that assists airline operations desks. It autonomously plans, selects, executes, and reflects on multiple operational tools (flight status, weather, maintenance records, gate assignments) using the OpenAI Chat Completions API with function calling.

### File Responsibilities
* `config.py`: Loads environment configurations (.env) securely.
* `data.py`: In-memory operational mock database (Flights, Maintenance, Weather, Passengers, Gates).
* `tools.py`: Python tool functions with built-in error handling.
* `schemas.py`: JSON Schema declarations enabling the model to select tools.
* `llm.py`: Provider client wrapper.
* `planner.py`: Produces pre-execution Goals and Step-by-Step Plans for operational transparency.
* `agent.py`: Multi-turn `while` loop that handles tool requests, local execution, and context re-injection.
* `reflector.py`: Post-execution critique auditing missing data, unnecessary tool calls, and confidence.
* `main.py`: CLI entry point running the end-to-end pipeline.

---

## 2. Setup & Execution
1. Clone / extract the project.
2. Install dependencies:
   ```bash
   pip install openai python-dotenv