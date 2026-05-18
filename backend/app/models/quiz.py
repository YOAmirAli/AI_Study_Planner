"""
Quiz Model - 3NF Normalized
Stores AI-generated quizzes for tasks
"""

from app.config.database import db
from datetime import datetime

class Quiz(db.Model):
    """
    Quiz Model - Normalized to 3NF
    
    Represents a quiz generated for a completed task
    
    3NF Compliance:
    - 1NF: All attributes are atomic
    - 2NF: No partial dependencies
    - 3NF: No transitive dependencies
    """
    __tablename__ = 'quizzes'
    
    # Primary Key
    quiz_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.task_id', ondelete='CASCADE'), nullable=False, index=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.course_id', ondelete='SET NULL'), nullable=True, index=True)
    
    # Quiz Information
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    total_questions = db.Column(db.Integer, nullable=False)
    
    # Quiz Status: 'pending', 'in_progress', 'completed'
    status = db.Column(db.String(20), nullable=False, default='pending', index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    started_at = db.Column(db.DateTime, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    questions = db.relationship('QuizQuestion', backref='quiz', lazy=True, cascade='all, delete-orphan')
    result = db.relationship('QuizResult', backref='quiz', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Quiz {self.title}>'
    
    def to_dict(self, include_questions=False, include_result=False, include_answers=False):
        """Convert quiz object to dictionary"""
        quiz_dict = {
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'task_id': self.task_id,
            'course_id': self.course_id,
            'title': self.title,
            'description': self.description,
            'total_questions': self.total_questions,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
        
        # Include course details
        if self.course_id:
            from app.models.course import Course
            course = Course.query.get(self.course_id)
            if course:
                quiz_dict['course'] = {
                    'course_id': course.course_id,
                    'course_name': course.course_name,
                    'course_code': course.course_code,
                    'color': course.color
                }
        
        # Include questions if requested
        if include_questions:
            quiz_dict['questions'] = [q.to_dict(include_answer=include_answers) for q in self.questions]
        
        # Include result if requested
        if include_result and self.result:
            quiz_dict['result'] = self.result.to_dict()
        
        return quiz_dict


class QuizQuestion(db.Model):
    """
    Quiz Question Model - Normalized to 3NF
    
    Stores individual questions for a quiz
    """
    __tablename__ = 'quiz_questions'
    
    # Primary Key
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Question Information
    question_number = db.Column(db.Integer, nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(500), nullable=False)
    option_b = db.Column(db.String(500), nullable=False)
    option_c = db.Column(db.String(500), nullable=False)
    option_d = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', or 'D'
    explanation = db.Column(db.Text, nullable=True)
    
    # User's answer (filled when quiz is taken)
    user_answer = db.Column(db.String(1), nullable=True)
    is_correct = db.Column(db.Boolean, nullable=True)
    
    def __repr__(self):
        return f'<QuizQuestion {self.question_number}>'
    
    def to_dict(self, include_answer=False):
        """Convert question object to dictionary"""
        question_dict = {
            'question_id': self.question_id,
            'quiz_id': self.quiz_id,
            'question_number': self.question_number,
            'question_text': self.question_text,
            'option_a': self.option_a,
            'option_b': self.option_b,
            'option_c': self.option_c,
            'option_d': self.option_d,
            'user_answer': self.user_answer,
            'is_correct': self.is_correct
        }
        
        # Only include correct answer and explanation after quiz is completed
        if include_answer:
            question_dict['correct_answer'] = self.correct_answer
            question_dict['explanation'] = self.explanation
        
        return question_dict


class QuizResult(db.Model):
    """
    Quiz Result Model - Normalized to 3NF
    
    Stores the result of a completed quiz
    """
    __tablename__ = 'quiz_results'
    
    # Primary Key
    result_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Foreign Keys (One-to-One with Quiz)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.quiz_id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False, index=True)
    
    # Result Information
    score = db.Column(db.Integer, nullable=False)  # Number of correct answers
    total_questions = db.Column(db.Integer, nullable=False)
    percentage = db.Column(db.Float, nullable=False)
    time_taken = db.Column(db.Integer, nullable=True)  # Time in seconds
    
    # Timestamp
    completed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<QuizResult {self.score}/{self.total_questions}>'
    
    def to_dict(self):
        """Convert result object to dictionary"""
        return {
            'result_id': self.result_id,
            'quiz_id': self.quiz_id,
            'user_id': self.user_id,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': self.percentage,
            'time_taken': self.time_taken,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }
