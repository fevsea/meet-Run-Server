from django.core.management.base import BaseCommand
from django.utils import timezone

from quedadas.models import Challenge


class Command(BaseCommand):
    help = 'Loock for finalized challenges'

    def handle(self, *args, **options):
        to_update = Challenge.objects.filter(completed=False).filter(deadline__gte=timezone.now())
        for challenge in to_update:
            challenge.check_completion()
        self.stdout.write("OK, done, that's all")
