from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, role='student', **extra_fields):
        """Create and return a regular user."""
        if not email:
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)
        
        # Ensure only superusers can be 'admin'
        if role == 'admin' and not extra_fields.get('is_superuser', False):
            raise ValueError("Only superusers can have the 'admin' role.")

        extra_fields.setdefault('is_active', True)  # Ensure user is active by default
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """Create and return a superuser with admin role."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')  # Set role to 'admin' for superusers

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ('alumni', 'Alumni'),
        ('student', 'Student'),
        ('admin', 'Admin'),  # Admin is a valid role but restricted
    ]

    email = models.EmailField(unique=True)  # Make email unique
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    # Removed graduation_year field from here - now only in AlumniProfile
    objects = UserManager()  # Use the custom manager

    REQUIRED_FIELDS = ['email', 'role']  # Required for createsuperuser

    def __str__(self):
        return f"{self.username} ({self.role})"