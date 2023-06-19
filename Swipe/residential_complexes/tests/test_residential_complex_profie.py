import pytest

pytestmark = pytest.mark.django_db


class TestResidentialComplexProfile:
    endpoint = '/residential-complexes/profile/'

    def test_profile_retrieve(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_profile_delete(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.delete(self.endpoint)
        assert response.status_code == 204
