"""
AI-Powered Schedule Generation Algorithm
Uses Grok AI to intelligently generate study schedules with breaks
"""

import os
import requests
from datetime import datetime, timedelta, time
from typing import List, Dict, Any

class ScheduleAlgorithm:
    """Intelligent schedule generation using Grok AI"""
    
    GROK_API_KEY = os.getenv('XAI_API_KEY')
    GROK_API_URL = "https://api.x.ai/v1/chat/completions"
    
    @staticmethod
    def generate_schedule(user_id: int, tasks: List[Dict], existing_blocks: List[Dict],
                         week_start_date, study_hours_per_day: int = 4) -> List[Dict]:
        """
        Generate intelligent study schedule using Grok AI
        
        Args:
            user_id: User ID
            tasks: List of pending tasks
            existing_blocks: Existing schedule blocks (classes, etc.)
            week_start_date: Start date of the week
            study_hours_per_day: Target study hours per day
            
        Returns:
            List of schedule blocks
        """
        
        # Prepare task information for AI
        task_info = []
        for task in tasks:
            task_info.append({
                'title': task.get('title'),
                'priority': task.get('priority', 'medium'),
                'due_date': task.get('due_date'),
                'estimated_hours': task.get('estimated_hours', 2),
                'course': task.get('course', {}).get('course_name', 'General'),
                'task_id': task.get('task_id')
            })
        
        # Prepare existing blocks information
        occupied_slots = []
        for block in existing_blocks:
            occupied_slots.append({
                'date': block.get('date'),
                'start_time': block.get('start_time'),
                'end_time': block.get('end_time'),
                'type': block.get('block_type')
            })
        
        # Generate schedule using Grok AI
        if ScheduleAlgorithm.GROK_API_KEY:
            try:
                ai_schedule = ScheduleAlgorithm._generate_with_grok_ai(
                    tasks=task_info,
                    occupied_slots=occupied_slots,
                    week_start=week_start_date,
                    study_hours_per_day=study_hours_per_day
                )
                if ai_schedule:
                    return ai_schedule
            except Exception as e:
                print(f"Grok AI generation failed: {e}, falling back to rule-based")
        
        # Fallback to rule-based algorithm
        return ScheduleAlgorithm._generate_rule_based(
            user_id, tasks, existing_blocks, week_start_date, study_hours_per_day
        )
    
    @staticmethod
    def _generate_with_grok_ai(tasks: List[Dict], occupied_slots: List[Dict],
                               week_start, study_hours_per_day: int) -> List[Dict]:
        """Generate schedule using Grok AI API"""
        
        # Create prompt for Grok
        prompt = f"""You are an intelligent study schedule generator. Create an optimal weekly study schedule.

**Week Start Date:** {week_start.isoformat()}
**Target Study Hours Per Day:** {study_hours_per_day}

**Tasks to Schedule:**
{ScheduleAlgorithm._format_tasks_for_prompt(tasks)}

**Occupied Time Slots (Classes/Commitments):**
{ScheduleAlgorithm._format_occupied_slots(occupied_slots)}

**Requirements:**
1. Schedule study sessions between 8:00 AM and 10:00 PM
2. Include 15-minute breaks after every 90 minutes of study
3. Include 30-minute lunch break (12:00-12:30) and dinner break (18:00-18:30)
4. Prioritize high-priority tasks and tasks with earlier due dates
5. Distribute study time evenly across the week
6. Avoid scheduling during occupied slots
7. Group similar subjects together when possible
8. Ensure adequate rest periods

**Output Format (JSON array):**
```json
[
  {{
    "date": "YYYY-MM-DD",
    "start_time": "HH:MM:SS",
    "end_time": "HH:MM:SS",
    "block_type": "study|break",
    "title": "Task title or Break",
    "task_id": task_id_or_null
  }}
]
```

Generate the schedule now:"""

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {ScheduleAlgorithm.GROK_API_KEY}"
        }
        
        payload = {
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert study schedule optimizer. Generate schedules in valid JSON format only."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "model": "grok-beta",
            "stream": False,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                ScheduleAlgorithm.GROK_API_URL,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Extract JSON from response
                import json
                import re
                
                # Try to find JSON array in the response
                json_match = re.search(r'\[[\s\S]*\]', content)
                if json_match:
                    schedule_data = json.loads(json_match.group())
                    
                    # Add user_id and is_auto_generated to each block
                    for block in schedule_data:
                        block['user_id'] = None  # Will be set by service
                        block['is_auto_generated'] = True
                    
                    return schedule_data
            
            print(f"Grok API error: {response.status_code} - {response.text}")
            return None
            
        except Exception as e:
            print(f"Error calling Grok AI: {e}")
            return None
    
    @staticmethod
    def _format_tasks_for_prompt(tasks: List[Dict]) -> str:
        """Format tasks for AI prompt"""
        if not tasks:
            return "No tasks to schedule"
        
        formatted = []
        for i, task in enumerate(tasks, 1):
            formatted.append(
                f"{i}. {task['title']} - Priority: {task['priority']}, "
                f"Due: {task.get('due_date', 'No deadline')}, "
                f"Est. Hours: {task.get('estimated_hours', 2)}, "
                f"Course: {task.get('course', 'General')}, "
                f"ID: {task.get('task_id')}"
            )
        return "\n".join(formatted)
    
    @staticmethod
    def _format_occupied_slots(slots: List[Dict]) -> str:
        """Format occupied slots for AI prompt"""
        if not slots:
            return "No occupied slots"
        
        formatted = []
        for slot in slots:
            formatted.append(
                f"- {slot['date']} from {slot['start_time']} to {slot['end_time']} ({slot['type']})"
            )
        return "\n".join(formatted)
    
    @staticmethod
    def _generate_rule_based(user_id: int, tasks: List[Dict], existing_blocks: List[Dict],
                            week_start_date, study_hours_per_day: int) -> List[Dict]:
        """
        Fallback rule-based schedule generation
        Implements intelligent scheduling logic without AI
        """
        schedule_blocks = []
        
        # Sort tasks by priority and due date
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (
                {'high': 0, 'medium': 1, 'low': 2}.get(t.get('priority', 'medium'), 1),
                t.get('due_date', '9999-12-31')
            )
        )
        
        # Define study time slots (avoiding meal times)
        study_periods = [
            ('08:00:00', '12:00:00'),  # Morning
            ('12:30:00', '14:00:00'),  # Early afternoon
            ('14:30:00', '18:00:00'),  # Late afternoon
            ('18:30:00', '21:00:00'),  # Evening
        ]
        
        # Generate schedule for each day of the week
        for day_offset in range(7):
            current_date = week_start_date + timedelta(days=day_offset)
            date_str = current_date.isoformat()
            
            # Get occupied slots for this day
            day_occupied = [
                block for block in existing_blocks
                if block.get('date') == date_str
            ]
            
            daily_study_hours = 0
            task_index = 0
            
            # Schedule study blocks for this day
            for period_start, period_end in study_periods:
                if daily_study_hours >= study_hours_per_day:
                    break
                
                # Check if period is available
                if ScheduleAlgorithm._is_time_available(
                    period_start, period_end, day_occupied
                ):
                    # Calculate study duration (90 minutes max per session)
                    remaining_hours = study_hours_per_day - daily_study_hours
                    session_hours = min(1.5, remaining_hours)
                    
                    if task_index < len(sorted_tasks):
                        task = sorted_tasks[task_index]
                        
                        # Create study block
                        start_time = datetime.strptime(period_start, '%H:%M:%S').time()
                        end_time = (
                            datetime.combine(current_date, start_time) +
                            timedelta(hours=session_hours)
                        ).time()
                        
                        schedule_blocks.append({
                            'user_id': user_id,
                            'task_id': task.get('task_id'),
                            'date': date_str,
                            'start_time': start_time.strftime('%H:%M:%S'),
                            'end_time': end_time.strftime('%H:%M:%S'),
                            'block_type': 'study',
                            'title': f"Study: {task.get('title')}",
                            'is_auto_generated': True
                        })
                        
                        daily_study_hours += session_hours
                        
                        # Add break after study session
                        if session_hours >= 1.5:
                            break_start = end_time
                            break_end = (
                                datetime.combine(current_date, break_start) +
                                timedelta(minutes=15)
                            ).time()
                            
                            schedule_blocks.append({
                                'user_id': user_id,
                                'task_id': None,
                                'date': date_str,
                                'start_time': break_start.strftime('%H:%M:%S'),
                                'end_time': break_end.strftime('%H:%M:%S'),
                                'block_type': 'break',
                                'title': 'Break',
                                'is_auto_generated': True
                            })
                        
                        task_index += 1
        
        return schedule_blocks
    
    @staticmethod
    def _is_time_available(start_time: str, end_time: str, occupied_blocks: List[Dict]) -> bool:
        """Check if a time slot is available"""
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end = datetime.strptime(end_time, '%H:%M:%S').time()
        
        for block in occupied_blocks:
            block_start = datetime.strptime(
                block['start_time'] if ':' in str(block['start_time']) else block['start_time'] + ':00',
                '%H:%M:%S' if block['start_time'].count(':') == 2 else '%H:%M'
            ).time()
            block_end = datetime.strptime(
                block['end_time'] if ':' in str(block['end_time']) else block['end_time'] + ':00',
                '%H:%M:%S' if block['end_time'].count(':') == 2 else '%H:%M'
            ).time()
            
            # Check for overlap
            if not (end <= block_start or start >= block_end):
                return False
        
        return True
