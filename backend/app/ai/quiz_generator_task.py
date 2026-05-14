
from app.ai.groq_client import get_groq_client
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
            client = get_groq_client()
            
            prompt = f"""Generate a {num_questions}-question multiple choice quiz to test understanding of the following task:

Task: {task_title}
Description: {task_description}

Create challenging but fair questions that test:
- Understanding of key concepts
- Application of knowledge
- Critical thinking
- Problem-solving

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

Make questions clear, concise, and educational. Ensure only ONE answer is correct.
Generate exactly {num_questions} questions.

Questions:"""

            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=3000,
                temperature=0.7
            )
            
            # Parse JSON response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                questions = json.loads(json_str)
                
                # Validate and format questions
                formatted_questions = []
                for i, q in enumerate(questions[:num_questions], 1):
                    formatted_questions.append({
                        'question_number': i,
                        'question_text': q.get('question', f'Question {i}'),
                        'option_a': q.get('option_a', 'Option A'),
                        'option_b': q.get('option_b', 'Option B'),
                        'option_c': q.get('option_c', 'Option C'),
                        'option_d': q.get('option_d', 'Option D'),
                        'correct_answer': q.get('correct_answer', 'A').upper(),
                        'explanation': q.get('explanation', 'Correct answer explanation')
                    })
                
                return {
                    'questions': formatted_questions,
                    'total_questions': len(formatted_questions)
                }
            else:
                raise ValueError("Could not parse AI response")
                
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
