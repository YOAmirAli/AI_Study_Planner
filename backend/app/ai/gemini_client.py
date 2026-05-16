"""
Google Gemini API Client - For quiz, summary, and tutoring
"""

import os
import google.generativeai as genai


class GeminiClient:
    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        genai.configure(api_key=self.api_key)
        model_name = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
        self.model = genai.GenerativeModel(model_name)

    def _generate(self, prompt: str, system: str = None, temperature: float = 0.7) -> str:
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        response = self.model.generate_content(
            full_prompt,
            generation_config={"temperature": temperature},
        )
        return response.text

    def generate_quiz(self, text: str, num_questions: int = 10) -> str:
        prompt = f"""Create a {num_questions}-question multiple choice quiz based on this text.

Text: {text[:3000]}

Format each question as JSON:
{{
    "question": "Question text",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct"
}}

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
