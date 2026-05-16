"""
AI Service Coordinator - HYBRID APPROACH

| Feature            | Module                         | Key / model        |
|--------------------|--------------------------------|--------------------|
| Quiz, Summary, Tutor | gemini_client (via ai_client) | GEMINI_API_KEY     |
| Flashcards         | custom_model.py                | Local trained model |
| Video recommendations | video_recommender.py        | YOUTUBE_API_KEY    |
| Task suggestions   | (this file)                    | Rule-based, no AI  |
"""

import json
from app.ai.ai_client import get_ai_client, get_ai_provider_name
from app.ai.custom_model import get_custom_model
from app.ai.video_recommender import get_video_recommender
from app.ai.text_processor import TextProcessor
from werkzeug.datastructures import FileStorage

class AIService:
    
    @staticmethod
    def generate_summary(text: str = None, file: FileStorage = None, length: str = 'moderate'):
        """Gemini API — summarization (requires GEMINI_API_KEY)"""
        try:
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text or len(text.strip()) < 50:
                return None, "Text is too short (minimum 50 characters)"
            
            client = get_ai_client()
            summary = client.generate_summary(text, length)
            
            return {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'ai_provider': get_ai_provider_name()
            }, None
            
        except Exception as e:
            return None, f"Failed to generate summary: {str(e)}"
    
    @staticmethod
    def generate_quiz(text: str = None, file: FileStorage = None, 
                     num_questions: int = 10, question_type: str = 'mixed'):
        """Gemini API — quiz generation (requires GEMINI_API_KEY)"""
        try:
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text or len(text.strip()) < 50:
                return None, "Text is too short (minimum 50 characters)"
            
            client = get_ai_client()
            quiz_data = client.generate_quiz(text, num_questions)
            
            # Parse JSON response
            import json as json_lib
            try:
                questions = json_lib.loads(quiz_data)
            except:
                questions = [{"question": quiz_data, "type": "short_answer"}]
            
            return {
                'questions': questions,
                'total_questions': len(questions),
                'question_type': question_type,
                'ai_provider': get_ai_provider_name()
            }, None
            
        except Exception as e:
            return None, f"Failed to generate quiz: {str(e)}"
    
    @staticmethod
    def generate_flashcards(text: str = None, file: FileStorage = None, num_cards: int = 20):
        """Use Custom Model for flashcards"""
        try:
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text or len(text.strip()) < 50:
                return None, "Text is too short (minimum 50 characters)"
            
            custom_model = get_custom_model()
            flashcards = custom_model.generate_flashcards(text, num_cards)
            
            return {
                'flashcards': flashcards,
                'total_cards': len(flashcards),
                'ai_provider': 'Custom Trained Model'
            }, None
            
        except Exception as e:
            return None, f"Failed to generate flashcards: {str(e)}"
    
    @staticmethod
    def recommend_materials(topic: str):
        """YouTube Data API — video recommendations (YOUTUBE_API_KEY in .env)"""
        try:
            if not topic or len(topic.strip()) < 3:
                return None, "Topic must be at least 3 characters"
            
            recommender = get_video_recommender()
            results = recommender.recommend_videos(topic)
            
            return results, None
            
        except Exception as e:
            return None, f"Failed to get recommendations: {str(e)}"
    
    @staticmethod
    def get_task_tutoring(task_title: str, task_description: str):
        """Gemini API — task tutoring (requires GEMINI_API_KEY)"""
        try:
            if not task_title or not task_description:
                return None, "Task title and description are required"
            
            client = get_ai_client()
            guidance = client.task_tutor(task_title, task_description)
            
            # Parse JSON response
            import json as json_lib
            try:
                guidance_dict = json_lib.loads(guidance)
            except:
                guidance_dict = {
                    'explanation': guidance[:200],
                    'learning_steps': ['Read carefully', 'Break down task', 'Research', 'Execute', 'Review'],
                    'key_concepts': [task_title],
                    'study_tips': ['Take notes', 'Practice regularly'],
                    'estimated_time': 60
                }
            
            return guidance_dict, None
            
        except Exception as e:
            return None, f"Failed to generate tutoring: {str(e)}"
    
    @staticmethod
    def suggest_course_tasks(course_name: str, description: str, num_tasks: int = 5):
        """Rule-based task suggestions (no AI needed)"""
        try:
            # Simple rule-based suggestions
            tasks = []
            keywords = description.lower().split()
            
            # Common task templates
            templates = [
                {"title": f"Read {course_name} Introduction", "priority": "high", "estimated_time": 60},
                {"title": f"Complete {course_name} Practice Problems", "priority": "high", "estimated_time": 120},
                {"title": f"Review {course_name} Key Concepts", "priority": "medium", "estimated_time": 45},
                {"title": f"Prepare {course_name} Study Notes", "priority": "medium", "estimated_time": 90},
                {"title": f"Take {course_name} Practice Quiz", "priority": "low", "estimated_time": 30}
            ]
            
            for i, template in enumerate(templates[:num_tasks]):
                tasks.append({
                    "title": template["title"],
                    "description": f"Complete this task for {course_name}",
                    "priority": template["priority"],
                    "estimated_time": template["estimated_time"],
                    "deadline_days": 7
                })
            
            return {
                'tasks': tasks,
                'total_suggestions': len(tasks),
                'course_name': course_name,
                'method': 'rule-based'
            }, None
            
        except Exception as e:
            return None, f"Failed to generate suggestions: {str(e)}"