from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from job_seeker.managers import CustomUserManager
from employer.models import Jobs

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True, error_messages={'required': 'Please provide email','unique':'This email address is taken'})
    phone = models.CharField(max_length=15, null=True, unique=True, error_messages={'required': 'Please provide phone number','unique':'This phone number is taken'})
    about = models.TextField(null=True, blank=True)
    is_employee = models.BooleanField(default=True)
    account_confirmed = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager() 

    def __str__(self):
        return f'{ self.email }'

    class Meta:
        verbose_name = 'User'


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker')
    dob = models.DateField(null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)
    
    def __str__(self):
        return f'{ self.user.email } - Employee'


class Resumes(models.Model):
    jobseeker = models.OneToOneField(JobSeeker, on_delete=models.CASCADE, related_name = 'resumes')
    resume = models.FileField(null=True, blank=True)

    def __str__(self):
        return f'{ self.jobseeker.user.email } - Resume'

# class ExtractedResume(models.Model):
#     pass

class Address(models.Model):
    jobseeker = models.OneToOneField(JobSeeker, on_delete=models.CASCADE, related_name='address')
    house_name = models.CharField(max_length=50, null=True, blank=True, help_text='House/Buiding Name')
    street = models.CharField(max_length=30,null=True, blank=True, help_text='Road/Area')
    city = models.CharField(max_length=50, null=True, blank=True)
    district = models.CharField(max_length=30, null=True, blank=True )
    state = models.CharField(max_length=30, null=True, blank=True )
    pin = models.CharField(max_length=10, null=True, blank=True )
    land_mark = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        # pylint: disable=E1101
        return f'{self.jobseeker.user.email} - Address'

class JobApplication(models.Model):
    user = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='jobapplication')
    jobs = models.ForeignKey(Jobs, related_name='jobapplication', on_delete=models.CASCADE)
    applied_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{ self.user.user.email }- Applications'