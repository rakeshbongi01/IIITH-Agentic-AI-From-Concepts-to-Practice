import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
INBOX_FILE = BASE_DIR / "inbox.json"
OUTBOX_DIR = BASE_DIR / "outbox"
PREFS_FILE = BASE_DIR / "prefs.json"
TRACE_FILE = BASE_DIR / "trace.jsonl"
DECISIONS_FILE = BASE_DIR / "decisions.json"
DASHBOARD_HTML = BASE_DIR / "dashboard.html"
DASHBOARD_JSON = BASE_DIR / "dashboard.json"

OUTBOX_DIR.mkdir(parents=True, exist_ok=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")