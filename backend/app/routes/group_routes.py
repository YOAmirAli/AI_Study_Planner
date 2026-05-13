from flask import Blueprint, request, jsonify
from app.services.group_service import GroupService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

group_bp = Blueprint('group', __name__, url_prefix='/api/groups')

@group_bp.route('', methods=['GET'])
@token_required
def get_user_groups():
    """
    Get all groups user is member of
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: List of user's groups
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        groups = GroupService.get_user_groups(user_id)
        
        return jsonify({
            'groups': groups,
            'count': len(groups)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('', methods=['POST'])
@token_required
def create_group():
    """
    Create a new study group
    Headers:
        Authorization: Bearer <token>
    Request Body:
        {
            "group_name": "Data Structures Study Group",
            "description": "Group for studying data structures and algorithms",
            "is_private": false,
            "max_members": 20
        }
    Returns:
        201: Group created
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
        
        # Validate required fields
        if 'group_name' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'group_name is required'
            }), 400
        
        # Create group
        group, error = GroupService.create_group(
            admin_user_id=user_id,
            group_name=data['group_name'],
            description=data.get('description'),
            is_private=data.get('is_private', False),
            max_members=data.get('max_members', 50)
        )
        
        if error:
            return jsonify({
                'error': 'Group Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Group created successfully',
            'group': group
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/<int:group_id>', methods=['GET'])
@token_required
def get_group_details(group_id):
    """
    Get group details with members
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Group details
        401: Unauthorized
        403: Not a member
        404: Group not found
    """
    try:
        user_id = get_current_user_id()
        group, error = GroupService.get_group_details(group_id, user_id)
        
        if error:
            if 'not found' in error.lower():
                status_code = 404
            elif 'not a member' in error.lower():
                status_code = 403
            else:
                status_code = 400
            
            return jsonify({
                'error': 'Access Denied',
                'message': error
            }), status_code
        
        return jsonify({
            'group': group
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/<int:group_id>/join', methods=['POST'])
@token_required
def join_group(group_id):
    """
    Join a group by group ID
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Successfully joined group
        400: Cannot join group
        401: Unauthorized
        404: Group not found
    """
    try:
        user_id = get_current_user_id()
        success, error = GroupService.join_group(group_id, user_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Join Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Successfully joined the group'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/join', methods=['POST'])
@token_required
def join_group_by_code():
    """
    Join a group using join code
    Headers:
        Authorization: Bearer <token>
    Request Body:
        {
            "join_code": "ABC123"
        }
    Returns:
        200: Successfully joined group
        400: Invalid code or cannot join
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data or 'join_code' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'join_code is required'
            }), 400
        
        join_code = data['join_code'].strip().upper()
        
        if len(join_code) != 6:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Join code must be 6 characters'
            }), 400
        
        group, error = GroupService.join_group_by_code(join_code, user_id)
        
        if error:
            return jsonify({
                'error': 'Join Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Successfully joined the group',
            'group': group
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/<int:group_id>/leave', methods=['POST'])
@token_required
def leave_group(group_id):
    """
    Leave a group
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Successfully left group
        400: Cannot leave group
        401: Unauthorized
        404: Group not found
    """
    try:
        user_id = get_current_user_id()
        success, error = GroupService.leave_group(group_id, user_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Leave Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Successfully left the group'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/<int:group_id>', methods=['PUT'])
@token_required
def update_group(group_id):
    """
    Update group information (admin only)
    Headers:
        Authorization: Bearer <token>
    Request Body:
        {
            "group_name": "Updated Group Name",
            "description": "Updated description",
            "is_private": true,
            "max_members": 30
        }
    Returns:
        200: Group updated
        400: Validation error
        401: Unauthorized
        403: Not admin
        404: Group not found
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        group, error = GroupService.update_group(group_id, user_id, **data)
        
        if error:
            if 'not found' in error.lower():
                status_code = 404
            elif 'admin' in error.lower():
                status_code = 403
            else:
                status_code = 400
            
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Group updated successfully',
            'group': group
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@group_bp.route('/<int:group_id>', methods=['DELETE'])
@token_required
def delete_group(group_id):
    """
    Delete a group (admin only)
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Group deleted
        401: Unauthorized
        403: Not admin
        404: Group not found
    """
    try:
        user_id = get_current_user_id()
        success, error = GroupService.delete_group(group_id, user_id)
        
        if not success:
            if 'not found' in error.lower():
                status_code = 404
            elif 'admin' in error.lower():
                status_code = 403
            else:
                status_code = 400
            
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Group deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
