from django.db import models
from django.conf import settings

class AlumniProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="alumni_profile")
    first_name = models.CharField(max_length=255,null=True, blank=True)
    last_name = models.CharField(max_length=255,null=True, blank=True)
    graduation_year = models.IntegerField()
    current_company = models.CharField(max_length=255, blank=True, null=True)
    job_title = models.CharField(max_length=255, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="alumni/profile_pictures/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.current_company if self.current_company else 'Unemployed'}"
