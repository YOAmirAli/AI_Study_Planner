"""
DEPRECATED: Use ai_service.py -> custom_model.py (trained T5 flashcards).
"""

from app.ai.groq_client import get_groq_client
from app.ai.text_processor import TextProcessor
import json

class FlashcardGenerator:
    """Generate flashcards from text"""
    
    @staticmethod
    def generate_flashcards(text: str, num_cards: int = 20) -> dict:
        """
        Generate flashcards from text
        
        Args:
            text (str): Input text to generate flashcards from
            num_cards (int): Number of flashcards (5-30)
            
        Returns:
            dict: Flashcards array with question-answer pairs
        """
        # Validate inputs
        if not TextProcessor.validate_text(text, min_length=50):
            raise ValueError("Text is too short to generate flashcards (minimum 50 characters)")
        
        if num_cards < 5 or num_cards > 30:
            raise ValueError("Number of flashcards must be between 5 and 30")
        
        # Clean text
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
        
        try:
            client = get_groq_client()
            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Try to parse JSON response
            try:
                json_start = response.find('[')
                json_end = response.rfind(']') + 1
                if json_start != -1 and json_end > json_start:
                    json_str = response[json_start:json_end]
                    flashcards = json.loads(json_str)
                else:
                    flashcards = FlashcardGenerator._parse_flashcards_fallback(response, num_cards)
            except:
                flashcards = FlashcardGenerator._parse_flashcards_fallback(response, num_cards)
            
            return {
                'flashcards': flashcards,
                'total_cards': len(flashcards)
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate flashcards: {str(e)}")
    
    @staticmethod
    def _parse_flashcards_fallback(text: str, num_cards: int) -> list:
        """Fallback parser if JSON parsing fails"""
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
