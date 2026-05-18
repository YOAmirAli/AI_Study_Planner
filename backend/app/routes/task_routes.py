from flask import Blueprint, request, jsonify
from app.services.task_service import TaskService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

task_bp = Blueprint('task', __name__, url_prefix='/api/tasks')

@task_bp.route('', methods=['GET'])
@token_required
def get_tasks():
    """
    Get all tasks with optional filters
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        status: Filter by status (pending, in_progress, completed)
        priority: Filter by priority (high, medium, low)
        course_id: Filter by course ID
        sort_by: Sort field (deadline, priority, created_at)
    
    Returns:
        200: List of tasks
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Get query parameters
        status = request.args.get('status')
        priority = request.args.get('priority')
        course_id = request.args.get('course_id', type=int)
        sort_by = request.args.get('sort_by', 'deadline')
        
        tasks = TaskService.get_user_tasks(
            user_id=user_id,
            status=status,
            priority=priority,
            course_id=course_id,
            sort_by=sort_by
        )
        
        # Get statistics
        stats = TaskService.get_task_statistics(user_id)
        
        return jsonify({
            'tasks': tasks,
            'statistics': stats,
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('', methods=['POST'])
@token_required
def create_task():
    """
    Create a new task
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "course_id": 1,
            "title": "Assignment 1",
            "description": "Complete chapter 1-3" (optional),
            "deadline": "2024-12-31T23:59:59",
            "priority": "high" (optional, default: medium),
            "estimated_time": 120 (optional, in minutes)
        }
    
    Returns:
        201: Task created successfully
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
        required_fields = ['course_id', 'title', 'deadline']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'{field} is required'
                }), 400
        
        task, error = TaskService.create_task(
            user_id=user_id,
            course_id=data.get('course_id'),
            title=data.get('title'),
            deadline=data.get('deadline'),
            priority=data.get('priority', 'medium'),
            description=data.get('description'),
            estimated_time=data.get('estimated_time')
        )
        
        if error:
            return jsonify({
                'error': 'Task Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Task created successfully',
            'task': task
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(task_id):
    """
    Get a single task by ID
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Task data
        404: Task not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        task = TaskService.get_task_by_id(task_id, user_id)
        
        if not task:
            return jsonify({
                'error': 'Not Found',
                'message': 'Task not found'
            }), 404
        
        return jsonify({
            'task': task
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/<int:task_id>', methods=['PUT'])
@token_required
def update_task(task_id):
    """
    Update task information
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "title": "Updated Title" (optional),
            "description": "Updated description" (optional),
            "deadline": "2024-12-31T23:59:59" (optional),
            "priority": "high" (optional),
            "status": "in_progress" (optional),
            "estimated_time": 180 (optional),
            "actual_time": 150 (optional)
        }
    
    Returns:
        200: Task updated successfully
        400: Validation error
        404: Task not found
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
        
        # Prevent "multiple values for argument" error by removing positional args from data
        data.pop('task_id', None)
        data.pop('user_id', None)
        
        task, error = TaskService.update_task(task_id, user_id, **data)
        
        if error:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Task updated successfully',
            'task': task
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/<int:task_id>', methods=['DELETE'])
@token_required
def delete_task(task_id):
    """
    Delete a task
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Task deleted successfully
        404: Task not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        success, error = TaskService.delete_task(task_id, user_id)
        
        if not success:
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), 404
        
        return jsonify({
            'message': 'Task deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/<int:task_id>/complete', methods=['PATCH'])
@token_required
def complete_task(task_id):
    """
    Mark task as completed
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body (optional):
        {
            "actual_time": 150 (optional, in minutes)
        }
    
    Returns:
        200: Task completed successfully
        404: Task not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json(silent=True) or {}
        
        task, error = TaskService.complete_task(
            task_id=task_id,
            user_id=user_id,
            actual_time=data.get('actual_time')
        )
        
        if error:
            return jsonify({
                'error': 'Complete Failed',
                'message': error
            }), 404
        
        return jsonify({
            'message': 'Task marked as completed',
            'task': task
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/upcoming', methods=['GET'])
@token_required
def get_upcoming_tasks():
    """
    Get tasks due in the next 7 days
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        days: Number of days to look ahead (default: 7)
    
    Returns:
        200: List of upcoming tasks
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        days = request.args.get('days', 7, type=int)
        
        tasks = TaskService.get_upcoming_tasks(user_id, days)
        
        return jsonify({
            'tasks': tasks,
            'count': len(tasks),
            'days_ahead': days
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@task_bp.route('/overdue', methods=['GET'])
@token_required
def get_overdue_tasks():
    """
    Get overdue tasks
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: List of overdue tasks
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        tasks = TaskService.get_overdue_tasks(user_id)
        
        return jsonify({
            'tasks': tasks,
            'count': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
