from django.db import models
from django.contrib.auth.models import User

from .const import STATUS_CHOICES, PRIORITY_CHOICES, ACTIVE, MEDIUM


class Tags(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categorys'

    def __str__(self):
        return self.name


class Task(models.Model):
    tags = models.ManyToManyField(
        Tags,
        related_name='tags',
        blank=True
        )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='category',
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=128)
    description = models.TextField()
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default=ACTIVE
        )
    priority = models.CharField(
        max_length=32,
        choices=PRIORITY_CHOICES,
        default=MEDIUM
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category']),
            models.Index(fields=['-created_at']),
        ]
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return self.title
