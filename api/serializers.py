from rest_framework import serializers
from main.models import *

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'status', 'bio', 'company', 'avatar', 'last_request']

class CoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'students', 'blocked_students', 'teacher', 'description']

class CourseFeedbacksSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFeedback
        fields = ['id', 'course', 'author', 'grade', 'comment', 'created_at']

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'text', 'link', 'read', 'created_at']