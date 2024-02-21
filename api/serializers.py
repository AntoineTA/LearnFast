from rest_framework import serializers
from main.models import *
from chat.models import Message
from django.urls import reverse

class CoursesSerializer(serializers.ModelSerializer):
    # Create new field to store the path of the course
    path = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['name', 'path']

    def get_path(self, obj):
        return reverse('course:detail', kwargs={'pk': obj.pk})

class CourseFeedbacksSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = CourseFeedback
        fields = ['course', 'grade', 'comment', 'created_at']

class NotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['text', 'link', 'read', 'created_at']

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['content', 'timestamp']

class UsersSerializer(serializers.ModelSerializer):
    courses = CoursesSerializer(many=True, read_only=True)
    blocked_courses = CoursesSerializer(many=True, read_only=True)
    courses_taught = CoursesSerializer(many=True, read_only=True)
    feedbacks = CourseFeedbacksSerializer(many=True, read_only=True)
    notifications = NotificationsSerializer(many=True, read_only=True)
    messages = MessagesSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'status',
            'bio',
            'company',
            'avatar',
            'courses',
            'blocked_courses',
            'courses_taught',
            'feedbacks',
            'notifications',
            'messages',
        ]
