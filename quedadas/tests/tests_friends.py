from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from populateDB import create_basic_user
from populateDB import create_basic_user_2


class FriendsTests(APITestCase):
    def setUp(self):
        pass

    def test_add_friend(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()
        create_basic_user_2()
        response = self.client.post(
            reverse('friends', kwargs={'pk': 2}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobar que se ha creado la solicitud

        response2 = self.client.get(
            reverse('friends', kwargs={'pk': 2}),
            data={'accepted': False}
        )
        self.assertEqual(response2.data['count'], 1)  # comprobar que se ha creado la solicitud y no esta aceptada

        self.user = User.objects.get(username='ericR')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        response = self.client.post(  # aceptar la solicitud
            reverse('friends', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)  # comprobar que se ha creado la solicitud

        response2 = self.client.get(
            reverse('friends', kwargs={'pk': 1}),
            data={'accepted': True}
        )
        self.assertEqual(response2.data['count'], 1)  # comprobar que se ha aceptado la solicitud

        response2 = self.client.get(
            reverse('friends', kwargs={'pk': 1}),
            data={'accepted': False}
        )
        self.assertEqual(response2.data['count'], 0)  # comprobar que ya no hay solicitudes pendientes

        response = self.client.delete(  # eliminar amistad
            reverse('friends', kwargs={'pk': 1}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)  # comprobar que se ha borrado

        response2 = self.client.get(
            reverse('friends', kwargs={'pk': 1}),
            data={'accepted': True}
        )
        self.assertEqual(response2.data['count'], 1)  # comprobar que se ha aceptado la solicitud

        response2 = self.client.get(
            reverse('friends', kwargs={'pk': 1}),
            data={'accepted': False}
        )
        self.assertEqual(response2.data['count'], 0)  # comprobar que ya no hay solicitudes pendientes

    def test_add_friend_no_exists(self):
        create_basic_user()
        self.user = User.objects.get(username='awaisI')
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        token.save()

        response = self.client.post(
            reverse('friends', kwargs={'pk': 2}),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
