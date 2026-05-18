"""
Quiz Service
Handles all quiz-related business logic
"""

from app.models.quiz import Quiz, QuizQuestion, QuizResult
from app.config.database import db
from datetime import datetime

class QuizService:
    """Quiz management service"""
    
    @staticmethod
    def create_quiz(user_id: int, task_id: int, course_id: int, title: str, 
                   questions_data: list, description: str = None):
        """
        Create a new quiz with questions
        
        Args:
            user_id (int): User ID
            task_id (int): Task ID
            course_id (int): Course ID
            title (str): Quiz title
            questions_data (list): List of question dictionaries
            description (str, optional): Quiz description
            
        Returns:
            tuple: (quiz_dict, error_message)
        """
        try:
            # Create quiz
            new_quiz = Quiz(
                user_id=user_id,
                task_id=task_id,
                course_id=course_id,
                title=title,
                description=description,
                total_questions=len(questions_data),
                status='pending'
            )
            
            db.session.add(new_quiz)
            db.session.flush()  # Get quiz_id
            
            # Create questions
            for q_data in questions_data:
                question = QuizQuestion(
                    quiz_id=new_quiz.quiz_id,
                    question_number=q_data['question_number'],
                    question_text=q_data['question_text'],
                    option_a=q_data['option_a'],
                    option_b=q_data['option_b'],
                    option_c=q_data['option_c'],
                    option_d=q_data['option_d'],
                    correct_answer=q_data['correct_answer'],
                    explanation=q_data.get('explanation', '')
                )
                db.session.add(question)
            
            db.session.commit()
            return new_quiz.to_dict(include_questions=False), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create quiz: {str(e)}"
    
    @staticmethod
    def get_user_quizzes(user_id: int, status: str = None):
        """
        Get all quizzes for a user
        
        Args:
            user_id (int): User ID
            status (str, optional): Filter by status
            
        Returns:
            list: List of quiz dictionaries
        """
        query = Quiz.query.filter_by(user_id=user_id)
        
        if status:
            query = query.filter_by(status=status)
        
        quizzes = query.order_by(Quiz.created_at.desc()).all()
        return [quiz.to_dict(include_result=True) for quiz in quizzes]
    
    @staticmethod
    def get_quiz_by_id(quiz_id: int, user_id: int, include_answers: bool = False):
        """
        Get a single quiz by ID
        
        Args:
            quiz_id (int): Quiz ID
            user_id (int): User ID (for authorization)
            include_answers (bool): Include correct answers
            
        Returns:
            dict: Quiz dictionary or None
        """
        quiz = Quiz.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        
        if not quiz:
            return None
        
        # Include answers if explicitly requested or if the quiz is already completed
        should_include = include_answers or quiz.status == 'completed'
        
        quiz_dict = quiz.to_dict(include_questions=True, include_result=True, include_answers=should_include)
        
        return quiz_dict
    
    @staticmethod
    def start_quiz(quiz_id: int, user_id: int):
        """
        Start a quiz (update status to in_progress)
        
        Args:
            quiz_id (int): Quiz ID
            user_id (int): User ID
            
        Returns:
            tuple: (quiz_dict, error_message)
        """
        quiz = Quiz.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        
        if not quiz:
            return None, "Quiz not found"
        
        if quiz.status != 'pending':
            return None, "Quiz already started or completed"
        
        try:
            quiz.status = 'in_progress'
            quiz.started_at = datetime.utcnow()
            db.session.commit()
            
            return quiz.to_dict(include_questions=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to start quiz: {str(e)}"
    
    @staticmethod
    def submit_quiz(quiz_id: int, user_id: int, answers: dict, time_taken: int = None):
        """
        Submit quiz answers and calculate score
        
        Args:
            quiz_id (int): Quiz ID
            user_id (int): User ID
            answers (dict): Dictionary of {question_id: user_answer}
            time_taken (int, optional): Time taken in seconds
            
        Returns:
            tuple: (result_dict, error_message)
        """
        quiz = Quiz.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        
        if not quiz:
            return None, "Quiz not found"
        
        if quiz.status == 'completed':
            return None, "Quiz already completed"
        
        try:
            score = 0
            total_questions = len(quiz.questions)
            
            # Grade each question
            for question in quiz.questions:
                user_answer = answers.get(str(question.question_id), '').upper()
                question.user_answer = user_answer
                question.is_correct = (user_answer == question.correct_answer)
                
                if question.is_correct:
                    score += 1
            
            # Calculate percentage
            percentage = (score / total_questions * 100) if total_questions > 0 else 0
            
            # Create result
            result = QuizResult(
                quiz_id=quiz.quiz_id,
                user_id=user_id,
                score=score,
                total_questions=total_questions,
                percentage=round(percentage, 2),
                time_taken=time_taken
            )
            
            # Update quiz status
            quiz.status = 'completed'
            quiz.completed_at = datetime.utcnow()
            
            db.session.add(result)
            db.session.commit()
            
            return result.to_dict(), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to submit quiz: {str(e)}"
    
    @staticmethod
    def get_pending_count(user_id: int):
        """
        Get count of pending quizzes
        
        Args:
            user_id (int): User ID
            
        Returns:
            int: Count of pending quizzes
        """
        return Quiz.query.filter_by(user_id=user_id, status='pending').count()
    
    @staticmethod
    def delete_quiz(quiz_id: int, user_id: int):
        """
        Delete a quiz
        
        Args:
            quiz_id (int): Quiz ID
            user_id (int): User ID
            
        Returns:
            tuple: (success, error_message)
        """
        quiz = Quiz.query.filter_by(quiz_id=quiz_id, user_id=user_id).first()
        
        if not quiz:
            return False, "Quiz not found"
        
        try:
            db.session.delete(quiz)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete quiz: {str(e)}"
