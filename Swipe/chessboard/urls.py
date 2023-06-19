from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Swipe.chessboard.views import ChessboardViewSet

router = DefaultRouter()
router.register(r'chessboard', ChessboardViewSet, basename="chessboard")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
