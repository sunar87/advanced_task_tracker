import pytest

from tasks.models import Task
from tasks.const import ACTIVE, MEDIUM


@pytest.mark.django_db
class TestTaskModel:

    def test_task_creation(self, setup_data):
        task, tag1, tag2, category, user = setup_data

        assert task.title == 'Test Task'
        assert task.description == 'This is a test task.'
        assert task.status == ACTIVE
        assert task.priority == MEDIUM
        assert task.user == user
        assert task.category == category
        assert tag1 in task.tags.all()
        assert tag2 in task.tags.all()
        assert task.expired_at is not None

    def test_task_str_method(self, setup_data):
        task, _, _, _, _ = setup_data
        assert str(task) == 'Test Task'

    def test_task_ordering(self, setup_data):
        task, _, _, _, _ = setup_data
        assert list(Task.objects.all()) == [task]

    def test_task_indexes(self, setup_data):
        task, _, _, _, _ = setup_data
        assert Task._meta.indexes

    def test_task_tags_relation(self, setup_data):
        task, tag1, tag2, _, _ = setup_data
        assert task.tags.count() == 2
        assert task.tags.filter(name='Tag1').exists()
        assert task.tags.filter(name='Tag2').exists()

    def test_task_category_relation(self, setup_data):
        task, _, _, category, _ = setup_data
        assert task.category == category
