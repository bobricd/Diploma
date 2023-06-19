import pytest
from dateutil.relativedelta import relativedelta
from django.utils import timezone

from Swipe.users.models import SubscriptionType, Subscription

pytestmark = pytest.mark.django_db


class TestSubscriptions:
    endpoint = '/users/subscriptions/'

    @pytest.fixture
    def subscription_type(self):
        subscription_type = SubscriptionType.objects.create(
            name="Test",
            price=25,
        )
        return subscription_type

    @pytest.fixture
    def subscription(self, owner_user, subscription_type):
        subscription_type = Subscription.objects.create(
            owner=owner_user,
            date=timezone.now().date() + relativedelta(months=1),
            subscription_type=subscription_type,
            auto_renewal=True
        )
        return subscription_type

    def test_subscription_list(self, authenticated_admin_user):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200

    def test_subscription_create(self, authenticated_owner_user, subscription_type, owner_user):
        payload = {
            "auto_renewal": True,
            "subscription_type": subscription_type.id,
            "owner": owner_user.id,
            "date": timezone.now().date() + relativedelta(months=1)
        }
        response = authenticated_owner_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_subscription_retrieve(self, authenticated_admin_user, authenticated_owner_user, subscription):
        response = authenticated_admin_user.get(f'{self.endpoint}{subscription.id}/')
        assert response.status_code == 200
        response = authenticated_owner_user.get(f'{self.endpoint}{subscription.id}/')
        assert response.status_code == 200

    def test_subscription_update(self, authenticated_admin_user, owner_user, subscription):
        payload = {
            "auto_renewal": False,
            "subscription_type": subscription.subscription_type.id,
            "owner": owner_user.id,
            "date": timezone.now().date()
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{subscription.id}/', data=payload)
        assert response.status_code == 200

    def test_subscription_delete(self, authenticated_admin_user, subscription):
        response = authenticated_admin_user.delete(f'{self.endpoint}{subscription.id}/')
        assert response.status_code == 204
