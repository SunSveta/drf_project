from rest_framework import permissions
from rest_framework.permissions import BasePermission


class OwnerOrModerator(BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().created_user:
            return True
        elif request.user.is_staff:
            return True

        return False


class ModeratorPermissionCreateDestroy(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return False
        return True


class OwnerOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user == view.get_object().created_user:
            return True
