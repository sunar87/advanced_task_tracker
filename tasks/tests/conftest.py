import pytest
from django.contrib.auth import get_user_model    
from django.utils import timezone
from tasks.models import Task, Tags, Category
from tasks.const import ACTIVE, MEDIUM


@pytest.fixture
def setup_data():
    user = get_user_model().objects.create_user(
        username='testuser',
        password='password',
        telegram_id='311234'
    )
    tag1 = Tags.objects.create(name='Tag1')
    tag2 = Tags.objects.create(name='Tag2')
    category = Category.objects.create(name='Category1')
    task = Task.objects.create(
        user=user,
        title='Test Task',
        description='This is a test task.',
        status=ACTIVE,
        priority=MEDIUM,
        category=category,
        expired_at=timezone.now() + timezone.timedelta(days=1)
    )
    task.tags.add(tag1, tag2)

    return task, tag1, tag2, category, user
