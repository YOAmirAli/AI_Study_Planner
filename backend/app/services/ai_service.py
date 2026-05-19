"""
AI Service Coordinator - HYBRID APPROACH

| Feature              | Module              | Backend              |
|----------------------|---------------------|----------------------|
| Quiz, Summary, Tutor | openai_client.py    | OPENAI_API_KEY       |
| Flashcards           | custom_model.py     | T5 fine-tuned local  |
| Video recommendations| video_recommender.py| YOUTUBE_API_KEY / search |
| Task suggestions     | (this file)         | Rule-based, no AI    |
"""

from werkzeug.datastructures import FileStorage

from app.ai.custom_model import get_custom_model
from app.ai.ai_client import get_ai_client, get_ai_provider_name
from app.ai.text_processor import TextProcessor
from app.ai.video_recommender import get_video_recommender


class AIService:
    @staticmethod
    def _extract_text(text: str = None, file: FileStorage = None):
        if file:
            if not file.filename.lower().endswith(".pdf"):
                return None, "Only PDF files are supported"
            text = TextProcessor.extract_from_pdf(file.read())
        if not text or len(text.strip()) < 50:
            return None, "Text is too short (minimum 50 characters)"
        return text, None

    @staticmethod
    def generate_summary(text: str = None, file: FileStorage = None, length: str = "moderate"):
        """OpenAI API — summarization"""
        try:
            text, err = AIService._extract_text(text, file)
            if err:
                return None, err

            client = get_ai_client()
            summary = client.generate_summary(text, length)

            original_length = len(text)
            summary_length = len(summary)
            compression_ratio = (
                round(summary_length / original_length * 100, 1)
                if original_length > 0
                else 0
            )

            return {
                "summary": summary,
                "original_length": original_length,
                "summary_length": summary_length,
                "compression_ratio": compression_ratio,
                "ai_provider": get_ai_provider_name(),
            }, None
        except Exception as e:
            return None, f"Failed to generate summary: {str(e)}"

    @staticmethod
    def generate_quiz(
        text: str = None,
        file: FileStorage = None,
        num_questions: int = 10,
        question_type: str = "mixed",
    ):
        """OpenAI API — quiz generation"""
        try:
            text, err = AIService._extract_text(text, file)
            if err:
                return None, err

            client = get_ai_client()
            raw = client.generate_quiz(text, num_questions, question_type=question_type)
            questions = client.parse_quiz_response(raw)

            return {
                "questions": questions,
                "total_questions": len(questions),
                "question_type": question_type,
                "ai_provider": get_ai_provider_name(),
            }, None
        except Exception as e:
            return None, f"Failed to generate quiz: {str(e)}"

    @staticmethod
    def generate_flashcards(text: str = None, file: FileStorage = None, num_cards: int = 20):
        """Custom T5 model — flashcard generation"""
        try:
            text, err = AIService._extract_text(text, file)
            if err:
                return None, err

            custom_model = get_custom_model()
            flashcards = custom_model.generate_flashcards(text, num_cards)

            return {
                "flashcards": flashcards,
                "total_cards": len(flashcards),
                "ai_provider": custom_model.provider_label,
            }, None
        except Exception as e:
            return None, f"Failed to generate flashcards: {str(e)}"

    @staticmethod
    def recommend_materials(topic: str):
        """YouTube API or youtube-search-python fallback"""
        try:
            if not topic or len(topic.strip()) < 3:
                return None, "Topic must be at least 3 characters"

            recommender = get_video_recommender()
            results = recommender.recommend_videos(topic)

            if results.get("error") and not results.get("videos"):
                return None, results.get("error", "No videos found")

            return results, None
        except Exception as e:
            return None, f"Failed to get recommendations: {str(e)}"

    @staticmethod
    def get_task_tutoring(task_title: str, task_description: str):
        """OpenAI API — learning guidance"""
        try:
            if not task_title or not task_description:
                return None, "Task title and description are required"

            client = get_ai_client()
            raw = client.task_tutor(task_title, task_description)
            guidance_dict = client.parse_tutor_response(raw, task_title)

            return guidance_dict, None
        except Exception as e:
            return None, f"Failed to generate tutoring: {str(e)}"

    @staticmethod
    def suggest_course_tasks(course_name: str, description: str, num_tasks: int = 5):
        """Rule-based task suggestions (no AI)"""
        try:
            templates = [
                {
                    "title": f"Read {course_name} Introduction",
                    "priority": "high",
                    "estimated_time": 60,
                },
                {
                    "title": f"Complete {course_name} Practice Problems",
                    "priority": "high",
                    "estimated_time": 120,
                },
                {
                    "title": f"Review {course_name} Key Concepts",
                    "priority": "medium",
                    "estimated_time": 45,
                },
                {
                    "title": f"Prepare {course_name} Study Notes",
                    "priority": "medium",
                    "estimated_time": 90,
                },
                {
                    "title": f"Take {course_name} Practice Quiz",
                    "priority": "low",
                    "estimated_time": 30,
                },
            ]

            tasks = []
            for template in templates[:num_tasks]:
                tasks.append(
                    {
                        "title": template["title"],
                        "description": f"Complete this task for {course_name}. {description[:120]}",
                        "priority": template["priority"],
                        "estimated_time": template["estimated_time"],
                        "deadline_days": 7,
                    }
                )

            return {
                "tasks": tasks,
                "total_suggestions": len(tasks),
                "course_name": course_name,
                "method": "rule-based",
            }, None
        except Exception as e:
            return None, f"Failed to generate suggestions: {str(e)}"
