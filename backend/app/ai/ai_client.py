"""
LLM client for hybrid AI features (quiz, summary, tutor).
Uses Google Gemini when GEMINI_API_KEY is set in .env.
"""

import os

from app.ai.gemini_client import get_gemini_client


def get_ai_client():
    if not os.getenv('GEMINI_API_KEY'):
        raise ValueError(
            "GEMINI_API_KEY is required for quiz, summary, and tutor. "
            "Add it to backend/.env"
        )
    return get_gemini_client()


def get_ai_provider_name() -> str:
    model = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    return f'Google Gemini ({model})'
