from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:pk>/', views.job_detail, name='job_detail'),

    # Employer
    path('employer/jobs/', views.employer_jobs, name='employer_jobs'),
    path('employer/jobs/new/', views.job_create, name='job_create'),
    path('employer/jobs/<int:pk>/edit/', views.job_edit, name='job_edit'),
    path('employer/applications/', views.employer_applications, name='employer_applications'),

    # Admin
    path('admin/jobs/', views.approve_jobs, name='approve_jobs'),
    path('admin/jobs/<int:pk>/approve/', views.approve_job, name='approve_job'),
    path('admin/jobs/<int:pk>/reject/', views.reject_job, name='reject_job'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),

    # Applications
    path('job/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('applied-jobs/', views.applied_jobs, name='applied_jobs'),  # Optional if implemented

    # Profile
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),

    path('register/', views.register, name='register'),

]
