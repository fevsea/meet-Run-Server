
from pyfcm import FCMNotification
import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
django.setup()
from django.contrib.auth.models import User

push_service = FCMNotification(api_key="AAAA19KbT04:APA91bFroH6rGfC-eywj49abV2OZMyVj-St1v7eOhwSADPKG0Fon8tfwVxMRYlcIYOkHf8xEqnqlpbIuqU7W3oF9LhxiDjLlKw4BoXaIknY75t1rBDZTP5OzY6iYz_MJF2FGAadmoqT_")
data_message = {
    "Nick" : "Mario",
    "body" : "great match!",
    "Room" : "PortugalVSDenmark"
}
message_body = "Hope you're having fun this weekend, don't forget to check today's news"
registration_id = User.objects.get(username="alejandroA").prof.token
#registration_id = "eGKFhSf5OiY:APA91bE7eY3Dv1oLGvStcnZhzRQRjO0aS7-DWq4IHpmi030ZOXHKgRsUISd83ZJjJID3YQiCfUzj0MUmI2unH7veUKpoo3CjRAzmeFb5E3l3GcZd8L29DbiMSkLD5mQs9Khx4_S4U2uq"

result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body, data_message=data_message)