from pyfcm import FCMNotification
import django
import os
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
#django.setup()
from django.contrib.auth.models import User
import asyncio

push_service = FCMNotification(api_key="AAAA19KbT04:APA91bFroH6rGfC-eywj49abV2OZMyVj-St1v7eOhwSADPKG0Fon8tfwVxMRYlcIYOkHf8xEqnqlpbIuqU7W3oF9LhxiDjLlKw4BoXaIknY75t1rBDZTP5OzY6iYz_MJF2FGAadmoqT_")

async def notify_user(User, message_body, data_message=None):
    registration_id = User.prof.token
    if registration_id is not None:
        result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body,
                                                  data_message=data_message)

def new_challenge(challenge):
    user = challenge.challenged
    type = "new_challenge"
    data = {"challenge_id": challenge.pk}
    notify_user(user, type, data)


data_message = {
    "title" : "Error del sistema",
    "text" : "La app ha provocado overflow de la lista de errores",
}

#message_body = "notification"
#registration_id = User.objects.get(username="alejandroA").prof.token
#registration_id = "fEF89mhL-Eo:APA91bGKHtf9B85tLZdIn4gYuTg5bxC9gGEHm4yMDC1ITNL-IrHC7dTvFM7exJHkCMLJ1i9JmuA9ngmnVp7sxTucU0CIGgTtTM_OKhXMv0bbUxQpV2yQfWkf9awTnS7QwBnUVpqpmMz0"
#result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body, data_message=data_message)
#result = push_service.notify_topic_subscribers(topic_name="all", message_body=message_body, data_message=data_message)
