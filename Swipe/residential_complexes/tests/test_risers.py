import pytest

pytestmark = pytest.mark.django_db


class TestRisers:
    endpoint = '/residential-complexes/risers/'

    def test_risers_list(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_risers_create(self, authenticated_builder_user, section):
        payload = {
            "number": 1,
            "section": section.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_risers_unique_create(self, authenticated_builder_user, residential_complex, riser):
        payload = {
            "number": 1,
            "section": riser.section.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 400

    def test_risers_retrieve(self, authenticated_builder_user, riser):
        response = authenticated_builder_user.get(f'{self.endpoint}{riser.id}/')
        assert response.status_code == 200

    def test_risers_update(self, authenticated_builder_user, riser):
        payload = {
            "number": 2,
            "section": riser.section.id
        }
        response = authenticated_builder_user.put(f'{self.endpoint}{riser.id}/', data=payload)
        assert response.status_code == 200
        assert response.data['number'] == payload['number']

    def test_risers_delete(self, authenticated_builder_user, riser):
        response = authenticated_builder_user.delete(f'{self.endpoint}{riser.id}/')
        assert response.status_code == 204
