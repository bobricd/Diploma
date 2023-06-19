import pytest


class TestFavouriteList:
    endpoint = '/users/favourite/'

    def test_favourite_list(self, authenticated_owner_user):
        response = authenticated_owner_user.get(self.endpoint)
        assert response.status_code == 200
