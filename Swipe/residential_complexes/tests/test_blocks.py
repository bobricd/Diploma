import pytest

pytestmark = pytest.mark.django_db


class TestBlocks:
    endpoint = '/residential-complexes/blocks/'

    def test_blocks_list(self, authenticated_builder_user, residential_complex):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200

    def test_blocks_create(self, authenticated_builder_user, residential_complex):
        payload = {
            "name": "Test"
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_blocks_unique_create(self, authenticated_builder_user, residential_complex, block):
        payload = {
            "name": "Block 1"
        }
        response = authenticated_builder_user.post(self.endpoint, data=payload)
        assert response.status_code == 400

    def test_blocks_retrieve(self, authenticated_builder_user, block):
        response = authenticated_builder_user.get(f'{self.endpoint}{block.id}/')
        assert response.status_code == 200

    def test_blocks_update(self, authenticated_builder_user, block):
        payload = {
            "name": "Block 2"
        }
        response = authenticated_builder_user.put(f'{self.endpoint}{block.id}/', data=payload)
        assert response.status_code == 200
        assert response.data['name'] == payload['name']

    def test_blocks_delete(self, authenticated_builder_user, block):
        response = authenticated_builder_user.delete(f'{self.endpoint}{block.id}/')
        assert response.status_code == 204
