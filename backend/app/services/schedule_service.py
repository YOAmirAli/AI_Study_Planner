from app.models.schedule import Schedule
from app.models.task import Task
from app.models.course import Course
from app.config.database import db
from app.ai.schedule_algorithm import ScheduleAlgorithm
from datetime import datetime, timedelta, time, date
from sqlalchemy import and_

class ScheduleService:
    """Schedule management service"""
    
    @staticmethod
    def create_schedule_block(user_id: int, schedule_date: str, start_time: str,
                             end_time: str, block_type: str, title: str = None,
                             task_id: int = None, color: str = None, is_auto_generated: bool = False):
        """
        Create a manual schedule block
        
        Args:
            user_id (int): User ID
            schedule_date (str): Date in ISO format
            start_time (str): Start time in HH:MM format
            end_time (str): End time in HH:MM format
            block_type (str): Type of block (class, study, break)
            title (str, optional): Block title
            task_id (int, optional): Associated task ID
            is_auto_generated (bool): Whether auto-generated
            
        Returns:
            tuple: (schedule_dict, error_message)
        """
        # Validate block type
        if block_type not in ['class', 'study', 'break']:
            return None, "Block type must be 'class', 'study', or 'break'"
        
        try:
            # Parse date and times
            block_date = datetime.fromisoformat(schedule_date).date()
            block_start = datetime.strptime(start_time, '%H:%M').time()
            block_end = datetime.strptime(end_time, '%H:%M').time()
            
            # Validate times
            if block_start >= block_end:
                return None, "Start time must be before end time"
            
            # Check for conflicts
            conflicts = Schedule.query.filter(
                and_(
                    Schedule.user_id == user_id,
                    Schedule.date == block_date,
                    Schedule.start_time < block_end,
                    Schedule.end_time > block_start
                )
            ).all()
            
            if conflicts:
                return None, "Time slot conflicts with existing schedule"
            
            # Create schedule block
            new_block = Schedule(
                user_id=user_id,
                task_id=task_id,
                date=block_date,
                start_time=block_start,
                end_time=block_end,
                block_type=block_type,
                title=title,
                color=color,
                is_auto_generated=is_auto_generated
            )
            
            db.session.add(new_block)
            db.session.commit()
            
            return new_block.to_dict(include_task=True), None
            
        except ValueError as e:
            return None, f"Invalid date/time format: {str(e)}"
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create schedule block: {str(e)}"
    
    @staticmethod
    def get_weekly_schedule(user_id: int, week_start_date: str = None):
        """
        Get schedule for a specific week
        
        Args:
            user_id (int): User ID
            week_start_date (str, optional): Start date of week (ISO format)
            
        Returns:
            dict: Weekly schedule with blocks grouped by date
        """
        # If no date provided, use current week
        if week_start_date:
            start_date = datetime.fromisoformat(week_start_date).date()
        else:
            today = date.today()
            start_date = today - timedelta(days=today.weekday())  # Monday
        
        end_date = start_date + timedelta(days=6)  # Sunday
        
        # Get all schedule blocks for the week
        blocks = Schedule.query.filter(
            and_(
                Schedule.user_id == user_id,
                Schedule.date >= start_date,
                Schedule.date <= end_date
            )
        ).order_by(Schedule.date, Schedule.start_time).all()
        
        # Group blocks by date
        schedule_by_date = {}
        for block in blocks:
            date_str = block.date.isoformat()
            if date_str not in schedule_by_date:
                schedule_by_date[date_str] = []
            schedule_by_date[date_str].append(block.to_dict(include_task=True))
        
        return {
            'week_start': start_date.isoformat(),
            'week_end': end_date.isoformat(),
            'schedule': schedule_by_date,
            'total_blocks': len(blocks)
        }
    
    @staticmethod
    def generate_ai_schedule(user_id: int, week_start_date: str = None,
                            study_hours_per_day: int = 4, course_id: int = None):
        """
        Generate AI-optimized study schedule
        
        Args:
            user_id (int): User ID
            week_start_date (str, optional): Start date of week
            study_hours_per_day (int): Target study hours per day
            course_id (int, optional): Filter tasks by specific course
            
        Returns:
            tuple: (schedule_dict, error_message)
        """
        try:
            # Determine week start date
            if week_start_date:
                start_date = datetime.fromisoformat(week_start_date).date()
            else:
                today = date.today()
                start_date = today - timedelta(days=today.weekday())
            
            # Get pending tasks (optionally filtered by course)
            query = Task.query.filter_by(
                user_id=user_id,
                status='pending'
            )
            
            if course_id:
                query = query.filter_by(course_id=course_id)
            
            tasks = query.all()
            
            if not tasks:
                course_msg = f" for the selected course" if course_id else ""
                return None, f"No pending tasks{course_msg} to schedule"
            
            task_dicts = [task.to_dict(include_course=True) for task in tasks]
            
            # Get existing schedule blocks (classes, manual blocks)
            existing_blocks = Schedule.query.filter(
                and_(
                    Schedule.user_id == user_id,
                    Schedule.date >= start_date,
                    Schedule.date <= start_date + timedelta(days=6)
                )
            ).all()
            
            existing_block_dicts = [block.to_dict() for block in existing_blocks]
            
            # Add class schedules from courses
            courses = Course.query.filter_by(user_id=user_id).all()
            for course in courses:
                if course.schedule:
                    # Parse schedule if it's a string
                    import json
                    schedule_data = course.schedule
                    if isinstance(schedule_data, str):
                        try:
                            schedule_data = json.loads(schedule_data)
                        except:
                            continue
                    
                    # Ensure schedule_data is a list
                    if not isinstance(schedule_data, list):
                        continue
                    
                    for class_time in schedule_data:
                        if not isinstance(class_time, dict):
                            continue
                            
                        day_name = class_time.get('day')
                        if not day_name:
                            continue
                            
                        # Convert day name to date
                        try:
                            day_offset = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                                         'Friday', 'Saturday', 'Sunday'].index(day_name)
                            class_date = start_date + timedelta(days=day_offset)
                            
                            # Parse time strings (HH:MM format) to full ISO format
                            start_time_str = class_time.get('start_time')
                            end_time_str = class_time.get('end_time')
                            
                            if not start_time_str or not end_time_str:
                                continue
                            
                            # Convert to datetime objects for ISO format
                            start_datetime = datetime.strptime(start_time_str, '%H:%M').time()
                            end_datetime = datetime.strptime(end_time_str, '%H:%M').time()
                            
                            existing_block_dicts.append({
                                'date': class_date.isoformat(),
                                'start_time': start_datetime.isoformat(),
                                'end_time': end_datetime.isoformat(),
                                'block_type': 'class'
                            })
                        except (ValueError, IndexError) as e:
                            print(f"Error processing class schedule: {e}")
                            continue
            
            # Generate schedule using AI algorithm
            generated_blocks = ScheduleAlgorithm.generate_schedule(
                user_id=user_id,
                tasks=task_dicts,
                existing_blocks=existing_block_dicts,
                week_start_date=start_date,
                study_hours_per_day=study_hours_per_day
            )
            
            # Delete old auto-generated blocks for this week
            Schedule.query.filter(
                and_(
                    Schedule.user_id == user_id,
                    Schedule.is_auto_generated == True,
                    Schedule.date >= start_date,
                    Schedule.date <= start_date + timedelta(days=6)
                )
            ).delete()
            
            # Save new blocks to database
            saved_blocks = []
            for block_data in generated_blocks:
                # Parse time strings properly
                start_time_str = block_data['start_time']
                end_time_str = block_data['end_time']
                
                # Convert ISO time format (HH:MM:SS) to time object
                start_time_obj = datetime.strptime(start_time_str, '%H:%M:%S').time()
                end_time_obj = datetime.strptime(end_time_str, '%H:%M:%S').time()
                
                new_block = Schedule(
                    user_id=block_data['user_id'],
                    task_id=block_data.get('task_id'),
                    date=datetime.fromisoformat(block_data['date']).date(),
                    start_time=start_time_obj,
                    end_time=end_time_obj,
                    block_type=block_data['block_type'],
                    title=block_data.get('title'),
                    is_auto_generated=block_data['is_auto_generated']
                )
                db.session.add(new_block)
                saved_blocks.append(new_block)
            
            db.session.commit()
            
            return {
                'message': 'Schedule generated successfully',
                'blocks_created': len(saved_blocks),
                'week_start': start_date.isoformat(),
                'schedule': [block.to_dict(include_task=True) for block in saved_blocks]
            }, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to generate schedule: {str(e)}"
    
    @staticmethod
    def update_schedule_block(schedule_id: int, user_id: int, **kwargs):
        """
        Update schedule block
        
        Args:
            schedule_id (int): Schedule ID
            user_id (int): User ID (for authorization)
            **kwargs: Fields to update
            
        Returns:
            tuple: (schedule_dict, error_message)
        """
        block = Schedule.query.filter_by(schedule_id=schedule_id, user_id=user_id).first()
        
        if not block:
            return None, "Schedule block not found"
        
        try:
            if 'date' in kwargs:
                block.date = datetime.fromisoformat(kwargs['date']).date()
            
            if 'start_time' in kwargs:
                block.start_time = datetime.strptime(kwargs['start_time'], '%H:%M').time()
            
            if 'end_time' in kwargs:
                block.end_time = datetime.strptime(kwargs['end_time'], '%H:%M').time()
            
            if 'title' in kwargs:
                block.title = kwargs['title']
            
            if 'block_type' in kwargs and kwargs['block_type'] in ['class', 'study', 'break']:
                block.block_type = kwargs['block_type']
            
            if 'color' in kwargs:
                block.color = kwargs['color']
            
            db.session.commit()
            return block.to_dict(include_task=True), None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update schedule block: {str(e)}"
    
    @staticmethod
    def delete_schedule_block(schedule_id: int, user_id: int):
        """
        Delete schedule block
        
        Args:
            schedule_id (int): Schedule ID
            user_id (int): User ID (for authorization)
            
        Returns:
            tuple: (success: bool, error_message)
        """
        block = Schedule.query.filter_by(schedule_id=schedule_id, user_id=user_id).first()
        
        if not block:
            return False, "Schedule block not found"
        
        try:
            db.session.delete(block)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete schedule block: {str(e)}"
