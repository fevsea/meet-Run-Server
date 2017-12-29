import unittest
from collections import OrderedDict

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from quedadas.models import Meeting
from rest_framework.authtoken.models import Token
from populateDB import populate
import collections

class MeetingsTests(APITestCase):
    @unittest.skip("demonstrating skipping")
    def test_create_meeting(self):
        """
        Ensure we can create a new meeting object.
        """
        url = reverse('meeting_list')
        data = {"title": "Quedada1",
                "description": "",
                "public": False,
                "level": 1,
                "date": "2017-10-18T09:03:39Z",
                "latitude": "1.34",
                "longitude": "41.21"}

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 1)
        self.assertEqual(Meeting.objects.get().title, 'Quedada1')

class MeetingsTests(APITestCase):
    def setUp(self):
        populate()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

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
        response = self.client.post(
            reverse('meeting_list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp = {
            'id': 3,
            'title': 'Testing Meeting',
            'description': 'bla bla bla',
            'public': False,
            'level': 1,
            'date': '2017-11-28T10:52:39Z',
            'latitude': '41.388576',
            'longitude': '2.11284',
            'owner': OrderedDict({
                'id': 6,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08034',
                'question': 'My question',
                'level': 1
        }),
            'chat' : None
        }
        self.assertEqual(response.data, resp)

    def test_create_invalid_notitle_meeting(self):
        self.valid_payload = {
            "description": "bla bla bla",
            "public": False,
            "level": 1,
            "date": "2017-11-28T10:52:39",
            "latitude": "41.388576",
            "longitude": "2.11284",
            "chat": None
        }
        response = self.client.post(
            reverse('meeting_list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp = {
            'title' : ['This field is required.']
        }
        self.assertEqual(response.data, resp)




        expectedRespJson = {}
        expectedRespJson['id'] = 3
        expectedRespJson['title'] = 'Testing Meeting'
        expectedRespJson['description'] = 'bla bla bla'
        expectedRespJson['public'] = False
        expectedRespJson['level'] = 1
        expectedRespJson['date'] = '2017-11-28T10:52:39Z'
        expectedRespJson['latitude'] = '41.388576'
        expectedRespJson['longitude'] = '2.11284'
        expectedRespJson['owner'] = repr({'id': 6,'username' : 'awaisI', 'first_name' : 'Awais', 'last_name' : 'Iqbal', 'postal_code': '08019', 'question' : 'My question', 'level' : '1'})
        expectedRespJson['chat'] = None
        expectedResp = {
            'id': 3,
            'title': 'Testing Meeting',
            "description": "bla bla bla",
            "public": False,
            "level": 1,
            "date": "2017-11-28T10:52:39",
            "latitude": "41.388576",
            "longitude": "2.11284",
            'owner' : {
                'id': 6,
                'username': 'awaisI',
                'first_name': 'Awais',
                'last_name': 'Iqbal',
                'postal_code': '08019',
                'question': 'My question',
                'level': '1'
            },
            expectedRespJson['chat'] : None
        }

