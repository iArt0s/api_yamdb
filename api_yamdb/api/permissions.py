from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к UnSAFE methods"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_staff is True):
            return True


class OnlyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.method == (
                'GET' or 'PATCH'):
            return True


class OnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.role == 'admin' or request.user.is_staff is True):
            return True


class OnlyAdmin1(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method is 'DELETE' or 'PATCH' and request.user.is_authenticated and (
                request.user == obj.author or request.user.role == (
                    'moderator' or 'admin') or request.user.is_staff is True) or request.method == (
                'GET'))
