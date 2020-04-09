from django.urls import path, include
from employer.views import post_job, JobDetailView, company_register

urlpatterns = [
    path('post_job/', post_job, name='post_job'),
    path('register/', company_register, name='register_company'),
]