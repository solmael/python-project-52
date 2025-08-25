from django.db import models
from django.db.models.deletion import ProtectedError


class Status(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    # def delete(self, using=None, keep_parents=False):
    #     if self.task_set.exists():
    #         raise ProtectedError(
    #             "Статус в задачах",
    #             self.task_set.all()
    #         )
    #     super().delete(using=using, keep_parents=keep_parents)