import pytest

pytestmark = pytest.mark.django_db


class TestApplications:
    endpoint = '/announcements/application/'

    def test_applications_list(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_applications_add(self, authenticated_owner_user, announcement_moderated_with_rc):
        response = authenticated_owner_user.post(
            f'/announcements/announcement/{announcement_moderated_with_rc.id}/to_residential_complex/')
        assert response.status_code == 200

    def test_applications_update(self, authenticated_builder_user, application, floor, riser):
        payload = {
            "floor": floor.id,
            "riser": riser.id
        }
        response = authenticated_builder_user.put(f'{self.endpoint}{application.id}/', data=payload)
        assert response.status_code == 200

    def test_applications_retrieve(self, authenticated_builder_user, application):
        response = authenticated_builder_user.get(f'{self.endpoint}{application.id}/')
        assert response.status_code == 200

    def test_applications_delete(self, authenticated_builder_user, application):
        response = authenticated_builder_user.delete(f'{self.endpoint}{application.id}/')
        assert response.status_code == 204
