import os
import random

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from Swipe.settings import BASE_DIR

pytestmark = pytest.mark.django_db


class TestAnnouncements:
    endpoint = '/announcements/announcement/'

    @staticmethod
    def get_images(count):
        dir_path = os.path.join(BASE_DIR, 'seed/announcements')
        images = []
        for _ in range(count):
            file_name = random.choice(os.listdir(dir_path))
            with open(os.path.join(dir_path, file_name), 'rb') as f:
                images.append(SimpleUploadedFile(name=file_name, content=f.read()))
        return images

    def test_announcement_list(self, authenticated_admin_user, announcement, announcement_moderated):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200
        assert len(response.data['results']) > 0

    def test_announcement_create(self, authenticated_owner_user):
        payload = {
            "images": self.get_images(5),
            "address": "test",
            "foundation_document": "Own",
            "destination": "Apartment",
            "number_rooms": 4,
            "layout": "Studio",
            "condition": "Need repair",
            "area": 55,
            "kitchen_area": 33,
            "has_balcony": True,
            "heating_type": "Gas",
            "payment_option": "Cash",
            "agent_commission": 500,
            "communication_method": "Messages",
            "description": "Test",
            "price": 200000,
        }
        response = authenticated_owner_user.post(self.endpoint, data=payload)
        assert response.status_code == 201
        payload['kitchen_area'] = 80
        response = authenticated_owner_user.post(self.endpoint, data=payload)
        assert response.status_code == 400

    def test_announcement_retrieve(self, authenticated_owner_user, announcement, announcement_moderated):
        response = authenticated_owner_user.get(f'{self.endpoint}{announcement.id}/')
        assert response.status_code == 404
        response = authenticated_owner_user.get(f'{self.endpoint}{announcement_moderated.id}/')
        assert response.status_code == 200

    #
    def test_announcement_update(self, authenticated_owner_user, announcement_moderated):
        images = [image.id for image in announcement_moderated.images.all()]
        new_images = self.get_images(2)
        payload = {
            "images": images,
            "new_images": new_images,
            "address": "test",
            "foundation_document": "Own",
            "destination": "Apartment",
            "number_rooms": 4,
            "layout": "Studio",
            "condition": "Need repair",
            "area": 55,
            "kitchen_area": 33,
            "has_balcony": True,
            "heating_type": "Gas",
            "payment_option": "Cash",
            "agent_commission": 500,
            "communication_method": "Messages",
            "description": "Test",
            "price": 200000,
        }
        response = authenticated_owner_user.put(f'{self.endpoint}{announcement_moderated.id}/', data=payload)
        assert response.status_code == 200
        assert len(response.data['images']) == len(new_images) + len(images)

    def test_announcement_delete(self, authenticated_owner_user, announcement_moderated, announcement):
        response = authenticated_owner_user.delete(f'{self.endpoint}{announcement_moderated.id}/')
        assert response.status_code == 204
        response = authenticated_owner_user.delete(f'{self.endpoint}{announcement.id}/')
        assert response.status_code == 404

    def test_announcement_my_list(self, authenticated_owner_user, announcement_moderated, announcement):
        response = authenticated_owner_user.get(f'{self.endpoint}announcement_my_list/')
        assert response.status_code == 200
        assert len(response.data['results']) == 2

    def test_announcement_to_residential_complex(self, authenticated_owner_user, announcement_moderated, announcement):
        response = authenticated_owner_user.post(
            f'{self.endpoint}{announcement_moderated.id}/to_residential_complex/')
        assert response.status_code == 400
