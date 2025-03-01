import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestCustomTelegramUserModel:

    @pytest.fixture
    def user_data(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
            telegram_id='123456789',
            telegram_username='testuser_tg',
            notification=True
        )
        return user

    def test_user_creation(self, user_data):
        user = user_data
        assert user.username == 'testuser'
        assert user.telegram_id == '123456789'
        assert user.telegram_username == 'testuser_tg'
        assert user.notification is True

    def test_token_creation(self, user_data):
        user = user_data
        token = Token.objects.get(user=user)
        assert token is not None

    def test_user_update(self, user_data):
        user = user_data
        user.notification = False
        user.save()
        user.refresh_from_db()
        assert user.notification is False

    def test_user_deletion(self, user_data):
        user = user_data
        user.delete()
        assert not get_user_model().objects.filter(
            username='testuser'
            ).exists()
