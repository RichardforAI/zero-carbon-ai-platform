"""Application configuration — loaded from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-chat")

# Timeout in seconds for LLM API calls
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "60"))

def is_llm_configured() -> bool:
    """Check if LLM API key has been set."""
    return bool(LLM_API_KEY and LLM_API_KEY != "sk-your-deepseek-api-key")
