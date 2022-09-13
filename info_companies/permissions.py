
from companies.models import Company
from rest_framework import permissions
from rest_framework.views import Request, View


class IsOnlyCompanyOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        company = Company.objects.get(id=request.data["company"])

        if request.user.id == company.owner_id.id:
            return True
