import os
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    print("[Warning] OPENAI_API_KEY is not set in environment or .env file.")