import pytest

pytestmark = pytest.mark.django_db


class TestSections:
    endpoint = '/residential-complexes/sections/'

    def test_sections_list(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_sections_create(self, authenticated_builder_user, block):
        payload = {
            "number": 1,
            "block": block.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_sections_unique_create(self, authenticated_builder_user, residential_complex, section):
        payload = {
            "number": 1,
            "block": section.block.id
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 400

    def test_sections_retrieve(self, authenticated_builder_user, section):
        response = authenticated_builder_user.get(f'{self.endpoint}{section.id}/')
        assert response.status_code == 200

    def test_sections_update(self, authenticated_builder_user, section):
        payload = {
            "number": 2,
            "block": section.block.id
        }
        response = authenticated_builder_user.put(f'{self.endpoint}{section.id}/', data=payload)
        assert response.status_code == 200
        assert response.data['number'] == payload['number']

    def test_sections_delete(self, authenticated_builder_user, section):
        response = authenticated_builder_user.delete(f'{self.endpoint}{section.id}/')
        assert response.status_code == 204
