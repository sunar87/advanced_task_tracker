from django.db import transaction, DatabaseError
from django.contrib.auth import get_user_model
from celery import shared_task

from .service import TaskService
from .management.commands.telegram import send_message_sync


@shared_task
def check_task_expiration(user_id):
    try:
        with transaction.atomic():
            expired_tasks = TaskService.get_expired_tasks(user_id=user_id)
            expired_tasks.update(status='expired')
            send_message_sync(message='Test')
            return f"Updated {expired_tasks.count()} tasks to 'expired' status for user {user_id}"
    except DatabaseError as e:
        print(f"Database error occurred: {e}")
        return "Failed to update tasks due to a database error"


@shared_task
def dispatch_check_task_expiration():
    User = get_user_model()
    users = User.objects.all()
    for user in users:
        check_task_expiration.delay(user_id=user.id)

# если у пользователя notifications = 1 and tg_id not None:
#   отправляем уведомление