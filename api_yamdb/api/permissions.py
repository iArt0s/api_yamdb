from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Класс Permission, ограничивающий доступ к UnSAFE methods"""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.role == 'admin':
            return True

class OnlyUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == ('GET' or 'PATCH'):
            return True

class OnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True     






# class IsOwnerOrReadOnly(permissions.BasePermission):
#     """
#     Класс Permission, ограничивающий доступ к UnSAFE methods
#     на уровне запроса и на уровне объекта.
#     """
#     def has_permission(self, request, view):
#         return (
#             request.method in permissions.SAFE_METHODS
#             or request.user.is_authenticated
#         )

#     def has_object_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:

#             return True

#         return obj.author == request.user
