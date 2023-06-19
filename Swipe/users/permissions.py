from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from Swipe.users.models import User


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user.role == User.RoleName.OWNER)


class IsBuilder(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.role == User.RoleName.BUILDER)


class HaveResidentialComplex(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            return bool(request.user.residentialcomplex)
        except ObjectDoesNotExist:
            return False


class IsMessageSender(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsAnnouncementOwner(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class IsSubscriptionOwnerOrAdmin(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.subscription == obj
