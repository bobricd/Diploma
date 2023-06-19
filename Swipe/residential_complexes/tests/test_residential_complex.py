import json
import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from Swipe.settings import BASE_DIR

pytestmark = pytest.mark.django_db


class TestResidentialComplexes:
    endpoint = '/residential-complexes/'

    def test_residential_complexes_list(self, authenticated_owner_user):
        response = authenticated_owner_user.get(f'{self.endpoint}list/')
        assert response.status_code == 200

    def test_residential_complexes_create(self, authenticated_builder_user, advantage):
        payload = {
            "advantages": [
                advantage.id
            ],
            "images": [
                {
                    "image": "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7",
                    "order": 1
                }
            ],
            "name": "test",
            "description": "test",
            "address": "test",
            "contact_first_name": "test",
            "contact_last_name": "test",
            "contact_phone": "+380731112222",
            "contact_email": "user@example.com",
            "house_status": "apartments",
            "house_type": "multiFamily",
            "house_class": "economy",
            "construction": "precastFoundations",
            "territory": "open",
            "communal_payments": "payments",
            "ceiling_height": 5,
            "distance_to_sea": 55
        }
        json_payload = json.dumps(payload)

        response = authenticated_builder_user.post(f'/residential-complexes/create/', data=json_payload,
                                                   content_type='application/json')
        assert response.status_code == 201
        response = authenticated_builder_user.post(f'{self.endpoint}create/', data=json_payload,
                                                   content_type='application/json')
        assert response.status_code == 400

    def test_residential_complexes_news_create(self, authenticated_builder_user, residential_complex):
        payload = {
            "title": "Test",
            "text": "Test"
        }
        response = authenticated_builder_user.post(f'{self.endpoint}news/create/', data=payload)
        assert response.status_code == 201
        residential_complex.delete()
        response = authenticated_builder_user.post(f'{self.endpoint}news/create/', data=payload)
        assert response.status_code == 400

    def test_residential_complexes_document_create(self, authenticated_builder_user, residential_complex):
        image_path = os.path.join(BASE_DIR, 'seed/residential_complexes/4926341.png')
        with open(image_path, 'rb') as f:
            image_data = f.read()
        file = SimpleUploadedFile(name='test_file.png', content=image_data)
        payload = {
            "file": file,
            "is_excel": "True"
        }
        response = authenticated_builder_user.post(f'{self.endpoint}document/create/', data=payload)
        assert response.status_code == 201
        residential_complex.delete()
        response = authenticated_builder_user.post(f'{self.endpoint}document/create/', data=payload)
        assert response.status_code == 400
