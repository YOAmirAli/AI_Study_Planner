"""
Groq API Client
Wrapper for Groq API (free alternative to OpenAI)
"""

import os
from groq import Groq

class GroqClient:
    """Groq API client for AI operations"""
    
    def __init__(self):
        """Initialize Groq client"""
        self.api_key = os.getenv('GROQ_API_KEY')
        self.model = os.getenv('GROQ_MODEL', 'meta-llama/llama-4-maverick-17b-128e-instruct')
        
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=self.api_key)
    
    def generate_completion(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text completion using Groq API
        
        Args:
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens to generate
            temperature (float): Sampling temperature (0-1)
            
        Returns:
            str: Generated text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant for students."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            raise Exception(f"Groq API error: {str(e)}")
    
    def generate_with_retry(self, prompt: str, max_tokens: int = 1000, 
                           temperature: float = 0.7, max_retries: int = 3) -> str:
        """
        Generate completion with retry logic
        
        Args:
            prompt (str): Input prompt
            max_tokens (int): Maximum tokens
            temperature (float): Sampling temperature
            max_retries (int): Maximum retry attempts
            
        Returns:
            str: Generated text
        """
        for attempt in range(max_retries):
            try:
                return self.generate_completion(prompt, max_tokens, temperature)
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                continue
        
        raise Exception("Failed after maximum retries")


# Global client instance
_groq_client = None

def get_groq_client() -> GroqClient:
    """Get or create Groq client instance"""
    global _groq_client
    if _groq_client is None:
        _groq_client = GroqClient()
    return _groq_client
