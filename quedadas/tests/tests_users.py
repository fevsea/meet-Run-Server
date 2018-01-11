from collections import OrderedDict

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from populateDB import create_basic_user


class UsersTests(APITestCase):
    def setUp(self):
        '''populate()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()'''

    def test_register_user_valid(self):
        self.valid_payload = {
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "password": "awaisawais",
            "postal_code": "08019",
            "question": "hola?",
            "answer": "hola",
            "level": 2
        }

        response = self.client.post(
            reverse('user-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        resp = {
            'id': 1,
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "password": "pbkdf2_sha256$30000$zOhtdyJpxhqR$QGJSYx/Vk+0qQm7CrFDt/1T2UoZpvY/aA2d4h5oIF7s=",
            "postal_code": "08019",
            "question": "hola?",
            "answer": "hola",
            "level": 2
        }
        self.assertEqual(response.data['id'], 1)
        self.assertEqual(response.data['username'], 'awaisI')
        self.assertEqual(response.data['first_name'], 'Awais')
        self.assertEqual(response.data['last_name'], 'Iqbal')
        self.assertEqual(response.data['postal_code'], '08019')
        self.assertEqual(response.data['question'], 'hola?')
        self.assertEqual(response.data['answer'], 'hola')
        self.assertEqual(response.data['level'], 2)
        self.assertIsNotNone(response.data['password'])

    def test_register_user_repeated_username(self):
        self.valid_payload = {
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "password": "awaisawais",
            "postal_code": "08019",
            "question": "hola?",
            "answer": "hola",
            "level": 2
        }

        self.client.post(
            reverse('user-list'),
            data=self.valid_payload,
            format='json'
        )
        response = self.client.post(
            reverse('user-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp = {
            "username": ["A user with that username already exists."]
        }
        self.assertEqual(response.data, resp)

    def test_register_user_empty_creation(self):
        self.valid_payload = {
            "username": "",
            "first_name": "",
            "last_name": "",
            "password": "",
            "postal_code": "",
            "question": "",
            "answer": "",
            "level": None
        }

        response = self.client.post(
            reverse('user-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        resp = {
            "username": ["This field may not be blank."],
            "password": ["This field may not be blank."],
            "postal_code": ["This field may not be blank."],
            "question": ["This field may not be blank."],
            "answer": ["This field may not be blank."],
            "level": ["This field may not be null."],

        }
        self.assertEqual(response.data, resp)

    def test_get_user(self):
        create_basic_user()
        response = self.client.get(
            reverse('user-detail', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "postal_code": "08019",
            "question": "hola?",
            "level": 1
        }
        self.assertEqual(response.data, resp)

    def test_get_users(self):
        create_basic_user()
        response = self.client.get(
            reverse('user-list'),
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
                     ('username', 'awaisI'),
                     ('first_name', 'Awais'),
                     ('last_name', 'Iqbal'),
                     ('postal_code', '08019'),
                     ('question', 'hola?'),
                     ('level', 1),
                 ])
             ]
             )
        ])
        self.assertEqual(response.data, resp)

    def test_update_user(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        self.valid_payload = {
            "username": "awaisI2",
            "first_name": "Awais2",
            "last_name": "Iqbal2",
            "postal_code": "08020",
            "question": "hola?",
            "level": 3
        }
        response = self.client.patch(
            reverse('user-detail', kwargs={'pk': 1}),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            "username": "awaisI2",
            "first_name": "Awais2",
            "last_name": "Iqbal2",
            "postal_code": "08020",
            "question": "hola?",
            "level": 3
        }
        self.assertEqual(response.data, resp)

    def test_delete_user(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        response = self.client.delete(
            reverse('user-detail', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_current_user(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()
        response = self.client.get(
            reverse('current-user'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'id': 1,
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "postal_code": "08019",
            "question": "hola?",
            "level": 1
        }
        self.assertEqual(response.data, resp)

    def test_change_password(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()
        self.valid_payload = {
            "old": "awaisawais",
            "new": "blabla"
        }

        response = self.client.post(
            reverse('change-password'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.valid_payload = {
            "username": "awaisI",
            "password": "awaisawais"
        }
        response = self.client.post(
            reverse('user-login'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_get_firebase_token(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()
        tok = "14f56ds12g56d1s56f1ds651f56ds1g56ds15f6ds156"
        self.valid_payload = {
            "token": tok
        }
        response = self.client.post(
            reverse('token'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(
            reverse('token'),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        resp = {
            'token': tok
        }
        self.assertEqual(response.data, resp)
