from rest_framework import permissions


class IsOwnerOrAdminUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj or request.user.is_staff:
            return True

        return False
