# jobboard/context_processors.py
def is_employer_context(request):
    return {
        'is_employer': request.user.groups.filter(name='Employer').exists() if request.user.is_authenticated else False
    }
