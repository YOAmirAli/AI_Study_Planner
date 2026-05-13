"""
Quiz Routes
API endpoints for quiz management
"""

from flask import Blueprint, request, jsonify
from app.services.quiz_service import QuizService
from app.ai.quiz_generator_task import TaskQuizGenerator
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id
from app.models.task import Task

quiz_bp = Blueprint('quizzes', __name__, url_prefix='/api/quizzes')

@quiz_bp.route('/generate', methods=['POST'])
@token_required
def generate_quiz():
    """
    Generate a quiz from a completed task
    
    Request Body:
        {
            "task_id": 1,
            "num_questions": 10
        }
    
    Returns:
        201: Quiz created
        400: Validation error
        404: Task not found
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        task_id = data.get('task_id')
        num_questions = data.get('num_questions', 10)
        
        if not task_id:
            return jsonify({'error': 'Task ID is required'}), 400
        
        # Get task
        task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Generate quiz using AI
        quiz_data = TaskQuizGenerator.generate_quiz(
            task.title,
            task.description or task.title,
            num_questions
        )
        
        # Create quiz in database
        quiz, error = QuizService.create_quiz(
            user_id=user_id,
            task_id=task_id,
            course_id=task.course_id,
            title=f"Quiz: {task.title}",
            questions_data=quiz_data['questions'],
            description=f"Test your knowledge on {task.title}"
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Quiz generated successfully',
            'quiz': quiz
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('', methods=['GET'])
@token_required
def get_quizzes():
    """Get all quizzes for current user"""
    try:
        user_id = get_current_user_id()
        status = request.args.get('status')
        
        quizzes = QuizService.get_user_quizzes(user_id, status)
        
        return jsonify({
            'quizzes': quizzes,
            'total': len(quizzes)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
@token_required
def get_quiz(quiz_id):
    """Get a single quiz"""
    try:
        user_id = get_current_user_id()
        quiz = QuizService.get_quiz_by_id(quiz_id, user_id)
        
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        return jsonify({'quiz': quiz}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/<int:quiz_id>/start', methods=['POST'])
@token_required
def start_quiz(quiz_id):
    """Start a quiz"""
    try:
        user_id = get_current_user_id()
        quiz, error = QuizService.start_quiz(quiz_id, user_id)
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Quiz started',
            'quiz': quiz
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@token_required
def submit_quiz(quiz_id):
    """
    Submit quiz answers
    
    Request Body:
        {
            "answers": {"1": "A", "2": "B", ...},
            "time_taken": 300
        }
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        answers = data.get('answers', {})
        time_taken = data.get('time_taken')
        
        result, error = QuizService.submit_quiz(quiz_id, user_id, answers, time_taken)
        
        if error:
            return jsonify({'error': error}), 400
        
        # Get updated quiz with results
        quiz = QuizService.get_quiz_by_id(quiz_id, user_id, include_answers=True)
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'result': result,
            'quiz': quiz
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/pending-count', methods=['GET'])
@token_required
def get_pending_count():
    """Get count of pending quizzes"""
    try:
        user_id = get_current_user_id()
        count = QuizService.get_pending_count(user_id)
        
        return jsonify({'count': count}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
@token_required
def delete_quiz(quiz_id):
    """Delete a quiz"""
    try:
        user_id = get_current_user_id()
        success, error = QuizService.delete_quiz(quiz_id, user_id)
        
        if not success:
            return jsonify({'error': error}), 400
        
        return jsonify({'message': 'Quiz deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
