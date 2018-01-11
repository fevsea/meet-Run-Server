from datetime import timedelta

from django.utils import timezone

from quedadas.controllers import firebaseCtrl


def ban_request(user):
    if user.prof.ban_date is None:
        user.prof.ban_count += 1
        if user.prof.ban_count >= 3:
            user.prof.ban_count = 0
            user.prof.ban_date = timezone.now() + timedelta(days=7)
            user.prof.save()
            firebaseCtrl.baned(user, 7)
