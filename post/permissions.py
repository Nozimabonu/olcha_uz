from rest_framework import permissions


class CustomPermission(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     if request.method in permissions.SAFE_METHODS:
    #         return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.author == request.user:

            if request.method == 'DELETE' and request.user.is_superuser:
                return True

            if request.method in ['PUT', 'PATCH'] and request.user.is_staff:
                return True


