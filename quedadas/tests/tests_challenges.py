from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from populateDB import create_basic_user
from populateDB import create_basic_user_2


class FriendsTests(APITestCase):
    def setUp(self):
        '''populate()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()'''

    def test_create_challenge(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()
        create_basic_user_2()

        self.valid_payload = {
            "creator": 1,
            "challenged": 2,
            "distance": 3,
            "deadline": "2018-11-28T10:52:00"
        }
        response = self.client.post(
            reverse('challenge-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobar que se ha creado la solicitud

        createdChallengeID = response.data['id']
        response2 = self.client.get(
            reverse('challenge-detail', kwargs={'pk': createdChallengeID})
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)  # miramos que existe la solicitud
        self.assertIsNotNone(response2.data['id'])  # comprobar que  hay contenido en el Challenge
        self.assertEqual(response2.data['accepted'], False)

        '''Cambiamos de usuario'''
        self.user = User.objects.get(username='ericR')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        response = self.client.post(  # aceptar la solicitud
            reverse('challenge-detail', kwargs={'pk': createdChallengeID})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)  # comprobar que se ha creado la solicitud

        response2 = self.client.get(
            reverse('challenge-detail', kwargs={'pk': createdChallengeID})
        )
        self.assertEqual(response2.status_code, status.HTTP_200_OK)  # miramos que existe la solicitud
        self.assertEqual(response2.data['id'], createdChallengeID)  # comprobar que  hay contenido en el Challenge
        self.assertEqual(response2.data['accepted'], True)
        # TODO hace falta comprobar todo el contenido ?


        response2 = self.client.get(
            reverse('challenge-list')
        )
        self.assertEqual(response2.data[0]['id'], 1)
        resp = {
            'id': 1,
            "username": "awaisI",
            "first_name": "Awais",
            "last_name": "Iqbal",
            "postal_code": "08019",
            "question": "hola?",
            "level": 1
        }
        self.assertEqual(response2.data[0]['creator'], resp)
        resp = {
            'id': 2,
            "username": "ericR",
            "first_name": "Eric",
            "last_name": "Rodríguez",
            "postal_code": "08019",
            "question": "hola?",
            "level": 1
        }
        self.assertEqual(response2.data[0]['challenged'], resp)
        self.assertEqual(response2.data[0]['distance'], 3)
        self.assertEqual(response2.data[0]['deadline'], "2018-11-28T10:52:00Z")
        self.assertEqual(response2.data[0]['creator_distance'], 0.0)
        self.assertEqual(response2.data[0]['challenged_distance'], 0.0)
        self.assertEqual(response2.data[0]['accepted'], True)
        self.assertEqual(response2.data[0]['completed'], False)

        response = self.client.delete(  # eliminar amistad
            reverse('challenge-detail', kwargs={'pk': createdChallengeID})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # comprobar que se ha borrado

        response2 = self.client.get(
            reverse('challenge-detail', kwargs={'pk': createdChallengeID})
        )
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)  # miramos que existe la solicitud

    def test_no_exists_challenge(self):
        response2 = self.client.get(
            reverse('challenge-detail', kwargs={'pk': 1})
        )
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)  # miramos que existe la solicitud

    def test_userB_no_exists(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        self.valid_payload = {
            "creator": 1,
            "challenged": 2,
            "distance": 3,
            "deadline": "2018-11-28T10:52:00"
        }
        response = self.client.post(
            reverse('challenge-list'),
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)  # comprobar que se ha creado la solicitud
