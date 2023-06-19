import pytest

from Swipe.announcements.models import Announcement

pytestmark = pytest.mark.django_db


class TestAnnouncementModeration:
    endpoint = '/announcements/moderate/'

    def test_moderate_list(self, authenticated_admin_user, announcement):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.data['results']) > 0

    def test_moderate_announcement_retrieve(self, authenticated_admin_user, announcement):
        response = authenticated_admin_user.get(f'{self.endpoint}{announcement.id}/')
        assert response.status_code == 200

    def test_moderate_not_approved(self, authenticated_admin_user, announcement):
        payload = {
            "approved": False,
            "moderate_message": "Incorrect photo"
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{announcement.id}/', data=payload)
        assert response.status_code == 200

    def test_moderate_approved(self, authenticated_admin_user, announcement):
        payload = {
            "approved": True,
            "moderate_message": "Incorrect photo"
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{announcement.id}/', data=payload)
        assert response.status_code == 200
        assert response.data['moderate_message'] == ""
