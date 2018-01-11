from django.db.models import Q
from rest_framework import generics, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from quedadas.controllers import challengeCtrl
from quedadas.controllers.challengeCtrl import accept_challenge
from quedadas.models import Challenge
from quedadas.serializers import ChallengeSerializer


class ChallengeList(generics.ListCreateAPIView):
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        user = self.request.user
        return challengeCtrl.get_list(user)


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView, APIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def post(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        if accept_challenge(challenge, request.user):
            return Response(200)
        return Response(403)
