from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Job, Application, Profile
from .forms import JobForm
from django.db import IntegrityError
from django.contrib.auth import login
from .forms import UserRegisterForm
from .decorators import employer_required, job_seeker_required, admin_required




# ==============================
# PUBLIC VIEWS
# ==============================

def job_list(request):
    jobs = Job.objects.filter(is_approved=True).order_by('-created_at')
    query = request.GET.get('q')
    location = request.GET.get('location')

    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(company__icontains=query))
    if location:
        jobs = jobs.filter(location__icontains=location)

    is_employer = False
    if request.user.is_authenticated and hasattr(request.user, 'profile'):
        is_employer = request.user.profile.is_employer

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'is_employer': is_employer
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_approved=True)
    return render(request, 'jobs/job_detail.html', {'job': job})

# ==============================
# EMPLOYER VIEWS (now public)
# ==============================

def job_create(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user if request.user.is_authenticated else None
            job.is_approved = False
            job.save()
            return redirect('employer_jobs')
    else:
        form = JobForm()
    return render(request, 'jobs/job_form.html', {'form': form})

def job_edit(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('employer_jobs')
    else:
        form = JobForm(instance=job)
    return render(request, 'jobs/job_form.html', {'form': form})

def employer_jobs(request):
    if request.user.is_authenticated:
        jobs = Job.objects.filter(posted_by=request.user)
    else:
        jobs = Job.objects.all()
    return render(request, 'jobs/employer_jobs.html', {'jobs': jobs})

def employer_applications(request):
    jobs = Job.objects.all()
    applications = Application.objects.filter(job__in=jobs).select_related('job', 'user')
    return render(request, 'employer/applications.html', {'applications': applications})

# ==============================
# ADMIN VIEWS (now public)
# ==============================


@employer_required
def approve_jobs(request):
    pending_jobs = Job.objects.filter(is_approved=False)
    return render(request, 'jobs/approve_jobs.html', {'pending_jobs': pending_jobs})

@employer_required
def approve_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.is_approved = True
        job.save()
    return redirect('approve_jobs')

@employer_required
def reject_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    if request.method == 'POST':
        job.delete()
    return redirect('approve_jobs')

# ==============================
# JOB APPLICATION (still protected)
# ==============================

from django.contrib.auth.decorators import login_required

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if Application.objects.filter(job=job, user=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job.id)

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter')

        Application.objects.create(
            user=request.user,
            job=job,
            resume=resume,
            cover_letter=cover_letter
        )

        send_mail(
            'New Application Received',
            f'{request.user.username} has applied to your job: {job.title}.',
            'no-reply@yourdomain.com',
            [job.posted_by.email],
        )

        messages.success(request, 'Application submitted successfully.')
        return redirect('applied_jobs')

    return render(request, 'jobs/apply.html', {'job': job})

# ==============================
# PROFILE (now public)
# ==============================

def edit_profile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
    else:
        profile = None

    if request.method == 'POST' and profile:
        profile.resume = request.FILES.get('resume', profile.resume)
        profile.skills = request.POST['skills']
        profile.education = request.POST['education']
        profile.experience = request.POST['experience']
        profile.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile', pk=request.user.pk)
    return render(request, 'accounts/edit_profile.html', {'profile': profile})

def profile(request, pk):
    profile = get_object_or_404(Profile, user__pk=pk)
    return render(request, 'accounts/profile.html', {'profile': profile})

def applied_jobs(request):
    if request.user.is_authenticated:
        applications = Application.objects.filter(user=request.user).select_related('job')
    else:
        applications = Application.objects.none()
    return render(request, 'jobs/applied_jobs.html', {'applications': applications})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('job_list')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def unauthorized(request):
   return render(request, 'jobs/unauthorized.html')


def home(request):
    return render(request, 'jobs/home.html')

