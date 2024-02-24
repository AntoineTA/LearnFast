from django.test import TestCase, Client
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import reverse

from .models import User, Course

from random import choices
import string

class UserListTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.group = Group.objects.create(name='Teachers')
        self.url = reverse('profile:list')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_denied_without_group(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_with_group(self):
        self.user.groups.add(self.group)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

class ProfileEditTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('profile:edit')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_granted_if_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_correct_user(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.context['user'], self.user)

    def test_form_valid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'status': 'Test status', 'bio': 'Test bio', 'company': 'Test company'})
        self.assertEqual(response.status_code, 302)

    def test_form_invalid(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'status': ''.join(choices(string.ascii_letters, k=101))})
        self.assertEqual(response.status_code, 200)

class CourseEnrollTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.teacher = User.objects.create_user(username='testteacher', password='12345')
        self.course = Course.objects.create(name='Test course', teacher=self.teacher, description='Test description')
        self.url = reverse('course:enroll', args=[self.course.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_enroll(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.courses.get(id=self.course.id), self.course)

    def test_enroll_if_blocked(self):
        self.course.blocked_students.add(self.user)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.user.courses.count(), 0)

    def test_enroll_if_teacher(self):
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.teacher.courses.count(), 0)

class CourseCreateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.url = reverse('course:create')

    def test_redirect_if_not_teacher(self):
        self.user.groups.create(name='Students')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_teacher(self):
        self.user.groups.create(name='Teachers')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        self.user.groups.create(name='Teachers')
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'name': 'Test course', 'description': 'Test description'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.courses_taught.count(), 1)

    def test_form_invalid(self):
        self.user.groups.create(name='Teachers')
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'name': '', 'description': 'Test description'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.user.courses_taught.count(), 0)

class CourseFeedbackAddTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.teacher = User.objects.create_user(username='testteacher', password='12345')
        self.course = Course.objects.create(name='Test course', teacher=self.teacher, description='Test description')
        self.url = reverse('course:feedback_add', args=[self.course.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_denied_if_not_enrolled(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_enrolled(self):
        self.course.students.add(self.user)
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_access_denied_if_feedback_exists(self):
        self.course.students.add(self.user)
        self.course.feedbacks.create(author=self.user, grade=5, comment='Test comment')
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_form_valid(self):
        self.course.students.add(self.user)
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'grade': 5, 'comment': 'Test comment'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.feedbacks.get(author=self.user).grade, 5)

    def test_form_invalid(self):
        self.course.students.add(self.user)
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.url, {'grade': 7, 'comment': 'Test comment'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.feedbacks.count(), 0)

class CourseMaterialAddTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.teacher = User.objects.create_user(username='testteacher', password='12345')
        self.course = Course.objects.create(name='Test course', teacher=self.teacher, description='Test description')
        self.url = reverse('course:material_add', args=[self.course.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_denied_if_not_teacher(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_teacher(self):
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_form_valid(self):
        self.client.login(username='testteacher', password='12345')
        dummy_file = SimpleUploadedFile('test_file.txt', b'This is a dummy file.')
        response = self.client.post(self.url, {'name': 'Test material', 'file': dummy_file})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.materials.count(), 1)

    def test_form_invalid(self):
        self.client.login(username='testteacher', password='12345')
        response = self.client.post(self.url, {'name': 'Test material', 'file': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.course.materials.count(), 0)

class CourseStudentBlockTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.teacher = User.objects.create_user(username='testteacher', password='12345')
        self.student = User.objects.create_user(username='teststudent', password='12345')
        self.course = Course.objects.create(name='Test course', teacher=self.teacher, description='Test description')
        self.course.students.add(self.student)
        self.url = reverse('course:student_block', args=[self.course.id, self.student.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_denied_if_not_teacher(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_teacher(self):
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.blocked_students.get(id=self.student.id), self.student)

class CourseStudentUnblockTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.teacher = User.objects.create_user(username='testteacher', password='12345')
        self.student = User.objects.create_user(username='teststudent', password='12345')
        self.course = Course.objects.create(name='Test course', teacher=self.teacher, description='Test description')
        self.course.blocked_students.add(self.student)
        self.url = reverse('course:student_unblock', args=[self.course.id, self.student.id])

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_access_denied_if_not_teacher(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

    def test_access_granted_if_teacher(self):
        self.client.login(username='testteacher', password='12345')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.course.students.get(id=self.student.id), self.student)
        self.assertEqual(self.course.blocked_students.count(), 0)