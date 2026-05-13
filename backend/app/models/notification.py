from app.config.database import db
from datetime import datetime

class Notification(db.Model):
    """
    Notification Model - System notifications and alerts
    Stores notifications for users about deadlines, alerts, and group activities
    """
    __tablename__ = 'notifications'
    
    # Primary Key
    notification_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Notification Information
    type = db.Column(db.Enum('deadline_reminder', 'overdue_alert', 'falling_behind', 
                            'study_reminder', 'group_activity', name='notification_type_enum'), 
                    nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    
    # Optional References
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id', ondelete='SET NULL'), nullable=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.group_id', ondelete='SET NULL'), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Notification {self.notification_id} - {self.type}>'
    
    def to_dict(self):
        """Convert notification to dictionary"""
        return {
            'notification_id': self.notification_id,
            'user_id': self.user_id,
            'type': self.type,
            'title': self.title,
            'message': self.message,
            'is_read': self.is_read,
            'task_id': self.task_id,
            'group_id': self.group_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
