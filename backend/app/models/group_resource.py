"""
Group Resource Model
Handles resources shared within groups
"""

from app.config.database import db
from datetime import datetime

class GroupResource(db.Model):
    """Resources shared in groups"""
    __tablename__ = 'group_resources'
    
    # Primary Key
    resource_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False, index=True)
    shared_by_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    # Resource Information
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    resource_type = db.Column(db.String(50), nullable=False)  # link, file, note
    resource_url = db.Column(db.String(500), nullable=True)
    content = db.Column(db.Text, nullable=True)  # For notes
    
    # Metadata
    tags = db.Column(db.String(500), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<GroupResource {self.resource_id} - {self.title}>'
    
    def to_dict(self, include_user=True):
        """Convert resource to dictionary"""
        resource_dict = {
            'resource_id': self.resource_id,
            'group_id': self.group_id,
            'shared_by_user_id': self.shared_by_user_id,
            'title': self.title,
            'description': self.description,
            'resource_type': self.resource_type,
            'resource_url': self.resource_url,
            'content': self.content,
            'tags': self.tags.split(',') if self.tags else [],
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        
        if include_user:
            from app.models.user import User
            user = User.query.get(self.shared_by_user_id)
            if user:
                resource_dict['shared_by'] = {
                    'user_id': user.user_id,
                    'name': user.name
                }
        
        return resource_dict
