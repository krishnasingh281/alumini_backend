from django.db import models
from django.contrib.auth.models import Group, User

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='event/event_pics/', blank=True, null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)  # Store event creation time

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Events"  # Ensures proper pluralization in Django Admin