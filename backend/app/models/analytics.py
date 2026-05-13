from app.config.database import db
from datetime import datetime

class Analytics(db.Model):
    """
    Analytics Model - Study session tracking and performance metrics
    
    Stores study session data for analytics and progress tracking
    """
    __tablename__ = 'analytics'
    
    # Primary Key
    record_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id', ondelete='SET NULL'), nullable=True, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Session Information
    session_date = db.Column(db.Date, nullable=False, index=True)
    hours_spent = db.Column(db.Numeric(6, 2), nullable=False)  # Study hours for this session
    
    # Performance Metrics
    completion_rate = db.Column(db.Numeric(5, 2), nullable=True)  # Percentage
    predicted_grade = db.Column(db.String(5), nullable=True)  # ML prediction (optional)
    
    # Notes
    notes = db.Column(db.Text, nullable=True)
    
    # Timestamp
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<Analytics {self.record_id} - User {self.user_id}>'
    
    def to_dict(self):
        """Convert analytics record to dictionary"""
        return {
            'record_id': self.record_id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'course_id': self.course_id,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'hours_spent': float(self.hours_spent) if self.hours_spent else 0,
            'completion_rate': float(self.completion_rate) if self.completion_rate else None,
            'predicted_grade': self.predicted_grade,
            'notes': self.notes,
            'recorded_at': self.recorded_at.isoformat() if self.recorded_at else None
        }
