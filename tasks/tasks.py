from django.db import transaction, DatabaseError
from celery import shared_task
import logging

from .service import TaskService
from users.models import CustomTelegramUser
from .const import MSG
from .management.commands.telegram import send_message_sync

logger = logging.getLogger(__name__)


@shared_task
def expired_tasks():
    total_updated_tasks = 0
    users = CustomTelegramUser.objects.all()

    for user in users:
        tasks = TaskService.get_expired_tasks(user_id=user.id)

        if tasks.exists():
            if user.notification:
                titles = [task.title for task in tasks]
                message = MSG.format('\n'.join(titles))
                send_message_sync(chat_id=user.telegram_id, message=message)
                logger.info(f"Sent notification to user {user.id} with {tasks.count()} expired tasks")
            with transaction.atomic:
                tasks.update(status='expired')
                total_updated_tasks += tasks.count()

    logger.info(f"Updated a total of {total_updated_tasks} tasks to 'expired' status")
    return f'Updated {total_updated_tasks} tasks'
