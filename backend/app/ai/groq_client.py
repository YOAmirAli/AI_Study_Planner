"""
Legacy module name — primary LLM client is OpenAI (openai_client.py).

Hybrid routing uses openai_client via ai_service.py. This file re-exports
OpenAI for backward compatibility with older imports (e.g. quiz_generator.py).
Optional: set GROQ_API_KEY only if you restore the original Groq implementation.
"""

from app.ai.openai_client import OpenAIClient, get_openai_client

# Backward-compatible aliases
GroqClient = OpenAIClient


def get_groq_client():
    """Returns OpenAI client (hybrid architecture uses OpenAI for LLM tasks)."""
    return get_openai_client()
