import unittest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from quedadas.models import Meeting


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
