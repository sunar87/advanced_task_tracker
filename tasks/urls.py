from django.urls import path

from . import views

app_name = 'tasks'

urlpatterns = [
    path('tasks/', views.tasks, name='task_list'),
    path('tasks/add/', views.add_task, name='add_task'),
    path('tasks/notifications/', views.notifications, name='notifications')
]
