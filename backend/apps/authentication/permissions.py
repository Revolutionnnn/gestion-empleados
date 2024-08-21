# permissions.py
from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Permiso personalizado para permitir solo a los superusuarios acceder a la vista.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
