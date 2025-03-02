from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) # Link to built-in user Model
    bio = models.TextField(blank = True, null = True) #Optional Bio field
    # profile_picture = models.ImageField(upload_to = 'profile_pics/', blank = True, null = True) #Profile picture
    created_at = models.DateTimeField(auto_now_add = True) #Automatically stores registration date


    def __str__(self):
        return self.user.username