from django.urls import path
from . import api

urlpatterns = [
    path('users', api.UserList.as_view(), name='users'),
    path('profile', api.UserDetail.as_view(), name='profile'),
]