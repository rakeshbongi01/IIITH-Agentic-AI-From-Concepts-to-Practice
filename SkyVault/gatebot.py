# Roll Number: cert-aai-2026-06-0002
from mcp_client import MCPClient
from mcp_server import MCPServer, ToolRegistry

# Rebuild the server/registry connection for the standalone consumer[cite: 1]
registry = ToolRegistry()
# In a real scenario, gatebot connects to an external server. 
# Here, we pass a local instance of the same server structure to prove tool reuse[cite: 1].
server = MCPServer(registry)
client = MCPClient(server)

# Execute the tool without importing tools.py or agent.py[cite: 1]
print("Requesting gate from SkyVault MCP Server...")
result = client.call_tool("find_available_gate", {"terminal": "Terminal 2"})
print(f"GateBot received: {result}")