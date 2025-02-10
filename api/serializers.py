from rest_framework import serializers
from tasks.models import Tags, Category, Task


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(
        many=True,
        read_only=True
    )
    category = CategorySerializer(
        read_only=True
    )

    class Meta:
        model = Task
        fields = '__all__'
