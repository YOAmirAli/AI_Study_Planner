"""
Text Summarizer using Groq API
"""

from app.ai.groq_client import get_groq_client
from app.ai.text_processor import TextProcessor

class Summarizer:
    """Generate summaries from text"""
    
    @staticmethod
    def summarize(text: str, length: str = 'moderate') -> dict:
        """
        Generate summary from text
        
        Args:
            text (str): Input text to summarize
            length (str): Summary length ('brief', 'moderate', 'detailed')
            
        Returns:
            dict: Summary result with text and metadata
        """
        # Validate text
        if not TextProcessor.validate_text(text, min_length=50):
            raise ValueError("Text is too short to summarize (minimum 50 characters)")
        
        # Clean text
        clean_text = TextProcessor.clean_text(text, max_length=10000)
        
        # Determine summary parameters based on length
        length_params = {
            'brief': {
                'instruction': 'Provide a very brief summary in 2-3 sentences',
                'max_tokens': 200
            },
            'moderate': {
                'instruction': 'Provide a moderate summary in 1-2 paragraphs',
                'max_tokens': 500
            },
            'detailed': {
                'instruction': 'Provide a detailed summary covering all main points',
                'max_tokens': 1000
            }
        }
        
        params = length_params.get(length, length_params['moderate'])
        
        # Create prompt
        prompt = f"""{params['instruction']} of the following text:

{clean_text}

Summary:"""
        
        try:
            # Get Groq client and generate summary
            client = get_groq_client()
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
                'length_type': length
            }
            
        except Exception as e:
            raise Exception(f"Failed to generate summary: {str(e)}")
