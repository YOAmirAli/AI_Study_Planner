from app.config.database import db
from datetime import datetime

class Group(db.Model):
    """
    Group Model - Study groups for collaboration
    Represents study groups where students can collaborate and share resources
    """
    __tablename__ = 'groups'
    
    # Primary Key
    group_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Group Information
    group_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    join_code = db.Column(db.String(10), unique=True, nullable=False, index=True)
    
    # Admin (creator of the group)
    admin_user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False)
    
    # Settings
    is_private = db.Column(db.Boolean, default=False, nullable=False)
    max_members = db.Column(db.Integer, default=50, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    members = db.relationship('GroupMember', backref='group', lazy=True, cascade='all, delete-orphan')
    messages = db.relationship('GroupMessage', backref='group', lazy=True, cascade='all, delete-orphan')
    resources = db.relationship('GroupResource', backref='group', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Group {self.group_id} - {self.group_name}>'
    
    def to_dict(self, include_members=False, include_stats=False):
        """Convert group to dictionary"""
        group_dict = {
            'group_id': self.group_id,
            'group_name': self.group_name,
            'description': self.description,
            'join_code': self.join_code,
            'admin_user_id': self.admin_user_id,
            'is_private': self.is_private,
            'max_members': self.max_members,
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_members:
            from app.models.user import User
            group_dict['members'] = []
            for member in self.members:
                user = User.query.get(member.user_id)
                if user:
                    group_dict['members'].append({
                        'user_id': user.user_id,
                        'name': user.name,
                        'email': user.email,
                        'role': member.role,
                        'joined_at': member.joined_at.isoformat() if member.joined_at else None
                    })
        
        if include_stats:
            from app.models.group_message import GroupMessage
            from app.models.group_resource import GroupResource
            
            # Add message count
            group_dict['message_count'] = GroupMessage.query.filter_by(group_id=self.group_id).count()
            
            # Add resource count
            group_dict['resource_count'] = GroupResource.query.filter_by(group_id=self.group_id).count()
        
        return group_dict
    
    def get_member_count(self):
        """Get current member count"""
        return len(self.members)
    
    def is_full(self):
        """Check if group is at maximum capacity"""
        return self.get_member_count() >= self.max_members
    
    def is_admin(self, user_id):
        """Check if user is admin of this group"""
        return self.admin_user_id == user_id
