from rest_framework.permissions import BasePermission


class IsAdminOrAgent(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and (
                request.user.user_type == 'admin' or request.user.user_type == 'agent'
            )
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.user_type == 'admin'
        )


class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.user_type == 'agent'
        )
