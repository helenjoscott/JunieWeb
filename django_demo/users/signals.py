from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to handle additional setup when a user is created.
    Currently used for any initialization that might be needed in the future.
    """
    if created:
        # Add any additional initialization here
        pass


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to handle additional actions when a user profile is saved.
    Currently used for any post-save operations that might be needed in the future.
    """
    # Add any post-save operations here
    pass