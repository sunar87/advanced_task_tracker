from django.urls import path

from . import views

urlpatterns = [
    path('api/tags/', views.TagsGetView.as_view(), name='tags'),
    path('api/tags/<int:tag_id>/', views.TagDetailView.as_view(), name='tag_detail'),
    path('api/categorys/', views.CategoryView.as_view(), name='categorys'),
    path('api/categorys/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('api/tasks/', views.TaskView.as_view(), name='tasks')
]
