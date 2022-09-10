from rest_framework import permissions
from rest_framework.views import Request, View

from .models import User

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):

        return request.user.id == user.id or request.user.is_superuser