from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404

from quedadas.serializers import ThrophySerializer


class Stats(generics.RetrieveAPIView):
    serializer_class = ThrophySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_object(self):
        user_pk = self.kwargs.get("pk", self.request.user.pk)
        user = get_object_or_404(User, pk=user_pk)
        return user.prof.statistics
