from app.models.notification import Notification
from app.models.task import Task
from app.models.user import User
from app.config.database import db
from datetime import datetime, timedelta
from sqlalchemy import and_

class NotificationService:
    """Notification management service"""
    
    @staticmethod
    def create_notification(user_id: int, notification_type: str, title: str, 
                          message: str, task_id: int = None, group_id: int = None):
        """
        Create a new notification
        Args:
            user_id (int): User ID
            notification_type (str): Type of notification
            title (str): Notification title
            message (str): Notification message
            task_id (int, optional): Related task ID
            group_id (int, optional): Related group ID
        Returns:
            tuple: (notification_dict, error_message)
        """
        try:
            # Validate notification type
            valid_types = ['deadline_reminder', 'overdue_alert', 'falling_behind', 
                          'study_reminder', 'group_activity']
            if notification_type not in valid_types:
                return None, f"Invalid notification type. Must be one of: {', '.join(valid_types)}"
            
            # Create notification
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                task_id=task_id,
                group_id=group_id
            )
            
            db.session.add(notification)
            db.session.commit()
            
            return notification.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create notification: {str(e)}"
    
    @staticmethod
    def get_user_notifications(user_id: int, unread_only: bool = False, limit: int = 50):
        """
        Get user notifications
        Args:
            user_id (int): User ID
            unread_only (bool): Only return unread notifications
            limit (int): Maximum number of notifications
        Returns:
            list: List of notifications
        """
        query = Notification.query.filter_by(user_id=user_id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
        return [notification.to_dict() for notification in notifications]
    
    @staticmethod
    def mark_notification_read(notification_id: int, user_id: int):
        """
        Mark notification as read
        Args:
            notification_id (int): Notification ID
            user_id (int): User ID (for authorization)
        Returns:
            tuple: (success: bool, error_message)
        """
        try:
            notification = Notification.query.filter_by(
                notification_id=notification_id, 
                user_id=user_id
            ).first()
            
            if not notification:
                return False, "Notification not found"
            
            notification.mark_as_read()
            return True, None
            
        except Exception as e:
            return False, f"Failed to mark notification as read: {str(e)}"
    
    @staticmethod
    def mark_all_read(user_id: int):
        """
        Mark all notifications as read for user
        Args:
            user_id (int): User ID
        Returns:
            tuple: (count: int, error_message)
        """
        try:
            notifications = Notification.query.filter_by(
                user_id=user_id, 
                is_read=False
            ).all()
            
            count = 0
            for notification in notifications:
                notification.mark_as_read()
                count += 1
            
            return count, None
            
        except Exception as e:
            return 0, f"Failed to mark notifications as read: {str(e)}"
    
    @staticmethod
    def delete_notification(notification_id: int, user_id: int):
        """
        Delete a notification
        Args:
            notification_id (int): Notification ID
            user_id (int): User ID (for authorization)
        Returns:
            tuple: (success: bool, error_message)
        """
        try:
            notification = Notification.query.filter_by(
                notification_id=notification_id,
                user_id=user_id
            ).first()
            
            if not notification:
                return False, "Notification not found"
            
            db.session.delete(notification)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete notification: {str(e)}"
    
    @staticmethod
    def clear_all_read(user_id: int):
        """
        Clear all read notifications for user
        Args:
            user_id (int): User ID
        Returns:
            tuple: (count: int, error_message)
        """
        try:
            notifications = Notification.query.filter_by(
                user_id=user_id,
                is_read=True
            ).all()
            
            count = len(notifications)
            for notification in notifications:
                db.session.delete(notification)
            
            db.session.commit()
            return count, None
            
        except Exception as e:
            db.session.rollback()
            return 0, f"Failed to clear notifications: {str(e)}"
    
    @staticmethod
    def delete_old_notifications(days_old: int = 30):
        """
        Delete notifications older than specified days
        Args:
            days_old (int): Delete notifications older than this many days
        Returns:
            int: Number of notifications deleted
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days_old)
            old_notifications = Notification.query.filter(
                Notification.created_at < cutoff_date
            ).all()
            
            count = len(old_notifications)
            for notification in old_notifications:
                db.session.delete(notification)
            
            db.session.commit()
            return count
            
        except Exception as e:
            db.session.rollback()
            return 0
    
    @staticmethod
    def create_deadline_reminders():
        """
        Create deadline reminder notifications for tasks due in 24-48 hours
        Returns:
            int: Number of reminders created
        """
        try:
            now = datetime.utcnow()
            tomorrow = now + timedelta(days=1)
            day_after = now + timedelta(days=2)
            
            # Find tasks due in 24-48 hours that don't have reminders yet
            upcoming_tasks = Task.query.filter(
                and_(
                    Task.deadline >= tomorrow,
                    Task.deadline <= day_after,
                    Task.status != 'completed'
                )
            ).all()
            
            reminders_created = 0
            for task in upcoming_tasks:
                # Check if reminder already exists
                existing = Notification.query.filter_by(
                    user_id=task.user_id,
                    type='deadline_reminder',
                    task_id=task.task_id
                ).first()
                
                if not existing:
                    hours_until = int((task.deadline - now).total_seconds() / 3600)
                    NotificationService.create_notification(
                        user_id=task.user_id,
                        notification_type='deadline_reminder',
                        title=f'Deadline Reminder: {task.title}',
                        message=f'Your task "{task.title}" is due in {hours_until} hours.',
                        task_id=task.task_id
                    )
                    reminders_created += 1
            
            return reminders_created
            
        except Exception as e:
            return 0
    
    @staticmethod
    def create_overdue_alerts():
        """
        Create overdue alert notifications for tasks past deadline
        Returns:
            int: Number of alerts created
        """
        try:
            now = datetime.utcnow()
            
            # Find overdue tasks
            overdue_tasks = Task.query.filter(
                and_(
                    Task.deadline < now,
                    Task.status != 'completed'
                )
            ).all()
            
            alerts_created = 0
            for task in overdue_tasks:
                # Check if alert already exists (only create once per day)
                today = datetime.utcnow().date()
                existing = Notification.query.filter(
                    and_(
                        Notification.user_id == task.user_id,
                        Notification.type == 'overdue_alert',
                        Notification.task_id == task.task_id,
                        Notification.created_at >= datetime.combine(today, datetime.min.time())
                    )
                ).first()
                
                if not existing:
                    days_overdue = (now - task.deadline).days
                    NotificationService.create_notification(
                        user_id=task.user_id,
                        notification_type='overdue_alert',
                        title=f'Overdue: {task.title}',
                        message=f'Your task "{task.title}" is {days_overdue} days overdue.',
                        task_id=task.task_id
                    )
                    alerts_created += 1
            
            return alerts_created
            
        except Exception as e:
            return 0
