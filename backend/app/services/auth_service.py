from app.models.user import User
from app.config.database import db
from app.utils.password_utils import hash_password, verify_password
from app.utils.validators import validate_email, validate_password_strength, validate_name
from app.utils.jwt_utils import create_token

class AuthService:
    """Authentication service for user registration and login"""
    
    @staticmethod
    def register_user(email: str, password: str, name: str, university: str = None, program: str = None):
        """
        Register a new user
        
        Args:
            email (str): User email
            password (str): Plain text password
            name (str): User name
            university (str, optional): University name
            program (str, optional): Program/degree name
            
        Returns:
            tuple: (user_dict, token, error_message)
        """
        # Validate email
        if not validate_email(email):
            return None, None, "Invalid email format"
        
        # Validate name
        is_valid_name, name_message = validate_name(name)
        if not is_valid_name:
            return None, None, name_message
        
        # Validate password strength
        is_valid_password, password_message = validate_password_strength(password)
        if not is_valid_password:
            return None, None, password_message
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email.lower()).first()
        if existing_user:
            return None, None, "Email already registered"
        
        try:
            # Hash password
            hashed_password = hash_password(password)
            
            # Create new user
            new_user = User(
                email=email.lower(),
                password=hashed_password,
                name=name.strip(),
                university=university.strip() if university else None,
                program=program.strip() if program else None
            )
            
            # Save to database
            db.session.add(new_user)
            db.session.commit()
            
            # Generate JWT token
            token = create_token(new_user.user_id)
            
            return new_user.to_dict(), token, None
            
        except Exception as e:
            db.session.rollback()
            return None, None, f"Registration failed: {str(e)}"
    
    @staticmethod
    def login_user(email: str, password: str):
        """
        Authenticate user and generate token
        
        Args:
            email (str): User email
            password (str): Plain text password
            
        Returns:
            tuple: (user_dict, token, error_message)
        """
        # Validate inputs
        if not email or not password:
            return None, None, "Email and password are required"
        
        # Find user by email
        user = User.query.filter_by(email=email.lower()).first()
        
        if not user:
            return None, None, "Invalid email or password"
        
        # Verify password
        if not verify_password(password, user.password):
            return None, None, "Invalid email or password"
        
        # Generate JWT token
        token = create_token(user.user_id)
        
        return user.to_dict(), token, None
    
    @staticmethod
    def get_user_by_id(user_id: int):
        """
        Get user by ID
        
        Args:
            user_id (int): User ID
            
        Returns:
            User: User object or None
        """
        return User.query.get(user_id)
