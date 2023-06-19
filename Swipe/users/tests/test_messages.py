import os
import random
import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from Swipe.users.models import Message

pytestmark = pytest.mark.django_db


class TestMessages:
    endpoint = '/users/messages/'

    @pytest.fixture
    def message_owner(self, owner_user, admin_user):
        message = Message.objects.create(
            sender=owner_user,
            text='test message',
            file=self.get_message_file(),
            receiver=admin_user
        )
        return message

    @pytest.fixture
    def message_admin(self, admin_user, owner_user):
        message = Message.objects.create(
            sender=admin_user,
            text='test message',
            file=self.get_message_file(),
            receiver=owner_user
        )
        return message

    @staticmethod
    def get_message_file():
        dir_path = os.path.join(os.getcwd(), 'seed/messages')
        file_name = random.choice(os.listdir(dir_path))
        with open(os.path.join(dir_path, file_name), 'rb') as f:
            file_data = f.read()
        return SimpleUploadedFile(name=file_name, content=file_data)

    def test_messages_list(self, authenticated_admin_user, authenticated_owner_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200
        response = authenticated_owner_user.get(self.endpoint)
        assert response.status_code == 200

    def test_message_owner_send(self, authenticated_owner_user):
        payload = {
            "text": "test",
            "file": self.get_message_file()
        }
        response = authenticated_owner_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_message_admin_send(self, authenticated_admin_user, owner_user):
        payload = {
            "text": "test",
            "file": self.get_message_file(),
            "receiver": owner_user.id
        }
        response = authenticated_admin_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_message_retrieve_owner(self, authenticated_owner_user, message_admin, message_owner):
        response = authenticated_owner_user.get(f'{self.endpoint}{message_owner.id}/')
        assert response.status_code == 200
        response = authenticated_owner_user.get(f'{self.endpoint}{message_admin.id}/')
        assert response.status_code == 403

    def test_message_retrieve_admin(self, authenticated_admin_user, message_admin, message_owner):
        response = authenticated_admin_user.get(f'{self.endpoint}{message_owner.id}/')
        assert response.status_code == 403
        response = authenticated_admin_user.get(f'{self.endpoint}{message_admin.id}/')
        assert response.status_code == 200

    def test_message_update(self, authenticated_owner_user, message_admin, message_owner):
        payload = {
            "text": "test",
            "file": self.get_message_file()
        }
        response = authenticated_owner_user.put(f'{self.endpoint}{message_owner.id}/', data=payload)
        assert response.status_code == 200
        response = authenticated_owner_user.put(f'{self.endpoint}{message_admin.id}/', data=payload)
        assert response.status_code == 403

    def test_message_delete(self, authenticated_owner_user, message_admin, message_owner):
        response = authenticated_owner_user.delete(f'{self.endpoint}{message_owner.id}/')
        assert response.status_code == 204
        response = authenticated_owner_user.delete(f'{self.endpoint}{message_admin.id}/')
        assert response.status_code == 403
