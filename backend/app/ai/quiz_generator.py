"""
DEPRECATED: Use ai_service.py -> openai_client.py (hybrid AI routing).
Kept for reference; not used by API routes.
"""

from app.ai.groq_client import get_groq_client
from app.ai.text_processor import TextProcessor
import json

class QuizGenerator:
    """Generate quizzes from text"""
    
    @staticmethod
    def generate_quiz(text: str, num_questions: int = 10, question_type: str = 'mixed') -> dict:
        """
        Generate quiz questions from text
        
        Args:
            text (str): Input text to generate quiz from
            num_questions (int): Number of questions (5-50)
            question_type (str): Type of questions ('mcq', 'short_answer', 'mixed')
            
        Returns:
            dict: Quiz with questions array
        """
        # Validate inputs
        if not TextProcessor.validate_text(text, min_length=50):
            raise ValueError("Text is too short to generate quiz (minimum 50 characters)")
        
        if num_questions < 5 or num_questions > 50:
            raise ValueError("Number of questions must be between 5 and 50")
        
        # Clean text
        clean_text = TextProcessor.clean_text(text, max_length=8000)
        
        # Create prompt based on question type
        if question_type == 'mcq':
            instruction = f"Generate {num_questions} multiple choice questions with 4 options each (A, B, C, D). Include the correct answer and a brief explanation."
        elif question_type == 'short_answer':
            instruction = f"Generate {num_questions} short answer questions. Include the correct answer for each."
        else:  # mixed
            mcq_count = num_questions // 2
            sa_count = num_questions - mcq_count
            instruction = f"Generate {mcq_count} multiple choice questions with 4 options and {sa_count} short answer questions. Include correct answers and explanations."
        
        prompt = f"""{instruction}

Based on this text:
{clean_text}

Format your response as a JSON array with this structure:
[
  {{
    "question": "Question text",
    "type": "mcq" or "short_answer",
    "options": ["A) option1", "B) option2", "C) option3", "D) option4"] (only for MCQ),
    "correct_answer": "B" or "answer text",
    "explanation": "Why this is correct"
  }}
]

Questions:"""
        
        try:
            client = get_groq_client()
            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    questions = json.loads(json_str)
                else:
                    # Fallback: parse manually
                    questions = QuizGenerator._parse_questions_fallback(response, num_questions)
            except:
                questions = QuizGenerator._parse_questions_fallback(response, num_questions)
            
            return {
                'questions': questions,
                'total_questions': len(questions),
                'question_type': question_type
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate quiz: {str(e)}")
    
    @staticmethod
    def _parse_questions_fallback(text: str, num_questions: int) -> list:
        """Fallback parser if JSON parsing fails"""
        questions = []
        lines = text.split('\n')
        
        current_q = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Simple parsing logic
            if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.')):
                if current_q:
                    questions.append(current_q)
                current_q = {
                    'question': line,
                    'type': 'short_answer',
                    'correct_answer': 'See explanation',
                    'explanation': 'Generated from text'
                }
        
        if current_q:
            questions.append(current_q)
        
        return questions[:num_questions]
