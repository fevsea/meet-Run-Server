from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    class Meta:
        model = Meeting
        fields = ('id', 'title', 'description', 'public', 'level', 'date', 'latitude', 'longitude')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'password')

class UserSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
