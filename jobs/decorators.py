from django.shortcuts import redirect
from functools import wraps

def employer_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'employer':
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return wrapper

def job_seeker_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.profile.role == 'job_seeker':
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return wrapper

def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return wrapper
