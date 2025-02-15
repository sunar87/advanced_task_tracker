from rest_framework import serializers
from tasks.models import Tags, Category, Task


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class TaskSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    tags = TagsSerializer(many=True)
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Task
        fields = ['title', 'description', 'category',
                  'tags', 'status', 'priority',
                  'user', 'created_at']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        category_data = validated_data.pop('category')
        category_instance = Category.objects.get(name=category_data['name'])

        task = Task.objects.create(
            **validated_data, category=category_instance
            )

        for tag_data in tags_data:
            tag_instance = Tags.objects.get(name=tag_data['name'])
            task.tags.add(tag_instance)

        return task
