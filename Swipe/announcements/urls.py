from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Swipe.announcements.views import AnnouncementViewSet, AnnouncementModerateViewSet, ApplicationsViewSet

router = DefaultRouter()
router.register(r'announcement', AnnouncementViewSet, basename="announcement")
router.register(r'moderate', AnnouncementModerateViewSet, basename="announcement_moderate")
router.register(r'application', ApplicationsViewSet, basename="application")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
