"""
Quiz Generator for Tasks using Unified AI Client
Generates MCQ quizzes based on completed tasks
"""

from app.ai.ai_client import get_ai_client
import json

class TaskQuizGenerator:
    """Generate MCQ quizzes for completed tasks"""
    
    @staticmethod
    def generate_quiz(task_title: str, task_description: str, num_questions: int = 10) -> dict:
        """
        Generate MCQ quiz based on task content
        
        Args:
            task_title (str): Title of the task
            task_description (str): Description of the task
            num_questions (int): Number of questions to generate (5-20)
            
        Returns:
            dict: Quiz with questions array
        """
        if num_questions < 5 or num_questions > 20:
            num_questions = 10
        
        try:
            client = get_ai_client()
            
            prompt = f"""Generate a {num_questions}-question multiple choice quiz to test understanding of the following task:

Task: {task_title}
Description: {task_description}

Create challenging but fair questions that test understanding of key concepts.

Format as JSON array:
[
  {{
    "question": "Question text here?",
    "option_a": "First option",
    "option_b": "Second option",
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_answer": "A",
    "explanation": "Why this answer is correct and others are wrong"
  }}
]

Generate exactly {num_questions} questions."""

            # We can use the existing client methods
            # But the client interface usually returns generic raw text and we parse it.
            # To be safe with Gemini/OpenAI format expectations, we call the raw _generate or chat if we had it.
            # Wait, the ai_client clients already have generate_quiz! Let's just use it!
            
            # Use the existing generate_quiz logic from the client
            task_text = f"Task: {task_title}\nDescription: {task_description}"
            raw = client.generate_quiz(task_text, num_questions=num_questions, question_type="mcq")
            questions = client.parse_quiz_response(raw)
            
            # Format questions to match the expected DB schema for TaskQuizGenerator
            formatted_questions = []
            for i, q in enumerate(questions[:num_questions], 1):
                # The generic client returns options as a list: ["A) ...", "B) ..."]
                # We need to map them to option_a, option_b, etc.
                options = q.get('options', [])
                opt_a = options[0] if len(options) > 0 else 'Option A'
                opt_b = options[1] if len(options) > 1 else 'Option B'
                opt_c = options[2] if len(options) > 2 else 'Option C'
                opt_d = options[3] if len(options) > 3 else 'Option D'
                
                # Strip "A) " prefix if present
                if opt_a.startswith("A) "): opt_a = opt_a[3:]
                if opt_b.startswith("B) "): opt_b = opt_b[3:]
                if opt_c.startswith("C) "): opt_c = opt_c[3:]
                if opt_d.startswith("D) "): opt_d = opt_d[3:]

                formatted_questions.append({
                    'question_number': i,
                    'question_text': q.get('question', f'Question {i}'),
                    'option_a': opt_a,
                    'option_b': opt_b,
                    'option_c': opt_c,
                    'option_d': opt_d,
                    'correct_answer': q.get('correct_answer', 'A').upper().replace(")", "").strip(),
                    'explanation': q.get('explanation', 'Correct answer explanation')
                })
            
            return {
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            }

        except Exception as e:
            print(f"Error generating quiz: {str(e)}")
            # Return fallback quiz
            return {
                'questions': TaskQuizGenerator._generate_fallback_quiz(task_title, num_questions),
                'total_questions': num_questions
            }
    
    @staticmethod
    def _generate_fallback_quiz(task_title: str, num_questions: int) -> list:
        """Generate a simple fallback quiz if AI fails"""
        questions = []
        for i in range(1, min(num_questions + 1, 6)):
            questions.append({
                'question_number': i,
                'question_text': f'What is an important concept related to {task_title}?',
                'option_a': 'Understanding the basics',
                'option_b': 'Skipping the fundamentals',
                'option_c': 'Ignoring best practices',
                'option_d': 'Avoiding documentation',
                'correct_answer': 'A',
                'explanation': 'Understanding the basics is crucial for mastering any topic.'
            })
        return questions
