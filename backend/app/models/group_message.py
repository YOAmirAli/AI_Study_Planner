"""
Group Message Model
Handles group chat/discussion messages
"""

from app.config.database import db
from datetime import datetime

class GroupMessage(db.Model):
    """Group chat messages"""
    __tablename__ = 'group_messages'
    
    # Primary Key
    message_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id', ondelete='CASCADE'), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Message Content
    message_text = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text', nullable=False)  # text, announcement, system
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    edited_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    read_records = db.relationship('GroupMessageRead', backref='message', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<GroupMessage {self.message_id}>'
    
    def to_dict(self, include_user=True):
        """Convert message to dictionary"""
        message_dict = {
            'message_id': self.message_id,
            'group_id': self.group_id,
            'user_id': self.user_id,
            'message_text': self.message_text,
            'message_type': self.message_type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'edited_at': self.edited_at.isoformat() if self.edited_at else None
        }
        
        if include_user:
            from app.models.user import User
            user = User.query.get(self.user_id)
            if user:
                message_dict['user'] = {
                    'user_id': user.user_id,
                    'name': user.name,
                    'email': user.email
                }
        
        return message_dict
