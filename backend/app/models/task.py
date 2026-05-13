from app.config.database import db
from datetime import datetime

class Task(db.Model):
    """
    Task Model - Normalized to 3NF
    
    3NF Compliance:
    - 1NF: All attributes are atomic
    - 2NF: No partial dependencies (all attributes depend on task_id)
    - 3NF: No transitive dependencies
    """
    __tablename__ = 'tasks'
    
    # Primary Key
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Task Information
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    deadline = db.Column(db.DateTime, nullable=False, index=True)
    
    # Priority: high, medium, low
    priority = db.Column(db.Enum('high', 'medium', 'low', name='priority_enum'), nullable=False, default='medium')
    
    # Status: pending, in_progress, completed
    status = db.Column(db.Enum('pending', 'in_progress', 'completed', name='status_enum'), nullable=False, default='pending')
    
    # Time tracking (in minutes)
    estimated_time = db.Column(db.Integer, nullable=True)  # AI-estimated or user-provided
    actual_time = db.Column(db.Integer, nullable=True)     # User-logged actual time
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Task {self.title}>'
    
    def to_dict(self, include_course=False):
        """Convert task object to dictionary"""
        task_dict = {
            'task_id': self.task_id,
            'course_id': self.course_id,
            'user_id': self.user_id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline.isoformat() if self.deadline else None,
            'priority': self.priority,
            'status': self.status,
            'estimated_time': self.estimated_time,
            'actual_time': self.actual_time,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
        
        # Optionally include course information
        if include_course and self.course:
            task_dict['course'] = {
                'course_id': self.course.course_id,
                'course_name': self.course.course_name,
                'course_code': self.course.course_code,
                'color': self.course.color
            }
        
        return task_dict
