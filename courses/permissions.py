from rest_framework.permissions import BasePermission
from datetime import datetime


class CanReadPremium(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff


class EvenYearsOnly(BasePermission):
    def has_permission(self, request, view):
        year = datetime.now().year
        return year % 2 == 0


class SuperUserOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_superuser


class UpdateOnly(BasePermission):
    def has_permission(self, request, view):
        permitted = request.method in ['PUT', 'PATCH']
        return permitted