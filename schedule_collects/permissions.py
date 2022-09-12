from turtle import pd

from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User

from schedule_collects.models import ScheduleCollect


class IsOnlyOwnerSchedule(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        schedule = ScheduleCollect.objects.get(id=view.kwargs["schedule_id"])

        if request.user.id == schedule.user.id:
            return True
