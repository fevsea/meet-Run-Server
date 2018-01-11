from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from quedadas.models import Zone, Profile
from quedadas.serializers import ZoneSerializer, ZipSerializer, RankingSerializer


class ZoneList(generics.ListAPIView):
    queryset = Zone.objects.order_by("-average")
    serializer_class = ZoneSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    pagination_class = None
    filter_fields = ('zip',)


class ZoneDetail(generics.ListAPIView):
    serializer_class = RankingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        zone = get_object_or_404(Zone, pk=self.kwargs["pk"])
        return zone.members.order_by("-statistics__distance")


class UserList(generics.ListAPIView):
    queryset = Profile.objects.order_by("-statistics__distance")
    serializer_class = RankingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)


class ZipList(APIView):
    @staticmethod
    def get():
        zips = Zone.objects.only("zip").order_by("zip").annotate(page_count=Count('members')).filter(page_count__gt=0)
        serializer = ZipSerializer(zips, many=True)
        return Response(serializer.data)
