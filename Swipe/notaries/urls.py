from django.urls import path, include
from rest_framework import routers

from Swipe.notaries.views import NotaryViewSet

router = routers.DefaultRouter()
router.register('', NotaryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
