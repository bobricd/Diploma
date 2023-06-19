import pytest

pytestmark = pytest.mark.django_db


class TestChessboard:
    endpoint = '/announcements/application/'

    def test_chessboard_section_list(self, authenticated_builder_user, announcement_moderated_with_rc, floor, riser):
        announcement_moderated_with_rc.floor = floor
        announcement_moderated_with_rc.riser = riser
        announcement_moderated_with_rc.save()
        response = authenticated_builder_user.get(f'/chessboards/chessboard/chessboard-list/{floor.section.id}/')
        assert response.status_code == 200
        assert len(response.data) == 1

    def test_chessboard_announcement_retrieve(self, authenticated_builder_user,
                                              announcement_moderated_with_rc, floor, riser):
        announcement_moderated_with_rc.floor = floor
        announcement_moderated_with_rc.riser = riser
        announcement_moderated_with_rc.save()
        response = authenticated_builder_user.get(
            f'/chessboards/chessboard/chessboard-announcement/{announcement_moderated_with_rc.id}/')
        assert response.status_code == 200
