from app.models.course import Course
from app.models.task import Task
from app.config.database import db
from sqlalchemy import func

class CourseService:
    """Course management service"""
    
    @staticmethod
    def create_course(user_id: int, course_name: str, course_code: str = None,
                     credit_hours: int = None, instructor: str = None,
                     color: str = None, schedule: list = None, topics: str = None):
        """
        Create a new course
        
        Args:
            user_id (int): User ID
            course_name (str): Course name
            course_code (str, optional): Course code
            credit_hours (int, optional): Credit hours
            instructor (str, optional): Instructor name
            color (str, optional): Hex color code
            schedule (list, optional): Class schedule
            topics (str, optional): Course topics
            
        Returns:
            tuple: (course_dict, error_message)
        """
        # Validate required fields
        if not course_name or not course_name.strip():
            return None, "Course name is required"
        
        # Validate credit hours
        if credit_hours is not None and (credit_hours < 0 or credit_hours > 20):
            return None, "Credit hours must be between 0 and 20"
        
        # Validate color format (hex color)
        if color and not color.startswith('#'):
            return None, "Color must be in hex format (e.g., #FF5733)"
        
        try:
            new_course = Course(
                user_id=user_id,
                course_name=course_name.strip(),
                course_code=course_code.strip() if course_code else None,
                credit_hours=credit_hours,
                instructor=instructor.strip() if instructor else None,
                color=color,
                schedule=schedule,
                topics=topics
            )
            
            db.session.add(new_course)
            db.session.commit()
            
            return new_course.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create course: {str(e)}"
    
    @staticmethod
    def get_user_courses(user_id: int):
        """
        Get all courses for a user
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of course dictionaries
        """
        courses = Course.query.filter_by(user_id=user_id).order_by(Course.created_at.desc()).all()
        return [course.to_dict() for course in courses]
    
    @staticmethod
    def get_course_by_id(course_id: int, user_id: int):
        """
        Get a single course by ID
        
        Args:
            course_id (int): Course ID
            user_id (int): User ID (for authorization)
            
        Returns:
            dict: Course dictionary or None
        """
        course = Course.query.filter_by(course_id=course_id, user_id=user_id).first()
        return course.to_dict() if course else None
    
    @staticmethod
    def update_course(course_id: int, user_id: int, **kwargs):
        """
        Update course information
        
        Args:
            course_id (int): Course ID
            user_id (int): User ID (for authorization)
            **kwargs: Fields to update
            
        Returns:
            tuple: (course_dict, error_message)
        """
        course = Course.query.filter_by(course_id=course_id, user_id=user_id).first()
        
        if not course:
            return None, "Course not found"
        
        try:
            # Update fields if provided
            if 'course_name' in kwargs and kwargs['course_name']:
                course.course_name = kwargs['course_name'].strip()
            
            if 'course_code' in kwargs:
                course.course_code = kwargs['course_code'].strip() if kwargs['course_code'] else None
            
            if 'credit_hours' in kwargs:
                if kwargs['credit_hours'] is not None and (kwargs['credit_hours'] < 0 or kwargs['credit_hours'] > 20):
                    return None, "Credit hours must be between 0 and 20"
                course.credit_hours = kwargs['credit_hours']
            
            if 'instructor' in kwargs:
                course.instructor = kwargs['instructor'].strip() if kwargs['instructor'] else None
            
            if 'color' in kwargs:
                if kwargs['color'] and not kwargs['color'].startswith('#'):
                    return None, "Color must be in hex format"
                course.color = kwargs['color']
            
            if 'schedule' in kwargs:
                course.schedule = kwargs['schedule']
            
            if 'topics' in kwargs:
                course.topics = kwargs['topics']
            
            db.session.commit()
            return course.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update course: {str(e)}"
    
    @staticmethod
    def delete_course(course_id: int, user_id: int):
        """
        Delete a course
        
        Args:
            course_id (int): Course ID
            user_id (int): User ID (for authorization)
            
        Returns:
            tuple: (success: bool, error_message)
        """
        course = Course.query.filter_by(course_id=course_id, user_id=user_id).first()
        
        if not course:
            return False, "Course not found"
        
        # Check if course has active tasks
        active_tasks = Task.query.filter_by(course_id=course_id, status='pending').count()
        if active_tasks > 0:
            return False, f"Cannot delete course with {active_tasks} active task(s). Complete or delete tasks first."
        
        try:
            db.session.delete(course)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete course: {str(e)}"
    
    @staticmethod
    def get_total_credit_hours(user_id: int):
        """
        Calculate total credit hours for user
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Total credit hours
        """
        total = db.session.query(func.sum(Course.credit_hours)).filter_by(user_id=user_id).scalar()
        return total if total else 0
