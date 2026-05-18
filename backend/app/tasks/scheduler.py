"""
Job Scheduler Configuration
Sets up APScheduler for automated notification jobs
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.tasks.cron_jobs import NotificationJobs
import atexit

class JobScheduler:
    """Job scheduler for automated tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Setup all scheduled jobs"""
        # Daily deadline check - 8:00 AM every day
        self.scheduler.add_job(
            func=NotificationJobs.daily_deadline_check,
            trigger=CronTrigger(hour=8, minute=0),
            id='daily_deadline_check',
            name='Daily Deadline Check',
            replace_existing=True
        )
        
        # Daily overdue check - 9:00 AM every day
        self.scheduler.add_job(
            func=NotificationJobs.daily_overdue_check,
            trigger=CronTrigger(hour=9, minute=0),
            id='daily_overdue_check',
            name='Daily Overdue Check',
            replace_existing=True
        )
        
        # Daily falling behind check - 10:00 AM every day
        self.scheduler.add_job(
            func=NotificationJobs.daily_falling_behind_check,
            trigger=CronTrigger(hour=10, minute=0),
            id='daily_falling_behind_check',
            name='Daily Falling Behind Check',
            replace_existing=True
        )
        
        # Weekly cleanup - 2:00 AM every Sunday
        self.scheduler.add_job(
            func=NotificationJobs.weekly_cleanup,
            trigger=CronTrigger(day_of_week='sun', hour=2, minute=0),
            id='weekly_cleanup',
            name='Weekly Cleanup',
            replace_existing=True
        )
    
    def start(self):
        """Start the scheduler"""
        try:
            self.scheduler.start()
            print("[OK] Job scheduler started successfully")
            
            # Print scheduled jobs
            jobs = self.scheduler.get_jobs()
            print(f"[OK] {len(jobs)} scheduled jobs loaded:")
            for job in jobs:
                print(f"  - {job.name} (ID: {job.id})")
            
            # Shutdown scheduler when app exits
            atexit.register(lambda: self.scheduler.shutdown())
        except Exception as e:
            print(f"Failed to start job scheduler: {e}")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("[OK] Job scheduler stopped")
    
    def get_jobs(self):
        """Get list of scheduled jobs"""
        return self.scheduler.get_jobs()

# Global scheduler instance
scheduler = None

def init_scheduler():
    """Initialize the global scheduler"""
    global scheduler
    if scheduler is None:
        scheduler = JobScheduler()
        scheduler.start()
    return scheduler

def get_scheduler():
    """Get the global scheduler instance"""
    return scheduler
