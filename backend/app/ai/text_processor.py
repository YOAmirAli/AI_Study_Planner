"""
Text Processor
Extract and process text from various sources
"""

import PyPDF2
from io import BytesIO

class TextProcessor:
    """Process text from different sources"""
    
    @staticmethod
    def extract_from_pdf(pdf_file) -> str:
        """
        Extract text from PDF file
        
        Args:
            pdf_file: File object or bytes
            
        Returns:
            str: Extracted text
        """
        try:
            # Handle both file objects and bytes
            if isinstance(pdf_file, bytes):
                pdf_file = BytesIO(pdf_file)
            
            # Create PDF reader
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def clean_text(text: str, max_length: int = 50000) -> str:
        """
        Clean and truncate text
        
        Args:
            text (str): Input text
            max_length (int): Maximum length
            
        Returns:
            str: Cleaned text
        """
        # Remove extra whitespace
        text = " ".join(text.split())
        
        # Truncate if too long
        if len(text) > max_length:
            text = text[:max_length] + "..."
        
        return text
    
    @staticmethod
    def validate_text(text: str, min_length: int = 100) -> bool:
        """
        Validate text length
        
        Args:
            text (str): Input text
            min_length (int): Minimum required length
            
        Returns:
            bool: True if valid
        """
        return len(text.strip()) >= min_length
