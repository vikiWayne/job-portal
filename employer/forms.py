from django import forms
from django.forms import ModelForm
from employer.models import Jobs, Employer
from django.contrib.auth.forms import UserCreationForm

class CompanyRegisterForm(ModelForm):
    class Meta:
        model = Employer
        fields = ['name','email','phone',]

class PostJobForm(ModelForm):
    class Meta:
        model = Jobs
        fields = ['title', 'description','qualifications','experience', 'salary', 'location']