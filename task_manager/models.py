from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    
    class Meta:
        swappable = 'AUTH_USER_MODEL'
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    labels = models.ManyToManyField('Label')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Status(models.Model):
    name = models.CharField(max_length=50)

class Label(models.Model):
    name = models.CharField(max_length=50)