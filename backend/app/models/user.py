from app.config.database import db
from datetime import datetime

class User(db.Model):
    """
    User Model - Normalized to 3NF
    
    3NF Compliance:
    - 1NF: All attributes are atomic (no repeating groups)
    - 2NF: No partial dependencies (all non-key attributes depend on entire primary key)
    - 3NF: No transitive dependencies (non-key attributes don't depend on other non-key attributes)
    """
    __tablename__ = 'users'
    
    # Primary Key
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # User Credentials
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)  # bcrypt hashed
    
    # User Profile Information
    name = db.Column(db.String(255), nullable=False)
    university = db.Column(db.String(255), nullable=True)
    program = db.Column(db.String(255), nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships will be added in later phases when models are created
    # Phase 3: courses, tasks
    # Phase 4: schedules
    # Phase 7: notifications
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def to_dict(self):
        """Convert user object to dictionary (excluding password)"""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'university': self.university,
            'program': self.program,
            'profile_picture': self.profile_picture,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
