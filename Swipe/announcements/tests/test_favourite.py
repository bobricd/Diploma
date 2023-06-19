import pytest

pytestmark = pytest.mark.django_db


class TestAnnouncementsFavourite:

    def test_add_to_favourite(self, authenticated_owner_user, announcement_moderated):
        response = authenticated_owner_user.post(
            f'/announcements/announcement/add-to-favourite/{announcement_moderated.id}/')
        assert response.status_code == 200

    def test_remove_from_favourite(self, authenticated_owner_user, announcement_moderated):
        response = authenticated_owner_user.delete(
            f'/announcements/announcement/remove-from-favourite/{announcement_moderated.id}/')
        assert response.status_code == 204
