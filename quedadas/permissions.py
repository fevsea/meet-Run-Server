from rest_framework import permissions

from django.contrib.auth.models import User

from quedadas.models import Meeting


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        return True
        # Write permissions are only allowed to the owner of the snippet.
        if isinstance(obj, Meeting):
            return obj.owner == request.user
        if isinstance(obj, User):
            return obj == request.user
        return False