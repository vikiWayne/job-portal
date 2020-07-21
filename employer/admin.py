from django.contrib import admin
from employer.models import Jobs, Employer, ExamQuestion, OpenedExams
# Register your models here.

admin.site.register(Employer)
admin.site.register(Jobs)
admin.site.register(ExamQuestion)
admin.site.register(OpenedExams)