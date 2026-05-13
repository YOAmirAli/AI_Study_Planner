"""
AI Service Coordinator
Supports both OpenAI (primary) and Groq (fallback)
"""

import os
from app.ai.openai_client import get_openai_client
from app.ai.groq_client import get_groq_client
from app.ai.text_processor import TextProcessor
from werkzeug.datastructures import FileStorage

class AIService:
    """Coordinate AI operations with OpenAI primary, Groq fallback"""
    
    @staticmethod
    def _get_ai_client():
        """Get available AI client (prefer OpenAI, fallback to Groq)"""
        try:
            return get_openai_client(), 'openai'
        except ValueError:
            try:
                return get_groq_client(), 'groq'
            except ValueError:
                raise Exception("No AI API key configured. Please set OPENAI_API_KEY or GROQ_API_KEY")
    
    @staticmethod
    def generate_summary(text: str = None, file: FileStorage = None, length: str = 'moderate'):
        """Generate summary from text or PDF file"""
        try:
            # Extract text from PDF if file provided
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text:
                return None, "No text provided"
            
            # Clean text
            clean_text = TextProcessor.clean_text(text, max_length=10000)
            
            # Determine summary parameters
            length_params = {
                'brief': {'instruction': 'Provide a very brief summary in 2-3 sentences', 'max_tokens': 200},
                'moderate': {'instruction': 'Provide a moderate summary in 1-2 paragraphs', 'max_tokens': 500},
                'detailed': {'instruction': 'Provide a detailed summary covering all main points', 'max_tokens': 1000}
            }
            params = length_params.get(length, length_params['moderate'])
            
            # Create prompt
            prompt = f"""{params['instruction']} of the following text:

{clean_text}

Summary:"""
            
            # Get AI client and generate
            client, provider = AIService._get_ai_client()
            summary = client.generate_with_retry(
                prompt=prompt,
                max_tokens=params['max_tokens'],
                temperature=0.5
            )
            
            return {
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': round(len(summary) / len(text) * 100, 2),
                'length_type': length,
                'ai_provider': provider
            }, None
            
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, f"Failed to generate summary: {str(e)}"
    
    @staticmethod
    def generate_quiz(text: str = None, file: FileStorage = None, 
                     num_questions: int = 10, question_type: str = 'mixed'):
        """Generate quiz from text or PDF file"""
        try:
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text:
                return None, "No text provided"
            
            clean_text = TextProcessor.clean_text(text, max_length=8000)
            
            # Create prompt based on question type
            if question_type == 'mcq':
                instruction = f"Generate {num_questions} multiple choice questions with 4 options each (A, B, C, D). Include the correct answer and a brief explanation."
            elif question_type == 'short_answer':
                instruction = f"Generate {num_questions} short answer questions. Include the correct answer for each."
            else:
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
            
            client, provider = AIService._get_ai_client()
            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse JSON response
            import json
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                questions = json.loads(json_str)
            else:
                questions = AIService._parse_questions_fallback(response, num_questions)
            
            return {
                'questions': questions,
                'total_questions': len(questions),
                'question_type': question_type,
                'ai_provider': provider
            }, None
            
        except Exception as e:
            return None, f"Failed to generate quiz: {str(e)}"
    
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
            
            if line.startswith(('1.', '2.', '3.', '4.', '5.')):
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
    
    @staticmethod
    def generate_flashcards(text: str = None, file: FileStorage = None, num_cards: int = 20):
        """Generate flashcards from text or PDF file"""
        try:
            if file:
                if not file.filename.endswith('.pdf'):
                    return None, "Only PDF files are supported"
                text = TextProcessor.extract_from_pdf(file.read())
            
            if not text:
                return None, "No text provided"
            
            clean_text = TextProcessor.clean_text(text, max_length=8000)
            
            prompt = f"""Generate {num_cards} flashcards from the following text. Each flashcard should have a question on one side and a concise answer on the other.

Text:
{clean_text}

Format your response as a JSON array:
[
  {{
    "question": "Question or term",
    "answer": "Answer or definition",
    "category": "topic category"
  }}
]

Flashcards:"""
            
            client, provider = AIService._get_ai_client()
            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            import json
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                flashcards = json.loads(json_str)
            else:
                flashcards = AIService._parse_flashcards_fallback(response, num_cards)
            
            return {
                'flashcards': flashcards,
                'total_cards': len(flashcards),
                'ai_provider': provider
            }, None
            
        except Exception as e:
            return None, f"Failed to generate flashcards: {str(e)}"
    
    @staticmethod
    def _parse_flashcards_fallback(text: str, num_cards: int) -> list:
        """Fallback parser for flashcards"""
        flashcards = []
        lines = text.split('\n')
        
        current_card = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if 'Q:' in line or 'Question:' in line:
                if current_card and 'question' in current_card:
                    flashcards.append(current_card)
                current_card = {'question': line.split(':', 1)[1].strip() if ':' in line else line}
            elif 'A:' in line or 'Answer:' in line:
                if current_card:
                    current_card['answer'] = line.split(':', 1)[1].strip() if ':' in line else line
                    current_card['category'] = 'General'
        
        if current_card and 'question' in current_card:
            flashcards.append(current_card)
        
        return flashcards[:num_cards]
    
    @staticmethod
    def recommend_materials(topic: str):
        """Recommend study materials for a topic"""
        try:
            if not topic or len(topic.strip()) < 3:
                return None, "Topic must be at least 3 characters"
            
            prompt = f"""Generate 8 popular and highly-rated educational YouTube video recommendations for the topic: "{topic}".

For each video, provide:
1. A realistic video title
2. Channel name (use real popular educational channels)
3. Estimated duration (format: MM:SS)
4. Brief description

Format as JSON array:
[
  {{
    "title": "Video title",
    "channel": "Channel name",
    "duration": "15:30",
    "description": "Brief description"
  }}
]

Focus on well-known educational channels like Khan Academy, Crash Course, freeCodeCamp, MIT OpenCourseWare, 3Blue1Brown, etc.

Videos:"""
            
            client, provider = AIService._get_ai_client()
            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            
            import json
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                videos_data = json.loads(json_str)
                
                videos = []
                for idx, video in enumerate(videos_data[:8]):
                    search_query = f"{video.get('title', topic)} {video.get('channel', '')}"
                    videos.append({
                        'title': video.get('title', f'{topic} Tutorial'),
                        'channel': video.get('channel', 'Educational Channel'),
                        'thumbnail': f'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                        'url': f'https://youtube.com/results?search_query={search_query.replace(" ", "+")}',
                        'duration': video.get('duration', '15:00'),
                        'description': video.get('description', 'Educational video')
                    })
                
                return {
                    'videos': videos,
                    'total_results': len(videos),
                    'search_query': topic,
                    'ai_provider': provider,
                    'note': 'AI-generated recommendations. Click to search on YouTube.'
                }, None
            else:
                return AIService._get_fallback_recommendations(topic), None
                
        except Exception as e:
            return AIService._get_fallback_recommendations(topic), None
    
    @staticmethod
    def _get_fallback_recommendations(topic: str) -> dict:
        """Fallback recommendations"""
        return {
            'videos': [
                {
                    'title': f'{topic} - Complete Tutorial',
                    'channel': 'freeCodeCamp',
                    'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                    'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+tutorial',
                    'duration': '15:30',
                    'description': 'Comprehensive tutorial'
                },
                {
                    'title': f'{topic} - Crash Course',
                    'channel': 'Crash Course',
                    'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                    'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+crash+course',
                    'duration': '12:45',
                    'description': 'Quick overview'
                },
                {
                    'title': f'{topic} Explained',
                    'channel': 'Khan Academy',
                    'thumbnail': 'https://img.youtube.com/vi/placeholder/mqdefault.jpg',
                    'url': f'https://youtube.com/results?search_query={topic.replace(" ", "+")}+explained',
                    'duration': '10:20',
                    'description': 'Clear explanation'
                }
            ],
            'total_results': 3,
            'search_query': topic,
            'note': 'Showing recommended searches. Click to find videos on YouTube.'
        }