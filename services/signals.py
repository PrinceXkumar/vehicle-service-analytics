from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    When a User is created, create a Profile.
    If the user is updated, save the profile (safe if already exists).
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Ensure profile exists and save updates if needed
        Profile.objects.get_or_create(user=instance)[0].save()
