def notify_user(User, data_message=None):
    from pyfcm import FCMNotification
    push_service = FCMNotification(
        api_key="AAAA19KbT04:APA91bFroH6rGfC-eywj49abV2OZMyVj-St1v7eOhwSADPKG0Fon8tfwVxMRYlcIYOkHf8xEqnqlpbIuqU7W3oF9LhxiDjLlKw4BoXaIknY75t1rBDZTP5OzY6iYz_MJF2FGAadmoqT_")

    registration_id = User.prof.token
    if registration_id is not None:
        result = push_service.single_device_data_message(registration_id=registration_id,
                                                         data_message=data_message)


def new_challenge(challenge):
    user = challenge.challenged
    data = {
        "type": "new_challenge",
        "challenge_id": challenge.pk,
        "challenger_username": challenge.creator.username
    }
    notify_user(user, data)


def challenge_accepted(challenge):
    user = challenge.creator
    data = {
        "type": "challenge_accepted",
        "challenge_id": challenge.pk,
        "challenged_username": challenge.challenged.username
    }
    notify_user(user, data)


def challenge_won(challenge, user):
    user = challenge.challenged
    data = {
        "type": "challenge_won",
        "challenge_id": challenge.pk,
        "winner_id": user.pk
    }
    notify_user(user, data)


def challenge_lost(challenge, user):
    data = {
        "type": "challenge_lost",
        "challenge_id": challenge.pk,
        "winner_id": user.pk
    }
    notify_user(user, data)


def challenge_finalized(challenge):
    userA = challenge.challenged
    userB = challenge.creator
    data = {
        "type": "challenge_finalized",
        "challenge_id": challenge.pk,
    }
    notify_user(userA, data)
    notify_user(userB, data)


def new_friend(friendship):
    user = friendship.friend
    data = {
        "type": "friend_request",
        "friend_id": friendship.creator.id,
        "friend_name": friendship.creator.username
    }
    notify_user(user, data)


def friend_accepted(friendship):
    user = friendship.creator
    data = {
        "type": "friend_accepted",
        "friend_id": friendship.friend.id,
        "friend_name": friendship.friend.username
    }
    notify_user(user, data)


def trophy_obtained(stats, name):
    user = stats.prof.user
    data = {
        "type": "new_trophy",
        "trophy_name": name
    }
    notify_user(user, data)


def baned(user, days):
    data = {
        "type": "baned",
        "days": days
    }
    notify_user(user, data)


def unBaned(user):
    data = {
        "type": "un_baned",
    }
    notify_user(user, data)