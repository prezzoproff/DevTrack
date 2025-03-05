from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender = User)
def create_user_profile(sender, instance, created, **kwargs):
    '''Automatically creates a Userprofile when a new user is registered.'''
    if created:
        UserProfile.objects.create(user = instance)
    
@receiver(post_save, sender = User)
def save_user_profile(sender, instance, **kwargs):
    ''''Automatically saves the userprofile when the user instance is updated.'''
    instance.userprofile.save()