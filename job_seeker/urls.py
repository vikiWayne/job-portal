from django.urls import path, include
from job_seeker import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jobs/', views.JobListView.as_view(), name='jobs'),
    path('profile/', views.profile, name='profile'),
    path('search/',views.SearchResultsView, name='search_results'),
]