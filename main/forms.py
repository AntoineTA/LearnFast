from django import forms
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'status', 'bio', 'company', 'avatar')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name', 'description')

class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ('grade', 'comment')

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('name', 'file',)