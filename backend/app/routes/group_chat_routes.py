"""
Group Chat and Enhanced Features Routes
Handles messaging, resources, and leaderboard
"""

from flask import Blueprint, request, jsonify
from app.services.group_chat_service import GroupChatService
from app.services.group_service import GroupService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id
from app.models.group_resource import GroupResource
from app.models.group_member import GroupMember
from app.models.quiz import QuizResult, Quiz
from app.models.task import Task
from app.models.user import User
from app.config.database import db
from sqlalchemy import func

group_chat_bp = Blueprint('group_chat', __name__)

# ============= MESSAGING ROUTES =============

@group_chat_bp.route('/api/groups/<int:group_id>/messages', methods=['POST'])
@token_required
def send_message(group_id):
    """Send a message to group chat"""
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data or 'message_text' not in data:
            return jsonify({'error': 'message_text is required'}), 400
        
        message, error = GroupChatService.send_message(
            group_id=group_id,
            user_id=user_id,
            message_text=data['message_text'],
            message_type=data.get('message_type', 'text')
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': message}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/messages', methods=['GET'])
@token_required
def get_messages(group_id):
    """Get group chat messages"""
    try:
        user_id = get_current_user_id()
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        messages, error = GroupChatService.get_group_messages(
            group_id=group_id,
            user_id=user_id,
            limit=limit,
            offset=offset
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        # Auto-mark messages as read when fetched
        from app.models.group_message_read import GroupMessageRead
        GroupMessageRead.mark_all_as_read(group_id, user_id)
        
        return jsonify({'messages': messages, 'count': len(messages)}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/messages/mark-read', methods=['POST'])
@token_required
def mark_messages_read(group_id):
    """Mark all messages in a group as read"""
    try:
        user_id = get_current_user_id()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        from app.models.group_message_read import GroupMessageRead
        success = GroupMessageRead.mark_all_as_read(group_id, user_id)
        
        if success:
            return jsonify({'message': 'All messages marked as read'}), 200
        else:
            return jsonify({'error': 'Failed to mark messages as read'}), 500
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/messages/unread-count', methods=['GET'])
@token_required
def get_unread_count(group_id):
    """Get unread message count for a group"""
    try:
        user_id = get_current_user_id()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        from app.models.group_message_read import GroupMessageRead
        unread_count = GroupMessageRead.get_unread_count(group_id, user_id)
        
        return jsonify({'unread_count': unread_count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/messages/<int:message_id>', methods=['DELETE'])
@token_required
def delete_message(group_id, message_id):
    """Delete a message"""
    try:
        user_id = get_current_user_id()
        success, error = GroupChatService.delete_message(message_id, user_id)
        
        if not success:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Message deleted'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= RESOURCES ROUTES =============

@group_chat_bp.route('/api/groups/<int:group_id>/resources', methods=['POST'])
@token_required
def share_resource(group_id):
    """Share a resource in the group"""
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        # Validate required fields
        if not data or 'title' not in data or 'resource_type' not in data:
            return jsonify({'error': 'title and resource_type are required'}), 400
        
        # Create resource
        resource = GroupResource(
            group_id=group_id,
            shared_by_user_id=user_id,
            title=data['title'],
            description=data.get('description'),
            resource_type=data['resource_type'],
            resource_url=data.get('resource_url'),
            content=data.get('content'),
            tags=','.join(data.get('tags', [])) if isinstance(data.get('tags'), list) else data.get('tags')
        )
        
        db.session.add(resource)
        db.session.commit()
        
        return jsonify({
            'message': 'Resource shared successfully',
            'resource': resource.to_dict(include_user=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/resources', methods=['GET'])
@token_required
def get_resources(group_id):
    """Get group resources"""
    try:
        user_id = get_current_user_id()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        resources = GroupResource.query.filter_by(group_id=group_id).order_by(
            GroupResource.created_at.desc()
        ).all()
        
        return jsonify({
            'resources': [r.to_dict(include_user=True) for r in resources],
            'count': len(resources)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@group_chat_bp.route('/api/groups/<int:group_id>/resources/<int:resource_id>', methods=['DELETE'])
@token_required
def delete_resource(group_id, resource_id):
    """Delete a resource"""
    try:
        user_id = get_current_user_id()
        
        resource = GroupResource.query.get(resource_id)
        if not resource or resource.group_id != group_id:
            return jsonify({'error': 'Resource not found'}), 404
        
        # Check if user is owner or admin
        from app.models.group import Group
        group = Group.query.get(group_id)
        
        if resource.shared_by_user_id != user_id and not group.is_admin(user_id):
            return jsonify({'error': 'You can only delete your own resources'}), 403
        
        db.session.delete(resource)
        db.session.commit()
        
        return jsonify({'message': 'Resource deleted'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============= LEADERBOARD ROUTE =============

@group_chat_bp.route('/api/groups/<int:group_id>/leaderboard', methods=['GET'])
@token_required
def get_leaderboard(group_id):
    """Get group leaderboard"""
    try:
        user_id = get_current_user_id()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        # Get all group members
        members = GroupMember.query.filter_by(group_id=group_id).all()
        
        leaderboard = []
        for member in members:
            user = User.query.get(member.user_id)
            if not user:
                continue
            
            # Get user stats
            tasks_completed = Task.query.filter_by(
                user_id=member.user_id,
                status='completed'
            ).count()
            
            # Get quiz stats
            quiz_results = db.session.query(
                func.avg(QuizResult.percentage).label('avg_score'),
                func.count(QuizResult.result_id).label('quiz_count')
            ).join(Quiz, Quiz.quiz_id == QuizResult.quiz_id).filter(
                Quiz.user_id == member.user_id
            ).first()
            
            avg_quiz_score = float(quiz_results.avg_score) if quiz_results.avg_score else 0
            quiz_count = quiz_results.quiz_count or 0
            
            # Calculate points (simple scoring system)
            points = (tasks_completed * 10) + (quiz_count * 5) + int(avg_quiz_score)
            
            leaderboard.append({
                'user_id': user.user_id,
                'name': user.name,
                'email': user.email,
                'role': member.role,
                'tasks_completed': tasks_completed,
                'quizzes_taken': quiz_count,
                'avg_quiz_score': round(avg_quiz_score, 2),
                'points': points,
                'joined_at': member.joined_at.isoformat() if member.joined_at else None
            })
        
        # Sort by points
        leaderboard.sort(key=lambda x: x['points'], reverse=True)
        
        # Add rank
        for i, member in enumerate(leaderboard):
            member['rank'] = i + 1
        
        return jsonify({
            'leaderboard': leaderboard,
            'count': len(leaderboard)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============= ACTIVITY FEED ROUTE =============

@group_chat_bp.route('/api/groups/<int:group_id>/activity', methods=['GET'])
@token_required
def get_activity(group_id):
    """Get recent group activity"""
    try:
        user_id = get_current_user_id()
        
        # Check if user is member
        if not GroupMember.is_member(group_id, user_id):
            return jsonify({'error': 'You are not a member of this group'}), 403
        
        # Get group members
        member_ids = [m.user_id for m in GroupMember.query.filter_by(group_id=group_id).all()]
        
        activities = []
        
        # Recent tasks completed
        recent_tasks = Task.query.filter(
            Task.user_id.in_(member_ids),
            Task.status == 'completed'
        ).order_by(Task.completed_at.desc()).limit(10).all()
        
        for task in recent_tasks:
            user = User.query.get(task.user_id)
            if user:
                activities.append({
                    'type': 'task_completed',
                    'user_name': user.name,
                    'description': f'completed task "{task.title}"',
                    'timestamp': task.completed_at.isoformat() if task.completed_at else None
                })
        
        # Recent quizzes
        recent_quizzes = db.session.query(Quiz, QuizResult, User).join(
            QuizResult, QuizResult.quiz_id == Quiz.quiz_id
        ).join(User, User.user_id == Quiz.user_id).filter(
            Quiz.user_id.in_(member_ids)
        ).order_by(QuizResult.completed_at.desc()).limit(10).all()
        
        for quiz, result, user in recent_quizzes:
            activities.append({
                'type': 'quiz_completed',
                'user_name': user.name,
                'description': f'scored {result.percentage}% on "{quiz.title}"',
                'timestamp': result.completed_at.isoformat() if result.completed_at else None
            })
        
        # Sort by timestamp
        activities.sort(key=lambda x: x['timestamp'] or '', reverse=True)
        
        return jsonify({
            'activities': activities[:20],  # Return top 20
            'count': len(activities[:20])
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
