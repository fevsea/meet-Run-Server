from datetime import timedelta

from django.utils import timezone

from quedadas.controllers import firebaseCtrl


def ban_request(requestor, user):
    if user.prof.ban_date is None:
        user.prof.ban_count.add(requestor)
        if user.prof.ban_count.count() >= 3:
            user.prof.ban_count.clear()
            user.prof.ban_date = timezone.now() + timedelta(days=7)
            user.prof.save()
            firebaseCtrl.baned(user, 7)


def unBan(baned):
    baned.ban_date = None
    baned.save()
    firebaseCtrl.unBaned(baned.user)