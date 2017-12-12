from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Meeting, Profile, Tracking, RoutePoint, Chat, Statistics, Challenge, Friendship


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
    chat = serializers.IntegerField(source="chat_r.pk", read_only=True)

    # participants = UserSerializerDetail(many=True, read_only=True)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    class Meta:
        model = Meeting
        fields = ('id', 'title', 'description', 'public', 'level', 'date', 'latitude', 'longitude', 'owner', 'chat')


class ChangePassword(serializers.Serializer):
    old = serializers.CharField(required=True)
    new = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoutePoint
        fields = ('latitude', 'longitude')


class TrackingSerializer(serializers.ModelSerializer):
    routePoints = PointSerializer(many=True, write_only=False)

    class Meta:
        model = Tracking
        read_only_fields = ('user', 'meeting')
        fields = ('user', 'meeting', 'averagespeed', 'distance', 'steps', 'totalTimeMillis', 'calories', 'routePoints')

    def create(self, validated_data):
        points_data = validated_data.pop('routePoints')
        tracking = Tracking.objects.create(**validated_data)
        for track_data in points_data:
            RoutePoint.objects.create(track=tracking, **track_data)
        return tracking


class ChatSerializer(serializers.ModelSerializer):
    listUsersChat = UserSerializerDetail(many=True, read_only=True)
    meeting = MeetingSerializer(many=False, read_only=True)

    class Meta:
        model = Chat
        fields = (
            'pk', 'chatName', 'listUsersChat', 'type', 'meeting', 'lastMessage', 'lastMessageUserName', 'lastDateTime')


class ChatSerializerCreate(serializers.ModelSerializer):
    def to_representation(self, value):
        return ChatSerializer().to_representation(value)

    class Meta:
        model = Chat
        fields = (
            'chatName', 'listUsersChat', 'type', 'meeting', 'lastMessage', 'lastMessageUserName', 'lastDateTime')


class TrackingSerializerNoPoints(serializers.ModelSerializer):
    class Meta:
        model = Tracking
        fields = ('user', 'meeting', 'averagespeed', 'distance', 'steps', 'totalTimeMillis', 'calories')


class StatsSerializer(serializers.ModelSerializer):
    lastTracking = TrackingSerializerNoPoints(many=False, read_only=True)

    class Meta:
        model = Statistics
        fields = (
            'distance', 'steps', 'totalTimeMillis', 'calories', 'meetingsCompletats', 'averagespeed', 'lastTracking',
            'maxDistance', 'maxAverageSpeed', 'maxDuration', 'minDistance', 'minAverageSpeed', 'minDuration')


class ChallengeSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super(ChallengeSerializer, self).to_representation(instance)
        data['creator'] = UserSerializerDetail(instance.creator).data
        data['challenged'] = UserSerializerDetail(instance.challenged).data
        return data

    class Meta:
        model = Challenge
        fields = (
            'id', 'creator', 'challenged', 'distance', 'created', 'deadline', 'creatorDistance', 'challengedDistance',
            'accepted', 'completed')


class FriendSerializer(serializers.ModelSerializer):
    creator = UserSerializerDetail(many=False, read_only=True)
    friend = UserSerializerDetail(many=False, read_only=True)

    class Meta:
        model = Friendship
        fields = ('created', 'creator', 'friend', 'accepted')
