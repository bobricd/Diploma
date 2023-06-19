import pytest

pytestmark = pytest.mark.django_db


class TestUserList:
    endpoint = '/users/'

    def test_user_list(self, authenticated_admin_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200
