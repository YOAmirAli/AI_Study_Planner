import re

def validate_email(email: str) -> bool:
    """
    Validate email format using regex
    
    Args:
        email (str): Email address to validate
        
    Returns:
        bool: True if valid email format, False otherwise
    """
    if not email:
        return False
    
    # Email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one number
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, "Password is strong"


def validate_name(name: str) -> tuple[bool, str]:
    """
    Validate user name
    
    Args:
        name (str): Name to validate
        
    Returns:
        tuple: (is_valid: bool, message: str)
    """
    if not name or not name.strip():
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    if len(name) > 255:
        return False, "Name must not exceed 255 characters"
    
    return True, "Name is valid"
