from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Quedada


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class QuedadasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quedada
        fields = ('id', 'title', 'description', 'public')