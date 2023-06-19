import pytest

pytestmark = pytest.mark.django_db


class TestSetPromotion:

    def test_set_promotion(self, authenticated_owner_user, announcement_moderated, promotion_type_obj):
        payload = {
            "promotion_type": promotion_type_obj.id,
        }
        response = authenticated_owner_user.put(
            f'/announcements/announcement/{announcement_moderated.id}/set_promotion/', data=payload)
        assert response.status_code == 200
