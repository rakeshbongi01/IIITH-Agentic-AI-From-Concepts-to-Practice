import json
from pathlib import Path
from typing import Dict, Any
from config import PREFS_FILE

def load_prefs() -> Dict[str, Any]:
    if not PREFS_FILE.exists():
        return {}
    try:
        with open(PREFS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_pref(key: str, value: Any) -> None:
    prefs = load_prefs()
    prefs[key] = value
    with open(PREFS_FILE, "w", encoding="utf-8") as f:
        json.dump(prefs, f, indent=2)