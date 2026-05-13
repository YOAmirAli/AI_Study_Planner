from flask import Blueprint, request, jsonify
from app.services.schedule_service import ScheduleService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

schedule_bp = Blueprint('schedule', __name__, url_prefix='/api/schedules')

@schedule_bp.route('', methods=['GET'])
@token_required
def get_schedule():
    """
    Get weekly schedule
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        week_start (optional): Start date of week (YYYY-MM-DD)
    
    Returns:
        200: Weekly schedule
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        week_start = request.args.get('week_start')
        
        schedule = ScheduleService.get_weekly_schedule(user_id, week_start)
        
        return jsonify(schedule), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@schedule_bp.route('/generate', methods=['POST'])
@token_required
def generate_schedule():
    """
    Generate AI-optimized study schedule
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "week_start": "2025-11-25" (optional),
            "study_hours_per_day": 4 (optional, default: 4),
            "course_id": 1 (optional, filter by specific course)
        }
    
    Returns:
        201: Schedule generated successfully
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json() or {}
        
        week_start = data.get('week_start')
        study_hours_per_day = data.get('study_hours_per_day', 4)
        course_id = data.get('course_id')
        
        # Validate study hours
        if not isinstance(study_hours_per_day, int) or study_hours_per_day < 1 or study_hours_per_day > 12:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Study hours per day must be between 1 and 12'
            }), 400
        
        result, error = ScheduleService.generate_ai_schedule(
            user_id, week_start, study_hours_per_day, course_id
        )
        
        if error:
            return jsonify({
                'error': 'Schedule Generation Failed',
                'message': error
            }), 400
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@schedule_bp.route('', methods=['POST'])
@token_required
def create_schedule_block():
    """
    Create manual schedule block
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "date": "2025-11-25",
            "start_time": "09:00",
            "end_time": "11:00",
            "block_type": "study",
            "title": "Study Session",
            "task_id": 1 (optional)
        }
    
    Returns:
        201: Schedule block created
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
        required_fields = ['date', 'start_time', 'end_time', 'block_type']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': f'{field} is required'
                }), 400
        
        block, error = ScheduleService.create_schedule_block(
            user_id=user_id,
            schedule_date=data['date'],
            start_time=data['start_time'],
            end_time=data['end_time'],
            block_type=data['block_type'],
            title=data.get('title'),
            task_id=data.get('task_id'),
            color=data.get('color')
        )
        
        if error:
            return jsonify({
                'error': 'Schedule Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Schedule block created successfully',
            'schedule': block
        }), 201
        
    except Exception as e:
        import traceback
        print('=== SCHEDULE CREATE ERROR ===')
        print(f'Error: {str(e)}')
        print(f'Traceback: {traceback.format_exc()}')
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@schedule_bp.route('/<int:schedule_id>', methods=['PUT'])
@token_required
def update_schedule_block(schedule_id):
    """
    Update schedule block
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "date": "2025-11-26" (optional),
            "start_time": "10:00" (optional),
            "end_time": "12:00" (optional),
            "title": "Updated Title" (optional),
            "block_type": "study" (optional)
        }
    
    Returns:
        200: Schedule block updated
        400: Validation error
        401: Unauthorized
        404: Schedule block not found
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Request body is required'
            }), 400
        
        block, error = ScheduleService.update_schedule_block(
            schedule_id, user_id, **data
        )
        
        if error:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Schedule block updated successfully',
            'schedule': block
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@schedule_bp.route('/<int:schedule_id>', methods=['DELETE'])
@token_required
def delete_schedule_block(schedule_id):
    """
    Delete schedule block
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Schedule block deleted
        401: Unauthorized
        404: Schedule block not found
    """
    try:
        user_id = get_current_user_id()
        
        success, error = ScheduleService.delete_schedule_block(schedule_id, user_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Schedule block deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@schedule_bp.route('/week/<string:week_date>', methods=['GET'])
@token_required
def get_week_schedule(week_date):
    """
    Get schedule for specific week
    
    Headers:
        Authorization: Bearer <token>
    
    Parameters:
        week_date: Date in YYYY-MM-DD format
    
    Returns:
        200: Weekly schedule
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        schedule = ScheduleService.get_weekly_schedule(user_id, week_date)
        
        return jsonify(schedule), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
