import pytest

from Swipe.users.models import User

pytestmark = pytest.mark.django_db


class TestUserBlackList:

    def test_user_blacklist(self, authenticated_admin_user):
        response = authenticated_admin_user.get('/users/blacklist/')
        assert response.status_code == 200

    def test_user_to_blacklist(self, authenticated_admin_user, owner_user):
        response = authenticated_admin_user.post(f'/users/to-black-list/{owner_user.id}/')
        assert response.status_code == 200
        response = authenticated_admin_user.get('/users/blacklist/')
        assert len(response.data['results']) > 0

    def test_user_remove_from_blacklist(self, authenticated_admin_user, owner_user):
        response = authenticated_admin_user.delete(f'/users/remove-from-black-list/{owner_user.id}/')
        assert response.status_code == 200
