from django.contrib import admin

from .models import Task, Tags, Category
from users.models import CustomTelegramUser


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',
                    'status', 'priority')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(CustomTelegramUser)
class CategoryUser(admin.ModelAdmin):
    pass
