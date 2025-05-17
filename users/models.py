from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import pyotp

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
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.jpg', null=True, blank=True)



    @property
    def is_2fa_enabled(self):
        return bool(self.otp_secret)


    def get_totp_uri(self):
        return pyotp.totp.TOTP(self.otp_secret).provisioning_uri(
            self.user.username, issuer_name="My Django App"
        )

    def verify_token(self, token):
        return pyotp.TOTP(self.otp_secret).verify(token)


    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)