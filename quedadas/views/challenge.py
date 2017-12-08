from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from quedadas.models import Challenge
from quedadas.serializers import ChallengeSerializer


class ChallengeList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        qs = Challenge.objects.filter(Q(creator=user) | Q(challenged=user)).distinct()
        return qs


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView, APIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        if challenge.challenged == request.user:
            challenge.accepted = True
            challenge.save()
            challenge.notify_accepted()
            return Response(200)
        return Response(403)
