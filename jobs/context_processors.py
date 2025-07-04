def user_role(request):
    is_employer = False
    is_admin = False

    if request.user.is_authenticated:
        if request.user.is_superuser:
            is_admin = True
        else:
            is_employer = getattr(request.user.profile, 'is_employer', False)

    return {
        'is_employer': is_employer,
        'is_admin': is_admin
    }
