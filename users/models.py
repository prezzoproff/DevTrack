from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True) # Link to built-in user Model
    first_name = models.CharField(max_length=100, default ='name')
    last_name = models.CharField(max_length=100, default = 'name')
    email = models.EmailField(default = "email@domain.com")
    bio = models.TextField(blank = True, null = True) #Optional Bio field
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True) #Automatically stores registration date
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)


    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)