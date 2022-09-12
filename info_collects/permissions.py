from turtle import pd

from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User


class IsInfoCollectionOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        user = User.objects.get(id=view.kwargs["id"])
        if request.user.id == user.id:
            return True
