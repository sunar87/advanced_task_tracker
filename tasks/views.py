from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from users.models import CustomTelegramUser
from .models import Task


def tasks(request):
    tasks = Task.objects.select_related(
        'category', 'user'
        ).prefetch_related(
            'tags'
            )
    return render(request, 'tasks.html', {'tasks': tasks})


@csrf_exempt
def notifications(request):
    if request.method == 'POST':
        user_id = request.POST.get('telegram_id')
        user_email = request.POST.get('email')
        try:
            user_profile = CustomTelegramUser.objects.get(email=user_email)
            user_profile.telegram_id = user_id
            user_profile.save()
            return JsonResponse(
                {'status': 'success', 'message': 'Telegram id linked successfuly'}
                )
        except CustomTelegramUser.DoesNotExist:
            return JsonResponse(
                {'status': 'error', 'message': 'User not found'}, status=404
                )
    return JsonResponse(
        {'status': 'error', 'message': 'Invalid request'}, status=400
        )
