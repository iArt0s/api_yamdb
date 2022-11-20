from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к UnSAFE methods"""

    def has_permission(self, request, view):
        if (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.check_admin
                     or request.user.is_staff is True)):
            return True


class IsOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and (
                request.user.check_admin or request.user.is_staff is True):
            return True


class IsReviewAndComment(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        permission_user = (request.user.is_authenticated
                           and (request.user == obj.author
                                or request.user.check_admin
                                or request.user.check_moderator
                                or request.user.is_staff is True))

        return (request.method not in permissions.SAFE_METHODS
                and permission_user
                or request.method == ('GET')
                )
