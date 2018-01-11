from django.db.models import Q

from quedadas.models import Challenge


def get_list(user):
    return Challenge.objects.filter(completed=False).filter(Q(creator=user) | Q(challenged=user)).distinct()


def accept_challenge(challenge, user):
    if challenge.challenged == user:
        challenge.accepted = True
        challenge.save()
        challenge.notify_accepted()
        return True
    return False
