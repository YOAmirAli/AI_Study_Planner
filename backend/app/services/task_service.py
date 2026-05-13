from app.models.task import Task
from app.models.course import Course
from app.config.database import db
from datetime import datetime, timedelta
from sqlalchemy import and_, or_

class TaskService:
    """Task management service"""
    
    @staticmethod
    def create_task(user_id: int, course_id: int, title: str, deadline: str,
                   priority: str = 'medium', description: str = None,
                   estimated_time: int = None):
        """
        Create a new task
        
        Args:
            user_id (int): User ID
            course_id (int): Course ID
            title (str): Task title
            deadline (str): Deadline (ISO format)
            priority (str): Priority level
            description (str, optional): Task description
            estimated_time (int, optional): Estimated time in minutes
            
        Returns:
            tuple: (task_dict, error_message)
        """
        # Validate required fields
        if not title or not title.strip():
            return None, "Task title is required"
        
        if not deadline:
            return None, "Deadline is required"
        
        # Verify course exists and belongs to user
        course = Course.query.filter_by(course_id=course_id, user_id=user_id).first()
        if not course:
            return None, "Course not found"
        
        # Parse and validate deadline
        try:
            deadline_dt = datetime.fromisoformat(deadline.replace('Z', '+00:00'))
            if deadline_dt < datetime.utcnow():
                return None, "Deadline must be in the future"
        except ValueError:
            return None, "Invalid deadline format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"
        
        # Validate priority
        if priority not in ['high', 'medium', 'low']:
            return None, "Priority must be 'high', 'medium', or 'low'"
        
        try:
            new_task = Task(
                user_id=user_id,
                course_id=course_id,
                title=title.strip(),
                description=description.strip() if description else None,
                deadline=deadline_dt,
                priority=priority,
                status='pending',
                estimated_time=estimated_time
            )
            
            db.session.add(new_task)
            db.session.commit()
            
            return new_task.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create task: {str(e)}"
    
    @staticmethod
    def get_user_tasks(user_id: int, status: str = None, priority: str = None,
                      course_id: int = None, sort_by: str = 'deadline'):
        """
        Get tasks with filters and sorting
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by status
            priority (str, optional): Filter by priority
            course_id (int, optional): Filter by course
            sort_by (str): Sort field (deadline, priority, created_at)
            
        Returns:
            list: List of task dictionaries
        """
        query = Task.query.filter_by(user_id=user_id)
        
        # Apply filters
        if status:
            query = query.filter_by(status=status)
        
        if priority:
            query = query.filter_by(priority=priority)
        
        if course_id:
            query = query.filter_by(course_id=course_id)
        
        # Apply sorting
        if sort_by == 'deadline':
            query = query.order_by(Task.deadline.asc())
        elif sort_by == 'priority':
            # Custom priority order: high > medium > low
            query = query.order_by(
                db.case(
                    (Task.priority == 'high', 1),
                    (Task.priority == 'medium', 2),
                    (Task.priority == 'low', 3)
                )
            )
        elif sort_by == 'created_at':
            query = query.order_by(Task.created_at.desc())
        
        tasks = query.all()
        return [task.to_dict(include_course=True) for task in tasks]
    
    @staticmethod
    def get_task_by_id(task_id: int, user_id: int):
        """
        Get a single task by ID
        
        Args:
            task_id (int): Task ID
            user_id (int): User ID (for authorization)
            
        Returns:
            dict: Task dictionary or None
        """
        task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
        return task.to_dict(include_course=True) if task else None
    
    @staticmethod
    def update_task(task_id: int, user_id: int, **kwargs):
        """
        Update task information
        
        Args:
            task_id (int): Task ID
            user_id (int): User ID (for authorization)
            **kwargs: Fields to update
            
        Returns:
            tuple: (task_dict, error_message)
        """
        task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
        
        if not task:
            return None, "Task not found"
        
        try:
            if 'title' in kwargs and kwargs['title']:
                task.title = kwargs['title'].strip()
            
            if 'description' in kwargs:
                task.description = kwargs['description'].strip() if kwargs['description'] else None
            
            if 'deadline' in kwargs:
                deadline_dt = datetime.fromisoformat(kwargs['deadline'].replace('Z', '+00:00'))
                task.deadline = deadline_dt
            
            if 'priority' in kwargs and kwargs['priority'] in ['high', 'medium', 'low']:
                task.priority = kwargs['priority']
            
            if 'status' in kwargs and kwargs['status'] in ['pending', 'in_progress', 'completed']:
                task.status = kwargs['status']
                if kwargs['status'] == 'completed' and not task.completed_at:
                    task.completed_at = datetime.utcnow()
            
            if 'estimated_time' in kwargs:
                task.estimated_time = kwargs['estimated_time']
            
            if 'actual_time' in kwargs:
                task.actual_time = kwargs['actual_time']
            
            db.session.commit()
            return task.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update task: {str(e)}"
    
    @staticmethod
    def complete_task(task_id: int, user_id: int, actual_time: int = None):
        """
        Mark task as completed
        
        Args:
            task_id (int): Task ID
            user_id (int): User ID
            actual_time (int, optional): Actual time spent in minutes
            
        Returns:
            tuple: (task_dict, error_message)
        """
        task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
        
        if not task:
            return None, "Task not found"
        
        try:
            task.status = 'completed'
            task.completed_at = datetime.utcnow()
            if actual_time:
                task.actual_time = actual_time
            
            db.session.commit()
            return task.to_dict(include_course=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to complete task: {str(e)}"
    
    @staticmethod
    def delete_task(task_id: int, user_id: int):
        """
        Delete a task
        
        Args:
            task_id (int): Task ID
            user_id (int): User ID (for authorization)
            
        Returns:
            tuple: (success: bool, error_message)
        """
        task = Task.query.filter_by(task_id=task_id, user_id=user_id).first()
        
        if not task:
            return False, "Task not found"
        
        try:
            db.session.delete(task)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete task: {str(e)}"
    
    @staticmethod
    def get_upcoming_tasks(user_id: int, days: int = 7):
        """
        Get tasks due in the next N days
        
        Args:
            user_id (int): User ID
            days (int): Number of days to look ahead
            
        Returns:
            list: List of upcoming tasks
        """
        now = datetime.utcnow()
        future = now + timedelta(days=days)
        
        tasks = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status != 'completed',
                Task.deadline >= now,
                Task.deadline <= future
            )
        ).order_by(Task.deadline.asc()).all()
        
        return [task.to_dict(include_course=True) for task in tasks]
    
    @staticmethod
    def get_overdue_tasks(user_id: int):
        """
        Get overdue tasks
        
        Args:
            user_id (int): User ID
            
        Returns:
            list: List of overdue tasks
        """
        now = datetime.utcnow()
        
        tasks = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status != 'completed',
                Task.deadline < now
            )
        ).order_by(Task.deadline.asc()).all()
        
        return [task.to_dict(include_course=True) for task in tasks]
    
    @staticmethod
    def get_task_statistics(user_id: int):
        """
        Get task statistics for user
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Task statistics
        """
        total = Task.query.filter_by(user_id=user_id).count()
        completed = Task.query.filter_by(user_id=user_id, status='completed').count()
        pending = Task.query.filter_by(user_id=user_id, status='pending').count()
        in_progress = Task.query.filter_by(user_id=user_id, status='in_progress').count()
        
        now = datetime.utcnow()
        overdue = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status != 'completed',
                Task.deadline < now
            )
        ).count()
        
        completion_rate = (completed / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'in_progress': in_progress,
            'overdue': overdue,
            'completion_rate': round(completion_rate, 2)
        }
