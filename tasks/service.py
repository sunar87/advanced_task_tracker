from django.utils import timezone

from .models import Task


class TaskService():

    @staticmethod
    def get_expired_tasks(user_id):
        expired_tasks = Task.objects.filter(
            user_id=user_id,
            expired_at__lt=timezone.now()
        ).exclude(
            status='expired'
        )
        return expired_tasks
