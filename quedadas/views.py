from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from quedadas.permissions import IsOwnerOrReadOnly
from .models import Meeting, Profile
from .serializers import UserSerializer, MeetingSerializer, UserSerializerDetail, TestSerializer


class MeetingList(generics.ListCreateAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class MeetingDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meeting.objects.all()
    serializer_class = MeetingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserSerializer
        return UserSerializerDetail

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerDetail
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class CurrentUserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def get(self, request, format=None):
        serializer = UserSerializerDetail(request.user)
        return Response(serializer.data)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if not user:
        return Response({"error": "Login failed"}, status=HTTP_401_UNAUTHORIZED)

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'meetings': reverse('meeting_list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format)
    })

class TestList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = TestSerializer