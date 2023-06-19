import pytest

pytestmark = pytest.mark.django_db


class TestRisers:
    endpoint = '/residential-complexes/floors/'

    def test_floors_list(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_floors_create(self, authenticated_builder_user, section):
        payload = {
            "number": 1,
            "section": section.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_floors_unique_create(self, authenticated_builder_user, residential_complex, floor):
        payload = {
            "number": 1,
            "section": floor.section.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 400

    def test_floors_retrieve(self, authenticated_builder_user, floor):
        response = authenticated_builder_user.get(f'{self.endpoint}{floor.id}/')
        assert response.status_code == 200

    def test_floors_update(self, authenticated_builder_user, floor):
        payload = {
            "number": 2,
            "section": floor.section.id
        }
        response = authenticated_builder_user.put(f'{self.endpoint}{floor.id}/', data=payload)
        assert response.status_code == 200
        assert response.data['number'] == payload['number']

    def test_floors_delete(self, authenticated_builder_user, floor):
        response = authenticated_builder_user.delete(f'{self.endpoint}{floor.id}/')
        assert response.status_code == 204
