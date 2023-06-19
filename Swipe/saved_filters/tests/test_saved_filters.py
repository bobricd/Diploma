import pytest

from Swipe.saved_filters.models import SavedFilters

pytestmark = pytest.mark.django_db


class TestSavedFilters:
    endpoint = '/saved-filters/'

    @pytest.fixture
    def saved_filters_obj(self, owner_user):
        saved_filters_obj = SavedFilters.objects.create(
            user=owner_user,
            min_price=10,
            max_price=5000,
            min_area=25,
            max_area=400,
            microdistrict="test",
            district="test",
            house_status="apartments",
            condition="Need repair",
            payment_option="Cash",
            number_rooms=5,
            destination="Apartment"
        )
        return saved_filters_obj

    def test_saved_filters_list(self, authenticated_owner_user):
        response = authenticated_owner_user.get(self.endpoint)
        assert response.status_code == 200

    def test_saved_filters_create(self, authenticated_owner_user):
        payload = {
          "min_price": 50,
          "max_price": 555,
          "min_area": 55,
          "max_area": 5555,
          "microdistrict": "test",
          "district": "test",
          "house_status": "apartments",
          "condition": "Need repair",
          "payment_option": "Cash",
          "number_rooms": 88,
          "destination": "Apartment"
        }
        response = authenticated_owner_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_saved_filters_retrieve(self, authenticated_owner_user, saved_filters_obj):
        response = authenticated_owner_user.get(f'{self.endpoint}{saved_filters_obj.id}/')
        assert response.status_code == 200

    def test_subscription_update(self, authenticated_owner_user, saved_filters_obj):
        payload = {
          "min_price": 88,
          "max_price": 8888,
          "min_area": 8,
          "max_area": 88,
          "microdistrict": "test1",
          "district": "test2",
          "house_status": "apartments",
          "condition": "Need repair",
          "payment_option": "Cash",
          "number_rooms": 1,
          "destination": "Apartment"
        }
        response = authenticated_owner_user.put(f'{self.endpoint}{saved_filters_obj.id}/', data=payload)
        assert response.status_code == 200

    def test_subscription_delete(self, authenticated_owner_user, saved_filters_obj):
        response = authenticated_owner_user.delete(f'{self.endpoint}{saved_filters_obj.id}/')
        assert response.status_code == 204
