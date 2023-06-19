import pytest

from Swipe.users.models import User

pytestmark = pytest.mark.django_db


class TestRegisterOwner:
    endpoint = '/register/owner/'

    def test_register(self, api_client):
        payload = {
            "email": "testowner@example.com",
            "password1": "Test12345",
            "password2": "Test12345"
        }
        response = api_client.post(self.endpoint, data=payload)
        assert response.status_code == 201
        assert User.objects.last().role == User.RoleName.OWNER

    def test_unique(self, api_client):
        payload = {
            "email": "test_unique@example.com",
            "password1": "Test12345",
            "password2": "Test12345"
        }
        api_client.post(self.endpoint, data=payload)
        response = api_client.post(self.endpoint, data=payload)
        assert response.status_code == 400
