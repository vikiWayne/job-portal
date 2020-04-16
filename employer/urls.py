from django.urls import path, include
from employer.views import  RegisterEmployerView, edit_employer

urlpatterns = [
    path('register/', RegisterEmployerView, name='employer-register'),
    path('account/',  edit_employer, name='employer-account')

]