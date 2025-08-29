from django.contrib.auth import get_user_model
from django.db import models

from .label import Label
from .status import Status

User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.PROTECT,
        related_name='author_tasks'
    )
    executor = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='executor_tasks'
    )
    labels = models.ManyToManyField(
        Label,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name