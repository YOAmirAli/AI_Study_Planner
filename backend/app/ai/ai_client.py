"""
LLM client shim — routes to Gemini or OpenAI based on .env config.
Used for quiz, summary, and tutor.
"""

import os
from app.ai.openai_client import get_openai_client
from app.ai.gemini_client import get_gemini_client


def get_ai_client():
    if os.getenv('GEMINI_API_KEY'):
        return get_gemini_client()
    return get_openai_client()


def get_ai_provider_name() -> str:
    if os.getenv('GEMINI_API_KEY'):
        client = get_gemini_client()
        return f"Gemini ({client.model.model_name})"
    client = get_openai_client()
    return f"OpenAI ({client.model})"
