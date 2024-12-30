from django.db import models
from django.contrib.auth.models import User

class UserActivity(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
    ]
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,  # Allow null values when the user is deleted
        blank=True
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    login_at = models.DateTimeField(auto_now_add=True)  # Automatically log the timestamp
    details = models.TextField(blank=True, null=True)  # Additional details about the action
    login_ip = models.GenericIPAddressField(blank=True, null=True)  # IP address of the user

    def __str__(self):
        return super().__str__()
       