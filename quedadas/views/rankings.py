from rest_framework import generics, permissions

from quedadas.models import Zone
from quedadas.serializers import ZoneSerializer


class ZoneList(generics.ListAPIView):
    queryset = Zone.objects.order_by("-average")
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

