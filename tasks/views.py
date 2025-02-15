from django.shortcuts import render

from .models import Task


def tasks(request):
    tasks = Task.objects.select_related(
        'category', 'user'
        ).prefetch_related(
            'tags'
            )
    return render(request, 'tasks.html', {'tasks': tasks})
