from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import Group, User

class Blogs(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    
   
    created_at = models.DateTimeField(auto_now_add=True)  # Store event creation time

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Blogs"  # Ensures proper pluralization in Django Admin