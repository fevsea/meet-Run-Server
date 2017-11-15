from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Meeting, Profile, Tracking, RoutePoint


class UserSerializer(serializers.ModelSerializer):
    postal_code = serializers.CharField(source='prof.postal_code')
    question = serializers.CharField(source='prof.question')
    answer = serializers.CharField(source='prof.answer')
    level = serializers.IntegerField(source='prof.level')

    def create(self, validated_data):
        profile_data = validated_data.pop('prof')
        user = User.objects.create(**validated_data)
        Profile.objects.create(user=user, **profile_data)
        return user

    class Meta:
        model = User
        related_fields = ['prof']
        fields = ('id', 'username', 'first_name', 'last_name', 'password', 'postal_code', 'question', 'answer', 'level')


class UserSerializerDetail(serializers.ModelSerializer):
    postal_code = serializers.CharField(source='prof.postal_code')
    question = serializers.CharField(source='prof.question')
    level = serializers.IntegerField(source='prof.level')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('prof')

        instance.prof.question = profile_data.get('question', instance.prof.question)
        instance.prof.postal_code = profile_data.get('postal_code', instance.prof.postal_code)
        instance.username = validated_data.get('username', instance.username)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.prof.level = profile_data.get('level', instance.prof.level)
        instance.save()
        instance.prof.save()

        return instance

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'postal_code', 'question', 'level')


class MeetingSerializer(serializers.ModelSerializer):
    owner = UserSerializerDetail(many=False, read_only=True)
    participants = UserSerializerDetail(many=True, read_only=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    class Meta:
        model = Meeting
        fields = (
        'id', 'title', 'description', 'public', 'level', 'date', 'latitude', 'longitude', 'owner', 'participants')


class ChangePassword(serializers.Serializer):
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint
        fields = ('latitude', 'longitude')


class TrackingSerializer(serializers.ModelSerializer):
    routePoints = PointSerializer(many=True, write_only=False)

    class Meta:
        model = Tracking
        fields = ('id', 'averagespeed', 'distance', 'steps', 'totalTimeMillis', 'calories', 'routePoints')

    def create(self, validated_data):
        points_data = validated_data.pop('routePoints')
        tracking = Tracking.objects.create(**validated_data)
        for track_data in points_data:
            RoutePoint.objects.create(track=tracking, **track_data)
        return tracking
