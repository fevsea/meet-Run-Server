from django.contrib.auth.models import User, Group
from django.core.serializers import json
from rest_framework import viewsets, generics, permissions
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Meeting
from .serializers import UserSerializer, GroupSerializer, MeetingSerializer


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'meetings': reverse('meeting_list', request=request, format=format),
        #'snippets': reverse('snippet-list', request=request, format=format)
    })