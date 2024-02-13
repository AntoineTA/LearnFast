from django import template
from datetime import timedelta
from django.utils import timezone

register = template.Library() 

# From https://stackoverflow.com/a/34572799
@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='unread_notifications')
def unread_notifications(user):
    return user.notifications.filter(read=False).count()

@register.simple_tag
def displayname(user):
    return user.first_name if user.first_name else user.username

@register.simple_tag
def displayrole(user):
    role = 'Student'
    if user.groups.filter(name='Teachers').exists():
        role = 'Teacher'
    return role

@register.simple_tag
def is_online(user):
    # Check if the user has made a request in the last minute
    return user.last_request >= timezone.now() - timedelta(minutes=1)