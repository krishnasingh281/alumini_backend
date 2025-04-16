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
                # Create alumni profile with default graduation year (you should update this)
                AlumniProfile.objects.create(user=instance, graduation_year=instance.graduation_year)
                print(f"Signal: Created AlumniProfile for {instance.username}")
        except Exception as e:
            print(f"Signal Error: {str(e)}")