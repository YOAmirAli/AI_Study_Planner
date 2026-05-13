"""
Task Tutor using Groq API
AI-powered study assistant that analyzes tasks and provides learning guidance
"""

from app.ai.groq_client import get_groq_client
import json

class TaskTutor:
    """AI tutor for task-based learning"""
    
    @staticmethod
    def analyze_and_teach(task_title: str, task_description: str) -> dict:
        """
        Analyze a task and provide comprehensive learning guidance
        
        Args:
            task_title (str): Title of the task
            task_description (str): Description of the task
            
        Returns:
            dict: Learning guidance with explanation, steps, resources, and tips
        """
        if not task_description or len(task_description.strip()) < 10:
            return {
                'explanation': 'This task needs more details to provide personalized guidance.',
                'learning_steps': [],
                'key_concepts': [],
                'resources': [],
                'study_tips': [],
                'estimated_time': 30
            }
        
        try:
            client = get_groq_client()
            
            prompt = f"""You are an expert AI tutor helping a student understand and complete their task.

Task Title: {task_title}
Task Description: {task_description}

Provide comprehensive learning guidance in the following JSON format:
{{
  "explanation": "Clear explanation of what this task is about and why it's important (2-3 sentences)",
  "learning_steps": [
    "Step 1: Detailed first step",
    "Step 2: Detailed second step",
    "Step 3: Detailed third step"
  ],
  "key_concepts": [
    "Concept 1: Brief explanation",
    "Concept 2: Brief explanation",
    "Concept 3: Brief explanation"
  ],
  "resources": [
    {{
      "title": "Resource title",
      "type": "video|article|tutorial|documentation",
      "description": "What this resource covers",
      "url": "Suggested search term or topic"
    }}
  ],
  "study_tips": [
    "Practical tip 1",
    "Practical tip 2",
    "Practical tip 3"
  ],
  "estimated_time": 60
}}

Provide 3-5 learning steps, 3-4 key concepts, 3-4 resources, and 3-4 study tips.
Make it practical, actionable, and encouraging.

Response:"""

            response = client.generate_with_retry(
                prompt=prompt,
                max_tokens=2000,
                temperature=0.7
            )
            
            # Parse JSON response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                guidance = json.loads(json_str)
                
                # Validate and format
                return {
                    'explanation': guidance.get('explanation', 'Let me help you understand this task.'),
                    'learning_steps': guidance.get('learning_steps', [])[:5],
                    'key_concepts': guidance.get('key_concepts', [])[:4],
                    'resources': guidance.get('resources', [])[:4],
                    'study_tips': guidance.get('study_tips', [])[:4],
                    'estimated_time': guidance.get('estimated_time', 60)
                }
            else:
                raise ValueError("Could not parse AI response")
                
        except Exception as e:
            print(f"Error in task tutor: {str(e)}")
            # Return fallback guidance
            return {
                'explanation': f'This task focuses on {task_title}. Let me help you break it down into manageable steps.',
                'learning_steps': [
                    'Read and understand the task requirements carefully',
                    'Break down the task into smaller subtasks',
                    'Research any unfamiliar concepts or terms',
                    'Create a plan and timeline for completion',
                    'Execute your plan step by step'
                ],
                'key_concepts': [
                    f'{task_title}: Core topic of this task',
                    'Time Management: Planning your study time effectively',
                    'Active Learning: Engaging with the material actively'
                ],
                'resources': [
                    {
                        'title': f'Introduction to {task_title}',
                        'type': 'video',
                        'description': 'Foundational overview of the topic',
                        'url': task_title
                    },
                    {
                        'title': f'{task_title} Tutorial',
                        'type': 'tutorial',
                        'description': 'Step-by-step guide',
                        'url': f'{task_title} tutorial'
                    },
                    {
                        'title': f'{task_title} Documentation',
                        'type': 'documentation',
                        'description': 'Official reference material',
                        'url': f'{task_title} documentation'
                    }
                ],
                'study_tips': [
                    'Start with the basics and build up gradually',
                    'Take regular breaks to maintain focus',
                    'Practice actively rather than just reading',
                    'Ask questions when you don\'t understand something'
                ],
                'estimated_time': 60
            }
