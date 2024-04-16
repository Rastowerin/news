from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):

        if request.user.is_superuser:
            return True

        return False


class IsCreator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.creator == request.user
