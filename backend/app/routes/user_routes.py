from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """
    Get user profile
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: User profile data
        401: Unauthorized
        404: User not found
    """
    try:
        user_id = get_current_user_id()
        user = UserService.get_user_profile(user_id)
        
        if not user:
            return jsonify({
                'error': 'Not Found',
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@user_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """
    Update user profile
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "name": "John Doe" (optional),
            "university": "ABC University" (optional),
            "program": "Computer Science" (optional),
            "profile_picture": "https://..." (optional)
        }
    
    Returns:
        200: Profile updated successfully
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        # Update profile
        user, error = UserService.update_user_profile(
            user_id=user_id,
            name=data.get('name'),
            university=data.get('university'),
            program=data.get('program'),
            profile_picture=data.get('profile_picture')
        )
        
        if error:
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@user_bp.route('/password', methods=['PUT'])
@token_required
def change_password():
    """
    Change user password
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "current_password": "OldPassword123",
            "new_password": "NewPassword123"
        }
    
    Returns:
        200: Password changed successfully
        400: Validation error
        401: Current password incorrect
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Current password and new password are required'
            }), 400
        
        # Change password
        success, error = UserService.change_password(
            user_id=user_id,
            current_password=current_password,
            new_password=new_password
        )
        
        if not success:
            status_code = 401 if 'incorrect' in error else 400
            return jsonify({
                'error': 'Password Change Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Password changed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
