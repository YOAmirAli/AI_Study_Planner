"""
Resource Model - 3NF Normalized
Stores student learning resources and materials
"""

from app.config.database import db
from datetime import datetime

class Resource(db.Model):
    """
    Resource Model - Normalized to 3NF
    
    Represents learning resources/materials for students including:
    - PDFs, documents, links, videos, notes
    - Associated with courses or standalone
    - Categorized by type and tags
    
    3NF Compliance:
    - 1NF: All attributes are atomic
    - 2NF: No partial dependencies (all attributes depend on resource_id)
    - 3NF: No transitive dependencies
    """
    __tablename__ = 'resources'
    
    # Primary Key
    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Resource Information
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Resource Type: 'pdf', 'link', 'video', 'document', 'note', 'other'
    resource_type = db.Column(db.String(50), nullable=False, default='document', index=True)
    
    # Storage
    file_path = db.Column(db.String(500), nullable=True)  # For uploaded files
    url = db.Column(db.String(500), nullable=True)  # For external links
    
    # Metadata
    file_size = db.Column(db.Integer, nullable=True)  # Size in bytes
    file_extension = db.Column(db.String(10), nullable=True)  # e.g., .pdf, .docx
    
    # Organization
    tags = db.Column(db.String(500), nullable=True)  # Comma-separated tags
    is_favorite = db.Column(db.Boolean, default=False, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_accessed = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Resource {self.title}>'
    
    def to_dict(self, include_course=False):
        """Convert resource object to dictionary"""
        resource_dict = {
            'resource_id': self.resource_id,
            'user_id': self.user_id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'file_path': self.file_path,
            'url': self.url,
            'file_size': self.file_size,
            'file_extension': self.file_extension,
            'tags': self.tags.split(',') if self.tags else [],
            'is_favorite': self.is_favorite,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_accessed': self.last_accessed.isoformat() if self.last_accessed else None
        }
        
        # Include course details if requested
        if include_course and self.course_id:
            from app.models.course import Course
            course = Course.query.get(self.course_id)
            if course:
                resource_dict['course'] = {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_code': course.course_code,
                    'color': course.color
                }
        
        return resource_dict
