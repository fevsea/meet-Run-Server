from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Meeting



class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ('id', 'title', 'description', 'public', 'level', 'date', 'latitude', 'longitude')

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
