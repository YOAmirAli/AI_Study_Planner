# Routes package
from .auth_routes import auth_bp
from .user_routes import user_bp
from .course_routes import course_bp
from .task_routes import task_bp

__all__ = ['auth_bp', 'user_bp', 'course_bp', 'task_bp']
