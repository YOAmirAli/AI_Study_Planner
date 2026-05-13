from flask_jwt_extended import create_access_token, get_jwt_identity, verify_jwt_in_request
from datetime import timedelta

def create_token(user_id: int) -> str:
    """
    Create JWT access token for user
    
    Args:
        user_id (int): User ID to encode in token
        
    Returns:
        str: JWT access token
    """
    # Token expires in 24 hours (configured in config.py)
    # Convert user_id to string as Flask-JWT-Extended requires string identity
    access_token = create_access_token(
        identity=str(user_id),
        expires_delta=timedelta(hours=24)
    )
    return access_token


def verify_token() -> int:
    """
    Verify JWT token and return user_id
    
    Returns:
        int: User ID from token, or None if invalid
    """
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        return int(user_id) if user_id else None
    except Exception:
        return None


def get_current_user_id() -> int:
    """
    Get current authenticated user ID from JWT token
    
    Returns:
        int: User ID from token
    """
    user_id = get_jwt_identity()
    return int(user_id) if user_id else None
