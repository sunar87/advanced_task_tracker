from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token


app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/token/', obtain_auth_token, name='token'),
]
