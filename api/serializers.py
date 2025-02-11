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
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
        )
    tags = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Tags.objects.all(), allow_null=True
        )

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        category = validated_data.pop('category')
        task = Task.objects.create(**validated_data, category=category)
        for tag in tags:
            task.tags.add(tag)
        return task
