"""
Signal handlers for the blog app.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Post, Comment


@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, **kwargs):
    """Handle post-save operations for Post model."""
    if created:
        # Add any post-creation operations here
        pass


@receiver(post_save, sender=Comment)
def comment_save_handler(sender, instance, created, **kwargs):
    """Handle post-save operations for Comment model."""
    if created:
        # Add any post-creation operations here
        pass