from app.models.analytics import Analytics
from app.models.task import Task
from app.models.course import Course
from app.models.quiz import Quiz, QuizResult
from app.config.database import db
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_

class AnalyticsService:
    """Analytics and progress tracking service"""
    
    @staticmethod
    def log_study_session(user_id: int, course_id: int = None, task_id: int = None,
                         session_date: str = None, hours_spent: float = 0, notes: str = None):
        """
        Log a study session
        
        Args:
            user_id (int): User ID
            course_id (int, optional): Course ID
            task_id (int, optional): Task ID
            session_date (str): Session date (YYYY-MM-DD)
            hours_spent (float): Hours spent studying
            notes (str, optional): Session notes
            
        Returns:
            tuple: (session_dict, error_message)
        """
        try:
            # Validate hours
            if hours_spent <= 0 or hours_spent > 24:
                return None, "Hours spent must be between 0 and 24"
            
            # Parse date
            if session_date:
                sess_date = datetime.fromisoformat(session_date).date()
            else:
                sess_date = date.today()
            
            # Create analytics record
            session = Analytics(
                user_id=user_id,
                course_id=course_id,
                task_id=task_id,
                session_date=sess_date,
                hours_spent=hours_spent,
                notes=notes
            )
            
            db.session.add(session)
            db.session.commit()
            
            return session.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to log session: {str(e)}"
    
    @staticmethod
    def get_dashboard_stats(user_id: int):
        """
        Get dashboard statistics
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Dashboard statistics
        """
        # Total courses
        total_courses = Course.query.filter_by(user_id=user_id).count()
        
        # Task statistics
        total_tasks = Task.query.filter_by(user_id=user_id).count()
        completed_tasks = Task.query.filter_by(user_id=user_id, status='completed').count()
        pending_tasks = Task.query.filter_by(user_id=user_id, status='pending').count()
        
        # Overdue tasks
        now = datetime.utcnow()
        overdue_tasks = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status != 'completed',
                Task.deadline < now
            )
        ).count()
        
        # Completion rate
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
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
        
        # Quiz statistics
        total_quizzes = Quiz.query.filter_by(user_id=user_id).count()
        completed_quizzes = Quiz.query.filter_by(user_id=user_id, status='completed').count()
        pending_quizzes = Quiz.query.filter_by(user_id=user_id, status='pending').count()
        
        # Average quiz score
        avg_score = db.session.query(func.avg(QuizResult.percentage)).join(
            Quiz, Quiz.quiz_id == QuizResult.quiz_id
        ).filter(Quiz.user_id == user_id).scalar() or 0
        
        # Total quiz time spent (in minutes)
        total_quiz_time = db.session.query(func.sum(QuizResult.time_taken)).join(
            Quiz, Quiz.quiz_id == QuizResult.quiz_id
        ).filter(Quiz.user_id == user_id).scalar() or 0
        
        return {
            'total_courses': total_courses,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'overdue_tasks': overdue_tasks,
            'completion_rate': round(completion_rate, 2),
            'study_hours_this_week': float(study_hours_this_week),
            'total_quizzes': total_quizzes,
            'completed_quizzes': completed_quizzes,
            'pending_quizzes': pending_quizzes,
            'avg_quiz_score': round(float(avg_score), 2),
            'total_quiz_time_minutes': int(total_quiz_time) if total_quiz_time else 0
        }
    
    @staticmethod
    def get_detailed_analytics(user_id: int):
        """
        Get detailed analytics with chart data
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Detailed analytics
        """
        # Get dashboard stats
        stats = AnalyticsService.get_dashboard_stats(user_id)
        
        # Study hours by course (for bar chart)
        hours_by_course = db.session.query(
            Course.course_name,
            Course.color,
            func.sum(Analytics.hours_spent).label('total_hours')
        ).join(Analytics, Analytics.course_id == Course.course_id).filter(
            Analytics.user_id == user_id
        ).group_by(Course.course_id).all()
        
        course_hours = [
            {
                'course_name': row[0],
                'color': row[1],
                'hours': float(row[2]) if row[2] else 0
            }
            for row in hours_by_course
        ]
        
        # Weekly study hours trend (last 8 weeks)
        weekly_trend = []
        for week_offset in range(7, -1, -1):
            week_start = date.today() - timedelta(days=date.today().weekday() + (week_offset * 7))
            week_end = week_start + timedelta(days=6)
            
            hours = db.session.query(func.sum(Analytics.hours_spent)).filter(
                and_(
                    Analytics.user_id == user_id,
                    Analytics.session_date >= week_start,
                    Analytics.session_date <= week_end
                )
            ).scalar() or 0
            
            weekly_trend.append({
                'week_start': week_start.isoformat(),
                'week_end': week_end.isoformat(),
                'hours': float(hours)
            })
        
        # Average study hours per day (last 30 days)
        thirty_days_ago = date.today() - timedelta(days=30)
        total_hours_30d = db.session.query(func.sum(Analytics.hours_spent)).filter(
            and_(
                Analytics.user_id == user_id,
                Analytics.session_date >= thirty_days_ago
            )
        ).scalar() or 0
        
        avg_hours_per_day = float(total_hours_30d) / 30 if total_hours_30d else 0
        
        # Quiz performance by course
        quiz_performance = db.session.query(
            Course.course_name,
            Course.color,
            func.avg(QuizResult.percentage).label('avg_score'),
            func.count(Quiz.quiz_id).label('quiz_count')
        ).join(Quiz, Quiz.course_id == Course.course_id).join(
            QuizResult, QuizResult.quiz_id == Quiz.quiz_id
        ).filter(Quiz.user_id == user_id).group_by(Course.course_id).all()
        
        quiz_by_course = [
            {
                'course_name': row[0],
                'color': row[1],
                'avg_score': round(float(row[2]), 2) if row[2] else 0,
                'quiz_count': row[3]
            }
            for row in quiz_performance
        ]
        
        # Recent quiz scores (last 10 quizzes)
        recent_quizzes = db.session.query(
            Quiz.title,
            QuizResult.percentage,
            QuizResult.score,
            QuizResult.total_questions,
            QuizResult.completed_at
        ).join(QuizResult, QuizResult.quiz_id == Quiz.quiz_id).filter(
            Quiz.user_id == user_id
        ).order_by(QuizResult.completed_at.desc()).limit(10).all()
        
        recent_quiz_scores = [
            {
                'title': row[0],
                'percentage': round(float(row[1]), 2),
                'score': row[2],
                'total_questions': row[3],
                'completed_at': row[4].isoformat() if row[4] else None
            }
            for row in recent_quizzes
        ]
        
        return {
            **stats,
            'hours_by_course': course_hours,
            'weekly_trend': weekly_trend,
            'avg_hours_per_day': round(avg_hours_per_day, 2),
            'quiz_by_course': quiz_by_course,
            'recent_quiz_scores': recent_quiz_scores
        }
    
    @staticmethod
    def get_study_sessions(user_id: int, limit: int = 50):
        """
        Get study session history
        
        Args:
            user_id (int): User ID
            limit (int): Maximum number of sessions
            
        Returns:
            list: Study sessions
        """
        sessions = Analytics.query.filter_by(user_id=user_id).order_by(
            Analytics.session_date.desc()
        ).limit(limit).all()
        
        return [session.to_dict() for session in sessions]
    
    @staticmethod
    def get_weekly_summary(user_id: int):
        """
        Get current week summary
        
        Args:
            user_id (int): User ID
            
        Returns:
            dict: Weekly summary
        """
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)
        
        # Study hours this week
        study_hours = db.session.query(func.sum(Analytics.hours_spent)).filter(
            and_(
                Analytics.user_id == user_id,
                Analytics.session_date >= week_start,
                Analytics.session_date <= week_end
            )
        ).scalar() or 0
        
        # Tasks completed this week
        tasks_completed = Task.query.filter(
            and_(
                Task.user_id == user_id,
                Task.status == 'completed',
                Task.completed_at >= datetime.combine(week_start, datetime.min.time()),
                Task.completed_at <= datetime.combine(week_end, datetime.max.time())
            )
        ).count()
        
        # Study sessions this week
        sessions_count = Analytics.query.filter(
            and_(
                Analytics.user_id == user_id,
                Analytics.session_date >= week_start,
                Analytics.session_date <= week_end
            )
        ).count()
        
        return {
            'week_start': week_start.isoformat(),
            'week_end': week_end.isoformat(),
            'total_study_hours': float(study_hours),
            'tasks_completed': tasks_completed,
            'study_sessions': sessions_count,
            'avg_hours_per_day': round(float(study_hours) / 7, 2)
        }
