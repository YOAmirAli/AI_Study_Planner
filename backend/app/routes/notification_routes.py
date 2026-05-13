from flask import Blueprint, request, jsonify
from app.services.notification_service import NotificationService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

notification_bp = Blueprint('notification', __name__, url_prefix='/api/notifications')

@notification_bp.route('', methods=['GET'])
@token_required
def get_notifications():
    """
    Get user notifications
    Headers:
        Authorization: Bearer <token>
    Query Parameters:
        unread_only (optional): true/false - Only return unread notifications
        limit (optional): Maximum number of notifications (default: 50)
    Returns:
        200: List of notifications
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = request.args.get('limit', 50, type=int)
        
        notifications = NotificationService.get_user_notifications(
            user_id, unread_only, limit
        )
        
        unread_count = len([n for n in notifications if not n['is_read']])
        
        return jsonify({
            'notifications': notifications,
            'count': len(notifications),
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@notification_bp.route('/<int:notification_id>/read', methods=['PATCH'])
@token_required
def mark_notification_read(notification_id):
    """
    Mark notification as read
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Notification marked as read
        401: Unauthorized
        404: Notification not found
    """
    try:
        user_id = get_current_user_id()
        success, error = NotificationService.mark_notification_read(
            notification_id, user_id
        )
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Mark Read Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Notification marked as read'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@notification_bp.route('/mark-all-read', methods=['PATCH'])
@token_required
def mark_all_read():
    """
    Mark all notifications as read
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: All notifications marked as read
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        count, error = NotificationService.mark_all_read(user_id)
        
        if error:
            return jsonify({
                'error': 'Mark All Read Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': f'{count} notifications marked as read',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@notification_bp.route('/<int:notification_id>', methods=['DELETE'])
@token_required
def delete_notification(notification_id):
    """
    Delete a notification
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: Notification deleted
        401: Unauthorized
        404: Notification not found
    """
    try:
        user_id = get_current_user_id()
        success, error = NotificationService.delete_notification(
            notification_id, user_id
        )
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Notification deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@notification_bp.route('/clear-all', methods=['DELETE'])
@token_required
def clear_all_read():
    """
    Clear all read notifications
    Headers:
        Authorization: Bearer <token>
    Returns:
        200: All read notifications cleared
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        count, error = NotificationService.clear_all_read(user_id)
        
        if error:
            return jsonify({
                'error': 'Clear Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': f'{count} notifications cleared',
            'count': count
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500

@notification_bp.route('', methods=['POST'])
@token_required
def create_notification():
    """
    Create a custom notification (for testing or manual notifications)
    Headers:
        Authorization: Bearer <token>
    Request Body:
        {
            "type": "group_activity",
            "title": "New Message",
            "message": "You have a new message in Study Group",
            "task_id": 1 (optional),
            "group_id": 1 (optional)
        }
    Returns:
        201: Notification created
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
        required_fields = ['type', 'title', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'{field} is required'
                }), 400
        
        # Create notification
        notification, error = NotificationService.create_notification(
            user_id=user_id,
            notification_type=data['type'],
            title=data['title'],
            message=data['message'],
            task_id=data.get('task_id'),
            group_id=data.get('group_id')
        )
        
        if error:
            return jsonify({
                'error': 'Notification Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Notification created successfully',
            'notification': notification
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
