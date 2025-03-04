from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Issues(models.Model):
    priority_choices = [
        ('low', 'low'),
        ('medium', 'medium'),
        ('high', 'high')
    ]

    status_choices = [
        ('open', 'open'),
        ('In progres', 'In progres'),
        ('Closed', 'Closed')
    ]

    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    priority = models.CharField(max_length=20, choices=priority_choices, default='medium')
    status = models.CharField(max_length=20, choices=status_choices, default= 'open')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



