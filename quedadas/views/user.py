from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_200_OK, HTTP_400_BAD_REQUEST, \
    HTTP_202_ACCEPTED, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.settings import api_settings

from quedadas.models import Friendship
from quedadas.permissions import IsOwnerOrReadOnly
from quedadas.serializers import UserSerializer, UserSerializerDetail, ChangePassword, StatsSerializer, TokenSerializer


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
@permission_classes((IsAuthenticated,))
def logout(request):
    user = request.user
    t = Token.objects.get(user=user)
    t.delete()
    Token.objects.create(user=user)
    return Response(status=HTTP_202_ACCEPTED)


class Friends(APIView):
    permission_classes = ((IsAuthenticated,))
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            user = get_object_or_404(User, pk=pk)
        friends_qs = user.prof.get_friends()
        page = self.paginate_queryset(friends_qs)
        if page is not None:
            serializer = UserSerializerDetail(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializerDetail(friends_qs, many=True)
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

class Stats(APIView):
    permission_classes = ((IsAuthenticated,))
    def get(self, request, pk=None):
        user = request.user
        if pk is not None:
            user = get_object_or_404(User, pk=pk)
        serializer = StatsSerializer(user.prof.statistics, many=False)
        return Response(serializer.data)


class Token(APIView):
    permission_classes = ((IsAuthenticated,))
    def get(self, request):
        user = request.user
        serializer = TokenSerializer({"token": user.prof.token}, many=False)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = JSONParser().parse(request)
        serializer = TokenSerializer(data=data)
        if serializer.is_valid():
            token = serializer.data["token"]
            user.prof.token = token
            user.prof.save()
            serializer = TokenSerializer({"token": user.prof.token}, many=False)
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

