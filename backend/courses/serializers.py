from rest_framework import serializers
from .models import Course, StudyMaterial

class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    materials = StudyMaterialSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'