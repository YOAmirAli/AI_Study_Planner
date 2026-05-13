from app.config.database import db
from datetime import datetime

class GroupMember(db.Model):
    """
    GroupMember Model - Group membership tracking
    Tracks which users are members of which groups and their roles
    """
    __tablename__ = 'group_members'
    
    # Composite Primary Key
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    
    # Member Information
    role = db.Column(db.Enum('admin', 'member', name='member_role_enum'), default='member', nullable=False)
    
    # Timestamps
    joined_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<GroupMember Group:{self.group_id} User:{self.user_id}>'
    
    def to_dict(self):
        """Convert group member to dictionary"""
        return {
            'group_id': self.group_id,
            'user_id': self.user_id,
            'role': self.role,
            'joined_at': self.joined_at.isoformat() if self.joined_at else None
        }
    
    @staticmethod
    def is_member(group_id, user_id):
        """Check if user is member of group"""
        return GroupMember.query.filter_by(group_id=group_id, user_id=user_id).first() is not None
    
    @staticmethod
    def get_user_groups(user_id):
        """Get all groups user is member of"""
        return GroupMember.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_group_members(group_id):
        """Get all members of a group"""
        return GroupMember.query.filter_by(group_id=group_id).all()
