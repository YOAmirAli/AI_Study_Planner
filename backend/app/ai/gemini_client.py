"""
Gemini client using the google-genai SDK (client.models.generate_content).
"""

import json
import os
import re

from google import genai
from google.genai import types


def _strip_json_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _parse_json(text: str, fallback=None):
    try:
        return json.loads(_strip_json_fence(text))
    except json.JSONDecodeError:
        return fallback


def _normalize_model_name(name: str) -> str:
    """New SDK expects 'gemini-2.5-flash', not 'models/gemini-2.5-flash'."""
    if name.startswith("models/"):
        return name[len("models/"):]
    return name


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key or self.api_key.startswith("your-"):
            raise ValueError("GEMINI_API_KEY is required and must be a valid key")
        self.model_name = _normalize_model_name(
            os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        )
        self.client = genai.Client(api_key=self.api_key)

    def _generate(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
        config_kwargs = {"temperature": temperature}
        if system:
            config_kwargs["system_instruction"] = system

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = getattr(response, "text", None)
        if text:
            return text.strip()
        if getattr(response, "candidates", None):
            parts = response.candidates[0].content.parts
            return "".join(getattr(p, "text", "") or "" for p in parts).strip()
        return str(response).strip()

    def generate_quiz(self, text: str, num_questions: int = 10, question_type: str = "mixed") -> str:
        if question_type == "mcq":
            desc = "multiple choice"
            format_instruction = """{
    "question": "Question text",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct",
    "type": "mcq"
}"""
        elif question_type == "short_answer":
            desc = "short answer"
            format_instruction = """{
    "question": "Question text",
    "correct_answer": "Expected short answer",
    "explanation": "Why this is correct",
    "type": "short_answer"
}"""
        else:
            desc = "mixed (some multiple choice and some short answer)"
            format_instruction = """For multiple choice:
{
    "question": "Question text",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct",
    "type": "mcq"
}
For short answer:
{
    "question": "Question text",
    "correct_answer": "Expected short answer",
    "explanation": "Why this is correct",
    "type": "short_answer"
}"""

        prompt = f"""Create a {num_questions}-question {desc} quiz based on this text.

Text: {text[:3000]}

Format each question as JSON according to its type:
{format_instruction}

Return as JSON array only, no markdown."""
        return self._generate(
            prompt,
            system="You are an expert quiz creator for students.",
            temperature=0.7,
        )

    def generate_summary(self, text: str, length: str = "moderate") -> str:
        length_map = {
            "brief": "2-3 sentences",
            "moderate": "1-2 paragraphs",
            "detailed": "3-4 paragraphs",
        }
        prompt = f"""Summarize the following text in {length_map.get(length, '1-2 paragraphs')}:

{text[:4000]}

Summary:"""
        return self._generate(
            prompt,
            system="You are an expert summarizer for students.",
            temperature=0.5,
        )

    def task_tutor(self, task_title: str, task_description: str) -> str:
        prompt = f"""Task: {task_title}
Description: {task_description}

Provide learning guidance in this JSON format only, no markdown:
{{
    "explanation": "What this task is about (2-3 sentences)",
    "learning_steps": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
    "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
    "study_tips": ["Tip 1", "Tip 2", "Tip 3", "Tip 4"],
    "estimated_time": 60
}}"""
        return self._generate(
            prompt,
            system="You are a helpful tutor for students.",
            temperature=0.7,
        )

    def parse_quiz_response(self, raw: str) -> list:
        parsed = _parse_json(raw)
        if isinstance(parsed, list):
            return parsed
        if isinstance(parsed, dict) and "questions" in parsed:
            return parsed["questions"]
        return [{"question": raw[:500], "type": "short_answer"}]

    def parse_tutor_response(self, raw: str, task_title: str) -> dict:
        parsed = _parse_json(raw)
        if isinstance(parsed, dict) and parsed.get("explanation"):
            return parsed
        return {
            "explanation": (raw or "")[:300],
            "learning_steps": [
                "Read the task requirements",
                "Break the work into small steps",
                "Research key concepts",
                "Complete the deliverable",
                "Review and revise",
            ],
            "key_concepts": [task_title],
            "study_tips": ["Take notes", "Use practice problems", "Review daily"],
            "estimated_time": 60,
        }

    def generate_with_retry(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        try:
            return self._generate(prompt, temperature=temperature)
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}") from e


_gemini_client = None


def get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = GeminiClient()
    return _gemini_client
