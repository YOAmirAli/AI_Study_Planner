"""
Scheduled Jobs for Notifications
Automated tasks that run on schedule to create notifications
"""
from app.services.notification_service import NotificationService
from app.services.prediction_service import PredictionService
from app.models.user import User
from app.models.notification import Notification
from datetime import datetime
from sqlalchemy import and_

class NotificationJobs:
    """Scheduled notification jobs"""
    
    @staticmethod
    def daily_deadline_check():
        """
        Daily job to check for upcoming deadlines
        Runs every day at 8:00 AM
        """
        try:
            print(f"[{datetime.now()}] Running daily deadline check...")
            # Create deadline reminders
            reminders_created = NotificationService.create_deadline_reminders()
            print(f"Created {reminders_created} deadline reminders")
            return reminders_created
        except Exception as e:
            print(f"Error in daily deadline check: {e}")
            return 0
    
    @staticmethod
    def daily_overdue_check():
        """
        Daily job to check for overdue tasks
        Runs every day at 9:00 AM
        """
        try:
            print(f"[{datetime.now()}] Running daily overdue check...")
            # Create overdue alerts
            alerts_created = NotificationService.create_overdue_alerts()
            print(f"Created {alerts_created} overdue alerts")
            return alerts_created
        except Exception as e:
            print(f"Error in daily overdue check: {e}")
            return 0
    
    @staticmethod
    def daily_falling_behind_check():
        """
        Daily job to check if students are falling behind
        Runs every day at 10:00 AM
        """
        try:
            print(f"[{datetime.now()}] Running daily falling behind check...")
            # Get all users
            users = User.query.all()
            alerts_created = 0
            
            for user in users:
                # Run prediction
                prediction = PredictionService.detect_falling_behind(user.user_id)
                
                if prediction['is_falling_behind'] and prediction['severity'] in ['medium', 'high']:
                    # Check if alert already exists today
                    today = datetime.utcnow().date()
                    existing = Notification.query.filter(
                        and_(
                            Notification.user_id == user.user_id,
                            Notification.type == 'falling_behind',
                            Notification.created_at >= datetime.combine(today, datetime.min.time())
                        )
                    ).first()
                    
                    if not existing:
                        # Create falling behind notification
                        severity_emoji = {'medium': '⚠️', 'high': '🚨'}
                        message = f"You are falling behind with {prediction['severity']} severity. "
                        message += f"Reasons: {', '.join(prediction['reasons'][:2])}"
                        
                        NotificationService.create_notification(
                            user_id=user.user_id,
                            notification_type='falling_behind',
                            title=f"{severity_emoji.get(prediction['severity'], '⚠️')} Falling Behind Alert",
                            message=message
                        )
                        alerts_created += 1
            
            print(f"Created {alerts_created} falling behind alerts")
            return alerts_created
        except Exception as e:
            print(f"Error in daily falling behind check: {e}")
            return 0
    
    @staticmethod
    def weekly_cleanup():
        """
        Weekly job to clean up old notifications
        Runs every Sunday at 2:00 AM
        """
        try:
            print(f"[{datetime.now()}] Running weekly cleanup...")
            # Delete notifications older than 30 days
            deleted_count = NotificationService.delete_old_notifications(days_old=30)
            print(f"Deleted {deleted_count} old notifications")
            return deleted_count
        except Exception as e:
            print(f"Error in weekly cleanup: {e}")
            return 0
