from app.config.database import db
from datetime import datetime

class Course(db.Model):
    """
    Course Model - Normalized to 3NF
    
    3NF Compliance:
    - 1NF: All attributes are atomic (schedule stored as JSON for flexibility)
    - 2NF: No partial dependencies (all attributes depend on course_id)
    - 3NF: No transitive dependencies (no non-key attribute depends on another non-key)
    """
    __tablename__ = 'courses'
    
    # Primary Key
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Course Information
    course_name = db.Column(db.String(255), nullable=False)
    course_code = db.Column(db.String(50), nullable=True)
    credit_hours = db.Column(db.Integer, nullable=True)
    instructor = db.Column(db.String(255), nullable=True)
    
    # AI-extracted topics from syllabus
    topics = db.Column(db.Text, nullable=True)
    
    # UI customization
    color = db.Column(db.String(7), nullable=True)  # Hex color code (e.g., #FF5733)
    
    # Class schedule stored as JSON
    # Format: [{"day": "Monday", "start_time": "09:00", "end_time": "10:30"}, ...]
    schedule = db.Column(db.JSON, nullable=True)
    
    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    tasks = db.relationship('Task', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.course_name}>'
    
    def to_dict(self):
        """Convert course object to dictionary"""
        return {
            'course_id': self.course_id,
            'user_id': self.user_id,
            'course_name': self.course_name,
            'course_code': self.course_code,
            'credit_hours': self.credit_hours,
            'instructor': self.instructor,
            'topics': self.topics,
            'color': self.color,
            'schedule': self.schedule,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
