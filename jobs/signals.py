# jobs/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = getattr(instance, '_profile_role', 'job_seeker')
        Profile.objects.create(user=instance, role=role)
