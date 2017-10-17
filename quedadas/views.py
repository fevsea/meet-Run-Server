from django.contrib.auth.models import User, Group
from django.core.serializers import json
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Meeting
from .serializers import UserSerializer, GroupSerializer, QuedadasSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@api_view(['GET', 'POST'])
def quedada_list(request, format=None):
    """
    List all quedadas, or create a new quedada.
    """
    if request.method == 'GET':
        quedadas = Meeting.objects.all()
        serializer = QuedadasSerializer(quedadas, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = QuedadasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'DELETE'])
def meeting_detail(request, pk, format=None):
    """
    Obtain, modify or delete a singe Quedada instance by id
    """
    try:
        meeting = Meeting.objects.get(pk=pk)
    except Meeting.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = QuedadasSerializer(meeting)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = QuedadasSerializer(meeting, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        meeting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def root(request, format=None):
    """
    What can I do for you?
    """

    data = [1, 2, 3, {'4': 5, '6': 7}]
    return Response(json.dumps(data, separators=(',', ':')))