import unittest
from collections import OrderedDict
import unittest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from populateDB import createBasicUser
from populateDB import createBasicUser2
from populateDB import createBasicUserMeeting


class MeetingsTests(APITestCase):
    def setUp(self):
        '''populate()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()'''

    def test_create_valid_chat_with_meeting(self):
        createBasicUserMeeting()
        createBasicUser2()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        ''' COmprobamos que la lista este vacia'''
        response = self.client.get(
            reverse('chat-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0) #comprobamos que no hay ningún chat en la base de datos

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1,2],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        ''' Creamos un chat'''
        response = self.client.post(
            reverse('chat-list'),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #comprobamos la respuesta de que se ha creado
        resp = {
            'pk': 1,
            'chatName': 'Chat1',
            'listUsersChat': [
                OrderedDict([  # cada usuario es un orderedDict
                    ('id', 1),
                    ('username', 'awaisI'),
                    ('first_name', 'Awais'),
                    ('last_name', 'Iqbal'),
                    ('postal_code', '08019'),
                    ('question', 'hola?'),
                    ('level', 1),
                ]),
                OrderedDict([
                    ('id', 2),
                    ('username', 'ericR'),
                    ('first_name', 'Eric'),
                    ('last_name', 'Rodríguez'),
                    ('postal_code', '08019'),
                    ('question', 'hola?'),
                    ('level', 1)
                ])
            ],
            'type': 1,
            'meeting': OrderedDict([  # cada usuario es un orderedDict
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
                     ('chat', 1)
                 ]),
            'lastMessage': 'Hola',
            'lastMessageUserName': 0,
            'lastDateTime': '2017-11-28T10:52:39Z'
        }
        self.assertEqual(response.data, resp) #comrpobamos el formato retornado en Json

        ''' Miramos que se pueda acceder al chat'''
        response = self.client.get (
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, resp) #comprobamos que la respuesta sea correcta

        ''' Miramos la lista con 1 chat'''
        response = self.client.get(
            reverse('chat-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # comprobamos que no hay ningún chat en la base de datos

        resp = OrderedDict([
            ('count',1),
            ('next',None),
            ('previous', None),
            ('results',[
                OrderedDict([
                    ('pk', 1),
                    ('chatName', 'Chat1'),
                    ('listUsersChat', [
                        OrderedDict([  # cada usuario es un orderedDict
                            ('id', 1),
                            ('username', 'awaisI'),
                            ('first_name', 'Awais'),
                            ('last_name', 'Iqbal'),
                            ('postal_code', '08019'),
                            ('question', 'hola?'),
                            ('level', 1),
                        ]),
                        OrderedDict([
                            ('id', 2),
                            ('username', 'ericR'),
                            ('first_name', 'Eric'),
                            ('last_name', 'Rodríguez'),
                            ('postal_code', '08019'),
                            ('question', 'hola?'),
                            ('level', 1)
                        ])
                    ]),
                    ('type', 1),
                    ( 'meeting',
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
                            ('chat', 1)
                        ])
                    ),
                    ('lastMessage', 'Hola'),
                    ('lastMessageUserName', 0),
                    ('lastDateTime', '2017-11-28T10:52:39Z')

                ])]
            )
        ]) #respuesta esperada solicitando la lista
        self.assertEqual(response.data,resp) #comprobamos los campos que se devuelven
        ''' Borramos el chat'''
        response = self.client.delete(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # comprobamos la respuesta de que se ha creado

        ''' No se encuentra el chat'''
        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        ''' Miramos que la lista este vacia'''
        response = self.client.get(
            reverse('chat-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)  # comprobamos que no hay ningún chat en la base de datos



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

