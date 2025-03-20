from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token

from users.models import CustomTelegramUser
from .models import Task


@login_required
def tasks(request):
    tasks = Task.objects.select_related(
        'category', 'user'
        ).prefetch_related(
            'tags'
            ).filter(
                user=request.user
            )
    token = None
    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        request.session['auth_token'] = token.key
    return render(request, 'tasks.html', {'tasks': tasks})


@csrf_exempt
def notifications(request):
    if request.method == 'POST':
        user_id = request.POST.get('telegram_id')
        user_email = request.POST.get('email')
        try:
            user_profile = CustomTelegramUser.objects.get(email=user_email)
            user_profile.telegram_id = user_id
            user_profile.notification = True
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


@login_required
def add_task(request):
    token = None
    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        request.session['auth_token'] = token.key
    return render(request, 'add_tasks.html', {'tasks': tasks})
