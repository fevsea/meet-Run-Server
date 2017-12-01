# -*- coding: utf-8 -*-
import django
import os
from datetime import datetime, timedelta, timezone
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
django.setup()
from quedadas.models import Meeting, Profile, Friendship
from django.contrib.auth.models import User

User.objects.create_superuser('admin', 'admin@example.com', 'meetnrun')

userA = User.objects.create_user(username='alejandroA', password='alejandroA', first_name="Alejandro", last_name="Agustin")
Profile(user=userA, question="My question", answer="My answer", postal_code="08181", level=2).save()
userB = User.objects.create_user(username='javierA', password='javierA', first_name="Javier", last_name="Alemán")
Profile(user=userB, question="My question", answer="My answer", postal_code="08181", level=3).save()
userC = User.objects.create_user(username='guillemC', password='guillemC', first_name="Guillem", last_name="Castro")
Profile(user=userC, question="My question", answer="My answer", postal_code="08034", level=1).save()
userD = User.objects.create_user(username='monicaF', password='monicaF', first_name="Mònica", last_name="Follana")
Profile(user=userD, question="My question", answer="My answer", postal_code="08034", level=1).save()
userE = User.objects.create_user(username='awaisI', password='awaisI', first_name="Awais", last_name="Iqbal")
Profile(user=userE, question="My question", answer="My answer", postal_code="08034", level=1).save()
userF = User.objects.create_user(username='marcP', password='marcP', first_name="Marc", last_name="Paricio")
Profile(user=userF, question="My question", answer="My answer", postal_code="08034", level=2).save()
userG = User.objects.create_user(username='ericR', password='ericR', first_name="Eric", last_name="Rodríguez")
Profile(user=userG, question="My question", answer="My answer", postal_code="08034", level=1).save()

from django.utils import timezone
Friendship(creator=userA, friend=userB).save()
Friendship(creator=userA, friend=userC).save()
Friendship(creator=userC, friend=userA).save()
Friendship(creator=userD, friend=userA).save()
Friendship(creator=userE, friend=userF).save()
Friendship(creator=userE, friend=userG).save()

meetingA = Meeting(owner=userA, title="Sortida pel marenostrum", public=True, level=3, latitude="41.488576",
        longitude="2.21284", date=(timezone.now()+timedelta(days=2)))
meetingA.save()
meetingA.participants.add(userB)

meetingB = Meeting(owner=userA, title="Guanta", public=True, level=2, latitude="41.388576",
        longitude="2.11284", date=(timezone.now()+timedelta(days=3)))
meetingA.save()
meetingA.participants.add(userB, userC, userD, userE, userF)

meetingC = Meeting(owner=userB, title="N'em a corre per l'eixample", public=False, level=1, latitude="41.378576",
        longitude="2.01284", date=(timezone.now()+timedelta(days=2))).save()