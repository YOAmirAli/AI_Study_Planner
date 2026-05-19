"""
LLM client shim — routes to Gemini or OpenAI based on .env config.
Used for quiz, summary, and tutor.
"""

import os
from typing import Optional

from app.ai.openai_client import get_openai_client
from app.ai.gemini_client import get_gemini_client


def is_valid_api_key(key: Optional[str]) -> bool:
    return bool(key and not key.startswith('your-'))


def _valid_key(key: Optional[str]) -> bool:
    return is_valid_api_key(key)


def get_ai_client(prefer_openai: bool = False):
    openai_ok = _valid_key(os.getenv('OPENAI_API_KEY'))
    gemini_ok = _valid_key(os.getenv('GEMINI_API_KEY'))

    if prefer_openai and openai_ok:
        return get_openai_client()
    if gemini_ok and not prefer_openai:
        return get_gemini_client()
    if openai_ok:
        return get_openai_client()
    if gemini_ok:
        return get_gemini_client()
    raise ValueError(
        "No AI API key configured. Set OPENAI_API_KEY or GEMINI_API_KEY on the server."
    )


def get_ai_provider_name(client=None) -> str:
    if client is None:
        client = get_ai_client()
    if hasattr(client, 'model_name'):
        return f"Gemini ({client.model_name})"
    return f"OpenAI ({client.model})"
