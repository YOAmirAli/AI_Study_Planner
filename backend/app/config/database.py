from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy instance
db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    db.init_app(app)
    
    with app.app_context():
        # Import all models here to ensure they are registered with SQLAlchemy
        from app.models import (
            User, Course, Task, Schedule, Analytics, Notification, 
            Group, GroupMember, GroupMessage, GroupMessageRead, GroupResource,
            Resource, Quiz, QuizQuestion, QuizResult
        )
        
        # Create all tables
        db.create_all()
        print("✓ PostgreSQL database tables created successfully")
    
    return db