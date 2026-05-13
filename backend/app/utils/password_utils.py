import bcrypt

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with 12 salt rounds
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash
    
    Args:
        password (str): Plain text password to verify
        hashed_password (str): Hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False
