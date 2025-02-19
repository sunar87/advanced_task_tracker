from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomTelegramUser(AbstractUser):
    telegram_id = models.CharField(
        max_length=64,
        unique=True
    )
    telegram_username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    notification = models.BooleanField(default=False)
