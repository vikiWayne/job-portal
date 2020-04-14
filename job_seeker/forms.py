from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from job_seeker.models import User, JobSeeker

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
         model = User
         fields = ['first_name','last_name','email','phone','about']

class EditEmployeeForm(ModelForm):
    class Meta:
        model = JobSeeker
        fields = ('profile_picture','dob','profession',)

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'There is something wrong with your credentials',
        'required_password': 'Password field is required',
        'required_username': 'Username field is required',
    }


# FORM VALIDATION 
