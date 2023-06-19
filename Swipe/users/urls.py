from django.urls import path, include
from rest_framework import routers

from Swipe.users.views import BlackListView, UserListView, UserDetailView, FavouriteListView, AddToBlackListView, \
    RemoveFromBlackListView, MessageViewSet, SubscriptionViewSet, SubscriptionTypeViewSet

router = routers.SimpleRouter()
router.register(r'messages', MessageViewSet)
router.register(r'subscriptions', SubscriptionViewSet)
router.register(r'subscription-types', SubscriptionTypeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', UserListView.as_view(), name='user_list'),
    path('profile/', UserDetailView.as_view(), name='user_detail'),
    path('blacklist/', BlackListView.as_view(), name='black_list'),
    path('favourite/', FavouriteListView.as_view(), name='favourite_list'),
    path('to-black-list/<int:pk>/', AddToBlackListView.as_view(), name="user_to_black_list"),
    path('remove-from-black-list/<int:pk>/', RemoveFromBlackListView.as_view(), name="user_remove_black_list"),
]
