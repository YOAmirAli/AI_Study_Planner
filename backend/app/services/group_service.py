from app.models.group import Group
from app.models.group_member import GroupMember
from app.models.user import User
from app.config.database import db
import random
import string

class GroupService:
    """Group collaboration service"""
    
    @staticmethod
    def _generate_join_code():
        """Generate a unique 6-character join code"""
        while True:
            # Generate random 6-character alphanumeric code
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            # Check if code already exists
            if not Group.query.filter_by(join_code=code).first():
                return code
    
    @staticmethod
    def create_group(admin_user_id: int, group_name: str, description: str = None,
                    is_private: bool = False, max_members: int = 50):
        """
        Create a new study group
        Args:
            admin_user_id (int): User ID of group admin
            group_name (str): Name of the group
            description (str, optional): Group description
            is_private (bool): Whether group is private
            max_members (int): Maximum number of members
        Returns:
            tuple: (group_dict, error_message)
        """
        try:
            # Validate group name
            if not group_name or len(group_name.strip()) < 3:
                return None, "Group name must be at least 3 characters"
            
            if len(group_name) > 100:
                return None, "Group name must be less than 100 characters"
            
            # Check if group name already exists for this user
            existing = Group.query.filter_by(
                admin_user_id=admin_user_id,
                group_name=group_name.strip()
            ).first()
            
            if existing:
                return None, "You already have a group with this name"
            
            # Generate unique join code
            join_code = GroupService._generate_join_code()
            
            # Create group
            group = Group(
                group_name=group_name.strip(),
                description=description,
                admin_user_id=admin_user_id,
                is_private=is_private,
                max_members=max_members,
                join_code=join_code
            )
            
            db.session.add(group)
            db.session.flush()  # Get the group_id
            
            # Add admin as first member
            admin_member = GroupMember(
                group_id=group.group_id,
                user_id=admin_user_id,
                role='admin'
            )
            
            db.session.add(admin_member)
            db.session.commit()
            
            return group.to_dict(include_members=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create group: {str(e)}"
    
    @staticmethod
    def get_user_groups(user_id: int):
        """
        Get all groups user is member of with statistics
        Args:
            user_id (int): User ID
        Returns:
            list: List of groups with stats
        """
        try:
            from app.models.group_message import GroupMessage
            from app.models.group_message_read import GroupMessageRead
            
            # Get user's memberships
            memberships = GroupMember.query.filter_by(user_id=user_id).all()
            
            groups = []
            for membership in memberships:
                group = Group.query.get(membership.group_id)
                if group:
                    group_dict = group.to_dict()
                    group_dict['user_role'] = membership.role
                    
                    # Add message count
                    message_count = GroupMessage.query.filter_by(group_id=group.group_id).count()
                    group_dict['message_count'] = message_count
                    
                    # Add unread message count for this user
                    unread_count = GroupMessageRead.get_unread_count(group.group_id, user_id)
                    group_dict['unread_count'] = unread_count
                    
                    groups.append(group_dict)
            
            return groups
            
        except Exception as e:
            print(f"Error getting user groups: {e}")
            return []
    
    @staticmethod
    def get_group_details(group_id: int, user_id: int):
        """
        Get group details with members
        Args:
            group_id (int): Group ID
            user_id (int): User ID (for authorization)
        Returns:
            tuple: (group_dict, error_message)
        """
        try:
            group = Group.query.get(group_id)
            if not group:
                return None, "Group not found"
            
            # Check if user is member
            if not GroupMember.is_member(group_id, user_id):
                return None, "You are not a member of this group"
            
            return group.to_dict(include_members=True), None
            
        except Exception as e:
            return None, f"Failed to get group details: {str(e)}"
    
    @staticmethod
    def join_group(group_id: int, user_id: int):
        """
        Join a group by group ID
        Args:
            group_id (int): Group ID
            user_id (int): User ID
        Returns:
            tuple: (success: bool, error_message)
        """
        try:
            group = Group.query.get(group_id)
            if not group:
                return False, "Group not found"
            
            # Check if already member
            if GroupMember.is_member(group_id, user_id):
                return False, "You are already a member of this group"
            
            # Check if group is full
            if group.is_full():
                return False, "Group is at maximum capacity"
            
            # Add member
            member = GroupMember(
                group_id=group_id,
                user_id=user_id,
                role='member'
            )
            
            db.session.add(member)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to join group: {str(e)}"
    
    @staticmethod
    def join_group_by_code(join_code: str, user_id: int):
        """
        Join a group using join code
        Args:
            join_code (str): Group join code
            user_id (int): User ID
        Returns:
            tuple: (group_dict or None, error_message)
        """
        try:
            # Find group by join code
            group = Group.query.filter_by(join_code=join_code.upper()).first()
            if not group:
                return None, "Invalid join code"
            
            # Check if already member
            if GroupMember.is_member(group.group_id, user_id):
                return None, "You are already a member of this group"
            
            # Check if group is full
            if group.is_full():
                return None, "Group is at maximum capacity"
            
            # Add member
            member = GroupMember(
                group_id=group.group_id,
                user_id=user_id,
                role='member'
            )
            
            db.session.add(member)
            db.session.commit()
            
            return group.to_dict(include_members=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to join group: {str(e)}"
    
    @staticmethod
    def leave_group(group_id: int, user_id: int):
        """
        Leave a group
        Args:
            group_id (int): Group ID
            user_id (int): User ID
        Returns:
            tuple: (success: bool, error_message)
        """
        try:
            group = Group.query.get(group_id)
            if not group:
                return False, "Group not found"
            
            # Check if user is admin
            if group.is_admin(user_id):
                return False, "Admin cannot leave group. Transfer admin role or delete group."
            
            # Find membership
            membership = GroupMember.query.filter_by(
                group_id=group_id,
                user_id=user_id
            ).first()
            
            if not membership:
                return False, "You are not a member of this group"
            
            # Remove membership
            db.session.delete(membership)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to leave group: {str(e)}"
    
    @staticmethod
    def delete_group(group_id: int, user_id: int):
        """
        Delete a group (admin only)
        Args:
            group_id (int): Group ID
            user_id (int): User ID (must be admin)
        Returns:
            tuple: (success: bool, error_message)
        """
        try:
            group = Group.query.get(group_id)
            if not group:
                return False, "Group not found"
            
            # Check if user is admin
            if not group.is_admin(user_id):
                return False, "Only group admin can delete the group"
            
            # Delete group (cascade will delete members)
            db.session.delete(group)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete group: {str(e)}"
    
    @staticmethod
    def update_group(group_id: int, user_id: int, **kwargs):
        """
        Update group information (admin only)
        Args:
            group_id (int): Group ID
            user_id (int): User ID (must be admin)
            **kwargs: Fields to update
        Returns:
            tuple: (group_dict, error_message)
        """
        try:
            group = Group.query.get(group_id)
            if not group:
                return None, "Group not found"
            
            # Check if user is admin
            if not group.is_admin(user_id):
                return None, "Only group admin can update the group"
            
            # Update fields
            if 'group_name' in kwargs:
                if len(kwargs['group_name'].strip()) < 3:
                    return None, "Group name must be at least 3 characters"
                group.group_name = kwargs['group_name'].strip()
            
            if 'description' in kwargs:
                group.description = kwargs['description']
            
            if 'is_private' in kwargs:
                group.is_private = kwargs['is_private']
            
            if 'max_members' in kwargs:
                if kwargs['max_members'] < group.get_member_count():
                    return None, "Cannot set max members below current member count"
                group.max_members = kwargs['max_members']
            
            db.session.commit()
            return group.to_dict(include_members=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update group: {str(e)}"
