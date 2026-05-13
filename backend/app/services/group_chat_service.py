"""
Group Chat Service
Handles group messaging functionality
"""

from app.models.group_message import GroupMessage
from app.models.group_member import GroupMember
from app.config.database import db
from datetime import datetime

class GroupChatService:
    """Group chat and messaging service"""
    
    @staticmethod
    def send_message(group_id: int, user_id: int, message_text: str, message_type: str = 'text'):
        """
        Send a message to group chat
        
        Args:
            group_id (int): Group ID
            user_id (int): User ID
            message_text (str): Message content
            message_type (str): Message type (text, announcement, system)
            
        Returns:
            tuple: (message_dict, error_message)
        """
        try:
            # Check if user is member
            if not GroupMember.is_member(group_id, user_id):
                return None, "You are not a member of this group"
            
            # Validate message
            if not message_text or len(message_text.strip()) == 0:
                return None, "Message cannot be empty"
            
            if len(message_text) > 5000:
                return None, "Message is too long (max 5000 characters)"
            
            # Create message
            message = GroupMessage(
                group_id=group_id,
                user_id=user_id,
                message_text=message_text.strip(),
                message_type=message_type
            )
            
            db.session.add(message)
            db.session.commit()
            
            return message.to_dict(include_user=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to send message: {str(e)}"
    
    @staticmethod
    def get_group_messages(group_id: int, user_id: int, limit: int = 50, offset: int = 0):
        """
        Get messages from group chat
        
        Args:
            group_id (int): Group ID
            user_id (int): User ID (for authorization)
            limit (int): Number of messages to fetch
            offset (int): Offset for pagination
            
        Returns:
            tuple: (messages_list, error_message)
        """
        try:
            # Check if user is member
            if not GroupMember.is_member(group_id, user_id):
                return None, "You are not a member of this group"
            
            # Get messages
            messages = GroupMessage.query.filter_by(group_id=group_id).order_by(
                GroupMessage.created_at.desc()
            ).limit(limit).offset(offset).all()
            
            # Reverse to show oldest first
            messages.reverse()
            
            return [msg.to_dict(include_user=True) for msg in messages], None
            
        except Exception as e:
            return None, f"Failed to get messages: {str(e)}"
    
    @staticmethod
    def delete_message(message_id: int, user_id: int):
        """
        Delete a message (only by sender or group admin)
        
        Args:
            message_id (int): Message ID
            user_id (int): User ID
            
        Returns:
            tuple: (success, error_message)
        """
        try:
            message = GroupMessage.query.get(message_id)
            if not message:
                return False, "Message not found"
            
            # Check if user is sender or admin
            from app.models.group import Group
            group = Group.query.get(message.group_id)
            
            if message.user_id != user_id and not group.is_admin(user_id):
                return False, "You can only delete your own messages"
            
            db.session.delete(message)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete message: {str(e)}"
