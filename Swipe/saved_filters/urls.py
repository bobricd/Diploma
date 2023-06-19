from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Swipe.saved_filters.views import SavedFiltersViewSet

router = DefaultRouter()
router.register(r'', SavedFiltersViewSet, basename="saved_filters")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]