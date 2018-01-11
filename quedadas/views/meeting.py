import operator
from functools import reduce

from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from rest_framework import generics, permissions, filters, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView

from quedadas.models import Meeting, Tracking
from quedadas.permissions import IsOwnerOrReadOnly, IsNotBaned
from quedadas.serializers import MeetingSerializer, TrackingSerializer, UserSerializerDetail


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all().order_by("date")
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsNotBaned)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class TrackingView(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.RetrieveModelMixin,
                   generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    serializer_class = TrackingSerializer
    queryset = Tracking.objects.all()
    lookup_fields = ('meeting', 'user')

    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        q = reduce(operator.and_, (Q(x) for x in filter.items()))
        return get_object_or_404(queryset, q)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def post(self, request, meeting, user, format=None):
        if Tracking.objects.filter(user=user).filter(meeting=meeting).exists():
            return Response(status=status.HTTP_409_CONFLICT)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.validated_data.update({
                'user': get_object_or_404(User, pk=user),
                'meeting': get_object_or_404(Meeting, pk=meeting)
            })
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UserMeeting(generics.ListAPIView):

    def get_queryset(self):
        pk = self.kwargs.get('pk', None)
        user = self.request.user
        if pk is not None:
            user = get_object_or_404(User, pk=pk)

        qs = (user.meetings_at.all() | user.meetings.all()).distinct()
        filt = self.request.query_params.get('filter', None)

        if filter is None or filter == "all":
            pass
        elif filt == "past":
            qs = qs.filter(date__lt=timezone.now())
        elif filt == "future":
            qs = qs.filter(date__gte=timezone.now()).exclude(tracks__in = user.tracks.all())
        return qs.order_by("date")

    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')
    pagination_class = None


class JoinMeeting(APIView):
    permission_classes = (IsAuthenticated, IsNotBaned)
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, pk, usr=None):
        meeting = get_object_or_404(Meeting, pk=pk)
        attendences = meeting.participants.all()
        page = self.paginate_queryset(attendences)
        if page is not None:
            serializer = UserSerializerDetail(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializerDetail(attendences, many=True)
        return Response(serializer.data)

    def post(self, request, pk, usr=None):
        user = request.user
        if usr is not None:
            user = get_object_or_404(User, pk=usr)
        meeting = get_object_or_404(Meeting, pk=pk)
        status_code = HTTP_204_NO_CONTENT if user in meeting.participants.all() else HTTP_201_CREATED
        meeting.participants.add(user)
        meeting.save()
        return Response(status=status_code)

    def delete(self, request, pk, usr):
        user = request.user
        if usr is not None:
            user = get_object_or_404(User, usr)
        meeting = get_object_or_404(Meeting, pk=pk)
        status_code = HTTP_200_OK if user in meeting.participants.all() else HTTP_204_NO_CONTENT
        meeting.participants.remove(user)
        meeting.save()
        return Response(status=status_code)

    @property
    def paginator(self):
        """
        The paginator instance associated with the view, or `None`.
        """
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        """
        Return a single page of results, or `None` if pagination is disabled.
        """
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        """
        Return a paginated style `Response` object for the given output data.
        """
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
