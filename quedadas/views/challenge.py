from django.db.models import Q
from rest_framework import generics, permissions
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


class ChallengeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Challenge.objects.all()
    serializer_class = ChallengeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
