# -*- coding: utf-8 -*-
import os
from datetime import timedelta

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rest.settings")
django.setup()
from quedadas.models import Meeting, Profile, Friendship, Zone
from django.contrib.auth.models import User
from django.utils import timezone

'''
    NO CAMBIAR, VARIOS TESTS UTILIZAN LA MISMA LLAMADA
'''
def createBasicUser():
    userE = User.objects.create_user(username='awaisI', password='awaisawais', first_name="Awais", last_name="Iqbal")
    Profile(user=userE, question="hola?", answer="hola", postal_code="08019", level=1).save()

def createBasicUser2():
    userG = User.objects.create_user(username='ericR', password='ericR', first_name="Eric", last_name="Rodríguez")
    Profile(user=userG, question="hola?", answer="hola", postal_code="08019", level=1).save()

def populate():
    zoneA, _ = Zone.objects.get_or_create(pk="08181")
    zoneB, _ = Zone.objects.get_or_create(pk="08034")

    adm = User.objects.create_superuser('admin', 'admin@example.com', 'meetnrun')
    #Profile(user=adm, question="My question", answer="My answer", postal_code=zoneA, level=2).save()

    userA = User.objects.create_user(username='alejandroA', password='alejandroA', first_name="Alejandro",
                                 last_name="Agustin")
    Profile(user=userA, question="My question", answer="My answer", postal_code=zoneA, level=0).save()
    userB = User.objects.create_user(username='javierA', password='javierA', first_name="Javier", last_name="Alemán")
    Profile(user=userB, question="My question", answer="My answer", postal_code=zoneA, level=0).save()
    userC = User.objects.create_user(username='guillemC', password='guillemC', first_name="Guillem", last_name="Castro")
    Profile(user=userC, question="My question", answer="My answer", postal_code=zoneB, level=0).save()
    userD = User.objects.create_user(username='monicaF', password='monicaF', first_name="Mònica", last_name="Follana")
    Profile(user=userD, question="My question", answer="My answer", postal_code=zoneB, level=0).save()
    userE = User.objects.create_user(username='awaisI', password='awaisI', first_name="Awais", last_name="Iqbal")
    Profile(user=userE, question="My question", answer="My answer", postal_code=zoneB, level=0).save()
    userF = User.objects.create_user(username='marcP', password='marcP', first_name=zoneB, last_name="Paricio")
    Profile(user=userF, question="My question", answer="My answer", postal_code=zoneB, level=0).save()
    userG = User.objects.create_user(username='ericR', password='ericR', first_name="Eric", last_name="Rodríguez")
    Profile(user=userG, question="My question", answer="My answer", postal_code=zoneB, level=0).save()



    Friendship(creator=userA, friend=userB).save()
    Friendship(creator=userA, friend=userC).save()
    Friendship(creator=userC, friend=userA).save()
    Friendship(creator=userD, friend=userA).save()
    Friendship(creator=userE, friend=userF).save()
    Friendship(creator=userE, friend=userG).save()

    meetingA = Meeting(owner=userA, title="Sortida pel marenostrum", public=True, level=2, latitude="41.488576",
                   longitude="2.21284", date=(timezone.now() + timedelta(days=2)))
    meetingA.save()
    meetingA.participants.add(userB)

    meetingB = Meeting(owner=userA, title="Guanta", public=True, level=1, latitude="41.388576",
                   longitude="2.11284", date=(timezone.now() + timedelta(days=3)))
    meetingA.save()
    meetingA.participants.add(userB, userC, userD, userE, userF)

    meetingC = Meeting(owner=userB, title="N'em a corre per l'eixample", public=False, level=0, latitude="41.378576",
                   longitude="2.01284", date=(timezone.now() + timedelta(days=2))).save()

if __name__ == "__main__":
    populate()