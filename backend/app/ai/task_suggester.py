"""
Task Suggester using Groq API
Generate task suggestions based on course description
"""

from app.ai.groq_client import get_groq_client
import json

class TaskSuggester:
    """Generate task suggestions for courses"""
    
    @staticmethod
    def suggest_tasks(course_name: str, description: str, num_tasks: int = 5) -> dict:
        """
        Generate task suggestions based on course description
        
        Args:
            course_name (str): Name of the course
            description (str): Course description
            num_tasks (int): Number of tasks to suggest (3-10)
            
        Returns:
            dict: Suggested tasks array
        """
        if not description or len(description.strip()) < 50:
            raise ValueError("Description must be at least 50 characters")
        
        if num_tasks < 3 or num_tasks > 10:
            num_tasks = 5
        
        try:
            client = get_groq_client()
            
            prompt = f"""Based on the following course information, suggest {num_tasks} specific, actionable tasks that a student should complete.

Course Name: {course_name}
Course Description: {description}

Generate practical tasks that include:
- Reading assignments
- Practice exercises
- Projects
- Quizzes/Tests
- Research topics

Format as JSON array:
[
  {{
    "title": "Task title",
    "description": "Detailed task description",
    "priority": "high|medium|low",
    "estimated_time": 120 (in minutes),
    "deadline_days": 7 (days from now)
  }}
]

Tasks:"""

            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse JSON response
            json_start = response.find('[')
            json_end = response.rfind(']') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                tasks = json.loads(json_str)
                
                # Validate and format tasks
                formatted_tasks = []
                for task in tasks[:num_tasks]:
                    formatted_tasks.append({
                        'title': task.get('title', 'Untitled Task'),
                        'description': task.get('description', ''),
                        'priority': task.get('priority', 'medium').lower(),
                        'estimated_time': task.get('estimated_time', 60),
                        'deadline_days': task.get('deadline_days', 7)
                    })
                
                return {
                    'tasks': formatted_tasks,
                    'total_suggestions': len(formatted_tasks),
                    'course_name': course_name
                }
            else:
                raise ValueError("Could not parse AI response")
                
        except Exception as e:
            # Return fallback suggestions
            return {
                'tasks': [
                    {
                        'title': f'Read {course_name} Introduction',
                        'description': 'Review the course materials and introduction',
                        'priority': 'high',
                        'estimated_time': 60,
                        'deadline_days': 3
                    },
                    {
                        'title': f'Complete {course_name} Practice Problems',
                        'description': 'Work through practice exercises',
                        'priority': 'medium',
                        'estimated_time': 120,
                        'deadline_days': 7
                    },
                    {
                        'title': f'{course_name} Quiz Preparation',
                        'description': 'Prepare for upcoming quiz',
                        'priority': 'high',
                        'estimated_time': 90,
                        'deadline_days': 5
                    }
                ],
                'total_suggestions': 3,
                'course_name': course_name,
                'note': 'Showing default suggestions'
            }
