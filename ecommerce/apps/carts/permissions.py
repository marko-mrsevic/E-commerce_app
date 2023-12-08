from rest_framework.permissions import BasePermission


class IsOwnerOrAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user or request.user.is_staff:
            return True

        return False


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
