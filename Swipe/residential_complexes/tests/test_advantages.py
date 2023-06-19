import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from Swipe.settings import BASE_DIR

pytestmark = pytest.mark.django_db


class TestAdvantages:
    endpoint = '/residential-complexes/advantages/'

    @staticmethod
    def get_logo():
        logo_path = os.path.join(BASE_DIR, 'seed/residential_complexes/4926341.png')
        with open(logo_path, 'rb') as f:
            logo_data = f.read()
        return SimpleUploadedFile(name='logo.png', content=logo_data, content_type='image/png')

    def test_advantage_list(self, authenticated_builder_user, authenticated_admin_user):
        response = authenticated_builder_user.get(self.endpoint)
        assert response.status_code == 200
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200

    def test_advantage_create(self, authenticated_admin_user):
        payload = {
          "name": 'Test',
          "logo": self.get_logo()
        }
        response = authenticated_admin_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_advantage_retrieve(self, authenticated_admin_user, advantage):
        response = authenticated_admin_user.get(f'{self.endpoint}{advantage.id}/')
        assert response.status_code == 200

    def test_advantage_update(self, authenticated_admin_user, advantage):
        payload = {
            "name": '123123',
            "logo": self.get_logo()
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{advantage.id}/', data=payload)
        assert response.status_code == 200

    def test_advantage_delete(self, authenticated_admin_user, advantage):
        response = authenticated_admin_user.delete(f'{self.endpoint}{advantage.id}/')
        assert response.status_code == 204
