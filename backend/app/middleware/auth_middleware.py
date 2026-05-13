from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def token_required(f):
    """
    Decorator to protect routes with JWT authentication
    
    Usage:
        @token_required
        def protected_route():
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            # Verify JWT token is present and valid
            verify_jwt_in_request()
            
            # Get user_id from token (convert to int as it's stored as string)
            user_id_str = get_jwt_identity()
            user_id = int(user_id_str) if user_id_str else None
            
            if not user_id:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid token identity'
                }), 401
            
            # Verify user exists in database
            user = User.query.get(user_id)
            if not user:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'User not found'
                }), 401
            
            # Continue to protected route
            return f(*args, **kwargs)
            
        except Exception as e:
            # Log the actual error for debugging
            print(f"Auth error: {type(e).__name__}: {str(e)}")
            return jsonify({
                'error': 'Unauthorized',
                'message': f'Invalid or expired token: {str(e)}'
            }), 401
    
    return decorated
