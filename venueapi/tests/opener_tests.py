import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from venueapi.models import Opener, Band, Concert
from django.contrib.auth.models import User

class OpenerTests(APITestCase):

    fixtures = ['users', 'tokens', 'bands', 'concerts', 'openers']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_create_opener(self):

        url = "/openers"
        data = {
            "band": 1,
            "concert": 1
        }

        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['band'], 1)
        self.assertEqual(json_response['concert'], 1)