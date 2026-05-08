from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20)
    instructor = models.CharField(max_length=200, blank=True)
    credits = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=300)
    url = models.URLField(blank=True)
    source_type = models.CharField(max_length=50)  # 'youtube', 'coursera', 'pdf'
    created_at = models.DateTimeField(auto_now_add=True)