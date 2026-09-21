import json
import time
from typing import Any, Dict
from config import TRACE_FILE

def log_event(cap: str, event_type: str, details: Dict[str, Any]) -> None:
    payload = {
        "timestamp": time.time(),
        "cap": cap,
        "event": event_type,
        **details
    }
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")