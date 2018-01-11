from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from quedadas.models import Chat
from quedadas.serializers import ChatSerializer, ChatSerializerCreate


class ChatList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    search_fields = ('chatName',)
    filter_fields = ('chatName',)

    def get_queryset(self):
        user = self.request.user
        return user.chats.all().order_by('-lastDateTime')

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = ChatSerializerCreate(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            response_serializer = ChatSerializer(obj)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.order_by('lastDateTime')
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer


class ChatP2p(APIView):
    def get(self, request, pk):
        user_a = request.user
        user_b = get_object_or_404(User, pk=pk)
        chats = Chat.objects.filter(listUsersChat=user_a).filter(listUsersChat=user_b).distinct()
        for chat in chats:
            if chat.listUsersChat.count() == 2:
                serializer = ChatSerializer(chat)
                return Response(serializer.data)
        return Response(status=404)
