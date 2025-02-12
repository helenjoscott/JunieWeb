from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds additional fields for user profile.
    """
    # Additional fields
    bio = models.TextField(max_length=500, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=200, blank=True)
    
    # Social media fields
    twitter = models.CharField(max_length=50, blank=True)
    linkedin = models.CharField(max_length=50, blank=True)
    github = models.CharField(max_length=50, blank=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email if self.email else self.username
    
    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
    
    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name
    
    def get_profile_completion_percentage(self):
        """
        Calculate the profile completion percentage based on filled fields.
        """
        fields = [
            self.bio, self.birth_date, self.avatar, self.location,
            self.website, self.twitter, self.linkedin, self.github,
            self.first_name, self.last_name
        ]
        filled_fields = sum(1 for field in fields if field)
        return (filled_fields / len(fields)) * 100