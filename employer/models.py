from django.db import models
from django.utils import timezone
from PIL import Image
# Create your models here.

class Employer(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(help_text='A Detailed Description about Employer')
    location = models.CharField(max_length=150, help_text='Employer location')
    email = models.EmailField(unique=True, error_messages={'required': 'Please provide email','unique':'This email address is taken'})
    phone = models.CharField(max_length=12, unique=True, help_text='Contact number')
    address = models.TextField(help_text='Detaild address', null=True, blank=True)
    about = models.TextField(help_text='About Employer', null=True, blank=True)

    def __str__(self):
        return f'{ self.name }'


JOB_TYPE = (
    ('full time', "Full time"),
    ('part time', "Part time"),
    ('internship', "Internship"),
)

class Jobs(models.Model):
    title = models.CharField(max_length=50, help_text='Job title')
    description = models.TextField(help_text='A Detailed Description about job')
    qualifications = models.CharField(max_length=150)
    experience = models.IntegerField(default='0', help_text='Minimum experience')
    salary = models.CharField(max_length=15, default='Salary package is not provided', help_text='Default currency is INR ₹')
    location = models.CharField(max_length=150, help_text='Job location')
    type = models.CharField(choices=JOB_TYPE , max_length=50)
    posted_by = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    posted_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{ self.title } '
