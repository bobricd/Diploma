import pytest

pytestmark = pytest.mark.django_db


class TestLogin:
    endpoint = '/login/'

    def test_login(self, api_client):
        payload = {
            'email': 'admin@admin.com',
            "password": 'Swipe12345'
        }
        response = api_client.post(self.endpoint, data=payload)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access_token"]}')
        assert response.status_code == 200
