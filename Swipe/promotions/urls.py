from django.urls import path, include
from rest_framework.routers import DefaultRouter

from Swipe.promotions.views import PromotionTypeViewSet

router = DefaultRouter()
router.register(r'promotion-type', PromotionTypeViewSet, basename="promotion_type")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
