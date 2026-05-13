from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """Register custom error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad Request',
            'message': str(error.description) if hasattr(error, 'description') else 'The request was invalid'
        }), 400
    
    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required'
        }), 401
    
    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            'error': 'Forbidden',
            'message': 'You do not have permission to access this resource'
        }), 403
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found'
        }), 404
    
    @app.errorhandler(409)
    def conflict(error):
        return jsonify({
            'error': 'Conflict',
            'message': str(error.description) if hasattr(error, 'description') else 'Resource conflict'
        }), 409
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal error occurred'
        }), 500
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        # Handle HTTP exceptions
        if isinstance(error, HTTPException):
            return jsonify({
                'error': error.name,
                'message': error.description
            }), error.code
        
        # Handle non-HTTP exceptions
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An unexpected error occurred'
        }), 500
