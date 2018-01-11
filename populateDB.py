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


def create_basic_user():
    zone_a, _ = Zone.objects.get_or_create(pk="08019")
    user_e = User.objects.create_user(username='awaisI', password='awaisawais', first_name="Awais", last_name="Iqbal")
    Profile(user=user_e, question="hola?", answer="hola", postal_code=zone_a, level=1).save()


def create_basic_user_2():
    zone_a, _ = Zone.objects.get_or_create(pk="08019")
    user_g = User.objects.create_user(username='ericR', password='ericR', first_name="Eric", last_name="Rodríguez")
    Profile(user=user_g, question="hola?", answer="hola", postal_code=zone_a, level=1).save()


def create_basic_user_meeting():
    zone_a, _ = Zone.objects.get_or_create(pk="08019")
    user_e = User.objects.create_user(username='awaisI', password='awaisawais', first_name="Awais", last_name="Iqbal")
    Profile(user=user_e, question="hola?", answer="hola", postal_code=zone_a, level=1).save()
    meeting_a = Meeting(owner=user_e, description="bla bla bla", title="Testing Meeting", public=False, level=1,
                        latitude="41.388576", longitude="2.11284", date="2017-11-28T10:52:39")
    meeting_a.save()


def populate():
    zone_a, _ = Zone.objects.get_or_create(pk="08181")
    zone_b, _ = Zone.objects.get_or_create(pk="08034")

    User.objects.create_superuser('admin', 'admin@example.com', 'meetnrun')

    user_a = User.objects.create_user(username='alejandroA', password='alejandroA', first_name="Alejandro",
                                      last_name="Agustin")
    Profile(user=user_a, question="My question", answer="My answer", postal_code=zone_a, level=0).save()
    user_b = User.objects.create_user(username='javierA', password='javierA', first_name="Javier", last_name="Alemán")
    Profile(user=user_b, question="My question", answer="My answer", postal_code=zone_a, level=0).save()
    user_c = User.objects.create_user(username='guillemC', password='guillemC', first_name="Guille", last_name="Castro")
    Profile(user=user_c, question="My question", answer="My answer", postal_code=zone_b, level=0).save()
    user_d = User.objects.create_user(username='monicaF', password='monicaF', first_name="Mònica", last_name="Follana")
    Profile(user=user_d, question="My question", answer="My answer", postal_code=zone_b, level=0).save()
    user_e = User.objects.create_user(username='awaisI', password='awaisI', first_name="Awais", last_name="Iqbal")
    Profile(user=user_e, question="My question", answer="My answer", postal_code=zone_b, level=0).save()
    user_f = User.objects.create_user(username='marcP', password='marcP', first_name=zone_b, last_name="Paricio")
    Profile(user=user_f, question="My question", answer="My answer", postal_code=zone_b, level=0).save()
    user_g = User.objects.create_user(username='ericR', password='ericR', first_name="Eric", last_name="Rodríguez")
    Profile(user=user_g, question="My question", answer="My answer", postal_code=zone_b, level=0).save()

    Friendship(creator=user_a, friend=user_b).save()
    Friendship(creator=user_a, friend=user_c).save()
    Friendship(creator=user_c, friend=user_a).save()
    Friendship(creator=user_d, friend=user_a).save()
    Friendship(creator=user_e, friend=user_f).save()
    Friendship(creator=user_e, friend=user_g).save()

    meeting_a = Meeting(owner=user_a, title="Sortida pel marenostrum", public=True, level=2, latitude="41.488576",
                        longitude="2.21284", date=(timezone.now() + timedelta(days=2)))
    meeting_a.save()
    meeting_a.participants.add(user_b)

    Meeting(owner=user_a, title="Guanta", public=True, level=1, latitude="41.388576",
            longitude="2.11284", date=(timezone.now() + timedelta(days=3)))
    meeting_a.save()
    meeting_a.participants.add(user_b, user_c, user_d, user_e, user_f)

    Meeting(owner=user_b, title="N'em a corre per l'eixample", public=False, level=0, latitude="41.378576",
            longitude="2.01284", date=(timezone.now() + timedelta(days=2))).save()


if __name__ == "__main__":
    populate()
