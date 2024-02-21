from .serializers import *
from .permissions import *
from main.models import *
from rest_framework import generics

class UserList(generics.ListAPIView):
    permission_classes = [IsTeacher]

    queryset = User.objects.all()
    serializer_class = UsersSerializer

class UserDetail(generics.RetrieveAPIView):
    def get_object(self):
        user = self.request.user
        return user

    serializer_class = UsersSerializer