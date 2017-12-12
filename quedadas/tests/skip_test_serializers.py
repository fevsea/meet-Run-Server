# coding=utf-8
import unittest

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from quedadas.serializers import UserSerializer


class SkeepUserTests(APITestCase):
    def setUp(self):
        pass
        # populate()

    @unittest.skip("demonstrating skipping")
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
