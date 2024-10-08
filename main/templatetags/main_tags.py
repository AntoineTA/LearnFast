from django import template
from datetime import timedelta
from django.utils import timezone
from django.db import models

register = template.Library() 

# From https://stackoverflow.com/a/34572799
@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter
def has_unread_notifications(user):
    return user.notifications.filter(read=False).exists()

@register.simple_tag
def unread_notifications_count(user):
    return user.notifications.filter(read=False).count()

@register.simple_tag
def displayname(user):
    if user.first_name and user.last_name:
        return user.first_name + ' ' + user.last_name
    elif user.first_name:
        return user.first_name
    else:
        return user.username

@register.simple_tag
def displayrole(user):
    role = 'Student'
    if user.groups.filter(name='Teachers').exists():
        role = 'Teacher'
    return role

@register.filter
def is_online(user):
    # Check if the user has made a request in the last minute
    return user.last_request >= timezone.now() - timedelta(minutes=5)

@register.simple_tag
def get_initials(user):
    if user.first_name and user.last_name:
        return user.first_name[0] + user.last_name[0]
    elif user.first_name:
        return user.first_name[0:2]
    else:
        return user.username[0:2]

@register.simple_tag
def display_size(size):
    if size < 1024:
        return str(size) + ' B'
    elif size < 1024 * 1024:
        return str(round(size / 1024, 2)) + ' KB'
    else:
        return str(round(size / (1024 * 1024), 2)) + ' MB'

@register.simple_tag
def relative_time(time):
    now = timezone.now()
    if time > now - timedelta(days=1):
        return 'Today'
    elif time > now - timedelta(days=2):
        return 'Yesterday'
    else:
        return time.strftime('%d %b %Y')

@register.filter
def has_feedback(user, course):
    return course.feedbacks.filter(author=user).exists()

@register.simple_tag
def avg_grade(course):
    return course.feedbacks.aggregate(models.Avg('grade'))['grade__avg']