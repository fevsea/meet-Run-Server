import django
import os
from pyfcm import FCMNotification


push_service = FCMNotification(api_key="AAAA19KbT04:APA91bFroH6rGfC-eywj49abV2OZMyVj-St1v7eOhwSADPKG0Fon8tfwVxMRYlcIYOkHf8xEqnqlpbIuqU7W3oF9LhxiDjLlKw4BoXaIknY75t1rBDZTP5OzY6iYz_MJF2FGAadmoqT_")

def notify_user(User, message_body, data_message=None):
    registration_id = User.prof.token
    if registration_id is not None:
        result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body,
                                                  data_message=data_message)

def new_challenge(challenge):
    user = challenge.challenged
    type = "new_challenge"
    data = {
        "challenge_id": challenge.pk,
        "challenger_username": challenge.creator.username
    }
    notify_user(user, type, data)

def challenge_accepted(challenge):
    user = challenge.challenged
    type = "challenge_accepted"
    data = {
        "challenge_id": challenge.pk,
        "challenged_username": challenge.challenged.username
    }
    notify_user(user, type, data)

def new_friend(friendship):
    user = friendship.friend
    type = "friend_request"
    data = {
        "friend_id": friendship.creator.id,
        "friend_name": friendship.creator.username
    }
    notify_user(user, type, data)

def friend_accepted(friendship):
    user = friendship.creator
    type = "friend_accepted"
    data = {
        "friend_id": friendship.friend.id,
        "friend_name": friendship.friend.username
    }
    notify_user(user, type, data)


data_message = {
    "title" : "Error del sistema",
    "text" : "La app ha provocado overflow de la lista de errores",
}


awais = "ffhIBWlzXnQ:APA91bGzzrfJnmZrE432EC_LF3XP9YLrKxtDG09ptiaa7sPPe2jIXeyFTixXNMQA2g3bZwXVZvRIudzaCYO3yyAhnaWj_zhDTUpFuGSlbcLNzrgtwrlkhukU6HL27YQ4tiRm-lebJ6Rc"
result = push_service.notify_single_device(registration_id=awais, message_body="notification",
                                                  data_message=data_message)

#message_body = "notification"
#registration_id = User.objects.get(username="alejandroA").prof.token
#registration_id = "fEF89mhL-Eo:APA91bGKHtf9B85tLZdIn4gYuTg5bxC9gGEHm4yMDC1ITNL-IrHC7dTvFM7exJHkCMLJ1i9JmuA9ngmnVp7sxTucU0CIGgTtTM_OKhXMv0bbUxQpV2yQfWkf9awTnS7QwBnUVpqpmMz0"
#result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body, data_message=data_message)
#result = push_service.notify_topic_subscribers(topic_name="all", message_body=message_body, data_message=data_message)
