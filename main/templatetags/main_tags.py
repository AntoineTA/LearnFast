# From https://stackoverflow.com/a/34572799
from django import template

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()

@register.filter(name='unread_notifications')
def unread_notifications(user):
    return user.notifications.filter(read=False).count()