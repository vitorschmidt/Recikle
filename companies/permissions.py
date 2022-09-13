from info_companies.models import InfoCompany
from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User

from .models import Company


class IsCompanyOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, company: Company):

        if request.user.is_company and request.user.id == company.owner_id.id:
            return True


class IsCompanyOrAdmin(permissions.BasePermission):
    def has_permission(self, request: Request, view: View):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_company or request.user.is_superuser
