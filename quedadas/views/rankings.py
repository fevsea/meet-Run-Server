from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework.views import APIView

from quedadas.controllers import rankingsCtrl
from quedadas.models import Zone
from quedadas.serializers import ZoneSerializer, ZipSerializer


class ZoneList(generics.ListAPIView):
    queryset = Zone.objects.order_by("-average")
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('zip',)


class ZipList(APIView):
    def get(self, request):
        zips = Zone.objects.only("zip")
        serializer = ZipSerializer(zips, many=True)
        return Response(serializer.data)