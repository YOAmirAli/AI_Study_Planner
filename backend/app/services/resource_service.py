"""
Resource Service
Handles all resource-related business logic
"""

from app.models.resource import Resource
from app.config.database import db
from datetime import datetime
import os

class ResourceService:
    """Resource management service"""
    
    @staticmethod
    def create_resource(user_id: int, title: str, resource_type: str,
                       description: str = None, course_id: int = None,
                       file_path: str = None, url: str = None,
                       file_size: int = None, file_extension: str = None,
                       tags: str = None):
        """
        Create a new resource
        
        Args:
            user_id (int): User ID
            title (str): Resource title
            resource_type (str): Type of resource
            description (str, optional): Description
            course_id (int, optional): Associated course ID
            file_path (str, optional): Path to uploaded file
            url (str, optional): External URL
            file_size (int, optional): File size in bytes
            file_extension (str, optional): File extension
            tags (str, optional): Comma-separated tags
            
        Returns:
            tuple: (resource_dict, error_message)
        """
        # Validate required fields
        if not title or not title.strip():
            return None, "Title is required"
        
        if resource_type not in ['pdf', 'link', 'video', 'document', 'note', 'other']:
            return None, "Invalid resource type"
        
        # Validate that either file_path or url is provided
        if not file_path and not url and resource_type != 'note':
            return None, "Either file or URL is required"
        
        try:
            new_resource = Resource(
                user_id=user_id,
                title=title.strip(),
                description=description.strip() if description else None,
                resource_type=resource_type,
                course_id=course_id,
                file_path=file_path,
                url=url,
                file_size=file_size,
                file_extension=file_extension,
                tags=tags,
                is_favorite=False
            )
            
            db.session.add(new_resource)
            db.session.commit()
            
            return new_resource.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create resource: {str(e)}"
    
    @staticmethod
    def get_user_resources(user_id: int, course_id: int = None, 
                          resource_type: str = None, is_favorite: bool = None):
        """
        Get resources for a user with optional filters
        
        Args:
            user_id (int): User ID
            course_id (int, optional): Filter by course
            resource_type (str, optional): Filter by type
            is_favorite (bool, optional): Filter favorites
            
        Returns:
            list: List of resource dictionaries
        """
        query = Resource.query.filter_by(user_id=user_id)
        
        if course_id is not None:
            query = query.filter_by(course_id=course_id)
        
        if resource_type:
            query = query.filter_by(resource_type=resource_type)
        
        if is_favorite is not None:
            query = query.filter_by(is_favorite=is_favorite)
        
        resources = query.order_by(Resource.created_at.desc()).all()
        return [resource.to_dict(include_course=True) for resource in resources]
    
    @staticmethod
    def get_resource_by_id(resource_id: int, user_id: int):
        """
        Get a single resource by ID
        
        Args:
            resource_id (int): Resource ID
            user_id (int): User ID (for authorization)
            
        Returns:
            dict: Resource dictionary or None
        """
        resource = Resource.query.filter_by(resource_id=resource_id, user_id=user_id).first()
        
        if resource:
            # Update last accessed time
            resource.last_accessed = datetime.utcnow()
            db.session.commit()
            
        return resource.to_dict(include_course=True) if resource else None
    
    @staticmethod
    def update_resource(resource_id: int, user_id: int, **kwargs):
        """
        Update resource information
        
        Args:
            resource_id (int): Resource ID
            user_id (int): User ID (for authorization)
            **kwargs: Fields to update
            
        Returns:
            tuple: (resource_dict, error_message)
        """
        resource = Resource.query.filter_by(resource_id=resource_id, user_id=user_id).first()
        
        if not resource:
            return None, "Resource not found"
        
        try:
            # Update allowed fields
            allowed_fields = ['title', 'description', 'resource_type', 'course_id', 
                            'url', 'tags', 'is_favorite']
            
            for key, value in kwargs.items():
                if key in allowed_fields and value is not None:
                    setattr(resource, key, value)
            
            resource.updated_at = datetime.utcnow()
            db.session.commit()
            
            return resource.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update resource: {str(e)}"
    
    @staticmethod
    def delete_resource(resource_id: int, user_id: int):
        """
        Delete a resource
        
        Args:
            resource_id (int): Resource ID
            user_id (int): User ID (for authorization)
            
        Returns:
            tuple: (success, error_message)
        """
        resource = Resource.query.filter_by(resource_id=resource_id, user_id=user_id).first()
        
        if not resource:
            return False, "Resource not found"
        
        try:
            # Delete file if exists
            if resource.file_path and os.path.exists(resource.file_path):
                os.remove(resource.file_path)
            
            db.session.delete(resource)
            db.session.commit()
            
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete resource: {str(e)}"
    
    @staticmethod
    def toggle_favorite(resource_id: int, user_id: int):
        """
        Toggle favorite status of a resource
        
        Args:
            resource_id (int): Resource ID
            user_id (int): User ID
            
        Returns:
            tuple: (resource_dict, error_message)
        """
        resource = Resource.query.filter_by(resource_id=resource_id, user_id=user_id).first()
        
        if not resource:
            return None, "Resource not found"
        
        try:
            resource.is_favorite = not resource.is_favorite
            db.session.commit()
            
            return resource.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to toggle favorite: {str(e)}"
