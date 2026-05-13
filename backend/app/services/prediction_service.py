from app.models.task import Task
from app.models.analytics import Analytics
from app.config.database import db
from datetime import datetime, timedelta, date
from sqlalchemy import and_, func

class PredictionService:
    """Falling behind prediction service"""
    
    @staticmethod
    def detect_falling_behind(user_id: int, expected_hours_per_week: int = 20):
        """
        Detect if student is falling behind using rule-based algorithm
        
        Algorithm:
        1. Calculate metrics (completion rate, upcoming deadlines, study hours)
        2. Apply detection rules
        3. Calculate severity (low, medium, high)
        4. Generate reasons and suggestions
        
        Args:
            user_id (int): User ID
            expected_hours_per_week (int): Expected study hours per week
            
        Returns:
            dict: Prediction result with flag, severity, reasons, suggestions
        """
        # Step 1: Calculate metrics
        metrics = PredictionService._calculate_metrics(user_id, expected_hours_per_week)
        
        # Step 2: Apply detection rules
        flags = []
        reasons = []
        suggestions = []
        
        # Rule 1: Low completion rate
        if metrics['completion_rate'] < 50:
            flags.append('low_completion_rate')
            reasons.append(f"Task completion rate is {metrics['completion_rate']:.1f}% (below 50%)")
            suggestions.append("Focus on completing pending tasks before taking on new ones")
        
        # Rule 2: Too many upcoming deadlines
        if metrics['upcoming_deadlines'] > 5:
            flags.append('many_upcoming_deadlines')
            reasons.append(f"{metrics['upcoming_deadlines']} tasks due in the next 7 days")
            suggestions.append("Prioritize tasks by deadline and break them into smaller chunks")
        
        # Rule 3: Insufficient study hours
        if metrics['study_hours_this_week'] < (expected_hours_per_week * 0.5):
            flags.append('insufficient_study_hours')
            reasons.append(f"Only {metrics['study_hours_this_week']:.1f} hours studied this week (expected: {expected_hours_per_week})")
            suggestions.append(f"Increase daily study time to meet the {expected_hours_per_week} hours/week goal")
        
        # Step 3: Calculate severity
        num_conditions = len(flags)
        if num_conditions == 0:
            severity = 'none'
            is_falling_behind = False
        elif num_conditions == 1:
            severity = 'low'
            is_falling_behind = True
        elif num_conditions == 2:
            severity = 'medium'
            is_falling_behind = True
        else:
            severity = 'high'
            is_falling_behind = True
        
        # Add general suggestions if falling behind
        if is_falling_behind:
            suggestions.append("Use the AI schedule generator to optimize your study time")
            suggestions.append("Consider using AI tools to summarize materials and create flashcards")
        
        return {
            'is_falling_behind': is_falling_behind,
            'severity': severity,
            'conditions_met': num_conditions,
            'flags': flags,
            'reasons': reasons,
            'suggestions': suggestions,
            'metrics': metrics
        }
    
    @staticmethod
    def _calculate_metrics(user_id: int, expected_hours: int):
        """
        Calculate metrics for prediction
        
        Args:
            user_id (int): User ID
            expected_hours (int): Expected hours per week
            
        Returns:
            dict: Calculated metrics
        """
        # Completion rate
        total_tasks = Task.query.filter_by(user_id=user_id).count()
        completed_tasks = Task.query.filter_by(user_id=user_id, status='completed').count()
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 100
        
        # Upcoming deadlines (next 7 days)
        now = datetime.utcnow()
        next_week = now + timedelta(days=7)
        upcoming_deadlines = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status != 'completed',
                Task.deadline >= now,
                Task.deadline <= next_week
            )
        ).count()
        
        # Study hours this week
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        study_hours_this_week = db.session.query(func.sum(Analytics.hours_spent)).filter(
            and_(
                Analytics.user_id == user_id,
                Analytics.session_date >= week_start,
                Analytics.session_date <= week_end
            )
        ).scalar() or 0
        
        return {
            'completion_rate': round(completion_rate, 2),
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'upcoming_deadlines': upcoming_deadlines,
            'study_hours_this_week': float(study_hours_this_week),
            'expected_hours_per_week': expected_hours
        }
