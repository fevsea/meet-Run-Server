from collections import OrderedDict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from populateDB import create_basic_user_2
from populateDB import create_basic_user_meeting


class ChatsTests(APITestCase):
    def setUp(self):
        create_basic_user_meeting()
        create_basic_user_2()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_create_delete_get_valid_chat_with_meeting(self):
        ''' COmprobamos que la lista este vacia'''
        response = self.client.get(
            reverse('chat-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)  # comprobamos que no hay ningún chat en la base de datos

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Miramos que se pueda acceder al chat'''
        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

        ''' Miramos la lista con 1 chat'''
        response = self.client.get(
            reverse('chat-list')
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)  # comprobamos que no hay ningún chat en la base de datos

        resp = OrderedDict([
            ('count', 1),
            ('next', None),
            ('previous', None),
            ('results', [
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
                    ('meeting',
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
        ])  # respuesta esperada solicitando la lista
        self.assertEqual(response.data, resp)  # comprobamos los campos que se devuelven
        ''' Borramos el chat'''
        response = self.client.delete(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)  # comprobamos la respuesta de que se ha creado

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

    def test_p2p_existing(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Comprobamos que la llamada devuelve el chat '''
        response = self.client.get(
            reverse('chat-p2p', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

    def test_p2p_not_found(self):
        ''' Comprobamos que la llamada devuelve el chat '''
        response = self.client.get(
            reverse('chat-p2p', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_chat_chatName(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat2",
            "listUsersChat": [1, 2],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobamos la respuesta de que se ha creado

        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp['chatName'] = "Chat2"
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

    def test_update_chat_listUsersChat(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobamos la respuesta de que se ha creado

        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

    def test_update_chat_not_existing_user(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2, 3],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # comprobamos la respuesta de que se ha creado

    def test_update_chat_last_message_userID_date(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Adios",
            "lastMessageUserName": 1,
            "lastDateTime": "2017-11-29T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobamos la respuesta de que se ha creado

        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp['lastMessage'] = "Adios"
        resp['lastMessageUserName'] = 1
        resp['lastDateTime'] = "2017-11-29T10:52:39Z"
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

    def test_update_chat_not_existing_meeting(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
            "type": 1,
            "meeting": 3,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # comprobamos la respuesta de que se ha creado

    def test_update_chat(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobamos la respuesta de que se ha creado

        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # resp[''] = ""
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta

    def test_update_chat(self):
        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
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
        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # comprobamos la respuesta de que se ha creado
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
        self.assertEqual(response.data, resp)  # comrpobamos el formato retornado en Json

        ''' Hacemos el update'''

        self.valid_payload = {
            "chatName": "Chat1",
            "listUsersChat": [1, 2],
            "type": 1,
            "meeting": 1,
            "lastMessage": "Hola",
            "lastMessageUserName": 0,
            "lastDateTime": "2017-11-28T10:52:39"
        }
        response = self.client.put(
            reverse('chat-detail', kwargs={'pk': 1}),
            data=self.valid_payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobamos la respuesta de que se ha creado

        response = self.client.get(
            reverse('chat-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # resp[''] = ""
        self.assertEqual(response.data, resp)  # comprobamos que la respuesta sea correcta
