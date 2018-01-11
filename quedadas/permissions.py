from django.contrib.auth.models import User
from rest_framework import permissions

from quedadas.models import Meeting


class IsNotBaned(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        user = request.user
        return user.prof.ban_date is None
