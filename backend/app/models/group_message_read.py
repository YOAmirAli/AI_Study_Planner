"""
Group Message Read Model
Tracks which messages have been read by which users
"""

from app.config.database import db
from datetime import datetime

class GroupMessageRead(db.Model):
    """Track message read status"""
    __tablename__ = 'group_message_reads'
    
    # Composite Primary Key
    message_id = db.Column(db.Integer, db.ForeignKey('group_messages.message_id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True)
    
    # Timestamp
    read_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f'<GroupMessageRead Message:{self.message_id} User:{self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'message_id': self.message_id,
            'user_id': self.user_id,
            'read_at': self.read_at.isoformat() if self.read_at else None
        }
    
    @staticmethod
    def mark_as_read(message_id: int, user_id: int):
        """Mark a message as read by a user"""
        try:
            # Check if already marked as read
            existing = GroupMessageRead.query.filter_by(
                message_id=message_id,
                user_id=user_id
            ).first()
            
            if not existing:
                read_record = GroupMessageRead(
                    message_id=message_id,
                    user_id=user_id
                )
                db.session.add(read_record)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            print(f"Error marking message as read: {e}")
            return False
    
    @staticmethod
    def mark_all_as_read(group_id: int, user_id: int):
        """Mark all messages in a group as read for a user"""
        try:
            from app.models.group_message import GroupMessage
            
            # Get all messages in the group
            messages = GroupMessage.query.filter_by(group_id=group_id).all()
            
            for message in messages:
                # Skip if already read
                existing = GroupMessageRead.query.filter_by(
                    message_id=message.message_id,
                    user_id=user_id
                ).first()
                
                if not existing:
                    read_record = GroupMessageRead(
                        message_id=message.message_id,
                        user_id=user_id
                    )
                    db.session.add(read_record)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error marking all messages as read: {e}")
            return False
    
    @staticmethod
    def get_unread_count(group_id: int, user_id: int):
        """Get count of unread messages in a group for a user"""
        try:
            from app.models.group_message import GroupMessage
            
            # Get all messages in the group
            all_messages = GroupMessage.query.filter_by(group_id=group_id).all()
            
            # Get messages read by this user
            read_message_ids = [r.message_id for r in GroupMessageRead.query.filter_by(user_id=user_id).all()]
            
            # Count unread (exclude user's own messages)
            unread_count = 0
            for message in all_messages:
                if message.user_id != user_id and message.message_id not in read_message_ids:
                    unread_count += 1
            
            return unread_count
        except Exception as e:
            print(f"Error getting unread count: {e}")
            return 0
