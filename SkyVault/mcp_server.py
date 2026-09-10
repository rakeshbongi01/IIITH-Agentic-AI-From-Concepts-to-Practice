# Roll Number: cert-aai-2026-06-0002

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, name, description, schema, func):
        self.tools[name] = {
            "description": description,
            "schema": schema,
            "func": func
        }

class MCPServer:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def handle_request(self, request: dict) -> dict:
        req_id = request.get("id")
        method = request.get("method")
        response = {"jsonrpc": "2.0", "id": req_id}

        if method == "initialize":
            response["result"] = {"server_name": "SkyVault_MCP", "protocol_version": "1.0"}
        
        elif method == "tools/list":
            tools_list = [{"name": n, "description": d["description"], "parameters": d["schema"]} 
                          for n, d in self.registry.tools.items()]
            response["result"] = {"tools": tools_list}
            
        elif method == "tools/call":
            params = request.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})
            
            if tool_name not in self.registry.tools:
                response["error"] = {"code": -32001, "message": f"Unknown tool: {tool_name}"}
            else:
                try:
                    func = self.registry.tools[tool_name]["func"]
                    response["result"] = func(**args)
                except Exception as e:
                    response["error"] = {"code": -32603, "message": str(e)}
        else:
            response["error"] = {"code": -32601, "message": "Method not found"}
            
        return response