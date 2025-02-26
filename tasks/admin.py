from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

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
class CustomTelegramUserAdmin(UserAdmin):
    list_display = ('username', 'telegram_id', 'telegram_username', 'notification', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Telegram Data', {'fields': ('telegram_id', 'telegram_username', 'notification')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Telegram Data', {'fields': ('telegram_id', 'telegram_username', 'notification')}),
    )
