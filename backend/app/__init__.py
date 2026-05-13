import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_app(config_name=None):
    """Application factory function"""
    
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Initialize CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # JWT error handlers
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Missing authorization header'
        }), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid token'
        }), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Token has expired'
        }), 401
    
    # Initialize database
    from app.config import init_db
    init_db(app)
    
    # Register blueprints (routes)
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Initialize job scheduler (Phase 7)
    try:
        from app.tasks.scheduler import init_scheduler
        init_scheduler()
    except Exception as e:
        print(f"⚠️ Job scheduler initialization failed: {e}")
    
    return app


def register_blueprints(app):
    """Register all blueprints"""
    
    # Health check route (Phase 1)
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'ok',
            'message': 'AI Study Planner API is running',
            'version': '1.0.0'
        }), 200
    
    # Phase 2: Authentication routes
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    
    # Phase 3: Course and Task routes
    from app.routes.course_routes import course_bp
    from app.routes.task_routes import task_bp
    app.register_blueprint(course_bp)
    app.register_blueprint(task_bp)
    
    # Phase 4: Schedule routes
    from app.routes.schedule_routes import schedule_bp
    app.register_blueprint(schedule_bp)
    
    # Phase 5: AI routes
    from app.routes.ai_routes import ai_bp
    app.register_blueprint(ai_bp)
    
    # Phase 6: Analytics routes
    from app.routes.analytics_routes import analytics_bp
    app.register_blueprint(analytics_bp)
    
    # Phase 7: Notification and Group routes
    from app.routes.notification_routes import notification_bp
    from app.routes.group_routes import group_bp
    app.register_blueprint(notification_bp)
    app.register_blueprint(group_bp)
    
    # Resource routes
    from app.routes.resource_routes import resource_bp
    app.register_blueprint(resource_bp)
    
    # Quiz routes
    from app.routes.quiz_routes import quiz_bp
    app.register_blueprint(quiz_bp)
    
    # Group chat and enhanced features
    from app.routes.group_chat_routes import group_chat_bp
    app.register_blueprint(group_chat_bp)


def register_error_handlers(app):
    """Register error handlers"""
    from app.middleware.error_handler import register_error_handlers as register_custom_handlers
    register_custom_handlers(app)
