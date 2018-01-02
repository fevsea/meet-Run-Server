import unittest
from collections import OrderedDict
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from populateDB import createBasicUser
from populateDB import createBasicUserMeeting


class MeetingsTests(APITestCase):
    def setUp(self):
        '''populate()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()'''

    def test_create_valid_meeting(self):
        self.valid_payload = {
            "title": "Testing Meeting",
            "description": "bla bla bla",
            "public": False,
            "level": 1,
            "date": "2017-11-28T10:52:39",
            "latitude": "41.388576",
            "longitude": "2.11284",
            "chat": None
        }
        createBasicUser()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            reverse('meeting_list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
        }),
            'chat' : None
        }
        self.assertEqual(response.data, resp)

    def test_create_empty_meeting(self):
        self.valid_payload = {
            "title": "",
            "description": "",
            "public": False,
            "level": None,
            "date": None,
            "latitude": "",
            "longitude": "",
            "chat": None
        }
        createBasicUser()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            reverse('meeting_list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp = {
            'title' : [
                "This field may not be blank."
            ],
            'level': [
                "This field may not be null."
            ],
            'date': [
                "This field may not be null."
            ],
            'latitude': [
                "This field may not be blank."
            ],
            'longitude': [
                "This field may not be blank."
            ]
        }
        self.assertEqual(response.data, resp)

    def test_get_meeting(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_title(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "title": "awaisI2",
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'awaisI2',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_description(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "description": "desc2",
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'desc2',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_public(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "public": True,
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': True,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_level(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "level": 2,
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 2,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_date(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "datet": "2017-12-28T10:52:39Z",
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_lat(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "latitude": "42.388576",
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '42.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_update_meeting_lon(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        self.valid_payload = {
            "longitude": "2.19984",
        }
        response = self.client.patch(
            reverse('meeting_detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.19984',
            'owner': OrderedDict({
                'id': 1,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'hola?',
                'level': 1
            }),
            'chat': None
        }
        self.assertEqual(response.data, resp)

    def test_delete_meeting(self):
        createBasicUserMeeting()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            reverse('meeting_detail', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            reverse('meeting_detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_meetings(self):
        createBasicUserMeeting()
        response = self.client.get(
            reverse('meeting_list'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = OrderedDict([
            ('count', 1),
            ('next', None),
            ('previous', None),
            ('results',
             [  # array de usuarios
                 OrderedDict([  # cada usuario es un orderedDict
                     ('id', 1),
                     ('title', 'Testing Meeting'),
                     ('description', 'bla bla bla'),
                     ('public', False),
                     ('level', 1),
                     ('date', '2017-11-28T10:52:39Z'),
                     ('latitude', '41.388576'),
                     ('longitude', '2.11284'),
                     ('owner',
                        OrderedDict([  # cada usuario es un orderedDict
                            ('id', 1),
                            ('username', 'awaisI'),
                            ('first_name', 'Awais'),
                            ('last_name', 'Iqbal'),
                            ('postal_code', '08019'),
                            ('question', 'hola?'),
                            ('level', 1)
                        ])
                     ),
                     ('chat', None)
                 ])
             ]
             )
        ])
        self.assertEqual(response.data, resp)
