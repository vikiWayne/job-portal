from django.urls import path, include
from employer.views import post_job, RegisterEmployerView

urlpatterns = [
    path('post_job/', post_job, name='post_job'),
    path('register/', RegisterEmployerView, name='employer-register'),

]