from flask import Blueprint, request, jsonify
from app.services.course_service import CourseService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id

course_bp = Blueprint('course', __name__, url_prefix='/api/courses')

@course_bp.route('', methods=['GET'])
@token_required
def get_courses():
    """
    Get all courses for authenticated user
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: List of courses
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        courses = CourseService.get_user_courses(user_id)
        
        # Get total credit hours
        total_credits = CourseService.get_total_credit_hours(user_id)
        
        return jsonify({
            'courses': courses,
            'total_credit_hours': total_credits,
            'count': len(courses)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@course_bp.route('', methods=['POST'])
@token_required
def create_course():
    """
    Create a new course
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "course_name": "Data Structures",
            "course_code": "CS201" (optional),
            "credit_hours": 3 (optional),
            "instructor": "Dr. Smith" (optional),
            "color": "#FF5733" (optional),
            "schedule": [{"day": "Monday", "start_time": "09:00", "end_time": "10:30"}] (optional)
        }
    
    Returns:
        201: Course created successfully
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
        
        course, error = CourseService.create_course(
            user_id=user_id,
            course_name=data.get('course_name'),
            course_code=data.get('course_code'),
            credit_hours=data.get('credit_hours'),
            instructor=data.get('instructor'),
            color=data.get('color'),
            schedule=data.get('schedule'),
            topics=data.get('topics')
        )
        
        if error:
            return jsonify({
                'error': 'Course Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Course created successfully',
            'course': course
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@course_bp.route('/<int:course_id>', methods=['GET'])
@token_required
def get_course(course_id):
    """
    Get a single course by ID
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Course data
        404: Course not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        course = CourseService.get_course_by_id(course_id, user_id)
        
        if not course:
            return jsonify({
                'error': 'Not Found',
                'message': 'Course not found'
            }), 404
        
        return jsonify({
            'course': course
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@course_bp.route('/<int:course_id>', methods=['PUT'])
@token_required
def update_course(course_id):
    """
    Update course information
    
    Headers:
        Authorization: Bearer <token>
    
    Request Body:
        {
            "course_name": "Updated Name" (optional),
            "course_code": "CS202" (optional),
            "credit_hours": 4 (optional),
            "instructor": "Dr. Johnson" (optional),
            "color": "#00FF00" (optional),
            "schedule": [...] (optional)
        }
    
    Returns:
        200: Course updated successfully
        400: Validation error
        404: Course not found
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
        
        course, error = CourseService.update_course(course_id, user_id, **data)
        
        if error:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Course updated successfully',
            'course': course
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@course_bp.route('/<int:course_id>', methods=['DELETE'])
@token_required
def delete_course(course_id):
    """
    Delete a course
    
    Headers:
        Authorization: Bearer <token>
    
    Returns:
        200: Course deleted successfully
        400: Cannot delete (has active tasks)
        404: Course not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        success, error = CourseService.delete_course(course_id, user_id)
        
        if not success:
            status_code = 404 if 'not found' in error.lower() else 400
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), status_code
        
        return jsonify({
            'message': 'Course deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@course_bp.route('/<int:course_id>/upload-syllabus', methods=['POST'])
@token_required
def upload_syllabus(course_id):
    """
    Upload course syllabus (PDF)
    
    Headers:
        Authorization: Bearer <token>
    
    Form Data:
        file: PDF file (max 10MB)
    
    Returns:
        200: File uploaded successfully
        400: Invalid file
        404: Course not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Verify course exists
        course = CourseService.get_course_by_id(course_id, user_id)
        if not course:
            return jsonify({
                'error': 'Not Found',
                'message': 'Course not found'
            }), 404
        
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({
                'error': 'Bad Request',
                'message': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({
                'error': 'Bad Request',
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            return jsonify({
                'error': 'Bad Request',
                'message': 'Only PDF files are allowed'
            }), 400
        
        # File upload will be implemented with file service
        # For now, return success message
        return jsonify({
            'message': 'Syllabus upload endpoint ready',
            'note': 'File upload functionality will be implemented with AI topic extraction in Phase 5'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
