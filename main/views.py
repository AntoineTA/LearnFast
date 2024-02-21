from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import TemplateView, DetailView, ListView, RedirectView, CreateView, UpdateView
from .forms import *

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile:own')
        return super().get(request)

class UserListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'profile/list.html'

    def test_func(self):
        return self.request.user.groups.filter(name='Teachers').exists()

    # Filter users by group specified in the URL
    def get_queryset(self):
        queryset = super().get_queryset()
        group_name = self.request.GET.get('group')
        if group_name:
            group = Group.objects.get(name=group_name)
            queryset = queryset.filter(groups__in=[group])
        return queryset

class SignupView(TemplateView, UserPassesTestMixin):
    template_name = 'registration/signup.html'

    def get(self, request):
        if (self.request.user.is_authenticated):
            return redirect('profile:own')
            
        form = SignupForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            # Add user to Student group
            student_group = Group.objects.get(name='Students')
            student_group.user_set.add(user)

            # Log the user in
            login(request, user)
            return redirect('profile:own')

        return render(request, self.template_name, 
            {'form': form})

class LogoutRedirectView(RedirectView):
    def get(self, request):
        logout(request)
        self.url = reverse('index')
        print(self.url)
        return super().get(request)

# Redirect to the user's profile page
class ProfileRedirectView(LoginRequiredMixin, RedirectView):
    def get(self, request):
        self.url = reverse('profile:detail', kwargs={'pk': request.user.id})
        return super().get(request)

class ProfileView(DetailView):
    model = User
    template_name = 'profile/detail.html'

class ProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = 'profile/edit.html'

    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect ('profile:own')

        # If form is not valid, re-render the page with the form
        return render(request, self.template_name, {'form': form})

class CourseListView(ListView):
    model = Course
    template_name = 'course/list.html'

class CourseView(DetailView):
    model = Course
    template_name = 'course/detail.html'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    template_name = 'course/create.html'
    form_class = CourseForm

    # form_valid is called when the form is submitted and valid
    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course:detail', kwargs={'pk': self.object.pk})

class CourseEnrollView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def test_func(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        is_blocked = self.request.user in course.blocked_students.all()
        is_teacher = self.request.user == course.teacher
        return not is_blocked and not is_teacher

    def get_redirect_url(self, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        course.students.add(self.request.user)
        Notification.objects.create(
            user=course.teacher,
            text=f'{self.request.user} enrolled in {course.name}',
            link=reverse('course:detail', kwargs={'pk': course.pk}))

        return reverse('course:detail', kwargs={'pk': self.kwargs['pk']})

class CourseFeedbackAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CourseFeedback
    template_name = 'course/feedback/add.html'
    form_class = CourseFeedbackForm

    def test_func(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        is_enrolled = self.request.user in course.students.all()
        has_feedback = course.feedbacks.filter(author=self.request.user).exists()
        return is_enrolled and not has_feedback

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.course = Course.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('course:detail', kwargs={'pk': self.object.course.pk})

class CourseMaterialAddView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = CourseMaterial
    template_name = 'course/material/add.html'
    form_class = CourseMaterialForm

    def test_func(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user == course.teacher

    def form_valid(self, form):
        form.instance.course = Course.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        # Notify each student enrolled in the course
        course = Course.objects.get(pk=self.kwargs['pk'])
        for student in course.students.all():
            Notification.objects.create(
                user=student,
                text=f'New material in {course.name}',
                link=reverse('course:detail', kwargs={'pk': course.pk}))

        return reverse('course:detail', kwargs={'pk': self.kwargs['pk']})

class CourseStudentBlockView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def test_func(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user == course.teacher

    def get_redirect_url(self, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        student = get_object_or_404(User, id=kwargs['student_id'])

        course.students.remove(student)
        course.blocked_students.add(student)

        return reverse('course:detail', kwargs={'pk': self.kwargs['pk']})

class CourseStudentUnblockView(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    def test_func(self):
        course = Course.objects.get(pk=self.kwargs['pk'])
        return self.request.user == course.teacher

    def get_redirect_url(self, *args, **kwargs):
        course = Course.objects.get(pk=self.kwargs['pk'])
        student = get_object_or_404(User, id=kwargs['student_id'])

        course.students.add(student)
        course.blocked_students.remove(student)

        return reverse('course:detail', kwargs={'pk': self.kwargs['pk']})

class NotificationReadView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, id=kwargs['notif_id'])
        notification.read = True
        notification.save()
        return reverse('profile:own') + '#notifications'

class NotificationDeleteView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, id=kwargs['notif_id'])
        notification.delete()
        return reverse('profile:own') + '#notifications'

class NotificationUnreadView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        notification = get_object_or_404(Notification, id=kwargs['notif_id'])
        notification.read = False
        notification.save()
        return reverse('profile:own') + '#notifications'