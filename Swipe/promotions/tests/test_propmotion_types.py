import pytest

pytestmark = pytest.mark.django_db


class TestPromotionType:
    endpoint = '/promotions/promotion-type/'

    def test_promotion_type_list(self, authenticated_owner_user, authenticated_admin_user, promotion_type_obj):
        response = authenticated_admin_user.get(self.endpoint)
        assert response.status_code == 200
        response = authenticated_owner_user.get(self.endpoint)
        assert response.status_code == 200

    def test_promotion_type_create(self, authenticated_admin_user):
        payload = {
          "effectivity": 100,
          "name": "Test",
          "price": 22
        }
        response = authenticated_admin_user.post(self.endpoint, data=payload)
        assert response.status_code == 201

    def test_promotion_type_retrieve(self, authenticated_admin_user, promotion_type_obj):
        response = authenticated_admin_user.get(f'{self.endpoint}{promotion_type_obj.id}/')
        assert response.status_code == 200

    def test_promotion_type_update(self, authenticated_admin_user, promotion_type_obj):
        payload = {
            "effectivity": 10,
            "name": "Test",
            "price": 22
        }
        response = authenticated_admin_user.put(f'{self.endpoint}{promotion_type_obj.id}/', data=payload)
        assert response.status_code == 200

    def test_promotion_type_delete(self, authenticated_admin_user, promotion_type_obj):
        response = authenticated_admin_user.delete(f'{self.endpoint}{promotion_type_obj.id}/')
        assert response.status_code == 204
