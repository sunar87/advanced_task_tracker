from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class CustomTelegramUser(AbstractUser):
    telegram_id = models.CharField(
        max_length=64,
        unique=True,
        null=True,
        blank=True
    )
    telegram_username = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    notification = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Token.objects.create(user=self)
