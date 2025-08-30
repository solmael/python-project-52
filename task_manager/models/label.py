from django.apps import apps
from django.db import models
from django.db.models.deletion import ProtectedError


class Label(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
        
    def delete(self, *args, **kwargs):
        task = apps.get_model('task__manager', 'task')
        
        if task.objects.filter(labels=self).exists():
            raise ProtectedError(None, task.objects.filter(labels=self))
        super().delete(*args, **kwargs)