# Roll Number: cert-aai-2026-06-0002
import json
import os

MEMORY_FILE = "skyvault_memory.json"

def _load_memory() -> dict:
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    return {}

def _save_memory(data: dict):
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def remember(key: str, value: str, source: str) -> str:
    """Saves a fact to persistent memory. Overwrites if key exists."""
    memory = _load_memory()
    memory[key] = {"value": value, "source": source}
    _save_memory(memory)
    return f"Successfully remembered: {key} = {value}"

def recall(query: str) -> str:
    """Retrieves a fact from persistent memory by key."""
    memory = _load_memory()
    if query in memory:
        return f"Recalled {query}: {memory[query]['value']} (Source: {memory[query]['source']})"
    return f"No memory found for '{query}'."

def get_memory_summary() -> str:
    memory = _load_memory()
    if not memory:
        return "Current Memory: Empty"
    summary = "Current Memory Context:\n"
    for k, v in memory.items():
        summary += f"- {k}: {v['value']}\n"
    return summary