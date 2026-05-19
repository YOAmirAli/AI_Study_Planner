"""
LLM client shim — routes to Gemini or OpenAI based on .env config.
Used for quiz, summary, and tutor.
"""

import os
from typing import Optional

from app.ai.openai_client import get_openai_client
from app.ai.gemini_client import get_gemini_client


def _valid_key(key: Optional[str]) -> bool:
    return bool(key and not key.startswith('your-'))


def get_ai_client():
    if _valid_key(os.getenv('GEMINI_API_KEY')):
        return get_gemini_client()
    return get_openai_client()


def get_ai_provider_name() -> str:
    if _valid_key(os.getenv('GEMINI_API_KEY')):
        client = get_gemini_client()
        return f"Gemini ({client.model_name})"
    client = get_openai_client()
    return f"OpenAI ({client.model})"
