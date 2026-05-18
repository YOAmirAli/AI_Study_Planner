"""
OpenAI API client for quiz generation, summarization, and task tutoring.
Requires OPENAI_API_KEY in backend/.env
"""

import json
import os
import re

from openai import OpenAI


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


class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key or self.api_key.startswith("your-"):
            raise ValueError(
                "OPENAI_API_KEY is required. Set a valid key in backend/.env"
            )
        self.client = OpenAI(api_key=self.api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    def generate_quiz(self, text: str, num_questions: int = 10, question_type: str = "mixed") -> str:
        if question_type == "mcq":
            desc = "multiple choice"
            format_instruction = """{
  "question": "string",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_answer": "A",
  "explanation": "string",
  "type": "mcq"
}"""
        elif question_type == "short_answer":
            desc = "short answer"
            format_instruction = """{
  "question": "string",
  "correct_answer": "string",
  "explanation": "string",
  "type": "short_answer"
}"""
        else:
            desc = "mixed (some multiple choice and some short answer)"
            format_instruction = """For multiple choice:
{
  "question": "string",
  "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
  "correct_answer": "A",
  "explanation": "string",
  "type": "mcq"
}
For short answer:
{
  "question": "string",
  "correct_answer": "string",
  "explanation": "string",
  "type": "short_answer"
}"""

        prompt = f"""Create exactly {num_questions} {desc} quiz questions from this study material.

Material:
{text[:3500]}

Return ONLY a JSON array. Each item formatted according to its type:
{format_instruction}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You create accurate academic quizzes. Output valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=2500,
        )
        return response.choices[0].message.content or "[]"

    def generate_summary(self, text: str, length: str = "moderate") -> str:
        length_map = {
            "brief": "2-3 sentences",
            "moderate": "1-2 paragraphs",
            "detailed": "3-4 paragraphs",
        }
        target = length_map.get(length, length_map["moderate"])

        prompt = f"""Summarize the following study material in {target}. Be clear and student-friendly.

Material:
{text[:4500]}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert academic summarizer.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.5,
            max_tokens=1200,
        )
        return (response.choices[0].message.content or "").strip()

    def task_tutor(self, task_title: str, task_description: str) -> str:
        prompt = f"""Task title: {task_title}
Task description: {task_description}

Return ONLY JSON (no markdown):
{{
  "explanation": "2-3 sentences",
  "learning_steps": ["step1", "step2", "step3", "step4", "step5"],
  "key_concepts": ["concept1", "concept2", "concept3"],
  "study_tips": ["tip1", "tip2", "tip3"],
  "estimated_time": 60
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a supportive study tutor. Output valid JSON only.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=1500,
        )
        return response.choices[0].message.content or "{}"

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


_openai_client = None


def get_openai_client() -> OpenAIClient:
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client
