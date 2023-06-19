import pytest

pytestmark = pytest.mark.django_db


class TestResidentialComplexFavourite:

    def test_add_to_favourite(self, authenticated_owner_user, residential_complex):
        response = authenticated_owner_user.post(
            f'/residential-complexes/add-to-favourite/{residential_complex.id}/')
        assert response.status_code == 200
        response = authenticated_owner_user.post(
            f'/residential-complexes/add-to-favourite/5/')
        assert response.status_code == 404

    def test_remove_from_favourite(self, authenticated_owner_user, residential_complex):
        response = authenticated_owner_user.delete(
            f'/residential-complexes/remove-from-favourite/{residential_complex.id}/')
        assert response.status_code == 204
        response = authenticated_owner_user.delete(
            f'/residential-complexes/remove-from-favourite/5/')
        assert response.status_code == 404
