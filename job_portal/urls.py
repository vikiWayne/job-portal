from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_view

from job_seeker import views as job_seeker_views
from job_seeker.forms import CustomAuthenticationForm
from employer.views import JobDetailView, EmployerListView , EmployerDetailView, JobsByEmployerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('job_seeker.urls')),
    path('employer/', include('employer.urls')),
    path('login/', auth_view.LoginView.as_view(template_name='job_seeker/login.html', redirect_authenticated_user=True, authentication_form=CustomAuthenticationForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'job_seeker/logout.html'), name='logout'),
    path('sign-up/', job_seeker_views.register, name='register'),
    path('social-auth/', include('social_django.urls', namespace='social')),

    path('job/<int:pk>/', JobDetailView.as_view(), name='job-detail'),
    path('job/<int:pk>/apply/', job_seeker_views.JobApplyView.as_view()),

    path('job/<int:pk>/cancel_application/', job_seeker_views.CancelJobApplication.as_view()),
    
    path('employers/', EmployerListView.as_view(), name='employers'),
    path('employer/<int:pk>/', EmployerDetailView.as_view(), name='employer-detail'),
    path('employer/<int:pk>/jobs/', JobsByEmployerView.as_view(), name='employer-jobs'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'job_seeker.views.handler404'