from flask import Blueprint, request, jsonify
from app.services.auth_service import AuthService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "Password123",
            "name": "John Doe",
            "university": "ABC University" (optional),
            "program": "Computer Science" (optional)
        }
    
    Returns:
        201: User created successfully with token
        400: Validation error
        409: Email already exists
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        university = data.get('university')
        program = data.get('program')
        
        # Check required fields
        if not email or not password or not name:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Email, password, and name are required'
            }), 400
        
        # Register user
        user, token, error = AuthService.register_user(
            email=email,
            password=password,
            name=name,
            university=university,
            program=program
        )
        
        if error:
            status_code = 409 if 'already registered' in error else 400
            return jsonify({
                'error': 'Registration Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'User registered successfully',
            'user': user,
            'token': token
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and get JWT token
    
    Request Body:
        {
            "email": "user@example.com",
            "password": "Password123"
        }
    
    Returns:
        200: Login successful with token
        400: Validation error
        401: Invalid credentials
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Email and password are required'
            }), 400
        
        # Authenticate user
        user, token, error = AuthService.login_user(email, password)
        
        if error:
            return jsonify({
                'error': 'Authentication Failed',
                'message': error
            }), 401
        
        return jsonify({
            'message': 'Login successful',
            'user': user,
            'token': token
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@auth_bp.route('/me', methods=['GET'])
@token_required
def get_current_user():
    """
    Get current authenticated user information
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: User information
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        user = AuthService.get_user_by_id(user_id)
        
        if not user:
            return jsonify({
                'error': 'Not Found',
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """
    Logout user (client-side token removal)
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Logout successful
    """
    # Note: JWT tokens are stateless, so logout is handled client-side
    # by removing the token from storage
    return jsonify({
        'message': 'Logout successful'
    }), 200
