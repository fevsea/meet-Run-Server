# coding=utf-8
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from populateDB import populate
from quedadas.models import Profile
from quedadas.serializers import UserSerializerDetail, UserSerializer


class UserTests(APITestCase):
    def setUp(self):
        populate()

    def test_serialize_one_user(self):
        """
        Serialization of one user
        """
        u = User.objects.get(pk=2)
        serialized = UserSerializer(u, many=False)
        res = """
        {
            'id': 2,
            'username': 'alejandroA',
            'first_name': 'Alejandro',
            'last_name': 'Agustin',
            'postal_code': '08181',
            'question': 'My question',
            'level': 2
        }
        """.replace('\n', '').replace(' ', '')

        self.assertEqual(str(serialized.data).replace(' ', ''), res)
