import pytest

from Swipe.users.models import SubscriptionType

pytestmark = pytest.mark.django_db


class TestSubscriptionTypes:
    endpoint = '/users/subscription-types/'

    @pytest.fixture
    def subscription_type(self, admin_user, owner_user):
        subscription_type = SubscriptionType.objects.create(
            name="Test",
            price=25,
        )
        return subscription_type

    def test_subscription_type_list(self, authenticated_admin_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200

    def test_subscription_type_create(self, authenticated_admin_user):
        payload = {
            "name": "Test",
            "price": 25
        }
        response = authenticated_admin_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_subscription_type_retrieve(self, authenticated_admin_user, subscription_type):
        response = authenticated_admin_user.get(f'{self.endpoint}{subscription_type.id}/')
        assert response.status_code == 200

    def test_subscription_type_update(self, authenticated_admin_user, subscription_type):
        payload = {
            "name": "Test12121",
            "price": 555
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{subscription_type.id}/', data=payload)
        assert response.status_code == 200

    def test_subscription_type_delete(self, authenticated_admin_user, subscription_type):
        response = authenticated_admin_user.delete(f'{self.endpoint}{subscription_type.id}/')
        assert response.status_code == 204
