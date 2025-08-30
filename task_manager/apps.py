from django.apps import AppConfig


class TaskManagerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'task_manager'

    def ready(self):
        # Keep this method empty as there are no signals or initialization tasks
        # required in the current implementation. This can be used in the future
        # for signal registration or other application startup tasks.
        pass