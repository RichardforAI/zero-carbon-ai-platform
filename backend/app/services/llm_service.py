"""LLM Service — OpenAI-compatible SDK wrapper for DeepSeek/Claude."""
import json
import re
from openai import OpenAI

from ..config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL, LLM_TIMEOUT, is_llm_configured

_client = None


def _get_client() -> OpenAI:
    """Lazy-init OpenAI client."""
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=LLM_API_KEY,
            base_url=LLM_BASE_URL,
            timeout=LLM_TIMEOUT,
        )
    return _client


def chat(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
    response_format: str | None = None,
) -> str:
    """Send a chat completion request and return the response text.

    Args:
        messages: List of {"role": "system"|"user"|"assistant", "content": "..."}
        temperature: 0.0-2.0, lower = more deterministic
        max_tokens: Maximum tokens in the response
        response_format: None or "json_object" for structured JSON output

    Returns:
        The LLM response text content.
    """
    kwargs = dict(
        model=LLM_MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    if response_format == "json_object":
        kwargs["response_format"] = {"type": "json_object"}

    response = _get_client().chat.completions.create(**kwargs)
    return response.choices[0].message.content


def chat_json(
    messages: list[dict],
    temperature: float = 0.3,
    max_tokens: int = 4096,
) -> dict:
    """Send a chat request expecting a JSON response.

    Returns parsed dict, or {} on failure.
    """
    try:
        text = chat(messages, temperature=temperature, max_tokens=max_tokens, response_format="json_object")
        # Strip markdown code fences if present
        text = re.sub(r'^```(?:json)?\s*\n?', '', text.strip())
        text = re.sub(r'\n?```\s*$', '', text.strip())
        return json.loads(text)
    except (json.JSONDecodeError, Exception):
        return {}


def is_configured() -> bool:
    """Check whether the LLM API key is properly set."""
    return is_llm_configured()
