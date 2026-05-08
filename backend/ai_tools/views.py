from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .services import AIService

ai_service = AIService()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_study_plan(request):
    tasks = request.data.get('tasks')
    available_hours = request.data.get('available_hours')
    
    plan = ai_service.generate_study_plan(tasks, available_hours)
    return Response({'study_plan': plan})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_summary(request):
    text = request.data.get('text')
    summary = ai_service.generate_summary(text)
    return Response({'summary': summary})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_quiz(request):
    topic = request.data.get('topic')
    num_questions = request.data.get('num_questions', 5)
    quiz = ai_service.generate_quiz(topic, num_questions)
    return Response({'quiz': quiz})