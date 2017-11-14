from datetime import date
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, filters, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_202_ACCEPTED, HTTP_201_CREATED, HTTP_204_NO_CONTENT, \
    HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.views import APIView

from quedadas.permissions import IsOwnerOrReadOnly
from .models import Meeting, Profile, Friendship
from .serializers import UserSerializer, MeetingSerializer, UserSerializerDetail, TestSerializer, ChangePassword, \
    TrackingSerializer


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
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

class Tracking(APIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def get(self, request, pk):
        pass
        m = get_object_or_404(Meeting, pk=pk).tracking
        serializer = TrackingSerializer(m)
        return Response(serializer.data)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.exclude(username="admin")

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


class Friends(APIView):
    permission_classes = ((IsAuthenticated, ))

    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            user = get_object_or_404(User, pk=pk)
        firends_qs = user.prof.get_friends()
        serializer = UserSerializerDetail(firends_qs, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None, format=None):
        user = request.user
        friend = get_object_or_404(User, pk=pk)
        status_code = HTTP_202_ACCEPTED
        firends_qs = user.prof.get_friends().filter(pk=pk)
        if (not firends_qs.exists() and pk != user.pk):
            Friendship(creator=user, friend=friend).save()
            status_code = HTTP_201_CREATED

        firends_qs = user.prof.get_friends()
        serializer = UserSerializerDetail(firends_qs, many=True)
        return Response(serializer.data, status_code)

    def delete(self, request, pk=None, format=None):
        user = request.user
        friend = get_object_or_404(User, pk=pk)
        status_code = HTTP_204_NO_CONTENT
        firends_qs = user.prof.get_friends().filter(pk=pk)
        if (firends_qs.exists() and pk != user.pk):
            Friendship.objects.filter(Q(creator=user, friend=friend) | Q(friend=user, creator=friend)).delete()
            status_code = HTTP_200_OK
        firends_qs = user.prof.get_friends()
        serializer = UserSerializerDetail(firends_qs, many=True)
        return Response(serializer.data, status_code)



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


class changePassword(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        serializer = ChangePassword(data=request.data)
        if serializer.is_valid():
            user = self.request.user
            if not user.check_password(serializer["old"].value):
                return Response(status=HTTP_403_FORBIDDEN)
            user.set_password(serializer["new"].value)
            user.save()
            return Response(status=HTTP_200_OK)
        else:
            return Response(status=HTTP_400_BAD_REQUEST)



@api_view(["GET"])
@permission_classes((IsAuthenticated, ))
def logout(request):
    user = request.user
    t = Token.objects.get(user=user)
    t.delete()
    Token.objects.create(user=user)
    return Response(status=HTTP_202_ACCEPTED)

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'meetings': reverse('meeting_list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format)
    })




class TestList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = TestSerializer