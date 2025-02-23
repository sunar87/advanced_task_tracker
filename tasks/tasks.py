from django.db import transaction, DatabaseError
from celery import shared_task

from .service import TaskService
from users.models import CustomTelegramUser
from .const import MSG
from .management.commands.telegram import send_message_sync


@shared_task
def check_task_expiration(user_id):
    try:
        with transaction.atomic():
            expired_tasks = TaskService.get_expired_tasks(user_id=user_id)
            custom_user = CustomTelegramUser.objects.filter(
                id=user_id
            ).first()
            if custom_user and custom_user.telegram_id:
                titles = [task.title for task in expired_tasks]
                expired_tasks.update(status='expired')
                if titles:
                    message = MSG.format('\n'.join(titles))
                    send_message_sync(
                        chat_id=custom_user.telegram_id, message=message
                    )
                    return f"Updated {expired_tasks.count()} tasks to 'expired' status for user {user_id}"
                return 'There no tasks'
    except DatabaseError as e:
        print(f"Database error occurred: {e}")
        return "Failed to update tasks due to a database error"
    
# Баг в вычислении titles при обновлении статуса приходит пустой queryset


@shared_task
def dispatch_check_task_expiration():
    users = CustomTelegramUser.objects.filter(notification=True).distinct()
    for user in users:
        check_task_expiration.delay(user_id=user.id)
