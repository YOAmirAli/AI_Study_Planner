from app.models.user import User
from app.config.database import db
from app.utils.password_utils import hash_password, verify_password
from app.utils.validators import validate_name

class UserService:
    """User management service for profile operations"""
    
    @staticmethod
    def get_user_profile(user_id: int):
        """
        Get user profile by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: User profile data or None
        """
        user = User.query.get(user_id)
        if user:
            return user.to_dict()
        return None
    
    @staticmethod
    def update_user_profile(user_id: int, name: str = None, university: str = None, 
                           program: str = None, profile_picture: str = None):
        """
        Update user profile information
        
        Args:
            user_id (int): User ID
            name (str, optional): New name
            university (str, optional): New university
            program (str, optional): New program
            profile_picture (str, optional): New profile picture URL
            
        Returns:
            tuple: (user_dict, error_message)
        """
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        
        try:
            # Update name if provided
            if name is not None:
                is_valid, message = validate_name(name)
                if not is_valid:
                    return None, message
                user.name = name.strip()
            
            # Update university if provided
            if university is not None:
                user.university = university.strip() if university else None
            
            # Update program if provided
            if program is not None:
                user.program = program.strip() if program else None
            
            # Update profile picture if provided
            if profile_picture is not None:
                user.profile_picture = profile_picture.strip() if profile_picture else None
            
            # Save changes
            db.session.commit()
            
            return user.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Update failed: {str(e)}"
    
    @staticmethod
    def change_password(user_id: int, current_password: str, new_password: str):
        """
        Change user password
        
        Args:
            user_id (int): User ID
            current_password (str): Current password
            new_password (str): New password
            
        Returns:
            tuple: (success: bool, error_message)
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        # Verify current password
        if not verify_password(current_password, user.password):
            return False, "Current password is incorrect"
        
        # Validate new password strength
        from app.utils.validators import validate_password_strength
        is_valid, message = validate_password_strength(new_password)
        if not is_valid:
            return False, message
        
        try:
            # Hash and update password
            user.password = hash_password(new_password)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Password change failed: {str(e)}"
    
    @staticmethod
    def delete_user(user_id: int):
        """
        Delete user account
        
        Args:
            user_id (int): User ID
            
        Returns:
            tuple: (success: bool, error_message)
        """
        user = User.query.get(user_id)
        if not user:
            return False, "User not found"
        
        try:
            db.session.delete(user)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Delete failed: {str(e)}"
