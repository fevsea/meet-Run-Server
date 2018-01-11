from datetime import timedelta

from django.utils import timezone

from quedadas.controllers import firebaseCtrl
from quedadas.models import Feed, Meeting, Tracking


def ban_request(requestor, user):
    if user.prof.ban_date is None:
        user.prof.ban_count.add(requestor)
        if user.prof.ban_count.count() >= 3:
            user.prof.ban_count.clear()
            user.prof.ban_date = timezone.now() + timedelta(days=7)
            user.prof.save()
            firebaseCtrl.baned(user, 7)


def un_ban(baned):
    baned.ban_date = None
    baned.save()
    firebaseCtrl.un_baned(baned.user)


def get_feed(user):
    feed = []
    friends = user.prof.get_friends()
    for friend in friends:
        # Past tracks
        tracks = Tracking.objects.filter(user=friend).order_by ("-created")[:10]
        for t in tracks:
            feed.append(Feed(t.meeting, 0, t.created, friend, t))

        # Future friends created
        created = friend.meetings.filter(date__gt=timezone.now()).order_by("-created")[:10]
        for m in created:
            feed.append(Feed(m, 1, m.created, friend))

    # Near meetings
    near = Meeting.objects.filter(owner__prof__postal_code=user.prof.postal_code).filter(
        date__gt=timezone.now()).order_by("-created")[:10]
    for m in near:
        feed.append(Feed(m, 3, m.created))

    return sorted(feed, key=lambda x: x.date, reverse=True)[:10]
