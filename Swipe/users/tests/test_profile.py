import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from Swipe.settings import BASE_DIR

pytestmark = pytest.mark.django_db


class TestUserProfile:
    endpoint = '/users/profile/'

    def test_profile_retrieve(self, authenticated_admin_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200

    def test_profile_update(self, authenticated_admin_user):
        image_path = os.path.join(BASE_DIR, 'seed/users/profile_image.png')
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image_file = SimpleUploadedFile(name='test_image.png', content=image_data, content_type='image/png')
        payload = {
            "email": "admin@admin.com",
            "profile_image": image_file,
            "first_name": "Admin",
            "last_name": "Admin",
            "phone": "+380731112448",
            "agent_first_name": "agent",
            "agent_last_name": "agent",
            "agent_phone": "+380638881652",
            "agent_email": "user@example.com",
            "switch_to_agent": False
        }
        response = authenticated_admin_user.put(self.endpoint, payload, format='multipart')
        assert response.status_code == 200
