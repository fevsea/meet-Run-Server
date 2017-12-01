from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from quedadas.models import Chat
from quedadas.permissions import IsOwnerOrReadOnly
from quedadas.serializers import ChatSerializer, ChatSerializerCreate



class ChatList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)


    def get_queryset(self):
        user = self.request.user
        return user.chats.all().order_by('lastDateTime')


    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer

    def create(self, request, *args, **kwargs):
        serializer = ChatSerializerCreate(data=request.data)

        if serializer.is_valid():
            obj = serializer.save()
            responseSerializer = ChatSerializer(obj)
            return Response(responseSerializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'PUT'):
            return ChatSerializerCreate
        return ChatSerializer
