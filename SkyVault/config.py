# Roll Number: cert-aai-2026-06-0002
import os
from dotenv import load_dotenv

# Load model provider configuration through environment variables[cite: 1]
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5-mini")

if not OPENAI_API_KEY:
    print("[Warning] OPENAI_API_KEY is not set in environment or .env file.")