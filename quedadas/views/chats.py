from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions

from quedadas.models import Chat
from quedadas.permissions import IsOwnerOrReadOnly
from quedadas.serializers import ChatSerializer, ChatSerializerCreate



class ChatList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = ChatSerializer

    def get_queryset(self):
        user = self.request.user
        return Chat.objects.filter(Q(userName=user) | Q(friendUsername=user)).order_by("last_message")


    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer


class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer
