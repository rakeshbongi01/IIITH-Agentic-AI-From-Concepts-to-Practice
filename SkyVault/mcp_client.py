# Roll Number: cert-aai-2026-06-0002
    
class MCPClient:
    def __init__(self, server):
        self.server = server
        self.request_id = 1
        self._send({"jsonrpc": "2.0", "id": self.request_id, "method": "initialize"})
        
    def _send(self, payload: dict) -> dict:
        self.request_id += 1
        return self.server.handle_request(payload)

    def list_tools(self) -> list:
        req = {"jsonrpc": "2.0", "id": self.request_id, "method": "tools/list"}
        return self._send(req).get("result", {}).get("tools", [])

    def call_tool(self, name: str, arguments: dict):
        req = {
            "jsonrpc": "2.0",
            "id": self.request_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments}
        }
        resp = self._send(req)
        if "error" in resp:
            return f"Error: {resp['error']['message']}"
        return resp.get("result")