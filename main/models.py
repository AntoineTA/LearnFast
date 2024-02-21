from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    status = models.CharField(max_length=100, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    company = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='main/profile/avatars/', blank=True, null=True)
    last_request = models.DateTimeField(auto_now_add=True)

class Course(models.Model):
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='courses')
    blocked_students = models.ManyToManyField(User, related_name='blocked_courses')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses_taught')
    description = models.TextField(max_length=1000)

    def __str__(self):
        return self.name

class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    grade = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    file = models.FileField(upload_to='main/course/materials/')
    name = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    text = models.TextField()
    link = models.CharField(max_length=200)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)