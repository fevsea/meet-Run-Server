from rest_framework import permissions


class IsNotBaned(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method != "POST":
            return True
        user = request.user
        return user.prof.ban_date is None
