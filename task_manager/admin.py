from django.contrib import admin
from .models import CustomUser, Task, Status, Label

admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Label)