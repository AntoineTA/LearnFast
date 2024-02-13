from django import forms
from django.forms import TextInput, PasswordInput
from django.contrib.auth.forms import UserCreationForm
from .models import *

class SignupForm(UserCreationForm):
    # Tailwind CSS from Flowbite
    input_style = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
    
    username = forms.CharField(widget=forms.TextInput(attrs={'class': input_style}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': input_style}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': input_style}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'bio', 'company')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('name',)

class CourseFeedbackForm(forms.ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ('grade', 'comment')

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ('name', 'file',)