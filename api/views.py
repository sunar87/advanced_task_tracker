from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAdminUser,
    AllowAny,
    IsAuthenticated
    )
from rest_framework import (
    status,
    generics
    )
import django_filters

from .serializers import (
    TagsSerializer,
    CategorySerializer,
    TaskSerializer
    )
from tasks.models import (
    Tags,
    Category,
    Task
    )
from .filters import TaskFilter
from .const import CHANGE_METHODS


class TagsView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        queryset = Tags.objects.prefetch_related('tags').all()
        serializer = TagsSerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = TagsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailView(APIView):

    def get_permissions(self):
        if self.request.method in CHANGE_METHODS:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get(self, request, tag_id):
        try:
            queryset = Tags.objects.get(id=tag_id)
        except Tags.DoesNotExist:
            return Response(
                {"detail": "Tag not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TagsSerializer(queryset)
        return Response(serializer.data)

    def put(self, request, tag_id):
        try:
            queryset = Tags.objects.get(id=tag_id)
        except Tags.DoesNotExist:
            return Response(
                {"detail": "Tag not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TagsSerializer(
            instance=queryset,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, tag_id):
        try:
            queryset = Tags.objects.get(id=tag_id)
        except Tags.DoesNotExist:
            return Response(
                {'detail': 'Tag not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryView(APIView):

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]

    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(
            instance=queryset,
            many=True
        )
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):

    def get_permissions(self):
        if self.request.method in CHANGE_METHODS:
            return [IsAuthenticated(), IsAdminUser()]
        return [AllowAny()]

    def get(self, request, category_id):
        try:
            queryset = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(queryset)
        return Response(serializer.data)

    def put(self, request, category_id):
        try:
            queryset = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(
            instance=queryset,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, category_id):
        try:
            queryset = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {'detail': 'Category not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskListView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = TaskFilter

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return Response(
            {'detail': 'Объект изменен успешно'}, status=status.HTTP_200_OK
            )

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response(
            {'detail': 'Объект удален успешно'}, status=status.HTTP_200_OK
            )
