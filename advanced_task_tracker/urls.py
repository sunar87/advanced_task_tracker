from django.contrib import admin
from django.urls import path, include

from users.views import login_view\

app_name = 'main'

urlpatterns = [
    path('', include('api.urls')),
    path('', include('tasks.urls')),
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('api/', include('users.urls'))
]
