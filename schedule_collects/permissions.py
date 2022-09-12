from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsOwnerUserOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        import pdb

        pdb.set_trace()
        return request.user.id == obj.id or request.user.is_superuser
