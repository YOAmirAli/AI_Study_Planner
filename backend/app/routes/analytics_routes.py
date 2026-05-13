from flask import Blueprint, request, jsonify
from app.services.analytics_service import AnalyticsService
from app.services.prediction_service import PredictionService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/progress')

@analytics_bp.route('/dashboard', methods=['GET'])
@token_required
def get_dashboard():
    """
    Get dashboard statistics
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Dashboard stats
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        stats = AnalyticsService.get_dashboard_stats(user_id)
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@analytics_bp.route('/analytics', methods=['GET'])
@token_required
def get_analytics():
    """
    Get detailed analytics with chart data
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Detailed analytics
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        analytics = AnalyticsService.get_detailed_analytics(user_id)
        
        return jsonify(analytics), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@analytics_bp.route('/session', methods=['POST'])
@token_required
def log_session():
    """
    Log a study session
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "course_id": 1 (optional),
            "task_id": 1 (optional),
            "session_date": "2025-11-25" (optional, defaults to today),
            "hours_spent": 2.5,
            "notes": "Studied algorithms" (optional)
        }
    
    Returns:
        201: Session logged
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
        
        # Validate hours_spent
        if 'hours_spent' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'hours_spent is required'
            }), 400
        
        # Log session
        session, error = AnalyticsService.log_study_session(
            user_id=user_id,
            course_id=data.get('course_id'),
            task_id=data.get('task_id'),
            session_date=data.get('session_date'),
            hours_spent=data.get('hours_spent'),
            notes=data.get('notes')
        )
        
        if error:
            return jsonify({
                'error': 'Session Logging Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Study session logged successfully',
            'session': session
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@analytics_bp.route('/sessions', methods=['GET'])
@token_required
def get_sessions():
    """
    Get study session history
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        limit (optional): Maximum number of sessions (default: 50)
    
    Returns:
        200: Session history
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        limit = request.args.get('limit', 50, type=int)
        
        sessions = AnalyticsService.get_study_sessions(user_id, limit)
        
        return jsonify({
            'sessions': sessions,
            'count': len(sessions)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@analytics_bp.route('/prediction', methods=['GET'])
@token_required
def get_prediction():
    """
    Get falling behind prediction
    
    Headers:
        Authorization: Bearer <token>
    
    Query Parameters:
        expected_hours (optional): Expected hours per week (default: 20)
    
    Returns:
        200: Prediction result
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        expected_hours = request.args.get('expected_hours', 20, type=int)
        
        prediction = PredictionService.detect_falling_behind(user_id, expected_hours)
        
        return jsonify(prediction), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@analytics_bp.route('/weekly-summary', methods=['GET'])
@token_required
def get_weekly_summary():
    """
    Get current week summary
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Weekly summary
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        summary = AnalyticsService.get_weekly_summary(user_id)
        
        return jsonify(summary), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
