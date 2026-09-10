# FlightOps: Project SkyVault (Fortnight Assignment 5)

**Roll Number: cert-aai-2026-06-0002**

## 1. Overview & Changes Since Assignment 4
Project SkyVault upgrades the FlightOps agent by introducing two major features: persistent memory and a Model Context Protocol (MCP) boundary. Unlike Assignment 4, which lost all context upon exit and hardcoded tool imports, this version persists user facts to a local JSON file across process restarts[cite: 1]. Additionally, all tool executions are now routed through hand-rolled JSON-RPC dictionaries via an `MCPServer` and `MCPClient`, replacing direct python imports[cite: 1].

## 2. Memory Conflict-Resolution Rule
**Rule: Last Write Wins (Overwrite).**
If a stored fact is restated with a different value for the same key, the new value completely overwrites the old value in the JSON storage. The system does not keep historical versions of the same key side-by-side[cite: 1].

## 3. Setup & Execution
1. Clone / extract the project.
2. Install dependencies:
   ```bash
   pip install openai python-dotenv