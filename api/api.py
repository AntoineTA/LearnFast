from main.models import *
from . import serializers
from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer