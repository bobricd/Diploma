import pytest
from Swipe.notaries.models import Notary

pytestmark = pytest.mark.django_db


class TestNotaries:
    endpoint = '/notaries/'

    @pytest.fixture
    def notary(self):
        notary = Notary.objects.create(
            first_name="Test",
            last_name="Test",
            phone='+380731111111',
            email='test@gamil.com'
        )
        return notary

    def test_notary_list(self, authenticated_admin_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200

    def test_notary_create(self, authenticated_admin_user):
        payload = {
            "first_name": "Test",
            "last_name": "Test",
            "phone": '+380738882244',
            "email": 'test@gamil.com'
        }
        response = authenticated_admin_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_notary_retrieve(self, authenticated_admin_user, notary):
        response = authenticated_admin_user.get(f'{self.endpoint}{notary.id}/')
        assert response.status_code == 200

    def test_subscription_update(self, authenticated_admin_user, notary):
        payload = {
            "first_name": "asdas",
            "last_name": "aaa",
            "phone": '+380738882244',
            "email": 'test@gamil.com'
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{notary.id}/', data=payload)
        assert response.status_code == 200

    def test_subscription_delete(self, authenticated_admin_user, notary):
        response = authenticated_admin_user.delete(f'{self.endpoint}{notary.id}/')
        assert response.status_code == 204
