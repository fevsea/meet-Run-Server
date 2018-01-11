from django.core.management.base import BaseCommand
from django.utils import timezone

from quedadas.controllers import firebaseCtrl
from quedadas.models import Challenge, Profile


class Command(BaseCommand):
    help = 'Loock for finalized challenges'

    def handle(self, *args, **options):
        to_update = Challenge.objects.filter(completed=False).filter(deadline__lte=timezone.now())
        for challenge in to_update:
            challenge.check_completion()

        to_check = Profile.objects.filter(ban_date__lte=timezone.now())
        for baned in to_check:
            baned.ban_date = None
            baned.save()
            firebaseCtrl.unBaned(baned.user)

        self.stdout.write("OK, done, that's all")
