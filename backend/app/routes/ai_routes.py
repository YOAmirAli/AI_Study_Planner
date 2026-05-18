from flask import Blueprint, request, jsonify
from app.services.ai_service import AIService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@ai_bp.route('/status', methods=['GET'])
@token_required
def ai_status():
    """Hybrid AI stack health (for demos / debugging)."""
    import os
    from pathlib import Path

    backend_root = Path(__file__).resolve().parents[2]
    model_dir = backend_root / 'models' / 'flashcard_model' / 'final'
    openai_key = os.getenv('OPENAI_API_KEY', '')
    youtube_key = os.getenv('YOUTUBE_API_KEY', '')

    return jsonify({
        'hybrid_ai': {
            'quiz_summary_tutor': 'openai',
            'flashcards': 't5_finetuned_local',
            'video_recommendations': 'youtube_api_or_search',
            'task_suggestions': 'rule_based',
        },
        'openai_configured': bool(openai_key and not openai_key.startswith('your-')),
        'openai_model': os.getenv('OPENAI_MODEL', 'gpt-4o-mini'),
        'youtube_api_configured': bool(youtube_key),
        'flashcard_model_trained': (model_dir / 'config.json').is_file(),
        'flashcard_model_path': str(model_dir),
    }), 200


@ai_bp.route('/summarize', methods=['POST'])
@token_required
def summarize_text():
    """
    Generate summary from text or PDF
    
    Headers:
        Authorization: Bearer <token>
    
    Form Data or JSON:
        text (optional): Direct text input
        file (optional): PDF file upload
        length (optional): 'brief', 'moderate', 'detailed' (default: 'moderate')
    
    Returns:
        200: Summary generated
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Extract file if present
        file = request.files.get('file')
        
        # Support both form data and JSON
        if request.is_json:
            data = request.get_json(silent=True) or {}
            text = data.get('text')
            length = data.get('length', 'moderate')
        else:
            text = request.form.get('text')
            length = request.form.get('length', 'moderate')
            
        if not file and not text:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Text or file is required'
            }), 400
        
        # Validate length
        if length not in ['brief', 'moderate', 'detailed']:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Length must be brief, moderate, or detailed'
            }), 400
        
        # Generate summary
        result, error = AIService.generate_summary(text, file, length)
        
        if error:
            return jsonify({
                'error': 'Summary Generation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Summary generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@ai_bp.route('/generate-quiz', methods=['POST'])
@token_required
def generate_quiz():
    """
    Generate quiz from text or PDF
    
    Headers:
        Authorization: Bearer <token>
    
    Form Data or JSON:
        text (optional): Direct text input
        file (optional): PDF file upload
        num_questions (optional): Number of questions (5-50, default: 10)
        question_type (optional): 'mcq', 'short_answer', 'mixed' (default: 'mixed')
    
    Returns:
        200: Quiz generated
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Extract file if present
        file = request.files.get('file')
        
        # Support both form data and JSON
        if request.is_json:
            data = request.get_json(silent=True) or {}
            text = data.get('text')
            num_questions = data.get('num_questions', 10)
            question_type = data.get('question_type', 'mixed')
        else:
            text = request.form.get('text')
            num_questions = request.form.get('num_questions', 10)
            question_type = request.form.get('question_type', 'mixed')
            
        if num_questions is not None:
            num_questions = int(num_questions)
            
        if not file and not text:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Text or file is required'
            }), 400
        
        # Validate inputs
        if question_type not in ['mcq', 'short_answer', 'mixed']:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Question type must be mcq, short_answer, or mixed'
            }), 400
        
        # Generate quiz
        result, error = AIService.generate_quiz(text, file, num_questions, question_type)
        
        if error:
            return jsonify({
                'error': 'Quiz Generation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Quiz generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@ai_bp.route('/create-flashcards', methods=['POST'])
@token_required
def create_flashcards():
    """
    Generate flashcards from text or PDF
    
    Headers:
        Authorization: Bearer <token>
    
    Form Data or JSON:
        text (optional): Direct text input
        file (optional): PDF file upload
        num_cards (optional): Number of flashcards (5-30, default: 20)
    
    Returns:
        200: Flashcards generated
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Extract file if present
        file = request.files.get('file')
        
        # Support both form data and JSON
        if request.is_json:
            data = request.get_json(silent=True) or {}
            text = data.get('text')
            num_cards = data.get('num_cards', 20)
        else:
            text = request.form.get('text')
            num_cards = request.form.get('num_cards', 20)
            
        if num_cards is not None:
            num_cards = int(num_cards)
            
        if not file and not text:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Text or file is required'
            }), 400
        
        # Generate flashcards
        result, error = AIService.generate_flashcards(text, file, num_cards)
        
        if error:
            return jsonify({
                'error': 'Flashcard Generation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Flashcards generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@ai_bp.route('/recommend-materials', methods=['POST'])
@token_required
def recommend_materials():
    """
    Recommend study materials for a topic
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "topic": "Machine Learning"
        }
    
    Returns:
        200: Recommendations generated
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        data = request.get_json()
        
        if not data or 'topic' not in data:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Topic is required'
            }), 400
        
        topic = data['topic']
        
        # Get recommendations
        result, error = AIService.recommend_materials(topic)
        
        if error:
            return jsonify({
                'error': 'Recommendation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Recommendations generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@ai_bp.route('/task-tutor', methods=['POST'])
@token_required
def task_tutor():
    """
    Get AI tutoring for a specific task
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "task_title": "Task title",
            "task_description": "Task description"
        }
    
    Returns:
        200: Learning guidance generated
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
        
        task_title = data.get('task_title')
        task_description = data.get('task_description')
        
        if not task_title or not task_description:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Task title and description are required'
            }), 400
        
        # Generate learning guidance
        result, error = AIService.get_task_tutoring(task_title, task_description)
        
        if error:
            return jsonify({
                'error': 'Task Tutoring Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Learning guidance generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@ai_bp.route('/suggest-tasks', methods=['POST'])
@token_required
def suggest_tasks():
    """
    Suggest tasks based on course description
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "course_name": "Data Structures",
            "description": "Course description...",
            "num_tasks": 5 (optional, default: 5)
        }
    
    Returns:
        200: Task suggestions generated
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
        
        course_name = data.get('course_name')
        description = data.get('description')
        num_tasks = data.get('num_tasks', 5)
        
        if not course_name or not description:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Course name and description are required'
            }), 400
        
        if len(description.strip()) < 50:
            return jsonify({
                'error': 'Validation Error',
                'message': 'Description must be at least 50 characters'
            }), 400
        
        # Generate task suggestions
        result, error = AIService.suggest_course_tasks(course_name, description, num_tasks)
        
        if error:
            return jsonify({
                'error': 'Task Suggestion Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Task suggestions generated successfully',
            **result
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
