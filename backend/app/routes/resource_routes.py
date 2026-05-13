"""
Resource Routes
API endpoints for managing learning resources
"""

from flask import Blueprint, request, jsonify
from app.services.resource_service import ResourceService
from app.middleware.auth_middleware import token_required
from app.utils.jwt_utils import get_current_user_id
from werkzeug.utils import secure_filename
import os

resource_bp = Blueprint('resources', __name__, url_prefix='/api/resources')

UPLOAD_FOLDER = 'uploads/resources'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'ppt', 'pptx', 'xls', 'xlsx', 'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resource_bp.route('', methods=['GET'])
@token_required
def get_resources():
    """
    Get all resources for the current user
    
    Query Parameters:
        course_id (optional): Filter by course
        resource_type (optional): Filter by type
        is_favorite (optional): Filter favorites (true/false)
    
    Returns:
        200: List of resources
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Get query parameters
        course_id = request.args.get('course_id', type=int)
        resource_type = request.args.get('resource_type')
        is_favorite = request.args.get('is_favorite')
        
        # Convert is_favorite to boolean
        if is_favorite is not None:
            is_favorite = is_favorite.lower() == 'true'
        
        resources = ResourceService.get_user_resources(
            user_id=user_id,
            course_id=course_id,
            resource_type=resource_type,
            is_favorite=is_favorite
        )
        
        return jsonify({
            'message': 'Resources retrieved successfully',
            'resources': resources,
            'total': len(resources)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@resource_bp.route('', methods=['POST'])
@token_required
def create_resource():
    """
    Create a new resource
    
    Form Data or JSON:
        title (required): Resource title
        resource_type (required): Type of resource
        description (optional): Description
        course_id (optional): Associated course ID
        url (optional): External URL
        tags (optional): Comma-separated tags
        file (optional): File upload
    
    Returns:
        201: Resource created
        400: Validation error
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        
        # Check if file upload or JSON
        if request.files and 'file' in request.files:
            # File upload
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'No file selected'
                }), 400
            
            if not allowed_file(file.filename):
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'File type not allowed'
                }), 400
            
            # Save file
            filename = secure_filename(file.filename)
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file_path = os.path.join(UPLOAD_FOLDER, f"{user_id}_{filename}")
            file.save(file_path)
            
            # Get file info
            file_size = os.path.getsize(file_path)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # Get form data
            title = request.form.get('title', filename)
            description = request.form.get('description')
            resource_type = request.form.get('resource_type', 'document')
            course_id = request.form.get('course_id', type=int)
            tags = request.form.get('tags')
            url = None
        else:
            # JSON data (for links/notes)
            data = request.get_json()
            
            if not data:
                return jsonify({
                    'error': 'Bad Request',
                    'message': 'Request body is required'
                }), 400
            
            title = data.get('title')
            description = data.get('description')
            resource_type = data.get('resource_type', 'link')
            course_id = data.get('course_id')
            url = data.get('url')
            tags = data.get('tags')
            file_path = None
            file_size = None
            file_extension = None
        
        # Validate required fields
        if not title:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Title is required'
            }), 400
        
        # Create resource
        resource, error = ResourceService.create_resource(
            user_id=user_id,
            title=title,
            resource_type=resource_type,
            description=description,
            course_id=course_id,
            file_path=file_path,
            url=url,
            file_size=file_size,
            file_extension=file_extension,
            tags=tags
        )
        
        if error:
            return jsonify({
                'error': 'Resource Creation Failed',
                'message': error
            }), 400
        
        return jsonify({
            'message': 'Resource created successfully',
            'resource': resource
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@resource_bp.route('/<int:resource_id>', methods=['GET'])
@token_required
def get_resource(resource_id):
    """
    Get a single resource by ID
    
    Returns:
        200: Resource details
        404: Resource not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        resource = ResourceService.get_resource_by_id(resource_id, user_id)
        
        if not resource:
            return jsonify({
                'error': 'Not Found',
                'message': 'Resource not found'
            }), 404
        
        return jsonify({
            'message': 'Resource retrieved successfully',
            'resource': resource
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@resource_bp.route('/<int:resource_id>', methods=['PUT'])
@token_required
def update_resource(resource_id):
    """
    Update a resource
    
    Request Body:
        title (optional): New title
        description (optional): New description
        resource_type (optional): New type
        course_id (optional): New course ID
        url (optional): New URL
        tags (optional): New tags
    
    Returns:
        200: Resource updated
        404: Resource not found
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
        
        resource, error = ResourceService.update_resource(resource_id, user_id, **data)
        
        if error:
            return jsonify({
                'error': 'Update Failed',
                'message': error
            }), 404 if 'not found' in error.lower() else 400
        
        return jsonify({
            'message': 'Resource updated successfully',
            'resource': resource
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@resource_bp.route('/<int:resource_id>', methods=['DELETE'])
@token_required
def delete_resource(resource_id):
    """
    Delete a resource
    
    Returns:
        200: Resource deleted
        404: Resource not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        success, error = ResourceService.delete_resource(resource_id, user_id)
        
        if not success:
            return jsonify({
                'error': 'Delete Failed',
                'message': error
            }), 404 if 'not found' in error.lower() else 400
        
        return jsonify({
            'message': 'Resource deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500


@resource_bp.route('/<int:resource_id>/favorite', methods=['POST'])
@token_required
def toggle_favorite(resource_id):
    """
    Toggle favorite status of a resource
    
    Returns:
        200: Favorite toggled
        404: Resource not found
        401: Unauthorized
    """
    try:
        user_id = get_current_user_id()
        resource, error = ResourceService.toggle_favorite(resource_id, user_id)
        
        if error:
            return jsonify({
                'error': 'Toggle Failed',
                'message': error
            }), 404 if 'not found' in error.lower() else 400
        
        return jsonify({
            'message': 'Favorite status updated',
            'resource': resource
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e)
        }), 500
