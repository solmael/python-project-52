from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.full_name

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