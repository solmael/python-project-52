from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.ForeignKey('Status', on_delete=models.CASCADE)
    labels = models.ManyToManyField('Label')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)