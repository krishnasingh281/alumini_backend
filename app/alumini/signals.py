# alumini/signals.py (create this file)

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import AlumniProfile

User = get_user_model()

@receiver(post_save, sender=User)
def create_alumni_profile(sender, instance, created, **kwargs):
    """Create an AlumniProfile when a user with role='alumni' is created"""
    if created and instance.role == 'alumni':
        try:
            # Check if profile already exists
            if not hasattr(instance, 'alumni_profile'):
                # Set default graduation year to 2020 for testing
                AlumniProfile.objects.create(user=instance, graduation_year=2020)
                print(f"Signal: Created AlumniProfile for {instance.username}")
        except Exception as e:
            print(f"Signal Error: {str(e)}")