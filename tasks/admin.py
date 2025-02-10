from django.contrib import admin

from .models import Task, Tags, Category


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
