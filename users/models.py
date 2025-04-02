from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link to built-in user Model
    first_name = models.CharField(max_length=100, default ='name')
    last_name = models.CharField(max_length=100, default = 'name')
    email = models.EmailField(default = "email@domain.com")
    bio = models.TextField(blank = True, null = True) #Optional Bio field
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True) #Automatically stores registration date
    two_factor_secret = models.CharField(max_length=32, blank=True, null=True)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)  # Store profile picture


    def __str__(self):
        return self.user.username
    