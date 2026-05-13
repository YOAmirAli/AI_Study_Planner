# OpenAI wrapper
"""
OpenAI API Client
Wrapper for OpenAI API for AI operations
"""

import os
from openai import OpenAI

class OpenAIClient:
    """OpenAI API client for AI operations"""
    
    def __init__(self):
        """Initialize OpenAI client"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4-turbo-preview')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=self.api_key)
    
    def generate_completion(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """
        Generate text completion using OpenAI API
        
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
            raise Exception(f"OpenAI API error: {str(e)}")
    
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
_openai_client = None

def get_openai_client() -> OpenAIClient:
    """Get or create OpenAI client instance"""
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAIClient()
    return _openai_client