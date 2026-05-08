import openai
from django.conf import settings

class AIService:
    def __init__(self):
        openai.api_key = settings.OPENAI_API_KEY

    def generate_study_plan(self, tasks, available_hours):
        """Generate a study plan based on tasks"""
        prompt = f"""
        Create a study plan for the following tasks:
        {tasks}
        Available study hours: {available_hours}
        
        Provide a day-by-day schedule with time allocations.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

    def generate_summary(self, text):
        """Generate summary of study material"""
        prompt = f"Summarize the following text concisely:\n{text}"
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content

    def generate_quiz(self, topic, num_questions=5):
        """Generate quiz questions"""
        prompt = f"""
        Generate {num_questions} multiple-choice quiz questions about {topic}.
        Include 4 options per question and mark the correct answer.
        """
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return response.choices[0].message.content