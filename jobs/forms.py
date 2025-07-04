from django import forms
from .models import Job
from django.contrib.auth.models import User
from .models import Profile


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            'title', 'company_name', 'description', 'location',
            'salary', 'category', 'job_type', 'experience'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
 
 
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])

        user._profile_role = self.cleaned_data['role']

        if commit:
            user.save()
        return user
