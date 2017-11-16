from datetime import date
from functools import reduce

from django.contrib.auth.models import User
from rest_framework import generics, permissions, filters, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK
from rest_framework.views import APIView
from django.db.models import Q
import operator

from quedadas.models import Meeting, Tracking
from quedadas.permissions import IsOwnerOrReadOnly
from quedadas.serializers import MeetingSerializer, TrackingSerializer, UserSerializerDetail


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all().order_by("date")
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
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
                'meeting' : get_object_or_404(Meeting, pk=meeting)
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
        return (user.meetings_at.all() | user.meetings.all()).distinct().filter(date__gt=date.today()).order_by("date")

    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'description')


class JoinMeeting(APIView):
    permission_classes = ((IsAuthenticated,))

    def get(self, request, pk):
        meeting = get_object_or_404(Meeting, pk=pk)
        attendences = meeting.participants
        serializer = UserSerializerDetail(attendences, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user = request.user
        meeting = get_object_or_404(Meeting, pk=pk)
        status_code = HTTP_204_NO_CONTENT if user in meeting.participants.all() else HTTP_201_CREATED
        meeting.participants.add(user)
        meeting.save()
        return Response(status=status_code)

    def delete(self, request, pk):
        user = request.user
        meeting = get_object_or_404(Meeting, pk=pk)
        status_code = HTTP_200_OK if user in meeting.participants.all() else HTTP_204_NO_CONTENT
        meeting.participants.remove(user)
        meeting.save()
        return Response(status=status_code)
