from django.utils import timezone
from django.db import transaction, DatabaseError

from celery import shared_task

from .models import Task


@shared_task
def check_task_expiration():
    try:
        with transaction.atomic():
            expired_tasks = Task.objects.filter(
                expired_at__lt=timezone.now()
            ).exclude(
                status='expired'
            )
            expired_tasks.update(status='expired')
            return f"Updated {expired_tasks.count()} tasks to 'expired' status."
    except DatabaseError as e:
        print(f"Database error occurred: {e}")
        return "Failed to update tasks due to a database error."
