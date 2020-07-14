from django.db import models
from django.utils import timezone

class Employer(models.Model):
    user = models.OneToOneField('job_seeker.User', on_delete=models.CASCADE, related_name='employer')
    location = models.CharField(max_length=150, help_text='Employer location')
    address = models.TextField(help_text='Detaild address', null=True, blank=True)

    def __str__(self):
        return f'{ self.user } - Employer'
        # return f'{ self.user.email } - Employer'


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
    salary = models.CharField(max_length=15, default='0.00', help_text='Default currency is INR ₹', null=True, blank =True)
    location = models.CharField(max_length=150, help_text='Job location')
    type = models.CharField(choices=JOB_TYPE , max_length=50)
    posted_by = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='jobs')
    posted_date = models.DateTimeField(auto_now=True)
    is_opened = models.BooleanField(default=True)

    def __str__(self):
        return f'{ self.title }- { self.is_opened }'

class ExamQuestion(models.Model):
    job         = models.ForeignKey(Jobs, on_delete=models.CASCADE, related_name='examQuestion')
    question    = models.TextField(max_length=200)
    option1     = models.CharField(max_length=50)
    option2     = models.CharField(max_length=50)
    option3     = models.CharField(max_length=50)
    option4     = models.CharField(max_length=50)
    answer      = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{ self.job.title } - Questions'