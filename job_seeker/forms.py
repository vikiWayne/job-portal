from django.forms import ModelForm
from django import forms
from job_seeker.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
         model = User
         fields = ['email']

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'There is something wrong with your credentials',
        'required_password': 'Password field is required',
        'required_username': 'Username field is required',
    }
