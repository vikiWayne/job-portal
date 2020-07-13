from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm

from job_seeker.models import User, JobSeeker, Address, Resumes

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','phone']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
         model = User
         fields = ['first_name','last_name','email','phone','about']

class EditEmployeeForm(ModelForm):
    profile_picture = forms.ImageField(error_messages = {'invalid':("Image files only")}, widget=forms.FileInput, required=False)

    class Meta:
        model = JobSeeker
        fields = ('dob','profession','gender','profile_picture')

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ('house_name', 'street', 'city', 'district', 'state', 'pin')

class ResumeForm(ModelForm):
    class Meta:
        model = Resumes
        fields = ('resume',)

class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': 'There is something wrong with your credentials',
        'required_password': 'Password field is required',
        'required_username': 'Username field is required',
    }


# FORM VALIDATION 
