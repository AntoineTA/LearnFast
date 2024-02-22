from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.urls import reverse
from main.models import User

class UserListAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.teacher_user = User.objects.create_user(username='teacher', password='12345')
        self.user = User.objects.create_user(username='student', password='12345')
        self.teacher_group = Group.objects.create(name='Teachers')
        self.teacher_user.groups.add(self.teacher_group)
        self.url = reverse('api:users')

    def test_access_denied_if_not_teacher(self):
        self.client.login(username='student', password='12345')
        response = self.client.get(self.url)
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_teacher(self):
        self.client.login(username='teacher', password='12345')
        response = self.client.get(self.url)
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, 200)