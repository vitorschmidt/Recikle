from django.shortcuts import get_object_or_404
from info_collects.models import InfoCollect
from rest_framework import permissions
from rest_framework.views import Request, View
from schedule_collects.models import ScheduleCollect

from .models import User


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):

        return request.user.id == user.id or request.user.is_superuser


class IsOwnerSchedule(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):

        user = User.objects.get(id=view.kwargs["id"])

        if request.user.id == user.id:
            return True

        return request.user.is_company or request.user.is_superuser


class IsOwnerInfoCollect(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, user: User):
        teste = get_object_or_404(InfoCollect, user_id=request.user.id)

        usuario = User.objects.filter(info_collect=teste)

        return request.user.id == usuario[0].id or request.user.is_superuser
