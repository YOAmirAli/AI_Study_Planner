"""
OpenAI API Client — optional fallback only.
Primary LLM for quiz, summary, and tutor is gemini_client.py (GEMINI_API_KEY).
"""

import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-3.5-turbo"  # Good balance of quality and cost
    
    def generate_quiz(self, text: str, num_questions: int = 10) -> dict:
        """Generate multiple choice quiz from text"""
        prompt = f"""Create a {num_questions}-question multiple choice quiz based on this text.

Text: {text[:3000]}

Format each question as JSON:
{{
    "question": "Question text",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Why this is correct"
}}

Return as JSON array."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert quiz creator for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def generate_summary(self, text: str, length: str = "moderate") -> str:
        """Generate summary from text"""
        length_map = {
            "brief": "2-3 sentences",
            "moderate": "1-2 paragraphs", 
            "detailed": "3-4 paragraphs"
        }
        
        prompt = f"""Summarize the following text in {length_map[length]}:

{text[:4000]}

Summary:"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert summarizer for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        return response.choices[0].message.content
    
    def task_tutor(self, task_title: str, task_description: str) -> dict:
        """Generate learning guidance for a task"""
        prompt = f"""Task: {task_title}
Description: {task_description}

Provide learning guidance in this JSON format:
{{
    "explanation": "What this task is about (2-3 sentences)",
    "learning_steps": ["Step 1", "Step 2", "Step 3", "Step 4", "Step 5"],
    "key_concepts": ["Concept 1", "Concept 2", "Concept 3"],
    "study_tips": ["Tip 1", "Tip 2", "Tip 3", "Tip 4"],
    "estimated_time": 60
}}"""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful tutor for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    
    def generate_with_retry(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Generic completion with retry"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")


# Global instance
_openai_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client