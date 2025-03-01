import pytest
from django.urls import reverse

from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestTasksView:

    def test_tasks_view_authenticated(self, client, setup_data):
        task, tag1, tag2, category, user = setup_data
        login_successful = client.login(
            username=user.username, password='password'
            )
        assert login_successful, "Login failed"
        response = client.get(reverse('tasks:task_list'))
        assert response.status_code == 200
        assert list(response.context['tasks']) == [task]
        assert 'auth_token' in client.session
        token = Token.objects.get(user=user)
        assert client.session['auth_token'] == token.key
